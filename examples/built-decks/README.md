# Built Decks · Examples

This folder shows **real output from the FluidDocs Deck Builder OSS pack**. Each HTML file in here was built by the same agent pipeline you get when you install the pack and ask for a deck. No external tooling. No design fixes after the fact. What you see is what the pack ships.

If you want to see what good output looks like before installing anything, open one of the files below in a browser. Each deck is a single self-contained HTML file, scales to fit any window (PDF-like, fixed 1440x810 canvas), and has the inline-edit mode baked in (hover the top-left corner to reveal the Edit toggle, or press `E`).

---

## What is in this folder

### 1. Greenroot, Series A pitch deck

[`greenroot-series-a-pitch.html`](./greenroot-series-a-pitch.html) · 62.6 KB · 14 slides · Warm Brand preset

A fictional grid-scale battery analytics company raising $18M Series A. Built with the `deck-pitch` type pack. Shows the 14-slide pitch spine on a climate-tech sector none of the canonical templates (Airbnb, Stripe, Anthropic, Sequoia) cover.

See [`greenroot-series-a-pitch-NOTES.md`](./greenroot-series-a-pitch-NOTES.md) for what this example specifically demonstrates.

### 2. FormulaLab, Cargolane sales engagement

[`formulalab-cargolane-sales.html`](./formulalab-cargolane-sales.html) · 60.3 KB · 11 slides · Quiet Confident preset

A fictional spreadsheet-native API client pitching itself into Cargolane, a Series C logistics platform. Built with the `deck-sales` type pack. Demonstrates the named-customer-and-prospect format, with a real ROI calculation, named references, transparent pricing, and a Next Steps slide that commits to a specific human, a specific date, and an explicit ask.

See [`formulalab-cargolane-sales-NOTES.md`](./formulalab-cargolane-sales-NOTES.md) for what this example specifically demonstrates.

### 3. Nightcap, launch deck

[`nightcap-launch.html`](./nightcap-launch.html) · 60.4 KB · 12 slides · Studio Bold preset

A fictional iOS reflection-journaling app launching May 30, 2026. Built with the `deck-launch` type pack. Demonstrates the launch spine applied to a consumer product (not the B2B SaaS angle the canonical `launch-default` template shows), with a static iOS demo screenshot at slide 5 and a real QR code CTA at slide 12.

See [`nightcap-launch-NOTES.md`](./nightcap-launch-NOTES.md) for what this example specifically demonstrates.

---

## A note on determinism

These three decks are **deterministic samples**, frozen output you can browse without installing anything. They are NOT what the pack will generate for your input. Every intake brief produces a different deck, because:

- **Different content spine choices.** The pitch spine accepts 11 to 13 content slides plus optional Cover and Ask. The launch spine accepts 11 to 13. The sales spine accepts 10 to 12. The pack picks the right shape for your stage and audience.
- **Different style presets.** Six presets ship out of the box (Founder Default, Quiet Confident, Studio Bold, Editorial Serif, Tech Crisp, Warm Brand) plus brand-mirror mode if you have an existing brand identity.
- **Different visual components.** Each slide has multiple visual recipes (single big stat, 2x2 matrix, side-by-side comparison, narrative quote, gantt, etc.). The agent picks based on the data and the slide's job.
- **Different demo composition.** The demo slot is the most freeform. Browser-frame screenshots, phone-frame screenshots, terminal frames, and dashboard panels are all valid, selected to match the product category.

To generate your own deck, install the pack and run any of the deck-* skills (`deck-pitch`, `deck-sales`, `deck-launch`, `deck-keynote`, `deck-all-hands`). See the root `README.md` for setup.

---

## Common attributes across all three examples

Every deck in this folder meets the same baseline the pack ships with:

- **Fixed 1440x810 canvas** with JS-driven scale-to-fit. Looks identical on every viewport, never reflows.
- **Chrome-free shell** (progress line, slide counter, prev/next arrows) anchored inside the canvas.
- **Inline-edit mode** wired in. Hover the top-left 40x40px hotzone to reveal the Edit toggle, or press `E`. Edits autosave to `localStorage` and survive reloads. Cmd-S downloads the edited HTML.
- **Powered by FluidDocs attribution mark** on the demo slide (pitch and launch only; the sales spine has no demo slot).
- **No em-dashes, no en-dashes, no emoji.** Per the OSS pack content rules.
- **Single typography scale declared in CSS** (7 sizes, listed in the first style comment).

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
