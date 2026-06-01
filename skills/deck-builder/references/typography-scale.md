# Typography Scale, Reference

> **Note**: In the OSS pack, the active Phase 3 reviewers are Brand, Copy, and Layout. Typography Scale is kept as a Phase 2 implementation reference and a Layout Reviewer sub-check rather than its own reviewer.

**Category covered**: typography scale drift, within-deck + cross-catalog.

Goal: prevent the "Sequoia-had-18-distinct-font-sizes" bug, the "LinkedIn-text-too-small" bug, and the "every deck uses a different scale" cross-catalog drift.

The mechanism is simple: the brief declares a scale. Every `font-size` in the shipped CSS must match one of the declared values. Exceptions require a brief update.

---

## Inputs

- The final `.html` (`$DECK`)
- The brief (`$BRIEF` section 5, declared typographic scale)

---

## Checks

### 1. Every `font-size` value matches the declared scale

Fully mechanical. Extract every `font-size` from the deck's CSS; diff against the scale.

```bash
node -e "
const fs=require('fs');
const h=fs.readFileSync('$DECK','utf8');
const brief=fs.readFileSync('$BRIEF','utf8');
const sizes=[...h.matchAll(/font-size:\\s*([0-9.]+)(px|rem|em)/g)].map(m=>m[1]+m[2]);
const scale=[...brief.matchAll(/^\\s*-\\s*([0-9.]+)(px|rem|em)\\s*[·,]/gm)].map(m=>m[1]+m[2]);
const unique=[...new Set(sizes)];
const off=unique.filter(s=>!scale.includes(s));
console.log('Sizes in deck:',unique.length,'Declared scale:',scale.length,'Off-scale:',off.length);
if(off.length){console.error('Off-scale:',off.join(', '));process.exit(1);}
"
```

Fail on any off-scale value.

### 2. Distinct size count <=7

Even if every size is declared, more than 7 distinct sizes in a 14-slide deck is a design smell. Sequoia had 18 and it read as chaotic. Target: 5 to 7.

```bash
grep -oE 'font-size:\s*[0-9.]+(px|rem|em)' "$DECK" | sort -u | wc -l
```

Fail if >7.

### 3. Minimums

- Body prose: >=14px
- Card body text: >=13.5px
- Metric numerals (the big stats on traction/market slides): >=22px
- Footnotes / citations / monospace metadata: >=10px (smaller than this is illegible)
- Slide `h2`: >=22px (the audience is reading from across a room in the worst case)

```bash
# Hunt for any body class with sub-14px
grep -nE '\.(lead|body|card-body|prose)[^{]*\{[^}]*font-size:\s*1[0-3]' "$DECK"
```

### 4. Consistency across similar elements

- All `h3` headers same size within the deck.
- All card titles same size.
- All metric stats same size (unless intentional hierarchy is declared in the brief).
- All eyebrows / slide-metas same size.
- All button text same size.

```bash
# Extract all h3 font-sizes
grep -nE 'h3\s*\{[^}]*font-size' "$DECK"
# Visual check, every h3 rule should resolve to the same size
```

### 5. Brand-appropriate display font

The brief's section 4 declared the display font. Verify the deck's `@import` line and `font-family` declarations match.

```bash
grep -nE "font-family:\s*'[^']+'" "$DECK" | sort -u
grep -nE "fonts.googleapis.com.*css2\?family=" "$DECK"
```

Flag if the imported font doesn't match the brief.

---

## Per-brand reference scales (seed data, extend as builds land)

These are the scales observed in the shipped decks. When starting a new deck in one of these brands, use this as the starting point for the brief.

### Airbnb

- 10px slide-meta, 12px counter
- 13px card body
- 15px lead body
- 20px section/h3
- 28px slide h2
- 44px cover / hero

Display: Poppins (stand-in for Cereal). Body: Inter.

### Uber

- 10px mono counter
- 12px slide-meta mono
- 14px body
- 16px lead
- 22px section/h3
- 34px slide h2
- 56px cover / hero big-number
- JetBrains Mono heavy use for numbers + labels

Display: Inter tight-tracking (-0.04em). Body: Inter.

### Stripe (anticipated, add after build)

- expected ~5-size scale, mono heavy for API-doc aesthetic

### Sequoia Classic (anticipated, avoid past 18-size bug)

- 10px slide-meta / monospace counter
- 11px footnotes
- 13.5px card body
- 15.5px lead paragraphs
- 19px section heads / h3
- 26px slide h2
- 38px cover / hero stat

Display: Fraunces (stand-in for Tiempos). Body: Inter.

Target: stay at these 7; do NOT add additional intermediary sizes during the build. If a slide feels like it needs a size not in the scale, that's a signal the layout or hierarchy is wrong, not that the scale needs to grow.

### Databricks (anticipated)

- expected DM Sans display + Inter body + JetBrains mono for metrics
- roughly 6-size scale

### Others

Fill in as shipped.

---

## Pass/fail report format

```
Typography (sub-check): PASS / FAIL

Brief declared scale: 10 / 12 / 14 / 22 / 34 / 56 px (Uber)

[PASS] All font-sizes in CSS match declared scale (14 distinct uses, 6 distinct sizes)
[PASS] Distinct size count: 6 (<=7 target)
[PASS] Minimums: body 14px OK, cards 14px OK, metrics 34px OK
[FAIL] Consistency: .card h3 is 22px on problem/moat slides, 20px on traction slide
[PASS] Display font matches brief: Inter + JetBrains Mono

Action: fix .card h3 on traction slide to 22px.
```

---

## Extending this reference

New scales: add a per-brand section above after each build. Observed per-brand scales become the starting template for that brand's future rebuilds.

New per-element minimums: if a user flags "text too small" on a specific element type in a new slide category, add the minimum rule here. Log in `learnings-log.md` under the typography category.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
