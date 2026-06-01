#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
crop_cover_assets.py

Agent-callable helper for Phase 3 cover-asset extraction. Use this instead
of hand-rolling fractional crops, fixed-fraction crops bleed source panel
background into extracted hero images, and baked-in backgrounds become
visible "frames" around alpha-unaware logos.

Exposes three functions an agent can import:

    find_panel_edge(page, axis='x', start_frac=0.30, end_frac=0.70,
                    tolerance=40, sample_stride=20)
    crop_hero_image(page, panel_edge_x, out_path, quality=88)
    extract_alpha_logo(page, bg_color, crop_bounds=None, tolerance=30,
                       out_path=None)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple, Union

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("Missing dependency: Pillow. Install with:\n  pip install --break-system-packages Pillow\n")
    sys.exit(2)


ImageOrPath = Union[Image.Image, str, Path]
BoundsT = Tuple[float, float, float, float]


def _open(img: ImageOrPath) -> Image.Image:
    if isinstance(img, (str, Path)):
        return Image.open(img).convert("RGB") if Image.open(img).mode != "RGBA" else Image.open(img)
    return img


def _resolve_bounds(bounds: BoundsT, w: int, h: int) -> Tuple[int, int, int, int]:
    x0, y0, x1, y1 = bounds
    if max(x0, x1) <= 1.0 and max(y0, y1) <= 1.0:
        return int(w * x0), int(h * y0), int(w * x1), int(h * y1)
    return int(x0), int(y0), int(x1), int(y1)


def find_panel_edge(
    page: ImageOrPath,
    axis: str = "x",
    start_frac: float = 0.30,
    end_frac: float = 0.70,
    brightness_delta: float = 40.0,
    sample_stride: int = 20,
) -> int:
    im = _open(page).convert("RGB")
    w, h = im.size
    px = im.load()

    if axis == "x":
        lo, hi = int(w * start_frac), int(w * end_frac)
        samples = list(range(0, h, sample_stride))
        prev_avg = None
        for x in range(lo, hi):
            tot = 0
            for y in samples:
                r, g, b = px[x, y]
                tot += (r + g + b) / 3
            avg = tot / len(samples)
            if prev_avg is not None and (avg - prev_avg) > brightness_delta:
                return x
            prev_avg = avg
        return _deepest_match(px, axis="x", w=w, h=h, stride=sample_stride)

    else:  # axis == 'y'
        lo, hi = int(h * start_frac), int(h * end_frac)
        samples = list(range(0, w, sample_stride))
        prev_avg = None
        for y in range(lo, hi):
            tot = 0
            for x in samples:
                r, g, b = px[x, y]
                tot += (r + g + b) / 3
            avg = tot / len(samples)
            if prev_avg is not None and (avg - prev_avg) > brightness_delta:
                return y
            prev_avg = avg
        return _deepest_match(px, axis="y", w=w, h=h, stride=sample_stride)


def _deepest_match(px, axis: str, w: int, h: int, stride: int) -> int:
    last = 0
    if axis == "x":
        for y in range(0, h, stride):
            for x in range(w):
                r, g, b = px[x, y]
                if (r + g + b) / 3 < 90 and x > last:
                    last = x
    else:
        for x in range(0, w, stride):
            for y in range(h):
                r, g, b = px[x, y]
                if (r + g + b) / 3 < 90 and y > last:
                    last = y
    return last


def crop_hero_image(
    page: ImageOrPath,
    panel_edge_x: int,
    out_path: str,
    safety_pad: int = 2,
    quality: int = 88,
) -> Tuple[int, int]:
    im = _open(page).convert("RGB")
    w, h = im.size
    x0 = min(max(0, panel_edge_x + safety_pad), w - 1)
    crop = im.crop((x0, 0, w, h))
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    crop.save(out_path, "JPEG", quality=quality, optimize=True)
    return crop.size


def extract_alpha_logo(
    page: ImageOrPath,
    bg_color: Tuple[int, int, int],
    crop_bounds: Optional[BoundsT] = None,
    tolerance: float = 30.0,
    auto_bbox: bool = True,
    out_path: Optional[str] = None,
) -> Image.Image:
    im = _open(page).convert("RGBA")
    w, h = im.size

    if crop_bounds:
        box = _resolve_bounds(crop_bounds, w, h)
        crop = im.crop(box)
    else:
        crop = im.copy()

    cw, ch = crop.size
    px = crop.load()
    br, bg, bb = bg_color
    tol_sq = tolerance * tolerance

    for y in range(ch):
        for x in range(cw):
            r, g, b, a = px[x, y]
            dr, dg, db = r - br, g - bg, b - bb
            if (dr * dr + dg * dg + db * db) < tol_sq:
                px[x, y] = (0, 0, 0, 0)
            else:
                px[x, y] = (r, g, b, 255)

    if auto_bbox:
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        crop.save(out_path, "PNG", optimize=True)

    return crop


def split_cover_panels(
    page: ImageOrPath,
    bg_color: Tuple[int, int, int],
    logo_bounds: BoundsT,
    hero_out: str,
    logo_out: str,
) -> dict:
    edge = find_panel_edge(page)
    hero_size = crop_hero_image(page, edge, hero_out)
    logo = extract_alpha_logo(page, bg_color=bg_color, crop_bounds=logo_bounds, out_path=logo_out)
    return {
        "panel_edge_x": edge,
        "hero_out": hero_out,
        "hero_size": hero_size,
        "logo_out": logo_out,
        "logo_size": logo.size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Crop cover-panel assets from a deck page image.")
    parser.add_argument("page", type=Path)
    parser.add_argument("--bg", required=True, help="Panel background color, e.g. '17,58,84' (R,G,B).")
    parser.add_argument("--logo-bounds", required=True,
                        help="Logo crop bounds as 'x0,y0,x1,y1' in pixels or fractions (0.0-1.0).")
    parser.add_argument("--hero-out", required=True)
    parser.add_argument("--logo-out", required=True)
    args = parser.parse_args()

    bg_color = tuple(int(x) for x in args.bg.split(","))
    bounds = tuple(float(x) for x in args.logo_bounds.split(","))

    result = split_cover_panels(
        page=args.page,
        bg_color=bg_color,
        logo_bounds=bounds,
        hero_out=args.hero_out,
        logo_out=args.logo_out,
    )
    for k, v in result.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
