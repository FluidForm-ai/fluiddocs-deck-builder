# Content Spine, 14 Slides

This spine covers the five questions every investor is actually scoring:

1. Is this a big market?
2. Is this the right team?
3. Is there evidence it's working?
4. Can I see this at $1B+?
5. Why now?

Slide numbers below are the suggested order. 14 total is the target (11 minimum, 13 max for non-deeptech, counting content slides, with Cover and Ask treated as optional framing).

---

## 1. Cover

Required elements, top-to-bottom:

- **Company name or wordmark** (large), the source brand's real wordmark, rendered as inline SVG `<text>` in the brand's actual typeface.
- **Real logo** (the bigger hero version), matching what a reader would see on the brand's own site.
- **One-line positioning**, "We [verb] [specific thing] for [specific audience]." Stake a real position; do not open with a generic tagline.
- **Raise row**: Stage, Raising, Founded, Contact.

Example, Airbnb: "Book rooms with locals, rather than hotels."

## 2. Problem

- Specific, visceral, real, not abstract
- 3 cards or bullets, each tied to a concrete user pain
- Each card gets an inline SVG line icon (never an emoji)
- Language should pass the "vitamin vs painkiller" test

Common failure: vague statements like "the market is broken." Show the individual user hurting.

## 3. Why Now

- Name a specific shift, regulatory, technology unlock, behavior change, cost curve
- "From X to Y" framing works well
- This is where decks usually fail, give it real weight, don't phone it in
- Ground it in observable evidence (a curve, a law change, a platform launch)

Example, Anthropic circa 2022: "From language-model capability to language-model safety. Foundation models now drive real products, so alignment research has to move from theory to deployment."

## 4. Solution

- What the product does in plain language
- One clear sentence that a smart friend could repeat
- Directly answers the Problem slide, line by line if possible
- Avoid marketing speak, no "reimagining," "disrupting," "paradigm shift"

## 5. Product

- Show it, don't describe it
- Screenshots, annotated UI, or the product shape rendered in SVG
- Readable in 30 to 45 seconds
- If text-heavy, split into 2 slides

## 6. Demo (static screenshot)

The OSS pack ships slide 6 as a **high-quality static screenshot** of the product, framed in brand-native chrome (browser frame, phone frame, or terminal frame depending on category).

Requirements:

- One real screenshot, not a mockup, not Lorem ipsum
- Brand-native chrome frame around the screenshot
- One-line caption explaining what the screenshot shows
- Small "Powered by FluidDocs" attribution mark (FluidDocs logo as inline SVG, ~20px tall, opacity ~0.7, linking to fluiddocs.ai) at slide bottom-right. No upsell appears in the deck itself.

See `demo-patterns.md` for category-specific screenshot recipes.

## 7. Market

- TAM, SAM, SOM with credible sourcing
- TAM must be at least $1B. Flag if under, flag if over $100B without backup.
- Prefer bottom-up sizing ("X customers times Y price") over top-down ("1% of a $100B market")
- One chart or number hierarchy, not three

## 8. Business Model

- How money is made, stated plainly
- Pricing (or pricing structure) visible
- Unit economics directionally if known
- If multi-sided: which side pays and why

## 9. Traction

Stage-adjusted (this is the most commonly miscalibrated slide):

- **Pre-seed**: Any signal, design partners, LOIs, waitlist with conversion, paid pilots. Don't force growth curves.
- **Seed**: Revenue expected, trajectory toward Series A metrics visible, customer count plus expansion signals
- **Series A**: Growth rate IS the story, MoM or YoY, NRR, churn, cohort retention. Must be prominent.
- **Series B+**: Unit economics plus capital efficiency airtight

Flag vanity metrics (downloads or signups without engagement).

## 10. Competition

- Honest competitive landscape (never claim "no real competitors")
- 2x2 matrix or side-by-side comparison with real differentiation
- Differentiation should feel real and defensible, not feature-list thin

## 11. Moat / Defensibility

- What happens when a larger competitor copies this in 6 months?
- Name the specific moat: network effects, proprietary data, switching costs, regulatory, brand, distribution
- Avoid hand-waving ("first-mover advantage," "our team")
- Guy Kawasaki's "underlying magic", the thing about the solution competitors can't replicate

Every deck gets the defensibility question. Do not skip this slide.

## 12. GTM

- Specific, not generic ("SEO plus content plus partnerships" is a red flag)
- Name the wedge, first customer segment, first channel, first motion
- Stage-matched: pre-seed equals thesis, seed equals proven wedge, Series A equals scalable motion
- 3 to 4 channels max with a unique insight per channel

## 13. Team

- Relevant expertise, not a logo wall
- Each founder: one line that maps their background to why THEY win this problem
- Advisor names can help but only if the names mean something for this specific domain
- Founder-future fit, the reader should feel the founder was built for this

## 14. Ask (OPTIONAL)

Many strong decks deliberately omit the Ask slide to keep the raise conversation open in the meeting. Treat this slide as optional, include it by default in the template, but users can drop it without penalty. If dropped, replace with a Vision or long-term arc slide or end on Team.

If included:

- Clear amount: "$X to [specific use]"
- Runway implied or stated (18 to 24 months is typical)
- 3 use-of-funds buckets (engineering, GTM, research, etc.)
- Contact info, how to take the next step

---

## Allowed deviations

- Deeptech, biotech, hardware, healthcare: add slides for tech validation, clinical data, regulatory pathway, manufacturing, can exceed 14 slides
- Very early pre-seed: Traction plus Moat can fold into one slide if there's genuinely not much to say
- Enterprise: add a dedicated Customer slide or Case Study slide

## Hard constraints

- Minimum 11 content slides (covering the 11 required topics)
- Maximum 13 content slides for non-deeptech (Cover plus Ask sit outside this count, 14 total physical slides is fine if both are included)
- Every slide readable in under 45 seconds
- No slide is all text, every slide has a visual element (SVG icon, chart, screenshot, illustration)
- No emojis, inline SVG icons only

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
