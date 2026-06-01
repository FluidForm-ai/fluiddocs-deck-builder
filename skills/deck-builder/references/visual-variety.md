# Visual Variety, Deeper-Dive Reference

> **Note**: In the OSS pack, the active Phase 3 reviewers are Brand, Copy, and Layout. Visual Variety is NOT a separate reviewer; it is kept here as a deeper-dive reference that the Brand Reviewer can consult when checking for cross-deck sameness or canonical-reference-brand leakage.

**Category covered**: visual rigidity, type-pack-canonical-brand-ism + cross-deck sameness.

Goal: catch "every deck feels like [the type pack's canonical reference brand] with different colors." Also catch the subtler pattern where the catalog homogenizes over time, every recent deck uses the same pattern for the same slide category, even though that pattern doesn't fit every brand.

This is the discipline that keeps the 13th through 50th decks visually distinctive, per deck type.

**Generalization note for non-pitch type packs.** The examples and seed matrix below are drawn from the pitch deck pack, where **Airbnb** is the canonical reference brand, so "Airbnb-ism" is shorthand for "patterns copied from the type pack's reference brand that shouldn't leak into non-reference decks." Other type packs substitute their own canonical reference:

| Type pack | Canonical reference brand (if applicable) | "-ism" to catch |
|---|---|---|
| deck-pitch | Airbnb | Airbnb-ism (2x2 matrix, flywheel, TAM rings, motion grid) |
| deck-sales | (tbd) | , |
| deck-launch | (tbd) | , |
| deck-keynote | Duarte / Apple-lineage (reference) | keynote-ism |
| deck-all-hands | (tbd) | , |

The cross-deck comparison matrix below is the PITCH type pack's matrix. Each type pack maintains its own matrix inside its own `visual-components.md` or a `visual-variety-matrix.md` file; the Brand Reviewer reads both this file (for the method) and the type pack's matrix (for the cross-deck comparison data) when running variety checks.

---

## Inputs

- The shipped `.html` file (`$DECK`)
- The brief (`$BRIEF` section 6, per-slide visual-component picks)
- The directory of previously shipped decks for this type (`$CATALOG`, declared in the brief, each type pack sets its own catalog directory)

---

## The cross-deck comparison matrix

Maintained in this file. Updated on every build. Each row is a deck; each column is a slide-component slot.

Seed state example (after a small set of pitch builds):

| Deck        | Problem       | Why Now       | Competition    | Moat                | GTM              | Market         | Traction         | Team            |
|-------------|---------------|---------------|----------------|---------------------|------------------|----------------|------------------|-----------------|
| Airbnb      | 3-card        | 3 shifts row  | 2x2 matrix     | 4-card + flywheel   | motion grid      | TAM rings      | growth curve     | 3-founder grid  |
| Uber        | 3-card        | 3 shifts row  | bold data table| 4-card + dark flywheel | city rail     | TAM rings (crescent-fix) | weekly bars | 3 + key-hires strip |
| Stripe      | TBD           | TBD           | TBD            | TBD                 | TBD              | TBD            | TBD              | TBD             |
| Anthropic   | TBD           | TBD           | TBD            | TBD                 | TBD              | TBD            | TBD              | TBD             |
| Sequoia     | TBD           | TBD           | TBD            | TBD                 | TBD              | TBD            | TBD              | TBD             |

After each build, fill in that deck's row. This matrix is the variety check's primary input.

---

## Checks

### 1. Brief declaration matches shipped

For each slide, verify the component actually shipped matches what the brief declared. Class names + visual structure should match `visual-components.md` for the declared pattern.

Fail if the shipped component differs from the brief without the brief being updated.

### 2. Canonical-reference-brand-ism leakage (non-reference decks only)

Same as Layout / Mechanical Reviewer check, but variety re-runs it because it's a visual issue, not just a code-pattern issue.

```bash
grep -nE "(comp-matrix|listing-grid|rausch|bélo|2x2-matrix)" "$DECK"
```

Also visual-structural grep, the Airbnb flywheel has a distinctive class pattern. If a non-Airbnb deck reproduces it exactly, flag.

### 3. Cross-deck sameness threshold

For each slide slot:

- Count how many of the **other** shipped decks use the same component pattern as this deck.
- If >=3 other decks use this pattern, flag the slide as "over-used."

Example: if Uber, OpenAI, Anthropic already used "capabilities ladder" for Moat, and now the new Perplexity deck also picks "capabilities ladder," that's the 4th use, flag and ask if another pattern better fits Perplexity's voice.

This prevents catalog homogenization.

### 4. Brand voice vs component fit

Cross-check each slide's picked component against the brand's design voice in `brand-tokens.md` "Visual component affinity" section.

Example: Airbnb picking a bold dark data table for Competition doesn't fit Airbnb's soft lifestyle voice, the 2x2 matrix does. If the brief declares a mismatched component, flag.

### 5. Shell + cover "feel like this specific brand"

This is the most subjective check. Open the deck. Does slide 1 immediately read as the source brand? Or could it be any brand from the catalog?

Signals it's NOT brand-native enough:
- Cover uses generic Inter + soft gradient regardless of brand
- Progress line is the brand color but everything else is the reference shell palette
- Brand-mark top-left is a generic square with a letter, when the brand has a real recognizable mark available

Fail if the deck could be mistaken for another brand's deck at a glance.

---

## Maintaining the matrix

Every build, after Phase 4 release:

1. Add this deck's row to the matrix above.
2. Compute the current "over-used" patterns (>=4 decks in the catalog using it).
3. Add those to a "watch list" at the bottom of this file, next builds should actively consider alternatives.

### Current watch list (patterns to avoid defaulting to)

*Empty at seed. Fill in as catalog grows.*

---

## Pass/fail report format

```
Visual Variety (deep-dive): PASS / FAIL

[PASS] Brief declarations match shipped components (14/14 slides)
[PASS] No Airbnb-ism leakage (Perplexity deck)
[FAIL] Cross-deck sameness: Moat = "capabilities ladder", now the 4th deck in catalog to use this (Uber, OpenAI, Anthropic already do). Consider "narrative stack" or "depth bars" for Perplexity.
[PASS] Brand voice fit: all components align with Perplexity's teal editorial voice
[PASS] Shell feels Perplexity-native at a glance

Action: reconsider Moat slide. Propose replacement in a Phase 2 bounce.
```

---

## Extending this reference

Every user-flagged sameness issue gets logged in `learnings-log.md` under the brand-variety category and the matrix gets updated. If a brand-new pattern emerges that isn't in `visual-components.md`, add it there too.

When the catalog reaches 12 decks, the matrix is complete, at that point the "over-used" threshold should probably drop from >=3 to >=2, since there are so few degrees of freedom left.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
