# Layout Reviewer

Owns: overflow plus canvas-scale integrity.

Runs after Phase 2 build, before Phase 4 release. Bounces the deck back to Phase 2 if any check fails.

## What this reviewer reads

1. The generated `.html` file at the fixed design canvas (1440x810).
2. The same file at small-viewport test sizes to verify scale-to-fit letterboxing works:
   - iPhone portrait, 390x844
   - iPad portrait, 768x1024
   - iPad landscape, 1024x768
   - Desktop typical, 1920x1080
3. The build brief's height budget table.

## Static-canvas checks (1440x810)

- **Every slide fits within 810px.** Walk the DOM, sum heights of every direct child of `.slide`. If projected total > 810px, flag the slide. Threshold for warning: 90% of budget (730px). Threshold for fail: 100% (810px).
- **Reserved zones unviolated.** Type packs may declare reserved header (e.g., top 60px for slide title) or footer (e.g., bottom 40px for page number) zones. Content does not cross these lines.
- **No `justify-content: center` on non-cover slides.** This is the center-overflow bug: when content grows beyond canvas, centering pushes the top off-screen instead of the bottom. Use `flex-start` everywhere except `.s-cover`.
- **No tall `aspect-ratio` without `max-height` cap.** A 16:9 video embedded in a slide can blow past canvas height if it's allowed to stretch. Cap with `max-height` matched to the slide's available zone.

## Responsive scaling checks (small viewports)

- **Scale-to-fit transform present.** `.deck-outer` has `transform: scale(min(winW/1440, winH/810))` or equivalent. The whole deck visibly shrinks to fit the viewport.
- **Letterboxed, never cropped.** At iPhone portrait, the deck shows the full 1440x810 composition, scaled down and letterboxed. Never reflowed, never cropped, never with horizontal scroll.
- **No `@media` reflows.** Search the CSS for `@media`. The only acceptable use is the outer scale transform. No grid reflows, no font-size changes, no hidden elements at small viewport.
- **No viewport units inside slides.** Search for `vw`, `vh`, `vmin`, `vmax` anywhere except the outer `.deck-outer` scale transform. Inside slides, all sizing is absolute px or relative to the slide's fixed canvas.

## Nav and chrome checks

- **Nav lives inside `.deck`.** Top-left nav arrows, slide counter, edit toggle, all scale with the canvas because they're inside `.deck`. NOT inside `.deck-outer`, NOT on `body`.
- **Inline-edit module is present.** Hotzone hover (40px top-left, 400ms grace) plus E key toggle plus localStorage autosave plus Ctrl/Cmd+S download. Use JS, not CSS sibling-selector (see `references/shell-pattern.md` for why).
- **Page indicator updates correctly.** Slide N of M counter reflects the visible slide.

## Cross-slide visual checks

- **Cover slide uses `.s-cover`.** Centered, no header chrome, brand mark in the eyebrow (user's own brand mark in Mode B; no pack mark).
- **Content slides use `.s-content` or type-pack-specific class.** Top-aligned, header chrome present, page indicator visible.
- **Demo slides (pitch slide 6, launch slide 5) use `.s-demo`.** Static screenshot fills the canvas; small "Powered by FluidDocs" attribution mark in the bottom-right corner (FluidDocs logo as inline SVG, ~20px tall, opacity ~0.7, wrapped in `<a href="https://fluiddocs.ai" target="_blank" rel="noopener">`).

## Pass criteria

Every check returns clean. If any check fails, report the slide and the specific issue and a proposed fix.

## Failure modes seen historically

- Slide 4 of a pitch deck had `justify-content: center` because the author treated it like a hero slide. At 850px of content, the top got pushed off-screen at 1440x810.
- Sales deck slide 7 embedded a chart with `aspect-ratio: 16/9` but no `max-height`. Chart filled 920px on a 540px-budget slide.
- All-hands deck used `font-size: 1vw` for body text. Worked at desktop, illegible at iPhone portrait after scale.
- Edit toggle implemented with `.hotzone:hover ~ .toggle { display: block }`. Broke because `.toggle` had `pointer-events: none`. Needed JS with 400ms grace timeout.

When you see one of these, add a new line to `references/learnings-log.md` so the next pass catches it earlier.

## Output format

```
Layout Reviewer: PASS
(or)
Layout Reviewer: FAIL · 2 items
  1. Slide 4 uses `justify-content: center` on `.s-content`. Content projected 870px on 810px canvas. Change to `flex-start`.
  2. iPhone portrait: deck does not letterbox. Missing `transform: scale(...)` on `.deck-outer`. See shell-pattern.md.
```
