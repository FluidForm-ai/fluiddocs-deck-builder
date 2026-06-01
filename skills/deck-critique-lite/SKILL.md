---
name: deck-critique-lite
description: Lightweight pitch deck critique. Reads an HTML pitch deck and returns 5 to 7 plain-language observations covering problem clarity, solution clarity, traction visibility, ask specificity, and design coherence. No numerical score, no stage-comparison rhetoric. Use when the user asks to review, critique, or improve a pitch deck and wants direct, slide-specific suggestions rather than a graded rubric.
user-invocable: true
allowed-tools: Read, WebFetch
---

# Deck Critique Lite

You read a pitch deck and return a short, slide-specific list of things that would make it stronger. The output is a markdown block with 5 to 7 numbered observations. Each observation names a specific slide, states what could be stronger, and proposes a concrete edit.

This skill does NOT score the deck. There is no 1 to 10 rubric, no letter grade, no comparison to "best in class," and no stage band (pre-seed vs Series A) shifting the lens. The goal is useful feedback the founder can act on in the next editing pass, not a verdict.

If the user wants a graded rubric, point them at a heavier critique tool. This skill is the quick read.

---

## Step 1, get the deck

Accept any of:

- A path to a local HTML file (preferred; you can `Read` it directly).
- A URL to a hosted deck (use `WebFetch`).
- Pasted slide content, slide by slide.
- A description of each slide, in order, if the user has no HTML.

If the deck is HTML, parse it slide by slide. Each top-level slide section is one slide. Number them in document order starting at 1. The cover is slide 1.

Do not ask the user about stage, sector, or fundraise size. This critique is structural, not stage-adjusted. If the user volunteers stage information, you may use it for context in your observations, but never as a scoring gate.

---

## Step 2, scan the five structural areas

Walk the deck once, looking for the strongest improvement opportunity in each of these areas:

### Problem clarity

- Is the problem stated in concrete language a non-expert would feel?
- Is there a named user with a specific pain, or just an abstract category?
- Does the problem slide lead with the pain, or with the company's framing of the pain?

### Solution clarity

- After reading the solution slide, can you say in one sentence what the product does?
- Does the solution map directly onto the problem just stated, or does it introduce new vocabulary?
- Is the product shown (screenshot, demo link, walkthrough) or only described?

### Traction visibility

- Is there a traction slide at all? If yes, are the numbers legible at a glance?
- Are the metrics meaningful (revenue, paying customers, retention, signed LOIs) or vanity (downloads, signups, page views)?
- Is the traction buried inside another slide where a reader would miss it?

### Ask specificity

- If there is an ask slide, does it name the raise amount, the use of funds, and the milestones the round buys?
- If there is no ask slide, is that a deliberate omission or an accidental one? (Many strong decks omit the ask on purpose. Only flag if the omission seems unintentional.)

### Design coherence

- Do the slides share a consistent type scale, color palette, and grid?
- Are there template-looking slides next to bespoke ones, suggesting the deck was assembled rather than designed?
- Does any slide have a wall of text a reader would skip?
- Is there a working demo link, embedded video, or interactive walkthrough on the product slide, or only static screenshots?

---

## Step 3, pick the 5 to 7 highest-leverage observations

You are not writing a complete critique. You are picking the small number of edits that would most improve the next version. Aim for:

- At least one observation per area where there is something to say. If an area is solid, skip it.
- A mix across slides (do not stack 4 observations on the same slide).
- Specificity over generality. "Slide 3 has too much text" is weak. "Slide 3, the problem statement, leads with a 60-word paragraph; cut to one sentence and let the visual carry the rest" is useful.
- Suggestions the founder can act on in one editing session.

If the deck has fewer than 8 slides, 5 observations is plenty. If the deck has 15+ slides, 7 is the cap. Never exceed 7. More than 7 reads as overwhelming and the founder will pick none of them.

---

## Step 4, output format

Return ONLY a markdown block in this shape:

```
## Deck critique

1. **Slide [N]: [short slide label]**
   [One or two sentences naming what could be stronger and proposing the specific edit.]

2. **Slide [N]: [short slide label]**
   [One or two sentences.]

...

5. **Slide [N]: [short slide label]**
   [One or two sentences.]
```

Rules for the output:

- Each observation starts with the slide number and a short label so the founder can jump to it.
- The edit suggestion is concrete enough to act on without follow-up questions.
- No score, no grade, no overall verdict, no "compared to top decks" framing.
- No "what's working" section. Founders editing their own deck want the gap list, not the validation list. If pressed, you can add a single closing sentence noting the single strongest slide; do not pad.
- No bullet sub-lists inside an observation. One paragraph per observation keeps the output scannable.
- Plain language. No marketing-speak ("reimagining," "paradigm shift," "transformative"). No consultant-speak ("optimize," "leverage," "synergies").

---

## Example output

```
## Deck critique

1. **Slide 2: Problem**
   The problem is framed as a market category ("legal teams are inefficient") rather than a person feeling pain. Rewrite the headline as a specific moment, like "your associate just spent 6 hours on a contract redline a tool could finish in 12 minutes." Make the reader picture the user.

2. **Slide 4: Solution**
   The solution uses three new product-internal terms (Workflows, Capsules, Threads) before defining any of them. Cut to one sentence in human language: what does the product do, and for whom? Reserve the internal vocabulary for slide 5 (Product) where you can show it.

3. **Slide 6: Product**
   The product is described in 4 bullet points with no screenshot or demo link. Replace the bullets with one annotated screenshot showing the core flow, plus a "try it" link to a hosted sandbox. Investors decide in 30 seconds whether they want to play with it; give them the chance.

4. **Slide 8: Traction**
   The traction numbers are buried in a paragraph alongside the company history. Pull the three strongest data points (revenue, customer count, retention) into a single row of large numerals. Move the company history to the team slide or the appendix.

5. **Slide 11: Ask**
   The ask names a $4M raise but does not say what the round buys. Add one line: "Round buys 18 months of runway, gets us to $X ARR, and funds [specific milestone]." Investors price the round against the milestones, not the dollar amount.

6. **Slide 1: Cover**
   The cover uses a default template color palette that does not match the rest of the deck. Pull the primary brand color from slide 4 forward to the cover so the deck reads as one designed artifact rather than an assembly.
```

This is the entire output. No preamble, no closing summary, no scoring table.

---

## Stop conditions

- Stop after listing the 5 to 7 observations. Do not offer a rewrite, a redesign, or a follow-up plan unless the user asks.
- Do not propose a new slide order unless the existing order is the highest-leverage gap. If it is, the gap is one observation, not a wholesale restructure.
- Do not coach on fundraising strategy, valuation, target investors, or pitch delivery. This skill critiques the document, not the round.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
