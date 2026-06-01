# Keynote Default Template

28-slide keynote deck for conference talks and TED-style presentations. Editorial Serif preset.

## Open in browser

[Open keynote-default.html](./keynote-default.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (28 slides)

1. Cover / Title
2. Hook (opening story or stat)
3. Thesis (the one idea)
4. Why This Matters Now
5. Argument 1
6. Argument 2
7. Argument 3
8. Argument 4
9. Argument 5
10. Argument 6 (or synthesis)
11. Story 1 Setup / Cast
12. Story 1 Problem
13. Story 1 Shift / Action
14. Story 1 Outcome
15. Story 2 Setup
16. Story 2 Problem
17. Story 2 Action and Outcome
18. Proof or Testimonial
19. Shift in Mindset
20. Implication 1
21. Implication 2
22. Implication 3
23. The Upside / Opportunity
24. The Biggest Objection
25. Why It Still Holds
26. The Trade-off or Caveat
27. Call to Action
28. Thank You / Contact

Spine source: `skills/deck-keynote/references/content-spine.md`. Flexible 20 to 35 range; default is 28 at roughly 21 minutes of speaking time.

## Preset: Editorial Serif

Magazine-grade typography designed for slides projected behind a speaker, not read off a screen.

- Palette: `--brand-primary` near-black `#1F1F1F`, `--brand-accent` editorial red `#A0344B`, `--brand-bg` cream `#FFFCF7`, ink text `#1F1F1F`.
- Typography: Lora for display, Source Serif Pro for body, JetBrains Mono for numeric callouts. Display sizes scale up to a 260px mega for hook and thesis slides.
- Character: full-bleed images, one idea per slide, mandatory visual anchor on every slide. Built for the speaker, not the audience reading along.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `keynote-default.html` to a new filename, replace the brand tokens inside the `:root` block (swap the cream and editorial red for your brand colors, swap the serif stack), then rewrite the thesis, arguments, and stories around your own talk. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-keynote` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
