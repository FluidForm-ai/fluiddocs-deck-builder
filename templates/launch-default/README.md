# Launch Default Template

12-slide product launch deck for announcement moments and go-to-market reveals. Studio Bold preset.

## Open in browser

[Open launch-default.html](./launch-default.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (12 slides)

1. Cover / Announcement
2. The Problem
3. Introducing the Product
4. How It Works
5. Demo (static product screenshot)
6. Who It's For
7. Availability and Pricing
8. Early Customers / Quotes
9. Roadmap (What's Next)
10. Why Now
11. Team / Credits
12. Try It (Strong CTA)

Spine source: `skills/deck-launch/references/content-spine.md`.

## Preset: Studio Bold

Editorial palette designed for a launch reveal that is meant to be screenshot, shared, and remembered.

- Palette: `--brand-primary` deep blue `#0B3D91`, `--brand-accent` saturated yellow `#F2B705`, `--brand-bg` warm paper `#FBF7EE`, ink text `#0B0B0B`.
- Typography: Playfair Display for display headlines, Inter for body, JetBrains Mono for callouts. The serif display reads as launch moment, not as ongoing SaaS chrome.
- Character: high contrast, confident type, screenshot-as-hero on the Demo slide, real CTA with QR code on the close.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `launch-default.html` to a new filename, replace the brand tokens inside the `:root` block (swap the blue and yellow for your brand colors, swap the font stack), then drop your product screenshot into the Demo slide and confirm the QR code on the CTA resolves to a real URL. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-launch` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
