#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
detect_palette.py

Dominant-color extraction for a single page image and cross-page aggregation.

The approach:
  1. Down-sample the image for speed.
  2. Mask near-white pixels (RGB all >= 240) so page backgrounds don't dominate.
  3. K-means cluster remaining pixels into k groups.
  4. Rank clusters by population; return the top_n as hex strings.

Cross-page aggregation takes each page's top-N palette, flattens to a single
point cloud, and re-clusters to k groups. Optional excluded-page indices let
cover photos be dropped from the aggregate.

This file is imported by extract_deck_pdf.py and is also runnable standalone:
    python detect_palette.py path/to/image.png --top-n 3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


NEAR_WHITE_THRESHOLD = 240
NEAR_BLACK_THRESHOLD = 20
SAMPLE_DIM = 200  # downsample longest side to this many px


def dominant_colors_for_image(
    image: Image.Image,
    k: int = 5,
    top_n: int = 3,
) -> list[str]:
    """Return top_n dominant non-white colors (excluding near-white) as hex."""
    rgb = image.convert("RGB")
    rgb.thumbnail((SAMPLE_DIM, SAMPLE_DIM))
    pixels = np.array(rgb).reshape(-1, 3)

    mask = ~np.all(pixels >= NEAR_WHITE_THRESHOLD, axis=1)
    filtered = pixels[mask]
    if filtered.size == 0:
        return []

    non_black_mask = ~np.all(filtered <= NEAR_BLACK_THRESHOLD, axis=1)
    near_black_count = int((~non_black_mask).sum())
    non_neutral = filtered[non_black_mask]

    palette: list[tuple[int, tuple[int, int, int]]] = []
    if non_neutral.size and HAS_SKLEARN:
        km = KMeans(n_clusters=min(k, len(non_neutral)), n_init=4, random_state=42)
        km.fit(non_neutral)
        centers = km.cluster_centers_.astype(int)
        counts = np.bincount(km.labels_, minlength=len(centers))
        for center, count in zip(centers, counts):
            palette.append((int(count), tuple(int(c) for c in center)))
    elif non_neutral.size:
        quantized = rgb.quantize(colors=k)
        pal = quantized.getpalette() or []
        color_counts = sorted(quantized.getcolors() or [], reverse=True)
        for count, idx in color_counts[:k]:
            start = idx * 3
            rgb_slice = pal[start: start + 3]
            if len(rgb_slice) < 3:
                continue
            r, g, b = rgb_slice
            if all(c >= NEAR_WHITE_THRESHOLD for c in (r, g, b)):
                continue
            palette.append((count, (r, g, b)))

    if near_black_count > len(filtered) * 0.02:
        palette.append((near_black_count, (11, 18, 32)))  # #0B1220

    palette.sort(key=lambda kv: -kv[0])
    hex_palette: list[str] = []
    for _, rgb_tuple in palette:
        hex_code = _rgb_to_hex(rgb_tuple)
        if _is_near_duplicate(hex_code, hex_palette):
            continue
        hex_palette.append(hex_code)
        if len(hex_palette) >= top_n:
            break
    return hex_palette


def aggregate_palette(
    per_page_palettes: list[list[str]],
    k: int = 5,
    exclude_page_indices: list[int] | None = None,
) -> list[str]:
    exclude = set(exclude_page_indices or [])
    colors: list[tuple[int, int, int]] = []
    for i, page_palette in enumerate(per_page_palettes):
        if i in exclude:
            continue
        for hex_code in page_palette:
            colors.append(_hex_to_rgb(hex_code))
    if not colors:
        return []

    arr = np.array(colors)
    if not HAS_SKLEARN:
        seen: dict[tuple[int, int, int], int] = {}
        for c in colors:
            seen[c] = seen.get(c, 0) + 1
        ranked = sorted(seen.items(), key=lambda kv: -kv[1])
        return [_rgb_to_hex(c) for c, _ in ranked[:k]]

    km = KMeans(n_clusters=min(k, len(arr)), n_init=4, random_state=42)
    km.fit(arr)
    centers = km.cluster_centers_.astype(int)
    counts = np.bincount(km.labels_, minlength=len(centers))

    ranked = sorted(zip(centers, counts), key=lambda cc: -cc[1])
    out: list[str] = []
    for center, _count in ranked:
        hex_code = _rgb_to_hex(tuple(int(c) for c in center))
        if _is_near_duplicate(hex_code, out):
            continue
        out.append(hex_code)
    return out[:k]


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def _hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    h = hex_code.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _is_near_duplicate(hex_code: str, existing: list[str], threshold: int = 25) -> bool:
    r1, g1, b1 = _hex_to_rgb(hex_code)
    for e in existing:
        r2, g2, b2 = _hex_to_rgb(e)
        dist = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        if dist < threshold:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract dominant colors from an image.")
    parser.add_argument("image_path", type=Path)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--top-n", type=int, default=3)
    args = parser.parse_args()

    img = Image.open(args.image_path)
    palette = dominant_colors_for_image(img, k=args.k, top_n=args.top_n)
    for color in palette:
        print(color)
    return 0


if __name__ == "__main__":
    sys.exit(main())
