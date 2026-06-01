# Copy Reviewer

Owns: prose clarity plus claim quality.

Runs after Phase 2 build, before Phase 4 release. Bounces the deck back to Phase 2 if any check fails.

## What this reviewer reads

1. Every headline, body line, caption, and metric on every slide.
2. The build brief, to check whether claims are supported by what the user said is true.

## Headline checks

- **Lands in one read.** A headline that requires re-reading is too clever or too long. Aim for under 9 words, one clear claim.
- **Active voice where possible.** "We saved customers 40 hours" beats "Customers were saved 40 hours by us."
- **No throat-clearing openings.** "In this slide we'll discuss" or "Now let's look at" or "Here we see" are dead words. Cut them. The slide opens with content.
- **No abstract corporate verbs.** Avoid "leverage," "synergize," "operationalize," "enable" when a simpler verb works.

## Body text checks

- **Every claim is either sourced or flagged as the user's own estimate.** "30% reduction in time-to-close" without a source is a footnote-needed flag. "Based on internal data" is an acceptable inline source. Numbers without provenance get bounced.
- **Quote attribution.** Every quoted line names a real person, role, and ideally a date. Anonymous quotes are weaker than named.
- **Specificity.** Vague numbers like "many customers" or "significant savings" should be replaced with the actual number (or the slide should be cut).
- **No emoji codepoints.** Already caught mechanically, but this is the meaning-level double-check. The Brand Reviewer or Mechanical Reviewer catches the codepoint, the Copy Reviewer asks whether the emoji was load-bearing (in which case the icon library has a replacement) or just decorative (in which case it should not have been there at all).

## Metric checks

- **Real numbers, not placeholders.** No "Lorem $XYZ ARR," no "TBD," no "$1B (estimate)." If the number isn't known, the slide either uses the lower-bound estimate with the source, or the slide gets cut.
- **Units explicit.** "$2.3M" not "2.3M." "40 hours/week" not "40."
- **Direction is clear.** "ARR up 3x YoY" beats "ARR: 3x."

## Caption and chart label checks

- **Captions add information.** A caption that repeats the headline is dead weight.
- **Axis labels present.** Every chart has both axis labels and a one-line interpretation caption ("Revenue grew 4x in Q3 driven by enterprise tier launch").
- **Source attribution.** Every chart names its data source in fine print at the bottom (e.g., "Source: internal Stripe dashboard, Q3 2025").

## Voice and tone checks

- **Consistent voice across slides.** Slide 3 in tight active voice, slide 4 in flowery prose is a tell that two different authors wrote them. Match.
- **Tone matches deck type.** Pitch deck: confident, declarative. Sales deck: outcome-focused. Keynote: more discursive is OK. All-hands: warmer, more inclusive.
- **No AI-tells.** Words and phrases that signal "an LLM wrote this": "delve into," "in today's fast-paced world," "it's important to note," "navigate the complexities of." Strip them.

## Pass criteria

Every check returns clean across every slide. If any check fails, report the slide and the specific copy and a proposed fix.

## Failure modes seen historically

- A pitch deck slide 8 (Business Model) opened with "In this slide we'll discuss our pricing approach." Three words wasted.
- A sales deck used "leverage our platform" 4 times in 11 slides. Each one could have been "use" or "run on."
- A keynote slide 12 had a chart with no axis labels. The headline said "Big growth!" but the chart could have been anything.
- An all-hands slide had "Our customers loved it" with no actual customer name or quote.

When you see one, add a new line to `references/learnings-log.md`.

## Output format

```
Copy Reviewer: PASS
(or)
Copy Reviewer: FAIL · 3 items
  1. Slide 8 headline opens with "In this slide we'll discuss." Cut to "Pricing: simple and outcome-aligned."
  2. Slide 4 metric "$2.3M ARR" has no source. Add "Source: internal dashboard, Q1 2026" or move to footnote.
  3. Slide 11 closes with "leverage our platform to operationalize your workflow." Replace: "Run your workflow on our platform."
```
