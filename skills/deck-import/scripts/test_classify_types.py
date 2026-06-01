#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""Smoke test: feed synthetic decks (one per OSS type) into detect_deck_type.

Expectation: each synthetic deck should be classified as its target type.
This doesn't exercise all role classifications, just the type-detection
layer, which is the new part of the classifier.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from classify_slides import classify_deck, SPINES


FIXTURES = {
    "pitch": [
        "Acme pitch deck",
        "The Problem: legal teams waste 40% of their week",
        "Why Now: AI inflection makes this possible",
        "Our Solution: we solve contract redlines",
        "Product features and how it works",
        "Live demo, see it in action",
        "Market: TAM $40B, SAM $8B, SOM $1B, total addressable market",
        "Business model: per seat per month, ARR, unit economics",
        "Traction: 50 paying customers, MoM growth, design partners",
        "Competition vs. legacy incumbents",
        "Moat: network effects, switching cost, defensible data advantage",
        "GTM: product-led growth, PLG motion, distribution",
        "Team: founded by X, previously at Y, years of experience",
        "Ask: we're raising $8M Series A. Use of funds.",
    ],
    "sales": [
        "Acme for your team, customer deck",
        "About You: your company's goals and your industry",
        "Your challenge: the problem with today's reality",
        "Why today, cost of inaction and urgency",
        "Our solution: how we solve it",
        "How it works: step 1, step 2, step 3",
        "Proof: case study and reference customer testimonials",
        "ROI: return on investment, payback, cost savings",
        "Implementation: rollout, onboarding, go-live timeline",
        "Pricing: per seat per month, tier, annual contract",
        "Next steps: book a meeting, proposal",
    ],
    "keynote": (
        # 28 slides, keynote range, with strong keynote signals spread
        # across early slides.
        [
            "Keynote, the one idea",
            "Imagine a world where, picture this",
            "My thesis: today I'll argue that",
            "Why this matters, the moment",
            "Evidence 1, research shows, data suggests",
            "Evidence 2, consider the following",
        ] +
        [f"Story {i}: here's what happened" for i in range(1, 9)] +
        [f"Implication {i}: what this means, what to do" for i in range(1, 6)] +
        [
            "Counter-argument: some might say",
            "Critics argue, but",
            "Still, the thesis holds",
            "Call to action: what I want you to do",
            "Your turn, go do this",
            "Thank you, questions? Q&A",
            "Contact and resources",
            "Final thought",
        ]
    ),
    "launch": [
        "Acme launches today",
        "The problem we saw",
        "Introducing Acme, now available",
        "How it works: step 1, step 2, step 3",
        "Demo: try the demo, walkthrough",
        "Who it's for, built for startups",
        "Availability & pricing: starting at $9/month, available in US",
        "Early customers, loved by these logos",
        "Roadmap: coming soon, upcoming",
        "Why now, market moment, the shift",
        "The team behind Acme",
        "Try it: get started, sign up, QR code",
    ],
    "all-hands": [
        "Welcome team, April all-hands",
        "Agenda: today's plan",
        "Big wins this month, celebrations",
        "Product highlights: what we shipped",
        "Customer story / customer spotlight",
        "Financial update: company metrics",
        "New hires, new faces, welcome to the team",
        "Team spotlight: team of the month",
        "Our values: living our values",
        "Upcoming events, mark your calendar",
        "Priorities: focus areas for next month",
        "Learnings: retrospective, what we learned",
        "Shout-outs, kudos, thank yous",
        "Q&A: questions? Ask us",
        "Open floor, next all-hands",
    ],
}


def make_extraction(slides: list[str]) -> dict:
    return {
        "source_pdf": "/tmp/fake.pdf",
        "extracted_at": "2026-04-23T00:00:00Z",
        "metadata": {
            "title": "Acme Deck",
            "author": "tester",
            "page_count": len(slides),
            "was_ocr_fallback": False,
        },
        "pages": [
            {
                "page_num": i + 1,
                "text": text,
                "image_path": "/tmp/fake.png",
                "image_dimensions": {"width": 1920, "height": 1080},
                "detected_font_families": ["Inter"],
                "has_hero_image": False,
                "dominant_palette": ["#0B1220"],
            }
            for i, text in enumerate(slides)
        ],
    }


def main() -> int:
    passed = 0
    failed = 0
    results = []
    for expected_type, slides in FIXTURES.items():
        with tempfile.TemporaryDirectory() as tmp:
            ep = Path(tmp) / "extraction.json"
            ep.write_text(json.dumps(make_extraction(slides)))
            out = classify_deck(ep)
            detected = out["deck_type"]
            conf = out["type_confidence"]
            ok = detected == expected_type
            results.append((expected_type, detected, conf, ok, out["type_alternatives"]))
            if ok:
                passed += 1
            else:
                failed += 1

    print(f"{'Expected':<18} {'Detected':<18} {'Conf':<8} {'OK'}")
    print("-" * 60)
    for expected, detected, conf, ok, alts in results:
        mark = "OK" if ok else "FAIL"
        print(f"{expected:<18} {detected:<18} {conf:<8} {mark}")
        if not ok:
            top3 = ", ".join(f"{a['type']}={a['score']}" for a in alts)
            print(f"    alts: {top3}")

    print(f"\n{passed}/{passed+failed} passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
