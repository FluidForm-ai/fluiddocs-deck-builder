#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
structural_check.py

Non-visual integrity validator for a built deck. Runs WITHOUT a browser,
safe fallback when Playwright is unavailable (no disk space for a chromium
download, offline sandbox, CI without a browser).

Checks the shipped HTML file against a set of mechanical rules that catch
roughly 80% of real defects without needing a screenshot:

    1. Slide count matches the expected spine
    2. No raw emoji / unintended Unicode glyphs (only the allowlisted set)
    3. No dangling era text in the prose (e.g. "Page 14 of 22")
    4. No broken internal anchors (#id references that don't resolve)
    5. All base64 data URLs parse cleanly (no truncated blobs)
    6. No duplicate element IDs
    7. Cover slide has both panel-left and panel-right (split-panel sanity)

Exit code is 0 if all checks pass, 1 if any hard check fails, 2 on script
error (bad args, missing file).

Usage:
    python structural_check.py <html-path> [--expected-slides N] [--verbose]
"""

from __future__ import annotations

import argparse
import base64
import re
import sys
from pathlib import Path
from typing import Iterable, Optional


# Codepoints we ALLOW to appear as literal characters (punctuation, separators).
ALLOWED_CHARS = {
    chr(0x00B7),  # middle dot
    chr(0x2013),  # en dash
    chr(0x2014),  # em dash
    chr(0x2026),  # ellipsis
    chr(0x201A),  # single low-9 quote
    chr(0x201E),  # double low-9 quote
    chr(0x201C),  # left double quote
    chr(0x201D),  # right double quote
    chr(0x201F),  # double high-reversed-9 quote
    chr(0x2018),  # left single quote
    chr(0x2019),  # right single quote
    chr(0x00AB),  # left guillemet
    chr(0x00BB),  # right guillemet
    chr(0x2039),  # single left guillemet
    chr(0x203A),  # single right guillemet
    chr(0x2010),  # hyphen
    chr(0x2011),  # non-breaking hyphen
    chr(0x2012),  # figure dash
    chr(0x2192),  # right arrow
    chr(0x2190),  # left arrow
    chr(0x2191),  # up arrow
    chr(0x2193),  # down arrow
}
EMOJI_RANGES = [
    (0x2600, 0x27BF),  # Misc symbols + dingbats
    (0x1F300, 0x1FAFF),  # All "real" emoji blocks
    (0x2700, 0x27BF),
]
ALLOWED_SYMBOLS = {"▱", "▰", "▪", "▫", "●", "○", "■", "□"}


def check_slide_count(html: str, expected: Optional[int]) -> list[str]:
    slides = re.findall(r'<section\s+class="slide[^"]*"', html)
    count = len(slides)
    issues = []
    if expected is not None and count != expected:
        issues.append(f"slide count: got {count}, expected {expected}")
    if count < 5:
        issues.append(f"slide count: only {count} slides, suspiciously low for a pitch deck")
    return issues


def check_emoji(html: str) -> list[str]:
    issues = []
    for i, ch in enumerate(html):
        code = ord(ch)
        if ch in ALLOWED_CHARS or ch in ALLOWED_SYMBOLS:
            continue
        for lo, hi in EMOJI_RANGES:
            if lo <= code <= hi:
                ctx = html[max(0, i - 50):i + 40].replace("\n", " ")
                issues.append(f"emoji codepoint U+{code:04X} at byte {i} in context: ... {ctx} ...")
                break
    return issues


def check_duplicate_ids(html: str) -> list[str]:
    ids = re.findall(r'\sid="([^"]+)"', html)
    seen: dict[str, int] = {}
    dupes: list[str] = []
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    for i, n in seen.items():
        if n > 1:
            dupes.append(f"duplicate id '{i}' used {n} times")
    return dupes


def check_anchor_integrity(html: str) -> list[str]:
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    hrefs = re.findall(r'href="#([^"]+)"', html)
    issues = []
    for h in hrefs:
        if h and h not in ids:
            issues.append(f"anchor href=#{h} has no matching id")
    return issues


def check_base64_blobs(html: str) -> list[str]:
    blobs = re.findall(r'data:image/(?:png|jpeg|jpg|gif|svg\+xml);base64,([A-Za-z0-9+/=]+)', html)
    issues = []
    for idx, b in enumerate(blobs):
        if len(b) < 200:
            issues.append(f"base64 blob #{idx + 1} is {len(b)} chars, likely truncated or placeholder")
            continue
        if len(b) % 4 != 0:
            issues.append(f"base64 blob #{idx + 1} has bad length {len(b)} (not multiple of 4)")
            continue
        try:
            base64.b64decode(b, validate=True)
        except Exception as e:  # noqa: BLE001
            issues.append(f"base64 blob #{idx + 1} failed to decode: {e}")
    return issues


def check_era_fragments(html: str) -> list[str]:
    """Catch page numbers like 'Page 14 of 22' that leaked from the source."""
    scrubbed = re.sub(r'/\*.*?\*/', ' ', html, flags=re.DOTALL)
    scrubbed = re.sub(r'<!--.*?-->', ' ', scrubbed, flags=re.DOTALL)

    patterns = [
        r'Page\s+\d+\s+of\s+\d+',
        r'Slide\s+\d+\s*/\s*\d+\b',
        r'\bConfidential\s+,?\s*Page',
    ]
    issues = []
    for p in patterns:
        for m in re.finditer(p, scrubbed, re.IGNORECASE):
            ctx = scrubbed[max(0, m.start() - 40):m.end() + 40]
            issues.append(f"era fragment '{m.group()}' in context: {ctx!r}")
    return issues


def check_cover_panels(html: str) -> list[str]:
    m = re.search(r'<section class="slide s-cover[^"]*"[^>]*>(.*?)</section>', html, re.DOTALL)
    if not m:
        return []
    cover_body = m.group(1)
    issues = []
    if 'panel-left' in cover_body or 'panel-right' in cover_body:
        if 'panel-left' not in cover_body:
            issues.append("cover slide: panel-right present but no panel-left")
        if 'panel-right' not in cover_body:
            issues.append("cover slide: panel-left present but no panel-right")
    return issues


def run(html_path: Path, expected_slides: Optional[int] = None, verbose: bool = False) -> int:
    if not html_path.exists():
        sys.stderr.write(f"File not found: {html_path}\n")
        return 2

    html = html_path.read_text()
    print(f"== Structural check: {html_path}  ({len(html) // 1024} KB) ==")

    checks = [
        ("slide count", lambda: check_slide_count(html, expected_slides)),
        ("emoji codepoints", lambda: check_emoji(html)),
        ("duplicate ids", lambda: check_duplicate_ids(html)),
        ("anchor integrity", lambda: check_anchor_integrity(html)),
        ("base64 blobs", lambda: check_base64_blobs(html)),
        ("era fragments", lambda: check_era_fragments(html)),
        ("cover-panel sanity", lambda: check_cover_panels(html)),
    ]

    total_issues = 0
    for name, fn in checks:
        issues = fn()
        if issues:
            total_issues += len(issues)
            print(f"\n[FAIL] {name}, {len(issues)} issue(s):")
            for msg in issues[:10]:
                print(f"   - {msg}")
            if len(issues) > 10:
                print(f"   ... ({len(issues) - 10} more suppressed; pass --verbose for full list)")
                if verbose:
                    for msg in issues[10:]:
                        print(f"   - {msg}")
        else:
            print(f"[ok]   {name}")

    print()
    if total_issues == 0:
        print("PASS: structural check clean.")
        return 0
    print(f"FAIL: {total_issues} issue(s) across {len([n for n,f in checks if f()])} check(s).")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run structural checks on a built deck HTML.")
    parser.add_argument("html_path", type=Path)
    parser.add_argument("--expected-slides", type=int, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    try:
        return run(args.html_path, args.expected_slides, args.verbose)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"Structural check failed to run: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
