#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
parse_slide_size.py

Phase 0 helper for the deck-import skill. Reads <p:sldSz cx cy/> from
ppt/presentation.xml and returns the slide dimensions in EMU.

This must run BEFORE any EMU-to-pixel conversion.

Usage:
    python parse_slide_size.py path/to/ppt/presentation.xml
    -> stdout: {"sldW_emu": 12192000, "sldH_emu": 6858000, "ratio": "16:9"}

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Tuple
from xml.etree import ElementTree as ET

NSMAP = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}

_REFERENCE_RATIOS = [
    ('16:9-widescreen', 12192000, 6858000),
    ('16:9-standard',   9144000,  5143500),
    ('4:3',             9144000,  6858000),
    ('16:10',           9144000,  5715000),
]


def parse_slide_size(presentation_xml: Path) -> Tuple[int, int]:
    """Read <p:sldSz cx cy/> from ppt/presentation.xml. Returns (cx_emu, cy_emu)."""
    tree = ET.parse(presentation_xml)
    sldSz = tree.find('.//p:sldSz', NSMAP)
    if sldSz is None:
        return (12192000, 6858000)
    cx = int(sldSz.get('cx', '12192000'))
    cy = int(sldSz.get('cy', '6858000'))
    return cx, cy


def aspect_ratio_label(cx_emu: int, cy_emu: int) -> str:
    for label, ref_cx, ref_cy in _REFERENCE_RATIOS:
        if abs(cx_emu - ref_cx) / ref_cx < 0.01 and abs(cy_emu - ref_cy) / ref_cy < 0.01:
            return label
    if cy_emu <= 0:
        return 'unknown'
    return f'{round(cx_emu / cy_emu, 3)}:1 (custom)'


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Read <p:sldSz cx cy/> from ppt/presentation.xml and emit JSON.')
    parser.add_argument('presentation_xml', type=Path)
    args = parser.parse_args()

    if not args.presentation_xml.exists():
        print(f'ERROR: presentation.xml not found at {args.presentation_xml}', file=sys.stderr)
        return 2

    cx, cy = parse_slide_size(args.presentation_xml)
    result = {
        'sldW_emu': cx,
        'sldH_emu': cy,
        'ratio':    aspect_ratio_label(cx, cy),
        'inches':   {
            'w': round(cx / 914400, 3),
            'h': round(cy / 914400, 3),
        },
    }
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
