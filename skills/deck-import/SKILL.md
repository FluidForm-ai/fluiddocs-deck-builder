---
name: deck-import
description: Convert any PDF or PPTX deck into a self-contained interactive HTML deck, one file, one link, shareable. Auto-detects input file extension (.pdf or .pptx) and routes to the matching extraction path. Detects which of the 5 deck types the source is (pitch, sales, launch, keynote, all-hands) and hands off to the matching deck-* skill. Trigger when the user uploads a .pdf or .pptx of any deck type, or says any variation of "convert this PDF to HTML", "turn this PPTX deck into HTML", "import this deck", "upgrade my deck", "make my deck interactive", "migrate my deck from PDF/PPTX". Mirrors source palette, typography, and slide structure 1-to-1 (no redesign), preserves slide count, uses extracted screenshots on demo slides where applicable, auto-extracts key fields, then confirms with the user before building. Reuses deck-builder core pipeline and per-type spines as role-labeling taxonomy. Fastest path from cold PDF or PPTX to warm shareable link.
---

# Deck Import (PDF or PPTX, HTML Deck, generic across 5 deck types)

You are converting a **PDF or PPTX deck** into an **interactive HTML deck**, the entry point for users who already have a deck and want the upgrade (shareable link, scale-to-fit canvas, navigation shell) without a redesign.

**Core principle**: the user's deck is already the deck. Your job is to faithfully reproduce it in HTML, not to redesign it. Mirror the palette. Mirror the typography where possible. Preserve slide count and order. Keep their words. The "upgrade" is the delivery medium, not the content.

**Two build modes, page-image is the default.** The skill ships two Phase 3 implementations:

- **Mode A, page-image (DEFAULT)**: each slide is rendered as a full-bleed background image of the source page. The HTML provides only the shell, role-meta pill on interior slides, progress bar, nav arrows, counter, scale-to-fit canvas, touch swipe. **Pixel-faithful by construction**, no palette drift, no typography mismatch, no source-text ghosting, no logo recreation. One-shot quality on virtually every deck. See `references/page-image-mode.md`.
- **Mode B, reconstruction (OPT-IN)**: every slide is rebuilt in HTML/CSS/SVG. Editable, but risk-prone: palette guessing, source-text ghosting on photo backgrounds, content rewriting, layout drift. Use only when the user explicitly asks to be able to edit slides later, or to upgrade specific visual components. The user opts in during Phase 2 by replying "reconstruction" or "rebuild".

Default Mode A. Switch only on explicit opt-in.

This skill is generic across 5 deck types, **pitch, sales, launch, keynote, all-hands**. It is NOT a general document converter. PDFs or PPTX files that aren't decks (whitepapers, resumes, research papers, portfolios) should be redirected to a doc-builder skill.

Conceptually, deck-import is **a type-pack-like layer in front of `deck-builder` + the matching `deck-<type>` skill** (Mode B only, Mode A doesn't need the handoff skill for build, only for role-label vocabulary). Mode A adds three front-end phases (Extract, Analyze, Confirm) plus a thin Mode A shell build. Mode B adds the same front-end phases then hands off to the standard reviewer gates per `references/review-adaptations.md`.

If the user has not installed `deck-builder` or the relevant `deck-<type>` skill for the detected type, surface the gap early and ask them to install.

---

## Auto-detect (Phase, 1, file-extension routing)

Before any extraction runs, examine the input file extension:

```
input_path = <user-supplied file path>
ext = lowercase suffix of input_path

if ext == ".pptx":
    → PPTX-only path (Phase 0p)
elif ext == ".pdf":
    → PDF path with optional sibling .pptx check (Phase 0)
else:
    → ask the user: "deck-import handles .pdf and .pptx files only. What did you mean?"
```

The PPTX-only path skips PDF rasterization entirely and uses `scripts/extract-pptx-only.py` (see Sub-phase C). It produces a JSON manifest with per-slide text, embedded images, speaker notes, and slide order. The PDF path runs the established extraction pipeline and OPTIONALLY uses sibling PPTX assets when available for higher fidelity.

Both paths converge at Phase 1 (Analyze) using the same `classification.json` shape, so everything downstream (Confirm, Build, Review, Release, Learn) is identical regardless of input format.

---

## When this skill runs (trigger anatomy)

The trigger description (in YAML frontmatter above) is deliberately broad because this is the primary adoption ramp for users who already have a deck. If the user uploads a PDF or PPTX that could plausibly be any of the 5 deck types AND mentions HTML, interactive, conversion, import, migration, or "upgrade" in any form, this skill is right.

**Edge cases**:
- File ambiguous between two deck types (e.g., reads like an all-hands OR a keynote): the Phase 1 classifier surfaces both in the confirmation block with scores. The user picks via "this is a <type>" in Phase 2.
- File is a research paper, whitepaper, or article: this is NOT the right skill. Redirect to a doc-builder.
- File is a resume or portfolio: not the right skill. Redirect to the appropriate doc skill.
- File is a handbook, wiki export, or multi-page report: not a deck. Redirect to a doc-builder.

The classifier treats "is this a deck at all?" as a sanity check. If no type scores above the "low" confidence threshold AND the page count is outside every canonical band (e.g., 40+ pages with dense prose), surface that observation and ask the user whether they want to proceed anyway, re-route to a doc-builder, or cancel.

---

## The conversion pipeline (6 phases)

| Phase | Owner | Gate | Output |
|---|---|---|---|
| 0. Extract | script (`extract_deck_pdf.py` or `extract-pptx-only.py`) | script exits 0 | JSON dump of per-slide text, per-slide images, metadata |
| 1. Analyze | script (`classify_slides.py`) + you | none | detected deck type, company, palette, typography, per-slide role guess, handoff skill |
| 2. Confirm | user | user approves or edits | locked conversion brief |
| 3. Build | you (calling handoff skill) | self-lint pass | `<Company>-<type>-Imported.html` file |
| 4. Review | 3 reviewers (deck-builder inheriting, type-calibrated) | all pass | 3 one-line audit entries |
| 5. Release | you | all reviewers passed | file + absolute path link + conversion report |
| 6. Learn | you, post-feedback | , | append to `references/conversion-learnings.md` |

The deck-builder 5-phase core maps onto Build, Review, Release, Learn (phases 3 to 6 here). Phases 0 to 2 (Extract, Analyze, Confirm) are this skill's original contribution.

---

## Phase 0 , Extract (PDF path)

**Input**: the PDF path (from upload or user-supplied filepath).
**Output**: a JSON file at `/tmp/deck-import-<timestamp>/extraction.json` plus a per-page images folder at `/tmp/deck-import-<timestamp>/pages/` (one PNG per slide). When PPTX is available (see Step 0a), an additional `pptx_assets.json` and an unzipped `ppt/` tree.
**Gate**: extraction script exits cleanly. If it doesn't, ask the user what's different about this PDF (encrypted? scanned? very large?).

### Step 0a , PPTX-first check (prefer PPTX as the primary source when available)

Before running the PDF extractor, check whether a `.pptx` of the same deck is reachable. PPTX gives roughly 5x the source fidelity of PDF-only extraction (exact source PNGs in `ppt/media/`, exact gradient color stops from `a:gradFill`, exact EMU positions from `p:spPr/a:xfrm`, exact `a:custGeom` shapes for non-standard outlines like semicircles or half-domes). Conversion runs that started PDF-only and only surfaced the PPTX mid-run consistently spend 6 to 8 extra iteration rounds reverse-engineering rasters and geometries that the PPTX already contains exactly.

Decision tree:

1. Look for a sibling `.pptx` in the same directory as the uploaded `.pdf` (same stem; e.g., `MyDeck.pdf` next to `MyDeck.pptx`).
2. If not present, look in the user's workspace folder for a `.pptx` with a matching stem.
3. If still not found, ask the user **before iterating from PDF**: "Do you have a `.pptx` of this deck? PPTX gives much more accurate extraction (exact source images, gradients, positions) and is the difference between 4 rounds and 12 rounds on most decks. If yes, drop it in and tell me the name."

If a PPTX is found, run BOTH extractors and treat the PPTX as the primary source for assets, the PDF as the rasterization fallback:

```bash
python scripts/extract_pptx_assets.py <pptx-path> --out /tmp/deck-import-<timestamp>/pptx/
python scripts/extract_deck_pdf.py <pdf-path>  --out /tmp/deck-import-<timestamp>/
```

`extract_pptx_assets.py` enumerates `ppt/slides/*.xml` plus their relationship files and emits a JSON document with, per slide: a list of pic refs `(rId, image_path, position_px, size_px)` keyed back to the unzipped media folder, plus a list of `a:gradFill` records `(color_stops, angle)`. Phase 1 reads this JSON for geometry and gradient ground truth.

### Step 0b , Read slide size first; cache (sldW_emu, sldH_emu) before any EMU-to-pixel conversion

Whether or not PPTX is available, but **mandatory** when PPTX is the source: parse `ppt/presentation.xml` and cache the `<p:sldSz cx="..." cy="..."/>` values **before** doing any EMU-to-pixel math. Default PowerPoint slide sizes range from 10x7.5" (4:3, `cy=6858000`) through 10x5.625" (16:9, `cy=5143500`) through 13.333x7.5" (16:9 widescreen, `cy=6858000` cx=12192000). Assuming the default 4:3 dimensions when the deck is 16:9 puts every Y position off by roughly 33%, components land below the intended row, headers drift up, bottoms get clipped.

```bash
python scripts/parse_slide_size.py /tmp/deck-import-<timestamp>/pptx/ppt/presentation.xml
# stdout: {"sldW_emu": 12192000, "sldH_emu": 6858000, "ratio": "16:9"}
```

The cached `(sldW_emu, sldH_emu)` becomes the divisor in every later position/size computation: `position_px = emu / sldW_emu * 1440` for x, `emu / sldH_emu * 810` for y. Bake this into the build script as constants at the top, not as inline literals.

### Step 0c , PDF extraction (always run; primary when PPTX unavailable, fallback rasterization when PPTX is the source)

Run:
```bash
python scripts/extract_deck_pdf.py <pdf-path> --out /tmp/deck-import-<timestamp>/
```

The script uses `pdfplumber` (text) + `pypdf` + `pdf2image` (page images) + `Pillow` (palette sampling) to produce:
- `extraction.json` with `{pages: [{page_num, text, image_path, dimensions}], metadata: {title, author, page_count, detected_aspect_ratio}}`
- `pages/page-<N>.png` per slide (at 2x resolution for high-quality screenshot placement)

If the PDF is scanned (no text layer), the script falls back to OCR via `pytesseract`. See `references/extraction-pipeline.md` for the full data contract and fallback rules.

### Step 0d , Prior-output scan (canonical-style reference detection)

Before Phase 1 finishes, scan the user's workspace for prior imports of the same company or the same shell signature. These are the canonical style reference, match them, don't reinvent.

```bash
ls <user-workspace>/*-Imported.html 2>/dev/null
ls <user-workspace>/*-Imported.html 2>/dev/null | xargs -I{} grep -l "data-shot" {} | head -5
```

Two signals to surface in the Phase 2 confirmation block:

1. **Company match.** Any prior `*-Imported.html` whose filename includes the detected company (case-insensitive). Display: `Prior imports, <files>. Match their style? (yes/no, default yes)`.
2. **Shell-signature match.** Any prior import using a `<div class="slide-img" data-shot="N">` pattern indicates Mode A page-image. Surface as: `Prior decks use Mode A page-image, defaulting to same.`

---

## Phase 0p , Extract (PPTX-only path)

**Input**: the PPTX path (from upload or user-supplied filepath).
**Output**: a JSON file at `/tmp/deck-import-<timestamp>/pptx-manifest.json` plus an extracted images folder at `/tmp/deck-import-<timestamp>/media/` (one image per embedded asset).
**Gate**: extraction script exits cleanly.

Run:
```bash
python scripts/extract-pptx-only.py <pptx-path> --out /tmp/deck-import-<timestamp>/
```

The script uses `python-pptx` to walk the file and emit:
- `pptx-manifest.json` with `{slides: [{slide_num, title, body_text, captions, notes, images: [{path, position_px, size_px}]}], metadata: {title, author, slide_count, slide_size_emu, ratio}}`
- `media/image-<slide>-<idx>.<ext>` per embedded image, with predictable naming

Speaker notes are preserved verbatim from each slide's notes pane. Slide order is the raw `presentation.xml` order, not filename-sorted (PowerPoint reorders slides without renumbering filenames).

The manifest shape was designed so Phase 1 (`classify_slides.py`) can consume it directly without translation, by treating each slide as if its `body_text` were the PDF page's extracted text. Image-position math uses the same EMU divisors as the PDF+PPTX hybrid path (see Step 0b).

PPTX-only skips Step 0a (no PDF to consult), Step 0c (no PDF extraction), and the page-image rasterization for Mode A. To produce Mode A page-images from a PPTX-only input, the build step converts each slide to PNG via LibreOffice headless conversion (`libreoffice --headless --convert-to png --outdir <out> <pptx>`) when LibreOffice is installed; otherwise the build step asks the user to provide a PDF render or falls back to Mode B reconstruction.

---

## Phase 1 , Analyze

**Input**: `extraction.json` (PDF path) or `pptx-manifest.json` (PPTX-only path), plus per-slide images.
**Output**: `classification.json` + a draft conversion brief (in memory / shown to user in Phase 2).
**Gate**: none, this phase is non-destructive analysis.

Analysis runs in two steps, both driven by `scripts/classify_slides.py`:

### Step 1: Detect deck type

The classifier scores all 5 deck types by:
1. Deck-wide match against each type's **type-signature keywords** (weighted phrases relatively unique to that type, e.g., "use of funds" signals pitch, "available now" signals launch, "Q&A" signals all-hands).
2. **Slide-count fit bonus**: how close `page_count` is to each type's canonical band (pitch is roughly 14, sales is roughly 11, keynote is roughly 28, launch is roughly 12, all-hands is roughly 15).

Confidence:
- **high**: winner >= 15 score AND >= 1.8x runner-up.
- **medium**: winner >= 8 AND >= 1.3x runner-up.
- **low**: otherwise. Classifier emits the top-3 alternatives so the confirmation block can show them and let the user override.

The winning type's matching `deck-<type>` skill is the **handoff skill** for Phase 3. Full vocabulary: `references/spine-tables.md`.

### Icon classification (when PPTX present)

For each icon SVG/PNG in `ppt/media/`, classify intended pairing:

- **`icon-on-colored-square`**, used inside `.stat-icon`, `.sol-icon`, `.wn-icon`, `.bm-feat .ic`, `.vis-st-row .ic`, etc. Source fill is `#ffffff` or `#fdfdfd`. Render as WHITE.
- **`icon-on-light-bg`**, standalone outline icon on a light slide background. Source fill is `#006838` or `#000000` (or the deck's primary). Render as PRIMARY color.

Map per-slot in the conversion brief. Before ImageMagick conversion:

```bash
sed -e 's/fill="#ffffff"/fill="<target>"/g' \
    -e 's/fill="#fdfdfd"/fill="<target>"/g' \
    -e 's/fill="#000000"/fill="<target>"/g' \
    -e 's/fill="inherit"//g' \
    source.svg > target.svg
```

The `inherit` fill is unsupported by ImageMagick and must be stripped, leaving it in produces transparent glyphs even when the fill cascade should resolve. Detailed recipe in `references/extraction-pipeline.md` "PPTX icon color normalization".

### Logo stack detection

When the source has a logo wall with stacked logos, detect pairing by overlapping x-ranges in bounding boxes, NOT by left-to-right adjacency. Phase 1 emits `(x, y, w, h)` per logo; group into vertical stacks where two logos' x-ranges overlap and their y-ranges differ by more than half the canvas-height of the wall region.

Horizontal-adjacency grouping pairs logos by reading order, which is wrong when the source visually stacks them. The fix matches what the user's eye sees. Recipe in `references/extraction-pipeline.md` "Logo stack detection".

### Step 2: Classify slide roles (using the winning type's spine)

For each slide, detect:

1. **Role** (a spot on the winning type's spine): keyword-match the extracted text against the spine vocabulary in `references/spine-tables.md`. Confidence levels: high / medium / low. Low-confidence slides are labeled "Content" and flagged for user correction in the confirmation block. Hard overrides still apply (Cover = page 1; Team-like slide = 3+ human names + role title; Ask/Asks = dollar amount + raise language, each adapted to which labels the winning spine actually uses).

2. **Company / counterparty name** (from title slide text + metadata title).

3. **Type-dependent context** (skill populates only fields matching the detected type):
   - pitch, stage + sector
   - sales, industry + deal-size band
   - keynote, venue + talk length
   - launch, product + availability
   - all-hands, size + meeting cadence

4. **Dominant palette** (3 to 5 colors): sample each page image with `detect_palette.py`. Cross-page aggregation to identify the true brand primary vs. per-slide accents. See `references/palette-typography-detection.md`.

5. **Typography family guess**: inspect `pdfplumber` font metadata per text block (PDF path) or `python-pptx` font metadata (PPTX-only path). Most files expose the actual font names (`Inter-Regular`, `Helvetica`, `TiemposHeadline-Medium`). When a detected font isn't web-safe, map to the closest Google Font stand-in per the table in `references/palette-typography-detection.md`.

6. **Images per slide**: note which slides have full-bleed or hero imagery. These become static screenshots in the HTML. For types with a Demo spine role (pitch, launch), extract the largest image on the detected demo slide as the hero and label it "[Static product preview, interactive demo available on request]". For all other types, imagery is handled per the handoff skill's visual patterns.

7. **Missing-spine-role flags**: if the winning type's canonical spine has roles without a matching slide, note for the confirmation block. This is advisory, not prescriptive, we preserve the source structure 1:1.

8. **Image content classification**: tag every extracted image as `photographic-real` / `ai-stylized` / `illustration` / `chart`. Detection heuristics in `references/image-sourcing.md`. If ANY images are tagged `ai-stylized`, add a Phase 2 swap-offer line to the confirmation block: "Source uses AI-rendered art for N images (slides X, Y, Z). Reply 'swap photos' to surface real-photo alternatives during the build. Reply 'keep' to use as-is." Default is KEEP, don't auto-swap without consent.

9. **Custom-geometry shape classification (PPTX-only step)**: when PPTX assets are available, walk each slide's `a:custGeom` entries and read each shape's `cx:cy` ratio from `a:xfrm/a:ext`. Map ratios to recognizable shape patterns so Phase 3 picks the right CSS recipe:
   - **Near 2:1** (within +/-0.15), true semicircle (half-circle). CSS recipe: `border-radius: <half-cx>px <half-cx>px 0 0` with no bottom border.
   - **Near 1.55:1** (within +/-0.15), half-dome (squat hemisphere). Same border-radius recipe but width is wider than height.
   - **Near 1:1**, full circle. CSS recipe: `border-radius: 50%`.
   - **Anything else**, flag the slide for hand-review; do not silently approximate.
   Record the shape classification in `classification.json` so the build script reaches for the right recipe instead of defaulting to `border-radius: 50%`.

10. **Background composition (photo-tint vs flat-gradient)**: every slide background is one of two types, and the distinction is the difference between a slide that feels native and one that feels flat.
    - **flat-gradient**: a pure CSS gradient with no underlying image. The source has only `a:gradFill` in the slide's `p:bg/p:bgPr`.
    - **photo-tint**: a photographic image overlaid with a colored gradient via PowerPoint's `background-blend-mode: multiply` semantics. The source has BOTH a `p:bg/p:bgPr/a:blipFill` (the photo) AND a gradient layer. The texture of the photo (stars, peak silhouettes, etc.) is meant to read through the tint.
    Detection (PPTX path): inspect `p:bg/p:bgPr` for the presence of `a:blipFill`, if present, classify as `photo-tint` and extract both the image and the gradient stops. Phase 3 will render this as `background-image: linear-gradient(...), url(photo); background-blend-mode: multiply, normal;` (see Phase 3 rule #13). Detection (PDF fallback): compute entropy on the background region; high entropy + a dominant tint cluster, likely photo-tint, surface for user confirmation.
    Full recipe in `references/palette-typography-detection.md`, "Background Composition" section.

Full analysis rules in `references/spine-tables.md` and `references/palette-typography-detection.md`.

---

## Phase 2 , Confirm (the "key fields" block)

**Input**: the draft analysis.
**Output**: an approved conversion brief, saved as `<Company>-<type>-Conversion-Brief.md` next to where the HTML will land.
**Gate**: user confirms or edits the confirmation block. No HTML is written until confirmation.

Present a compact confirmation block, NOT the full deck-builder brief. The user came here with an existing deck; don't make them fill in 10 sections of founder intake. Show only what was detected, formatted for one-glance review. Use the template in `references/confirmation-block-template.md`.

The confirmation block is **type-aware**: it shows the detected type + confidence + alternatives (if not high confidence), the handoff skill, the type-dependent context fields, the slide-role list from the winning spine, and, only for pitch / launch, a Demo line that includes the `demo_mode` opt-in (user can reply "interactive demo" to flip the default from static to interactive BEFORE Phase 3 runs).

**Hard "PPTX available?" row at the top of every confirmation block when input was PDF.** Phase 0a quietly checks for a sibling `.pptx`; this row is the EXPLICIT ASK whenever Phase 0a didn't find one. Surfacing the question in the confirmation block converts roughly 3 wasted rounds per PPTX-available-but-not-found run into a one-line user reply. Show the row even when PPTX was detected ("yes, pulled icons, gradients, custGeom from `<name>.pptx`") so the user can confirm the right file was picked up. Skip this row when input was already PPTX.

**Hard "Build mode" row immediately after PPTX row.** Default is **`page-image`** (Mode A, full-bleed source pages, shell only, pixel-faithful, no reconstruction risk). The user can flip to `reconstruction` (Mode B) by replying "reconstruction" or "rebuild". Mode B is required when the user wants to edit slide content later, add an interactive demo, or upgrade specific components. Mode A is the right answer for roughly 90% of conversions, the source IS the deck.

**"Prior style match" row when Step 0d found prior outputs.** Pre-fills Build Mode based on whether existing imports use Mode A. The user can override.

Example (pitch, high confidence, Mode A default):

```
Extracted your 14-slide deck. Here's what I detected, reply "go" to build, or tell me what to change:

  PPTX available?  unknown, drop into uploads to enable 5x fidelity
  Build mode       page-image (default, pixel-faithful, each slide is the source page)
                   Reply "reconstruction" to rebuild slides in HTML/CSS instead
  Prior imports    Acme-partnership-Imported.html, Acme-sales-Imported.html
                   Both use page-image, matching style.

  Deck type      pitch (high confidence)
  Handoff skill  deck-pitch (role-label vocabulary only; Mode A skips HTML handoff)

  Company        Acme
  Context        Stage Series A · Sector Vertical AI (Legal)
  Slide count    14 (preserving 1:1)
  Palette        #0B1220 ink · #F97316 primary · #F8FAFC surface (sampled; informational in Mode A)
  Typography     Display: Tiempos Headline · Body: Inter (informational in Mode A)
  Slide roles    Cover, Problem, Solution, Why Now, Market, Product, Product (cont), Demo,
                 Traction, Competition, Moat, GTM, Team, Ask
  Demo slide     n/a in Mode A, source slide is rendered as-is.
                 Reply "interactive demo" to switch to Mode B and build a working demo.

Output path      <user-workspace>/Acme-pitch-Imported.html

Reply "go" to build, or tell me what to change.
```

Keep it that short. If the user edits fields, including type, update the brief and re-display before building.

Once approved, the conversion brief is the single source of truth for Phase 3, reviewers will diff against it exactly like they do for a native-authored deck. Template: `references/conversion-brief-template.md`.

### If the user overrides the detected type

1. Re-run `classify_page(..., type_name=new_type)` for each slide using the new spine.
2. Update the handoff skill to match (pitch, deck-pitch; sales, deck-sales; ...).
3. Rewrite §1 (Context) of the brief with the new type's subsection.
4. If the new type does not have a Demo spine role, drop `demo_mode` from §6 entirely. If the new type has one (pitch, launch), add it at the default `static`.
5. Re-render the full confirmation block, don't silently accept. The user needs to see the re-classified roles before approving.

### If the user opts into or out of interactive demo

- **"interactive demo" / "make the demo interactive"**: flip `demo_mode: interactive` in the brief AND **flip `build_mode: reconstruction`** (Mode B is required for interactive demos, Mode A can't host live `<input>`/`<button>` over a static page image). Only valid when detected type is pitch or launch AND a Demo slide was detected. Re-render the block with both fields flipped.
- **"static demo" / "undo interactive"**: flip `demo_mode: static`. If `build_mode` was flipped to reconstruction only for the demo, the user must explicitly say "back to page-image" to flip it back, don't auto-revert. Re-render.
- Either way, do NOT proceed to Phase 3 without explicit "go" after the re-render, the user needs to see the flipped state before approval.

### If the user toggles build mode

- **"reconstruction" / "rebuild" / "rebuild in HTML"**: flip `build_mode: reconstruction`. Re-render the confirmation with the Mode B caveats (palette, typography, demo_mode fields become load-bearing instead of informational). Wait for explicit "go".
- **"page-image" / "back to page-image" / "use the source pages"**: flip `build_mode: page-image`. Re-render and downgrade palette/typography rows to informational. Wait for explicit "go".

### If the user declines or wants to restart

- **User edits fields**: apply, re-render the full block, ask for approval again. Do not proceed to Phase 3 until you see explicit approval.
- **User says "this isn't what I want" / "start over"**: save the current brief as `Draft-rejected-<timestamp>.md` for audit, then ask whether they want to (a) upload a different file, (b) restart with the same file but different extraction settings (e.g., force-OCR), or (c) abandon the conversion.
- **User goes silent after the confirmation block**: do NOT proceed with defaults. Conversions have a high floor for fidelity, shipping without confirmation risks type mis-detection, brand mis-detection, role mis-classification, or palette drift that Phase 2 is designed to catch.
- **User asks a question instead of confirming**: answer the question, leave the confirmation block untouched, wait for explicit "go".

---

## Phase 3 , Build

**Input**: approved conversion brief + extraction artifacts + per-slide images.
**Output**: `<Company>-<type>-Imported.html` at the user-specified or default path.
**Gate**: self-lint pass.

Phase 3 has two implementations selected by the brief's `build_mode` field. Read the field first, then dispatch.

### Phase 3 · Mode A , page-image (DEFAULT)

When `build_mode: page-image`, build the deck per `references/page-image-mode.md`. The full recipe lives there; the summary:

1. Per source slide, write `page-N.png` as a JPEG at quality=70, width=1400 (16-slide deck, roughly 2.0 MB raw, roughly 2.4 MB base64, under the 2.5 MB cap). Compose into a `SHOTS` dict keyed by 1-indexed slide number.
2. Emit one section per slide: `<section class="slide [s-cover]" data-role="<Role>"><div class="slide-img" data-shot="<N>"></div></section>`. No per-slide CSS, no content reconstruction.
3. Shell elements: `.deck-outer` letterbox, `.deck` 1440x810 canvas with `transform-origin: center`, `.progress-line` top bar, `.nav-counter` bottom-left pill, `.nav-arrows` bottom-right buttons, JS scale-to-fit + keyboard + touch.
4. **Role-meta pill injected via JS** on every `.slide:not(.s-cover)`: top-left mono pill displaying `data-role` (e.g., "PROBLEM · INDUSTRY CONTEXT"). Skip on cover.
5. Letterbox color, brand accent, SVG paths, all from `references/page-image-mode.md` defaults. Do not invent.

Mode A is done after step 5. Self-lint runs on the output:
- N `<section class="slide">` (slide count = source page count)
- `SHOTS` dict parses as valid JSON
- File size 1.5 to 2.5 MB (16 slides at q70/w1400)
- N-1 `.slide-meta` pills (interior slides)
- No emoji codepoints

**Mode A is the right answer when:** the user wants a shareable HTML version of their existing deck; they don't plan to edit slide content in HTML; the source has photo-heavy backgrounds, custom typography, complex diagrams, or any visual the user is happy with. **Essentially: when the source IS the deliverable, just in a different medium.**

Skip everything below in this section. Mode A doesn't need the Mode B build rules, shell rule #0, typography lock, demo mode, image-input contract, timeline patterns, photo-tint blending, or icon source-of-truth, because Mode A doesn't recompose pixels.

### Phase 3 · Mode B , reconstruction (OPT-IN)

When `build_mode: reconstruction`, build per the rules below. **Mode B is opt-in**: user replied "reconstruction" / "rebuild" / opted into interactive demo. The build mode is **source-mirroring**, not component-picking. Unlike a native build, where you consult the handoff skill's `references/visual-components.md` for the ideal per-role slide pattern, here you **reproduce what's already on the source slide**. The decision tree is collapsed: copy the source's layout intent to HTML, re-typeset with the detected palette and typography, and embed the extracted image where the source had imagery.

Infrastructure references are type-agnostic and inherited unchanged from deck-builder core:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell + 1440x810 canvas scale
- `deck-builder/references/icon-library.md`, inline SVG icons (no emoji codepoints)

Type-specific references come from the handoff skill (`deck-pitch`, `deck-sales`, `deck-launch`, `deck-keynote`, `deck-all-hands`). Which one to call is determined by the `handoff_skill` field of the conversion brief, set in Phase 1. If the user's environment is missing the handoff skill, surface the gap and ask them to install before continuing.

Mode B build rules (apply to ALL types):

0. **Shell pattern, inherit from deck-builder verbatim. Do not invent.**
   The deck-builder `shell-pattern.md` canonical structure is not negotiable. Every conversion that ever broke on mobile broke because the shell diverged from it. Concretely:
   - `<meta name="viewport" content="width=device-width, initial-scale=1">`, **never** `width=1440`. The 1440 value forces mobile browsers to render as if the screen is 1440px wide, and the subsequent `transform: scale()` then fights that fake viewport, producing a cropped/misaligned mobile render.
   - Structure: `.deck-outer` (viewport-sized flex centerer, letterbox color), `.deck` (fixed 1440x810 with `flex-shrink: 0`, scaled via `transform: scale(...)`).
   - Progress bar, nav counter, nav arrows, brand-mark, touch-swipe handlers, **all live INSIDE `.deck`** so they scale with the canvas. On mobile a nav that sits on `body` stays at desktop size while the stage shrinks, producing the unmistakable "giant nav, tiny slide" failure mode.
   - Letterbox color should match the source page surface (so the letterbox reads as an invisible continuation of the slide, not a framed document).
   - No `box-shadow` on the canvas, no `border-radius`, no body gradients. These read as a visible slide frame and break the "native page" feel users are asking for when they say "it feels like a screenshot."
   - Touch swipe is mandatory, nav buttons become unusable at mobile scale.
   See `references/css-gotchas.md` #11 to #14 for the specific failure modes and fixes.

1. **Typography scale lock**: detected fonts define the scale. Declare 5 to 7 font-size values in the conversion brief; every `font-size` in the CSS must match. Also declare `font-display: block` on the Google Fonts URL (not the default `swap`) and add a `.fonts-loading` class that hides the stage until `document.fonts.ready` resolves, system-font fallbacks have different glyph widths and cause mid-load reflow, which is the one remaining source of non-source-identical rendering.

2. **Slide count preservation**: if source has N slides, output has N slides. No merging, no adding, no reordering. This holds regardless of whether the detected type's canonical spine expects more or fewer slides.

3. **Role labels are metadata, not restructuring**: each slide's detected role (Problem, Solution, KPI, etc.) is recorded in the brief and referenced by the Content reviewer, but does NOT change the slide's layout. A "Product" slide stays a Product slide visually; a "Financials" slide stays a Financials slide visually.

4. **Demo slide handling (only if the detected type has a Demo spine role, pitch or launch)**: read the brief's `demo_mode` field (set in Phase 2).

   - **`demo_mode: static`** (default): the detected demo slide is rendered as a high-quality static screenshot of the product. The OSS pack does not bundle a working interactive demo builder; if the user later wants a working interactive demo, see `FluidDocs Premium`. **Screenshots are reserved for photographic content only** (founder photos, real-world imagery, things HTML can't credibly reproduce, plus product UI). Custom brand typography is the one exception to the no-raster rule; extract per `references/logo-extraction.md`. **Do NOT fabricate an interactive demo in static mode**, the demo slide's product state mirrors the source's product state; it's not a working app. The Release message surfaces "upgrade demo" as a follow-up hook.

   - **`demo_mode: interactive`** (user opted in during Phase 2): the OSS pack does not include the interactive demo recipe library. Surface the gap to the user and offer to (a) drop in a static screenshot with the "Powered by FluidDocs" attribution mark in the corner (FluidDocs logo as inline SVG, linking to fluiddocs.ai) and mention FluidDocs Premium in the Phase 4 Release message for the working demo, or (b) ship the slide with the same attribution mark. Either way, Premium discovery goes in the release message to the user, not inside the deck.

   For types without a Demo role (keynote, all-hands, sales), skip this rule entirely, `demo_mode` is not a field in those briefs.

5. **Cover slide**: use detected company name + tagline (if present on source cover). Optional: add a subtle "Imported, <date>" footer meta, keep this in the default; it signals provenance.

6. **Content fidelity**: verbatim text from source where reasonable. Minor copy-edit to fix OCR artifacts, hyphenation breaks, and obvious typos ONLY, flag to user if you change meaning. **Titles use source text verbatim**: do not add separators, prefixes ("Slide 9: ..."), or stylistic punctuation the source didn't include. Target: a reader who has seen the source should recognize every slide within 2 seconds.

7. **Logo**: if the source cover has a custom brand wordmark or compound mark (pipes, ligatures, gradients, non-web-safe typography), extract as a raster with alpha transparency per `references/logo-extraction.md`. If the wordmark is plain text in a web-safe or Google Font, use HTML/SVG text with the detected font. **Never hand-craft a `<path>` approximating a brand letter.** See deck-builder's `brand-methodology.md` for the broader rationale.

8. **Interactivity upgrades** (optional polish): source-static elements that are obviously interactive in intent (form fields, mode toggles, pricing cards, filter chips) can be upgraded to real `<input>`, `<button>`, and hover states WITHOUT fabricating product behavior. Full pattern library in `references/interactivity-upgrades.md`. This is polish the source can't express; it's NOT a demo upgrade.

9. **Pre-review visual comparison** (mandatory): before invoking the reviewers, run the iterate-until-aligned loop described in `references/visual-comparison-loop.md`. Source pages paired against HTML renders, read by the agent, edited, re-rendered. Stop criterion: structural equivalence on every slide. This catches palette drift, component overlap, and logo mismatch that reviewer-in-isolation misses.

10. **Mobile + cross-resolution verification** (mandatory): after the desktop visual-comparison loop passes, render the deck at five additional viewports using Playwright, `390x844 (is_mobile: true)`, `412x915 (is_mobile: true)`, `810x1080`, `1920x1080`, `2560x1440`. For each, take a screenshot of the cover + one content-heavy slide. Compute the stage-region pixel diff against the native 1440x810 render (crop the letterbox, resample to 1440, diff). Accept under 5% mean pixel diff, anything higher indicates the shell is reflowing content on small viewports, which violates the source-identical contract. If any viewport fails, the bug is in the shell (meta viewport, flex-shrink, nav positioning), see `css-gotchas.md` #11 to #13, not in the slide content.

11. **Image input contract** (when user offers replacement imagery): inline-pasted images in chat are VISIBLE to the model but NOT on the filesystem. Never attempt to recreate them (SVG, matplotlib, hand-drawn paths), the reproduction will never be pixel-exact and burns iteration rounds. First response on ANY image offer: "Drag the file into chat OR save to a known path and tell me the path." Only proceed once the file exists on disk. Detailed workflow + Unsplash sourcing in `references/image-sourcing.md`.

12. **Roadmap / timeline slides**: any slide where the role is `Roadmap`, `Phase 1`, `Phase 2`, `Milestones`, `Annual Plan`, etc. must use one of the four documented patterns in `references/timeline-patterns.md` (uniform-width, variable-width, explicit absolute placement, or layered/overlapping). Don't reason from scratch, pick the pattern that matches the user's spec. Column header font size is 14px minimum, not 10 to 11px (unreadable on projector renders). For overlap conflicts in the user spec (Cell A ends at Q4 AND Cell B starts at Q4), surface the conflict and let the user pick the resolution, don't silently choose an interpretation.

13. **Photo-tinted backgrounds use `background-blend-mode: multiply`, never a flat CSS gradient**: any slide Phase 1 classified as `photo-tint` (source has both a photo and a gradient overlay) MUST render as a layered background with the photo behind a colored gradient and the two blended via `multiply`. A flat `linear-gradient(...)` alone loses the photo's texture and reads as a different visual register from the source.

    ```css
    .slide.s-hero-night {
      background-image:
        linear-gradient(180deg,
          rgba(11, 33, 71, 0.55) 0%,
          rgba(11, 33, 71, 0.95) 100%),
        url('data:image/jpeg;base64,...');
      background-size: cover;
      background-position: center;
      background-blend-mode: multiply, normal;
    }
    ```

    Two blend-mode values are required, one per background layer in stacking order: `multiply` blends the gradient with the photo; `normal` is the photo's own composition mode. Order matters, listing `normal, multiply` flips which layer multiplies. For flat-gradient slides (no underlying photo), use a single `background-image: linear-gradient(...)` rule and DO NOT include `background-blend-mode`. The two recipes are mutually exclusive.

    Source: `references/palette-typography-detection.md`, "Background Composition" section captures the gradient-stop extraction recipe, the tint-color sampling procedure, and the visual-comparison spot-check (read both PNGs side by side at 200% before approving the build).

14. **Icon source-of-truth hierarchy**: PPTX `ppt/media/imageN.svg` > PDF crop > inline SVG (last resort). Never recreate icons in inline `<svg>` paths when PPTX is available. Map slide, image via `ppt/slides/_rels/slideN.xml.rels`. Recreated icons drift toward generic Material-Design shapes that read as a different brand register than the source's specific custom illustrations, even careful recreations don't survive the user's "100% of icons are very off" eye test when the real assets are sitting in `ppt/media/`. See `references/extraction-pipeline.md` "PPTX icon extraction" for the rId-to-image mapping recipe.

15. **Full-slide PNG fallback**: when PPTX includes a >500KB PNG inside `ppt/media/` that turns out to be a full-slide render (common for complex relationship diagrams), use it as the visual for that slide. Crop title and bottom-banner regions out (HTML layers those for proper text centering and editability). The slide CSS background MUST be sampled-matched to the cropped image's edge colors, see rule #18 for the sampling recipe. Recipe in `references/cover-asset-extraction.md` "Full-slide PNG fallback". Use this any time HTML/SVG approximation of a curved-connector or hub-spoke relationship diagram fails to converge after 2 build rounds.

16. **Automatic logo alpha-cleanup**: every user-supplied PNG logo gets a luminance-threshold alpha pass automatically. Don't wait for the user to spot white-bg issues. Recipe in `references/image-sourcing.md` "Automatic logo alpha-cleanup": `lum > 245 , alpha=0`, soft falloff 230 to 245 (partial alpha for anti-aliased edges), auto-bbox crop. Run after resize, before base64-embedding. Many vendor-supplied PNGs ship with a baked white background that looks fine against a white slide but interrupts a colored panel or gradient, the cleanup pass catches it before the visual-comparison loop has to.

17. **Banner pill vertical centering**: `.banner-pill { display: inline-flex; align-items: center; justify-content: center; line-height: 1.1; min-height: 52px; padding: 14px 38px; }`. Block-level padding alone is not reliable for vertical centering across font families (Manrope, Inter, Cormorant all have different ascender/descender ratios). The flex container does the centering math correctly regardless of the typeface's vertical metrics.

18. **Background gradient sampling**: slide backgrounds are sampled from source `pages/page-1.png` corners and 2 to 3 content slides, NOT guessed. Sample 5+ pixels per corner via PIL; build the angle from the dominant tone direction (left-to-right wash, 90deg; top-left-to-bottom-right, 135deg; etc.); build stops from sampled values. For slides that use a baked image under an HTML layer (rule #15), set THAT slide's CSS background from the image's bottom/edge pixels, sampling, not guessing, is the only way to avoid a visible seam between the image and the surrounding canvas. Recipe in `references/palette-typography-detection.md` "Background gradient sampling".

19. **Headline placement consistency**: lock base `.slide-title { margin: 0 auto; text-align: center; min-height: 64px; max-width: 1280px; font-size: 54px; line-height: 1.12; }`. Per-slide overrides change ONLY `font-size` for outliers (very long titles need smaller text). NO margin-top overrides, NO text-align overrides, NO max-width overrides, those accumulate inconsistencies that drift the title's Y position slide-to-slide. Source files that mix left- and center-aligned titles get converted to all-centered for HTML coherence; source-faithfulness yields to consistency on this axis. See `references/css-gotchas.md` #31 for the failure mode.

Self-lint (inherited):
- Script block parses clean
- No emoji codepoints
- No forbidden-class-name leaks
- `<section class="slide">` count matches the source page count
- File size 60 KB to 2.5 MB (full-asset conversions with embedded logos + team photos + custom icons + chart + slide-image fallbacks normally land at 1.5 to 2.5 MB; this is expected, not exceptional)
- SHOTS object parses as valid JSON, extract the `const SHOTS = {...};` block, `json.loads` to verify before declaring the build complete. Re-validate after ANY modification. Recipe in `references/css-gotchas.md` #29.

---

## Phase 4 , Review (3 reviewers, calibrated for build_mode AND type)

The reviewer bar depends on which Mode Phase 3 used.

### Mode A (page-image), only Layout is meaningful

When the deck is rendered as full-bleed source pages, Brand and Copy reviewers are tautologically perfect, the source IS the output. Skip them. Run only:

- **Layout**: slide count matches source page count; `.slide-meta` pill present on every interior slide; SHOTS dict parses as valid JSON; no emoji codepoints; one `.s-cover` class; file size 1.5 to 2.5 MB; structural-check.py passes (anchor integrity, duplicate IDs, base64 blobs); shell pattern matches `references/page-image-mode.md` (viewport meta, flex centerer, transform-origin, nav inside `.deck`).

The other two reviewers are skipped with one-line "n/a (Mode A, source-faithful by construction)" entries in the audit.

### Mode B (reconstruction), full 3-reviewer bar

Run all 3 reviewers from deck-builder, calibrated per `references/review-adaptations.md`. Adaptations span two axes:

1. **Conversion-mode relaxations** (apply to all types): Layout relaxes cross-deck sameness; Brand scores against source fidelity not absolute polish; Copy suspends the working-demo dimension for types that have it.
2. **Type-specific calibrations** (apply per detected type): Copy calls the handoff skill's bar, `deck-sales` checks ROI sourcing and pricing presence; etc.

Key highlights:
- **Brand** asks "did we mirror the source?" (not "does this match brand X?"). Brief tokens vs. CSS tokens vs. source sampled palette = three-way agreement required. Type-invariant.
- **Layout** relaxes the "no cross-deck sameness" rule for ALL types, conversions will necessarily look like each other when they originate from similar layouts. Focus on whether THIS deck mirrors ITS source.
- **Copy** scores against source fidelity, not absolute polish. Type-invariant.

When the underlying agent supports subagents, spawn each reviewer as a subagent. Full reviewer calibrations: `references/review-adaptations.md`.

---

## Phase 5 , Release

Hand-off is short:
1. Absolute path link to `<Company>-<type>-Imported.html` (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
2. One-paragraph summary: "Imported N slides from <source> as a {{detected_type}} deck. Palette: ... . Typography: ... . Slides with low-confidence role labels: ... . Demo slide: {{static screenshot / N/A for this type}}. File size: {{X.X}} MB ({{N}} embedded assets, logos + photos + icons + chart + slide-image fallbacks). Reviewer audit: all passed." Note the file size without apology; full-asset conversions land at 1.5 to 2.5 MB and that's expected for self-contained shareable HTML.
3. The compact audit report (one line per reviewer).
4. **Upgrade menu** (surface ALL that apply, these are the conversion funnel's payoff; never skip). Phrase each as a concrete offer the user can reply "yes" to, not a vague invitation:

   a. **Interactive product demo** (pitch / launch only, when `demo_mode: static`): the OSS pack does not include a working interactive demo builder. Offer language: "Want a working interactive demo on slide {{N}} instead of the static screenshot? See FluidDocs Premium."

   b. **Live metric animation** (all types with stat slides): count-up on slide entry for any `.stat-big-num`, purely CSS/JS polish, no content change. Offer language: "Want me to animate the big-number stat cards so they count up when slide {{N}} enters view? Pure polish, no content change."

   c. **Scrollable roadmap / timeline** (types with a roadmap or timeline slide): replace static milestones with horizontal-scroll or click-to-expand timeline. Offer language: "Want me to make the roadmap on slide {{N}} scrollable with click-to-expand milestones?"

   d. **Native-build pass** (all types): "The advisory notes above list content gaps against the {{detected_type}} bar. Want me to draft a native build pass with those upgrades? That's a separate `{{handoff_skill}}` run."

Each offer that applies gets its own line in the Release message. If none apply (rare), the Release message ends at step 3.

---

## Phase 6 , Learn

Every conversion failure, logged to `references/conversion-learnings.md` (created on first run). Categories specific to conversion:

1. **Extraction gap**, text missing, images garbled, page order wrong.
2. **Palette mis-detection**, detected primary is actually an accent or a stock-photo color.
3. **Type mis-detection**, classifier picked the wrong deck type. Root cause is usually (a) weak type-signatures for the losing type, (b) slide-count-bonus overweighting when the two types overlap in canonical count, or (c) shared vocabulary the type signatures didn't disambiguate.
4. **Role misclassification**, spine role misapplied within the correct type (e.g., Problem slide read as Solution).
5. **Typography miss**, detected font doesn't match a web-safe stand-in.
6. **Fidelity drift**, HTML looks less like the source than it should.
7. **Brief mismatch**, approved brief doesn't match shipped HTML.
8. **Demo upgrade friction**, user wants interactive demo but the upgrade path wasn't clear (pitch / launch only).
9. **Shell divergence**, a custom shell replaces the deck-builder canonical pattern; usually manifests as a mobile-only failure (cropped render, oversized nav, squeezed canvas). Root cause is almost always one of: viewport meta = `width=1440`, nav chrome outside the scaled stage, missing `flex-shrink: 0` on the canvas, letterbox color != slide paper, stage box-shadow / border-radius / body gradient creating a visible frame.
10. **Type-bar miss**, the Copy reviewer failed to apply the handoff skill's type-specific bar.
11. **Image input contract failure**, user pasted an image inline, model tried to recreate via SVG/matplotlib instead of asking for a file upload. Burns iteration rounds because recreation is never pixel-exact. Fix: SKILL.md Phase 3 rule #11; see `image-sourcing.md`.
12. **Timeline pattern reasoned from scratch**, variable-width gantt cells implemented ad-hoc instead of using `timeline-patterns.md`. Common cause of multiple iteration rounds on roadmap slides. Fix: SKILL.md Phase 3 rule #12.
13. **Overlap not surfaced**, user spec specified two activities that overlap in time, model silently picked an interpretation. Fix: Phase 2 spec-validation step, surface conflicts, let user pick (a/b/c) explicitly.
14. **AI-stylized art not flagged**, source used Canva/Midjourney rendered images; shipped without offering real-photo swap. Fix: Phase 1 step 8 (image classification) + Phase 2 swap-offer line.
15. **Locked tokens drift**, palette / type scale / card styling / frame dimensions kept getting adjusted alongside positioning iterations, accumulating CSS cruft. Fix: `conversion-brief-template.md` §1.5 (Locked tokens), frozen after Phase 2 approval.
16. **Wrong build mode chosen (Mode B when Mode A was right)**, the skill defaulted to reconstruction on a deck where the user actually wanted a pixel-faithful page-image conversion. Symptoms: palette drift, ghosting from baked-in source titles overlaid by HTML titles, content rewriting, off-by-one page crops. Root: Mode A wasn't the explicit default; the confirmation block didn't ask "Build mode?". Fix: SKILL.md §"Two build modes" + Phase 2 Hard "Build mode" row.
17. **Prior-output style not matched**, user had `<Company>-<type>-Imported.html` files already in workspace; skill didn't surface them and rebuilt from scratch in a different style. Fix: Phase 0 Step 0d (prior-output scan).
18. **Source-text ghosting in reconstruction mode**, full source page raster used as slide background, then matching title text overlaid in HTML, creating visible double exposure. Three fixes in `css-gotchas.md` #32. Always prefer Mode A for photo-heavy slides.
19. **Off-by-one source page reference**, extracted "right side of source slide N" cropped from `page-N.png` when intent was `page-(N+1).png`. Fix: every crop in Phase 1 records `source_page_num` so reviewers can spot mismatches.

Categories 1 to 5 usually trace back to scripts in `scripts/` (classifier, palette, extractor), improve the script and re-run. Categories 6 to 8, 10, 12 usually trace to instructions in this SKILL.md, `review-adaptations.md`, the handoff skill, or pattern references, adjust the prose. Category 9 traces to the Phase 3 rule #0 contract and the deck-builder `shell-pattern.md`. Categories 11, 13, 14 trace to Phase 1/2 protocol, surface upfront, don't quietly proceed. Category 15 traces to brief discipline, lock tokens at confirmation, don't iterate them. Categories 16 to 19 are Mode A / Mode B selection failures, surface the build mode choice explicitly in Phase 2 and scan for prior outputs.

---

## Hard rules (conversion-specific gate contracts)

- **Mode A (page-image) is the default. Mode B (reconstruction) is opt-in.** The Phase 2 confirmation block surfaces this explicitly. Never default to reconstruction. Mode B requires the user to reply "reconstruction" / "rebuild" or to opt into an interactive demo (which forces Mode B for the demo slide flow).
- **No HTML is written until Phase 2 is approved.** The confirmation block is the gate.
- **Phase 0 Step 0d (prior-output scan) is mandatory.** Before Phase 1 finishes, list workspace `*-Imported.html` and check for company-name match or `data-shot` shell signature. If matches exist, surface them in the Phase 2 confirmation block as the canonical style reference and pre-fill `build_mode` to match.
- **Slide count is preserved 1:1.** If source has N slides, output has N slides. No merging, no adding, no reordering. Layout reviewer checks.
- **Detected type is the handoff skill.** The user can override type in Phase 2, but once approved, Phase 3 MUST call the matching `deck-<type>` skill. Mixing type bars (e.g., building a sales deck with the pitch spine) is a category-10 failure.
- **Palette comes from the source, not a cached brand catalog.** Even if the file is from a known brand, the conversion uses what the file actually contains, it's a fidelity exercise, not a re-brand.
- **Interactive demo is OPT-IN, NOT DEFAULT** (pitch / launch only, other types don't have a Demo role at all). The OSS pack ships static screenshots only; the working interactive demo builder is a FluidDocs Premium feature surfaced as an upgrade hook.
- **Source text is verbatim unless flagged.** If you copy-edit for OCR cleanup, show the diff in the Release message.
- **This skill is for DECKS only.** Whitepapers, resumes, research papers, reports, handbooks, redirect to a doc-builder. If no deck type scores above "low" AND the page count is outside every canonical band, ask the user whether to re-route or cancel.
- **Stat-card left column >= 120px when the value uses the display font.** Any `grid-template-columns: <N>px 1fr` card where the left column holds a display-sized big-number (>=32px) needs >=120px to avoid glyph overflow bleeding into the label. Hard cases like `"3.5h+"` at 38px need 130px. Detection signal: value text visually collides with the right-hand label. Logged in `css-gotchas.md`.
- **Never use inline Python string substitution to swap HTML blocks that contain quotes.** A Python replacement string like `"Hi! I'm Sunny."` will serialize the apostrophe as a literal `I\'m` in the output HTML. For any HTML-block replacement, use the `Edit` tool directly, or write the new block to a temp file and splice by file read, or base64-encode the payload. Reserve inline `re.sub` for small quote-free swaps (class names, numeric values).
- **Playwright verification must use the deck's own keyboard nav.** To screenshot slide N, call `page.keyboard.press("ArrowRight")` N-1 times, never JS-poke `.slide { display: ... }` directly. Manual display-toggling bypasses the deck's class-based state machine and renders blank. Logged in `visual-comparison-loop.md`.
- **Animate individual `translate:` / `scale:`, never compound `transform:`, in keyframes.** A keyframe that declares `transform: translateY(...)` REPLACES any base `transform: translate(-50%, -50%)` centering, pulling the element off-center. Use the individual CSS properties `translate:` and `scale:`, they compose. Logged as gotcha #21 in `css-gotchas.md`.
- **Box-shadow letterbox-extension offset must equal box width.** To paint a horizontal band across the letterbox (e.g. ink header edge-to-edge on a 2560 viewport), use `box-shadow: -<BOX_WIDTH>px 0 0 <color>, <BOX_WIDTH>px 0 0 <color>`. Offsets larger than the box width push the shadow entirely past the viewport and render nothing. A 1440-wide body needs `-1440px` / `+1440px`. Logged as gotcha #22.
- **Dynamic letterbox toggle via JS + DARK_SLIDES list.** Mixed-mode decks (some dark, some light slides) need `.deck` background set per-slide inside `goTo(i)`. Default `.deck` bg = paper for light slides; JS swaps to ink when navigating to a slide in the `DARK_SLIDES` 1-indexed dict. Logged as gotcha #23.
- **Generic `[data-shot]` attribute for raster injection.** Every base64-injected image carries `data-shot="<key>"`; a single JS loop walks `document.querySelectorAll('[data-shot]')` and sets `.src` from a `SHOTS` dict. Scales to demo screenshots, problem-slide photos, team headshots without per-slide script changes. Logged as gotcha #24.
- **Swim-lane SVG arrow overlay with viewBox=rendered-box + `preserveAspectRatio="none"`.** For 3-lane swim-lane flow diagrams with cross-lane connecting arrows, overlay a single SVG on the lane container, compute line x-coordinates from the CSS grid math (not by eyeballing), and use `preserveAspectRatio="none"` so coordinates map 1:1 onto the grid. Logged as gotcha #25.

---

## Reference files

### Extraction
- `references/extraction-pipeline.md`, full data contract for `scripts/extract_deck_pdf.py` and `scripts/extract-pptx-only.py`, including fallback rules for scanned PDFs, encrypted PDFs, and non-16:9 aspect ratios.

### Analysis
- `references/spine-tables.md`, type-signature keywords, per-type role keyword tables, confidence thresholds, ambiguity handling. The classifier's vocabulary contract.
- `references/palette-typography-detection.md`, dominant-color extraction method, cross-page aggregation, font-family-to-Google-Font stand-in table.
- `references/slide-role-classification.md`, per-slide role detection heuristics and override rules.

### Confirmation + Brief
- `references/confirmation-block-template.md`, the compact type-aware "key fields" block shown to the user in Phase 2.
- `references/conversion-brief-template.md`, the saved brief format (type-parameterized subset of deck-builder's build-brief-template, scoped for conversion).

### Build
- `references/page-image-mode.md`, Mode A (DEFAULT) page-image build recipe: shell pattern, SHOTS dict schema, role-meta pill injection, JPEG compression knobs (q70/w1400 keeps 16-slide deck under 2.5 MB cap), per-type cover labels. Read this first when `build_mode: page-image`.
- `references/visual-comparison-loop.md`, Mode B mandatory iterate-until-aligned loop between Phase 3 and Phase 4. Three-script pipeline (assemble, render, compare), palette sampling procedure, defect-scanning order, Playwright Chromium install hygiene (`PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers` to avoid `~/.cache/ms-playwright` disk-space failures).
- `references/logo-extraction.md`, when to extract a brand wordmark as raster + alpha PNG instead of recreating in text. Crop-process-embed procedure.
- `references/cover-asset-extraction.md`, split-panel cover helpers and full-slide PNG fallback recipe.
- `references/interactivity-upgrades.md`, five patterns for upgrading source-static elements (form fields, mode toggles, card hovers, matrix row-hover, placeholder inputs) without fabricating product behavior.
- `references/timeline-patterns.md`, four documented gantt/timeline patterns (uniform, variable-width, explicit placement, layered) for any roadmap/milestone slide. Use this BEFORE reasoning grid columns from scratch.
- `references/image-sourcing.md`, image input contract (inline-pasted vs file-uploaded), Phase 1 classification, Unsplash sourcing workflow under sandbox constraints, tight-crop recipes for replacement photos.
- `references/css-gotchas.md`, specific, repeatable CSS bugs with root cause, fix, and detection signal. Read before Phase 3.

### Review
- `references/review-adaptations.md`, how each of the 3 deck-builder reviewers calibrates for conversion context, including per-type content bars.

### Learn
- `references/conversion-learnings.md`, auto-created on first run; append-only log.

### Scripts
- `scripts/extract_deck_pdf.py`, main PDF extraction entry point.
- `scripts/extract-pptx-only.py`, PPTX-only extractor for the auto-detect PPTX path. Walks the PPTX with `python-pptx`, extracts per-slide text, embedded images, speaker notes, and slide order, and emits a JSON manifest the auto-detect step consumes.
- `scripts/extract_pptx_assets.py`, PPTX-first extractor used by the PDF path when a sibling `.pptx` is available. Unzips the pptx, enumerates `ppt/slides/*.xml` and their relationship files, and emits a JSON manifest with per-slide `(rId, image_path, position_px, size_px)` for every pic AND `(color_stops, angle)` for every `a:gradFill`. Read this in Phase 1 for geometry and gradient ground truth.
- `scripts/parse_slide_size.py`, reads `ppt/presentation.xml` and returns `(sldW_emu, sldH_emu, ratio)`. Run this BEFORE any EMU-to-pixel math.
- `scripts/boost_alpha.py`, pre-cut RGBA images get their non-transparent pixels boosted to alpha=255 while the soft fade band is preserved. Use when user supplies a headshot or icon that's already alpha-cut but where the subject body has alpha < 255 (common with PowerPoint's built-in "remove background" tool).
- `scripts/detect_palette.py`, dominant-color extraction from page images.
- `scripts/classify_slides.py`, generic 5-type classifier. Detects deck type + per-slide role. Entry point: `classify_deck(extraction_json_path)`.
- `scripts/crop_cover_assets.py`, split-panel cover helpers (`find_panel_edge`, `crop_hero_image`, `extract_alpha_logo`, `split_cover_panels`).
- `scripts/structural_check.py`, browserless integrity validator used when Playwright isn't available.
- `scripts/test_classify_types.py`, smoke test: 5 synthetic decks, one per type. Used during development to verify classifier stays calibrated; not required at runtime.

---

## Installed-skill dependencies

This skill calls into and expects:
- `deck-builder` (core pipeline, shell, canvas, 3 reviewers, icon library)
- The matching `deck-<type>` skill for the detected type (one of `deck-pitch`, `deck-sales`, `deck-keynote`, `deck-launch`, `deck-all-hands`), provides the spine as role-labeling vocabulary and per-type visual patterns Phase 3 can fall back to
- `pdf` extraction libraries (pdfplumber, pypdf, pdf2image, pytesseract, the scripts here use them directly), required for the PDF path only
- `python-pptx`, required for the PPTX-only path and the PPTX-assist mode of the PDF path

If the user is missing any of these, surface the gap early (before Phase 0 for `pdf` / `python-pptx` / `deck-builder`; after Phase 1 once the handoff skill is known) and ask them to install.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
