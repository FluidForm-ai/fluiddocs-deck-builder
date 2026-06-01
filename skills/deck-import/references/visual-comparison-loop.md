# Visual Comparison Loop, Phase 4 Verification Gate

A companion to `review-adaptations.md`. Where that file tells reviewers HOW to calibrate, this file tells the agent (you) HOW to run an **iterate-until-aligned visual loop** BEFORE the reviewers run. Treat this as a pre-review gate: if source and HTML disagree visually, fix first, review second.

**Why this exists**: early conversion runs shipped with component overlap, palette drift, and logo mismatch because the reviewers ran against the HTML in isolation, no one was paired source-vs-HTML. A side-by-side grid is the cheapest way to catch fidelity drift, and it doubles as an artifact you can paste back to the user to show your work.

---

## The three-script loop

Every conversion Phase 3, Phase 4 transition runs this loop. All three scripts live in the **working directory** for the conversion (e.g., `/tmp/deck-import-<timestamp>/`), not in the skill, they're per-conversion artifacts, not reusable infrastructure.

### 1. `assemble.py`, rebuild the HTML

Combines the CSS, the per-slide HTML constructors, and the shell/nav/JS into the final file.

Structural requirements:
- CSS lives in a separate `deck_css.txt` so it can be edited independently.
- Per-slide HTML constructors live in `build_html.py` as `slide_NN_<role>()` functions. A single `SLIDES` list determines order.
- `assemble.py` uses `exec(code, ns)` to pick up `SLIDES` and `ROLES` from `build_html.py`.
- Output path: the final release path.

Rebuilding must be idempotent and fast (<2s). If it takes longer, you're doing too much work per build.

### 2. `render.py`, screenshot every slide with Playwright

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={'width': 1440, 'height': 810}, device_scale_factor=1)
    page = ctx.new_page()
    page.goto('file://' + HTML, wait_until='networkidle')
```

Navigate slide-by-slide via the deck's keyboard nav (see the Navigation rule below). Screenshot `full_page=False` so you get the 1440x810 viewport not the scrolled body.

Output: `renders/slide-NN.png`, one per slide.

### 3. `compare.py`, generate side-by-side grids

For each slide index:
- Open `pages/page-NN.png` (source) and `renders/slide-NN.png` (HTML).
- Resize both to the same width (900px recommended) preserving aspect.
- Paste side-by-side onto a canvas with a dark header bar labeling SOURCE vs REBUILT.
- Save as `compare/cmp-NN.png`.

Read the comparison PNGs back with the Read tool (they're images; multimodal agents see them natively). You don't need a fancy diff algorithm, your eyes catch palette drift, overlap, and component misplacement in a single pass.

---

## The loop itself

```
assemble, render, compare, READ the compare images
  v (defects visible)
edit deck_css.txt or build_html.py
  v
assemble, render, compare, READ again
  v (defects resolved OR below threshold)
proceed to Phase 4 (3 reviewers)
```

**Stop criterion**: every slide's comparison PNG shows "structurally equivalent" layout. Structurally equivalent means:
- Same visual hierarchy (hero element in same zone)
- Same color distribution (no bright orange where source was cream)
- No components overlapping that weren't overlapping in the source
- Logos, wordmarks, and key text in matching positions

**Not required**: pixel-perfect match. This is a conversion, not a photocopy. Typography rendering, font hinting, and sub-pixel anti-aliasing will always differ.

**Budget**: roughly 3 to 5 loop iterations is normal for a 14 to 22 slide deck. If you're on iteration 8 and the same slide keeps breaking, step back, you're probably fighting the wrong CSS. Check for specificity wars, inherited flex constraints, or a parent rule overriding your fix.

---

## Palette sampling, do this in iteration 1

Before touching layout, sample the source palette empirically. The extraction script's aggregated palette is good for the brief but can miss corner-accent gradients.

```python
from PIL import Image
import numpy as np
img = np.array(Image.open('pages/page-02.png').convert('RGB'))
h, w = img.shape[:2]
# Sample corners + center
for name, (y, x) in [('TL',(10,10)),('TR',(10,w-10)),('BL',(h-10,10)),('BR',(h-10,w-10)),('C',(h//2,w//2))]:
    r,g,b = img[y,x]
    print(f'{name}: #{r:02X}{g:02X}{b:02X}')
```

Lesson learned in early runs: source looked warm/orange because of a subtle bottom-right radial gradient. Base was **#F9F9F9** (near-white). The HTML rebuild initially used an aggressive warm gradient across the whole canvas, totally wrong. Five minutes of sampling would have caught it before any CSS was written.

Corollary: when in doubt, make the background near-white and add accent only in one corner. Most modern decks (2023+) use near-white bases with subtle radial accents, not full warm washes.

---

## What to look for in each comparison PNG

Check in this order (easy wins first):

1. **Color cast**: does the HTML look warmer / cooler / more saturated than the source? fix `.slide` background before touching anything else.
2. **Logo and wordmark**: are they the right shape and position? Custom brand typography, extract as raster (see `logo-extraction.md`).
3. **Hero element position**: is the big thing in the right quadrant?
4. **Text overlap**: are labels, pills, or headers colliding with body copy? Usually an absolute-positioned element that forgot its container.
5. **Grid alignment**: are N-column grids lining up? Check `grid-template-columns` vs the source's visual bounds.
6. **Micro-typography**: line-height, letter-spacing, font-weight mismatches. Fix last, they're the finest-grained.

Most conversion defects are in categories 1 to 3. Don't rabbit-hole on category 6 if categories 1 to 3 still have issues.

---

## Output contract from the visual loop

When the loop finishes, you should have:
- `/tmp/deck-import-<ts>/renders/`, one PNG per slide at 1440x810
- `/tmp/deck-import-<ts>/compare/`, one side-by-side PNG per slide
- A clean HTML file at the release path

Archive the compare grids with the brief, they're valuable for Phase 6 (Learn) and for the Release message ("here's each slide paired against source, for your review").

---

## Fallback when Playwright can't install

Playwright needs roughly 500MB for the chromium download. In constrained sandboxes (CI with a full disk, offline VM, strict egress policy), the install fails and the visual loop above becomes impossible to run. **Do not skip verification** in that case, fall back to the structural check.

Run `scripts/structural_check.py` from the skill:

```bash
python ${SKILL_DIR}/scripts/structural_check.py \
    <output>.html --expected-slides 15
```

It validates seven mechanical properties without a browser:

1. Slide count matches the expected spine
2. No stray emoji/symbol codepoints
3. No duplicate element IDs
4. `href="#..."` anchors resolve to real `id=`s in the doc
5. Every base64 data URL parses cleanly (no truncated blobs)
6. No era fragments (`Page 14 of 22`, `Slide 3/15`, etc.)
7. If the cover has `panel-left`, it also has `panel-right`

Exits 0 on pass, 1 on fail, 2 on script error. A clean pass is NOT equivalent to a visual comparison, it catches roughly 80% of real defects (wrong slide count, orphaned anchors, broken logos) but won't catch palette drift, hero-misposition, or overlap. When Playwright returns, re-run the full visual loop before the release if the deck is still editable.

Record the fact that you fell back in the conversion brief appendix so the next run knows to budget disk for Playwright up front.

---

## Navigation rule, always use the deck's keyboard nav

To screenshot slide N in Playwright, call `page.keyboard.press("ArrowRight")` N-1 times and wait roughly 300ms between presses, then a final 600ms settle before the screenshot. The deck's nav maintains internal state that layout calculations depend on, JS-poking `.slide { display: ... }` directly bypasses that state and renders blank or mis-laid-out slides.

```python
async def goto_slide(page, n):
    for _ in range(n - 1):
        await page.keyboard.press("ArrowRight")
        await asyncio.sleep(0.3)
    await asyncio.sleep(0.6)
```

Never do `page.evaluate("document.querySelectorAll('.slide').forEach(...)")`, that's a category-9 shell-divergence trap. See `css-gotchas.md` #19 for the full root-cause writeup.

### Silent-failure warning, the active class is `.active`, not `.is-active`

If you ignore the above and JS-poke anyway (don't), the class name is **`active`**. The shell CSS has:

```css
.slide { display: none; opacity: 0; }
.slide.active { display: flex; opacity: 1; }
```

There is no `.is-active` rule. Flipping `classList.add('is-active')` is a no-op: every slide stays `display: none`, every screenshot comes back as the cover or empty, and the visual loop gaslights you into thinking the build is broken when it's the render harness.

If you absolutely must JS-poke (e.g., keyboard nav is blocked by the host), belt-and-suspender both: toggle the class AND set inline style fallbacks so a class-name typo can't hide the slide:

```python
page.evaluate(f"""
    () => {{
        const slides = document.querySelectorAll('.slide');
        slides.forEach((s, idx) => {{
            if (idx === {i-1}) {{
                s.classList.add('active');
                s.style.display = 'flex';
                s.style.opacity = '1';
            }} else {{
                s.classList.remove('active');
                s.style.display = 'none';
                s.style.opacity = '0';
            }}
        }});
    }}
""")
```

---

## Playwright Chromium install hygiene

Playwright's default install path is `~/.cache/ms-playwright`. In many sandboxes, `/` has limited space which is insufficient for the Chromium download (roughly 108 MB) plus the headless shell. Use `/tmp` instead, it has more headroom.

```bash
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers
pip install playwright --break-system-packages
python3 -m playwright install chromium
```

When running Playwright from a Python script, set the env var before importing:

```python
import os
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/tmp/pw-browsers'
from playwright.sync_api import sync_playwright
```

If you skip this, the first install attempt errors with `ENOSPC` / `Failed to download Chrome for Testing` and the visual-comparison loop is blocked until reinstall succeeds.

Logged as `css-gotchas.md` #35.
