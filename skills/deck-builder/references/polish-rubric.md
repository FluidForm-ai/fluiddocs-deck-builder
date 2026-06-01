# Polish Rubric, Deeper-Dive Reference

> **Note**: In the OSS pack, the active Phase 3 reviewers are Brand, Copy, and Layout. Polish is NOT a separate reviewer; this rubric is kept as a deeper-dive reference. The Layout Reviewer may invoke it when looking for the "one slide that ships less polished than the rest" pattern.

**Category covered**: polish unevenness, the "slide 4 problem."

Goal: catch the pattern where 9 to 10 slides ship polished and 4 to 5 ship unpolished. The Demo slide always gets attention; Moat, Why-Now, and Competition routinely ship worse. This rubric ensures every slide clears the deck's median.

This is the most subjective check. The rubric needs to be sharp enough that two independent passes would agree.

---

## Inputs

- The final `.html` rendered in a browser (view one slide at a time).
- The brief section 6 (per-slide visual-component picks, the intended design).

---

## The per-slide scoring rubric

Each slide scores 1 to 5 on five dimensions. Target: every slide >= 3.5 average, and every slide >= deck median, 1.

### Dimension 1: Visual density

Is the slide using its content area well, not empty, not crammed?

- **1, Empty**: huge blank zones, content clustered in one corner, feels like a draft.
- **2, Sparse**: content present but underutilized; slide feels like it's waiting to be filled.
- **3, Balanced**: content uses the content area proportionally; some breathing room but no void.
- **4, Rich**: multiple hierarchies working together, secondary elements support the primary.
- **5, Dense and legible**: high info-per-slide while still readable at a glance, the Airbnb listings grid, the Stripe API-doc split.

Target: every slide >=3.

### Dimension 2: Element alignment

Is everything on a grid, or do things feel randomly placed?

- **1, Chaos**: nothing aligns; each element on its own coordinate system.
- **2, Drift**: roughly aligned but with visible off-by-pixel offsets on cards, icons, spacing.
- **3, Mostly aligned**: consistent gutters, consistent card widths, consistent top-alignment of cards in a row.
- **4, Precise**: grid system visible; cards align across rows; baselines align where text shares a line.
- **5, Invisible grid**: everything clearly on a system without looking like it, the viewer feels calm without knowing why.

Target: every slide >=3.

### Dimension 3: Hero moment

Does the slide have something memorable? A single thing the viewer will remember?

- **1, Prose wall**: paragraph-only, no visual anchor.
- **2, Titled list**: an `h2` and some bullets. Functional but forgettable.
- **3, Structured**: a chart, table, or card grid, readable but not striking.
- **4, Anchored**: one element the eye lands on first, a big stat, a chart, a quote, a visual that tells the story.
- **5, Signature**: the slide has a memorable signature move, Airbnb's listings carousel, Stripe's live API response, ElevenLabs' waveform.

Target: every content slide >=3. Demo/Traction/Market typically >=4.

### Dimension 4: Craft-level

The small-details bar. Do the icons match? Do buttons have hover states? Do card shadows match? Do the corners have the right radius for this brand?

- **1, Rough**: icons mismatched in stroke weight, buttons inconsistent, random corner radii.
- **2, Uneven**: mostly consistent but clear exceptions on some elements.
- **3, Clean**: consistent icon stroke, consistent buttons, consistent radii.
- **4, Considered**: hover states where expected, subtle animations where they serve, brand-specific small details (Airbnb's pill shapes, Stripe's subtle gradients, Sequoia's serif pulls).
- **5, Finished**: every small detail looks like the brand's in-house team shipped it.

Target: every slide >=3.

### Dimension 5: Brand fidelity (per slide)

Does this specific slide feel like the source brand? Not "the deck", this slide.

- **1, Brand-free**: could be any brand; generic.
- **2, Palette-only**: uses brand colors but structure is generic.
- **3, Structured brand**: uses brand colors + brand-appropriate components.
- **4, Voice**: brand-appropriate tone in copy + brand-appropriate visual structure.
- **5, Unmistakable**: this slide could not be any other brand.

Target: every slide >=3. Cover + Team usually >=4.

---

## Aggregation + flagging logic

For each slide: mean of the 5 dimensions = slide polish score.

- **Deck median**: median of all slide polish scores.
- **Any slide < median, 1** : flag.
- **Any slide < 3.0 on any single dimension** : flag (regardless of median).
- **The Slide 4 / Moat / Why-Now / Competition quartet gets extra scrutiny**, historically the weakest across the catalog. If any of these scores equal to or below median, still note in the report (not a fail, but a watch flag).

---

## The "less polished than the rest" pattern

This is the specific bug this rubric exists to catch. Look for:

- One slide with a simpler visual component than its neighbors (bullet list next to data-rich slides).
- One slide with plainer typography (default-weight `h2` next to neighbors with letter-spacing + weight polish).
- One slide with fewer hierarchies (flat body text next to multi-tier content).
- One slide missing a "finishing touch" (no footnote, no data source, no small caption, where others have them).

If you notice a slide as "the plain one" when clicking through, the median flag should catch it mechanically.

---

## Pass/fail report format

```
Polish (deep-dive): PASS / FAIL

Deck median polish: 3.8

Slide-by-slide scores (density / alignment / hero / craft / brand):

 1. Cover         5/5/5/4/5 = 4.8
 2. Problem       4/4/3/4/4 = 3.8
 3. Why Now       3/3/2/3/3 = 2.8  <- FLAG (below median, 1; hero dim < 3)
 4. Solution      4/4/4/4/4 = 4.0
 5. Product       4/4/4/4/4 = 4.0
 6. Demo          5/5/5/5/5 = 5.0
 7. Market        4/4/4/3/4 = 3.8
 8. Business      3/4/3/3/3 = 3.2  <- WATCH (at median, 0.6)
 9. Traction      4/4/4/4/4 = 4.0
10. Competition   4/4/4/3/4 = 3.8
11. Moat          3/3/3/3/3 = 3.0  <- FLAG (below median, 1)
12. GTM           4/4/4/4/4 = 4.0
13. Team          4/4/4/4/4 = 4.0
14. Ask           4/4/3/3/4 = 3.6

Flags:
- Slide 3 (Why Now) is materially below the deck, prose-only, no visual anchor. Add a single "from X to Y" chart or an era-shift callout.
- Slide 11 (Moat) uses plain card grid where other slides have richer hierarchies. Add a flywheel or a "per-X metric" treatment.

Watches:
- Slide 8 (Business Model) is near median, no flag, but could use a hero moment.
```

---

## Extending this rubric

This is the most subjective check, so:

1. Every user "slide X feels unpolished" comment goes in `learnings-log.md` under the polish category.
2. Over time, build up per-brand polish reference, what a 5-on-craft looks like for Airbnb vs Uber vs Stripe.
3. If a dimension consistently fails to catch real issues, refine its rubric here. The goal is calibration such that two independent passes would give within +/-0.5 on each slide.

When the catalog is large enough (>=12 decks), do a retrospective: for every deck the user flagged as "slide X is less polished," does this rubric reproduce that flag? If not, tighten.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
