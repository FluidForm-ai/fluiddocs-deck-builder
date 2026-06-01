# Stripe Pitch Template

14-slide pitch deck mirroring Stripe's brand language for a payments-infrastructure pitch.

## Open in browser

[Open stripe-pitch.html](./stripe-pitch.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (14 slides)

1. Cover
2. Problem
3. Why Now
4. Solution
5. Product
6. Demo (static screenshot)
7. Market
8. Business Model
9. Traction
10. Competition
11. Moat / Defensibility
12. GTM
13. Team
14. Ask

Spine source: `skills/deck-pitch/references/content-spine.md`.

## Brand context

Mirror of the visual system Patrick Collison and John Collison made canonical at Stripe.

- Palette: deep indigo `#635BFF` plus accent violet against a near-white surface and ink black for body type.
- Typography: Sohne-style geometric sans with a tight tracking on display, paired with a mono accent for code and metric callouts.
- Narrative: "Payments infrastructure for the internet." Problem, solution, and product slides lean on developer-led positioning and integration-first proof.
- Founders: Patrick and John Collison listed on the Team slide.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `stripe-pitch.html` to a new filename, replace the brand tokens inside the `:root` block (palette, fonts, accent), then swap the slide copy. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-pitch` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
