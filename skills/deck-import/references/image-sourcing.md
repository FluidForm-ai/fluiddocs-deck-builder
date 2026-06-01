# Image Sourcing, When and How to Replace Source Photos

The extractor pulls all imagery from the source deck. Often that's fine. Sometimes the source photos are AI-rendered stock that doesn't ship-quality, and the user wants real photography. This reference documents the workflow under sandbox constraints.

## The inline-pasted-image trap

**This is the #1 time-waster in conversion runs.** When the user pastes an image into chat ("here's the radar"), the model SEES the image but the filesystem does NOT have it. Any attempt to recreate it (SVG, matplotlib) will never be pixel-exact, no matter how many rounds you iterate.

**Default response on first ask**, whenever the user offers an image:

> "I can see what you pasted but I can't access it as a file. Two ways to give me the actual file:
> 1. Drag the file directly into chat (creates a real upload)
> 2. Save it to a known path (e.g., `<workspace>/img/<filename>`) and tell me the filename
>
> Either works. Don't proceed with anything image-related until the file exists on disk."

Send this BEFORE attempting any recreation. The user thinks they've already given you the image. Set the expectation up front; save 4 to 5 iteration rounds.

## When to offer the image swap

Phase 1 should classify each extracted image:

- **photographic-real**, actual product photo, founder portrait, real-world scene, keep
- **ai-stylized**, Canva/Midjourney/DALL-E rendered art (cinematic colored lighting, exaggerated bokeh, vague brand details), flag for swap offer
- **illustration**, hand-drawn or vector illustration, keep unless explicitly bad
- **chart**, graph/data visualization, keep (or rebuild as native HTML/SVG per the rest of the skill)

Detection heuristics for `ai-stylized`:
- Saturation > 0.6 across the entire image (real photos have variation)
- Bokeh circles that are perfectly round and identical sized
- Subject is centered with dramatic radial light
- No identifiable brand/product detail (no readable text, generic shapes)
- Image is the same composition repeated across multiple slides

If any image is flagged `ai-stylized`, add this line to the Phase 2 confirmation block:

> ```
> Source uses AI-rendered art for N images (slides X, Y, Z).
> Reply "swap photos" to surface real-photo alternatives during the build.
> Reply "keep" to use the source images as-is.
> ```

The default (no reply) is KEEP. Don't auto-swap without consent, some decks intentionally use stylized imagery.

## How to source replacement photos

### Path A, Unsplash via comparison page (preferred)

Unsplash is free for commercial use, no attribution required. Build a comparison HTML page that loads images directly from `images.unsplash.com` CDN, present 4 to 6 candidates per slot, let the user pick.

**Workflow**:

1. `WebSearch` for the subject + "unsplash", gather 4 to 6 specific photo IDs (e.g., `photo-1461023058943-07fcbe16d735`)
2. Build a comparison page at `<workspace>/<Brand>-Image-Options.html` with `<img src="https://images.unsplash.com/photo-XXX?w=900&h=1200&q=80&fit=crop">` tags
3. Page should include: thumbnails of each candidate, a label, a short description ("warm tones, cinematic", "minimalist lifestyle"), and the photo ID
4. Tell the user: "Reply with the IDs you want (e.g., `cb_b` and `es_a`)"
5. After user picks, tell them: "Right-click each image in the options page, Save Image As, save to `<workspace>/img/<filename>.jpg`"

**Why this works**: the user's browser loads images directly from the Unsplash CDN. The model never has to download anything. The user's right-click, save puts the file in the img folder where the file tools can pick it up.

### Path B, User pastes CDN URL in message

If the user is comfortable in chat:

1. Tell them: "Paste the direct Unsplash CDN URL (e.g., `https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=2400&q=90`) in your next message."
2. Once the URL is in the user message, `web_fetch` will accept it (URL is now in provenance)
3. Download via `web_fetch`, save to disk, process

### Path C, User uploads their own photos

If the user has Midjourney renders, brand photography, or any other source:
- They drag the files into chat, they land in the uploads folder
- Move/copy to a known workspace path (`<workspace>/img/<canonical_filename>.jpg`)
- Continue

## What doesn't work (and why)

- **`curl`, `wget`, `lynx`** in bash, blocked by sandbox network policy. Will silently return "Exit code 2" with no content.
- **Python `urllib`, `requests`, `httpx`, `aiohttp`**, same network block. Don't try these as a fallback.
- **`web_fetch` on arbitrary CDN URLs**, provenance check rejects any URL not previously seen in a user message or a prior `web_fetch` result.
- **Generating images**, the model can't generate new images directly. Don't promise this.

## After file is on disk

Standard processing for replacement photos:

```python
from PIL import Image

# Crop to standard 3:4 portrait (or 4:3 landscape, match the slot)
def to_aspect(img, tw, th):
    sw, sh = img.size
    tar, sar = tw/th, sw/sh
    if sar > tar:
        new_w = int(sh * tar)
        l = (sw - new_w) // 2
        return img.crop((l, 0, l + new_w, sh)).resize((tw, th), Image.LANCZOS)
    else:
        new_h = int(sw / tar)
        t = (sh - new_h) // 2
        return img.crop((0, t, sw, t + new_h)).resize((tw, th), Image.LANCZOS)
```

Save with:
- Close-up portrait slots: 720x960 @ q=92
- Background photos: 800x1000 @ q=92
- Product thumbnails: 300x300 square @ q=88 (subject tightened to roughly 80% frame fill)

Then sync to the build folder if the deck has a co-located img directory.

## Tight crop on subject (when user says "zoom in on the glass")

Pixel-bounds approach (single row + single column scan) is unreliable when the source image has bokeh blur or gradient backgrounds.

Better: prompt the user for the rough region (e.g., "left 55% of image, vertical center"), use proportional coordinates:

```python
cw, ch = img.size
x1 = int(cw * 0.02)   # tight left
x2 = int(cw * 0.55)   # crop out the bokeh right half
y1 = int(ch * 0.20)   # leave breathing room above
y2 = int(ch * 0.96)   # leave breathing room below
tight = img.crop((x1, y1, x2, y2))
```

Then run through `to_aspect` to normalize to the target slot ratio.

**Watch the to_aspect math**: if `to_aspect(720, 960)` (3:4) gets a 477x912 source (ratio 0.52, much taller than 3:4), it will crop the TOP and BOTTOM aggressively. To preserve a full glass top-to-bottom, widen the source crop (include more bokeh background on the right) so the source ratio is closer to 3:4 before to_aspect runs.

## Quality bar for replacement photos

- Subject occupies >= 60% of the visible frame after final crop
- No baked-in product packaging text that conflicts with the brand
- Lighting matches the deck's palette mood (warm cream deck, warm-toned photos)
- Aspect ratio at source is >= 3:4 (taller is fine, wider works but wastes pixels in to_aspect)
- File size after processing: 60 to 120 KB at 720x960 JPEG q=92

If a candidate fails any of these, drop it from the comparison page.

---

## Alpha Detection, Pre-Cut RGBA with a Semi-Transparent Subject

Some user-supplied headshots and icons arrive already alpha-cut, but with the subject body rendered at a partial alpha (e.g., `alpha=197` across the face/body) and a soft fade band at the edges (`alpha=10 to 80`). This is common when:

- The user ran the original through PowerPoint's "remove background" tool, which leaves a soft halo.
- The image came out of Canva's bg-removal, which keeps fine hair / fur detail by feathering alpha rather than hard-masking.
- It's a vector export from Figma with translucent fills that flattened to a partial alpha when rasterized.

Treating these as "needs bg removal" with a color-distance pass is the wrong move, the soft fade band reads as "background-like" to color-distance heuristics and gets erased, producing a hard-edged silhouette that floats badly against any non-matching background. The right move is to detect the existing alpha range BEFORE any color-based removal runs, and if the input is pre-cut, just boost the subject's alpha to 255 while preserving the fade band.

### Detect before removing

```python
from PIL import Image
import numpy as np

def needs_color_removal(img_path):
    """Return True only if the image is RGB or solid-alpha RGBA (i.e., the bg
    has not already been cut out). Pre-cut RGBA images return False and should
    be handled by boost_alpha.py, not by color-distance removal."""
    im = Image.open(img_path)
    if im.mode == 'RGB':
        return True
    if im.mode == 'RGBA':
        a = np.array(im)[..., 3]
        # Solid alpha (every pixel 255) = source has no transparency yet
        if a.min() == 255:
            return True
        # Already alpha-cut (range < 255) = pre-cut, don't run color removal
        return False
    # Other modes (P, L, LA): convert to RGBA and re-check
    return needs_color_removal(img_path)  # after re-saving as RGBA
```

### Boost the subject alpha; preserve the fade band

When the input is pre-cut RGBA, use `scripts/boost_alpha.py`:

```bash
python scripts/boost_alpha.py path/to/arjun.png --threshold 30 --out path/to/arjun-boosted.png
```

The script reads the alpha channel, finds every pixel with `alpha > threshold` (default 30), and writes those pixels back at `alpha = 255`. Pixels with `alpha <= threshold` (the soft fade band) are left untouched. Result: the subject body renders fully opaque, the edges keep their soft falloff, the headshot reads clean on any background without losing the natural feathering.

### When to use which threshold

- **`--threshold 30`** (default): aggressive solidification, keeps only the very softest 12% of the alpha range as a halo. Use for headshots where the subject should read crisp against a saturated panel.
- **`--threshold 60`**: gentler, keeps a wider halo. Use when the original feathering is intended (e.g., a "fading into the background" portrait).
- **`--threshold 10`**: barely modifies anything; use only when you want to clean up rounding noise (alpha=1 to 10 noise pixels at the corners).

### Visual verify after boost

After running the boost, composite a preview against the target panel color and read the result:

```python
from PIL import Image
panel = (11, 33, 71)             # target panel hex
boosted = Image.open('arjun-boosted.png')
prev = Image.new('RGB', boosted.size, panel)
prev.paste(boosted, (0, 0), boosted)
prev.save('/tmp/preview.png')
```

Open `/tmp/preview.png`. The subject should sit cleanly against the panel without a visible color halo (sign of partial alpha leaking the bg through) or a hard saw-tooth edge (sign of the threshold being too aggressive). If you see either, re-run with a different threshold.

### Common failure mode this prevents

Without alpha detection, the flow is: user supplies `arjun.png`, script assumes RGB-with-bg, runs color-distance removal with a sampled "background" color (which is actually empty pixels around the subject), removes the soft halo entirely, boosts what's left, ships a hard-edged headshot on the navy panel that the user calls out as "worse than before."

With alpha detection, the same flow becomes: user supplies `arjun.png`, script reads alpha range, sees it's already cut, routes to `boost_alpha.py`, subject solid, halo preserved, ships cleanly. Zero color-distance pass runs.

---

## Automatic Logo Alpha-Cleanup

Every user-supplied PNG logo gets a luminance-threshold alpha pass automatically. Not optional, not user-flagged. Many vendor-supplied logos arrive with baked-in white backgrounds that the user hadn't noticed in isolation, they only become visible as floating white boxes once placed on the deck's pale-green gradient or other colored panel.

The cost of running the pass on every logo is zero (it's idempotent: a logo without a white bg passes through unchanged). The cost of skipping it is one round-trip with the user every time a vendor PNG has a baked-in background.

### Detect: does this logo have a white background?

```python
import numpy as np
from PIL import Image

def has_white_bg(img_path, sample_inset=2, lum_threshold=240):
    """Sample the four corners of the image. If 3+ corners average lum > 240
    AND the image is in RGB mode (no alpha), assume a baked white background."""
    im = Image.open(img_path)
    if im.mode == 'RGBA':
        # Already has alpha, see "Alpha Detection" section above
        return False
    arr = np.array(im.convert('RGB'))
    h, w = arr.shape[:2]
    s = sample_inset
    corners = [
        arr[s:s+10, s:s+10].mean(axis=(0,1)),
        arr[s:s+10, w-s-10:w-s].mean(axis=(0,1)),
        arr[h-s-10:h-s, s:s+10].mean(axis=(0,1)),
        arr[h-s-10:h-s, w-s-10:w-s].mean(axis=(0,1)),
    ]
    bright = sum(1 for c in corners if c.mean() > lum_threshold)
    return bright >= 3
```

### Pass: luminance threshold with soft falloff

```python
from PIL import Image
import numpy as np

def cleanup_logo(img_path, out_path, hard_threshold=245, soft_threshold=230):
    """Convert near-white pixels to alpha=0, near-near-white pixels to
    partial alpha (anti-aliased edges), auto-bbox crop, save as PNG."""
    im = Image.open(img_path).convert('RGBA')
    arr = np.array(im).astype(np.int16)
    lum = arr[..., :3].mean(axis=-1)
    alpha = np.ones_like(lum, dtype=np.uint8) * 255
    # Hard zero for everything above hard_threshold
    alpha[lum >= hard_threshold] = 0
    # Soft falloff between soft_threshold and hard_threshold
    falloff = (lum >= soft_threshold) & (lum < hard_threshold)
    falloff_alpha = 255 - ((lum - soft_threshold) / (hard_threshold - soft_threshold) * 255)
    alpha[falloff] = falloff_alpha[falloff].clip(0, 255).astype(np.uint8)
    arr[..., 3] = alpha
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA')
    # Auto-bbox crop to drop the transparent margin the white removal exposed
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(out_path, 'PNG', optimize=True)
```

### When to apply

Phase 3 build script runs the pass on every user-supplied logo automatically, no user prompt, no Phase 2 confirmation. Order of operations:

1. User drops a logo PNG into the assets folder.
2. Detect mode (RGB vs RGBA vs pre-cut RGBA, see Alpha Detection above for the routing).
3. If RGB with detected white bg, run `cleanup_logo()`.
4. If RGBA solid alpha, run `cleanup_logo()` defensively (it's idempotent against transparent corners; a logo that's already alpha-cut comes out unchanged).
5. If RGBA pre-cut, route to `boost_alpha.py` per the Alpha Detection section above.
6. Resize to target dimensions, base64-embed.

Logos that fail detection (rare: a brand whose primary color is near-white) get a visual-comparison flag, the build pauses and asks the user to confirm before embedding.

### Why automatic, not user-flagged

The user typically does not notice a logo's baked-in white background in isolation, the original logo PNG looked fine on whatever surface they pulled it from. They only see the problem when the logo lands on a colored deck panel, by which point we've spent a round of iteration getting there. Running the pass by default trades a tiny amount of script time for zero user-feedback rounds on logo backgrounds.
