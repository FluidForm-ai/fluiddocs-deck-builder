#!/usr/bin/env python3
# SPDX-License-Identifier: MIT  (see LICENSE in the repo root)
"""
extract_pptx_assets.py

Phase 0 PPTX-assist extractor for the deck-import skill, used by the PDF
path when a sibling .pptx is available alongside the .pdf.

When a .pptx of the source deck is available, this script gives roughly 5x
the fidelity of PDF-only extraction. It unzips the pptx, walks every
slide's XML plus its relationships file, and emits a JSON manifest with:

  - per-slide list of pic refs:
      (rId, image_path, position_px, size_px)
    keyed back to the unzipped ppt/media/ folder
  - per-slide list of <a:gradFill> records (slide bg + per-shape):
      (color_stops, angle, scope)
  - per-slide background classification: photo-tint / flat-gradient / solid
  - per-slide list of <a:custGeom> shapes with cx:cy ratio

The build script reads this JSON for geometry, gradients, and asset paths
instead of approximating from the rasterized PDF.

For PPTX-only input (no PDF), use extract-pptx-only.py instead, which emits
a slimmer manifest tailored to the auto-detect routing path.

Usage:
    python extract_pptx_assets.py <pptx-path> --out /tmp/deck-import-<ts>/pptx/

Output structure:
    <out_dir>/
        ppt/                  -- unzipped pptx contents
        pptx_assets.json      -- the manifest

Dependencies: stdlib only (zipfile + xml.etree).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

NSMAP = {
    'a':  'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p':  'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r':  'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rs': 'http://schemas.openxmlformats.org/package/2006/relationships',
}

for prefix, uri in NSMAP.items():
    ET.register_namespace(prefix if prefix != 'rs' else '', uri)

EMU_PER_INCH = 914400
PPT_ANGLE_PER_DEG = 60000


def emu_to_px(emu: int, total_emu: int, canvas_px: int) -> float:
    if total_emu <= 0:
        return 0.0
    return round((emu / total_emu) * canvas_px, 2)


def parse_slide_size(presentation_xml: Path) -> Tuple[int, int]:
    tree = ET.parse(presentation_xml)
    sldSz = tree.find('.//p:sldSz', NSMAP)
    if sldSz is None:
        return (12192000, 6858000)
    cx = int(sldSz.get('cx', '12192000'))
    cy = int(sldSz.get('cy', '6858000'))
    return cx, cy


def parse_rels(rels_path: Path) -> Dict[str, Dict[str, str]]:
    if not rels_path.exists():
        return {}
    tree = ET.parse(rels_path)
    rels = {}
    root = tree.getroot()
    for child in root:
        local = child.tag.split('}', 1)[-1]
        if local != 'Relationship':
            continue
        rId = child.get('Id', '')
        rels[rId] = {
            'Type':   child.get('Type', ''),
            'Target': child.get('Target', ''),
        }
    return rels


def resolve_rel_target(slide_path: Path, target: str) -> Path:
    return (slide_path.parent / target).resolve()


def read_color_stops(grad_fill: ET.Element) -> List[Tuple[float, str, Optional[float]]]:
    stops = []
    gs_list = grad_fill.find('a:gsLst', NSMAP)
    if gs_list is None:
        return stops
    for gs in gs_list.findall('a:gs', NSMAP):
        pos = float(gs.get('pos', '0')) / 1000.0
        srgb = gs.find('a:srgbClr', NSMAP)
        scheme = gs.find('a:schemeClr', NSMAP)
        alpha_el = None
        color: Optional[str] = None
        if srgb is not None:
            color = f"#{srgb.get('val', '000000')}"
            alpha_el = srgb.find('a:alpha', NSMAP)
        elif scheme is not None:
            color = f"scheme:{scheme.get('val', 'accent1')}"
            alpha_el = scheme.find('a:alpha', NSMAP)
        if color is None:
            continue
        alpha_pct: Optional[float] = None
        if alpha_el is not None:
            alpha_pct = float(alpha_el.get('val', '100000')) / 1000.0
        stops.append((round(pos, 2), color, alpha_pct))
    return stops


def read_grad_angle(grad_fill: ET.Element) -> Optional[int]:
    lin = grad_fill.find('a:lin', NSMAP)
    if lin is None:
        return None
    try:
        return int(lin.get('ang', '0'))
    except ValueError:
        return 0


def ppt_angle_to_css(emu_angle: int) -> int:
    deg = (emu_angle / PPT_ANGLE_PER_DEG) % 360
    return int((deg + 180) % 360)


def read_xfrm(shape: ET.Element) -> Optional[Dict[str, int]]:
    xfrm = shape.find('.//a:xfrm', NSMAP)
    if xfrm is None:
        return None
    off = xfrm.find('a:off', NSMAP)
    ext = xfrm.find('a:ext', NSMAP)
    if off is None or ext is None:
        return None
    try:
        return {
            'x_emu':  int(off.get('x',  '0')),
            'y_emu':  int(off.get('y',  '0')),
            'cx_emu': int(ext.get('cx', '0')),
            'cy_emu': int(ext.get('cy', '0')),
        }
    except ValueError:
        return None


def classify_custgeom(xfrm: Dict[str, int]) -> Dict[str, Any]:
    cx = max(xfrm.get('cx_emu', 0), 0)
    cy = max(xfrm.get('cy_emu', 1), 1)
    ratio = cx / cy if cy else 0
    if abs(ratio - 1.0) <= 0.15:
        bucket = 'circle'
    elif abs(ratio - 2.0) <= 0.15:
        bucket = 'semicircle'
    elif abs(ratio - 1.55) <= 0.15:
        bucket = 'half-dome'
    else:
        bucket = 'other'
    return {'ratio': round(ratio, 3), 'bucket': bucket}


def extract(pptx_path: Path, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    extract_root = out_dir
    ppt_dir = out_dir / 'ppt'
    if ppt_dir.exists():
        shutil.rmtree(ppt_dir)
    with zipfile.ZipFile(pptx_path, 'r') as zf:
        zf.extractall(extract_root)

    presentation_xml = ppt_dir / 'presentation.xml'
    sldW_emu, sldH_emu = parse_slide_size(presentation_xml)
    canvas_w_px, canvas_h_px = 1440, 810  # deck canvas

    slides_dir = ppt_dir / 'slides'
    slide_files = sorted(slides_dir.glob('slide*.xml'),
                         key=lambda p: int(re.search(r'slide(\d+)\.xml', p.name).group(1)))

    manifest: Dict[str, Any] = {
        'source':       str(pptx_path),
        'sldW_emu':     sldW_emu,
        'sldH_emu':     sldH_emu,
        'canvas_px':    {'w': canvas_w_px, 'h': canvas_h_px},
        'aspect_ratio': f"{round(sldW_emu / sldH_emu, 2)}:1",
        'slide_count':  len(slide_files),
        'slides':       [],
    }

    for slide_path in slide_files:
        slide_num = int(re.search(r'slide(\d+)\.xml', slide_path.name).group(1))
        rels_path = slide_path.parent / '_rels' / f'{slide_path.name}.rels'
        rels = parse_rels(rels_path)

        slide_tree = ET.parse(slide_path)

        pics: List[Dict[str, Any]] = []
        for pic in slide_tree.findall('.//p:pic', NSMAP):
            blip = pic.find('.//a:blip', NSMAP)
            rId = blip.get(f"{{{NSMAP['r']}}}embed", '') if blip is not None else ''
            target = rels.get(rId, {}).get('Target', '')
            image_path = ''
            if target:
                try:
                    abs_path = resolve_rel_target(slide_path, target)
                    image_path = str(abs_path.relative_to(extract_root))
                except (ValueError, OSError):
                    image_path = target
            xfrm = read_xfrm(pic)
            entry: Dict[str, Any] = {
                'rId': rId,
                'image_path': image_path,
            }
            if xfrm:
                entry['position_px'] = {
                    'x': emu_to_px(xfrm['x_emu'], sldW_emu, canvas_w_px),
                    'y': emu_to_px(xfrm['y_emu'], sldH_emu, canvas_h_px),
                }
                entry['size_px'] = {
                    'w': emu_to_px(xfrm['cx_emu'], sldW_emu, canvas_w_px),
                    'h': emu_to_px(xfrm['cy_emu'], sldH_emu, canvas_h_px),
                }
                entry['position_emu'] = {'x': xfrm['x_emu'], 'y': xfrm['y_emu']}
                entry['size_emu'] = {'cx': xfrm['cx_emu'], 'cy': xfrm['cy_emu']}
                w_px = entry['size_px']['w']
                h_px = entry['size_px']['h']
                if w_px > 0 and h_px > 0:
                    aspect = w_px / h_px if h_px else 0
                    full_bleed = w_px >= 0.8 * canvas_w_px
                    is_short = h_px < 200
                    if full_bleed and is_short and aspect >= 5:
                        entry['role_hint'] = 'curve-divider'
            pics.append(entry)

        gradients: List[Dict[str, Any]] = []
        for bg_grad in slide_tree.findall('.//p:bg//a:gradFill', NSMAP):
            ang = read_grad_angle(bg_grad)
            stops = read_color_stops(bg_grad)
            gradients.append({
                'scope':       'background',
                'color_stops': [{'pos_pct': s[0], 'color': s[1], 'alpha_pct': s[2]} for s in stops],
                'angle_emu':   ang,
                'angle_ppt_deg': (ang / PPT_ANGLE_PER_DEG) % 360 if ang is not None else None,
                'angle_css_deg': ppt_angle_to_css(ang) if ang is not None else None,
            })
        for sp in slide_tree.findall('.//p:sp', NSMAP):
            for grad in sp.findall('.//a:gradFill', NSMAP):
                ang = read_grad_angle(grad)
                stops = read_color_stops(grad)
                gradients.append({
                    'scope':       'shape',
                    'color_stops': [{'pos_pct': s[0], 'color': s[1], 'alpha_pct': s[2]} for s in stops],
                    'angle_emu':   ang,
                    'angle_ppt_deg': (ang / PPT_ANGLE_PER_DEG) % 360 if ang is not None else None,
                    'angle_css_deg': ppt_angle_to_css(ang) if ang is not None else None,
                })

        bg = slide_tree.find('.//p:bg//p:bgPr', NSMAP)
        bg_type = 'inherit'
        bg_image_rId = ''
        if bg is not None:
            blip = bg.find('.//a:blipFill', NSMAP)
            grad = bg.find('.//a:gradFill', NSMAP)
            solid = bg.find('.//a:solidFill', NSMAP)
            if blip is not None:
                bg_type = 'photo-tint'
                blip_inner = blip.find('a:blip', NSMAP)
                if blip_inner is not None:
                    bg_image_rId = blip_inner.get(f"{{{NSMAP['r']}}}embed", '')
            elif grad is not None:
                bg_type = 'flat-gradient'
            elif solid is not None:
                bg_type = 'solid'
        bg_image_path = ''
        if bg_image_rId:
            target = rels.get(bg_image_rId, {}).get('Target', '')
            if target:
                try:
                    abs_path = resolve_rel_target(slide_path, target)
                    bg_image_path = str(abs_path.relative_to(extract_root))
                except (ValueError, OSError):
                    bg_image_path = target

        custgeom_shapes: List[Dict[str, Any]] = []
        for sp in slide_tree.findall('.//p:sp', NSMAP):
            cust = sp.find('.//a:custGeom', NSMAP)
            if cust is None:
                continue
            xfrm = read_xfrm(sp)
            if not xfrm:
                continue
            cls = classify_custgeom(xfrm)
            custgeom_shapes.append({
                'position_px': {
                    'x': emu_to_px(xfrm['x_emu'], sldW_emu, canvas_w_px),
                    'y': emu_to_px(xfrm['y_emu'], sldH_emu, canvas_h_px),
                },
                'size_px': {
                    'w': emu_to_px(xfrm['cx_emu'], sldW_emu, canvas_w_px),
                    'h': emu_to_px(xfrm['cy_emu'], sldH_emu, canvas_h_px),
                },
                'size_emu':       {'cx': xfrm['cx_emu'], 'cy': xfrm['cy_emu']},
                'cx_cy_ratio':    cls['ratio'],
                'shape_bucket':   cls['bucket'],
            })

        manifest['slides'].append({
            'slide':          slide_num,
            'pics':           pics,
            'gradients':      gradients,
            'background': {
                'type':       bg_type,
                'image_rId':  bg_image_rId,
                'image_path': bg_image_path,
            },
            'custgeom':       custgeom_shapes,
        })

    manifest_path = out_dir / 'pptx_assets.json'
    manifest_path.write_text(json.dumps(manifest, indent=2))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description='Extract PPTX assets into JSON manifest.')
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()

    if not args.pptx.exists():
        print(f'ERROR: pptx not found at {args.pptx}', file=sys.stderr)
        return 2
    if args.pptx.suffix.lower() != '.pptx':
        print(f'WARN: expected .pptx extension, got {args.pptx.suffix}', file=sys.stderr)

    manifest = extract(args.pptx, args.out)
    summary = {
        'sldW_emu':    manifest['sldW_emu'],
        'sldH_emu':    manifest['sldH_emu'],
        'slide_count': manifest['slide_count'],
        'manifest':    str(args.out / 'pptx_assets.json'),
        'media_dir':   str(args.out / 'ppt' / 'media'),
    }
    print(json.dumps(summary))
    return 0


if __name__ == '__main__':
    sys.exit(main())
