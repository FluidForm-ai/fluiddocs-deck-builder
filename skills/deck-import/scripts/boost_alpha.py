#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
boost_alpha.py

Phase 3 image-handling helper for the deck-import skill.

Some user-supplied headshots and icons arrive already alpha-cut, but with
the subject body rendered at a partial alpha (e.g. alpha=197 across the
face/body) and a soft fade band at the edges (alpha=10-80). This is common
when:

    - The user ran the original through PowerPoint's "remove background"
      tool, which leaves a soft halo.
    - The image came out of Canva's bg-removal, which keeps fine hair / fur
      detail by feathering alpha rather than hard-masking.
    - It's a vector export from Figma with translucent fills that flattened
      to partial alpha when rasterized.

Running color-distance background removal on these inputs erases the soft
fade band and ships a hard-edged silhouette. The right move is to detect
the existing alpha range first (see references/image-sourcing.md "Alpha
Detection" section), and if the input is pre-cut RGBA, boost the subject's
alpha to 255 while preserving the fade band.

This script does the boost: every pixel with alpha > threshold becomes
fully opaque (alpha=255); pixels with alpha <= threshold are left alone so
the natural feathering survives.

Usage:
    python boost_alpha.py path/to/arjun.png --threshold 30 --out path/to/arjun-boosted.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Tuple

try:
    from PIL import Image
    import numpy as np
except ImportError as e:
    sys.stderr.write(
        f'Missing dependency: {e.name}. Install with:\n'
        f'  pip install --break-system-packages Pillow numpy\n'
    )
    sys.exit(2)


def detect_alpha_state(img_path: Path) -> Tuple[str, Tuple[int, int]]:
    """Inspect an image's alpha channel and report its state."""
    im = Image.open(img_path)
    if im.mode == 'RGB':
        return 'opaque', (255, 255)
    if im.mode == 'RGBA':
        a = np.array(im)[..., 3]
        amin = int(a.min())
        amax = int(a.max())
        if amin == 255:
            return 'opaque', (amin, amax)
        return 'pre-cut', (amin, amax)
    return 'unknown', (0, 0)


def boost_alpha(img_path: Path, out_path: Path, threshold: int = 30) -> dict:
    im = Image.open(img_path)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    arr = np.array(im)
    h, w = arr.shape[:2]

    alpha = arr[..., 3]
    alpha_before = (int(alpha.min()), int(alpha.max()))

    mask = alpha > threshold
    boosted = alpha.copy()
    boosted[mask] = 255

    arr[..., 3] = boosted

    out_im = Image.fromarray(arr, 'RGBA')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_im.save(out_path, 'PNG', optimize=True)

    boosted_pixels = int(mask.sum())
    preserved_pixels = int((~mask).sum())
    return {
        'input':              str(img_path),
        'output':             str(out_path),
        'size':               {'w': w, 'h': h},
        'threshold':          threshold,
        'alpha_min_before':   alpha_before[0],
        'alpha_max_before':   alpha_before[1],
        'alpha_min_after':    int(boosted.min()),
        'alpha_max_after':    int(boosted.max()),
        'pixels_boosted':     boosted_pixels,
        'pixels_preserved':   preserved_pixels,
        'pixel_total':        boosted_pixels + preserved_pixels,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Boost pre-cut RGBA alpha while preserving the soft fade band.')
    parser.add_argument('input', type=Path)
    parser.add_argument('--threshold', type=int, default=30)
    parser.add_argument('--out', type=Path, default=None)
    parser.add_argument('--detect-only', action='store_true')
    args = parser.parse_args()

    if not args.input.exists():
        print(f'ERROR: input not found at {args.input}', file=sys.stderr)
        return 2

    state, (amin, amax) = detect_alpha_state(args.input)

    if args.detect_only:
        import json
        print(json.dumps({
            'state':           state,
            'alpha_min':       amin,
            'alpha_max':       amax,
            'recommendation':  (
                'No bg removal needed; the image is already alpha-cut. Use boost_alpha to solidify the subject.'
                if state == 'pre-cut'
                else 'Run color-distance background removal first (see logo-extraction.md / cover-asset-extraction.md), then re-evaluate.'
                if state == 'opaque'
                else 'Convert to RGBA and re-run detection.'
            ),
        }))
        return 0

    out_path = args.out
    if out_path is None:
        stem = args.input.stem
        out_path = args.input.with_name(f'{stem}-boosted.png')

    summary = boost_alpha(args.input, out_path, threshold=args.threshold)
    import json
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
