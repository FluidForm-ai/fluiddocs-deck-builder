#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
classify_slides.py

Phase 1 generic deck classifier, detects deck TYPE and per-slide ROLE.

This classifier handles the 5 OSS deck types:
pitch, sales, launch, keynote, all-hands.

Flow:
  1. For each deck type, score the deck against "type-signature" keywords
     (words that strongly indicate THIS type over others) + slide-count fit.
  2. Pick the winning type. Emit top 3 with scores so the confirmation block
     can show alternatives.
  3. Using the winning type's spine, classify each slide into a role.

Input:  extraction.json from extract_deck_pdf.py
        OR pptx-manifest.json from extract-pptx-only.py
        (both expose the same {pages|slides: [{page_num|slide_num, text|body_text, ...}]} shape after normalization).
Output: classification.json alongside the input, with
        deck_type, type_confidence, type_scores, pages[].

The vocabulary here mirrors `references/spine-tables.md`. If you change the
keyword tables, update the reference too, reviewers audit the classifier's
decisions against that document.

Runnable standalone:
    python classify_slides.py /tmp/deck-import-<ts>/extraction.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Spine definitions (5 OSS types)
# ---------------------------------------------------------------------------

SPINES: dict[str, dict] = {
    "pitch": {
        "spine": [
            "Cover", "Problem", "Why Now", "Solution", "Product", "Demo",
            "Market", "Business Model", "Traction", "Competition", "Moat",
            "GTM", "Team", "Ask",
        ],
        "target_count": 14,
        "tolerance": 3,
        "type_signatures": [
            ("use of funds", 8), ("we're raising", 7), ("seed round", 6),
            ("pre-seed", 6), ("series a", 4), ("series b", 4),
            ("tam", 5), ("sam", 5), ("som", 5),
            ("addressable market", 5), ("moat", 5),
            ("pitch deck", 6), ("pitch", 3),
        ],
        "role_keywords": {
            "Problem": [
                ("problem", 3), ("broken", 2), ("painful", 2), ("frustrated", 2),
                ("wastes", 2), ("manual", 1), ("inefficient", 2),
                ("users struggle", 3), ("pain point", 3), ("error-prone", 2),
            ],
            "Why Now": [
                ("why now", 5), ("inflection", 3), ("shift", 2),
                ("made possible by", 3), ("breakthrough", 2),
                ("for the first time", 3), ("enabled by", 3), ("timing", 2),
            ],
            "Solution": [
                ("solution", 3), ("introducing", 3), ("we built", 2),
                ("our approach", 2), ("we solve", 3), ("solves", 2),
                ("we help", 2), ("we enable", 2),
            ],
            "Product": [
                ("product", 2), ("features", 2), ("how it works", 3),
                ("built for", 1), ("workflow", 1), ("architecture", 2),
            ],
            "Demo": [
                ("demo", 4), ("live demo", 5), ("walkthrough", 3),
                ("see it in action", 4), ("product tour", 3),
            ],
            "Market": [
                ("tam", 5), ("sam", 4), ("som", 4), ("market size", 4),
                ("addressable market", 5), ("market opportunity", 4),
                ("total addressable", 5),
            ],
            "Business Model": [
                ("pricing", 3), ("revenue model", 4), ("unit economics", 4),
                ("gross margin", 4), ("arr", 3), ("mrr", 3),
                ("subscription", 2), ("ltv", 3), ("cac", 3),
                ("business model", 5), ("how we make money", 5),
            ],
            "Traction": [
                ("traction", 5), ("growth", 2), ("mom", 2), ("yoy", 2),
                ("waitlist", 2), ("paying customers", 3), ("since launch", 2),
                ("design partners", 3), ("loi", 3),
            ],
            "Competition": [
                ("competition", 4), ("competitors", 4), ("differentiation", 3),
                ("incumbents", 3), ("existing solutions", 3),
                ("competitive landscape", 5),
            ],
            "Moat": [
                ("moat", 5), ("defensible", 4), ("barrier to entry", 4),
                ("network effect", 4), ("flywheel", 3), ("data advantage", 3),
                ("switching cost", 3),
            ],
            "GTM": [
                ("go-to-market", 5), ("gtm", 4), ("distribution", 3),
                ("sales motion", 4), ("plg", 3), ("product-led", 3),
            ],
            "Team": [
                ("team", 3), ("founded by", 3), ("founders", 3),
                ("previously at", 2), ("years of experience", 2),
            ],
            "Ask": [
                ("ask", 4), ("raising", 4), ("seed round", 3),
                ("use of funds", 5), ("we're raising", 5), ("investment", 2),
            ],
        },
    },

    "sales": {
        "spine": [
            "Cover", "About You", "Problem", "Why Today", "Solution",
            "How It Works", "Proof", "ROI", "Implementation", "Pricing",
            "Next Steps",
        ],
        "target_count": 11,
        "tolerance": 2,
        "type_signatures": [
            ("next steps", 5), ("book a meeting", 5), ("proposal", 3),
            ("case study", 4), ("reference customer", 5), ("roi", 4),
            ("implementation plan", 5), ("cost savings", 3),
            ("return on investment", 5), ("sales deck", 6),
            ("customer deck", 6), ("why today", 5),
            ("why us", 3), ("pricing tier", 4), ("per seat per month", 4),
        ],
        "role_keywords": {
            "About You": [
                ("about you", 5), ("your team", 2), ("your company", 2),
                ("your industry", 3), ("your goals", 3), ("discovery", 3),
            ],
            "Problem": [
                ("your challenge", 4), ("pain point", 4), ("struggling with", 3),
                ("the problem", 3), ("today's reality", 3),
            ],
            "Why Today": [
                ("why today", 5), ("why now", 4), ("cost of delay", 4),
                ("cost of inaction", 5), ("urgency", 2),
            ],
            "Solution": [
                ("our solution", 4), ("we help", 2), ("how we solve", 4),
                ("what we do", 3),
            ],
            "How It Works": [
                ("how it works", 5), ("workflow", 2), ("step 1", 2),
                ("our process", 3),
            ],
            "Proof": [
                ("customers", 1), ("case study", 4), ("testimonial", 4),
                ("our customers", 3), ("reference", 3), ("proof", 3),
                ("results", 2),
            ],
            "ROI": [
                ("roi", 5), ("return on investment", 5), ("payback", 4),
                ("cost savings", 3), ("value calculation", 4),
                ("dollars saved", 3),
            ],
            "Implementation": [
                ("implementation", 4), ("rollout", 3), ("onboarding", 3),
                ("timeline", 2), ("kickoff", 2), ("go-live", 3),
            ],
            "Pricing": [
                ("pricing", 5), ("per seat", 3), ("per user", 3),
                ("starting at", 3), ("tier", 2), ("subscription", 2),
                ("annual contract", 3),
            ],
            "Next Steps": [
                ("next steps", 5), ("book a meeting", 4), ("let's talk", 3),
                ("schedule", 2), ("proposal", 3),
            ],
        },
    },

    "keynote": {
        "spine": [
            "Cover", "Hook", "Thesis", "Why This Matters Now",
            "Argument & Evidence", "Stories & Proof", "Implications",
            "Counter-arguments", "Call To Action", "Thank You",
        ],
        "target_count": 28,
        "tolerance": 8,  # keynotes span 20 to 35
        "type_signatures": [
            ("thank you for having me", 6), ("my thesis", 5),
            ("today i want to argue", 6), ("today i'll argue", 6),
            ("the one idea", 5), ("story time", 3),
            ("keynote", 5), ("ted", 4), ("conference talk", 5),
            ("speaker", 2), ("talk", 1),
        ],
        "role_keywords": {
            "Hook": [
                ("story", 2), ("imagine", 3), ("picture this", 4),
                ("let me tell you", 3),
            ],
            "Thesis": [
                ("my thesis", 5), ("the one idea", 4), ("today i'll argue", 5),
                ("i believe", 2),
            ],
            "Why This Matters Now": [
                ("why now", 4), ("why this matters", 5), ("the moment", 3),
            ],
            "Argument & Evidence": [
                ("evidence", 3), ("research shows", 3), ("data suggests", 3),
                ("consider", 2),
            ],
            "Stories & Proof": [
                ("story", 2), ("example", 2), ("case in point", 3),
                ("here's what happened", 4),
            ],
            "Implications": [
                ("what this means", 4), ("implications", 4),
                ("what to do", 3), ("how to apply", 3),
            ],
            "Counter-arguments": [
                ("objection", 3), ("counter-argument", 5),
                ("some might say", 4), ("critics argue", 4),
            ],
            "Call To Action": [
                ("call to action", 5), ("what i want you to do", 5),
                ("your turn", 3), ("go do this", 3),
            ],
            "Thank You": [
                ("thank you", 4), ("questions?", 3), ("q&a", 3),
            ],
        },
    },

    "launch": {
        "spine": [
            "Cover", "Problem", "Introducing", "How It Works", "Demo",
            "Who It's For", "Availability & Pricing", "Early Customers",
            "Roadmap", "Why Now", "Team", "Try It",
        ],
        "target_count": 12,
        "tolerance": 2,
        "type_signatures": [
            ("introducing", 5), ("now available", 6), ("available today", 6),
            ("launch day", 6), ("ga", 3), ("generally available", 6),
            ("sign up", 3), ("try it", 4), ("try now", 4), ("get started", 3),
            ("starting at $", 5), ("launch", 3), ("announcing", 5),
            ("product launch", 8), ("now live", 5),
        ],
        "role_keywords": {
            "Problem": [
                ("problem", 3), ("pain", 2), ("today's reality", 2),
            ],
            "Introducing": [
                ("introducing", 5), ("meet", 3), ("announcing", 4),
                ("presenting", 3), ("now available", 4),
            ],
            "How It Works": [
                ("how it works", 5), ("workflow", 3), ("step 1", 2),
                ("step 2", 2), ("step 3", 2),
            ],
            "Demo": [
                ("demo", 4), ("try the demo", 5), ("see it", 3),
                ("walkthrough", 3),
            ],
            "Who It's For": [
                ("who it's for", 5), ("built for", 3), ("made for", 3),
                ("designed for", 3),
            ],
            "Availability & Pricing": [
                ("availability", 4), ("pricing", 4), ("starting at", 4),
                ("free for", 3), ("per month", 3), ("available in", 3),
            ],
            "Early Customers": [
                ("customers", 2), ("testimonial", 3), ("early customer", 5),
                ("logo", 1), ("used by", 2), ("loved by", 3),
            ],
            "Roadmap": [
                ("roadmap", 4), ("coming soon", 3), ("next quarter", 2),
                ("upcoming", 3), ("what's next", 2),
            ],
            "Why Now": [
                ("why now", 5), ("market moment", 3), ("the shift", 3),
                ("timing", 2),
            ],
            "Team": [
                ("team", 3), ("founders", 3), ("the team behind", 4),
            ],
            "Try It": [
                ("try it", 5), ("get started", 4), ("sign up", 4),
                ("download", 3), ("visit", 2), ("qr code", 3),
            ],
        },
    },

    "all-hands": {
        "spine": [
            "Cover", "Agenda", "Big Wins", "Product Highlights",
            "Customer Stories", "Financial Update", "Hiring",
            "Team Spotlights", "Values", "Upcoming Events", "Priorities",
            "Learnings", "Shout-outs", "Q&A", "Open Floor",
        ],
        "target_count": 15,
        "tolerance": 2,
        "type_signatures": [
            ("all-hands", 8), ("all hands", 8), ("town hall", 7),
            ("team meeting", 4), ("welcome team", 5), ("monthly all hands", 8),
            ("shout-outs", 6), ("shout outs", 6), ("kudos", 4),
            ("new faces", 5), ("q&a", 2), ("open floor", 5),
            ("this month at", 4),
        ],
        "role_keywords": {
            "Agenda": [
                ("agenda", 5), ("today's plan", 3), ("topics", 2),
            ],
            "Big Wins": [
                ("big wins", 5), ("wins this month", 5), ("celebrations", 3),
            ],
            "Product Highlights": [
                ("product highlights", 5), ("what we shipped", 4),
                ("feature release", 4),
            ],
            "Customer Stories": [
                ("customer story", 5), ("customer spotlight", 5),
                ("our customer", 3),
            ],
            "Financial Update": [
                ("financial update", 5), ("company metrics", 4),
                ("burn", 2), ("revenue", 2),
            ],
            "Hiring": [
                ("new hires", 5), ("new faces", 5), ("welcome to", 3),
                ("open roles", 3), ("join us", 2),
            ],
            "Team Spotlights": [
                ("team spotlight", 5), ("highlight", 2),
                ("team of the month", 5),
            ],
            "Values": [
                ("values", 3), ("culture", 3), ("our values", 5),
                ("living our values", 5),
            ],
            "Upcoming Events": [
                ("upcoming events", 5), ("mark your calendar", 4),
                ("save the date", 4), ("upcoming", 2),
            ],
            "Priorities": [
                ("priorities", 4), ("next month", 3), ("focus areas", 3),
            ],
            "Learnings": [
                ("learnings", 4), ("retrospective", 4), ("what we learned", 4),
                ("setbacks", 3),
            ],
            "Shout-outs": [
                ("shout-outs", 5), ("shout outs", 5), ("kudos", 5),
                ("thank yous", 4), ("recognition", 3),
            ],
            "Q&A": [
                ("q&a", 4), ("questions?", 3), ("ask us", 3),
            ],
            "Open Floor": [
                ("open floor", 5), ("closing", 2), ("next all-hands", 4),
            ],
        },
    },
}

# Mapping from detected deck type to handoff skill (used downstream in Phase 3).
HANDOFF_SKILL: dict[str, str] = {
    "pitch": "deck-pitch",
    "sales": "deck-sales",
    "keynote": "deck-keynote",
    "launch": "deck-launch",
    "all-hands": "deck-all-hands",
}

# ---------------------------------------------------------------------------
# Shared regexes
# ---------------------------------------------------------------------------

DOLLAR_AMOUNT_RE = re.compile(r"\$\s?\d+(\.\d+)?\s?[MmBbKk]")
CAPITALIZED_NAME_RE = re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b")
ROLE_TITLE_RE = re.compile(r"\b(CEO|CTO|CFO|COO|CPO|VP|Founder|Co-Founder)\b", re.I)

TYPE_NAMES = list(SPINES.keys())


# ---------------------------------------------------------------------------
# Keyword matching helpers
# ---------------------------------------------------------------------------

def count_keyword(lowered: str, keyword: str) -> int:
    if " " in keyword or "-" in keyword:
        return lowered.count(keyword.lower())
    return len(re.findall(rf"\b{re.escape(keyword.lower())}\b", lowered))


def score_keywords(text: str, keyword_weights: list[tuple[str, int]]) -> int:
    if not text:
        return 0
    lowered = text.lower()
    total = 0
    for kw, w in keyword_weights:
        hits = count_keyword(lowered, kw)
        if hits:
            total += w * hits
    return total


# ---------------------------------------------------------------------------
# Deck-type detection
# ---------------------------------------------------------------------------

def detect_deck_type(
    pages: list[dict],
    page_count: int,
) -> dict:
    text_scores: dict[str, int] = {}
    count_bonus: dict[str, int] = {}

    deck_text = " ".join((p.get("text") or "") for p in pages)

    for type_name, spec in SPINES.items():
        text_scores[type_name] = score_keywords(deck_text, spec["type_signatures"])

        target = spec["target_count"]
        tol = spec["tolerance"]
        diff = abs(page_count - target)
        if diff == 0:
            count_bonus[type_name] = 8
        elif diff <= tol:
            count_bonus[type_name] = max(2, 8 - diff * 2)
        elif diff <= tol + 3:
            count_bonus[type_name] = max(0, 2 - (diff - tol))
        else:
            count_bonus[type_name] = -min(diff - tol, 10)

    final = {t: text_scores[t] + count_bonus[t] for t in TYPE_NAMES}
    ranked = sorted(final.items(), key=lambda kv: -kv[1])

    winner, winner_score = ranked[0]
    runner_up_score = ranked[1][1] if len(ranked) > 1 else 0

    if winner_score >= 15 and winner_score >= 1.8 * max(runner_up_score, 1):
        confidence = "high"
    elif winner_score >= 8 and winner_score >= 1.3 * max(runner_up_score, 1):
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "type": winner,
        "confidence": confidence,
        "scores": final,
        "text_scores": text_scores,
        "count_bonus": count_bonus,
        "ranked": ranked,
    }


# ---------------------------------------------------------------------------
# Per-slide role classification (uses winning type's spine)
# ---------------------------------------------------------------------------

def classify_page(
    page_num: int,
    text: str,
    company_name: str,
    has_hero_image: bool,
    was_ocr: bool,
    type_name: str,
) -> dict:
    spec = SPINES[type_name]
    role_keywords = spec["role_keywords"]
    overrides: list[str] = []
    words = text.split() if text else []
    word_count = len(words)

    if page_num == 1:
        has_company = bool(company_name) and company_name.lower() in (text or "").lower()
        if (word_count <= 40 and has_company) or word_count <= 10:
            return {
                "page_num": page_num,
                "role": "Cover",
                "confidence": "high",
                "scores": {},
                "overrides": ["cover-page-1"],
            }

    name_hits = len(CAPITALIZED_NAME_RE.findall(text or ""))
    has_role_title = bool(ROLE_TITLE_RE.search(text or ""))
    team_role = None
    for candidate in ("Team", "Team & Hiring", "Hiring", "Team Spotlights"):
        if candidate in role_keywords or candidate in spec["spine"]:
            team_role = candidate
            break
    if team_role and name_hits >= 3 and has_role_title:
        return {
            "page_num": page_num,
            "role": team_role,
            "confidence": "high",
            "scores": {},
            "overrides": ["team-names-with-titles"],
        }

    ask_role = None
    for candidate in ("Ask", "Asks"):
        if candidate in role_keywords or candidate in spec["spine"]:
            ask_role = candidate
            break
    if ask_role and DOLLAR_AMOUNT_RE.search(text or ""):
        lowered = (text or "").lower()
        if any(w in lowered for w in ("raise", "raising", "round", "funding", "use of funds")):
            return {
                "page_num": page_num,
                "role": ask_role,
                "confidence": "high",
                "scores": {},
                "overrides": ["ask-dollar-amount-with-raise-language"],
            }

    scores: dict[str, int] = {}
    for role, kw_list in role_keywords.items():
        scores[role] = score_keywords(text or "", kw_list)

    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    if not ranked:
        return {
            "page_num": page_num,
            "role": "Content",
            "confidence": "low",
            "scores": {},
            "overrides": ["no-scoreable-roles"],
        }
    top, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0

    role = "Content"
    confidence = "low"
    if top_score >= 3 and (second_score == 0 or top_score >= 2 * second_score):
        role = top
        confidence = "high"
    elif top_score >= 2 and (second_score == 0 or top_score >= 1.5 * second_score):
        role = top
        confidence = "medium"

    if has_hero_image and role in ("Product", "Introducing"):
        demo_score = scores.get("Demo", 0)
        if demo_score > 0 and top_score - demo_score <= 2 and "Demo" in role_keywords:
            role = "Demo"
            overrides.append("demo-hero-image-beats-product")

    if was_ocr:
        if confidence == "high":
            confidence = "medium"
        elif confidence == "medium":
            confidence = "low"

    return {
        "page_num": page_num,
        "role": role,
        "confidence": confidence,
        "scores": scores,
        "overrides": overrides,
    }


# ---------------------------------------------------------------------------
# Company name detection
# ---------------------------------------------------------------------------

def infer_company_name(extraction: dict) -> str:
    """Best-effort company name detection from metadata + cover slide."""
    meta_title = extraction["metadata"].get("title")
    if meta_title and len(meta_title) < 40:
        cleaned = re.sub(
            r"(?i)\s*(pitch\s+deck|sales\s+deck|"
            r"keynote|launch\s+deck|deck|final|v\d+|\d{4}).*$",
            "", meta_title,
        )
        cleaned = cleaned.strip(" -_")
        if cleaned:
            return cleaned
    pages = extraction.get("pages", [])
    if pages:
        first_text = pages[0].get("text", "").strip()
        for line in first_text.splitlines():
            line = line.strip()
            if 2 <= len(line) <= 30 and line[0].isalpha():
                return line
    return ""


# ---------------------------------------------------------------------------
# Top-level entry
# ---------------------------------------------------------------------------

def classify_deck(extraction_json_path: Path) -> dict:
    with open(extraction_json_path, "r") as f:
        extraction = json.load(f)

    # Normalize PPTX-only manifest shape into the extraction.json shape that
    # the rest of this module expects.
    if "slides" in extraction and "pages" not in extraction:
        extraction = _normalize_pptx_manifest(extraction)

    company_name = infer_company_name(extraction)
    was_ocr = bool(extraction["metadata"].get("was_ocr_fallback"))
    page_count = extraction["metadata"].get("page_count") or len(extraction.get("pages", []))

    type_result = detect_deck_type(extraction["pages"], page_count)
    winning_type = type_result["type"]

    page_results = []
    for page in extraction["pages"]:
        result = classify_page(
            page_num=page["page_num"],
            text=page.get("text", ""),
            company_name=company_name,
            has_hero_image=page.get("has_hero_image", False),
            was_ocr=was_ocr,
            type_name=winning_type,
        )
        page_results.append(result)

    spine = SPINES[winning_type]["spine"]
    present_roles = {r["role"] for r in page_results if r["confidence"] != "low"}
    missing_spine = [r for r in spine if r not in present_roles and r != "Cover"]

    alternatives = [
        {"type": t, "score": s}
        for t, s in type_result["ranked"][:3]
    ]

    output = {
        "company_name_guess": company_name,
        "deck_type": winning_type,
        "type_confidence": type_result["confidence"],
        "type_scores": type_result["scores"],
        "type_text_scores": type_result["text_scores"],
        "type_count_bonus": type_result["count_bonus"],
        "type_alternatives": alternatives,
        "handoff_skill": HANDOFF_SKILL[winning_type],
        "spine": spine,
        "spine_coverage": {
            "present": sorted(present_roles),
            "missing": missing_spine,
        },
        "pages": page_results,
    }

    out_path = extraction_json_path.parent / "classification.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    return output


def _normalize_pptx_manifest(manifest: dict) -> dict:
    """Translate a pptx-manifest.json shape into the extraction.json shape so
    the rest of the classifier can run unchanged."""
    pages = []
    for s in manifest["slides"]:
        # Concatenate title + body_text + captions so keyword matching has
        # everything in one bucket per slide.
        pieces = [s.get("title") or "", s.get("body_text") or ""]
        for cap in (s.get("captions") or []):
            pieces.append(cap)
        text = "\n".join(p for p in pieces if p)
        pages.append({
            "page_num": s.get("slide_num"),
            "text": text,
            "image_path": "",
            "image_dimensions": {"width": 0, "height": 0},
            "detected_font_families": [],
            "has_hero_image": bool(s.get("images")),
            "dominant_palette": [],
        })
    return {
        "source_pdf": manifest.get("source_pptx", ""),
        "extracted_at": manifest.get("extracted_at", ""),
        "metadata": {
            "title": manifest.get("metadata", {}).get("title"),
            "author": manifest.get("metadata", {}).get("author"),
            "page_count": manifest.get("metadata", {}).get("slide_count") or len(pages),
            "was_ocr_fallback": False,
        },
        "pages": pages,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify deck type + slide roles from extraction or PPTX manifest JSON."
    )
    parser.add_argument(
        "extraction_json", type=Path,
        help="Path to extraction.json (PDF path) or pptx-manifest.json (PPTX-only path).",
    )
    args = parser.parse_args()

    if not args.extraction_json.exists():
        sys.stderr.write(f"input not found: {args.extraction_json}\n")
        return 1

    result = classify_deck(args.extraction_json)
    print(
        f"Detected deck type: {result['deck_type']} "
        f"({result['type_confidence']} confidence)"
    )
    print(f"Handoff skill: {result['handoff_skill']}")
    print("Top 3 type candidates:")
    for alt in result["type_alternatives"]:
        print(f"  {alt['type']:<18} score={alt['score']}")
    print(f"\nCompany guess: {result['company_name_guess']!r}")
    print(f"\nPer-slide roles:")
    for p in result["pages"]:
        print(f"  Slide {p['page_num']:>2}: {p['role']:<24} ({p['confidence']})")
    print(f"\n  Written to: {args.extraction_json.parent / 'classification.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
