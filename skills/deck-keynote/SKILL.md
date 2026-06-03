---
name: deck-keynote
description: Build narrative-driven, speaker-centric keynote decks (20-35 slides, default 28) for conference talks, TED-style presentations, and standalone speaker decks. Triggers, "keynote", "keynote deck", "conference talk", "TED-style talk", "speaker deck". Inherits full pipeline from deck-builder core; type-specific spine, visual patterns, and demo recipes defined here. Keynotes are the most elastic and visual of all deck types, every slide requires a visual anchor, one idea per slide, mandatory opening hook.
---

# Deck Keynote, a type pack for the `deck-builder` core

**Build silently.** Do not narrate the skill architecture (the "type pack" and "core" split) or announce which files you are reading. Skip preambles like "I'll start by reading...". Gather what you need, then build the deck.

This skill builds **conference keynotes, TED-style talks, and speaker-centric presentations**. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, and learnings log. This file only declares what's **keynote-specific**.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md`, the canonical 28-slide keynote spine (flexible 20-35 range)
- `visual-components.md`, per-slide visual pattern catalog, emphasizing imagery and large-type design
- `demo-patterns.md`, optional interactive demo recipes suited to live talks (kept as a visual reference; most keynotes ship without a demo slot)

**Declarations the brief locks in for keynote builds**:
- `deck_type: keynote`
- `Target slide count`: 28 (flexible 20-35)
- `Catalog directory ($CATALOG)`: user-specified output directory
- `Forbidden class-name leaks`: (empty)
- Demo: optional (off by default)
- Density mode: live-presentation by default; ask the user whether the deck is for a live talk (sparse, image-led, 45s/slide pacing) or for async reading (denser text, self-explanatory slides)

---

## Phase 1 intake (keynote-specific batched questions)

When the trigger fires, the agent runs Phase 1 from `deck-builder/SKILL.md`. In addition to the generic intake, ask these keynote-specific questions in a single batched message:

1. **Talk length**: how many minutes is the speaking slot? (Drives slide count: ~45 seconds per slide.)
2. **Density mode**: is this deck for a live presentation (sparse, image-led, speaker carries the words) or for async reading (denser text, the slides explain themselves without a speaker)? This drives type sizes, text-per-slide, and whether speaker notes are inline or hidden.
3. **Thesis in one sentence**: the single idea every slide must support.
4. **Demo**: does the talk include a live interactive demo moment? (Default: no.)
5. **Speaker brand tokens**: any existing speaker site, talk page, or brand kit to mirror?

Batch these into one message. Do not interrogate slide by slide.

---

## Phase 2 auto-preview (run on turn 1 of Phase 2)

Before writing the full deck, the agent must auto-generate 3 first-slide previews and let the user pick a direction. Do not ask the user how to choose a style; pick the 3 from `deck-builder/references/style-presets.md`:

1. **Safe preset**: a clean, conference-default cover (full-bleed photo + large title, dark text on light bg or vice versa).
2. **Bold preset**: a high-contrast bold-type cover (single thesis phrase at 240pt+, solid color background).
3. **Wildcard preset**: an unexpected aesthetic (asymmetric layout, oversized monogram, or an artistic visual that matches the speaker's brand if known).

Steps:

1. Write the 3 first-slide HTML previews to `.skill-temp/keynote-preview-{safe,bold,wildcard}.html`.
2. Open all 3 in the user's browser.
3. Ask, "Which style do you want? A, B, C, or mix elements from these?"
4. Only after the user picks does the full Phase 2 build begin.

**Autonomous run exception**: for autonomous runs without a user browser to open previews in, skip the visual preview step. Instead, document the preset choice (palette, typography, character) as a code block in the brief and proceed directly to full build. The user can iterate on the preset post-build via the inline-edit module if needed.

---

## What this type pack inherits from `deck-builder` core

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates.

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`, fill in `deck_type: keynote` plus the other keynote-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell + 1440×810 canvas scale + inline-edit module
- `deck-builder/references/style-presets.md`, the preset catalog used by the auto-preview step above
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol + logo safety + nested-subpath rule

**Phase 3 reviewer specs** (all in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared; filter by `Deck type = keynote`).

---

## Output expectations (keynote-specific)

Phase 4 deliverable:

1. The `.html` file at `<CATALOG_DIR>/<Speaker-Name>-Keynote.html` or user-specified path.
2. The brief alongside it: `<Speaker-Name>-Brief.md`.
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
4. A one-paragraph design/content summary.
5. The compact audit report (3 reviewers, one line each).

Do not write walls of explanation. The file is the deliverable.

---

## Hard rules specific to keynote decks

- **No slide is all text.** Every slide has a visual anchor, a full-bleed image, a chart, a single word at 120pt+, or a bold design element. Slides support the speaker; they do not substitute for the speaker.
- **One idea per slide.** Each slide carries one main thought, one story beat, or one data point. No slide is a paragraph; no slide lists five unrelated ideas.
- **Opening hook is mandatory.** Slide 2 (immediately after cover) must hook the audience with a story, a striking stat, or a provocative statement. Never start with "Hi, I'm X" or an agenda slide.
- **45 seconds per slide.** Keynote reads at a strict 45 seconds per slide. A 28-slide deck is a ~21-minute talk; a 20-slide deck is ~15 minutes; a 35-slide deck is ~26 minutes. Content and slide count must align with the intended talk length.
- **Density mode discipline.** If live-presentation mode, keep text minimal; if async-reading mode, slides must stand alone without a speaker. Do not mix modes within a single deck.
- **No emoji on any slide.** All decorative elements use the icon library (`deck-builder/references/icon-library.md`); emoji are forbidden.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
