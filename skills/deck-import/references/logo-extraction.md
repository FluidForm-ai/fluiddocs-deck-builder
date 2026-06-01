# Logo & Brand Typography Extraction

When the source deck contains a **custom wordmark or logo** that isn't a standard font, do NOT try to recreate it in CSS text or hand-craft an SVG path. Extract it as a raster from the source and embed base64.

This is a narrow exception to the "photos only" raster rule in SKILL.md. The rule exists because text-based wordmarks drift visually from any source's custom compressed sans-serif when kerning, weight, or non-standard glyphs (pipes, ligatures) are involved, and no CSS-only approach is going to match without custom font files we don't have.

---

## When extraction is warranted

Extract as raster if any of these hold:

- **Custom typography**, the letterforms aren't available as a web-safe or Google Font (e.g., a compressed condensed sans-serif).
- **Ligatures or compound marks**, pipes, bars, dots, or unusual inter-letter glyphs that aren't easy to recreate.
- **Color gradient or stroke effects**, the wordmark has a gradient fill, inner stroke, or two-tone color that's painful to CSS.
- **User explicitly requests it**, "just keep the logo as an image" is always valid.

When extraction is NOT warranted:
- Standard font (Inter, Helvetica, etc.) with plain black text, use `<text>` or HTML text with the detected font.
- Cover-only logo that won't repeat, fine, extract it once.
- Wordmark repeats on every slide, **also fine to extract once** and reference the base64 from a shared `LOGO_IMG` constant. Don't embed the base64 string 22 times.

---

## Extraction procedure

### 1. Locate the logo in the source

Use page 1 (cover) from `pages/page-01.png`. Open in PIL:

```python
from PIL import Image
img = Image.open('pages/page-01.png')
print(img.size)  # e.g., (2880, 1620)
```

Pinpoint the logo coordinates by opening the PNG and clicking or by overlaying a grid.

### 2. Crop + alpha-process

```python
crop = img.crop((336, 730, 1140, 930)).convert('RGBA')
import numpy as np
arr = np.array(crop)
# Treat luminance > 240 as background, full alpha transparency
lum = arr[...,:3].mean(axis=-1)
arr[..., 3] = np.where(lum > 240, 0, 255)
Image.fromarray(arr).save('assets/logo_alpha.png')
```

The luminance threshold depends on the source background. Sample it first, if the source has a cream background (#F9F5EF), 240 is too aggressive; use 230. If it's pure white, 248 is fine.

### 3. Embed base64 in build_html.py

```python
import base64, os
def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

LOGO_IMG = f"data:image/png;base64,{b64('assets/logo_alpha.png')}"

def wordmark(cls=''):
    return f'<img class="wordmark-img {cls}" src="{LOGO_IMG}" alt="Brand Name" />'
```

### 4. Size responsibly with CSS

```css
.wordmark-img {
  display: inline-block;
  height: auto;
  object-fit: contain;
}
.wordmark-img.wm-xl { width: 280px; }   /* cover slide */
.wordmark-img.wm-lg { width: 180px; }   /* feature headers */
.wordmark-img.wm-stack { width: 140px; } /* slide eyebrow */
```

Never rely on the source PNG's intrinsic pixel dimensions, always declare CSS width or height so the layout is deterministic.

### 5. Watch the file-size budget

A 804x200 alpha PNG is roughly 15KB. Acceptable. If your extraction comes in at 50KB+, you're cropping too wide or saving at too-high resolution. Keep the logo at 2x the largest displayed size (e.g., 560px wide for a 280px display size).

Conversion SKILL.md caps file size at 2.5 MB total. Budget roughly 30KB for the logo, leaving the rest for CSS and any founder photos.

---

## Anti-pattern: hand-crafted SVG paths

Do not try to recreate a custom wordmark with `<path d="M...">` unless the source ships the actual paths (rare). Hand-crafted paths always:

- Miss kerning nuances.
- Approximate but don't match stroke weights.
- Break when the designer updates the brand.

The extract-and-embed path is the shortest route to visual fidelity. Invest five minutes in a clean crop and an alpha pass, not an hour in path math.

---

## Edge case: monochrome wordmarks on colored backgrounds

If the source cover has a white wordmark on a dark background, the luminance-threshold approach above DOES NOT work. Luminance separates bright from dark, and here both glyph and background are bright-ish (a white glyph on a saturated navy or teal panel, both colors have meaningful brightness, and inverting the threshold catches too many glyph pixels or too few background pixels depending on where you tune it).

Switch to **color-distance** alpha cleanup: sample the panel fill color from the source, then mark any pixel within euclidean RGB distance `D` of the panel color as transparent. This cleanly separates the glyph from the background regardless of how bright either one is.

```python
from PIL import Image
page = Image.open('pages/page-01.png').convert('RGBA')
w, h = page.size
# Sample the panel color by eye or via a corner pixel inside the left panel
BG = (17, 58, 84)  # navy

crop = page.crop((int(w*0.03), int(h*0.28), int(w*0.42), int(h*0.60)))
px = crop.load()
cw, ch = crop.size
TOL = 30  # euclidean RGB distance
for y in range(ch):
    for x in range(cw):
        r, g, b, a = px[x, y]
        d = ((r-BG[0])**2 + (g-BG[1])**2 + (b-BG[2])**2) ** 0.5
        px[x, y] = (0, 0, 0, 0) if d < TOL else (r, g, b, 255)

# Auto-bbox removes transparent margins from the crop-rect overshoot
bbox = crop.getbbox()
if bbox:
    crop = crop.crop(bbox)
crop.save('assets/logo.png', 'PNG', optimize=True)
```

**Tolerance guidance**:
- `30`, default, works for clean solid panels (navy, purple at most angles)
- `40 to 45`, bump when the panel has subtle banding, gradient steps, or JPEG compression halos
- `20 to 25`, drop when the logo itself has meaningful dark shadows you want to preserve

After cleanup, inspect the PNG visually. If the logo still has a visible rectangular frame when placed back on the panel, the tolerance was too low and background pixels leaked through. If the glyph edges look gnawed, the tolerance was too high and anti-aliased glyph pixels got alpha'd out, drop by 5 to 10 and retry.

The full agent-callable version of this routine lives in `scripts/crop_cover_assets.py::extract_alpha_logo`. Prefer that over inlining the loop, it handles auto-bbox, fractional vs pixel bounds, and safe defaults.

**Why luminance-thresholded output looks broken on colored panels**:
If you ran `np.where(lum > 240, 0, 255)` on a navy panel, the navy background (brightness roughly 53) stayed fully opaque because it's dark, so the PNG saved as RGBA but every single pixel had alpha=255. When the PNG was placed back on the navy panel in the HTML, users saw a rectangular "frame" of navy around the white wordmark. `np.where(lum < 15, 0, 255)` inverts to catch dark panel pixels, but then any shadow or deep-saturation pixel inside the glyph also goes transparent, producing gnawed edges. Color-distance doesn't have either failure mode.

If in doubt, ask the user for a source logo file, most founders have the raw SVG in a brand folder somewhere.

**For full split-panel covers** (logo + hero on one slide), see `cover-asset-extraction.md` for the panel-edge pixel-scan approach that pairs with this alpha-cleanup.

---

## Hero / reveal slides, re-extract at higher resolution

A corner-eyebrow logo and a full-canvas reveal logo have very different quality bars. The default extraction procedure above is tuned for the former (<=280px displayed width, roughly 15KB PNG). Reuse that asset on a reveal slide, where the logo might render at 800 to 1100px, and it looks pixelated or "made up" even though the geometry is correct.

**When to trigger the hero-quality path**:
- The slide's role is `brand_reveal`, a ceremonial mark moment, or similar.
- The logo occupies >=40% of the canvas width in the source.
- The user says anything like "the logo looks off" or "it feels made up" after review.

**Procedure**, keep the alpha/color-distance cleanup from above, but change two things:

1. **Mask the central region only**, to exclude any framing elements (amber/teal side rails, gradient panels, decorative borders) that a luminance or color-distance threshold would otherwise preserve as opaque pixels:

   ```python
   import numpy as np
   from PIL import Image
   src = Image.open('pages/page-17.png').convert('RGB')
   arr = np.array(src)
   h, w = arr.shape[:2]
   # Skip the outer 25 to 30% on each side, tune to where the rails end
   region = arr[:, int(w*0.28):int(w*0.72)]
   mask = ~((region[:,:,0] > 245) & (region[:,:,1] > 245) & (region[:,:,2] > 245))
   ys, xs = np.where(mask)
   top, bottom = ys.min(), ys.max()
   left, right = xs.min(), xs.max()
   crop = Image.fromarray(region[top:bottom+1, left:right+1])
   ```

2. **Upscale 1.5x with Lanczos** before saving, so the asset carries real detail when the CSS scales it up to reveal dimensions:

   ```python
   crop = crop.resize((int(crop.width * 1.5), int(crop.height * 1.5)), Image.LANCZOS)
   crop.save('assets/logo-hires.png', 'PNG', optimize=True)
   ```

**File-size exception**: hero-quality logos land around 80 to 100 KB, not the 15 to 30 KB corner-logo budget. That's expected, reveal slides justify the bytes. If you're over 150 KB, re-mask to a tighter bounding box.
