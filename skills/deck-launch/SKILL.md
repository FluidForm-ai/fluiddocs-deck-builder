---
name: deck-launch
description: Builds launch decks for product announcements and go-to-market moments. Trigger on "launch deck", "product launch", "product announcement", "launch template", "go-to-market launch", or "launch presentation". A thin type pack inheriting the full 5-phase pipeline from deck-builder core. Deck-launch-specific. 12-slide structure with a demo slot on Slide 5 (static screenshot in OSS), co-located Availability and Pricing slide, and strong CTA with QR code/URL that resolves.
---

# Deck Launch, a type pack for the `deck-builder` core

**Keep your process invisible.** Do not narrate the skill architecture (the "type pack" and "core" split) or announce which files you are reading. Skip preambles like "I'll start by reading...". Gather what you need, then build the deck.

This skill builds launch decks for product announcements and go-to-market moments. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, and learnings log. This file only declares what is launch-specific.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md`, the canonical 12-slide launch deck spine
- `visual-components.md`, per-slide brand-native patterns
- `demo-patterns.md`, static-screenshot recipes for the Slide 5 demo slot

**Declarations the brief locks in for launch builds**:
- `deck_type: launch`
- Target slide count: 12
- Catalog directory ($CATALOG): user-declared in the brief
- Forbidden class-name leaks: (none)
- Demo: Slide 5 ships as a static product screenshot

---

## What this type pack inherits from `deck-builder` core

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn. 3 reviewer gates (Brand, Copy, Layout).

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`. Fill in `deck_type: launch` plus the other launch-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell, 1440x810 canvas scale, and inline-edit module
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol plus logo safety plus nested-subpath rule
- `deck-builder/references/style-presets.md`, named aesthetic presets for Mode B users without a brand

### Auto-preview (turn 1, before the full build)

Before writing the full deck, generate 3 first-slide HTML previews based on the user's content. Do not ask the user how to choose a style. Just generate three distinct visual directions (one safe preset, one bold preset, one wildcard from `style-presets.md`), save them to a `.skill-temp/` folder, and open all 3 in the user's browser. Then ask "Which style do you want? A, B, C, or mix elements?"

Only after the user picks does the full Phase 2 build begin.

**Autonomous run exception**: for autonomous runs without a user browser to open previews in, skip the visual preview step. Instead, document the preset choice (palette, typography, character) as a code block in the brief and proceed directly to full build. The user can iterate on the preset post-build via the inline-edit module if needed.

**Phase 3 reviewer specs** (in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

**Phase 3 reviewer support** (in `deck-builder/references/`):
- `brand-authenticity.md`, `rendering-checks.md`, `typography-scale.md`, `mechanical-checks.md`

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared. Filter by `Deck type = launch`).

---

## Output expectations (launch-specific)

Phase 4 deliverable:

1. The `.html` file at `<CATALOG_DIR><Product>-Deck.html`
2. The brief alongside it: `<Product>-Brief.md`
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it)
4. A one-paragraph design and content summary
5. The compact audit report (3 reviewers, one line each)

Do not write walls of explanation. The file is the deliverable.

---

## Hard rules specific to launch decks

- **Slide 5 is the demo slot.** In OSS it ships as a high-quality static product screenshot with a small **"Powered by FluidDocs" attribution mark** in the bottom-right (FluidDocs logo as inline SVG, opacity ~0.7, linking to fluiddocs.ai). Reviewers verify the screenshot is real and recognizable, not a placeholder. No upsell appears in the deck output.
- **Availability and Pricing are co-located.** Same slide or adjacent slides (never buried after slide 8).
- **The CTA slide (Slide 12) has a QR code or URL that actually resolves.** Reviewers will test it. A broken link is a failing review.
- **No unsourced claims.** Early Customers slide (Slide 8) names real customers or shows real logos, never placeholder/generic testimonials.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
