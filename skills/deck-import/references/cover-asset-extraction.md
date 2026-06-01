# Cover Asset Extraction, Split-Panel Covers

Companion to `logo-extraction.md`. That file handles single-logo-on-white extraction; this file handles the harder case: a **split-panel cover** where the left panel is a saturated brand color carrying a wordmark + tagline + contact, and the right panel is a photo or screenshot. Most pitch deck covers from 2022+ are this layout.

The failure mode is specific and keeps reappearing across conversions: fractional crops bleed source panel background + wordmark fragments into the extracted hero image, or bake the panel fill into the logo PNG as a visible frame. The fix is deterministic pixel-scan, not guessed fractions.

---

## Why fractional crops fail

A first-pass extraction hard-codes:

```python
# WRONG, bleeds panel background into hero
phones = page.crop((int(w * 0.39), 0, w, h))
```

This guesses that the left panel ends at x=0.39 of page width. On real decks the panel often actually extends to x=0.499, so the extracted hero JPEG carries 10% of brand background plus the right edge of any wordmark and tagline. On the cover slide those fragments visibly bleed through the hero image as a floating dark rectangle mid-slide, and the logo's own background bakes into its PNG creating a visible rectangular frame around the wordmark on the brand panel.

Hard-coding the split fraction is brittle because every deck lays the panel differently: 42%, 45%, 50%, 55% are all common. Scan for the transition instead of guessing.

---

## Correct flow, scan, then crop

Use `scripts/crop_cover_assets.py` helpers:

```python
from crop_cover_assets import find_panel_edge, crop_hero_image, extract_alpha_logo

# 1. Find the left-panel, right-panel boundary empirically
edge = find_panel_edge('pages/page-01.png')
# returns an integer pixel x, the first column where average brightness
# jumps from panel-fill to page-paper

# 2. Crop the hero image starting just past the edge
crop_hero_image('pages/page-01.png', edge + 2, 'assets/cover-phones.jpg')

# 3. Extract the wordmark with alpha-clean on the panel color
extract_alpha_logo(
    'pages/page-01.png',
    bg_color=(17, 58, 84),              # sample from the panel first
    crop_bounds=(0.03, 0.28, 0.42, 0.60),
    out_path='assets/logo.png',
)
```

`find_panel_edge` samples every 20th row between x=0.30 and x=0.70 of the page, averages the brightness, and returns the first column where the row-average jumps by >=40 units. A stray dark phone pixel in one row doesn't fool it because the scan works on row-averaged brightness, not individual pixels.

---

## Sampling the panel background color

Before calling `extract_alpha_logo`, know the panel color. Sample page 1 corners:

```python
from PIL import Image
im = Image.open('pages/page-01.png').convert('RGB')
w, h = im.size
px = im.load()
for name, (x, y) in [
    ('top-left', (20, 20)),
    ('mid-left', (20, h//2)),
    ('bot-left', (20, h - 20)),
]:
    print(name, px[x, y])
```

All three should return the panel color if it's a solid fill. Use that tuple as `bg_color` in the alpha pass.

If the panel is a gradient, pixel-scanning won't give you a single color. In that case: take one corner sample, use a wider tolerance (60 to 80), and accept that near-gradient pixels will pass through as semi-transparent. Review the logo PNG visually after extraction.

---

## Alpha cleanup vs luminance threshold

`logo-extraction.md` describes the luminance-based alpha pass for white-on-white or light-gray logos. That approach FAILS when:

- The wordmark is **white** and the panel is **bright but colored**. Luminance threshold cannot separate "white glyph" from "bright colored fill" cleanly.
- The panel has **any dominant hue**, orange, red, navy, teal, brand-dark, the glyphs share luminance range with the panel fill.

The color-based pass (`extract_alpha_logo`) compares each pixel's euclidean distance in RGB from the sampled panel color. Pixels within tolerance, alpha=0. Pixels outside tolerance, preserve color, force alpha=255. Auto-bbox removes transparent margins left by the crop bounds.

Tolerance of 30 is a reasonable default. If the panel fill has subtle banding or JPEG compression halos, bump to 40 to 45. If the logo has deep shadows (rare on minimal cover marks), drop to 20 to 25 so the shadows don't get alpha'd out.

---

## After extraction, verify visually

Before embedding base64 in the HTML:

```python
# Render a preview combining the two on a mock panel
from PIL import Image
panel_color = (17, 58, 84)
phones = Image.open('assets/cover-phones.jpg')
logo = Image.open('assets/logo.png')

preview = Image.new('RGB', (1200, 500), panel_color)
lt = logo.copy(); lt.thumbnail((500, 150))
preview.paste(lt, (50, 100), lt)          # alpha paste
pt = phones.copy(); pt.thumbnail((600, 500))
preview.paste(pt, (600, 0))
preview.save('/tmp/preview.jpg', quality=85)
```

Read the preview with the Read tool and visually verify:
- No wordmark fragments in the right half
- No dark rectangle floating over the phones
- The logo edges are clean against the panel fill, no dark halo frame

If either check fails, re-run with different `bg_color` (try one pixel over from where you sampled) or a different crop bound. Cheap, deterministic, 15 seconds per iteration.

---

## When the source is NOT split-panel

Full-bleed photographic covers (anything with edge-to-edge imagery) don't need panel-edge detection. In that case:

- Extract the whole page as the hero
- If a wordmark is overlaid, extract it as a separate alpha PNG using `logo-extraction.md`'s luminance-threshold approach
- Skip this file

The decision tree: open page-01, ask "is there a vertical color boundary between the left-third-or-so and the right?" If yes, split-panel, use this file. If no, full-bleed, use `logo-extraction.md`.

---

## Display Compound Words

Editorial covers love compound display headlines: "Founder-Services", "Half-Time", "Self-Made", "Co-Founder." The U+002D hyphen carries the weight of those compounds, but in serif foundry faces (Cormorant Garamond, Playfair Display, Tiempos Headline, GT Sectra) the hyphen glyph sits roughly at the descender line, not the x-height center. At display sizes (80 to 140px) it reads as a low-floating dash rather than the intended em-rule-style separator, and the compound word breaks visually into two free-floating halves.

Browser fixes for vertical alignment are inconsistent. Safari, Chrome, and Firefox all snap baseline shifts slightly differently when applied to a single U+002D character mid-word; `vertical-align: 0.22em` on an inline `<span>` wrapping just the hyphen works in Chrome but jitters in Safari, and the surrounding letters reflow when the hyphen's box shifts.

The portable, pixel-perfect fix is to replace U+002D entirely with a custom span styled as a small `currentColor` rectangle.

### Recipe

```html
<h1 class="cb-display">Founder<span class="cb-dash" aria-hidden="true"></span>Services</h1>
```

```css
.cb-display {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 500;
  font-size: 124px;
  line-height: 0.95;
  color: var(--ink);
  letter-spacing: -0.01em;
}

.cb-dash {
  display: inline-block;
  width: 0.38em;            /* width relative to font-size, roughly 47px at 124px */
  height: 0.07em;           /* thickness roughly 8.7px at 124px, match font weight */
  background: currentColor;
  margin: 0 0.06em;         /* breathing room on both sides */
  vertical-align: 0.22em;   /* lift toward x-height center */
}

/* Optional: scale the dash for screen-reader output */
.cb-display .cb-dash::before {
  content: '\002D';         /* literal hyphen for screen readers (a11y) */
  position: absolute;
  width: 1px; height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}
```

The numeric tuning (`width: 0.38em`, `height: 0.07em`, `vertical-align: 0.22em`) was tested against Cormorant Garamond at 124px display weight. For other faces:

| Font family | width | height | vertical-align |
|---|---|---|---|
| Cormorant Garamond | 0.38em | 0.07em | 0.22em |
| Playfair Display | 0.34em | 0.08em | 0.20em |
| Tiempos Headline | 0.36em | 0.07em | 0.21em |
| GT Sectra | 0.40em | 0.06em | 0.24em |
| Lora | 0.32em | 0.08em | 0.18em |

Sans-serif faces (Inter, GT Walsheim, Nunito) usually render the hyphen near x-height center already and don't need this treatment. Only reach for the span when the source visually centers the hyphen and the default browser render is dropping it to the baseline.

### Accessibility

The literal hyphen lives in a visually-hidden `::before` so screen readers say "founder-dash-services" not "founder services." `aria-hidden="true"` on the span itself prevents the empty rectangle from being announced.

### When to use this

Phase 1 flags display headlines that contain a U+002D in serif faces >= 80px. The build script then auto-wraps the hyphen in the `cb-dash` span. For non-serif faces, or for body-sized text, leave U+002D unchanged.

---

## Curve Divider Extraction

Sales / services / founder-tier decks frequently use a soft curve divider between two content regions, a horizontal wave separating a photo-tinted hero from a card grid, a sloping diagonal between two text blocks, a U-shaped scoop at the bottom of a panel. The curves are usually drawn as bezier paths in PowerPoint (`p:sp` with a custom `a:custGeom`) and rasterized to PNG when the file is exported.

Two reasons to prefer the raster from `ppt/media/` over a CSS approximation:

1. **Source fidelity.** PowerPoint hand-tunes the bezier, control points, smoothing, asymmetric curves. CSS `border-radius` is two corner radii (or four for asymmetric corners); it cannot reproduce a hand-tuned bezier. Approximations are visibly different and read as "almost right but off."
2. **Round-trip survival.** When the PPTX was authored from a Figma export or a designer's vector source, the curve is intrinsic to the design system. The raster from `ppt/media/` IS that vector flattened at the export resolution; using it preserves the original intent.

### Recipe

When PPTX is available, the `extract_pptx_assets.py` JSON manifest lists every pic on every slide:

```json
{
  "slide": 6,
  "pics": [
    {
      "rId": "rId4",
      "image_path": "ppt/media/image27.png",
      "position_px": {"x": 0, "y": 690},
      "size_px": {"w": 1440, "h": 120},
      "role_hint": "curve-divider"
    }
  ]
}
```

Identify dividers by these heuristics:

- Width near full slide width (>=80% of `sldW_px`) AND height < 200px AND y position near top/bottom or between two content regions.
- Filename pattern (`image27.png`, `wave.png`, `divider.png` if the source named them).
- Aspect ratio >= 5:1 (wide-and-short).

In the build script, embed the divider as a `background-image` on the boundary div:

```css
.s-curve-divider {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 120px;
  background-image: url('data:image/png;base64,iVBORw0KGgo...');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  pointer-events: none;
}
```

For dividers that should tile horizontally (a repeating scallop), use `background-size: 240px 120px; background-repeat: repeat-x` and check the seam at the tile boundary.

### When PPTX is not available

Fall back to a CSS approximation, but ONLY after you've shown the user the approximation side-by-side with the source PDF and confirmed they accept the difference. The two patterns that get close enough on common dividers:

```css
/* Pattern A, gentle wave via two large border-radius pseudos */
.s-wave::before, .s-wave::after {
  content: ''; position: absolute; left: -10%; right: -10%;
  height: 120px;
}
.s-wave::before { top: 0; background: var(--surface); border-radius: 0 0 50% 50% / 0 0 120px 120px; }

/* Pattern B, SVG path inline for asymmetric curves */
.s-wave-svg {
  width: 100%; height: 120px;
  background: url('data:image/svg+xml,...') center/100% 100% no-repeat;
}
```

Both lose detail vs the raster. Use the raster when you can.

### Detection in Phase 1

If `extract_pptx_assets.py` finds pics matching the wide-and-short heuristic on slides between two content regions, flag them as `role_hint: curve-divider` in the manifest. The Phase 3 build script picks them up directly. If no PPTX is available but the source page shows a horizontal curve transition between content blocks, surface the divider to the user in the Phase 2 confirmation block: "Slide N has a curve divider, do you have the source PPTX? CSS-only approximation gets close but not exact."

---

## Full-Slide PNG Fallback

Some slides have complex visual compositions, curved-connector relationship diagrams, hub-and-spoke layouts, branching trees with custom illustrations, where HTML/SVG approximation doesn't converge after 2 build rounds. When the source PPTX includes a full-slide PNG render of that slide inside `ppt/media/`, use the PNG directly as the slide visual.

### When to reach for it

Heuristic: scan `ppt/media/` for PNGs > 500 KB. Most icon PNGs are 5 to 30 KB; a >500 KB PNG with dimensions near the slide canvas (e.g., 1920x1080 +/- 10%) is almost certainly a baked render of an entire slide. Cross-check by inspecting which slide's `_rels` file references it.

Alternative trigger: if the build script has spent >= 2 iterations on a complex relationship diagram and the user is still flagging visual divergence, fall back to the full-slide PNG.

### Crop the title and bottom-banner regions

The PNG bakes everything, title text, slide footer, the diagram itself. Title text in a raster doesn't scale cleanly to other languages or get edited in HTML; bottom banners interact awkwardly with the deck's nav chrome. Crop them out before embedding:

```python
from PIL import Image

src = Image.open('ppt/media/image46.png').convert('RGB')
w, h = src.size

# Sample title-strip and footer-strip heights from the source page.
# Typical values for a 1920x1080 render with a single-line title at top
# and a banner pill at bottom:
TITLE_STRIP_H = int(h * 0.13)   # crop top roughly 13%
FOOTER_STRIP_H = int(h * 0.08)  # crop bottom roughly 8%

middle = src.crop((0, TITLE_STRIP_H, w, h - FOOTER_STRIP_H))
middle.save('assets/slide-11-middle.jpg', 'JPEG', quality=85, optimize=True)
```

HTML then layers a normal `.slide-title` element above the cropped image (so the title is editable and consistent with the rest of the deck per gotcha #31), and a normal `.banner-pill` below it if the source had one.

### Match the slide CSS background to the cropped image's edges

The cropped image is unlikely to be edge-bleed-clean: its top row and bottom row will have specific colors (a pale green wash at the top fading to a lighter wash at the bottom, for instance). If the slide's CSS background is a different gradient, a visible seam appears at the image boundary.

Sample 5+ pixels from the bottom row of the cropped image and build a `linear-gradient(...)` from them as the slide background. See `references/palette-typography-detection.md` "Embedded-image background matching" for the sampling recipe.

### When NOT to use it

- Slides where HTML approximation works (most slides). Full-slide PNGs are a fallback for complex diagrams, not a default.
- Slides where the user has indicated they want to edit the text content. Once the visual is a raster, text edits require regenerating the PNG.
- Slides where any element on the diagram is interactive (live links, hover states). The raster can't be made interactive without overlaying transparent click regions, which is fragile.
