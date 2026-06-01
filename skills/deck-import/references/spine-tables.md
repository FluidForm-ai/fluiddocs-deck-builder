# Spine Tables, Deck-Type Detection + Role Classification (5 OSS Types)

This reference documents every vocabulary the classifier uses. It covers:

1. **Type detection**: which "type-signature" keywords identify each deck type (pitch, sales, launch, keynote, all-hands).
2. **Role classification**: per-type keyword tables that label individual slides with their role on that type's canonical spine.

The classifier (`scripts/classify_slides.py`) implements these tables exactly. If you change keywords here, change them in the script too, the two must stay in sync because reviewers audit the classifier's decisions against this document.

---

## How detection works

Given a deck's extracted text and page count:

1. **Type-signature scoring**: for each of the 5 deck types, sum the weighted keyword matches across the entire deck (concatenated text of all slides).
2. **Slide-count fit bonus**: each type has a `target_count` (e.g., pitch=14, sales=11, keynote=28) and a `tolerance`. Decks within tolerance get a bonus; decks far outside get a penalty. Slide count is a strong signal on its own.
3. **Combined score** = signature score + count bonus. Highest wins.
4. **Confidence**:
   - **High**: combined score >= 15 AND winner >= 1.8x runner-up
   - **Medium**: combined score >= 8 AND winner >= 1.3x runner-up
   - **Low**: otherwise, confirmation block surfaces top 2 to 3 alternatives so the user can override.

Once a type is locked, we classify each slide using THAT type's role keywords. Low-confidence slides fall back to "Content" and get flagged in the confirmation block.

---

## Hard overrides (apply to every type)

Before score-based role classification, these overrides short-circuit:

- **Cover**: first slide, <=40 words containing company name, OR simply <=10 words. role = Cover (high confidence).
- **Team-like slide**: 3+ detected human names (capitalized two-word pattern) + at least one role title (CEO/CTO/Founder/etc.). role = whichever Team-ish slot exists in the winning spine (Team, Team & Hiring, Hiring, Team Spotlights).
- **Ask/Asks**: contains a dollar-amount pattern (`$NM`, `$NK`, `$NB`) combined with raise/funding language. role = Ask (pitch).

---

## The 5 spines

### 1. pitch (14 slides, tolerance +/-3)

**Spine**: Cover · Problem · Why Now · Solution · Product · Demo · Market · Business Model · Traction · Competition · Moat · GTM · Team · Ask

**Type signatures (weight)**: `use of funds` (8), `we're raising` (7), `seed round` (6), `pre-seed` (6), `series a` (4), `series b` (4), `tam` (5), `sam` (5), `som` (5), `addressable market` (5), `moat` (5), `pitch deck` (6), `pitch` (3)

**Role keywords**: Problem (`problem`, `broken`, `painful`, `users struggle`, `pain point`, `error-prone`, `inefficient`); Why Now (`why now`, `inflection`, `made possible by`, `for the first time`, `enabled by`, `timing`); Solution (`solution`, `introducing`, `we built`, `we solve`, `our approach`); Product (`product`, `features`, `how it works`, `architecture`); Demo (`demo`, `live demo`, `walkthrough`, `see it in action`); Market (`tam`, `sam`, `som`, `market size`, `addressable market`); Business Model (`pricing`, `revenue model`, `unit economics`, `ltv`, `cac`, `business model`); Traction (`traction`, `mom`, `yoy`, `paying customers`, `design partners`, `loi`); Competition (`competition`, `competitors`, `differentiation`, `incumbents`); Moat (`moat`, `defensible`, `barrier to entry`, `network effect`, `flywheel`); GTM (`go-to-market`, `gtm`, `plg`, `product-led`, `sales motion`); Team (`team`, `founded by`, `founders`, `previously at`); Ask (`ask`, `raising`, `use of funds`, `we're raising`, `investment`).

---

### 2. sales (11 slides, tolerance +/-2)

**Spine**: Cover · About You · Problem · Why Today · Solution · How It Works · Proof · ROI · Implementation · Pricing · Next Steps

**Type signatures**: `next steps` (5), `book a meeting` (5), `case study` (4), `reference customer` (5), `roi` (4), `implementation plan` (5), `return on investment` (5), `sales deck` (6), `customer deck` (6), `why today` (5), `pricing tier` (4), `per seat per month` (4)

**Role keywords**: About You (`about you`, `your team`, `your industry`, `your goals`, `discovery`); Problem (`your challenge`, `pain point`, `struggling with`, `today's reality`); Why Today (`why today`, `cost of inaction`, `cost of delay`, `urgency`); Solution (`our solution`, `how we solve`, `what we do`); How It Works (`how it works`, `workflow`, `our process`); Proof (`case study`, `testimonial`, `reference`, `results`); ROI (`roi`, `return on investment`, `payback`, `cost savings`, `dollars saved`); Implementation (`implementation`, `rollout`, `onboarding`, `go-live`); Pricing (`pricing`, `per seat`, `starting at`, `tier`, `annual contract`); Next Steps (`next steps`, `book a meeting`, `proposal`).

**Logo divider straddle pattern**: editorial sales / services / founder-tier decks frequently use a row of half-domes or semicircles that *straddle* a wave divider, the dome's flat bottom sits on the wave's top edge, and only the top hemisphere of the dome is visible above the divider. Below the wave is a different content region (usually a card grid or a photo-tinted hero strip). The straddle creates a visual hinge between two content blocks and is one of the canonical patterns for the Proof / Case-Study row and the Implementation / Roadmap row in editorial sales decks.

Two source ratios are common in `a:custGeom`:

| Shape | cx:cy ratio | Build recipe |
|---|---|---|
| True semicircle | roughly 2:1 (within +/-0.15) | `width: <2r>px; height: <r>px; border-radius: <r>px <r>px 0 0;`, flat bottom anchored on the divider |
| Half-dome (squat hemisphere) | roughly 1.55:1 (within +/-0.15) | `width: <cx>px; height: <cy>px; border-radius: <cx/2>px <cx/2>px 0 0;`, wider than tall, same anchor |

Anchoring: align the dome's flat bottom to the divider's top edge so the silhouette doesn't peek below the wave. Use `position: absolute; bottom: 0` on the dome inside its container, and ensure the container's overflow is clipped at the divider line.

Reference shape detection from `a:custGeom` lives in the SKILL.md Phase 1 step 9 ("Custom-geometry shape classification"). Phase 3 picks the recipe from the ratio bucket, do not default to `border-radius: 50%` (full circle) when the source ratio is 2:1 or 1.55:1.

---

### 3. launch (12 slides, tolerance +/-2)

**Spine**: Cover · Problem · Introducing · How It Works · Demo · Who It's For · Availability & Pricing · Early Customers · Roadmap · Why Now · Team · Try It

**Type signatures**: `introducing` (5), `now available` (6), `available today` (6), `launch day` (6), `generally available` (6), `starting at $` (5), `announcing` (5), `product launch` (8), `now live` (5), `try it` (4), `try now` (4)

**Role keywords**: Problem (`problem`, `pain`, `today's reality`); Introducing (`introducing`, `meet`, `announcing`, `presenting`, `now available`); How It Works (`how it works`, `workflow`, `step 1`, `step 2`, `step 3`); Demo (`demo`, `try the demo`, `see it`, `walkthrough`); Who It's For (`who it's for`, `built for`, `made for`, `designed for`); Availability & Pricing (`availability`, `pricing`, `starting at`, `free for`, `per month`); Early Customers (`early customer`, `testimonial`, `used by`, `loved by`); Roadmap (`roadmap`, `coming soon`, `upcoming`, `what's next`); Why Now (`why now`, `market moment`, `the shift`, `timing`); Team (`team`, `founders`, `the team behind`); Try It (`try it`, `get started`, `sign up`, `download`, `qr code`).

---

### 4. keynote (28 slides, tolerance +/-8)

**Spine**: Cover · Hook · Thesis · Why This Matters Now · Argument & Evidence · Stories & Proof · Implications · Counter-arguments · Call To Action · Thank You

**Type signatures**: `thank you for having me` (6), `my thesis` (5), `today i want to argue` (6), `today i'll argue` (6), `the one idea` (5), `keynote` (5), `ted` (4), `conference talk` (5), `speaker` (2)

**Role keywords**: Hook (`story`, `imagine`, `picture this`, `let me tell you`); Thesis (`my thesis`, `the one idea`, `today i'll argue`, `i believe`); Why This Matters Now (`why now`, `why this matters`, `the moment`); Argument & Evidence (`evidence`, `research shows`, `data suggests`, `consider`); Stories & Proof (`example`, `case in point`, `here's what happened`); Implications (`what this means`, `implications`, `what to do`, `how to apply`); Counter-arguments (`objection`, `counter-argument`, `some might say`, `critics argue`); Call To Action (`call to action`, `what i want you to do`, `your turn`); Thank You (`thank you`, `questions?`, `q&a`).

Keynote roles are coarser because keynote content is more fluid, the same "story" keyword could appear in Hook, Stories & Proof, or Implications. This is OK: the fidelity bar is the slide text and visual layout, not the role label.

**Founder-journey subtype, alternation pattern**: keynotes framed as a personal / founder journey frequently alternate **timeline-step, photo-collage, timeline-step, photo-collage** for five to ten beats in a row. The timeline slides are near-identical structurally (same axis, one more milestone lit up each step), and a naive classifier will pool adjacent pages as "timeline variants" and miss the photo-collage beats in between. When that happens downstream, the builder maps every slide in the block to `timeline_slide()` and the photo pages render as empty timelines.

**Detection**: in a keynote, if you see >=3 consecutive pages with a timeline-like horizontal axis, check whether any of them are actually raster-heavy (has_hero_image = true). If alternating pages show hero images while the others are vector-only, that's the alternation pattern, classify each page independently rather than pooling.

**Build-time rule**: never reuse a role across adjacent pages in a founder-journey block without re-examining each page's raster content. `timeline_slide(N, steps)` and `raster_slide(asset, label)` should interleave.

---

### 5. all-hands (15 slides, tolerance +/-2)

**Spine**: Cover · Agenda · Big Wins · Product Highlights · Customer Stories · Financial Update · Hiring · Team Spotlights · Values · Upcoming Events · Priorities · Learnings · Shout-outs · Q&A · Open Floor

**Type signatures**: `all-hands` (8), `all hands` (8), `town hall` (7), `welcome team` (5), `monthly all hands` (8), `shout-outs` (6), `kudos` (4), `new faces` (5), `open floor` (5)

**Role keywords**: Agenda (`agenda`, `today's plan`, `topics`); Big Wins (`big wins`, `wins this month`, `celebrations`); Product Highlights (`product highlights`, `what we shipped`, `feature release`); Customer Stories (`customer story`, `customer spotlight`); Financial Update (`financial update`, `company metrics`); Hiring (`new hires`, `new faces`, `welcome to`); Team Spotlights (`team spotlight`, `team of the month`); Values (`values`, `culture`, `our values`, `living our values`); Upcoming Events (`upcoming events`, `mark your calendar`, `save the date`); Priorities (`priorities`, `focus areas`); Learnings (`learnings`, `retrospective`, `setbacks`); Shout-outs (`shout-outs`, `kudos`, `thank yous`, `recognition`); Q&A (`q&a`, `questions?`, `ask us`); Open Floor (`open floor`, `closing`, `next all-hands`).

---

## Why the spine vocabulary, specifically

Each deck type has a canonical spine because the corresponding `deck-*` skill expects it. A pitch deck's reviewers check for Problem to Solution flow; a sales deck's reviewers check for ROI and Next Steps; an all-hands deck's reviewers check for celebration and candor balance. The role labels are metadata the downstream reviewer uses, they don't restructure your slides.

Slides that don't map cleanly to any canonical role fall back to "Content" (low confidence). This is by design. The user can either leave them unlabeled (the HTML output still includes the slide verbatim) or assign a custom role during Phase 2.

---

## Ambiguity handling across types

Some keywords compete across types. The classifier's `type_signatures` list is tuned to minimize collisions, but when they do collide, slide count is the tiebreaker:

- **11 slides**, sales
- **12 slides**, launch
- **14 slides**, pitch
- **15 slides**, all-hands
- **25 to 35 slides**, keynote

When both signature score AND slide count don't converge, confidence drops to `medium` or `low`, and the confirmation block shows the top 2 to 3 alternatives. The user is the final arbiter, we'd rather ask than guess wrong.

---

## Confidence impact

Confidence changes what happens downstream:

- **High type confidence**: handoff skill locked, no prompt to override.
- **Medium type confidence**: confirmation block shows alternatives hint: `, or maybe <alt1> or <alt2>`.
- **Low type confidence**: alternatives prominent, user must confirm type before slide-role display is trusted.

For per-slide roles:
- **High role confidence**: role locked into the brief.
- **Medium role confidence**: flagged in confirmation block: `Slide 7 looks like <role> (medium confidence), confirm?`.
- **Low / unclassified**: labeled "Content" in the brief, surfaced with the first 30 words of slide text.

When `was_ocr_fallback == true` (scanned PDF), lower each role confidence one step (high to medium, medium to low). OCR text is noisier, so keyword-match confidence is inherently less reliable.
