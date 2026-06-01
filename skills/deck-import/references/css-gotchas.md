# CSS Gotchas, Conversion-Mode Traps

Specific, repeatable bugs that cost iteration time on real conversion runs. Each entry: the bug, the root cause, the fix, and the detection signal. Grow this file with each conversion; high-yield reading before Phase 3.

---

## 1. Scale-to-fit double-centering

**Bug**: The entire deck renders offset up-and-left or down-and-right in the viewport.

**Cause**: CSS applies `translate(-50%, -50%) scale(s)` to `.deck` while the parent `.deck-outer` is a flex container that already centers children. The flex center + the translate stack, and the canvas drifts.

**Fix**: `transform: scale(s)` only. The flex parent handles centering; transform only scales.

```js
function setScale(){
  var s = Math.min(window.innerWidth / 1440, window.innerHeight / 810);
  deck.style.transform = 'scale(' + s + ')';  // NOT translate(-50%,-50%) scale(s)
}
```

**Detection**: open the HTML full-screen, resize the window. If the deck drifts toward a corner as the window shrinks, it's this bug.

---

## 2. CSS escape-sequence doubling

**Bug**: A character that should render as a right arrow shows up as literal `\2192` on the slide.

**Cause**: Building CSS strings with Python f-strings or concatenation, where `\2192` gets escaped to `\\2192`, which CSS then renders as the literal characters `\2192`.

**Fix**: In the final CSS output, arrow/check/misc Unicode in `content:` rules must be a single backslash: `content: '\2192';`. If you build CSS through Python, write it in a raw triple-quoted string, not an f-string; or apply a `sed` fixup pass to the final file.

**Detection**: visually scan for any `\NNNN` sequence on a slide. Also grep the final CSS: four backslashes (in a grep pattern, two literal backslashes) should return zero matches in the shipped file.

---

## 3. Aggressive warm gradient drowns the slide

**Bug**: Source is a near-white page with a subtle corner accent; HTML is a full warm-orange wash.

**Cause**: Misreading the source palette at 1:1 without sampling pixel values. The eye exaggerates corner accents into overall tint when briefing from memory.

**Fix**: Sample the source corners (see `visual-comparison-loop.md` §Palette sampling). Base background should be near-white (#F9F9F9, #FAFAFA, or similar). Accent only via a radial gradient anchored to one corner:

```css
.slide {
  background:
    radial-gradient(700px 500px at 100% 100%, rgba(251,146,60,0.32), transparent 70%),
    #F9F9F9;
}
```

**Detection**: side-by-side grid (see `visual-comparison-loop.md`). Color cast is the #1 thing your eyes catch.

---

## 4. Absolute-positioned eyebrow overlaps page header

**Bug**: The "Features" pill and the wordmark stack on top of each other in the top-left.

**Cause**: `.wm-stack` class applies `position: absolute` to position the wordmark on the cover slide. On feature slides, the same class is nested inside `.s-feat-head` which is already absolutely positioned, double-absolute collapses them.

**Fix**: Contextual position reset.

```css
.s-feat-head .wordmark-img {
  position: static;  /* override absolute when inside feat-head */
}
```

**Detection**: component overlap on feature slides.

---

## 5. Grid with implicit rows overflows vertically

**Bug**: A 3-column grid renders correctly but rows keep expanding, pushing content off-canvas.

**Cause**: `grid-template-columns: repeat(3, 1fr)` without declaring `grid-template-rows` lets rows size to content. On a density-heavy conversion slide, content overflows the 810px canvas.

**Fix**: Declare explicit row bounds.

```css
.s02-grid {
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  max-height: 480px;
  overflow: hidden;
}
```

**Detection**: Layout Reviewer flags overflow. Playwright renders at 1440x810 but your visible content runs past 810, you'll see a cut-off in the screenshot.

---

## 6. Flex `shrink` clips cover wordmark

**Bug**: Source cover reads `FLUID | form`; HTML cover reads `F L U I D | f o r` (last letters clipped).

**Cause**: Cover uses `display: flex` and the wordmark wrapper doesn't declare `flex-shrink: 0`, so when the parent runs out of space the wordmark shrinks letter-by-letter. Non-standard glyph behavior under shrink compresses letter-spacing.

**Fix**:

```css
.s-cover .cover-left,
.s-cover .cover-left .wordmark-img {
  flex-shrink: 0;
  white-space: nowrap;
}
```

**Detection**: open the cover in the render PNG. If any letter is visibly compressed or clipped compared to the source, it's this.

---

## 7. Tick marks as horizontal bars

**Bug**: Checkmark or plus icons look like short hyphens instead of crosses.

**Cause**: A `.tick` class builds the cross using a single `::before` pseudo with `height: 2px`, which gives you a horizontal bar, not a plus.

**Fix**: Use `::before` + `::after`, one horizontal one vertical:

```css
.s04-tick {
  width: 26px; height: 26px; position: relative;
}
.s04-tick::before, .s04-tick::after {
  content: ''; position: absolute;
  background: var(--primary);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
.s04-tick::before { width: 100%; height: 3px; }
.s04-tick::after { width: 3px; height: 100%; }
```

**Detection**: zoom into the tick elements in the render. If they're visibly a line not a cross, it's this.

---

## 8. Image `src` with sandbox path the browser can't resolve

**Bug**: Base64 embed works, but swapping to an `assets/` relative path breaks the image (broken-icon).

**Cause**: The conversion HTML ships as a single file. Any `src="assets/foo.png"` assumes the `assets/` folder is alongside the HTML, which it won't be after Release. Keep everything base64.

**Fix**: Base64-embed every raster. Logo, founder photos, anything. A 220KB file with all images inline is fine; a 40KB file with broken image links is not.

**Detection**: open the HTML by double-click from Finder (not via `file://`). If an image is missing, it's a path-resolution issue.

---

## 9. `position: absolute` without a `position: relative` parent

**Bug**: A slide's absolutely-positioned label jumps to the top of the deck, not the slide.

**Cause**: The slide itself needs `position: relative` for absolute children to anchor correctly. If the `.slide` class lacks it, absolute children escape up the DOM until they find an anchor, often the `html` element.

**Fix**: always include `position: relative` on `.slide`.

```css
.slide {
  position: relative;  /* mandatory for absolute children */
  width: 1440px;
  height: 810px;
  ...
}
```

**Detection**: absolutely-positioned elements appearing in wrong slides or at viewport edges.

---

## 10. Interactivity handler attached before DOM is ready

**Bug**: Mode toggle buttons on slide 8 don't respond to clicks.

**Cause**: The JS event listener runs inside the IIFE at script-parse time, but the `<script>` tag is inside the deck container which may not have streamed in fully yet on some browsers, or, more often, the listener query selector runs but no elements match because you've typo'd the class.

**Fix**: Wrap in a DOMContentLoaded check OR put the `<script>` at the very end of `<body>` after `.deck-outer` closes (which is what `assemble.py` does). Also, log the query-selector length once during dev:

```js
var cards = document.querySelectorAll('[data-s08] [data-s08-card]');
if (!cards.length) console.warn('s08 cards missing, check selector');
cards.forEach(...);
```

**Detection**: click a toggle, watch for state change. If nothing happens, open DevTools console and run the selector manually.

---

## 11. `<meta viewport content="width=1440">` breaks mobile

**Bug**: On desktop the deck looks fine. On an iPhone it renders as a tiny cropped fragment, only part of one slide visible, landscape content squeezed into a rectangle in the middle of the screen.

**Cause**: `width=1440` in the viewport meta tells the mobile browser "render this page as if the device screen is 1440px wide." The browser then zooms the entire viewport to fit the 1440 page into, say, a 390px device. On top of that, your own `transform: scale(min(vw/1440, vh/810))` runs against that fake 1440 viewport, not the real 390. The two scalings compose incorrectly, producing a cropped mid-screen render.

**Fix**: Always use `<meta name="viewport" content="width=device-width, initial-scale=1">`. The browser reports real device pixels; the JS scale transform then does all the resize work. This is the deck-builder canonical pattern, never deviate.

**Detection**: open the HTML on a real phone or in Playwright with `is_mobile: true` on a 390x844 viewport. If the slide is cropped or centered in a small rectangle rather than filling the device width, it's this bug.

---

## 12. Nav chrome outside the scaled stage

**Bug**: On mobile, the nav pill at the bottom is huge (desktop-sized) while the slide above it is tiny. Progress bar at the top is the same, full-width even though the slide is scaled to 27%.

**Cause**: Progress bar and nav were declared `position: fixed` as siblings of `.deck-outer` on `body`. They never scale with the transform, they stay anchored to the viewport. On desktop the size mismatch isn't noticeable; on mobile it becomes grotesque.

**Fix**: Put all chrome elements INSIDE the scaled canvas:

```html
<div class="deck-outer">
  <div class="deck">  <!-- this gets transform: scale(s) -->
    <div class="prog-bar"></div>
    <section class="slide active">...</section>
    <section class="slide">...</section>
    <div class="nav"><!-- arrows, counter, dots --></div>
  </div>
</div>
```

All chrome uses `position: absolute` in the 1440x810 coordinate system. They scale with the canvas and stay proportional at every screen size.

**Detection**: render in Playwright at `viewport: 390x844, is_mobile: true`. If nav buttons are larger than your finger relative to the slide, nav is outside the scale.

---

## 13. Stage squeezed by flexbox on narrow mobile

**Bug**: On a 390px-wide iPhone, the 1440x810 canvas visually becomes 390xsomething-weird. Text on slide 1 wraps differently than on desktop, which is supposed to be impossible.

**Cause**: `.deck-outer` is a flex container. Its child `.deck` (the 1440x810 canvas) doesn't declare `flex-shrink: 0`, so flexbox squeezes it to fit the narrow viewport. The `transform: scale()` doesn't help because the canvas dimensions themselves have been compressed below 1440px, and text now wraps at the compressed width.

**Fix**: Lock the canvas dimensions so flexbox cannot squeeze them:

```css
.deck {
  width: 1440px; height: 810px;
  min-width: 1440px; min-height: 810px;
  flex-shrink: 0;
  transform-origin: center center;
  /* transform: scale(s) set by JS */
}
```

**Detection**: on mobile, measure an element that should be 1440px, if it's returning 390 or some other narrow value, flex is squeezing the canvas.

---

## 14. Letterbox color that reads as a visible frame

**Bug**: User feedback: "the white space on all sides doesn't make sense" or "it feels like a screenshotted HTML", the deck has a visible rectangle edge around the slide instead of feeling edge-to-edge native.

**Cause**: Body/letterbox background is a different color from the slide paper (e.g., body `#E9ECEE` + slide `#FFFFFF`), OR the `.deck` canvas has a `box-shadow` / `border-radius` / `background: linear-gradient(...)` applied for "depth," which creates a visible seam between the canvas and the viewport.

**Fix**: Set `html`, `body`, `.deck-outer`, and `.deck` all to the same letterbox color, which should equal the slide paper color for most conversions. No shadow, no border-radius, no body gradient. The slide must appear to be a seamless continuation of the viewport.

```css
:root { --paper: #FFFFFF; --letterbox: var(--paper); }
html, body { background: var(--letterbox); }
.deck-outer { background: var(--letterbox); }
.deck { background: var(--paper); /* no box-shadow, no border-radius */ }
```

For dark-native brands, `--letterbox` and `--paper` both become the brand's dark surface. The principle is still "letterbox = page" so there's no visible frame.

**Detection**: resize the window past the slide's aspect ratio. If you can see a rectangular boundary between slide and background, the letterbox is wrong. The slide edge should be invisible.

---

## 15. Fonts arriving after first paint reflow the layout

**Bug**: The first render shows the slide with slightly different text wrap than the final steady state. Sometimes a line that should fit on one line wraps to two for roughly 300ms, then snaps back.

**Cause**: Google Fonts with `font-display: swap` (the default) renders text in a system fallback while the real font loads, then swaps. The fallback has different glyph widths, which changes line-wrap. For the brief window before the real font arrives, the layout is not source-identical.

**Fix**: Two-part gate.

1. Load fonts with `display=block`:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=block" rel="stylesheet">
```

2. Hide the stage until fonts resolve:
```html
<html class="fonts-loading">
<style>
  html.fonts-loading .deck { visibility: hidden; }
</style>
<script>
  var root = document.documentElement;
  var timeout = setTimeout(function(){ root.classList.remove('fonts-loading'); }, 3000);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function(){
      clearTimeout(timeout);
      root.classList.remove('fonts-loading');
    });
  } else {
    clearTimeout(timeout);
    root.classList.remove('fonts-loading');
  }
</script>
```

3s cap ensures the deck eventually shows even if a font never arrives (e.g., offline).

**Detection**: open the deck with cold cache (incognito). Watch for any flash where text wraps differently, then snaps back. If you see a reflow, the gate isn't working.

---

## #16, 4:3 decks leave bottom whitespace unless body is `flex: 1`

**Symptom**: content slides (team grid, swim lanes, demo mockups) render top-heavy with 200 to 300px of blank canvas below the last row, even though the source fills the full page.

**Root cause**: spine templates default to a 16:9 canvas (1440x810). Components are implicitly sized to consume roughly 700px of vertical after the header bar. When the source is 4:3 (1440x1080, typical PowerPoint default), the same components consume the same 700px and leave the extra 270px as dead space below. Flex-column bodies don't stretch unless explicitly told to.

**Fix**:
```css
.s-body           { display: flex; flex-direction: column; flex: 1; }
.s06-body,
.s11-body,
.s-shot-body     { flex: 1; justify-content: space-between; }
.s06-lanes       { flex: 1; }  /* let lanes fill remaining vertical */
.s06-lane        { min-height: 220px; display: flex; align-items: center; }
```

**When to apply**: whenever `metadata.detected_aspect_ratio` is 4:3 (or any non-16:9 ratio with more vertical space than the spine assumes). The Phase 3 build step should branch on aspect and inject the `flex: 1` stretch rules into content-slide bodies.

**Detection during visual comparison**: look for any slide where the bottom quarter of the HTML render is empty paper and the corresponding source page has content there. That's the tell.

---

## 17. Stat-card left column too narrow for display-font values

**Symptom**: on a stat card with `grid-template-columns: <Npx> 1fr`, the big-number value visually collides with the right-hand label. In extreme cases the value literally overflows into the label column.

**Example (before)**:
```css
.stat-card { display: grid; grid-template-columns: 90px 1fr; gap: 14px; }
.stat-card .big { font: 700 38px/1 Nunito, sans-serif; }
```
For a value like `"3.5h+"`, the glyph sequence at 38px is wider than 90px, so the `+` bleeds into the label cell.

**Fix**: left column must be >= 120px for any display-font value (>=32px). Hard cases with suffixes (`h+`, `M+`, `x10`, `%`, etc.) need 130 to 140px. Bump the gap to 18px too so there's breathing room between the value and label.

```css
.stat-card { display: grid; grid-template-columns: 130px 1fr; gap: 18px; }
```

**Rule**: >=120px min for any stat-card column containing a display-font big-number. Apply in Phase 3 build step before the first Playwright render, cheap to get right upfront, expensive to catch in review because the overflow only manifests at certain value strings.

**Detection during visual comparison**: look for any stat card where the value's last glyph appears to touch or overlap the label's first letter. If you squint and can't tell where the value ends, the column is too narrow.

---

## 18. Python `re.sub` HTML replacement string smuggles literal backslashes through apostrophes

**Symptom**: an apostrophe in a Python replacement string for HTML markup injection renders as `I\'m` (literal backslash visible) in the output HTML. Affects any user-facing text with contractions (`I'm`, `it's`, `don't`, `won't`, `you're`).

**Root cause**: Python string literals escape `'` inside single-quoted strings. When you pass the string to `re.sub` or embed it in a heredoc, the escape can survive into the output depending on quoting context.

**Fix**: NEVER do inline Python string substitution to splice HTML blocks that contain quoted text. Instead:

1. **Preferred**: use the `Edit` tool directly on the HTML file. Edit's `old_string` / `new_string` matching is exact and doesn't re-escape.
2. Write the new block to a temp file and splice by file read:
   ```python
   with open('/tmp/new_block.html') as f: new_block = f.read()
   html = html.replace(OLD_MARKER, new_block)
   ```
3. Base64-encode the payload before passing it through shell or re.sub.

**Reserve inline `re.sub` for**: class-name swaps, numeric value changes, quote-free identifier renames. Anything with prose / contractions / quoted attributes is a trap.

---

## 19. Playwright slide navigation, never JS-poke `.slide { display }`; always use keyboard nav

**Symptom**: Playwright screenshot of slide N renders blank or renders slide 1's content even though you set `display: flex` on slide N via `page.evaluate()`.

**Root cause**: the deck's class-based state machine (inherited from deck-builder `shell-pattern.md`) maintains internal state about which slide is active. Manually toggling `display` on `.slide` elements desynchronizes that state, the nav still thinks slide 1 is active, layout calculations run against slide 1, and the "visible" slide N renders without proper layout.

**Fix**: always advance via the deck's own keyboard nav:
```python
# To screenshot slide N:
for _ in range(N - 1):
    await page.keyboard.press("ArrowRight")
    await asyncio.sleep(0.3)  # allow transition
await asyncio.sleep(0.6)  # final settle
await page.screenshot(path=OUT)
```

**Never do**:
```python
# DON'T, breaks the nav state machine
await page.evaluate("""
  document.querySelectorAll('.slide').forEach((s, i) => {
    s.style.display = i === 2 ? 'flex' : 'none';
  });
""")
```

---

## 20. Split-panel cover, fractional crop bleeds panel background into hero image

**Symptom**: converted cover slide shows a visible dark rectangle floating over the hero photo/screenshot on the right half of the slide. Zooming in reveals fragments of the source wordmark or tagline embedded inside the hero image. Logo PNG on the left panel shows a visible rectangular frame of the panel color around the wordmark.

**Root cause**: fractional crop like `page.crop((int(w * 0.39), 0, w, h))` guesses where the left panel ends. Every deck lays the panel differently, 42%, 45%, 50%, 55% are all common. When the guess is too low, the crop includes the right edge of the panel plus whatever text sits in it. When the agent then saves the crop as a JPEG with no alpha, the bled-in panel area gets baked into the hero permanently.

In parallel, using `logo-extraction.md`'s luminance-threshold alpha pass on a **white-wordmark-on-colored-panel** source fails because the navy/teal/brand-dark panel is mid-brightness, not bright-white. The PNG saves with every pixel at alpha=255, no transparency, and when placed back on the panel in HTML, the logo's own panel-colored background shows up as a rectangle frame around the wordmark.

**Fix**:

1. **Pixel-scan for the panel edge**, don't guess fractions:
   ```python
   from crop_cover_assets import find_panel_edge, crop_hero_image
   edge = find_panel_edge('pages/page-01.png')
   crop_hero_image('pages/page-01.png', edge + 2, 'assets/hero.jpg')
   ```
2. **Use color-distance alpha** on the logo, not luminance:
   ```python
   from crop_cover_assets import extract_alpha_logo
   extract_alpha_logo(
       'pages/page-01.png',
       bg_color=(17, 58, 84),    # sample empirically from panel corners
       crop_bounds=(0.03, 0.28, 0.42, 0.60),
       tolerance=30,
       out_path='assets/logo.png',
   )
   ```
3. **Verify by compositing** a preview of logo + hero on a mock panel of the sampled color before base64-embedding. See `cover-asset-extraction.md` §After extraction.

**Detection during visual comparison**: on the cover render, look for any rectangular region of panel color where there shouldn't be one, either a dark frame around the wordmark or a ghost rectangle in the right-hand hero. The bug is invisible to the page-level source comparison because both sides show the final composited cover, not the underlying assets. Zoom into the cover-compare PNG at 200% to catch it.

---

## 21. `@keyframes transform` clobbers base `translate(-50%, -50%)` centering

**Symptom**: a centered element (cover hero, thank-you card, modal) shifts off-center or cuts off at the viewport edge mid-animation. Devtools shows `transform: translateY(14px)` instead of the expected `transform: translate(-50%, -50%) translateY(14px)`.

**Root cause**: `transform` is a single compound property. When a keyframe declares `transform: translateY(...)`, it REPLACES whatever `transform` the base rule set, including the `translate(-50%, -50%)` you used to anchor the element to its own center.

**Fix**: animate the individual `translate` / `scale` CSS properties instead of the compound `transform`. These compose with any existing `transform` rather than replacing it.

```css
/* wrong, clobbers transform: translate(-50%, -50%) */
@keyframes fade-up   { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0);  } }
@keyframes scale-in  { from { opacity: 0; transform: scale(0.94);       } to { opacity: 1; transform: scale(1);       } }

/* right, composes with base transform */
@keyframes fade-up   { from { opacity: 0; translate: 0 14px; } to { opacity: 1; translate: 0 0; } }
@keyframes scale-in  { from { opacity: 0; scale: 0.94;       } to { opacity: 1; scale: 1;       } }
```

**Detection during visual comparison**: after rendering a slide with a centered hero or card, read computed `transform` matrix on the centered element, if it's not identity-plus-translate(-50%,-50%) (the expected baseline after the animation completes), the keyframe is clobbering. Easiest to catch by scrolling the rendered PNG horizontally: centered elements cut off at the right edge or float leftward.

---

## 22. Box-shadow letterbox-extension offset must equal box width (not exceed it)

**Symptom**: CSS `box-shadow: -2000px 0 0 var(--paper), 2000px 0 0 var(--paper)` on `.s-body` should paint paper-colored bands across the letterbox on wider-than-canvas viewports, but the letterbox renders as whatever's behind (`.deck`'s ink, or default white), NOT paper. Pixel-sample at viewport edge confirms the extension isn't rendering.

**Root cause**: `box-shadow: <x> <y> <blur> <color>` with no spread value paints a **copy of the box** at the offset. The shadow has the same size as the box (e.g. 1440xh). With x-offset = -2000, the shadow rectangle lives at x=-2000 to x=-2000+1440 = -560. Its **right edge at x=-560 is still well to the left of the viewport origin (x=0)**, so the entire shadow lies in the clip region of `.deck { overflow: hidden }` and renders nowhere visible.

**Fix**: make the offset equal the box's width (or smaller), not larger. For a 1440-wide body:

```css
/* tiles adjacent copies on each side, shadow's nearest edge touches box edge */
.s-body {
  background: var(--paper);
  box-shadow: -1440px 0 0 var(--paper), 1440px 0 0 var(--paper);
}
```

Shadow at x=-1440 covers x=-1440 to x=0 (exactly adjacent to the box's left edge). On any viewport wider than canvas, the left letterbox falls within x=(viewport_stage_offset_unscaled < 0, 0), which is covered by the shadow. Same for the right.

**Rule of thumb**: *shadow-offset = box-width* is the sweet spot. Smaller offsets cause the shadow to overlap the box (visually harmless if same color, but wastes paint). Larger offsets leave a gap or push the shadow offscreen entirely.

Apply the same rule to header (`.s-hdr`) and footer (`.s-foot`) with ink extension, and to whole-slide dark backgrounds.

---

## 23. Dynamic letterbox JS toggle with DARK_SLIDES list, companion pattern to #22

**Symptom**: on decks with mixed dark and light slides (cover + thank-you are ink, interior slides are paper), a single static letterbox color creates a jarring mismatch. Unified ink letterbox sandwiches light slides as floating dark-framed cards; unified paper letterbox leaves dark slides floating with white frames.

**Root cause**: fixed-canvas decks get horizontal letterbox on wider-than-canvas viewports. The letterbox is painted by `.deck`'s background. A single color can't match both dark and light slides.

**Fix**: keep `.deck` bg as the **majority color** (paper, since most interior slides are light), and have JS swap it to ink when navigating to a dark slide:

```css
.deck { background: var(--paper); }  /* base, light slides */
```

```javascript
var deckEl  = document.getElementById('deck');
var stageEl = document.getElementById('stage');
var DARK_SLIDES = {1: true, 13: true};  // 1-indexed, cover + thank-you
function setLetterbox(i) {
  var dark = DARK_SLIDES[i+1];
  deckEl.style.background  = dark ? '#2F2F39' : '#FFFFFF';
  stageEl.style.background = dark ? '#2F2F39' : '#FFFFFF';
}
// Call from inside goTo(i) after setting active slide.
```

Combine with gotcha #22: header and footer still need `box-shadow` to extend ink across the letterbox on **light** slides so the dark bands read edge-to-edge.

**Where DARK_SLIDES comes from**: the palette analysis in Phase 1. Any slide whose source page has >90% dark background (cover, thank-you, section dividers) goes in the list.

---

## 24. Generic `[data-shot]` attribute for raster asset injection

**Symptom**: ad-hoc JS like `document.getElementById('s16-img').src = S16_SHOT` doesn't scale when a new slide type (problem slide with real photos, team slide with headshots) needs the same base64-injection pattern. You end up repeating the script for each slide.

**Fix**: every raster image that's base64-injected at runtime carries a `data-shot="<key>"` attribute; a single JS loop walks `[data-shot]` and sets `img.src` from a `SHOTS` dict keyed by the same string:

```html
<!-- S16 demo screenshot -->
<img class="s-shot-img" data-shot="s16" alt="..."/>
<!-- S04 problem-slide left photo -->
<img class="s04-photo" data-shot="s04-left" alt="..."/>
<!-- S04 problem-slide right photo -->
<img class="s04-photo" data-shot="s04-right" alt="..."/>
```

```javascript
var SHOTS = {
  's16': '<base64 data URI>',
  's17': '<base64 data URI>',
  's04-left':  '<base64 data URI>',
  's04-right': '<base64 data URI>',
};
var shotEls = document.querySelectorAll('[data-shot]');
for (var j = 0; j < shotEls.length; j++) {
  var key = shotEls[j].getAttribute('data-shot');
  if (SHOTS[key]) shotEls[j].src = SHOTS[key];
}
```

Drop-in for any new raster asset: add the attribute to the HTML, add the key to the `SHOTS` dict. No script changes.

---

## 25. Swim-lane SVG arrow overlay, viewBox-matches-rendered pattern

**Symptom**: the source has a 3-lane swim-lane flow diagram with circles connected by vertical arrows across lanes. Your HTML rebuild gets the circles right but the arrows are missing, or they render but don't align with the circle centers.

**Fix**: overlay a single SVG on the swim-lane container, sized to match the container exactly, with `preserveAspectRatio="none"` so arrow coordinates map 1:1 onto the grid cells:

```html
<div class="s06-body">
  <!-- z-index above lanes, pointer-events: none so circles stay clickable -->
  <svg class="s06-arrows" viewBox="0 0 1320 780" preserveAspectRatio="none">
    <defs>
      <marker id="arr-dn" markerWidth="10" markerHeight="10" refX="5" refY="8" markerUnits="userSpaceOnUse">
        <polygon points="0,0 10,0 5,8" fill="#2F2F39"/>
      </marker>
      <marker id="arr-up" markerWidth="10" markerHeight="10" refX="5" refY="2" markerUnits="userSpaceOnUse">
        <polygon points="5,2 0,10 10,10" fill="#2F2F39"/>
      </marker>
    </defs>
    <!-- Lines positioned via grid math, not eyeballing -->
    <line x1="305" y1="195" x2="305" y2="548" marker-end="url(#arr-dn)"/>
    ...
  </svg>
  <!-- lane rows ... -->
</div>
```

```css
.s06-arrows {
  position: absolute;
  left: 60px; right: 60px;   /* matches body horizontal padding */
  top: 85px;                 /* below any phase-chevron header row */
  bottom: 48px;              /* above footer */
  pointer-events: none;
  z-index: 3;                /* above lane backgrounds */
}
.s06-arrows line { stroke: var(--ink); stroke-width: 2; }
```

### Grid-math for coordinates

Don't eyeball. Compute column centers from the actual CSS grid spec.

### ViewBox = rendered box

Use `preserveAspectRatio="none"` and size the viewBox to match the SVG's rendered pixel box (computed from the body's usable vertical space).

---

## 26. Composite slide, HTML text overlays raster text, both render

**Symptom**: a thank-you / contact / closing slide shows duplicated or "ghost" text. One copy reads crisp (the HTML version); a fainter or misaligned second copy bleeds through from under it, often clipped at a column edge.

**Root cause**: the source slide is a split layout, text block on one side, photo on the other, and the conversion extracted the **entire source page** as a single raster for use as a background or one half of a two-column HTML layout, while the HTML ALSO rebuilt the text block natively as CSS-styled rows. Both sets of text render.

**Why it's not caught earlier**: raster extraction defaults to "page N has a hero photo, extract the whole page as one PNG." For pure photo slides, fine. For split-layout slides where half the page is structured text the HTML is rebuilding, that default is the bug.

**Fix**: for composite slides, crop the raster to only the region the HTML is NOT rebuilding. If the HTML owns the left column and the photo sits in the right column:

```python
from PIL import Image
src = Image.open('pages/page-27.png').convert('RGB')
w, h = src.size
# Keep only the right panel, sample the split point empirically or via find_panel_edge()
split_x = int(w * 0.52)
right = src.crop((split_x, 0, w, h))
right.save('assets/ty-photo-only.jpg', 'JPEG', quality=82, optimize=True)
```

**Detection**:
1. During visual comparison, look for any text on a text-rebuilt slide that appears twice, or any text that appears to start mid-word at a column edge.
2. Before export, check for any raster asset whose filename suggests a full-page extract being placed inside a partial-width HTML column, that combination is the smell.

**Rule of thumb**: if you're using `.col { width: 50% }` or similar to place a raster into half a slide, the raster should have been cropped to roughly 50% of its source width before encoding. Full-page rasters belong on full-bleed slides only.

---

## 27. Slide-class `position: relative` overrides base `.slide` absolute positioning

**Symptom**: an entire slide-type renders shorter than the 810px canvas. Background gradients and full-bleed images end mid-page; raw letterbox color appears below the content.

**Root cause**: the base `.slide` rule declares `position: absolute; inset: 0` (or equivalent `top/left/right/bottom: 0`), which forces every slide to fill the 1440x810 canvas exactly. When a per-type class, `.s-cover`, `.s-services`, `.s-ty`, anything `.s-<role>`, ALSO declares `position: relative`, it wins on cascade specificity (or just order-of-declaration when specificity ties) and replaces the absolute positioning. The slide then sizes to its content height instead of filling the canvas.

**Fix**: never declare `position` on slide-type classes. Strip any `position: relative` (or `position: absolute`) declaration from `.s-<role>` rules and leave the base `.slide` to handle positioning context.

```css
/* correct, base owns positioning */
.slide {
  position: absolute;
  inset: 0;
  width: 1440px;
  height: 810px;
}

.s-cover {
  /* No position declaration. Children absolute-anchor to .slide. */
  background: linear-gradient(180deg, var(--ink) 0%, #1B3A6B 100%);
}
```

**Detection**: render the slide at desktop resolution and look at the bottom edge of the canvas. If the background color or gradient stops mid-page and letterbox color shows below, check the slide-type class's `position` declaration. Also grep the CSS file: `grep -n "position: relative" deck.css | grep "\.s-"` should return ZERO matches in a healthy build.

---

## 28. `<a:custGeom>` half-dome shapes, don't default to `border-radius: 50%`

**Symptom**: source slide has a logo "straddle" pattern, a row of dome-shaped containers sitting on a wave divider, each holding a logo, with only the top hemisphere of the dome visible above the wave. Your HTML reproduces the dome row but the shapes look slightly off.

**Root cause**: source shapes are `<a:custGeom>` in the PPTX with explicit cx and cy from `<a:xfrm><a:ext>`. The ratio is informative:

- `cx:cy is roughly 2:1` (e.g., 200x100 EMU), true semicircle. Build with `border-radius: <cy>px <cy>px 0 0` where `cy = half of cx`.
- `cx:cy is roughly 1.55:1` (e.g., 213x137 EMU), half-dome. Build with `border-radius: <cx/2>px <cx/2>px 0 0`. The dome is wider than it is tall, so the top corners curl back inward more aggressively.
- `cx:cy is roughly 1:1`, full circle. `border-radius: 50%`.

Defaulting to `border-radius: 50%` on any of these produces a full-circle silhouette. With the dome anchored on a wave divider, the lower hemisphere pokes below the wave instead of being clipped by it.

**Fix**: inspect the ratio in Phase 1 (see SKILL.md Phase 1 step 9) and pick the recipe from the ratio bucket.

```css
/* True semicircle, cx:cy = 2:1 */
.dome-semi {
  width: 160px;
  height: 80px;
  border-radius: 80px 80px 0 0;       /* full top rounding, flat bottom */
}

/* Half-dome, cx:cy is roughly 1.55:1 */
.dome-half {
  width: 213px;
  height: 137px;
  border-radius: 106.5px 106.5px 0 0; /* cx/2 for both top corners */
}

/* Anchored on the divider, clip lower body, prevent overflow showing */
.dome-row {
  position: absolute;
  bottom: 120px;                       /* divider's top edge */
  display: flex;
  gap: 24px;
}
.dome-row > .dome-semi,
.dome-row > .dome-half {
  align-self: flex-end;                /* flat bottom rests on the divider line */
}
```

**Detection**: read the source page at 200%. If you see a row of domes that visually anchor on a curve/divider, inspect the PPTX for `<a:custGeom>` and read each shape's `cx:cy`. Map to the ratio bucket. Reject any visual that has a dome's lower hemisphere showing below the divider.

---

## 29. JSON injection into base64-heavy SHOTS object fails unpredictably

**Symptom**: after modifying `const SHOTS = {...};` via text find/replace, the JSON parses with errors like "Extra data" or "Expecting ',' delimiter" at high character positions. Browsers silently fail to load any `[data-shot]` images, the whole image wall goes blank with no console error.

**Root cause**: base64-encoded strings inside SHOTS contain edge cases, when one value is `data:image/png;base64,...` and the next is `data:image/jpeg;base64,...`, the boundary may include sequences that look like JSON structural characters to a naive parser. Text-based find-and-replace can match the wrong closing brace because `}` appears inside base64 payloads more often than you'd expect.

**Fix**: never inject into the existing SHOTS object. Rebuild from a Python dict:

```python
import base64, json, os

result = {}
for key, (base_dir, fname, mime) in SHOTS_MAP.items():
    p = os.path.join(base_dir, fname)
    b64 = base64.b64encode(open(p, 'rb').read()).decode()
    result[key] = f'data:image/{mime};base64,{b64}'
shots_json = json.dumps(result, separators=(',', ':'))

src = open(html_path).read()
i0 = src.find('const SHOTS = ')
i_end = src.find("document.querySelectorAll('[data-shot]')", i0)
i_nl = src.rfind('\n', i0, i_end)
new_src = src[:i0] + f'const SHOTS = {shots_json};' + src[i_nl:]
open(html_path, 'w').write(new_src)

# VALIDATE, parse the new SHOTS region before declaring success
ni0 = new_src.find('const SHOTS = ')
ni1 = new_src.find('};\n', ni0)
json.loads(new_src[ni0 + 14:ni1 + 1])  # raises on failure
```

The downstream landmark `document.querySelectorAll('[data-shot]')` is stable across builds. Don't use bare `};` as the boundary because base64 + JS-block boundaries are not 1:1, `};` can appear inside a base64 payload at the wrong place.

**Detection**: after any SHOTS modification, programmatically extract and `json.loads` the object. Eyeballing is not reliable at this scale; the failure surfaces only at runtime as missing images, and only when the malformed value happens to be one of the later entries.

---

## 30. Banner pill text appears stuck to the top of the pill

**Symptom**: a bordered pill like `<div class="banner-pill">Some text</div>` with `padding: 14px 38px` has its text visually closer to the top of the pill than the bottom. The pill appears taller than necessary, and the imbalance varies subtly across font families.

**Root cause**: block-level elements use the line-box default flow, which is biased by the font's ascender/descender ratio. Manrope's ascender is taller than its descender, so text sits visually higher in the line-box than mathematical center. Block-level padding adds the same amount above and below the line-box, but the line-box itself is asymmetric, so the result is asymmetric.

**Fix**: use inline-flex centering:

```css
.banner-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1.1;
  min-height: 52px;
  padding: 14px 38px;
}
```

- `inline-flex` keeps the pill width hugging content (no full-row expansion).
- `align-items: center` does the vertical centering on the flex axis, which uses the box's mathematical center regardless of typeface metrics.
- `min-height` guarantees a consistent pill height even if `line-height` changes.
- `line-height: 1.1` keeps the text node tight so flex centering has room to work.

**Detection**: render the pill at 200% and measure the gap above vs below the text. They should be equal. If the top gap is visibly larger than the bottom (or vice versa), the line-box flow is doing the centering rather than flex.

---

## 31. Headline Y position drifts across slides

**Symptom**: reading the deck slide-by-slide, the title text appears at slightly different vertical positions per slide. Some slides feel like the title is higher, others lower. Eyebrow pills on some slides cause additional drift. Each individual slide looks fine in isolation; only the slide-to-slide comparison reveals the inconsistency.

**Root cause**: per-slide `.slide-title` selectors accumulate `margin-top` overrides (`margin-top: 0`, `margin-top: 6px`, `margin-top: 10px`) over multiple build iterations. Each adjustment fixed the slide it was made on but didn't propagate to the others. Combined with eyebrow presence on some slides (which sits absolutely at `top: 36px` but visually overlaps with the title's render zone), the title's effective position varies.

**Fix**: lock the base `.slide-title` rule ONCE and never override layout, only font-size:

```css
.slide-title {
  margin: 0 auto;
  text-align: center;
  min-height: 64px;
  max-width: 1280px;
  font-size: 54px;
  font-weight: 700;
  line-height: 1.12;
  letter-spacing: -0.02em;
  color: var(--ink);
}

/* Per-slide overrides: ONLY font-size, never layout */
.s-problem .slide-title { font-size: 50px; }      /* outlier: long title */
.s-gtm    .slide-title { font-size: 48px; }      /* outlier: 2-line wrap */
```

Per-slide rules touch ONLY `font-size`. No `margin` overrides, no `text-align` overrides, no `max-width` overrides. Source files that have a mix of left- and center-aligned titles get converted to all-centered for HTML coherence, source-faithfulness yields to consistency on this axis. The user's eye registers slide-to-slide title drift faster than a 2-degree alignment delta from the source.

**Detection**: render the deck full-screen and tab through slides slowly. The title baseline should not move vertically. If it moves, grep the CSS for `.slide-title` overrides and verify each only touches `font-size`.

---

## 32. Source-text ghosting on photo-bleed slides (Mode B only)

**Failure mode**: In Mode B reconstruction, embedding a full source page raster as a slide background and then overlaying matching title text in HTML creates a visible "double exposure", the source's title is already baked into the photo, so the HTML title sits directly over the source title, slightly offset, with both readable.

**Detection signal**: Cover, Problem, Integration, and Thank-You slides where the source has photo backgrounds with overlaid titles. Read the slide screenshot and verify only ONE copy of every title-word appears.

**Root cause**: Source page rasters contain ALL source content, including title text. They're not "background photos", they're rendered slides. Using them as backgrounds and overlaying matching titles is content double-up.

**Fix priority order**:
1. **Switch to Mode A.** Mode A renders the source page as-is, no overlay; no ghosting possible. This is the right answer for any photo-heavy slide.
2. If Mode B is required for the slide (e.g., interactive demo): crop only the photographic region, excluding the source title area, before using as a background.
3. Last resort (Mode B, full-page raster only available): apply heavy Gaussian blur (radius >= 24) plus an opacity scrim. This obliterates the baked-in text while preserving photographic mood. Don't rely on this, find a cleaner asset if possible.

---

## 33. Off-by-one source page references in Phase 1 crops

**Failure mode**: Phase 1 extracted "right side of source slide N" but cropped from `page-N.png` when the intent was `page-(N+1).png` (or vice versa). Result: the market slide's right-side construction-worker photo turned out to be the comparison-table slide cropped wrong.

**Detection signal**: A slide's embedded image content doesn't match the slide's narrative, text says "construction worker at site" but image shows a table.

**Root cause**: Source pages are 1-indexed but it's easy to confuse "source page N" with "output slide N" when they share numbering. Phase 1 crops should record `source_page_num` explicitly.

**Fix**: Phase 1 extraction must label every crop with `(source_page_num, crop_region, intent_description)` in `classification.json`. Reviewers should verify `intent_description` matches what's actually visible in the crop.

---

## 34. Mode A SHOTS dict is keyed by string slide number, not page filename

**Failure mode**: Building the SHOTS dict with `shots[i] = data_uri` (integer key) produces JSON with numeric keys after `json.dumps`, but HTML `data-shot="1"` is a string. Lookup fails silently, every `.slide-img` shows empty background.

**Detection signal**: Mode A render shows pure white slides instead of source pages. SHOTS object inspects as `{"1": "data:..."}` in JSON (string keys per JSON spec) but the JS `SHOTS[el.getAttribute("data-shot")]` may return undefined depending on how the dict was built.

**Root cause**: Python int keys get coerced to strings on `json.dumps`, but if the dict is built dict-comprehension-style with int keys, the resulting JSON is fine. The bug is more often in HTML, `data-shot="01"` (zero-padded) won't match `SHOTS["1"]`.

**Fix**: Use string keys consistently, `shots[str(i)] = data_uri` in Python, `data-shot="1"` (not `"01"`) in HTML. Or zero-pad both sides.

---

## 35. Playwright Chromium install fills `~/.cache/ms-playwright` and fails

**Failure mode**: `python3 -m playwright install chromium` errors with `ENOSPC` because the default install path `~/.cache/ms-playwright` sits on a small `/` partition (roughly 2 GB free in many sandboxes) and Chromium needs roughly 108 MB plus the host headless shell.

**Detection signal**: Install errors with `ENOSPC` and `Failed to download Chrome for Testing`. Visual-comparison loop blocked.

**Fix**: Install to `/tmp/pw-browsers` instead.

```bash
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers
python3 -m playwright install chromium
```

Then prepend `os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/tmp/pw-browsers'` to any Python script that uses `sync_playwright()`. `/tmp` has roughly 10 GB free in most sandboxes so the install succeeds.

---

## 36. INVESTOR PRESENTATION (and similar text markers) sampled as brand accent

**Failure mode**: Phase 1 palette sampling picks up bright-saturated text colors (e.g., purple `#7B3FA0` rendered as a one-off CTA on a cover) and classifies them as brand accents. In Mode B reconstruction, the wrong accent gets propagated across the deck (orange CTAs everywhere, when actually the cover CTA was purple as a one-off text marker).

**Detection signal**: Mode B deck shows a different accent color than the source for body text. Phase 1's detected accent is `#7B3FA0` but the source's actual brand orange is `#E15A3C`.

**Root cause**: Palette sampling doesn't distinguish "deck-wide brand accent" from "one-slide text marker color". Bright saturated colors that appear on a single slide are usually text markers, not brand accents.

**Fix**: Phase 1 palette detection should weight a color's brand-accent confidence by the number of slides where it appears. A color present on >=3 slides is a brand accent. A color present on only 1 slide is a text marker, record separately, do not propagate. Detection script update needed in `scripts/detect_palette.py`.

**Workaround until script fix**: When user reviews the Phase 2 confirmation, the Palette row shows the candidates with slide-counts. User can edit "accent should be #E15A3C not #7B3FA0".

**Mode A escape hatch**: Mode A doesn't use the detected palette except for the shell letterbox + brand bar. The slide content's colors are baked into the JPEG rasters. So this gotcha only affects Mode B.
