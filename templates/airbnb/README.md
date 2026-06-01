# Airbnb Pitch Template

14-slide pitch deck mirroring Airbnb's 2008 seed deck for Y Combinator.

## Open in browser

[Open airbnb-pitch.html](./airbnb-pitch.html)

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

Mirror of the 2008 seed deck Brian Chesky and Joe Gebbia took into the Y Combinator winter batch. Era is pre-rebrand AirBed & Breakfast.

- Palette: Rausch red `#FF5A5F` as the single bold accent against off-white and ink black.
- Typography: clean sans body with a confident hero size on the cover, matching the 2008 deck's flat, lecture-slide feel.
- Narrative: "Book rooms with locals, rather than hotels." Cover, problem, and market follow the original ordering and one-line positioning.
- Founders: Brian Chesky, Joe Gebbia, Nathan Blecharczyk listed on the Team slide.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `airbnb-pitch.html` to a new filename, replace the brand tokens inside the `:root` block (palette, fonts, accent), then swap the slide copy. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-pitch` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
