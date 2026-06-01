#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
extract_deck_pdf.py

Phase 0 extraction script for the deck-import skill (PDF path).

Input: a PDF deck.
Output: extraction.json (text + font metadata + palette + image paths per page)
        + pages/page-NN.png (one high-res image per slide).

Usage:
    python extract_deck_pdf.py <pdf-path> --out /tmp/deck-import-<ts>/ [--force-ocr] [--image-dpi 150] [--max-pages 30]

The agent reads extraction.json, not the PDF directly. This script is the
deterministic layer; the agent is the reasoning layer. Keep it idempotent:
same PDF in, same JSON out.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
    from pypdf import PdfReader
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e.name}. Install with:\n"
        f"  pip install --break-system-packages pdfplumber pypdf pdf2image Pillow pytesseract scikit-learn\n"
    )
    sys.exit(2)

try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from detect_palette import dominant_colors_for_image, aggregate_palette
except ImportError:
    sys.stderr.write("detect_palette.py must be in the same directory as extract_deck_pdf.py\n")
    sys.exit(2)


@dataclass
class PageRecord:
    page_num: int
    text: str
    image_path: str
    image_dimensions: dict
    detected_font_families: list
    has_hero_image: bool
    dominant_palette: list


FONT_PREFIX_RE = re.compile(r"^[A-Z]{6}\+")
FONT_WEIGHT_SUFFIX_RE = re.compile(
    r"[-_ ]?(Thin|ExtraLight|Light|Regular|Medium|SemiBold|Bold|ExtraBold|Black"
    r"|Italic|Oblique)$",
    re.IGNORECASE,
)


def normalize_fontname(raw: str) -> str:
    if not raw:
        return ""
    name = FONT_PREFIX_RE.sub("", raw)
    prev = None
    while prev != name:
        prev = name
        name = FONT_WEIGHT_SUFFIX_RE.sub("", name)
    return name.strip()


def extract_text_and_fonts(page) -> tuple[str, list[str]]:
    text = page.extract_text() or ""
    fonts: set[str] = set()
    for char in page.chars:
        fontname = char.get("fontname", "")
        normalized = normalize_fontname(fontname)
        if normalized:
            fonts.add(normalized)
    return text, sorted(fonts)


def ocr_page_image(image: Image.Image) -> str:
    if not HAS_OCR:
        return ""
    try:
        return pytesseract.image_to_string(image)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"OCR failed for a page: {exc}\n")
        return ""


def has_hero_image_heuristic(image: Image.Image) -> bool:
    small = image.resize((200, 113))
    pixels = small.getdata()
    total = len(pixels)
    near_white = sum(1 for r, g, b, *_ in pixels if r > 240 and g > 240 and b > 240)
    non_white_ratio = 1 - (near_white / total)
    return non_white_ratio > 0.45


def extract_deck(
    pdf_path: Path,
    out_dir: Path,
    force_ocr: bool = False,
    image_dpi: int = 150,
    max_pages: int = 30,
) -> dict:
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    try:
        pypdf_reader = PdfReader(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        if "pycryptodome" in msg.lower() or "crypt" in msg.lower():
            raise RuntimeError(
                "This PDF appears to be encrypted. Install pycryptodome "
                "(`pip install --break-system-packages pycryptodome`) and "
                "retry, or ask the user for the password if it's "
                "password-protected."
            ) from exc
        raise
    if pypdf_reader.is_encrypted:
        try:
            pypdf_reader.decrypt("")
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "This PDF is password-protected. Ask the user for the "
                "password and re-run the extraction."
            ) from exc
    meta = pypdf_reader.metadata or {}
    page_count = len(pypdf_reader.pages)
    if page_count < 3:
        sys.stderr.write(
            f"WARNING: PDF has only {page_count} page(s). Pitch decks typically "
            f"have 10+ slides, verify this is the right PDF before proceeding.\n"
        )

    if page_count > max_pages:
        sys.stderr.write(
            f"WARNING: PDF has {page_count} pages, over max ({max_pages}). "
            f"Processing first {max_pages} only.\n"
        )
        page_count = max_pages

    page_images = convert_from_path(
        str(pdf_path),
        dpi=image_dpi,
        first_page=1,
        last_page=page_count,
    )

    first_img = page_images[0]
    w, h = first_img.size
    aspect = w / h if h else 1.0
    detected_aspect = _label_aspect(aspect)

    pages: list[PageRecord] = []
    was_ocr_fallback = False

    with pdfplumber.open(str(pdf_path)) as pdf:
        for i in range(page_count):
            pp_page = pdf.pages[i]
            pil_image = page_images[i]

            image_filename = f"page-{i + 1:02d}.png"
            image_full_path = pages_dir / image_filename
            pil_image.save(image_full_path, "PNG")

            if force_ocr:
                text = ocr_page_image(pil_image)
                fonts: list[str] = []
            else:
                text, fonts = extract_text_and_fonts(pp_page)
                if len(text.strip()) < 20 and HAS_OCR:
                    text = ocr_page_image(pil_image)
                    was_ocr_fallback = True
                    fonts = []

            hero = has_hero_image_heuristic(pil_image)
            palette = dominant_colors_for_image(pil_image, k=5, top_n=3)

            pages.append(
                PageRecord(
                    page_num=i + 1,
                    text=text,
                    image_path=str(image_full_path),
                    image_dimensions={"width": pil_image.width, "height": pil_image.height},
                    detected_font_families=fonts,
                    has_hero_image=hero,
                    dominant_palette=palette,
                )
            )

    all_fonts: dict[str, int] = {}
    for p in pages:
        for f in p.detected_font_families:
            all_fonts[f] = all_fonts.get(f, 0) + 1
    top_fonts = sorted(all_fonts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    dominant_font_families = [f for f, _ in top_fonts]

    aggregated_palette = aggregate_palette(
        [p.dominant_palette for p in pages], k=5, exclude_page_indices=_pages_to_exclude(pages)
    )

    hero_slides = [p.page_num for p in pages if p.has_hero_image]
    longest = max(pages, key=lambda p: len(p.text or ""), default=None)
    shortest = min(pages, key=lambda p: len(p.text or ""), default=None)

    result = {
        "source_pdf": str(pdf_path.resolve()),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "title": _safe_meta(meta, "/Title"),
            "author": _safe_meta(meta, "/Author"),
            "subject": _safe_meta(meta, "/Subject"),
            "creator": _safe_meta(meta, "/Creator"),
            "page_count": page_count,
            "detected_aspect_ratio": detected_aspect,
            "was_ocr_fallback": was_ocr_fallback,
            "was_encrypted": pypdf_reader.is_encrypted,
        },
        "pages": [asdict(p) for p in pages],
        "aggregated": {
            "dominant_palette_across_deck": aggregated_palette,
            "dominant_font_families": dominant_font_families,
            "slides_with_hero_images": hero_slides,
            "longest_text_slide": longest.page_num if longest else None,
            "shortest_text_slide": shortest.page_num if shortest else None,
        },
    }

    json_path = out_dir / "extraction.json"
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    return result


def _label_aspect(ratio: float) -> str:
    if 1.7 < ratio < 1.8:
        return "16:9"
    if 1.3 < ratio < 1.4:
        return "4:3"
    if 0.95 < ratio < 1.05:
        return "1:1"
    if 0.7 < ratio < 0.75:
        return "A4 / letter portrait"
    return f"{ratio:.2f}:1"


def _safe_meta(meta, key: str) -> Optional[str]:
    try:
        v = meta.get(key) if meta else None
        return str(v) if v else None
    except Exception:  # noqa: BLE001
        return None


def _pages_to_exclude(pages: list[PageRecord]) -> list[int]:
    if pages and pages[0].has_hero_image and len(pages[0].text.strip()) < 30:
        return [0]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text + images + palette from a deck PDF.")
    parser.add_argument("pdf_path", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--force-ocr", action="store_true")
    parser.add_argument("--image-dpi", type=int, default=150)
    parser.add_argument("--max-pages", type=int, default=30)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    try:
        result = extract_deck(
            pdf_path=args.pdf_path,
            out_dir=args.out,
            force_ocr=args.force_ocr,
            image_dpi=args.image_dpi,
            max_pages=args.max_pages,
        )
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"Extraction failed: {exc}\n")
        return 1

    print(f"Extracted {result['metadata']['page_count']} pages.")
    print(f"  JSON:   {args.out / 'extraction.json'}")
    print(f"  Images: {args.out / 'pages'}/")
    if result["metadata"]["was_ocr_fallback"]:
        print("  Note:   OCR fallback was used, lower role-classification confidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
