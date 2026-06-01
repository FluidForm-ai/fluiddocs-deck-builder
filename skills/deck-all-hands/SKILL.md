---
name: deck-all-hands
description: "Builds 15-slide all-hands decks for company-wide team meetings with balance of wins and candor. Trigger phrases: all-hands deck, town hall deck, monthly all-hands, company-wide meeting, team meeting deck, all-hands presentation. Type-specific: celebration and candor balance (only-wins hides problems), company-appropriate financials (not board-level detail), Q&A placeholder (live meeting owns Q&A not slides). Inherits 5-phase pipeline from deck-builder core."
---

# Deck All-Hands, a type pack for the `deck-builder` core

This skill builds **15-slide all-hands decks for company-wide team meetings**. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, and learnings log. This file only declares what's **all-hands-specific**.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md`, the canonical 15-slide all-hands spine
- `visual-components.md`, per-slide brand-native patterns
- `demo-patterns.md`, light demo recipes for product updates (optional; single moments only)

**Declarations the brief locks in for all-hands builds**:
- `deck_type: all-hands`
- `Target slide count`: 15
- `Catalog directory ($CATALOG)`: declared in the build brief (a folder the user picks for shipped examples)
- `Forbidden class-name leaks`: (empty)
- Demo: optional

---

## What this type pack inherits from `deck-builder` core

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates (Brand, Copy, Layout).

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`, fill in `deck_type: all-hands` plus the other all-hands-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell + 1440x810 canvas scale + inline-edit module
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol + logo safety + nested-subpath rule
- `deck-builder/references/style-presets.md`, named aesthetic presets when the user has no brand

### Auto-preview (Phase 2, turn 1)

Before writing the full 15-slide deck, generate 3 first-slide HTML previews. Do not ask the user how to choose a style. Just generate three distinct visual directions (one safe preset, one bold preset, one wildcard from `deck-builder/references/style-presets.md`), save them to a `.skill-temp/` folder, and open all 3 in the user's browser. Then ask "Which style do you want? A, B, C, or mix elements?"

Only after the user picks does the full Phase 2 build begin. The pattern matches the UX bar of a modern deck-builder skill. Show, don't ask.

**Autonomous run exception**: for autonomous runs without a user browser to open previews in, skip the visual preview step. Instead, document the preset choice (palette, typography, character) as a code block in the brief and proceed directly to full build. The user can iterate on the preset post-build via the inline-edit module if needed.

**Phase 3 reviewer specs** (all in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared; filter by `Deck type = all-hands`).

---

## Output expectations (all-hands-specific)

Phase 4 deliverable:

1. The `.html` file at `<CATALOG_DIR><Company>-Deck.html`.
2. The brief alongside it: `<Company>-Brief.md`.
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
4. A one-paragraph design/content summary.
5. The compact audit report (3 reviewers, one line each).

Do not write walls of explanation. The file is the deliverable.

---

## Hard rules specific to all-hands decks

- **Balance of celebration and candor.** An all-hands with only wins signals hiding something. Include at least one learning, challenge, or honest retrospective slide.
- **Financial slides stay appropriate for the audience.** Company-wide numbers (ARR, headcount, burn) only, never board-level detail (detailed P&L, cap table, sensitive unit economics).
- **Q&A slide is placeholder.** Slide 14 kickstarts the conversation. The live meeting is where Q&A happens, not the deck. Keep questions short and focus on engagement, not exhaustive slide coverage.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
