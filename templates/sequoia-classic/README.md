# Sequoia Classic Template

10-slide pitch deck in the institutional memo aesthetic Sequoia Capital codified for early-stage founders.

## Open in browser

[Open sequoia-classic.html](./sequoia-classic.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (10 slides)

1. Cover
2. Problem
3. Solution
4. Why Now
5. Market
6. Competition
7. Product
8. Business Model
9. Team
10. Financials and Ask

Spine derived from the classic Sequoia "writing a business plan" outline, rendered as a 10-slide deck with the Cover treated as Slide 1.

## Brand context

Mirror of the institutional memo style Sequoia publishes in its own writing-a-business-plan guidance.

- Palette: institutional black on white with a single red `#A8132A` accent. No drop shadows, no gradients. Reads as printed memo, not as screen UI.
- Typography: serif throughout, single-column hierarchy with generous line-height. The deck looks like it could be printed and handed across a partners' meeting table.
- Narrative: short, declarative slide titles. Each title states a claim; the body slide proves it.
- No named founder mirror. Use this template when the brand cue you want is "Sequoia partner reading this" rather than a specific company.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `sequoia-classic.html` to a new filename, replace the brand tokens inside the `:root` block (palette, fonts, accent), then swap the slide copy. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-pitch` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
