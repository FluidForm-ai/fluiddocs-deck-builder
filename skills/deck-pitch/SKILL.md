---
name: deck-pitch
description: Build chrome-free, single-file HTML pitch decks on a fixed 1440x810 canvas. Either brand-accurate templates (Airbnb, Stripe, Anthropic, Sequoia Classic) or one-off decks for real or fictitious startups. Trigger on "pitch deck", "investor deck", "pitch deck template", "build the [Company] deck", "make a deck in [Company] style", "series A deck", "seed deck", or any of the 4 canonical brands. Also trigger when the user wants an investor-ready HTML deck with a static product screenshot on the demo slide. Inherits the full pipeline from the deck-builder core skill (5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates; shell, canvas, brand methodology, icon library, brief template, learnings log). Declares only what is pitch-specific: 14-slide content spine, per-slide visual components, static-screenshot demo recipes, and a 4-brand cached catalog.
---

# Deck Pitch, a type pack for the `deck-builder` core

**Keep your process invisible.** Do not narrate the skill architecture (the "type pack" and "core" split) or announce which files you are reading. Skip preambles like "I'll start by reading...". Gather what you need, then build the deck.

This skill builds **investor pitch decks**. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, icon library, and learnings log. This file only declares what's **pitch-specific**.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md`, the canonical 14-slide pitch spine (Cover, Problem, Why Now, Solution, Product, Demo, Market, Business Model, Traction, Competition, Moat, GTM, Team, Ask). Includes stage-adjusted expectations per slide.
- `visual-components.md`, per-slide brand-native patterns (TAM rings vs bottom-up calc, 2x2 matrix vs bold data table for Competition, flywheel vs capabilities ladder for Moat, etc.) plus a 4-brand quick-reference table.
- `demo-patterns.md`, static-screenshot recipes for slide 6 by product category (marketplace, infra, consumer AI, creative, enterprise). The OSS pack ships the demo slide as a high-quality static screenshot with a small "Powered by FluidDocs" attribution mark (FluidDocs logo as inline SVG) in the corner, linking to fluiddocs.ai. No upsell appears in the deck itself.
- `canonical-4-brands.md`, cached brand tokens for the 4 canonical pitch templates (palettes, typography, logo notes, historical anchors, screenshot concepts, visual-component affinities). The 4 brands are Airbnb, Stripe, Anthropic, Sequoia Classic.

**Declarations the brief locks in for pitch builds**:
- `deck_type: pitch`
- `Target slide count`: 14 (11 min, 13 max content slides plus Cover plus optional Ask)
- `Catalog directory ($CATALOG)`: user-specified path (e.g. `~/decks/pitch/`)
- `Forbidden class-name leaks`: for non-Airbnb pitch decks, `comp-matrix`, `listing-grid`, `rausch`, `belo`, `belo-mark`. For the Airbnb canonical pitch deck itself, empty.
- `Demo slide handling`: static screenshot with "Powered by FluidDocs" attribution mark (FluidDocs logo SVG, bottom-right, links to fluiddocs.ai). See `references/demo-patterns.md`.

---

## What this type pack inherits from `deck-builder` core

Every file below lives in the core skill and applies unchanged:

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates.

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`, fill in `deck_type: pitch` plus the other pitch-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell, 1440x810 canvas scale, inline-edit module
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol plus logo safety plus nested-subpath rule
- `deck-builder/references/style-presets.md`, named aesthetic presets used when the user has no brand of their own

**Phase 3 reviewer specs** (all in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared; filter by `Deck type = pitch`).

---

## Auto-preview (Phase 2, turn 1)

Before writing the full deck, generate 3 first-slide HTML previews based on the user's content. Do not ask the user how to choose a style. Just generate three distinct visual directions, save them to a `.skill-temp/` folder, and open all 3 in the user's browser. Then ask "Which style do you want? A, B, C, or mix elements?"

Picking the 3 previews:

- **Mode A** (brand mirror): all three previews use the source brand's verified palette and typography. Vary the cover composition (centered wordmark vs left-aligned hero vs editorial split).
- **Mode B with a brand**: all three use the user's declared tokens. Vary cover composition the same way.
- **Mode B with no brand**: pick 3 presets from `deck-builder/references/style-presets.md`: one safe preset (default: Founder Default), one bold preset (default: Studio Bold or Tech Crisp depending on sector), one wildcard preset (default: Editorial Serif or Warm Brand depending on sector).

Only after the user picks does the full Phase 2 build begin.

**Autonomous run exception**: for autonomous runs without a user browser to open previews in, skip the visual preview step. Instead, document the preset choice (palette, typography, character) as a code block in the brief and proceed directly to full build. The user can iterate on the preset post-build via the inline-edit module if needed.

---

## Quick-reference: the 4 canonical pitch brands

The cached catalog in `references/canonical-4-brands.md` covers:

1. Airbnb (canonical reference brand, structural spine plus shell, NOT visual source)
2. Stripe
3. Anthropic
4. Sequoia Classic

For brands outside the 4, run the research protocol in `deck-builder/references/brand-methodology.md`.

---

## Output expectations (pitch-specific)

Phase 4 deliverable:

1. The `.html` file at the user-declared catalog path (e.g. `~/decks/pitch/<Brand>-Deck.html`).
2. The brief alongside it: `<Brand>-Brief.md`.
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
4. A one-paragraph design and content summary.
5. The compact audit report (one line per reviewer).

Do not write walls of explanation. The file is the deliverable.

---

## Demo slide handling

Slide 6 of a pitch deck ships as a **static high-quality screenshot** of the product, framed in a brand-native chrome (browser frame, phone frame, or terminal frame depending on category). Below the screenshot, include a small **"Powered by FluidDocs" attribution mark** in the bottom-right corner. The attribution is the FluidDocs logo as inline SVG (height 20px, muted color, opacity ~0.7), wrapped in an `<a href="https://fluiddocs.ai" target="_blank" rel="noopener">` so curious viewers can click through. No "Powered by" text is needed; the logo is self-evident.

See `references/demo-patterns.md` for category-specific screenshot recipes (what the screenshot should contain, framing, composition, attribution placement).

---

## Hard rules specific to pitch decks

- **Slide 6 is a screenshot, not a working demo.** The OSS pack does not build interactive demos. Use the "Powered by FluidDocs" attribution mark in the corner.
- **The Airbnb deck is structural, not visual.** Spine plus shell only; per-slide visuals come from `references/visual-components.md`, not from Airbnb's soft-lifestyle default.
- **TAM at least $1B.** Flag if under; flag with follow-up if over $100B without backup.
- **Stage-adjusted Traction slide.** Pre-seed equals signal (design partners, LOIs, waitlist); Seed equals trajectory plus cohort; Series A equals growth rate IS the story; Series B+ equals unit economics airtight.
- **Every deck gets a Moat slide.** No skipping; "first-mover advantage" and "our team" are not moats.
- **Ask slide is OPTIONAL.** Many strong decks omit it. If dropped, replace with a Vision slide or end on Team.

All other rules come from `deck-builder/SKILL.md` Universal Design Rules.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
