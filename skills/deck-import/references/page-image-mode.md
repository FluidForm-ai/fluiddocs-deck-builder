# Mode A · Page-Image Build (DEFAULT)

When the conversion brief's `build_mode: page-image`, every slide is a full-bleed background image of the corresponding source page. The HTML provides only the shell, role-meta pill on interior slides, progress bar, nav arrows, counter, scale-to-fit canvas, touch swipe. No per-slide CSS, no content reconstruction.

**Pixel-faithful by construction.** The source IS the output. There is no palette to guess, no typography to match, no source-text ghost to fight, no logo to recreate, no diagram to redraw. This is the right answer for roughly 90% of conversions and the documented default.

---

## When Mode A is right

- User wants a shareable HTML version of their existing deck.
- User does not plan to edit slide content in HTML.
- Source has photo-heavy backgrounds, custom typography, custom illustrations, complex diagrams, or any visual the user is happy with.
- User said "convert", "import", "upgrade my deck", or "make it shareable" without saying "rebuild" / "redesign" / "edit" / "interactive demo".

## When to switch to Mode B

- User explicitly replies `reconstruction` / `rebuild` / `rebuild in HTML` in Phase 2.
- User opts into an interactive demo on a pitch or launch deck, Mode A can't host live `<input>`/`<button>` over a static page image, so opting into an interactive demo automatically flips `build_mode: reconstruction`.
- User says they want to edit specific slides later.
- User asks to upgrade specific visual components (animated KPI count-up, clickable comparison table, etc.).

---

## Asset extraction

For each source page, render a JPEG at quality=70, width=1400. This keeps a 16-slide deck under the 2.5 MB cap.

```python
from PIL import Image
import base64, json

shots = {}
for i in range(1, page_count + 1):
    im = Image.open(f"{EXTRACT_DIR}/pages/page-{i:02d}.png").convert('RGB')
    target_w = 1400
    new_h = int(im.height * target_w / im.width)
    im = im.resize((target_w, new_h), Image.LANCZOS)
    dst = f"{ASSETS_DIR}/slide-{i:02d}.jpg"
    im.save(dst, 'JPEG', quality=70, optimize=True)
    shots[str(i)] = "data:image/jpeg;base64," + base64.b64encode(open(dst, 'rb').read()).decode()

with open(f"{ASSETS_DIR}/shots.json", 'w') as f:
    json.dump(shots, f)
```

For PPTX-only input, render each slide to PNG via LibreOffice headless conversion first when LibreOffice is installed (`libreoffice --headless --convert-to png --outdir <out> <pptx>`), then feed those PNGs into the loop above. If LibreOffice is not available, ask the user to provide a PDF render of the deck, or fall back to Mode B reconstruction.

**Calibration table** (informational, for decks that need different settings):

| Deck length | Width | Quality | Approx base64 payload | Notes |
|---|---|---|---|---|
| 11 slides | 1500 | 76 | roughly 1.9 MB | sales |
| 12 slides | 1400 | 74 | roughly 2.0 MB | launch |
| 14 to 16 slides | 1400 | 70 | roughly 2.4 MB | pitch / all-hands |
| 28 slides | 1200 | 64 | roughly 2.4 MB | keynote |

Always validate the final HTML stays under 2.5 MB. If it doesn't, drop width by 100px or quality by 4 and re-encode.

---

## Shell structure

The shell pattern is fixed. Copy this exactly.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{Company}}, {{Type Label}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=block" rel="stylesheet">
<style>
:root {
  --ink:           {{detected_ink}};         /* sampled from cover; fallback #104858 */
  --brand:         {{detected_accent}};       /* sampled from cover; fallback #DC4C30 */
  --letterbox:     {{detected_letterbox}};    /* darker ink variant; fallback #0E3F50 */
  --font-mono:     'JetBrains Mono', ui-monospace, monospace;
  --fs-footnote:   10px;
  --fs-mono:       12px;
  --fs-eyebrow:    11px;
}

/* The viewport-meta is `width=device-width, initial-scale=1`. NEVER width=1440,
   see css-gotchas.md #11 for the mobile failure mode. */

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  height: 100%;
  overflow: hidden;
  background: var(--letterbox);
  font-family: 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
body.fonts-loading .deck { visibility: hidden; }

.deck-outer {
  position: fixed; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: var(--letterbox);
  overflow: hidden;
}

.deck {
  position: relative;
  width: 1440px; height: 810px;
  background: #FFFFFF;
  transform-origin: center center;
  overflow: hidden;
  flex-shrink: 0;
}

.slide {
  position: absolute; inset: 0;
  display: none;
  overflow: hidden;
  background: #FFFFFF;
  opacity: 0;
  transition: opacity 300ms ease;
}
.slide.active { display: block; opacity: 1; }

.slide-img {
  position: absolute; inset: 0;
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}

/* === Navigation chrome (inside .deck so it scales) === */
.progress-line {
  position: absolute; top: 0; left: 0;
  height: 3px;
  background: var(--brand);
  width: 6.25%;
  transition: width 320ms ease;
  z-index: 100;
}
.nav-counter {
  position: absolute; bottom: 18px; left: 28px;
  font-family: var(--font-mono);
  font-size: var(--fs-mono);
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.92);
  background: rgba(14, 63, 80, 0.55);
  backdrop-filter: blur(6px);
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  z-index: 100;
}
.nav-arrows {
  position: absolute; bottom: 16px; right: 28px;
  display: flex; gap: 10px; z-index: 100;
}
.nav-btn {
  width: 40px; height: 40px; border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.55);
  background: rgba(14, 63, 80, 0.45);
  backdrop-filter: blur(6px);
  color: #FFFFFF;
  cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all 180ms ease;
  padding: 0;
}
.nav-btn:hover { border-color: var(--brand); background: var(--brand); }
.nav-btn svg { width: 16px; height: 16px; }

/* === Slide role meta (injected via JS on interior slides) === */
.slide-meta {
  position: absolute; top: 22px; left: 28px;
  z-index: 5;
  font-family: var(--font-mono);
  font-size: var(--fs-footnote);
  color: rgba(255, 255, 255, 0.92);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 600;
  background: rgba(14, 63, 80, 0.55);
  backdrop-filter: blur(6px);
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.s-cover .slide-meta { display: none; }
</style>
</head>
<body class="fonts-loading">
  <div class="deck-outer">
    <div class="deck">
      <div class="progress-line"></div>

      <!-- One section per source slide. data-role drives the meta pill. -->
      <section class="slide s-cover active" data-role="Cover">
        <div class="slide-img" data-shot="1"></div>
      </section>
      <section class="slide" data-role="{{role_2}}">
        <div class="slide-img" data-shot="2"></div>
      </section>
      <!-- ... slides 3..N ... -->

      <div class="nav-counter"><span class="current">01</span> / <span class="total">{{N}}</span></div>
      <div class="nav-arrows">
        <button class="nav-btn prev" aria-label="Previous slide">{{chevron-left-svg}}</button>
        <button class="nav-btn next" aria-label="Next slide">{{chevron-right-svg}}</button>
      </div>
    </div>
  </div>

<script>
const SHOTS = {{shots_dict_inlined}};

(function init() {
  // 1. Inject background images
  document.querySelectorAll('.slide-img').forEach(el => {
    const k = el.getAttribute('data-shot');
    if (SHOTS[k]) el.style.backgroundImage = 'url("' + SHOTS[k] + '")';
  });

  // 2. Inject role-meta pill on interior slides
  document.querySelectorAll('.slide:not(.s-cover)').forEach(s => {
    const role = s.getAttribute('data-role') || '';
    if (role) {
      const meta = document.createElement('div');
      meta.className = 'slide-meta';
      meta.textContent = role;
      s.appendChild(meta);
    }
  });

  // 3. Scale-to-fit + nav (boilerplate)
  // ... standard scale, go(), keyboard, touch handlers ...
})();
</script>
</body>
</html>
```

---

## Per-type cover labels

The Phase 1 detected type drives a label that may be rendered inside the deck shell (in titles, meta, or an optional cover pill). The second field after `·` is type-specific context (sector for pitch, industry for sales, etc.).

| Detected type | Label format | Example |
|---|---|---|
| pitch | `Pitch Deck · {{sector}}` | `Pitch Deck · ConstructionTech` |
| sales | `Sales Deck · {{industry}}` | `Sales Deck · Construction SaaS` |
| launch | `Launch Deck · {{product}}` | `Launch Deck · Passport v2` |
| keynote | `Keynote · {{venue_or_topic}}` | `Keynote · TED-style Construction` |
| all-hands | `All-Hands · {{month}}` | `All-Hands · May 2026` |

If the context field is unknown after Phase 1, omit the ` · {{context}}` suffix entirely.

---

## Self-lint (Mode A)

Before declaring the build complete, the structural check must pass these:

- `<section class="slide">` count = source page count
- `SHOTS` object is valid JSON (`json.loads` after extracting `const SHOTS = {...};`)
- N-1 `.slide-meta` pills injected on interior slides (count: total slides , 1)
- Letterbox color, brand color set as CSS variables (not inline literals)
- `<meta name="viewport" content="width=device-width, initial-scale=1">` (never `width=1440`)
- No emoji codepoints anywhere
- File size between 1.5 MB and 2.5 MB (16-slide pitch is roughly 2.4 MB at q70/w1400)

Run `scripts/structural_check.py <output.html>`, it checks all of the above plus base64-blob integrity and anchor-target validity.

---

## Reviewer scope under Mode A

Per `references/review-adaptations.md` (mode-aware section): Mode A skips Brand and Copy reviewers because the source IS the output. Only **Layout** runs. The Copy Reviewer's type-specific advisory layer (e.g., "your pitch deck has no Team / Traction / Ask slide") still surfaces as advisory notes in Release, but those gaps are in the source, not the conversion.

---

## What Mode A does NOT do

- **No reconstruction.** No HTML rebuild of any slide content.
- **No palette overrides.** The slide images carry their own colors. Only the SHELL (letterbox, brand bar, nav pills) uses CSS variables, and those defaults are fine for almost every deck.
- **No typography rendering.** Source fonts are baked into the slide PNGs. The shell uses Inter + JetBrains Mono for its own chrome only.
- **No interactive demo.** Mode A can't host live `<input>`/`<button>` over a static page image. Switch to Mode B for that.
- **No animated stat count-ups.** Same reason.
- **No scrollable timelines.** Same reason.
- **No editable content.** Slide content is bitmap. Editing means re-exporting from the source app and re-running Mode A.

For any of the above, switch to Mode B during Phase 2.
