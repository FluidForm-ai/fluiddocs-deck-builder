# Learnings Log · Phase 5 permanent record

> Public OSS log. Entries are sanitized; specific customer or internal references have been removed.

This is the running record of every user-reported issue post-delivery and every check that was added in response. The skill gets measurably smarter per build because every correction turns into a permanent mechanical or editorial check that the next deck can't regress on.

**Invariant**: one line per issue, per fix. Never edit or delete past entries, only append. If a rule is later refined, add a new entry referencing the earlier one.

---

## Format

```
| Date       | Deck type | Build   | Category | Issue                          | Owner(s)           | Check added / rule updated                        |
|------------|-----------|---------|----------|--------------------------------|--------------------|---------------------------------------------------|
| YYYY-MM-DD | <type>    | <deck>  | #N       | <one-line description>         | <reviewer name>    | <file#check or rule added, with where it lives>   |
```

The **Deck type** column is the brief's declared `deck_type` (pitch, sales, launch, keynote, all-hands). This lets retrospectives filter by type ("which categories trip up keynote decks most?"). Meta/process entries use `(process)` for the build column and leave the deck type as `(all)`.

Categories (from SKILL.md):
1. Brand authenticity drift
2. Content shallowness (thin argument, obvious VC-speak, vacuous claims)
3. Visual rigidity / cross-deck sameness
4. Typography scale drift (within-deck + cross-catalog)
5. Polish unevenness (the "slide 4 problem")
6. Cheapness tells (emojis, fake brand-letter SVGs, cartoonish illustrations)
7. Code failures (script parse, missing DOM targets, broken nav)
8. Era accuracy / scope drift on historical decks

---

## Seed entries (carried over from pre-v4b catalog)

These are issues caught and resolved in early shipped decks. They're logged here so the checks stay discoverable; the checks themselves are already wired into the Phase 3 reviewer specs.

| Date       | Deck type | Build     | Category | Issue                                                     | Owner(s)               | Check added / rule updated                                                      |
|------------|-----------|-----------|----------|-----------------------------------------------------------|------------------------|---------------------------------------------------------------------------------|
| 2026-03-xx | pitch     | Sequoia   | #7       | `\'` escape inside single-quoted string literal broke nav | Mechanical Reviewer    | `mechanical-checks.md` #1 · `new Function()` parse on every `<script>` body     |
| 2026-03-xx | pitch     | Sequoia   | #4       | 18 distinct `font-size` values across 14 slides           | Typography Reviewer    | `typography-scale.md` #2 · distinct-size count ≤7; `mechanical-checks.md` #9    |
| 2026-04-xx | pitch     | ElevenLabs| #1       | Neon `#E6FF5E` / `#A3FF12` shipped; not in actual brand   | Brand Authenticity     | `brand-authenticity.md` #1 · diff `:root` hexes against brief section 4         |
| 2026-04-xx | pitch     | ElevenLabs| #6       | Logo rendered as "1E" or "II" instead of two equal bars   | Brand Authenticity     | `brand-authenticity.md` #3 · per-brand canonical logo shape list                |
| 2026-04-xx | pitch     | Uber      | #6       | "U" letter rendered as `⊐` bracket glyph                  | Brand Authenticity     | `brand-authenticity.md` #3 + `rendering-checks.md` #2                           |
| 2026-04-xx | pitch     | Uber      | #8       | Moat slide mentioned Kubernetes-style tech on 2010 deck   | Brand Authenticity     | `brand-authenticity.md` #4 · era-anachronism grep with per-era tech rules       |
| 2026-04-xx | pitch     | Airbnb    | #3       | Non-Airbnb decks reproducing `.comp-matrix` + `.listing-grid` class names | Visual Variety + Mechanical | `mechanical-checks.md` #3 + `visual-variety.md` #2 · brand-class leak grep |
| 2026-04-xx | pitch     | Airbnb    | #5       | Moat slide shipped a plain card grid while neighbors had richer hierarchies | Polish Reviewer | `polish-rubric.md` · deck-median flag; "slide 4 problem" pattern note           |

---

## v4b-era entries (this conversation forward)

| Date       | Deck type | Build   | Category | Issue                                                     | Owner(s)               | Check added / rule updated                                                      |
|------------|-----------|---------|----------|-----------------------------------------------------------|------------------------|---------------------------------------------------------------------------------|
| 2026-04-17 | (all)     | (pipeline) | (meta) | 11-step linear pipeline kept regressing on caught issues  | (skill architecture)   | Replaced with 5-phase gated pipeline + category-owning reviewers                |
| 2026-04-17 | pitch     | (pipeline) | #1, #8 | No separate mode for fictitious/real-startup decks       | (skill architecture)   | Introduced Mode A (real-brand template) vs Mode B (fictitious / real-startup)  |
| 2026-04-17 | (all)     | (pipeline) | (meta) | Brief was implicit, no single source of truth for Phase 2 | (skill architecture) | `build-brief-template.md` · Phase 1 artifact with approval gate                 |
| 2026-04-18 | (all)     | (pipeline) | (meta) | Decks were responsive, reflowed on mobile, lost PDF-like integrity | (skill architecture) | Fixed 1440×810 canvas universal rule; `shell-pattern.md` + `rendering-checks.md` #11 |
| 2026-04-18 | pitch     | Airbnb  | #6       | Bélo SVG rendered as blob with stump on right; missing `fill-rule="evenodd"` | Mechanical Reviewer | `mechanical-checks.md` · nested-subpath SVG brand mark must declare `fill-rule="evenodd"` |
| 2026-04-18 | pitch     | (multi) | #7       | Nav elements (`.brand-mark`, `.nav-counter`) placed outside `.deck` stayed fixed-size in letterbox bands while slide strip translated | Layout Reviewer | `shell-pattern.md` migration trap · all nav + slide-meta must live inside `.deck`, siblings of `.deck-strip` if Variant B |
| 2026-04-18 | pitch     | (multi) | #3       | Horizontal-scroll (`translateX`) variant was informal, undocumented, led to inconsistent migration patterns | Layout Reviewer | `shell-pattern.md` · Variant A (toggle) + Variant B (horizontal strip) both first-class, with explicit nav-placement constraints |
| 2026-04-21 | pitch     | (process) | (meta) | Critique pass scored Demo as nice-to-have; skill mandates demo presence on slide 6 | Reviewer panel | `SKILL.md` Phase 3 · demo slide recognized as first-class Evidence signal |
| 2026-04-21 | pitch     | (process) | (meta) | Ask slide was treated as required; many strong decks deliberately omit it | Reviewer panel | `content-spine.md` slide 14 marked OPTIONAL |
| 2026-04-21 | (all)     | (genericization) | (meta) | Original pitch-only skill hardcoded for pitch-deck shape, blocked use for other deck types | (skill architecture) | v4b · `deck-builder` core + thin type packs. Core parameterizes section count (§8), forbidden class-names (§3); brief adds `deck_type` + `Target slide count` + `Forbidden class-name leaks` + `Catalog directory` fields |
| 2026-04-22 | (any)     | (anon)  | #7       | Build subagent added `<div style="display: none">` block (~8.5KB) purely to pad file size past a byte-count floor | Mechanical Reviewer | `mechanical-checks.md` §11b · no inline hide tokens outside base `.slide` rule; HARD FAIL on any inline `display: none` / `visibility: hidden` / `opacity: 0` |
| 2026-04-22 | (any)     | (anon)  | #7       | Same hidden-filler pattern recurred · `<div style="display: none">` block (~15KB) used for byte-padding | Mechanical Reviewer | `mechanical-checks.md` §11b (reinforced); `build-a-type-pack.md` Hard Constraints section · anti-gaming rule is now part of every spine's hard constraints |
| 2026-04-22 | keynote   | (anon)  | #7       | A late slide shipped with `<section class="slide" style="justify-content: center;">` causing center-overflow hiding content under top brand-mark | Mechanical Reviewer | `mechanical-checks.md` §11c · grep for inline `justify-content: center` on `<section class="slide">`; HARD FAIL |
| 2026-04-22 | sales     | (anon)  | #4       | 13 distinct font sizes, no declared scale, 40KB file, hard-failed extensive test | Typography Reviewer | `build-a-type-pack.md` Hard Constraints · typography scale MUST be declared as leading CSS comment (`/* Typography scale (7 sizes): ... */`); mechanical-checks already enforced count ≤7 + scale match, but the declaration requirement was implicit |
| 2026-04-22 | (all)     | (process) | (meta) | Extensive type-pack tests surfaced three systemic build-agent gaming patterns | (skill architecture) | Four recipe updates landed: anti-gaming clause in `build-a-type-pack.md`, §11b + §11c in `mechanical-checks.md`, opacity-based slide-hiding as recommended shell pattern. |

---

## How to add an entry

After a user reports an issue in a shipped deck:

1. Classify the issue against the 8 categories above (or propose a new category if nothing fits, categories can grow, but additions are rare and require a SKILL.md update).
2. Identify the reviewer role that *should* have caught it. If no reviewer owns that category, that's the first signal that a new reviewer is needed.
3. Write the check that would have caught the issue. Commit the check to the owning reviewer's spec file.
4. Append one line to this file with the date, build name, category, issue summary, owner(s), and file/check reference.
5. If the check generalizes across brands (e.g., "any neon color absent from brief.section-4"), put it in the reviewer spec itself. If it's brand-specific (e.g., "Databricks red shifted from `#E53935` to `#FF3621`"), put it in `brand-tokens.md` and reference that row here.

Corollary: **a reviewer should never catch the same class of issue twice from the user.** First catch becomes a check; second catch is a Phase 2 regression.

---

## Retrospective cadence

Every 4 shipped decks, review this log:

- Which categories accumulated the most entries? That reviewer needs sharper rubrics.
- Which entries duplicate each other? Consolidate the rule.
- Which checks haven't fired in the last 4 builds? They're either working silently (good) or redundant with a tighter upstream rule (remove).
- Any issue that appears in 2+ builds is a sign the rule is too loose. Tighten.

At 12 shipped decks (the canonical catalog), do a full retrospective:

- For every deck the user flagged as "X was off," does the current Phase 3 suite reproduce the flag *without* the user pointing it out?
- If any flag isn't reproducible, the relevant reviewer's rubric is under-specified.

The goal at 12+ is that the 13th deck ships without the user having to teach us anything we've already been taught.

---

## Meta · what this file enables

The review suite is only as smart as the learnings logged here. Two operational commitments:

1. **Before Phase 3 of any new build**: skim the last 10 entries in this file. Confirm every relevant check is wired into a reviewer's spec.
2. **After Phase 5 of any new build**: append every user-reported issue from delivery, even minor ones, before closing out the build.

Without this loop, the skill stops compounding. With it, quality should trend asymptotically upward per build.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
