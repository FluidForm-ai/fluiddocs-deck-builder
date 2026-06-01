# Rendering Checks, Layout Reviewer Spec

**Owner**: Layout Reviewer (Phase 3).
**Categories owned**: center-overflow / height-budget bugs, shell logo rendering, scroll/overflow bugs, viewport-fit failures, the structural layout problems that ship visibly broken.

This is the checklist that catches the bugs that actually ship. Every deck the user has flagged had at least one of these issues. Run this audit before handing off.

Every check has a diagnostic pattern (how to grep for the bug) and a fix recipe. Framed as a Phase 3 reviewer: fail if any check fires. Fixes live in Phase 2; the Layout Reviewer in Phase 3 only verifies they were done.

---

## 1. The center-overflow bug (causes logo overlap on most slides)

**Symptom**: Eyebrow or h2 text bleeds under the brand-mark top-left. Content appears cut off at the top. Scroll reveals content exists, but initial view is broken.

**Root cause**: `.slide` or a content slide selector has `justify-content: center` + content height > viewport height. Flexbox centers overflow symmetrically.

**Grep for it**:
```
grep -n "justify-content: center" <deck>.html
```

Every match on a `.s-XXX { ... }` rule that is NOT `.s-cover` is a bug.

**Fix**: Replace with `justify-content: flex-start` or remove the property entirely (let it inherit from `.slide` default of `flex-start`).

**Why this keeps happening**: copy-paste from other slide rules. Prevent it by setting `flex-start` on `.slide` itself (the shell-pattern.md default).

---

## 2. Logo glyph verification

**Symptom**: The "brand letter" (U for Uber, S for Stripe, etc.) renders as a wrong-shape mark, a bracket, a chunk, or a pinwheel.

**Root cause**: Hand-crafted SVG path approximating the letter is wrong. E.g., `M14 23h34v3.2H18.4v14.4H48v3.2H14V23z` traces a bracket, not a U.

**The right approach**:
- Prefer inlining the actual brand logo SVG (from their press kit) for the wordmark.
- For the small brand-mark (top-left on each slide), if the company doesn't have a simple "monogram" SVG, use `<text>` with the brand display font instead of a fake path:

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="12" fill="#000"/>
  <text x="32" y="34" text-anchor="middle" dominant-baseline="central"
        font-family="Inter, sans-serif" font-size="42" font-weight="900"
        letter-spacing="-2" fill="#fff">U</text>
</svg>
```

**Verify before shipping**: imagine the glyph in the positioned viewBox. Letters with enclosed space (B, D, O, P, Q, R) cannot be done with a single path + fills unless you know SVG fill-rules. When in doubt, use `<text>`.

---

## 3. Team grid count mismatch

**Symptom**: Last row has 1 or 2 cards floating in a 3-col grid, leaving awkward empty cells.

**Root cause**: `grid-template-columns: repeat(3, 1fr)` with 4, 5, or 7 team members.

**Recipes by count**:
- **3 founders**: `repeat(3, 1fr)`, perfect
- **4 founders**: `repeat(2, 1fr)` 2x2, or `repeat(4, 1fr)` single row if cards fit
- **5 total (3 founders + 2 key hires)**: 3-col for founders, then separate `.team-key-hires` block underneath with a 1:1:1 grid (label card + 2 hire cards), OR 2 hire cards in `repeat(2, 1fr)` under the founders
- **6 founders + hires**: `repeat(3, 1fr)` 2 rows
- **7+**: split into "Core team" (3) + "Extended team" (pills or smaller cards below)

**Default pattern**: founders get full-size cards in primary grid; post-founder hires get smaller cards in a labeled sub-section.

---

## 4. Concentric ring text overlap (Market slide)

**Symptom**: TAM, SAM, SOM numbers appear stacked on top of each other in the center of the rings. Only the innermost is readable.

**Root cause**: All three `.ring` elements use `justify-content: center`, placing their text in the geometric center. Since the rings are concentric, those centers coincide.

**Fix**: Place each label in its visible crescent, not its geometric center.

```css
.ring.tam {  /* outermost, text in TOP crescent */
  inset: 0;
  justify-content: flex-start; padding-top: 5%;
}
.ring.sam {  /* middle, text in MIDDLE-TOP crescent */
  inset: 20%;
  justify-content: flex-start; padding-top: 10%;
}
.ring.som {  /* innermost, centered is fine */
  inset: 42%;
  justify-content: center;
}
```

Alternatively: drop concentric rings entirely and use a bar-chart or Sankey-style market sizing for brands where that feels more native (Stripe, Databricks).

---

## 5. Aspect-ratio overflow (visual blocks, phone mockups, charts)

**Symptom**: A product mockup or visual block runs off the top and bottom of the slide.

**Root cause**: Element has `aspect-ratio: 9/19` (phone), `aspect-ratio: 4/5` (card), or similar tall ratio without a pixel `max-height` cap. On the fixed 810px canvas, the ratio forces the block taller than the content area (~596px after padding).

**Fix**: Always cap visual blocks with a pixel `max-height` (not `vh`, canvas is fixed) and let the element scale:

```css
.sol-visual {
  max-height: 520px;       /* fits inside 810, 104, 96 = 610px content area */
  aspect-ratio: 4/5;
  width: 100%;
  margin: 0 auto;
}
.sol-phone {
  height: 88%;             /* scale inside the capped container */
  aspect-ratio: 9/19;
}
```

**Why pixels, not `vh`**: the canvas is fixed at 810px and scaled as a whole via CSS transform. Viewport units inside the canvas would compute against the outer viewport, not the canvas, so `64vh` on a 400px-tall phone would produce a 256px block even though the deck itself is scaled. Always reason in canvas pixels.

---

## 6. Rigid Airbnb-pattern leakage

**Symptom**: The Uber deck's Competition slide is a soft 2x2 positioning matrix. The Stripe deck's Moat slide has Airbnb's flywheel. Every deck ends up feeling like "Airbnb with different colors."

**Root cause**: Airbnb-Deck.html was used as the visual reference instead of the structural reference. Every component got copied verbatim.

**Fix**: For each brand, pick visual components from `visual-components.md` that match the brand's actual design voice. The structural spine stays (14 slides, eyebrow + h2 + visual), the visuals change.

Grep for Airbnb-isms that leaked in:
```
grep -nE "(comp-matrix|comp-axis|listing-grid|rausch)" <deck>.html
```

Any match in a non-Airbnb deck is a bug.

---

## 7. Brand-mark / slide-meta overlap zones

**Symptom**: Top-right slide-meta text ("07 / 14 · Market") ends up under a chart, or top-left brand-mark sits under an eyebrow.

**Root cause**: Content top-offset < 104px OR content's internal elements overflow their container and push into the header zone.

**The reserved zones** (never put content here):
- Top-left: `0, 0` to `240px, 72px` (brand-mark zone)
- Top-right: last `300px, 72px` of the slide width (slide-meta zone)
- Bottom-left: `0, 100%-72px` to `180px, 100%` (nav-counter zone)
- Bottom-right: last `140px, 72px` (arrow buttons zone)

**Fix**: Keep `.slide { padding: 104px 96px 96px }` sacred. If a specific slide (like Demo) uses reduced padding, remove the brand-mark and slide-meta on that slide.

---

## 8. Cover slide wordmark rendering

**Symptom**: The large cover logo is stretched, squished, or tiny.

**Root cause**: SVG with no `width`/`height` attributes and no CSS sizing, or the viewBox doesn't match the glyph bounds.

**Fix**: Always set an explicit CSS size for the cover wordmark:

```css
.s-cover .brand-logo-lg { width: 72px; height: 72px; }
```

And verify the viewBox and the content fit. For `<text>`-based logos, use `dominant-baseline="central"` for reliable vertical centering across browsers.

---

## 9. The pre-delivery audit (run in order)

Before handing off, run this five-minute audit. Skipping this is how the Uber deck shipped with 6 layout bugs.

```
1. Open the deck in a browser at 1440x900 (or larger).
2. Click through all 14 slides. For each, check:
   - Does the eyebrow / h2 overlap the top-left brand-mark? (center-overflow bug)
   - Does any text overlap the top-right slide-meta? (header zone bug)
   - Are there visible text overlaps? (z-index / positioning bugs)
   - Does the brand-mark glyph render as the intended letter? (logo verification)
   - Is anything cut off at the top or bottom? (over the 810px canvas budget)
   - Does the layout feel like this specific brand, or like Airbnb with different colors? (rigidity bug)
3. Resize the browser window to a narrow width (~420px) and verify:
   - The deck scales down proportionally, letterboxed top/bottom.
   - Layout is IDENTICAL to the desktop layout, just smaller. Nothing reflows or collapses.
   - Nav arrows are still pressable (will be tiny, that's expected; pinch-zoom works).
4. Resize to ultrawide (~2400px) and verify:
   - Deck scales up to fit height, letterboxed left/right.
   - Aspect ratio preserved.
5. Grep: `grep -nE "(justify-content: center|comp-matrix|comp-axis|@media)" <deck>.html`
   - `justify-content: center` on non-cover slides = bug.
   - Airbnb-ism classes in non-Airbnb decks = bug.
   - `@media` that reflows layout = bug (fixed canvas should not reflow).
6. Check the deck contains a `.deck-outer` wrapper and `.deck` has fixed pixel dimensions (width: 1440px, height: 810px).
7. Check `setScale()` function exists in the JS and is wired to `resize` + `orientationchange`.
```

**Do not ship until all 14 slides pass.**

---

## 10. Common grep patterns for bugs

```bash
# Center-overflow bug (any match on .s-XXX other than s-cover is a bug)
grep -nE "\.s-[a-z]+\s*\{[^}]*justify-content: center" <deck>.html

# Airbnb-isms that leaked into a non-Airbnb deck
grep -nE "(comp-matrix|listing-grid|rausch|bélo)" <deck>.html

# Missing brand-mark on content slides (count should equal slide count, 1 for cover)
grep -c "class=\"brand-mark\"" <deck>.html

# Tall aspect ratios without a pixel max-height
grep -nE "aspect-ratio:\s*[0-9]+/[12][0-9]" <deck>.html
# (then check each match has a max-height: Xpx cap nearby, not vh)

# Verify section count = 14 (or your target)
grep -c "<section class=\"slide" <deck>.html

# ---- Fixed-canvas integrity checks ----

# Confirm the .deck-outer wrapper exists
grep -c 'class="deck-outer"' <deck>.html
# Expected: 1

# Confirm .deck uses FIXED pixel dimensions (not 100vw/100vh)
grep -nE "\.deck\s*\{" <deck>.html
# Then manually verify the next few lines contain width: 1440px and height: 810px.
# If you see width: 100vw or height: 100vh inside .deck {}, the deck is still responsive, fix.

# Viewport units leaking inside slides (fixed canvas should use px)
grep -nE "(max-height|min-height|height):\s*[0-9]+vh" <deck>.html
# Matches inside slide content = bug. Only acceptable location is .deck-outer / html / body.

# @media queries that reflow layout (fixed canvas = no reflow)
grep -nE "@media\s*\(" <deck>.html
# Expected: 0 matches. Any @media that changes grid-template-columns, font-size, or display
# is a fixed-canvas integrity violation.

# setScale() wired to resize
grep -c "setScale" <deck>.html
# Expected: >=3 (function def + initial call + resize listener). Missing = no scale-to-fit.
```

---

## 11. Fixed-canvas integrity checklist

The fixed 1440x810 canvas introduces a class of checks. Run all of these after migrating an older deck or building a new one:

1. `<div class="deck-outer">` wraps everything.
2. `.deck` has `width: 1440px; height: 810px;` (not `100vw` / `100vh`).
3. `.deck` has `transform-origin: center center;` and `overflow: hidden;`.
4. `.slide` has `overflow: hidden;` (not `overflow: auto;`, there is no scroll in fixed canvas).
5. `.slide` uses absolute pixel padding (e.g. `104px 96px 96px`), never `vh` / `vw`.
6. All `.progress-line`, `.nav-counter`, `.nav-arrows` use `position: absolute` (not `fixed`) and live INSIDE `.deck`.
7. The `setScale()` function exists and is attached to both `resize` and `orientationchange`.
8. No `@media` queries in the stylesheet (or at most one `@media print` if needed, nothing that reflows).
9. No `vh`/`vw` inside any slide-level CSS. Use pixels.
10. `.deck-outer` has `overflow: hidden` so the scaled deck never bleeds out.

If any fails, the deck is not a true fixed-canvas deck. Bounce back to Build.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
