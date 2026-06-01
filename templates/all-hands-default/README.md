# All-Hands Default Template

15-slide all-hands deck for company-wide team meetings. Warm Brand preset.

## Open in browser

[Open all-hands-default.html](./all-hands-default.html)

No install needed. Double-click the file. Press `E` inside the deck to enter inline edit mode.

## Spine (15 slides)

1. Cover / Hello
2. Agenda
3. Big Wins This Month
4. Product Highlights
5. Customer Stories
6. Financial Update (appropriate level)
7. Hiring / New Faces
8. Team Spotlights
9. Values / Culture Moment
10. Upcoming Events
11. Priorities for Next Month
12. Learnings / Retrospective
13. Thank Yous / Shout-outs
14. Q&A Kickoff
15. Open Floor

Spine source: `skills/deck-all-hands/references/content-spine.md`. Balance of celebration and candor is enforced; slides 3, 6, and 12 together set a realistic picture.

## Preset: Warm Brand

Friendly, human palette designed for a live team meeting where the deck supports the speaker rather than replacing them.

- Palette: `--brand-primary` warm orange `#C84E2C`, `--brand-accent` amber `#F5C26B`, `--brand-bg` cream `#FFF6EC`, `--brand-surface` deeper cream `#FFEDD9`, ink text `#2A1F1A`.
- Typography: Manrope for display and body, JetBrains Mono for KPI callouts. A single sans family keeps the deck feeling like an internal doc, not a launch keynote.
- Character: warm, conversational, room for team photos and customer logos. The Q&A slide is a placeholder for live conversation, not a packed FAQ.

## Inline edit module

The inline edit module is built in. Press `E` to toggle edit mode and click any element to type new copy. `Ctrl/Cmd+S` downloads the edited HTML as a new file. `localStorage` autosaves between page loads so a refresh does not lose work.

## Customize

To fork: copy `all-hands-default.html` to a new filename, replace the brand tokens inside the `:root` block (swap the orange and amber for your brand colors, swap the font if you have a company sans), then drop in this month's wins, hires, learnings, and priorities. Keep the section class names so the inline edit module continues to pick up every editable field. For the full build pipeline, install the `deck-builder` skill and the `deck-all-hands` type pack from the parent repo.

## License

MIT licensed. Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder
