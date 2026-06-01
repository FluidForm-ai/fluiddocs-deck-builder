# Anthropic Pitch Template

14-slide pitch deck mirroring Anthropic's research-lab aesthetic for a foundation-model or AI-safety pitch.

## Open in browser

[Open anthropic-pitch.html](./anthropic-pitch.html)

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

Mirror of the editorial, paper-stock visual system Anthropic uses on its own research site.

- Palette: cream `#F5F0E8` ground, saddle-brown accent, deep ink for body. No gradients, no glass.
- Typography: serif display (Tiempos or close substitute) paired with a humanist sans for body. Reads like a research paper, not a SaaS landing page.
- Narrative: "From language-model capability to language-model safety." Why Now and Solution slides carry the lab-to-product framing.
- Founders: Dario Amodei and Daniela Amodei listed on the Team slide.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `anthropic-pitch.html` to a new filename, replace the brand tokens inside the `:root` block (palette, fonts, accent), then swap the slide copy. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-pitch` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
