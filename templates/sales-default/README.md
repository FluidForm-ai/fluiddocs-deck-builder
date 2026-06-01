# Sales Default Template

11-slide B2B sales deck for the post-discovery, pre-close conversation. Quiet Confident preset.

## Open in browser

[Open sales-default.html](./sales-default.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (11 slides)

1. Cover
2. About You (Discovery Summary)
3. The Problem (Their Pain, Their Words)
4. Why Today (Cost of Inaction)
5. Our Solution (Plain Language)
6. How It Works (Product Mechanics)
7. Proof (Named Reference Customers)
8. ROI / Value (Numbers, Not Claims)
9. Implementation (Timeline, Effort, Onboarding)
10. Pricing (Clear, No Hand-Waving)
11. Next Steps (Specific, Calendar-Ready)

Spine source: `skills/deck-sales/references/content-spine.md`.

## Preset: Quiet Confident

Muted sage and warm bronze palette designed to read as account-specific, consultative, and trustworthy. The opposite of a high-contrast launch deck.

- Palette: `--brand-primary` sage `#4A5D4F`, `--brand-accent` bronze `#8B6F47`, `--brand-bg` warm cream `#FAF8F3`, ink text `#2D3A2F`.
- Typography: Source Serif Pro for display, Inter for body, JetBrains Mono for numbers and price callouts. The mono is used sparingly on the ROI and Pricing slides.
- Character: low-saturation, generous whitespace, account-specific by design. Cover and About You slides are built to feel one-of-one rather than templated.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `sales-default.html` to a new filename, replace the brand tokens inside the `:root` block (swap sage and bronze for your brand colors, swap the font stack), then update the deal-specific content on the Cover and About You slides. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-sales` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
