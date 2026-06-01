# Timeline / Gantt Patterns for Roadmap Slides

Conversion-mode recipes for milestones-over-time slides (roadmap, phases, quarterly plan, OKR timeline).

Use this file whenever a slide's spine role is `Roadmap`, `Phase 1`, `Phase 2`, `Milestones`, `Annual Plan`, or any time-axis-with-activity-cells layout.

## When to use which

| Pattern | When | Example slide |
|---|---|---|
| **A · Uniform-width** | All milestones span exactly 1 quarter | Phase 2 deck with one activity per quarter |
| **B · Variable-width** (`grid-column: span N`) | Some activities span multiple quarters (Prototyping spans Q3+Q4) | Phase 1 with development phases |
| **C · Explicit absolute placement** (`grid-column: X / span N`) | Below-arrow / secondary rows where cells start at specific quarters with gaps | "Select Product Placement at Q2-Q4 2026, Begin Fulfilling at Q1 2027" |
| **D · Layered/overlapping** | Two activities literally overlap in time (handoff bands) | "BFD starts at Q4 2026 while SPP ends at Q4 2026" |

Always start with the simplest pattern that fits the user's spec. Escalate only when needed.

---

## Pattern A, Uniform-width gantt

Use this when every milestone is one quarter wide. Cleanest, easiest to read.

**HTML**:
```html
<div class="gantt">
  <div class="gantt-header">
    <div class="cell row-label">Timing</div>
    <div class="cell">Q1 2027</div>
    <div class="cell">Q2 2027</div>
    <div class="cell">Q3 2027</div>
    <div class="cell">Q4 2027</div>
    <div class="cell">Q1 2028</div>
    <div class="cell">Q2 2028</div>
    <div class="cell">Q3 2028</div>
    <div class="cell">Q4 2028</div>
  </div>

  <div class="gantt-row">
    <div class="row-label">Home Single-Serve</div>
    <div class="gantt-cell future">Scale Launch</div>
    <div class="gantt-cell future">Iterate</div>
    <div class="gantt-cell future">Update Run</div>
    <div class="gantt-cell future">Next Dev</div>
    <div class="gantt-cell empty"></div>
    <div class="gantt-cell future">Limited Release</div>
    <div class="gantt-cell empty"></div>
    <div class="gantt-cell empty"></div>
  </div>
</div>
```

**CSS** (canonical, copy verbatim):
```css
.gantt { display: grid; gap: 8px; }
.gantt-header, .gantt-row {
  display: grid;
  grid-template-columns: 130px repeat(8, 1fr);
  gap: 8px;
  align-items: stretch;
}
.gantt-header .cell {
  font-family: var(--mono);
  font-size: 14px;
  letter-spacing: 0.10em;
  color: var(--ink);
  font-weight: 600;
  text-transform: uppercase;
  text-align: center;
  padding: 6px 0;
}
.gantt-row { min-height: 76px; align-items: center; }
.gantt-cell {
  height: 100%;
  display: flex; align-items: center; justify-content: center;
  text-align: center;
  font-size: 13px; line-height: 1.2;
  font-weight: 700;
  padding: 8px 6px;
  border-radius: 4px;
  color: var(--ink);
}
.gantt-cell.completed { background: var(--sage); color: white; }
.gantt-cell.future    { background: var(--amber-2); color: var(--ink); }
.gantt-cell.empty     { background: transparent; }
```

Note the column count in `grid-template-columns` always matches the number of quarter labels. The row-label is its own first column.

---

## Pattern B, Variable-width gantt

Use this when some milestones span multiple quarters. Each cell can declare `style="grid-column: span N"` to occupy N consecutive columns.

**Example: Phase 1 with Prototyping spanning Q3+Q4 2025**:
```html
<div class="gantt-row">
  <div class="row-label">Home Single-Serve</div>
  <div class="gantt-cell completed">IP / Technology Development</div>
  <div class="gantt-cell completed" style="grid-column: span 2;">Prototyping</div>
  <div class="gantt-cell future" style="grid-column: span 2;">Initial Prototype Release</div>
  <div class="gantt-cell future">Initial Production Run</div>
  <div class="gantt-cell future" style="grid-column: span 2;">Full Product Launch</div>
</div>
```

**Math check**: 1 + 2 + 2 + 1 + 2 = 8 (all 8 quarter columns accounted for, no empties needed)

If your spans don't total to the number of quarters, add `<div class="gantt-cell empty"></div>` cells to pad.

---

## Pattern C, Explicit absolute placement

Use this for below-arrow rows where cells start at specific quarters with leading gaps.

**Example: Select Product Placement spans Q2-Q4 2026, Begin Fulfilling at Q1 2027**:
```html
<div class="gantt-row">
  <div class="row-label"></div>
  <div class="gantt-cell empty"></div>
  <div class="gantt-cell empty"></div>
  <div class="gantt-cell empty"></div>
  <div class="gantt-cell empty"></div>
  <div class="gantt-cell future" style="grid-column: span 3;">Select Product Placement; 1.5M to Revenue</div>
  <div class="gantt-cell future">Begin Fulfilling Distributor LOIs</div>
</div>
```

The 4 empty cells take cols 2-5 by default placement. Then the span-3 cell takes cols 6-8. Then the final cell takes col 9.

**Alternative, fully explicit placement** (works when default placement order is hard to reason about):
```html
<div class="gantt-row">
  <div class="row-label"></div>
  <div class="gantt-cell future" style="grid-column: 6 / span 3;">Select Product Placement</div>
  <div class="gantt-cell future" style="grid-column: 9 / span 1;">Begin Fulfilling</div>
</div>
```

`grid-column: 6 / span 3` means "start at column 6, span 3 columns", cols 6, 7, 8.

---

## Pattern D, Overlapping cells

Use this when the user EXPLICITLY wants two activities to overlap in time (e.g., a handoff band). Don't use it to resolve spec conflicts, surface those instead (see "Resolving overlap conflicts" below).

```html
<div class="gantt-row">
  <div class="row-label"></div>
  <div class="gantt-cell future" style="grid-column: 6 / span 3; z-index: 1;">SPP</div>
  <div class="gantt-cell future" style="grid-column: 8 / span 2; z-index: 2; background: var(--amber);">BFD</div>
</div>
```

Both cells occupy column 8. The second cell renders on top (higher z-index). Tweak the background of the upper cell to differentiate it visually, usually a slightly different amber shade or a translucent overlay.

---

## Resolving overlap conflicts in user spec

When a user spec creates an overlap (e.g., "Cell A ends at Q4 2026 AND Cell B starts at Q4 2026"), DO NOT silently pick an interpretation. Surface the conflict and ask:

> "Initial Production Run ends at Q4 2026 and Full Product Launch starts at Q4 2026, those overlap. Pick one:
> (a) Initial Production Run is just Q3 2026 (ends at start of Q4), Full Product Launch is Q4 2026 + Q1 2027
> (b) Initial Production Run is Q3+Q4 2026, Full Product Launch is just Q1 2027
> (c) Literal overlap at Q4 2026 with Pattern D (visual stacking)"

In practice, (a) and (b) are clean grid layouts; (c) is for handoff bands where the overlap is intentional storytelling.

---

## Column header sizing (TIMING row)

Don't use 10 to 11px for column headers; they're unreadable on most projector renders.

**Minimum**: 14px, mono font, ink color (not ink-soft), font-weight 600, uppercase, letter-spacing 0.10em.

Same for the row-label column. Both should read clearly from across a room.

---

## Photo-in-gantt-slide composition

Roadmap slides often have a founder photo or product shot top-right. Common failure: photo overlaps the column headers because the gantt margin-top is too tight.

**Rule**: photo bottom edge + 20px <= gantt top edge. If photo is `top: 48px; height: 156px`, photo bottom = 204px. Gantt must start at >= 224px. With section title at roughly 110px and gantt `margin-top` from title, set the margin-top to >= 150px (yielding gantt start at roughly 260px, comfortable clearance).

Verified working: `margin-top: 150px` is the safe default for any roadmap slide where the photo is `width: 280px; height: 156px` at top-right.
