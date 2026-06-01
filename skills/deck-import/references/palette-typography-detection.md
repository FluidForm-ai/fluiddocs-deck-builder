# Palette + Typography Detection

The conversion's visual fidelity depends on getting two things right: the color palette and the typeface family. Both are detected from the source (PDF or PPTX), confirmed with the user, and then locked into the conversion brief.

---

## Palette detection

### Method (implemented in `scripts/detect_palette.py`)

1. **Sample each page image** at 200 DPI. For each page, reduce to a compact color histogram (down to 128 colors using `Pillow.Image.quantize(colors=128)`).
2. **Mask near-white and near-black pixels**, they dominate trivially and aren't the "brand" color. Threshold: RGB all >= 240 = near-white (excluded); RGB all <= 20 = near-black (kept separately as the likely "ink" color).
3. **Cluster the remaining pixels with k-means (k=5)** using `scikit-learn`. Alternative: `colorthief` for a simpler but less controllable implementation.
4. **Rank clusters by pixel count.** The top cluster is likely a background or dominant area color. The #2 cluster is usually the brand primary.
5. **Aggregate across pages**: take the union of each page's top-3 clusters, then re-cluster across pages (k=5 again). The resulting 5 colors are the deck-level palette.

### Palette role assignment

Once you have 5 candidate colors, assign them to the 6 brief roles:

| Brief role | Selection heuristic |
|---|---|
| Primary (brand accent) | The highest-chroma color that appears on >=3 pages. Fall back to the most frequent non-neutral color. |
| Surface (background) | The most frequent very-light or very-dark color. Usually a page-level background. |
| Ink (text) | If near-black was detected in Step 2, this is it. Otherwise, the darkest color in the palette. |
| Muted (secondary text, borders) | A mid-grey in the palette. If no mid-grey, use a desaturated variant of Ink (e.g., `color-mix(Ink, Surface, 40%)`). |
| Accent (optional) | The second-highest-chroma color, if materially different from Primary. Can be `null`. |
| Border/divider | 10 to 15% opacity of Ink, computed; not directly detected. |

### Edge cases

- **Source has a rainbow deck** (Canva, design-agency decks): palette will have many high-chroma colors. Take the most frequent one as Primary; flag others in the brief as "additional palette candidates" for user review.
- **Source is all black-and-white**: Primary defaults to `#0B1220` (near-black ink), Surface to `#FFFFFF`, Accent to `null`. Flag in confirmation: "I didn't detect a distinctive brand color, reply with your brand primary hex if you want one."
- **Source uses gradients heavily**: k-means will pick midpoints of gradients rather than endpoints. This is fine, a midpoint is usually a reasonable brand primary.
- **Source has a cover with a full-bleed photo**: don't let photo colors dominate. Exclude page 1 from cross-page aggregation if the cover is photo-heavy (detected via entropy > threshold on the page image).

### Palette confidence

- **High**: same Primary detected on >=60% of pages.
- **Medium**: Primary detected on 30 to 60% of pages.
- **Low**: Primary detected on <30% of pages (likely a photo-driven deck). Confirm with user.

Surface confidence in the confirmation block when medium or low.

---

## Typography detection

### Method

1. **Pull font metadata from `pdfplumber`** (PDF path) or `python-pptx` (PPTX-only path): for each slide, iterate text runs and collect unique fontname values.
2. **Normalize** by stripping subset prefixes (`ABCDEF+Inter-Regular`, `Inter-Regular`), stripping weight/style suffixes (`Inter-Bold`, `Inter`), and deduplicating.
3. **Aggregate across slides**: rank by frequency. Top 1 to 3 font families are the deck's typography.
4. **Map to web-safe equivalents** using the stand-in table below.

### Font stand-in table

Many decks use foundry fonts that aren't available on Google Fonts. Map to the closest free equivalent.

| Detected family | Google Font stand-in | Display notes |
|---|---|---|
| Inter | Inter | Direct match |
| SF Pro, SF Pro Display, San Francisco | Inter | Closest free equivalent |
| Helvetica, Helvetica Neue | Inter (for display), Arial (for body fallback) | |
| Arial | Inter | Arial is a system font, but Inter renders more consistently cross-browser |
| Roboto | Roboto | Direct match |
| Open Sans | Open Sans | Direct match |
| Poppins | Poppins | Direct match |
| Montserrat | Montserrat | Direct match |
| Tiempos Headline, Tiempos Text | Playfair Display (serif headline) or Lora (serif body) | Closest serif family |
| GT Walsheim, GT America | DM Sans | Geometric sans |
| Avenir, Avenir Next | Nunito Sans | Humanist sans |
| Futura | Jost | Geometric sans |
| Gotham | Montserrat | |
| Proxima Nova | Nunito Sans or Mulish | |
| Source Sans Pro | Source Sans 3 | Direct match |
| Georgia | Lora | Serif |
| Times, Times New Roman | Playfair Display (display), Lora (body) | Serif |
| Merriweather | Merriweather | Direct match |
| Courier, Courier New | JetBrains Mono, IBM Plex Mono | Monospace |
| Monaco, Consolas, Menlo | JetBrains Mono | Monospace |
| IBM Plex Sans, IBM Plex Mono, IBM Plex Serif | IBM Plex (direct) | Direct match |
| Circular, Circular Std | Poppins or DM Sans | Geometric sans |
| Neue Haas Grotesk | Inter | |
| Aktiv Grotesk | Work Sans | |

### Scale extraction

Inspect character sizes (via pdfplumber or python-pptx) to guess the deck's typographic scale. Collect all sizes, bucket them into clusters (tolerance +/-1pt), and take the top 5 to 7 cluster centers as candidate font-size values.

Convert points to CSS pixels (1pt is roughly 1.33px) and round to common values:
- 10pt, 13px (small caption / meta)
- 11pt, 15px (body)
- 14pt, 19px (card title / subhead)
- 18pt, 24px (h3)
- 24pt, 32px (h2)
- 36pt, 48px (hero stat / cover)

These become the typographic scale declared in the conversion brief. Every CSS `font-size` in the output must match one of them.

### Typography confidence

- **High**: the top font family appears on >=60% of pages.
- **Medium**: 30 to 60%.
- **Low**: <30%.

Low typography confidence usually means the deck is heavy on imagery (little extracted text) or uses many decorative fonts. In both cases, fall back to a sensible default, Inter for sans, Lora for serif, and flag in the confirmation block.

---

## Output format

The confirmation block and conversion brief receive a structured result:

```json
{
  "palette": {
    "primary": "#F97316",
    "surface": "#FFFFFF",
    "ink": "#0B1220",
    "muted": "#64748B",
    "accent": null,
    "border": "color-mix(in oklab, #0B1220 15%, transparent)",
    "confidence": "high",
    "additional_candidates": []
  },
  "typography": {
    "display_detected": "Tiempos Headline",
    "display_web": "Playfair Display",
    "body_detected": "Inter",
    "body_web": "Inter",
    "mono_detected": null,
    "mono_web": null,
    "scale_px": [13, 15, 19, 24, 32, 48],
    "confidence": "high"
  }
}
```

The confirmation block presents this in compact, user-readable form (see `confirmation-block-template.md`). The conversion brief stores this exact JSON.

---

## What NOT to do

- **Don't guess a brand's official color from the company name.** Even if the source is from a company with a well-known brand color (e.g., Airbnb's Rausch), the conversion should mirror the source's actual sampled palette. If the source was black-and-white-printed, the conversion should be black-and-white. Branding is the user's decision, not the skill's.
- **Don't re-source fonts from the web.** If the source used a paid foundry font the user doesn't own the web license for, the stand-in is the correct output, not an attempted fetch.
- **Don't average colors across pages to "smooth" the palette.** That produces muddy mid-grey. Cluster, don't average.

---

## Gradient Extraction (PPTX path)

When PPTX is the primary source, gradients live in `a:gradFill` blocks inside `p:spPr` (shape backgrounds), `p:bg/p:bgPr` (slide backgrounds), or `a:lnFill` (stroke fills). Read them directly rather than approximate from the rasterized PDF page.

### Reading `a:gradFill`

A typical gradient block looks like:

```xml
<a:gradFill rotWithShape="1">
  <a:gsLst>
    <a:gs pos="0">
      <a:srgbClr val="0B2147"/>
    </a:gs>
    <a:gs pos="100000">
      <a:srgbClr val="1B3A6B"/>
    </a:gs>
  </a:gsLst>
  <a:lin ang="18900044" scaled="0"/>
</a:gradFill>
```

Per stop:
- `pos="0"` through `pos="100000"`, position along the gradient axis, in 1000ths of a percent. Divide by 1000 to get a CSS percentage.
- `a:srgbClr val="..."`, explicit hex (6 digits, no `#`).
- `a:schemeClr val="accent1"`, theme color reference; resolve via `ppt/theme/theme1.xml` `a:clrScheme`. If unresolved, fall back to a sampled pixel from the rendered PDF page.

Per axis:
- `a:lin ang="<emu_angle>"`, linear gradient. `ang` is in **60000ths of a degree, PPT compass convention** (clockwise from north / "up"). Divide by 60000 to get degrees.
- `a:path path="circle|rect|shape"`, radial / shape-relative gradient. CSS equivalent is `radial-gradient(...)`; map per shape geometry.

### EMU-angle to CSS conversion

PPT and CSS both measure clockwise but anchor differently. PPT 0deg points "up" (north). CSS `linear-gradient(0deg, ...)` also paints upward, but its 0deg is the OUTGOING direction (so the first stop is at the bottom). They look like the same convention until you test 45deg and find the gradient running the wrong direction.

Helper:

```python
def ppt_angle_to_css(emu_angle):
    """Convert PPT a:lin@ang (EMU, 60000ths of a degree) to CSS linear-gradient deg.
    Returns (css_deg, reverse_stops_flag). reverse_stops=True means feed the gradient
    stops in reverse order (CSS will still render the same direction, but the stop
    order needs flipping)."""
    deg = (emu_angle / 60000) % 360       # PPT degrees, 0=north, clockwise
    # PPT: 0=up, 90=right, 180=down, 270=left
    # CSS linear-gradient: 0=to top (so 0 = paint upward, color stop 0 is at bottom)
    # Same compass orientation, but PPT puts stop 0 at the start of the axis (the
    # direction the arrow points FROM); CSS puts stop 0 at the start of the gradient
    # line (where the gradient begins, opposite of the angle's "to" direction).
    # Net: rotate by 180 to align gradient line direction.
    css_deg = (deg + 180) % 360
    return css_deg, False                  # default, flip stops if visual check fails
```

Reference table for common angles:

| PPT `ang` (EMU) | PPT degrees | CSS `linear-gradient` deg | Equivalent (stops reversed) |
|---:|---:|---:|---|
| 0 | 0deg (up) | 180deg | 0deg (reverse stops) |
| 5400000 | 90deg (right) | 270deg | 90deg (reverse stops) |
| 10800000 | 180deg (down) | 0deg | 180deg (reverse stops) |
| 16200000 | 270deg (left) | 90deg | 270deg (reverse stops) |
| 2700000 | 45deg (up-right) | 225deg | 45deg (reverse stops) |
| 18900044 | 315deg (up-left) | 135deg | 315deg (reverse stops) |

Either column produces the same visual; pick whichever reads cleaner in the CSS. After conversion, **render side-by-side against the source page** and verify the gradient flows in the same direction, every once in a while a theme variant flips the relation and the stops need to be reversed.

### Diagonal angles

PPT diagonals (45deg, 135deg, 225deg, 315deg) need extra care because CSS does its own thing at the corner. Use the explicit degree form (`linear-gradient(135deg, ...)`) rather than the keyword form (`to bottom right`), the keyword treats the box aspect ratio differently and the gradient line ends up off-axis on non-square targets.

---

## Background Composition

Every slide background is one of two types, and the distinction is the difference between a slide that feels native and one that feels flat.

### flat-gradient (the simple case)

The slide background is a pure CSS gradient with no underlying photo or texture. Source has only `a:gradFill` in `p:bg/p:bgPr` (or no `p:bg` at all, in which case the master slide's gradient applies). CSS:

```css
.slide.s-gradient-only {
  background-image: linear-gradient(135deg, #0B2147 0%, #1B3A6B 100%);
}
```

Do NOT include `background-blend-mode`, there's nothing to blend.

### photo-tint (the editorial case)

The slide background is a photograph (night sky, mountains, milky way, cityscape, hands-on-keyboard, etc.) overlaid with a colored gradient via PowerPoint's blend semantics. The texture of the photo is meant to read through the tint, stars, peak silhouettes, glint on the keyboard are visible THROUGH the navy/burgundy/forest gradient. Source has BOTH a `p:bg/p:bgPr/a:blipFill` (the photo, referenced by `r:embed` to a `ppt/media/` PNG/JPG) AND a gradient layer.

CSS recipe (the only correct render):

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

Two `background-blend-mode` values are required, one per `background-image` layer in stacking order:
- First value (`multiply`) blends the gradient layer with what's below it (the photo).
- Second value (`normal`) is how the photo composes with the slide background, usually no blend.

Order matters. Listing them as `normal, multiply` flips which layer multiplies and produces a wash instead of a tinted photo.

### Detection (PPTX path)

```python
# Inside extract_pptx_assets.py
blip = bg_pr.find('.//a:blipFill', NSMAP)
grad = bg_pr.find('.//a:gradFill', NSMAP)
if blip is not None:
    bg_type = 'photo-tint'   # photo + (typically) a gradient overlay
elif grad is not None:
    bg_type = 'flat-gradient'
else:
    bg_type = 'solid'        # a:solidFill or master inherit
```

When `bg_type = 'photo-tint'`, extract BOTH the photo (via the `r:embed` rId, `ppt/media/<file>`) AND the gradient color stops + angle. The build script needs both. Save the image alongside other slide assets and reference by data URI or relative path.

### Detection (PDF fallback)

When PPTX isn't available, classify from the rendered PDF page:

```python
import numpy as np
from PIL import Image

def classify_bg(page_png_path, edge_inset=80):
    img = np.array(Image.open(page_png_path).convert('RGB'))
    h, w = img.shape[:2]
    # Sample the four background strips (top, bottom, left, right inset from edges)
    samples = np.concatenate([
        img[10:edge_inset, :, :].reshape(-1, 3),
        img[-edge_inset:-10, :, :].reshape(-1, 3),
        img[:, 10:edge_inset, :].reshape(-1, 3),
        img[:, -edge_inset:-10, :].reshape(-1, 3),
    ])
    # Entropy proxy: stddev across samples. Pure gradient, low (<25 per channel).
    # Photo+tint, high (>40 typical) because the texture survives the multiply.
    sd = samples.std(axis=0).mean()
    return 'photo-tint' if sd > 35 else 'flat-gradient'
```

Surface the classification in the Phase 2 confirmation block when the inferred type is `photo-tint` so the user can correct if the heuristic missed.

### Verification

Before approving the build, render the HTML slide and the source page at the same width and read both PNGs side-by-side at 200% in a viewer. Two things to verify:

1. **Color tint matches**: sample one pixel from the same screen position on each render, RGB values should be within +/-5 per channel.
2. **Texture survives**: pick a recognizable feature in the photo (a star, a peak silhouette, the glint on a glass), it should be visible in the HTML render too. If the texture is gone, the multiply isn't kicking in, usually because the gradient layer is fully opaque (drop alpha to 0.55 to 0.95 range) or the `background-blend-mode` order is wrong.

---

## Background Gradient Sampling

Slide backgrounds are sampled from the source rendered pages, NOT guessed. Guessing produces a flatter-than-source visual that user feedback catches as "the background gradient almost isn't coming through." Sampling lands within +/-5 RGB of source, every time.

### Recipe

Sample 5+ pixels per corner of `pages/page-1.png` (the cover), plus 2 to 3 pixels per corner of two content slides for cross-page validation:

```python
from PIL import Image

def sample_bg_corners(page_png_path, inset=10, sample_size=12):
    """Return RGB samples from each corner of the page image.
    inset: how far from the edge to sample (avoid the absolute edge).
    sample_size: how many pixels in each direction to average."""
    im = Image.open(page_png_path).convert('RGB')
    w, h = im.size
    s = sample_size
    return {
        'top_left':    tuple(int(c) for c in im.crop((inset, inset, inset+s, inset+s)).resize((1,1)).getpixel((0,0))),
        'top_right':   tuple(int(c) for c in im.crop((w-inset-s, inset, w-inset, inset+s)).resize((1,1)).getpixel((0,0))),
        'bottom_left': tuple(int(c) for c in im.crop((inset, h-inset-s, inset+s, h-inset)).resize((1,1)).getpixel((0,0))),
        'bottom_right':tuple(int(c) for c in im.crop((w-inset-s, h-inset-s, w-inset, h-inset)).resize((1,1)).getpixel((0,0))),
    }
```

### Build the angle from the dominant tone direction

Compare the four corner samples to figure out which way the gradient flows:

- Lighter on the right than the left, left-to-right wash, CSS `linear-gradient(90deg, ...)` or `(118deg, ...)` for a tilted wash.
- Lighter on the bottom than the top, top-to-bottom wash, `(180deg, ...)`.
- Lighter at one corner than the diagonal corner, diagonal wash, `(135deg, ...)` or `(45deg, ...)`.

Compute a lightness metric per corner (`L = 0.299*R + 0.587*G + 0.114*B`), then pick the angle that aligns with the steepest L-gradient axis.

### Build the stops from the sampled values

Place the corner samples at the gradient's start, midpoints, and end. Example:

```css
.slide {
  background: linear-gradient(
    118deg,
    #D7ECE0 0%,      /* top-left */
    #E9F4DC 30%,     /* upper-mid wash */
    #FBFFE8 65%,     /* warm middle */
    #F2FAD9 100%     /* bottom-right */
  );
}
```

Generally 3 to 5 stops is plenty; more than 5 produces visible banding from the LCD's color resolution.

### Validate

Render the slide at the same width as `pages/page-1.png`. Pixel-sample the same screen positions on both. RGB delta per channel should be <= 5. If any channel is off by >= 10, the angle is wrong (try +/-30deg from current) or one of the stops needs nudging (often the middle stop drifts away from sampled value during CSS interpretation).

---

## Embedded-Image Background Matching

When a slide uses a baked image (per `cover-asset-extraction.md` "Full-Slide PNG Fallback") layered with HTML text elements, the underlying CSS background must match the image's edge colors. Otherwise the image's bottom row blends to one color while the surrounding CSS background is a different color, producing a visible horizontal seam right at the image boundary.

### Sample the image's edges

```python
from PIL import Image

def sample_image_edge(img_path, edge='bottom', sample_count=5):
    """Sample N evenly-spaced pixels from one edge of the image.
    edge: 'top', 'bottom', 'left', 'right'."""
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    pixels = []
    for i in range(sample_count):
        if edge == 'bottom':
            x = int((i + 0.5) / sample_count * w)
            y = h - 5
        elif edge == 'top':
            x = int((i + 0.5) / sample_count * w)
            y = 5
        elif edge == 'left':
            x = 5
            y = int((i + 0.5) / sample_count * h)
        else:  # 'right'
            x = w - 5
            y = int((i + 0.5) / sample_count * h)
        pixels.append(tuple(int(c) for c in im.getpixel((x, y))))
    return pixels
```

### Build a matching CSS gradient

For a slide where the image sits at the top and HTML banner sits below, sample the image's BOTTOM edge and build a horizontal gradient that picks up where the image leaves off:

```python
edges = sample_image_edge('assets/slide-11-middle.jpg', edge='bottom', sample_count=5)
# Use the leftmost, middle, and rightmost samples for a 3-stop gradient
left = '#{:02X}{:02X}{:02X}'.format(*edges[0])
mid  = '#{:02X}{:02X}{:02X}'.format(*edges[2])
right= '#{:02X}{:02X}{:02X}'.format(*edges[4])

slide_bg = f'linear-gradient(90deg, {left}, {mid}, {right})'
```

Apply ONLY to the slide that uses the baked image, other slides keep the deck's default sampled background.

### Why this matters

The eye is extremely good at spotting horizontal seams between near-similar colors. A 5-RGB difference between the image's bottom row and the slide CSS background reads as a visible line; 10-RGB difference reads as a hard seam. Sampling, not guessing, is the only way to make the boundary invisible.
