# Review Adaptations for Conversion Mode

The 3 reviewer gates from deck-builder (Brand, Copy, Layout) run unchanged in their structure, same spec files, same independence rule, same pass/fail gating. What changes is the **calibration**: the reviewers judge against a different target because "conversion" is not "native authorship", AND because the conversion is now type-aware, a sales deck gets sales-deck review bars, a keynote deck gets keynote-deck review bars, etc.

**Build mode also gates which reviewers run.** Mode A (page-image, default) only runs Layout, the other two are tautologically perfect because the source IS the output. Mode B (reconstruction) runs all 3 with the calibrations in §§1 to 3. See §0 below for the mode-aware gating table.

This file is the diff. Every reviewer below cross-references its spec in `deck-builder/reviewers/<name>.md`, read that first, then apply the adaptations here. Per-type calibrations are in §§1 to 3 under "Type-specific calibration".

---

## 0. Build mode determines reviewer scope

The conversion brief's `build_mode` field switches which reviewers run.

### Mode A, page-image (DEFAULT)

The deck is rendered as full-bleed source pages with a deck shell. There's no HTML reconstruction of any slide content, the source IS the output. Two of the three reviewers are skipped because they have nothing to judge:

| Reviewer | Mode A status | Reason |
|---|---|---|
| 1. Brand | **skip, n/a** | Slide content is the source raster. No CSS palette to verify. The shell's letterbox + brand bar use safe defaults. |
| 2. Copy | **advisory only** | The source's content gaps are surfaced as advisory notes in Release. Does NOT block release because the gaps exist in the source, not the conversion. |
| 3. Layout | **RUN** | Slide count matches source; `.slide-meta` pills present on N-1 interior slides; SHOTS valid JSON; no emoji codepoints; one `.s-cover`; viewport meta is `device-width` not `1440`; file size 1.5 to 2.5 MB; `structural_check.py` passes; shell pattern matches `page-image-mode.md` (deck-outer flex centerer, deck transform-origin center, nav inside .deck, flex-shrink: 0). |

Audit format under Mode A: 3 one-line entries, 1 reading "PASS · <details>" and 2 reading "n/a (Mode A, source-faithful by construction)". The Copy reviewer's advisory layer appends type-specific notes (missing Team/Traction/Ask for pitch, missing Customer Stories for all-hands, etc.) as informational additions in the Release message.

### Mode B, reconstruction (OPT-IN)

All 3 reviewers run with the conversion-mode calibrations documented in §§1 to 3 below. This is the path when the user opted into reconstruction or opted into an interactive demo.

When the underlying agent supports subagents, spawn each reviewer as a subagent.

---

## 1. Brand Reviewer

**Spec**: `deck-builder/reviewers/brand.md`

**Standard target**: does the CSS match the declared brand (re-verified against the brand's live page)?

**Conversion target**: does the CSS match the **source's sampled palette and detected typography**, three-way agreement with the brief?

### Three-way agreement check

| Source | Origin |
|---|---|
| 1. Brief palette (§3) | Locked during Phase 2 confirmation |
| 2. Final CSS tokens | Shipped HTML's `:root` |
| 3. Source sampled palette | Re-sample during Phase 4 by the reviewer using `scripts/detect_palette.py` on the source |

Pass: all three agree within `ΔE <= 5` for each color (perceptual distance, approximate by computing RGB euclidean distance, threshold roughly 20).

Fail: any mismatch. Common failures:
- Brief palette locked in a color the user edited AFTER re-rendering, but the shipped CSS still has the old color.
- Re-sampling detects a color the original palette detection missed (e.g., accent on a single late slide that wasn't surfaced).

### Type-specific calibration

No meaningful variation. Brand asks the same question for every deck type: does the shipped HTML mirror the source's palette and typography? The detected type doesn't move this bar.

### What NOT to check

- Brand anachronisms (e.g., "Uber 2010 era palette"), irrelevant for conversions. The conversion is locked to what the source actually contains today.
- Logo-shape matches a live brand page, irrelevant. The conversion uses the source's extracted cover image or the detected typography-based wordmark, not a fresh fetch.

---

## 2. Copy Reviewer

**Spec**: `deck-builder/reviewers/copy.md`

**Standard target** (native builds): copy is on-spec for the deck type, no claim is unsupported, voice matches the brief.

**Conversion target**: score the same dimensions, BUT:

- **Working-demo dimension is conditional on `demo_mode` in the brief §6**:
  - If `demo_mode: static` (default for pitch / launch), dimension is **SUSPENDED**. The reviewer notes "N/A, conversion mode, static demo per brief" and does NOT lower scores for absence of interactivity.
  - If `demo_mode: interactive` (user opted in during Phase 2), dimension is **UN-SUSPENDED**. The reviewer judges the demo slide against the handoff skill's demo bar.
  - For types without a Demo spine role (keynote, all-hands, sales), dimension is permanently N/A.
- **Content scores reflect the source**, not the conversion skill's work. If the source had a weak Why Now, the conversion also has a weak Why Now, that's the source's content, not the conversion's failure. The reviewer's role in conversion mode is to surface content gaps to the user as **upgrade opportunities**, not to fail the build for them.

### Type-specific calibration, what to check beyond the generic rubric

In conversion mode the Copy Reviewer ALSO calls the handoff skill's type-specific bar:

- **pitch** (`deck-pitch`), spine coverage (Problem / Why Now / Solution / Market / Traction / Ask). Working-demo SUSPENDED.
- **sales** (`deck-sales`), every ROI claim sourced; pricing NOT hidden; Next Steps names a specific human and date.
- **keynote** (`deck-keynote`), one idea per slide; mandatory opening hook on slide 1 to 2; every slide has a visual anchor.
- **launch** (`deck-launch`), Availability & Pricing slide co-located; CTA with QR/URL; working-demo SUSPENDED per §6.
- **all-hands** (`deck-all-hands`), celebration AND candor balance (not only-wins); company-appropriate financials (not board-level detail); Q&A placeholder.

These bars are **advisory in conversion mode** (they produce advisory notes in the Copy report, not blockers), but they MUST be checked and reported. Silence = miss.

### The Copy report format (conversion mode)

Instead of pass/fail per dimension, the Copy Reviewer produces a two-part output:

1. **Fidelity score**: did the HTML preserve the source content? 1 to 10 scale. Only this score gates the release.
2. **Advisory content notes**: a list of "here's what the source deck could improve, per the {{detected_type}} bar", these are NOT blockers, they're follow-up suggestions the user can act on with a separate native-build pass using the `{{handoff_skill}}` skill.

Example (pitch):

```
Fidelity score: 9/10. Content preserved 1:1 except one OCR cleanup on slide 3 (hyphenation).

Advisory content notes (not blockers, judged against the deck-pitch bar):
- Why Now slide leans on timing but doesn't cite a specific unlock. Consider adding.
- Competition slide lists three competitors without quantified differentiation. Consider a feature-vs-feature table.
- Ask slide is missing use-of-funds breakdown. Consider adding.

Want me to draft a native build pass with these upgrades? That's a separate deck-pitch run.
```

This keeps conversion-mode Review short and non-blocking while still surfacing real content work the user might want to do, on the RIGHT type bar.

---

## 3. Layout Reviewer

**Spec**: `deck-builder/reviewers/layout.md`

**Standard target**: no overflow on 1440x810; scales correctly on small viewports.

**Conversion target**: identical. Overflow risk is HIGHER for conversions because source files may have dense slides that don't fit into the 1440x810 content area. Reviewer pays extra attention to:

- Slides with >150 words of extracted body text (likely to overflow).
- Slides where the source had a 4:3 or portrait aspect ratio but the HTML tries to show full content at 16:9.
- Hero-image slides where the image dimensions force overflow (very tall image, thin canvas).

### Type-specific calibration

- **keynote** (20 to 35 slides, often full-bleed imagery), letterboxing calculus differs when the source has image-dominant slides; verify no forced crop.
- **all-hands** and **sales** (mixed content), no special calibration; standard rules apply.

Pass: all slides fit within the 810px canvas with header+footer reserved zones intact. Scale-to-fit letterboxing works at small viewports.

Layout also covers the mechanical checks the deck-builder Layout reviewer owns:

- **Section count = source page count**. If brief says 14 slides, shipped HTML has 14 `<section class="slide">`. Mismatch = fail.
- **File size ceiling raised to 2.5 MB** because embedded screenshots add weight. If above 2.5 MB, compress the embedded PNGs (JPEG encode at quality 85 for non-cover images).
- **Every embedded image has `onerror` handler**, even inline base64 ones (in case base64 is corrupt).
- **No hand-crafted `<path>` approximating a brand letter**, if the source had a custom logo and it's not extractable as an image, use `<text>` with the detected display font. Never a path.
- **demo_mode verification**, read brief §6. If `demo_mode: interactive`, slide {{demo_slide_num}} MUST contain real `<input>` / `<button>` / `<select>` / event handlers wired to JS state. If `demo_mode: static`, the demo slide MUST NOT contain fabricated interactivity beyond the standard interactivity-upgrades patterns.

---

## How reviewers run in conversion mode (operational note)

Same independence rule as deck-builder: each reviewer runs as a separate invocation. When the underlying agent supports subagents, spawn each reviewer as a subagent; otherwise, re-read with a fresh frame between runs.

Review can run in parallel across the 3 reviewers. The conversion brief + shipped HTML + source file are the only inputs, reviewers DO NOT have access to the conversation history or the extraction JSON (to stay independent).

Handoff-skill calibration (§2 above) is passed to reviewers by writing the detected type + handoff skill into the brief (§0 of the conversion-brief template). Reviewers read the brief first, then apply the appropriate type-specific bar.

---

## What this file does NOT change

- The failure categories in Phase 6 (Learn) are the same as deck-builder's, minus a couple that don't apply (brand anachronism) and plus a few that do (extraction gap, palette mis-detection, role misclassification, typography miss, fidelity drift, shell divergence, type mis-detection). See SKILL.md §Phase 6.
- The gate contract: all 3 reviewers must pass before Release. Conversion doesn't relax gating, only the bars for Layout and Copy are adjusted (uniformly across types), and Copy is type-calibrated.
- The file structure: conversion output is still a single HTML file, same canvas, same shell.
