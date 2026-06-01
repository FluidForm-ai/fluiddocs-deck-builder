# Visual Components, Brand-Native Patterns

The content spine is fixed (14 slides). The visual expression of each slide should change per brand. If every deck uses Airbnb's 2x2 competition matrix and Airbnb's TAM rings and Airbnb's flywheel, every deck ends up feeling like "Airbnb with different colors", which is a known failure mode.

Use Airbnb as the **structural** reference (what each slide contains, slide-to-slide pacing). Pick visual components from this file that match the source brand's actual design voice.

---

## Competition slide, 5 patterns

Pick one. Do not default to the 2x2 matrix unless the brand is genuinely soft or lifestyle.

### A. 2x2 positioning matrix (Airbnb default)
- Best for: consumer, lifestyle, design-forward brands with abstract axes
- Brands: Airbnb
- Visual: two crossed axes, competitor pills positioned, "us" pill bold in top-right
- **Why it fails elsewhere**: reads as soft or marketing in brands that want to look rigorous or enterprise

### B. Bold data comparison table
- Best for: enterprise, infra, API-first brands
- Brands: Stripe
- Visual: dark header row, 4 to 6 competitor rows, 4 to 5 feature columns with check, x, dot icons, "us" row highlighted in brand primary
- Implementation: `grid-template-columns: 1.8fr 1fr 1fr 1fr 1fr` for the rows
- Uses `<svg>` check or x icons (not emojis): green check, red x, amber half-dot
- Takeaway card underneath with a big Mono stat ("1 of 1", "3x", "Only operator that...")

### C. Feature-bar comparison
- Best for: creative tools, AI products where "capability levels" are the story
- Brands: Anthropic
- Visual: competitors as rows, each with 3 to 5 horizontal bars showing capability strength on different dimensions
- Bars fill in brand primary; empty equals thin muted line

### D. Radar or spider chart
- Best for: multi-dimensional product comparisons, technical products
- Visual: polygon overlays on a 5 to 6-axis radar grid, brand as a solid polygon, competitors as outlined polygons
- Risk: can feel academic, use only if the brand has a technical voice

### E. Narrative card stack
- Best for: Sequoia memo-style, early-stage "we're the only serious attempt" framing
- Brands: Sequoia Classic, Anthropic
- Visual: 4 stacked cards, each "Why [Competitor] doesn't solve this," with the last card being "Why we do." Prose-heavy, no icons.

### Universal rule
The "us" treatment should be brand-primary accented (row highlight, filled polygon, filled bars, card border) and visually unambiguous. Never ambiguous side-by-side, the reader should know instantly which column is the subject of the deck.

---

## Moat slide, 4 patterns

### A. Defensibility 4-card grid plus footer flywheel
- Best for: marketplaces, consumer networks
- Brands: Airbnb
- Visual: 2x2 grid of moat cards (network effect, data moat, switching costs, regulatory), plus a footer "flywheel" bar with pills and arrows
- Flywheel: single row of pills with arrow markers between them; dark background plus brand-primary border-left

### B. Moat depth bars
- Best for: enterprise, infra
- Brands: Stripe
- Visual: 5 to 6 categories as rows, each with a horizontal bar showing "our depth" vs "competitor depth" (color-coded)
- Feels like a dashboard

### C. Capabilities ladder
- Best for: AI or foundation-model brands
- Brands: Anthropic
- Visual: vertical ladder with 4 to 5 rungs, each rung a capability (inference, tool use, safety, multi-modal, agentic)
- Brand-primary highlights the rungs we own; grey for rungs others have; forward arrow at top for where we're heading
- Feels like a product roadmap

### D. "What happens when [big competitor] copies this in 6 months"
- Best for: Sequoia memo-style, early-stage realism
- Brands: Sequoia Classic
- Visual: a single big question as the eyebrow, then 3 prose blocks with competitor scenarios and our response
- No chart. Editorial. Serif.

---

## GTM slide, 4 patterns

### A. City rollout rail (horizontal timeline)
- Best for: marketplaces with geographic expansion
- Brands: Airbnb
- Visual: dark bar, brand-gradient rail line, 4 to 5 milestones as dots with quarter labels and one-line descriptions
- Avoid soft pastel gradients, bold dark rail reads more rigorous

### B. Motion grid (4 channels)
- Best for: multi-motion GTM (self-serve plus sales plus partnerships plus PLG)
- Brands: Stripe
- Visual: 2x2 grid of channel cards, each with an icon, motion name, unique insight
- Plus a weighted-funnel visualization below showing CAC payback

### C. Channel bars (sized by CAC or LTV)
- Best for: data-forward brands
- Brands: Stripe
- Visual: horizontal bars for each channel, sized by expected volume, colored by efficiency
- Table-like. API-doc feel.

### D. Wedge narrative (pre-seed or seed)
- Best for: very early stage
- Brands: any pre-seed, Anthropic, Sequoia Classic
- Visual: single big arrow pointing from "wedge customer" to "expansion" with numbers at each stage
- 3 text blocks: wedge, beachhead, expansion

---

## Traction slide, 4 patterns (stage-matched)

### A. Growth curve (MoM or YoY)
- Best for: Series A+ where growth IS the story
- Brands: Stripe
- Visual: single big line chart with annotations (launch, product milestone, enterprise partnership)
- Brand-primary line on a subtle grid

### B. Weekly bar cohort
- Best for: Seed, pre-Series A, where absolute numbers are low but the slope is real
- Brands: any seed-stage
- Visual: 12-week bar chart, monospace week labels, brand-primary bars
- Small metric cards above (total trips, DAU, signups, whatever)

### C. Logo grid plus retention
- Best for: enterprise, B2B
- Brands: Stripe
- Visual: 8 to 12 customer logos in a grid plus one big NRR or retention number plus one big growth rate
- Logos should be real-looking SVG wordmarks, not emoji placeholders

### D. Quiet-confidence metrics (pre-seed)
- Best for: Sequoia memo, very early stage
- Brands: Sequoia Classic, Anthropic
- Visual: 3 big numbers in monospace, each with a one-line context, "162 beta riders, 100% repeat inside 10 days," "1,400 waitlist," etc.
- No chart. Reader assembles the narrative.

---

## Market slide, 4 patterns

### A. Concentric TAM, SAM, SOM rings (default)
- Best for: consumer, B2C, soft brands
- Brands: Airbnb
- **Critical fix**: labels must sit in their visible crescents (see rendering-checks.md), not stacked in the center
- Three rings, inset 0, 20%, 42%, labels at top of each crescent

### B. Bottom-up calc grid
- Best for: bottom-up marketplaces, SaaS
- Brands: Stripe
- Visual: equation-style display, `X customers x $Y ARPU x Z segments = $TAM`
- Monospace, big numbers, with a "how we get to $1B ARR" footer

### C. Sankey or flow diagram
- Best for: flows between segments (who buys what)
- Brands: Stripe
- Visual: left column equals customer segments, right column equals revenue types, flows between
- Harder to build; use only if the story genuinely is about flow

### D. Single "big number" plus credibility
- Best for: mature markets where TAM is well-known
- Brands: Sequoia Classic, Anthropic
- Visual: one number 200px tall, a source line, and 2 to 3 supporting rows
- Feels like a memo

---

## Team slide, 4 patterns (founder-count-adjusted)

### A. 3-founder equal-grid (classic)
- For: exactly 3 founders, no other named hires
- Layout: `repeat(3, 1fr)` with full-size cards

### B. 3 founders plus key hires sub-section
- For: 3 founders plus 1 to 3 named early hires
- Layout: 3-col primary grid for founders, then a `.team-key-hires` strip below, a dark "First hires" label card plus 1 to 2 smaller hire cards in its own sub-grid

### C. 2-founder hero split
- For: exactly 2 founders
- Layout: `repeat(2, 1fr)` with bigger cards that include photo, longer bio, and one "why this founder wins this problem" paragraph
- More real-estate per founder since there's room

### D. Narrative team intro (memo style)
- For: Sequoia-style decks, early stage
- Brands: Sequoia Classic
- Visual: prose paragraphs per founder, no avatars, serif body, just names as bold inline
- Plus an advisor roster below in horizontal pills

### Advisor strip (applies to all patterns)
- Below the main team grid, a dark or light horizontal strip with 2 to 4 advisor pills
- Pattern: `<b>Name</b> · firm · why they matter`
- Do NOT use advisor logos unless they're extremely recognizable

---

## Problem slide, 3 patterns

### A. 3-card problem grid
- Default. Works for most.
- Each card: icon plus title plus 2-line description

### B. Narrative plus single-stat pull-quote
- Best for: memo-style, dark-theme, editorial
- Brands: Sequoia Classic, Anthropic
- Visual: prose paragraph with one big inline stat pulled out as a quote

### C. Before/After split
- Best for: AI products replacing legacy workflows
- Brands: Anthropic
- Visual: left column equals old way (greyed, long list of pain), right column equals new way (brand-primary, short list)

---

## Why Now slide, 2 patterns

### A. 3 shifts in a horizontal row
- Default. Each shift: "From X to Y" with a small chart or data point
- Works for most brands

### B. Single curve or timeline
- Best for: AI, deeptech, where there's one dominant "unlock" curve (model capability, cost-per-inference, hardware cost)
- Visual: one chart showing the inflection point, with an annotation at "today"

---

## Cross-cutting rules

1. **Dark-theme native brands** (Sequoia-memo-style as a deliberate variant) should have the Moat, GTM, Competition slides in dark even if the rest of the deck is light. Consistency beats uniformity. Default to light theme otherwise.

2. **Monospace accents** (JetBrains Mono) feel native on API, infra, data brands (Stripe). Use for stats, dates, code-like labels. Overuse on soft consumer brands (Airbnb) feels wrong.

3. **Gradient backgrounds** are fine for some consumer brands; avoid on Anthropic, Sequoia, too product-marketing.

4. **Big stat cards** (a single number 80 to 160px tall with a label) feel native almost everywhere, use liberally for traction and market slides.

5. **The "us" highlight** in Competition, Moat, GTM must ALWAYS use the brand primary (not a generic blue or green). The reader should feel the brand color wherever the subject of the deck is referenced.

---

## Quick-reference: which pattern per brand

| Brand       | Competition       | Moat                   | GTM             | Market           | Traction              |
|-------------|-------------------|------------------------|-----------------|------------------|-----------------------|
| Airbnb      | 2x2 matrix        | 4-card plus flywheel   | Motion grid     | TAM rings        | Growth curve          |
| Stripe      | Data table        | Depth bars             | Channel bars    | Bottom-up calc   | Logo grid plus NRR    |
| Anthropic   | Narrative stack   | Capabilities ladder    | Wedge narrative | Single big number | Quiet-confidence      |
| Sequoia     | Narrative stack   | Memo-style             | Wedge narrative | Single big number | Quiet-confidence      |

Treat the table as a default, not a rule. If a specific brand's actual historical deck used a different pattern (and it worked), follow that instead.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
