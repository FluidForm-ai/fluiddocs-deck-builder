# Conversion Learnings Log

Append-only log of conversion failures and the checklist items that now prevent them. Every user-reported issue on a conversion lands here. Starts empty; grows with each build.

Columns (pipe-separated for readability):

| Date | Source | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|---|

Categories (from SKILL.md Phase 6):
1. Extraction gap, text missing, images garbled, page order wrong
2. Palette mis-detection, detected primary is actually an accent or photo color
3. Role misclassification, Problem slide read as Solution, etc.
4. Typography miss, detected font doesn't match a web-safe stand-in
5. Fidelity drift, HTML looks less like the source than it should
6. Brief mismatch, approved brief doesn't match shipped HTML
7. Demo upgrade friction, user wants interactive demo but upgrade path wasn't clear

---

## Log

### Run 1, first real conversion (22-slide Canva-authored pitch)

**Run context**: 22-slide Canva-authored pitch deck. Tested both the skill's pipeline and two upgrade paths (photo-only raster rule, interactive affordances).

**Issues encountered**:

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 1 | 5. Fidelity drift | First build embedded entire page screenshots as raster, not a conversion, a source-in-an-HTML-shell | Rebuild in pure HTML/CSS/SVG; rasters only for founder photos | SKILL.md Phase 3 rule #4 rewritten, screenshots reserved for photographic content only |
| 2 | 2. Palette mis-detection | HTML used aggressive warm orange wash; source was near-white (#F9F9F9) with a subtle BR corner gradient | Sample corners + center on page 2 with PIL; rebuild `.slide` background as radial-anchor only | New file `visual-comparison-loop.md` §Palette sampling; first thing to do each run |
| 3 | 5. Fidelity drift | `FLUID\|form` wordmark rendered in CSS text drifted visually from source's custom compressed sans-serif | Extract source logo as alpha PNG, embed base64 as shared `LOGO_IMG` constant | New file `logo-extraction.md`, when and how to extract a wordmark as raster |
| 4 | 5. Fidelity drift | Scale-to-fit canvas drifted up-and-left on resize because transform applied both translate and scale | Use `transform: scale(s)` only; flex parent centers | `css-gotchas.md` §1 |
| 5 | 6. Brief mismatch | Arrow in CSS content rule rendered as literal `\2192` text | Double-backslash in Python f-string resolved to `\\2192` in CSS; fix to single backslash | `css-gotchas.md` §2 |
| 6 | 5. Fidelity drift | "Features" pill overlapped wordmark on feature slides | `.wm-stack` was absolute; override with `position: static` inside `.s-feat-head` | `css-gotchas.md` §4 |
| 7 | 5. Fidelity drift | Slide 4 crosses rendered as horizontal bars, not plus signs | Rebuilt `.s04-tick` with `::before` (horizontal) + `::after` (vertical) | `css-gotchas.md` §7 |
| 8 | 5. Fidelity drift | Cover wordmark letters wrapping / shrinking (`FLUID \| f o r`) | Added `flex-shrink: 0` and `white-space: nowrap` to cover-left and wordmark | `css-gotchas.md` §6 |
| 9 | 7. Demo upgrade friction (inverse) | User wanted SOME interactivity polish but NOT a faked product demo | Added `<input>` in form slide, `<button>` toggles on mode selectors, card hovers, all no-fabrication patterns | New file `interactivity-upgrades.md`; Phase 3 rule #8 added |
| 10 | 5. Fidelity drift | Reviewer-in-isolation missed component overlap because no one was paired source-vs-HTML | Added mandatory visual comparison loop as Phase 3 to Phase 4 gate | New file `visual-comparison-loop.md`; Phase 3 rule #9 added |

**Net new reference files**:
- `visual-comparison-loop.md`, pre-review iterate-until-aligned loop
- `logo-extraction.md`, raster extraction for custom wordmarks
- `interactivity-upgrades.md`, no-fabrication polish patterns
- `css-gotchas.md`, specific repeatable bug catalog

---

### Run 2, second real conversion (20-slide Canva-authored pitch)

**Run context**: 20-slide Canva-authored pitch deck. Surfaced a new class of bug: the SHELL itself was wrong, not the slide content. Three rounds of user feedback escalated from cosmetic ("feels like a screenshot") to structural ("resolution lock not working on mobile").

**Issues encountered**:

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 1 | 5. Fidelity drift | HTML looked like a static rendering, no entrance animations, no hover states, no click affordances | Added interactivity layer: staggered entrance animations, glow pulse on highlight bubble, click-highlight on competition bubbles, card pulse feedback, partner grayscale hover | `interactivity-upgrades.md` already covered the patterns; checklist item: always apply them to conversion builds, not just on demand |
| 2 | 5. Fidelity drift | User: "whitespace on all sides doesn't make sense." Letterbox was `#E9ECEE` gray against `#FFFFFF` slide; stage had `box-shadow` creating a visible framed-page edge | Remove stage box-shadow and body gradient; match letterbox color to slide paper so the slide edge becomes invisible | `css-gotchas.md` #14 added; SKILL.md Phase 3 rule #0 now forbids stage shadow / border-radius / body gradient |
| 3 | **Shell divergence** (new category) | User: "resolution lock not working, this is how it renders on mobile." Screenshot showed a cropped slide fragment in the middle of the phone screen. Root cause: `<meta viewport content="width=1440">`, nav chrome on `body` (not inside scaled stage), no `flex-shrink: 0` on canvas | Rewire shell to match deck-builder `shell-pattern.md` verbatim: `width=device-width` viewport, nav inside `.deck`, `flex-shrink: 0` + `min-width: 1440px` on canvas, touch swipe | `css-gotchas.md` #11 to #13 added; SKILL.md Phase 3 rule #0 added, shell is inherited verbatim from deck-builder, not reinvented |
| 4 | 5. Fidelity drift | Potential mid-load reflow: Google Fonts `display=swap` default means system-fallback renders first, shifts to real font, wrap points change briefly | Switch to `display=block` + `fonts-loading` class that hides the stage until `document.fonts.ready` resolves (3s timeout fallback) | `css-gotchas.md` #15 added; SKILL.md Phase 3 rule #1 extended with font-gate instruction |

**Category added to Phase 6 list**: "Shell divergence, custom shell replaces the deck-builder canonical pattern; usually fails on mobile first." Until this run, conversion failures were content-level (palette, logo, wrap). Shell-level failures hit a different axis and need their own review pass.

---

### Run 3, 15-slide consumer AI pitch

**Source:** 15-page generated deck, toy company.

### Failures caught + fixed
1. **Slide 2 stat-card overflow (Layout)**: `.stat-card { grid-template-columns: 90px 1fr }` was too narrow for "3.5h+" at 38px, text bled into the "Daily Screen Time" label. **Fix:** widened to `130px 1fr` and bumped gap to 18px. **Rule:** When a stat big-number is >=36px display font, the left column must be >=120px. Add to css-gotchas.
2. **Emoji codepoint check**: 61 instances of U+2713/U+2717/U+26A0 failed mechanical check. **Fix:** Custom glyph system, `<span class="gly-ok/no/wn"></span>` + CSS `::before { content: '\2713' }` escape sequences. Zero codepoints in final.
3. **Slide 3 image crop bleed**: First crop of toy photo included sliver of "conversations with children" text. **Fix:** Tightened crop y-start.

### Reusable patterns
- Custom glyph replacement (CSS escape-sequence) is now the default way to handle check/cross/warning glyphs in source decks.
- Stat-card min-column rule: 120px minimum for any grid-template-columns containing a display-font stat big-number.

### Phase 5 upgrade run (same source): swap static slide 3 for interactive AI demo

**Context:** After the 6-phase pipeline shipped, offered a post-release upgrade: replace the static three-toys product photo on slide 3 with a working chat-stream demo. (The OSS pack does not bundle a working interactive demo builder; this run was historical, captured here for the failure modes it surfaced.)

**Failures caught + fixed**

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 11 | Build-hygiene | Python `re.sub` replacement string containing an apostrophe (`"Hi! I'm Sunny."`) serialized as `I\'m` in the output HTML, literal backslash survived into the rendered text | Edit tool directly, or write markup to a temp file and splice by file read. Reserve inline `re.sub` for quote-free swaps | SKILL.md Hard rules section, new rule forbidding inline-Python HTML replacement with quotes |
| 12 | Verification | Trying to force slide N visible in Playwright via `document.querySelectorAll('.slide').forEach(s => s.style.display = ...)` bypassed the deck's class-based state machine and rendered blank | Always use `page.keyboard.press("ArrowRight")` N-1 times to advance via the deck's own nav | SKILL.md Hard rules + `visual-comparison-loop.md`, keyboard nav is the only way to advance |
| 13 | Phase-5 process | Post-release upgrade was offered ad-hoc with no structured menu. User said yes, but the conversion funnel would benefit from a repeatable offer set | Expanded Phase 5 bullet 5 into a structured upgrade menu with 3 categories: metric animation, scrollable roadmap, native-build pass | SKILL.md Phase 5, upgrade menu block |

---

### Run 4, 15-slide EV charging pitch (split-panel cover)

**Source**: 15-slide investor deck for an EV charging marketplace. Split-panel cover (navy left / photo right) with white custom wordmark on the navy.

### Failures caught + fixed

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 14 | 5. Fidelity drift | Cover hero JPEG cropped at `x=0.39` hard-coded fraction; actual panel boundary was at x=0.499. Crop carried 10% of navy background plus wordmark + tagline fragments visibly bleeding into the right-hand hero. | Pixel-scan the panel-to-panel brightness transition. New helper `scripts/crop_cover_assets.py::find_panel_edge` samples every 20th row, returns first column where row-averaged brightness jumps >=40 units. Re-crop from `edge + 2`. | New file `cover-asset-extraction.md`; new script `scripts/crop_cover_assets.py`; `css-gotchas.md` #20. |
| 15 | 5. Fidelity drift | Logo PNG extracted via luminance-threshold alpha pass (`np.where(lum > 240, 0, 255)`), white wordmark on navy panel. Luminance threshold kept every navy pixel fully opaque, so the PNG baked a navy rectangle into the logo; placed back on the panel, a visible dark frame surrounded the wordmark. | Switch to **color-distance** alpha: pixels within euclidean RGB distance `tolerance=30` of the sampled panel color, alpha=0. New helper `extract_alpha_logo` in same script. `logo-extraction.md` edge-case section rewritten with full recipe + tolerance guidance. | `logo-extraction.md` §"Edge case: monochrome wordmarks on colored backgrounds", now the full color-distance recipe with 20/30/45 tolerance guidance. |
| 16 | 7. Demo upgrade friction | User requested interactive phone-frame demo for the Solution slide post-release. No reusable demo starter existed for map-first mobile consumer products. (The OSS pack does not bundle a working interactive demo builder.) | Captured the phone-frame + pin-map + pay-sheet + charging-ring pattern as a starter idea. | n/a in OSS. |
| 17 | Verification | Playwright refused to install (disk full on sandbox `/` partition, chromium download failed). No visual loop possible. | Added `scripts/structural_check.py` fallback, 7 mechanical checks (slide count, emoji codepoints, duplicate IDs, anchor integrity, base64 blob parseability, era fragments, cover-panel sanity). Catches roughly 80% of real defects without a browser. Exits 0/1/2. | `visual-comparison-loop.md` §"Fallback when Playwright can't install" added. |

### Net new reference files
- `references/cover-asset-extraction.md`, split-panel cover decision tree + scan-then-crop flow + post-extraction visual verification recipe.
- `scripts/crop_cover_assets.py`, agent-callable: `find_panel_edge`, `crop_hero_image`, `extract_alpha_logo`, `split_cover_panels`.
- `scripts/structural_check.py`, browserless integrity validator.

### Net new SKILL.md rules (to codify)
- Split-panel covers MUST use `find_panel_edge` for the hero crop, never hard-code fractional splits.
- Logos on colored panels MUST use color-distance alpha, not luminance threshold.
- If Playwright install fails, run `structural_check.py` as the Phase 4 gate and record the fallback in the brief appendix.

---

### Run 5, 14-slide beverage hardware pitch, video demo

**Source**: 14-slide pitch deck for premium home brewer beverage tech. AI-rendered cinematic stock photos throughout. User also supplied a HEVC product demo video for slide 3.

### Failures caught + fixed (this run alone, 7 user-feedback rounds)

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 18 | Image input contract | User kept pasting images inline ("here's the radar", "here's the timeline screenshot"). Burned 4 to 5 rounds approximating them with SVG/matplotlib while they thought the actual file was in use. Inline-pasted images are visible to the model but not saved to disk. | First time a user offers an image, respond with the upload contract before doing anything else: "Drag the file into chat OR save directly to /img/ with this exact filename." Only proceed after the file exists on disk. | SKILL.md Phase 3 rule #11 added (image input contract); new `references/image-sourcing.md` documents the inline-vs-file gap and the right workflow. |
| 19 | Fidelity drift | Source photos were AI-generated stock (gold-swirl espresso, dark teal cold brew). User wanted real photography. Option wasn't surfaced until round 5, after multiple recropping passes. | Phase 1 image classification step: tag each extracted image as `photographic-real` / `ai-stylized` / `illustration` / `chart`. If any are `ai-stylized`, surface a Phase 2 confirmation line: "Source uses AI-rendered stock for N images. Keep these, or pull stock-photo alternatives?" | SKILL.md Phase 1 step 8 added (image classification); confirmation-block-template.md gets a new optional `ai_imagery_swap` line. |
| 20 | Fidelity drift (cropping) | Image crops bled into adjacent slide content, product thumbs on slide 5 included sliver of the headline text because crop bounds were roughly 5% too wide. | Pixel-scan algorithm uses TWO orthogonal scans (one row + one column at slide midpoints), and rejects any detected content region that intersects with a `pdfplumber` text bbox on the same slide. Tighten margins by 2 to 3% inward after detection to avoid edge slivers. | `extraction-pipeline.md` §"Image bounding boxes" rewritten with the dual-scan + text-bbox-rejection recipe. |
| 21 | Fidelity drift (timelines) | Variable-width gantt cells (Prototyping spans 2 quarters, others span 1) were not a documented pattern. Each iteration of "make this cell wider" was reasoned from scratch. Took 3 rounds to land. | New `references/timeline-patterns.md` with three worked recipes: uniform-width gantt, variable-width gantt with `grid-column: span N`, and a worked example resolving overlap conflicts. | New file `references/timeline-patterns.md`; SKILL.md Phase 3 rule #12 added pointing to it for any roadmap/timeline slide. |
| 22 | Brief mismatch / overlap detection | User spec: "Initial Production Run end at Q4 2026" AND "Full Product Launch start at Q4 2026", those overlap at Q4. Silently picked an interpretation. User would have appreciated the call-out. | When user spec creates a Q-column overlap, surface it before implementing: "These overlap at Q4 2026, pick (a) A ends start of Q4, (b) B starts start of next, (c) literal overlap with z-stacking." | SKILL.md Phase 2 spec-validation step added; same rule applies to any user spec that maps to grid-column positions. |
| 23 | Fidelity drift (title verbatim) | Inserted `·` separators into slide titles ("Timeline and Milestones · Phase 1") and cover labels ("Pitch Deck · Beverage Tech") that the source didn't have. User flagged and asked for removal. | Titles use SOURCE TEXT VERBATIM. Do not add separators, prefixes (e.g., "Slide 9:"), or stylistic punctuation that the source didn't include. If the source has no separator between "Milestones" and "Phase 1", neither does the HTML. | SKILL.md Phase 3 rule #6 (content fidelity) extended with explicit "no added punctuation in titles" clause. |
| 24 | Component visual weight | Slide 4 had a user-provided radar image with a baked-in black border. To "match" it, a similar border was added to the Competitors card. This made BOTH components look like floating boxes and emphasized the disconnect, not reduced it. The fix was the opposite: remove the matching styling. | When one component on a slide has a baked-in visual frame, do NOT add similar styling to siblings. Either crop the frame out of the asset, or leave the other components in the deck's default surface treatment so the framed asset reads as an inset, not a competitor. | `css-gotchas.md` #21 added: "Don't echo a baked-in frame, it doubles the visual weight, doesn't balance it." |
| 25 | Thumb visual consistency | Three product thumbnails (slide 5) at the same 150x150 frame still looked different sized because one image (blue shield) had significant dark periphery while the other two filled their frames. User read this as the frame being a different size. | When generating square thumbs from variable source images, apply an additional 10 to 15% inward tighten so the SUBJECT fills the visible area at roughly the same ratio across all thumbs. Pure cover-crop is insufficient when source compositions vary. | `extraction-pipeline.md` §"Thumb generation" updated with the subject-tighten step. |
| 26 | Sandbox image fetch | Curl, wget, and Python urllib are blocked. `web_fetch` has a provenance check (URL must have appeared in user message or prior web_fetch). Couldn't download Unsplash CDN URLs even after the user picked from a comparison page. | Two workarounds work today: (a) build a comparison HTML page that loads images directly from Unsplash CDN; user right-clicks, Save As, /img/. (b) User pastes the direct CDN URL in a message, which puts it in provenance and unblocks web_fetch. Both documented in new `image-sourcing.md`. | New `references/image-sourcing.md`, workflow for sourcing replacement photos under sandbox constraints. |
| 27 | Iteration cost | The styling brief was never locked. Each round adjusted borders, padding, photo dimensions, then user flagged a related issue, then adjusted adjacent styling, accumulating CSS cruft. Roughly 7 rounds of iteration. | Phase 2 brief MUST lock these tokens explicitly before Phase 3 starts: palette HEX values, type scale (5 to 7 sizes), card styling (border, padding, radius, surface), photo crop dimensions, thumb dimensions. After "go" these are frozen, only content/positioning iterates in subsequent rounds. | `conversion-brief-template.md` §"Locked tokens" section added at top of brief, distinct from the editable per-slide sections. |

### Net new reference files
- `references/timeline-patterns.md`, uniform / variable / overlapping gantt patterns with CSS recipes.
- `references/image-sourcing.md`, image input contract + Unsplash workflow + AI-stylized swap option.

### Net new SKILL.md rules
- Phase 1 step 8: classify extracted images by content type; flag AI-stylized for Phase 2 swap offer.
- Phase 2 spec-validation: surface overlap conflicts in user-supplied positioning specs before implementing.
- Phase 3 rule #6 extended: titles verbatim, no added punctuation.
- Phase 3 rule #11 added: image input contract, never start recreating until file is on disk.
- Phase 3 rule #12 added: any roadmap/timeline slide must use one of the documented patterns from `timeline-patterns.md`.
- `conversion-brief-template.md` Locked Tokens section at top.

---

### Run 6, founder-services sales deck (PDF-first then PPTX surfaced)

**Source**: editorial sales/proposal deck. Photographic backgrounds (night sky, mountains, milky way) tinted with a navy color gradient via `background-blend-mode: multiply`, custom `<a:custGeom>` semicircle "logo straddle" shapes sitting on a wave divider, Cormorant Garamond display headlines with compound hyphens. A `.pptx` of the same source was uploaded mid-run (round 9 of 12), surfacing the biggest skill-level miss of this run, PPTX extraction is roughly 5x higher fidelity than PDF-only and would have eliminated roughly 8 of 12 iteration rounds had Phase 0 checked for it first.

### Failures caught + fixed

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 28 | 5. Fidelity drift / shell divergence | Six slide-type classes (`.s-cover`, `.s-services`, `.s-ty`, etc.) declared `position: relative`, which overrode the base `.slide { position: absolute; inset: 0 }` rule. Slides sized to their content height instead of filling the 810px canvas. | Never declare `position: relative` on slide-type classes. The base `.slide` is the only place positioning context is set; per-type styling stays inside it. Strip any `position` declaration from `.s-<role>` rules and re-render. | `css-gotchas.md` #27 added. |
| 29 | 0. Extraction gap / sizing | Build assumed default 10x7.5" slide dimensions (`cy=6858000` EMU) when the source was 16:9 at 10x5.625" (`cy=5143500` EMU). Every Y position extracted from PPTX was off by roughly 33%. | Phase 0 must read `<p:sldSz>` from `ppt/presentation.xml` FIRST and cache `(sldW_emu, sldH_emu)` before any EMU-to-pixel conversion runs. The cached pair is the divisor for every position/size in the build. | New script `scripts/parse_slide_size.py`; SKILL.md Phase 0 updated with the sldSz read step. |
| 30 | 5. Fidelity drift (root cause: extraction strategy) | Spent 8 rounds approximating icons, backgrounds, dividers, semicircle logos from PDF rasters when a `.pptx` of the same deck existed in the user's workspace folder. PPTX gives exact source PNGs, exact `<a:gradFill>` color stops, exact EMU positions, and exact `<a:custGeom>` shapes. | Phase 0 first checks for a sibling `.pptx` (matching filename in the upload directory, OR matching filename in the user's workspace folder). If present, PPTX extraction is the PRIMARY source. PDF extraction is the fallback when PPTX isn't available. | New script `scripts/extract_pptx_assets.py`; SKILL.md Phase 0 amended with the PPTX-first rule. |
| 31 | 5. Fidelity drift | Source slides 4/5 use `<a:custGeom>` half-dome shapes (213x137 EMU, cx:cy ratio 1.55:1) as logo holders that straddle a wave divider, only the top hemisphere is visible above the divider. Initial build treated them as full circles (border-radius: 50%), which sat ON the wave rather than straddling it. | Phase 1 classifier inspects every `<a:custGeom>` shape's cx:cy ratio. Near 2:1, semicircle. Near 1.55:1, half-dome. Build with `border-radius: <half-cx>px <half-cx>px 0 0` plus `border-bottom: none` so the flat side aligns to the divider's top edge. | `spine-tables.md` sales-deck "Logo divider straddle" pattern added; `css-gotchas.md` #28 added. |
| 32 | 5. Fidelity drift (gradient direction) | Source `<a:lin ang="18900044">` encodes 315deg in PPT compass convention (clockwise from north, 60000ths of a degree). CSS `linear-gradient(<angle>, ...)` uses a different convention. First CSS conversion used the raw 315deg and produced a gradient that flowed the opposite direction across the slide. | Helper `ppt_angle_to_css(emu_angle)` returns `(css_deg, color_order_hint)` so the build script either rotates by the converted degree or reverses the stop order. PPT 315deg, CSS 45deg same-order, or 225deg with reversed stops. Both give the same visual; pick whichever reads cleaner in the CSS. | `palette-typography-detection.md` "Gradient Extraction" section added with the angle conversion table and recipe. |
| 33 | 5. Fidelity drift / image processing | User-supplied `arjun.png` was already pre-cut (RGBA, transparent corners, alpha=0 at edges) but the subject itself was semi-transparent (alpha roughly 197 across the face/body, roughly 0 at the soft fade band). Color-distance bg-removal pass treated the soft-fade band as "background-like" and erased it, producing a hard-edged headshot floating on the navy panel, worse than before. | Detect existing alpha range FIRST before any color-based removal. If the input is RGBA AND alpha min < 255 AND alpha max < 255, the file is pre-cut, do NOT run color-distance removal. Instead, boost any pixel with alpha > threshold (30) to alpha=255 while leaving the soft-fade band intact. | `image-sourcing.md` "Alpha Detection" section added; new script `scripts/boost_alpha.py`. |
| 34 | 5. Fidelity drift (typography) | Cover headline "Founder-Services" in Cormorant Garamond display weight at 124px: the U+002D hyphen rendered near the baseline. The compound word read as "Founder Services" with a low-floating dash, not the intended editorial em-rule treatment. CSS `vertical-align` shifts were inconsistent across browsers. | Replace U+002D in display-sized compound words with a custom dash span (`<span class="cb-dash"></span>`) styled as a small currentColor rectangle with `vertical-align: 0.22em`. Font-independent, pixel-perfect, consistent across browsers. | `cover-asset-extraction.md` "Display Compound Words" section added. |
| 35 | 5. Fidelity drift (background composition) | Source uses photographic backgrounds (night sky, mountains, milky way) overlaid with a navy color gradient via PowerPoint's `background-blend-mode: multiply` semantics, the photo's texture and stars/peaks read through the tint. CSS used a flat `linear-gradient(...)` only and lost the texture entirely. User feedback: "color gradient and color itself overall is different, feels flat." | Phase 1 classifies each slide background as `photo-tint` (photo + colored gradient overlay) vs `flat-gradient` (pure CSS gradient). For `photo-tint` slides, extract the source photo + the gradFill stops, and render as `background-image: linear-gradient(<stops>), url(<photo>); background-blend-mode: multiply, normal;`. NEVER a flat gradient when source is photo-tinted. | `palette-typography-detection.md` "Background Composition" section added; SKILL.md Phase 3 rule added (photo-bg multiply recipe). |
| 36 | 5. Fidelity drift (vector vs raster dividers) | Source PPTX uses pre-rendered PNGs for the white curve divider on slides 6/8 (`image27.png`) and the thin wave divider on slides 4/5 (`image3.png`). CSS approximation with `border-radius` curves diverged in shape, the source's hand-tuned bezier wasn't reproducible with two corner radii. | When PPTX is available, extract the divider raster directly from `ppt/media/` and embed as `background-image`. CSS-curve approximation is the fallback when only the PDF is available. | `cover-asset-extraction.md` "Curve Divider Extraction" section added. |

### Net new reference files / sections
- `palette-typography-detection.md`, new sections: "Gradient Extraction", "Background Composition"
- `image-sourcing.md`, new section: "Alpha Detection"
- `cover-asset-extraction.md`, new sections: "Display Compound Words", "Curve Divider Extraction"
- `spine-tables.md`, sales-deck spine: "Logo divider straddle" pattern
- `css-gotchas.md`, #27 (slide-class `position: relative` override), #28 (custGeom half-dome shapes).

### Net new SKILL.md rules
- **Phase 0**: read `<p:sldSz>` from `ppt/presentation.xml` first and cache `(sldW_emu, sldH_emu)` before any EMU-to-pixel conversion.
- **Phase 0**: if a `.pptx` is uploaded alongside the `.pdf`, or exists in the user's workspace folder with a matching filename, prefer PPTX extraction as the PRIMARY source, PDF is the fallback.
- **Phase 1**: inspect `<a:custGeom>` shape cx:cy ratio. Near 2:1 = semicircle. Near 1.55:1 = half-dome. Map to `border-radius: <half-cx>px <half-cx>px 0 0` patterns.
- **Phase 1**: classify each slide background as `photo-tint` vs `flat-gradient`.
- **Phase 3 (new rule)**: photo-bg slides use `background-image: linear-gradient(...), url(photo); background-blend-mode: multiply, normal;`, never a flat CSS gradient when the source is photo-tinted.

### Net new scripts
- `scripts/extract_pptx_assets.py`, unzip pptx, enumerate `ppt/slides/*.xml` + rels, emit JSON with per-slide list of `(rId, image_path, position_px, size_px)` for pics AND `(color_stops, angle)` for each `<a:gradFill>`.
- `scripts/parse_slide_size.py`, parse `ppt/presentation.xml`, return `(sldW_emu, sldH_emu)`.
- `scripts/boost_alpha.py`, for RGBA images with alpha range < 255, boost any alpha > threshold to 255 while preserving the soft fade band.

---

### Run 7, AI-fintech pitch deck (PPTX-surfaced mid-run)

**Source**: 14-slide pitch deck for AI loan officer for banks/lenders. Manrope typography, dark-green (#006838) on light cream-green gradient backgrounds. Custom wordmark in navy with teal dot. Mid-run the user surfaced the `.pptx` for icon extraction.

### Failures caught + fixed

| # | Category | Issue | Fix | Checklist update |
|---|---|---|---|---|
| 37 | 5. Fidelity drift / asset extraction | Recreated 19 source icons as inline `<svg>` paths from rough source-PDF visual inspection. Result was generic Material-Design-shaped icons that read as a different brand register than the source's specific custom illustrations. User: "the icons 100% of them are very off." | When PPTX is available, icons live in `/ppt/media/imageN.svg` and `imageN.png`. Map slide, image via `/ppt/slides/_rels/slideN.xml.rels`. **Do not recreate icons in inline SVG when PPTX exists**, pull the source rasters/SVGs and embed as `<img>` tags. | `extraction-pipeline.md` "PPTX icon extraction" section; SKILL.md Phase 3 rule #14 (icon source-of-truth hierarchy). |
| 38 | 5. Fidelity drift (icon color) | PPTX icons used `fill="#ffffff"` (white-on-green) and `fill="#006838"` (green-on-light) for two distinct visual styles. Rendered with default settings, white-on-green icons appeared invisible (white on white). | Phase 1 classifies each icon's intended pairing: `icon-on-colored-square` (render white) vs `icon-on-light-bg` (render in primary). Before rendering: `sed -e 's/fill="#ffffff"/fill="<target>"/g' -e 's/fill="inherit"//g'`. ImageMagick can't render `fill="inherit"`, strip it. | `extraction-pipeline.md` "PPTX icon color normalization" section. |
| 39 | 0. Extraction (full-slide PNG as fallback) | Slide 11 had a complex relationship-diagram visual. HTML/SVG approximation drifted across three build rounds. PPTX `/ppt/media/` contained `image46.png`, a full-slide PNG render. | When PPTX includes a full-slide PNG render of a slide (look for >500KB PNGs in `ppt/media/`), use it as the visual for that slide. Crop title and bottom banner regions; HTML layers those for editability. Match the slide CSS background to the cropped image's edge colors. | `cover-asset-extraction.md` "Full-slide PNG fallback" section; SKILL.md Phase 3 rule #15. |
| 40 | 9. Shell divergence / state mutation | Injected a new key into existing SHOTS object via text-find + insert. Twice the injection broke the JSON because base64 strings contain edge cases. Result: all 60+ embedded images failed to load. | **Never inject into the existing SHOTS object via find-and-replace.** Rebuild SHOTS from scratch by collecting every asset path into a Python dict, base64-encoding, `json.dumps(separators=(",",":"))`, replacing the entire `const SHOTS = {...};` block. Use a stable downstream landmark (`document.querySelectorAll('[data-shot]')`) for end-of-line. **Validate by re-parsing the new SHOTS region after write.** | `css-gotchas.md` #29; SKILL.md Phase 3 self-lint adds "SHOTS object parses as valid JSON". |
| 41 | 5. Fidelity drift (logo backgrounds) | Two user-supplied logos had baked-in white backgrounds, appeared as white boxes interrupting the wall vs the slide gradient. | Run luminance-threshold alpha pass on **every** logo automatically. Recipe: `lum > 245, alpha=0`; soft falloff 230 to 245 (partial alpha for AA edges); auto-bbox crop. Catches near-white bgs the user wouldn't notice in isolation. | `image-sourcing.md` "Automatic logo alpha-cleanup" section; SKILL.md Phase 3 rule #16. |
| 42 | 4. Role misclassification (logo grouping) | Source slide 5 had stacked logos in two columns vertically. Build paired by horizontal adjacency (left-right reading order) instead of vertical stacking. | Identify pairing by vertical proximity, not horizontal adjacency. Phase 1 emits a `(x, y, w, h)` bounding box per logo; group by overlapping x-ranges to detect vertical stacks before HTML layout. | `extraction-pipeline.md` "Logo stack detection" section. |
| 43 | 6. Polish (banner text alignment) | `.banner-pill` defaulted to block-level with `padding: 14px 38px`. Text sat near top of the green-bordered box across multiple fonts because the default line-box flow didn't account for Manrope metrics. | Banner pills MUST use `display: inline-flex; align-items: center; justify-content: center; line-height: 1.1; min-height: 52px`. Block-level padding is not reliable for vertical centering across font families. | `css-gotchas.md` #30; SKILL.md Phase 3 rule #17. |
| 44 | 5. Fidelity drift (slide-image background seam) | Slide 11 used a baked PDF page render with near-white left edge transitioning to pale yellow-green right edge. Slide's underlying CSS was a stronger green gradient. Visible horizontal seam at image bottom. | When a slide uses a baked image + HTML layer, set THAT slide's CSS background to match the image's edge colors. Sample 5+ pixels from the bottom row via PIL; build `linear-gradient(90deg, <left>, <middle>, <right>)` from sampled values. | `palette-typography-detection.md` "Embedded-image background matching" section. |
| 45 | 6. Polish (badge restraint) | Slide 3 demo badge was bright orange `#FF6B1F`, 16px, 2deg tilt, animated translate, animated chevron, read as off-brand and overly attention-grabbing. User: "feels too much; not on brand." | Interactive-demo badges use brand colors: white bg, primary border, primary text, subtle 1.6s pulse on a single dot (not whole element). Restraint over loudness. Sizing: 11.5px font, 7px 14px padding, 20px border-radius. | `interactivity-upgrades.md` "Interactive-demo badge" section. |
| 46 | 5. Fidelity drift (background gradient) | Initial slide background was a guessed `linear-gradient(135deg, #EEF6EA 0%, #FFFBF5 55%, #F2F7E8 100%)`, visually flatter than source. User: "background gradient in all slides almost isn't coming through." | Sample 5+ corner/edge pixels from `pages/page-1.png` via PIL. Build the angle from dominant tone direction; build stops from sampled values. Actual source: `linear-gradient(118deg, #D7ECE0 0%, #E9F4DC 30%, #FBFFE8 65%, #F2FAD9 100%)`. | `palette-typography-detection.md` "Background gradient sampling" section; SKILL.md Phase 3 rule #18. |
| 47 | 6. Polish (headline placement) | Per-slide `.slide-title` overrides accumulated inconsistencies, mixed `margin-top` (0/6/10px), mixed text-align values, mixed max-widths. Titles drifted Y position across slides. | Lock base `.slide-title { margin: 0 auto; text-align: center; min-height: 64px; max-width: 1280px; font-size: 54px }` ONCE. Per-slide overrides change ONLY font-size for outliers. Convert source left-aligned titles to centered for deck-wide consistency. | `css-gotchas.md` #31; SKILL.md Phase 3 rule #19. |
| 48 | 5. Self-lint cap (file size) | SKILL.md self-lint cap previously said `60 to 220 KB`. Realistic full-fidelity conversion with all real logos + photos + icons + chart + embedded page render lands at 1.5 to 2.5 MB. Cap creates pressure to downscale. | Update cap to `60 KB to 2.5 MB`. Full-asset conversions land at 1.5 to 2.5 MB and that's normal. Release message notes final size without apology. | SKILL.md Phase 3 self-lint updated; Phase 5 Release template includes "File size: X.X MB". |

### Net new reference sections
- `extraction-pipeline.md`, "PPTX icon extraction", "PPTX icon color normalization", "Logo stack detection"
- `cover-asset-extraction.md`, "Full-slide PNG fallback"
- `image-sourcing.md`, "Automatic logo alpha-cleanup"
- `palette-typography-detection.md`, "Embedded-image background matching", "Background gradient sampling"
- `interactivity-upgrades.md`, "Interactive-demo badge"
- `css-gotchas.md`, #29 (JSON injection into SHOTS), #30 (banner-pill centering), #31 (headline placement consistency)

### Net new SKILL.md rules
- Phase 1, icon-pairing classification (icon-on-colored-square vs icon-on-light-bg) when PPTX present; logo stack detection by overlapping x-ranges.
- Phase 2, confirmation block now opens with a hard "PPTX available?" row, not an opportunistic Phase 0 check.
- Phase 3, rules 14 (icon source-of-truth hierarchy), 15 (full-slide PNG fallback), 16 (automatic logo alpha-cleanup), 17 (banner pill vertical centering), 18 (background gradient sampling), 19 (headline placement consistency).
- Phase 3 self-lint, file-size cap raised to 60 KB to 2.5 MB; new "SHOTS object parses as valid JSON" check.
- Phase 5 Release, summary line includes "File size: X.X MB (N embedded assets)".

---

### Run 8, 16-slide pitch deck, Mode A default revealed

**Source**: 16-slide pitch deck, ConstructionTech vertical, no PPTX available, no PPTX requested at Phase 0.

**Iterations**: 3.
- v1: Mode B reconstruction (default at the time). 10 distinct defects on Phase 4 review.
- v2: Mode B with fixes (asset re-extraction, blur scrims, layout repositioning, source-text restoration). Remaining drift on colors / logo placement / palette register.
- v3: Switched to Mode A (page-image) after user pointed at prior imports as canonical reference. Pixel-faithful in one shot.

**Root cause**: Skill defaulted to Mode B reconstruction. Should have defaulted to Mode A page-image. Prior outputs in user workspace were canonical reference but not surfaced.

**Categories triggered**:
- 16 (Wrong build mode chosen): central failure. v1 + v2 = 2 wasted iterations.
- 17 (Prior-output style not matched): contributed to category 16, if Step 0d had run, Mode A would have been pre-selected.
- 18 (Source-text ghosting in reconstruction mode): v1 cover, problem, integration, thank-you all ghosted.
- 19 (Off-by-one source page reference): v1 market_photo cropped from page 10 instead of page 11.
- 6 (Fidelity drift): general bucket for v1's palette + content-rewriting drift.

**Fixes landed in skill**:
- SKILL.md: added "Two build modes" section at top; Mode A is the explicit default. Phase 2 confirmation block now has a mandatory `Build mode` row. Phase 3 split into Mode A and Mode B implementations. Phase 4 review bar calibrated per mode (Mode A: Layout only).
- Phase 0 Step 0d (prior-output scan) added, surfaces existing `*-Imported.html` files in workspace.
- New reference `page-image-mode.md` documents Mode A shell, SHOTS dict schema, eyebrow injection, JPEG knobs (q70/w1400 for 16-slide).
- `confirmation-block-template.md` updated with `{{pptx_status_line}}`, `{{build_mode_line}}`, `{{prior_imports_line}}` placeholders.
- `css-gotchas.md` #32 (source-text ghosting), #33 (off-by-one page refs), #34 (SHOTS string-key consistency), #35 (Playwright install path), #36 (text-marker color mis-sampling).
- `review-adaptations.md` mode-aware section (Mode A skips 2 of 3 reviewers).

---

## Categories rollup

Categories 1 to 5 usually trace back to scripts in `scripts/` (classifier, palette, extractor), improve the script and re-run. Categories 6 to 8, 10, 12 usually trace to instructions in SKILL.md, `review-adaptations.md`, the handoff skill, or pattern references, adjust the prose. Category 9 traces to the Phase 3 rule #0 contract and the deck-builder `shell-pattern.md`. Categories 11, 13, 14 trace to Phase 1/2 protocol, surface upfront, don't quietly proceed. Category 15 traces to brief discipline, lock tokens at confirmation, don't iterate them. Categories 16 to 19 are Mode A / Mode B selection failures, surface the build mode choice explicitly in Phase 2 and scan for prior outputs.
