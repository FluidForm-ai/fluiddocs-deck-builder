# Build Brief Template (Phase 1 artifact)

Fill this in before any HTML is written. Save as `<Brand>-Brief.md` next to where the deck will live. Get explicit user approval before proceeding to Phase 2.

Every reviewer in Phase 3 diffs the shipped deck against this brief. The brief is the single source of truth.

---

## Template

Copy everything below the line into the brief file and fill in.

---

```markdown
# <Brand> Deck, Build Brief

**Deck type**: pitch / sales / launch / keynote / all-hands
**Mode**: A (real-brand template) / B (fictitious or real-startup deck)
**Status**: Draft / Approved / In Build / In Review / Released
**Author**: [you]
**User approver**: [user]
**Date**: YYYY-MM-DD
**Target slide count**: [integer, e.g., 14 for pitch, 11 for sales, 28 for keynote]
**Catalog directory ($CATALOG)**: [path to the directory where decks of this type are shipped]
**Forbidden class-name leaks**: list one class name per line between the explicit HTML-comment anchors below. The mechanical-check extractor reads exactly what sits between these anchors, so leave them in place even when the list is empty. For a deck that IS the canonical reference (e.g., an actual Airbnb pitch deck) or for deck types with no canonical-brand catalog, leave the block empty (anchors only, no class names).

```
<!-- BEGIN forbidden-class-leaks -->
comp-matrix
listing-grid
rausch
belo
belo-mark
<!-- END forbidden-class-leaks -->
```

## 0. Deck type context (drives which type pack's references apply)

The chosen deck type determines:
- Which type pack's `content-spine.md` the build follows
- Which type pack's `visual-components.md` supplies per-slide patterns
- Whether `demo-patterns.md` applies (pitch, launch typically yes; others typically no)
- Which `$CATALOG` directory reviewers compare against

Installed type packs ship as their own skills (e.g. `deck-pitch`, `deck-sales`, `deck-launch`, `deck-keynote`, `deck-all-hands`).

## 1. Company basics

- **Name**: ____
- **One-line positioning**: We [verb] [specific thing] for [specific audience].
- **Stage**: Pre-seed / Seed / Series A / B+
- **Sector**: [marketplace / infra / consumer AI / enterprise SaaS / creative tool / fintech / ...]
- **Primary product**: [the thing the demo will show]

## 2. Era + historical anchor (Mode A only)

- **Era being depicted**: YYYY (e.g., "UberCab 2010 seed")
- **Founders of that era**: names + one-line backgrounds
- **Competitors of that era**: list (must not include post-era entrants)
- **Business-model terms of the era**: take rate, pricing, contract shape
- **Raise size norms of the era**: seed range, Series A range
- **Platform assumptions of the era**: iPhone generation, web baseline, cloud baseline
- **Known era risks**: [iPhone 6 on a 2009 deck = bug, list gotchas]

For Mode A, this section must be source-researched in Phase 1. `brand-tokens.md` anchors are a starting point, not a ceiling.

## 3. Founder intake (Mode B only)

- **Founders**: names + backgrounds + why-this-team-wins-this-problem (one sentence each)
- **Tone**: actual investor pitch / illustrative-fictional / portfolio piece / teaching material
- **Problem**: 3 concrete user pains
- **Why now**: the shift that makes this possible now
- **Traction inputs**: real numbers if they exist; otherwise `[REPLACE]` placement plan
- **Ask**: raise amount + use of funds (or `[REPLACE]`)

## 4. Brand tokens (source-verified)

- **Mode A**: re-fetched from ____ (URL) on ____ (date). Cached entry in `brand-tokens.md` matches / does-not-match (if mismatch, flag what).
- **Mode B**: approach = archetype-mirror / custom-palette / full-custom. Archetype (if used) = ____.

**Palette**
- Primary: `#______`
- Surface (light/dark default): `#______`
- Ink: `#______`
- Muted: `#______`
- Accent (optional): `#______`
- Border/divider: `#______`

**Typography**
- Display: ____ (Google Font or stand-in: ____)
- Body: ____ (stand-in: ____)
- Mono (if used): ____

**Logo approach**
- Cover wordmark: inline SVG from brand press kit / custom `<text>`-in-`<rect>` / user-provided asset
- Corner brand-mark: monogram / wordmark-small / `<text>`-in-`<rect>` fallback

## 5. Typographic scale (locked)

Declare every `font-size` value this deck is allowed to use. Every `font-size` in the final CSS must match one of these. Target: 5 to 7 distinct values, not more.

Example:
- 10px · slide-meta / monospace counters
- 11px · footnotes
- 13.5px · card body text
- 15.5px · lead paragraphs
- 19px · section heads / `h3`
- 26px · slide `h2`
- 38px · cover / hero stat

Fill in for this deck:
- ____px · [role]
- ____px · [role]
- ____px · [role]
- ____px · [role]
- ____px · [role]
- ____px · [role]
- ____px · [role]

**Minimums**: body text >=14px, card body >=13.5px, legible metrics >=22px. Exceptions must be justified.

## 6. Per-slide visual component picks

The spine comes from the chosen type pack's `content-spine.md`. For each slide in that spine, name the pattern from the type pack's `visual-components.md` and a one-line rationale.

| # | Slide (from type pack's content-spine.md) | Chosen component (from type pack's visual-components.md) | Rationale |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| ... | | | |

Example rows for a **deck-pitch** build (14-slide spine):

| # | Slide | Chosen component | Rationale |
|---|---|---|---|
| 1 | Cover | (wordmark hero style) | |
| 2 | Problem | 3-card / narrative+stat / before-after | |
| 3 | Why Now | 3 shifts row / single unlock curve | |
| 4 | Solution | (describe) | |
| 5 | Product | (describe) | |
| 6 | Demo | (category from demo-patterns.md) | |
| 7 | Market | TAM rings / bottom-up calc / Sankey / big-number | |
| 8 | Business Model | (describe) | |
| 9 | Traction | growth curve / weekly bars / logo grid+NRR / quiet-confidence | |
| 10 | Competition | 2x2 matrix / bold data table / feature bars / radar / narrative stack | |
| 11 | Moat | 4-card+flywheel / depth bars / capabilities ladder / narrative | |
| 12 | GTM | city rail / motion grid / channel bars / wedge narrative | |
| 13 | Team | 3-founder / 3+key-hires / 2-founder hero / narrative memo | |
| 14 | Ask | (describe) | |

For sales, launch, keynote, all-hands, consult the corresponding type pack's `content-spine.md` for the slide list.

## 7. Demo concept

For deck types where a working interactive demo is canonical (pitch, launch):
- **Category**: marketplace / infra / consumer AI / creative / enterprise (from the type pack's `demo-patterns.md`)
- **Screenshot or interaction surface**: in the OSS pack, the demo slide is typically a high-quality static screenshot. Note what the screenshot must show.
- **Optional**: link to a hosted live demo (`href` from the slide) if available.

For deck types without an interactive demo (all-hands, etc.):
- **Demo**: N/A, no demo slide for this deck type.

## 8. Height budget per slide

Declare, at each target viewport, the content-area height each slide is allowed to consume. Numbers, not prose.

Slide viewport targets: 1440x720, 1440x800, 1440x900 (default). Content area = viewport, (header zone 104px + footer zone 96px) = 520 / 600 / 700 px.

| # | Slide | 720p budget | 800p budget | 900p budget | Known overflow risks |
|---|---|---|---|---|---|
| 1 | Cover | 520 | 600 | 700 | , |
| 2 | Problem | 460 | 540 | 640 | icon + 2-line bodies |
| 3 | Why Now | | | | |
| ... | ... | | | | |

Any slide projected >90% of its budget in Phase 3, flag.

## 9. Known risks for THIS build

- Era gotchas: ____
- Brand gotchas (e.g., light-brand / dark-product split, neon that isn't really in the palette): ____
- Cross-deck sameness risk: how many of the last 5 builds used these same components? ____

## 10. Approval

- [ ] User reviewed
- [ ] User approved
- Date approved: ____

No HTML gets written until this line has a date.

---
```

---

## Using the brief in Phase 3

In the OSS pack there are 3 active reviewers in Phase 3 (Brand, Copy, Layout). Each diffs the shipped deck against this brief:

- **Brand Reviewer** checks sections 2, 3, 4 (era / founder intake / tokens) and section 6 (component picks for brand-voice fit).
- **Copy Reviewer** checks sections 1, 2, 3 for narrative consistency, no unresolved `[REPLACE]` markers beyond what the brief sanctions, and tone alignment.
- **Layout Reviewer** checks sections 5 (font-sizes match scale), 6 (declared component shipped), 8 (height budget respected), and runs mechanical checks (forbidden class-name leaks, file size, section count matches target).

If a shipped deck diverges from its brief, the divergence is the bug, not the brief.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
