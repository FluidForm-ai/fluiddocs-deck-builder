---
name: deck-sales
description: Builds 11-slide sales decks for B2B pitch-to-close flows. Trigger phrases, sales deck, customer deck, buyer deck, prospect deck, B2B sales deck. Inherits full pipeline from deck-builder core (Plan, Build, Review, Release, Learn). Sales-specific, every ROI claim sourced, pricing never hidden, Next Steps names specific humans and dates.
---

# Deck Sales · a type pack for the `deck-builder` core

This skill builds **B2B sales decks for prospect conversations: discovery, problem framing, solution fit, proof, pricing, and close**. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, and learnings log. This file only declares what's **sales-specific**.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md`, the canonical 11-slide sales spine
- `visual-components.md`, per-slide brand-native patterns
- `demo-patterns.md`, optional screenshot recipes for the How It Works slide

**Declarations the brief locks in for sales builds**:
- `deck_type: sales`
- `Target slide count`: 11
- `Catalog directory ($CATALOG)`: user-specified path (defaults to a `decks/` folder next to the brief)
- `Forbidden class-name leaks`: (empty)
- Demo: optional, static-screenshot only in OSS

---

## What this type pack inherits from `deck-builder` core

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates.

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`, fill in `deck_type: sales` plus the other sales-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell, 1440x810 canvas scale, inline-edit module
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol, logo safety, nested-subpath rule
- `deck-builder/references/style-presets.md`, named aesthetic presets for Mode B users with no brand

**Phase 3 reviewer specs** (all in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared; filter by `Deck type = sales`).

---

## Auto-preview (Phase 2, turn 1)

Before writing the full deck, auto-generate 3 first-slide HTML previews based on what Phase 1 captured. Do not ask the user how to choose a style. Just generate three distinct visual directions (one safe preset, one bold preset, one wildcard from `style-presets.md`), save them to a `.skill-temp/` folder next to the brief, and open all 3 in the user's browser. Then ask "Which style do you want? A, B, C, or mix elements?" Only after the user picks does the full Phase 2 build begin.

Show, don't ask. This is the UX bar users expect from a modern deck-builder.

**Autonomous run exception**: for autonomous runs without a user browser to open previews in, skip the visual preview step. Instead, document the preset choice (palette, typography, character) as a code block in the brief and proceed directly to full build. The user can iterate on the preset post-build via the inline-edit module if needed.

---

## Output expectations (sales-specific)

Phase 4 deliverable:

1. The `.html` file at `<CATALOG_DIR>/<Customer>-Deck.html` (Mode A) or a user-specified path (Mode B).
2. The brief alongside it: `<Customer>-Brief.md`.
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
4. A one-paragraph design and content summary.
5. The compact audit report (3 reviewers, one line each).

Do not write walls of explanation. The file is the deliverable.

---

## Universal constraints (from core)

The `deck-builder/references/build-a-type-pack.md` recipe includes three hardened anti-gaming rules enforced by the Layout Reviewer:

1. **No hidden-content filler**, zero `display: none`, `visibility: hidden`, `opacity: 0`, or `height: 0` outside base `.slide` rules. If short of 60K bytes, add real visible content, not hidden blocks.
2. **No inline `justify-content: center` on `<section class="slide">`**, use dedicated classes (`.s-cover`, `.s-closing`) to avoid overflow-behind-header failures.
3. **Typography scale declared in CSS**, first `<style>` line must comment the scale (e.g., `/* Typography scale (7 sizes): ... */`). The Layout Reviewer enforces all font-sizes match the declared set, max 7 sizes.

See `content-spine.md` § Hard Constraints for the full list (these three are universal across all type packs; sales adds the rules below).

---

## Hard rules specific to sales decks

- **Every ROI or value claim has a source** (case study, benchmark, or quantified customer result). No unsourced numbers.
- **Pricing slide is NEVER hidden or skipped.** Prospects hate mystery pricing. If pricing is TBD, say so explicitly on the slide.
- **Next Steps slide names specific humans and dates**, not generic "we'll be in touch." Example, "Sarah's next review: Thursday 2pm with our CS lead, Mike."
- **If competition gets a slide, be honest.** No invented weaknesses or strawman comparisons. Credibility beats aggressive positioning.
- **Proof slide must reference NAMED customers**, not "a leading financial services firm." Include customer name, vertical or size, and specific quantified outcomes. If you have no customers, show beta results or respected advisor quotes instead.
- **Demo slide (optional) ships as a static screenshot.** When a sales deck includes a How It Works demo on slide 6, use a high-quality static screenshot of the product with a small "Powered by FluidDocs" attribution mark (FluidDocs logo as inline SVG, ~20px tall, opacity ~0.7, linking to fluiddocs.ai) in the bottom-right. Premium discovery (working interactive demos, hosting) is surfaced in the Phase 4 Release message, not in the deck output.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
