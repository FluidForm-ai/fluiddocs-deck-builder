# Extraction Pipeline, Data Contract + Fallback Rules

This file covers two extraction paths:

1. **PDF path** (`scripts/extract_deck_pdf.py` + optional `scripts/extract_pptx_assets.py`), used when input is `.pdf`.
2. **PPTX-only path** (`scripts/extract-pptx-only.py`), used when input is `.pptx` and no PDF is provided.

Both paths are deliberately deterministic: same input in, same JSON + images out. The agent reads the JSON; it doesn't re-run OCR or image diffing itself. This separation keeps Phase 0 fast and auditable.

---

## Data contract (extraction.json, PDF path)

```json
{
  "source_pdf": "/absolute/path/to/deck.pdf",
  "extracted_at": "2026-04-23T14:22:00Z",
  "metadata": {
    "title": "Acme Pitch Q2 2026",
    "author": "Founder Name",
    "subject": null,
    "creator": "Keynote 13.1",
    "page_count": 14,
    "detected_aspect_ratio": "16:9",
    "was_ocr_fallback": false,
    "was_encrypted": false
  },
  "pages": [
    {
      "page_num": 1,
      "text": "Acme\nWe help legal teams draft contracts 10x faster.\n...",
      "image_path": "/tmp/deck-import-<ts>/pages/page-01.png",
      "image_dimensions": {"width": 2880, "height": 1620},
      "detected_font_families": ["Tiempos Headline", "Inter"],
      "has_hero_image": false,
      "dominant_palette": ["#0B1220", "#F97316", "#F8FAFC"]
    },
    { "page_num": 2, "...": "..." }
  ],
  "aggregated": {
    "dominant_palette_across_deck": ["#0B1220", "#F97316", "#F8FAFC", "#94A3B8"],
    "dominant_font_families": ["Tiempos Headline", "Inter"],
    "slides_with_hero_images": [1, 5, 8],
    "longest_text_slide": 3,
    "shortest_text_slide": 14
  }
}
```

Field notes:

- `metadata.detected_aspect_ratio`, computed from page 1 dimensions. If the PDF is 4:3, 1:1, or something weird, the conversion brief will note this; the output canvas stays 1440x810 but slides are centered with letterbox padding rather than full-bleed.
- `pages[].image_path`, always a PNG at 2x the slide's rendered dimensions (so a 1920x1080 slide renders at 3840x2160). This gives you headroom for Retina displays when the image is placed as a hero.
- `pages[].detected_font_families`, pulled from `pdfplumber`'s `chars[].fontname` field. May include foundry prefixes (`ABCDEF+Inter-Regular`), normalize by stripping the `^[A-Z]+\+` prefix.
- `aggregated.dominant_palette_across_deck`, the top 4 colors after cross-page aggregation. Different from per-page palettes, which are noisy (a single photo dominates its page).
- `was_ocr_fallback`, `true` if the PDF had no text layer (scanned deck) and OCR was used. Role classification is less reliable in this case; flag in the confirmation block.

---

## Data contract (pptx-manifest.json, PPTX-only path)

```json
{
  "source_pptx": "/absolute/path/to/deck.pptx",
  "extracted_at": "2026-04-23T14:22:00Z",
  "metadata": {
    "title": "Acme Pitch Q2 2026",
    "author": "Founder Name",
    "slide_count": 14,
    "slide_size_emu": {"cx": 12192000, "cy": 6858000},
    "ratio": "16:9"
  },
  "slides": [
    {
      "slide_num": 1,
      "title": "Acme",
      "body_text": "We help legal teams draft contracts 10x faster.",
      "captions": [],
      "notes": "Speaker notes verbatim from the notes pane.",
      "images": [
        {
          "path": "/tmp/deck-import-<ts>/media/image-1-1.png",
          "position_px": {"x": 720, "y": 400},
          "size_px": {"w": 600, "h": 400}
        }
      ]
    }
  ]
}
```

This manifest is consumed directly by `classify_slides.py` (treating each slide's `body_text` as if it were the PDF page's extracted text). Image-position math uses the same EMU divisors as the PDF+PPTX hybrid path (see Step 0b in SKILL.md).

---

## Fallback rules (PDF path)

### PDF is encrypted
- If pypdf raises `DependencyError` or `PyCryptodomeNotInstalled`, install `pycryptodome` via pip and retry.
- If PDF is password-protected, stop and ask the user for the password. Do not try to brute-force.

### PDF has no text layer (scanned)
- `pdfplumber` returns empty strings for all pages, trigger OCR fallback.
- Use `pdf2image.convert_from_path(...)` + `pytesseract.image_to_string(...)` per page.
- Set `was_ocr_fallback: true` in metadata. Downstream: Analysis Phase lowers role-classification confidence ceilings by one step (high to medium, medium to low).

### PDF is very large (>50 MB or >50 pages)
- Pitch decks don't exceed 30 pages in practice. If the PDF is bigger, it's probably not a pitch deck.
- Script warns and asks the user to confirm before proceeding. User may say "yes, process anyway" (e.g., a sales or keynote deck being miscategorized) or "stop, this is the wrong PDF."

### PDF is not 16:9
- Common non-16:9 formats: 4:3 (legacy), 1:1 (social share), A4/letter (document-style PDFs).
- Script records `detected_aspect_ratio`. Build Phase will letterbox-pad the slide content inside the 1440x810 canvas rather than stretching. A 4:3 source deck, for instance, centers each slide with roughly 90px gutters left/right.

### Multiple decks in one PDF
- Rare but happens (someone merged two decks). Script flags if there are >2 "cover-like" pages (page_num=1 and a later page with company name + tagline).
- Ask the user: "This PDF looks like it might contain 2 decks. Should I process them separately, or treat as one?"

---

## Script invocation

Run from the skill's own `scripts/` directory (`${SKILL_DIR}/scripts/extract_deck_pdf.py` or `extract-pptx-only.py`). Never hardcode the install path, the skill may be installed at various paths depending on the agent's setup.

### PDF path
```bash
python "${SKILL_DIR}/scripts/extract_deck_pdf.py" \
    <pdf-path> \
    --out /tmp/deck-import-<timestamp>/ \
    [--force-ocr]         # skip text layer even if present, force OCR
    [--image-dpi 200]     # default 150; raise for high-res screenshots
    [--max-pages 30]      # safety cap
```

### PPTX-only path
```bash
python "${SKILL_DIR}/scripts/extract-pptx-only.py" \
    <pptx-path> \
    --out /tmp/deck-import-<timestamp>/
```

**Success signal**: script exits 0 on success. Non-zero exit with a message on stderr indicates failure. The agent reads the exit code, do not try to parse prose output for success/failure.

PDF output directory structure:
```
/tmp/deck-import-<ts>/
├── extraction.json
└── pages/
    ├── page-01.png
    ├── page-02.png
    └── ...
```

PPTX-only output directory structure:
```
/tmp/deck-import-<ts>/
├── pptx-manifest.json
└── media/
    ├── image-1-1.png
    ├── image-2-1.png
    └── ...
```

---

## Python dependencies

Installed via `pip install --break-system-packages <pkg>`:

PDF path:
- `pdfplumber` (text + font metadata)
- `pypdf` (metadata + encryption check)
- `pdf2image` (page to image conversion; requires poppler-utils at the OS level)
- `Pillow` (image manipulation, palette sampling)
- `pytesseract` (OCR fallback; requires tesseract at the OS level)
- `scikit-learn` (k-means clustering for palette extraction; alternative: `colorthief`)

PPTX path (either):
- `python-pptx` (walks PPTX content, extracts text, images, notes)

On macOS, poppler + tesseract are typically available via brew. On Linux sandboxes (Ubuntu 22), install via `apt-get install poppler-utils tesseract-ocr`.

---

## What the agent does after Phase 0

Read the manifest JSON (`extraction.json` for PDF path, `pptx-manifest.json` for PPTX-only path). Do NOT re-run extraction logic in-process, scripts are the deterministic layer, the agent is the reasoning layer. If something in the JSON looks off (e.g., all pages have empty text, or the page count is 1), inspect the source file directly with the relevant tools before raising a user-facing error.

---

## PPTX icon extraction

When PPTX is available (either as the primary source on the PPTX-only path, or as a sibling alongside the PDF on the PDF path), source icons live in `ppt/media/imageN.svg` and `ppt/media/imageN.png`. Don't recreate them as inline `<svg>` paths, generic recreations drift toward Material-Design shapes that read as a different brand register than the source's specific custom illustrations.

### Map slide to image via relationships

`ppt/slides/_rels/slideN.xml.rels` lists every `<Relationship>` referenced by `slideN.xml`. For each image:

```python
import re, zipfile
from xml.etree import ElementTree as ET

NS_REL = 'http://schemas.openxmlformats.org/package/2006/relationships'

def icons_for_slide(extract_root, slide_num):
    """Return [(rId, image_path_relative_to_extract_root), ...] for one slide."""
    rels_path = extract_root / 'ppt' / 'slides' / '_rels' / f'slide{slide_num}.xml.rels'
    if not rels_path.exists():
        return []
    tree = ET.parse(rels_path)
    out = []
    for child in tree.getroot():
        if not child.tag.endswith('Relationship'):
            continue
        target = child.get('Target', '')
        rid    = child.get('Id', '')
        if 'image' not in target.lower():
            continue
        # Target is usually '../media/imageN.png' (relative to slides/)
        abs_path = (rels_path.parent / target).resolve()
        try:
            rel = abs_path.relative_to(extract_root)
        except ValueError:
            rel = abs_path
        out.append((rid, str(rel)))
    return out
```

`extract_pptx_assets.py` already emits this mapping in `pptx_assets.json` under each slide's `pics` list, read that JSON rather than re-parsing relationships in the build script.

### Embed as `<img>`, not inline SVG

Build script reads the SVG/PNG, base64-encodes, and embeds as a `data:` URI in an `<img>` tag rather than inlining the SVG paths:

```python
import base64
b64 = base64.b64encode(open(svg_path, 'rb').read()).decode()
img_tag = f'<img class="ic" alt="" src="data:image/svg+xml;base64,{b64}">'
```

This keeps the source's stroke widths, corner rounding, and aspect ratios exactly as authored. Inline-SVG recreation can't credibly match a custom illustration set.

---

## PPTX icon color normalization

PPTX icons frequently use two distinct color styles within the same deck:

- **`fill="#ffffff"`** (or `#fdfdfd`) for white-on-colored-square slots, `.stat-icon`, `.sol-icon`, etc.
- **`fill="#006838"`** (or `#000000`) for outline-on-light-bg slots, standalone icons on the slide paper.

Rendered with default settings, the white-on-colored set appears invisible against any white surface in the HTML preview (white-on-white). The fix is to set the fill per-slot before rendering, matching the icon's intended pairing classified in Phase 1.

### sed-based fill swap

Before ImageMagick conversion or before base64-embedding:

```bash
sed -e 's/fill="#ffffff"/fill="<target>"/g' \
    -e 's/fill="#fdfdfd"/fill="<target>"/g' \
    -e 's/fill="#000000"/fill="<target>"/g' \
    -e 's/fill="inherit"//g' \
    source.svg > target.svg
```

`<target>` is the deck's primary brand color (e.g., `#006838`) when the slot is `icon-on-light-bg`, or stays white when the slot is `icon-on-colored-square`.

### Strip `fill="inherit"`

ImageMagick doesn't honor `fill="inherit"`, the cascading-color resolution happens at SVG parse time and ImageMagick's SVG renderer skips it. Result: glyphs rendered with `fill="inherit"` come out transparent. Strip the attribute entirely (`-e 's/fill="inherit"//g'`) so the browser/renderer falls back to the parent element's `fill` (typically `currentColor`).

### When to apply

Phase 1 emits an `icon_pairing` classification per icon slot (`icon-on-colored-square` vs `icon-on-light-bg`). Phase 3 reads the classification, runs the sed substitution with the right target color, and only then base64-embeds. Don't try to skip the swap and rely on CSS `filter: invert()` or `currentColor`, both interact badly with SVG `<defs>` and gradient stops in custom illustrations.

---

## Logo stack detection

When the source has a logo wall with stacked logos, naive horizontal-adjacency grouping pairs logos by reading order (e.g., United+TurnKey, Hoot+SM), but the source visually stacks them (United-then-Hoot is one column; TurnKey-then-SM is the next).

### Detect by overlapping x-ranges

Phase 1 emits an `(x, y, w, h)` bounding box per logo. Group logos into vertical stacks where:

1. The x-ranges of two boxes overlap by >= 60% of the narrower box's width.
2. The y-ranges of the two boxes differ by more than half the canvas-height of the wall region (so they're stacked, not side-by-side at the same y).

```python
def detect_stacks(boxes, x_overlap_min=0.6, y_distance_min_frac=0.5, wall_height=None):
    """boxes = [(x, y, w, h), ...]. Returns list of stack indices."""
    n = len(boxes)
    if wall_height is None:
        wall_height = max(b[1] + b[3] for b in boxes) - min(b[1] for b in boxes)
    y_threshold = wall_height * y_distance_min_frac
    stacks = []
    used = set()
    for i in range(n):
        if i in used:
            continue
        xi, yi, wi, hi = boxes[i]
        for j in range(i + 1, n):
            if j in used:
                continue
            xj, yj, wj, hj = boxes[j]
            # x-range overlap fraction
            overlap = max(0, min(xi + wi, xj + wj) - max(xi, xj))
            narrower = min(wi, wj)
            overlap_frac = overlap / narrower if narrower else 0
            if overlap_frac >= x_overlap_min and abs(yi - yj) >= y_threshold:
                stacks.append([i, j])
                used.add(i); used.add(j)
                break
    # Singletons
    for i in range(n):
        if i not in used:
            stacks.append([i])
    return stacks
```

### HTML layout consequence

Once stacks are detected, the build script emits a column-per-stack flexbox layout rather than a single row of boxes. Singletons become 1-row columns; pairs become 2-row columns. The user's eye sees the same vertical pairings as the source.
