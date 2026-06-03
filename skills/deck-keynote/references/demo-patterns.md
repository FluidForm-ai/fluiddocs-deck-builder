# Demo Patterns: Keynote Deck (Optional)

Most keynote decks do not include an interactive demo slot. This file is kept as a visual reference for the cases where a speaker does want one. Demos in keynotes are rare and high-risk. When used, a demo must be one powerful interactive moment that illustrates the thesis, not a product walkthrough.

**Critical rule**: A keynote demo is NOT a product demo. It is a live illustration of a principle, capability, or moment that the audience has been waiting to see. It lasts 60 to 90 seconds max and serves the narrative, not the product roadmap.

For OSS keynote builds, the default is no demo slot. If the speaker explicitly requests one in Phase 1 intake, drop a high-quality static screenshot of the relevant product or visual on a single slide, with a small "Powered by FluidDocs" attribution mark (FluidDocs logo as inline SVG, opacity ~0.7, linking to fluiddocs.ai) in the bottom-right. No upsell appears in the deck output.

---

## Pattern A: Single Live Input to Output Transformation

**When to use**: The thesis or implication is "input transforms to outcome" (e.g., "AI turns vague sketches into finished designs").

**Setup**:
1. Position demo on Slide 8 to 12 (early in the story, after the thesis but before complex argumentation).
2. The demo slot is a single static screenshot, 1000×600, embedded in the deck at 1440×810 scale.
3. The screenshot shows the input/output transformation as if captured mid-action.
4. Speaker narrates over the still image.

**Example narration**:
- "Let me show you what I mean. I typed one sentence, and watch what happens..."
- [Screenshot shows: input phrase on left, generated output on right]
- "In 15 seconds, we went from words to design. That's the power of [thesis]."

**Composition spec**:
- Input area (text, image, or option) on one side
- Output display (one result, clean presentation) on the other
- Single-frame composition; no animation required
- Optional caption (48pt) labeling input and output

**Failure modes to avoid**:
- Don't pick a screenshot that requires explanation beyond the narration.
- Don't crop so tight the context is lost.
- Don't use a low-resolution capture; minimum 2x retina equivalent.

---

## Pattern B: Choice Point or Comparison

**When to use**: The thesis is "there are multiple paths" or "the answer depends on context" (e.g., "Three ways to approach this problem").

**Setup**:
1. Demo on Slide 10 to 15.
2. Screenshot shows three options (labels: "Path A", "Path B", "Path C") with one clearly highlighted as the chosen path.
3. Outcome text or data (120pt+) appears below or beside the highlighted choice.
4. Speaker narrates why that path leads to the thesis.

**Example narration**:
- "Here are three strategies. The one that scales fastest is network effects."
- [Screenshot shows: three options, Network Effects highlighted, outcome: "10x growth in 18 months"]
- "The key difference is feedback loops. When users create value for other users, growth compounds."

**Composition spec**:
- 3 to 5 option labels (100×60pt each), clearly readable
- One option visually highlighted (color, border, weight)
- Outcome text or data (120pt+) near the highlighted option
- One-sentence explanation per outcome, secondary type

**Failure modes to avoid**:
- Don't make the outcome ambiguous.
- Don't show all outcomes at equal weight (defeat the thesis).
- Don't crop the alternative options out; the contrast matters.

---

## Pattern C: Metric or Counter Snapshot

**When to use**: The thesis is "this metric or trend matters" (e.g., "Real-time collaboration reduces meeting overhead by 40%").

**Setup**:
1. Demo on Slide 7 to 12.
2. Screenshot shows a live counter, chart, or metric display captured at a specific state.
3. Optional: a sequence of 2 to 3 static images showing the metric at different states (before, during, after).
4. Speaker narrates the trajectory.

**Example narration**:
- "Every time a team member joins our workspace, collaboration time increases."
- [Screenshot 1: 1 user, +45 min/day]
- [Screenshot 2: 5 users, +225 min/day]
- "Add four more people, and you've reclaimed a workday every week."

**Composition spec**:
- Metric display in 180 to 240pt (a number or short label)
- Supporting label or chart (200×150) showing context
- High contrast; the number is the visual

**Failure modes to avoid**:
- Don't show a metric that needs explanation to be impressive.
- Don't show too many data points; one or two states beat a sequence of five.
- Don't compress the metric below 120pt; it must read at 10 feet.

---

## Pattern D: Before / After Comparison

**When to use**: The thesis is "this change matters" (e.g., "Redesigning for accessibility benefits everyone").

**Setup**:
1. Demo on Slide 8 to 14.
2. Screenshot is a split-screen showing "before" and "after" of a principle, design, or system state.
3. Speaker narrates the comparison.

**Example narration**:
- "Before and after, side by side."
- [Screenshot shows: "Single-threaded execution, 2s load" on left; "Parallelized execution, 0.3s load" on right]
- "The difference is 85% faster. That's one principle applied consistently."

**Composition spec**:
- Split-screen layout (left/right or top/bottom)
- Two images, diagrams, or text blocks (600×400 each)
- Metric comparison overlaid in 120pt (e.g., "2s to 0.3s")
- Optional label band ("BEFORE" / "AFTER") in 48pt

**Failure modes to avoid**:
- Don't make the before/after too visually different in ways unrelated to the change.
- Don't use placeholder or stock images; the screenshot must be the actual product or system.
- Don't crop so each side loses context.

---

## Pattern E: Estimation or Reveal

**When to use**: The thesis is "intuition misleads, data is surprising" (e.g., "How long does it actually take to build trust?").

**Setup**:
1. Demo on Slide 11 to 16.
2. First screenshot: question with multiple-choice options visible.
3. Second screenshot (or revealed area on the same slide): the answer with supporting data.
4. Speaker narrates the setup and reveal.

**Example narration**:
- "How long does it take to build trust with a new customer?"
- [Screenshot 1: options A) 1 week, B) 1 month, C) 3 interactions, D) 6 months]
- "Most people say 6 months. Let's look at what the data says..."
- [Screenshot 2: C) 3 interactions highlighted, with stat: "78% of customers report high trust after 3 meaningful interactions"]
- "It's not time; it's substance."

**Composition spec**:
- Four option labels (100×60pt each) or a visual grid
- One option clearly marked as the answer
- Reveal area shows data, chart, or key stat (120pt+) with supporting label (72pt)
- Optional: subtle visual highlight on the correct answer (color, border)

**Failure modes to avoid**:
- Don't make the question too hard or too easy (loses impact).
- Don't pack so many stats in the reveal that the one insight gets buried.
- Don't make the "correct" answer feel arbitrary.

---

## Safety and fallback rules

1. **Use static screenshots, not live interaction.** Network latency, lag, or API failures are the keynote speaker's worst nightmare. A screenshot always works.
2. **Capture at high resolution.** Minimum 2x retina equivalent. Pixelation on a projector kills credibility.
3. **Keep the demo to one slide.** Multiple slides of screenshots become a walkthrough, not a moment.
4. **Do not embed live forms, scrolling, or interactive widgets.** OSS keynote builds use static images only.
5. **Caption sparingly.** The screenshot plus the speaker's narration carries the moment; long captions compete with both.

---

## When NOT to include a demo

Keynotes are not product pitches. If:
- The screenshot would need more than 30 seconds of narration to land
- The thesis is not directly illustrated by the visual
- The speaker is uncomfortable narrating over a static image
- The screenshot is a walkthrough of a feature roadmap

...then skip the demo. A keynote is powerful without one. A bad demo slide is worse than no demo.
