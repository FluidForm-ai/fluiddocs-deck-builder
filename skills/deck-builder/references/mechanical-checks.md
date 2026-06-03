# Mechanical Checks, Phase 2 Self-Lint Reference

> **Note**: In the OSS pack, the active Phase 3 reviewers are Brand, Copy, and Layout. The mechanical checks below run as a Phase 2 self-lint pass and as the foundation of the Layout Reviewer's structural audit. They are NOT a separate reviewer in the OSS pack.

Every check in this file is fully automatable. No judgment calls. If a check fails, the lint fails. No exceptions, the bar is "all mechanical checks pass or the deck goes back to Phase 2."

This file also runs in Phase 2 as the self-lint pass. Build fixes anything caught here before handing off to Phase 3. If Phase 3's Layout Reviewer still catches something here, that's a Phase 2 regression.

---

## Inputs

- The final `.html` file (`$DECK`).
- The brief file (`$BRIEF`).
- The directory of previously shipped decks for this type (`$CATALOG`, declared in the brief, varies by deck type).

---

## Checks (run in order; any fail = lint fails)

### 1. Script parses cleanly

```bash
node -e "const fs=require('fs');const h=fs.readFileSync('$DECK','utf8');const m=h.match(/<script[^>]*>([\\s\\S]*?)<\\/script>/g)||[];m.forEach((s,i)=>{const body=s.replace(/<\\/?script[^>]*>/g,'');try{new Function(body);console.log('script',i+1,'OK')}catch(e){console.error('script',i+1,'FAIL',e.message);process.exit(1)}})"
```

Fail if any `<script>` body fails `new Function()`. Common causes: `\'` escapes inside single-quoted string literals, stray template-literal backticks.

### 2. No emoji codepoints anywhere

```bash
grep -nP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{1F000}-\x{1F2FF}]" "$DECK"
```

Any match fails.

### 3. No forbidden class-name leaks (type-pack-canonical-brand-ism check)

Each type pack has a canonical reference brand whose class names would leak into non-canonical decks if the build blindly copies from the reference. The brief declares the list; this check greps against it.

The brief delimits the forbidden class-name list with explicit HTML-comment anchors so this extraction never depends on heading formatting or surrounding whitespace. The brief template's section 3 block looks like:

```
<!-- BEGIN forbidden-class-leaks -->
comp-matrix
listing-grid
rausch
belo
belo-mark
<!-- END forbidden-class-leaks -->
```

Extraction:

```bash
# Extract the forbidden class-name list from the brief between the explicit anchors (one per line)
leaks=$(awk '/<!-- BEGIN forbidden-class-leaks -->/,/<!-- END forbidden-class-leaks -->/' "$BRIEF" | grep -v "<!-- " | grep -vE '^\s*$' | tr '\n' '|' | sed 's/|$//')
[ -z "$leaks" ] && { echo "SKIP section 3, brief declares no forbidden class-names (self-verify this is intentional)"; }
[ -n "$leaks" ] && grep -nE "($leaks)" "$DECK" && { echo "FAIL forbidden class-name leak"; exit 1; }
```

Example lists by type pack:
- **deck-pitch** canonical = Airbnb : `comp-matrix|listing-grid|rausch|bélo|belo-mark`
- **deck-sales** canonical = (the reference sales deck's class names once the pack ships)

A deck explicitly mirroring the canonical brand (e.g., the Airbnb pitch deck itself) declares an empty forbidden list in its brief, this check then skips.

### 4. Every scripted DOM target resolves

```bash
node -e "
const fs=require('fs'),h=fs.readFileSync('$DECK','utf8');
const scripts=(h.match(/<script[^>]*>([\\s\\S]*?)<\\/script>/g)||[]).join('\\n');
const ids=[...scripts.matchAll(/getElementById\\(['\\\"]([^'\\\"]+)['\\\"]\\)/g)].map(m=>m[1]);
const sels=[...scripts.matchAll(/querySelector(?:All)?\\(['\\\"]([^'\\\"]+)['\\\"]\\)/g)].map(m=>m[1]);
const missing=[];
ids.forEach(i=>{if(!new RegExp('id=[\\\"\\']'+i+'[\\\"\\']').test(h))missing.push('#'+i);});
if(missing.length){console.error('Missing DOM targets:',missing.join(', '));process.exit(1);}else console.log('All',ids.length+sels.length,'targets present (IDs verified directly, selectors rely on class existence)');
"
```

Any missing ID fails. Class selectors: verify at least one matching `class=\"...\"` attribute exists in markup.

### 5. Every CDN `<img>` has an `onerror` handler

```bash
grep -nE "<img[^>]*src=['\"]https?://(images\\.unsplash|[a-z]+\\.cdn)" "$DECK" | grep -v "onerror"
```

Any match (CDN image WITHOUT onerror) fails.

### 6. No hand-crafted brand-letter paths

```bash
# Flag any <path> with > 60 chars of d-attribute inside an SVG < 80px viewBox
# Hand-crafted letter paths tend to be short, complex, and inside small viewBoxes.
grep -nE '<svg[^>]*viewBox=\"0 0 (6[0-9]|7[0-9]) (6[0-9]|7[0-9])\"' "$DECK" | head -5
# Manual follow-up: for each match, confirm either <text>-based rendering or an inlined brand SVG from press kit.
```

Not strictly mechanical, but flagged patterns must be justified in the review note. Fail if hand-crafted `<path>` approximates a letter AND the deck is Mode A for a brand whose logo is available from press kit.

### 6b. Nested-subpath brand SVGs declare `fill-rule="evenodd"`

```bash
# Any <path> whose d-attribute contains 2+ 'z' terminators is a multi-subpath shape
# (the Airbnb bélo, Stripe stroked wordmarks, any logo with inner cutouts).
# Without fill-rule="evenodd" the nested shapes stack solid under the default
# nonzero rule, the logo renders as a blob with weird edges.
node -e "
const fs=require('fs'), h=fs.readFileSync('$DECK','utf8');
const paths = [...h.matchAll(/<path\\b[^>]*d=\"([^\"]+)\"[^>]*>/g)];
const bad = paths.filter(p => (p[1].match(/z/gi)||[]).length >= 2 && !/fill-rule=\"evenodd\"/.test(p[0]));
if (bad.length) { console.error('FAIL, nested-subpath <path> missing fill-rule=evenodd:'); bad.forEach(b=>console.error('  ',b[0].slice(0,120)+'...')); process.exit(1); }
console.log('OK');
"
```

Fail if any `<path>` with >=2 subpaths lacks `fill-rule="evenodd"`. Rule introduced after the Airbnb-Deck bélo shipped as a solid blob, three nested subpaths (inner heart, middle loop, outer shell) rendered as a filled mass with no thin-line cutouts under the default nonzero fill rule.

### 7. File size (hard ceiling, advisory floor)

File size is an output, not a target. Never add content, markup, or whitespace to move the byte count. Substance is enforced by the content-density targets in the type pack's content-spine and by section 8 (section count), not by bytes. A complete, concise deck that lands under the old 60K mark still passes.

```bash
size=$(wc -c < "$DECK")
# Hard ceiling only: over 180K means runaway markup or an oversized inline asset.
if [ "$size" -gt 180000 ]; then echo "FAIL size=$size (over 180000 ceiling)"; exit 1; fi
# Advisory floor: a very small file is a hint to recheck content-density, not a fail. Do NOT pad.
if [ "$size" -lt 40000 ]; then echo "WARN size=$size (small: recheck spine content-density targets; do NOT pad bytes)"; fi
```

### 8. Section count matches brief

The brief declares the target slide count, pitch defaults to 14, sales defaults to 11, keynote may target 28+, etc. This check reads the brief and enforces the declared number.

```bash
count=$(grep -cE '<section class="slide' "$DECK")
expected=$(awk -F': *' '/\*\*Target slide count\*\*/ {gsub(/[^0-9]/,"",$2); print $2; exit}' "$BRIEF")
if [ -z "$expected" ]; then
  echo "FAIL brief is missing **Target slide count** field"; exit 1
fi
if [ "$count" -ne "$expected" ]; then
  echo "FAIL section count=$count (brief declared $expected)"; exit 1
fi
echo "PASS section count=$count matches brief's declared $expected"
```

If the type pack allows a range (e.g., pitch: 11 min / 13 max content slides + Cover + optional Ask = 12 to 14 total), the brief declares the chosen exact number and this check enforces that number. Range validation happens in the brief-approval gate (Phase 1), not here.

### 9. Every `font-size` matches the brief's declared scale

If the brief uses a named style preset (Founder Default, Quiet Confident, Studio Bold, Editorial Serif, Tech Crisp, Warm Brand), the declared scale is the one published in `references/style-presets.md` under that preset. Copy it verbatim into the brief's section 5 so this lint can diff against it. If the brief uses a custom scale, declare every allowed size in section 5 with a one-line role per size. Either way, every `font-size` value in the final CSS must match one of the declared sizes.

Extract every `font-size` value from the deck's CSS. Compare against the scale declared in the brief (section 5).

```bash
node -e "
const fs=require('fs');
const h=fs.readFileSync('$DECK','utf8');
const brief=fs.readFileSync('$BRIEF','utf8');
const sizesInDeck=[...h.matchAll(/font-size:\\s*([0-9.]+(px|rem|em))/g)].map(m=>m[1]);
const scaleDeclared=[...brief.matchAll(/^\\s*-\\s*([0-9.]+px)\\s*[·,]/gm)].map(m=>m[1]);
const unique=[...new Set(sizesInDeck)];
const drift=unique.filter(s=>!scaleDeclared.includes(s));
if(drift.length){console.error('Off-scale sizes in deck:',drift.join(', '));process.exit(1);}else console.log('All',unique.length,'sizes match declared scale');
"
```

### 10. CSS palette tokens match brief

Extract `:root` custom properties from the deck. Compare against brief section 4.

```bash
node -e "
const fs=require('fs');
const h=fs.readFileSync('$DECK','utf8');
const brief=fs.readFileSync('$BRIEF','utf8');
const root=(h.match(/:root\\s*\\{[^}]+\\}/)||[])[0]||'';
const inDeck=[...root.matchAll(/--[a-z-]+:\\s*(#[0-9a-fA-F]{3,8})/g)].map(m=>m[1].toLowerCase());
const inBrief=[...brief.matchAll(/#([0-9a-fA-F]{6})/g)].map(m=>'#'+m[1].toLowerCase());
const drift=inDeck.filter(c=>!inBrief.some(b=>b.includes(c.slice(1))||c.includes(b.slice(1))));
if(drift.length)console.error('Palette drift (in deck but not in brief):',drift.join(', '));
"
```

Warn (not hard-fail) on drift, brief might omit shades. Confirm with user if flagged.

### 11b. No hidden-content filler (anti-gaming)

Build sub-agents have been observed adding a `<div style="display: none">` or `visibility: hidden` block full of padding to clear the section 7 file-size floor without writing real visible content. This is an automatic HARD FAIL.

Rule: the ONLY legal `display: none` / `visibility: hidden` / `opacity: 0` occurrences are:
- The base `.slide { display: none }` toggle rule (Variant A shell)
- The base `.slide { opacity: 0 }` transition rule (opacity-hiding shell)
- CSS pseudo-class state rules (`:hover`, `.active`, etc.)

Any additional instance, inline on an element, or a new CSS rule on a non-slide selector used to hide a block of content, fails the check.

```bash
# Count every inline or CSS-rule hide token OUTSIDE the two base .slide rules
# Count all occurrences
total_hides=$(grep -cE 'display:\s*none|visibility:\s*hidden|opacity:\s*0' "$DECK")

# Count the legal base-slide occurrences
base_display=$(grep -cE '^\s*display:\s*none;?\s*$' "$DECK")  # inside .slide { ... }
base_opacity=$(grep -cE '^\s*opacity:\s*0;?\s*$' "$DECK")     # inside .slide { ... }

# Inline style attributes using hide tokens, always illegal
inline_hides=$(grep -cE 'style="[^"]*(display:\s*none|visibility:\s*hidden|opacity:\s*0)' "$DECK")
[ "$inline_hides" -gt 0 ] && { echo "FAIL inline hide tokens found ($inline_hides), anti-gaming check"; grep -nE 'style="[^"]*(display:\s*none|visibility:\s*hidden)' "$DECK"; exit 1; }

# Pseudo-class rules like `.slide.active { display: flex }` are fine, the check above only flags inline hides.
# Manual follow-up for CSS rules beyond the two base ones: confirm each is a pseudo-class / state rule, not content-hiding.
echo "PASS no inline hidden-content filler (total display:none/visibility:hidden/opacity:0 tokens=$total_hides; inline=$inline_hides)"
```

Recommended build pattern: use **opacity-based slide hiding** (all slides always in DOM, `.slide { opacity: 0 }` base rule + `.slide.active { opacity: 1 }` toggle, zero `display: none` usage). This makes the anti-gaming check trivial: any `display: none` grep hit anywhere in the file is an automatic red flag.

### 11c. No inline `justify-content: center` on `<section class="slide">`

The shell pattern's "layout bug" section warns that center-aligning a content slide can overflow the 810px canvas (top half bleeds under the brand-mark). A build sub-agent that needs centered content on a specific slide must define a dedicated CSS class (`.s-cover`, `.s-closing`, `.s-thanks`, etc.), not apply `justify-content: center` inline.

```bash
grep -nE '<section class="slide[^"]*"\s+style="[^"]*justify-content:\s*center' "$DECK" && {
  echo "FAIL inline justify-content: center on <section class=\"slide\">, define a dedicated class instead"
  exit 1
}
echo "PASS no inline center on section.slide"
```

### 11. Meta-check: no unresolved `[REPLACE]` markers the user didn't sanction

Count `[REPLACE]` markers. If the brief says "Mode A template with `[REPLACE]` scaffolding" the count is expected; if the brief says "actual investor pitch" it should be 0.

```bash
count=$(grep -cE "\\[REPLACE" "$DECK")
echo "[REPLACE] count: $count"
# Compare to brief expectation
```

---

## Pass/fail report format

```
Mechanical Self-Lint: PASS / FAIL

[PASS] Script parses clean
[PASS] No emoji codepoints
[PASS] No Airbnb-isms (N/A, Airbnb deck)
[FAIL] Missing DOM target: #hero-cta referenced in script, not in markup
[PASS] CDN images have onerror
[PASS] No hand-crafted letter paths
[PASS] File size 94832 bytes (in range)
[PASS] 14 sections
[PASS] All font-sizes match declared scale
[WARN] Palette drift: #F4F0EB in deck, closest brief value #F5F1EB
[PASS] [REPLACE] count: 7 (brief expected 5 to 10)

Action: fix #hero-cta (add element to markup or remove script reference). Verify #F4F0EB vs #F5F1EB with user.
```

---

## When this lint fires a new check

Every user-reported mechanical issue after delivery adds a check here. Log the date + source build + check added in `references/learnings-log.md`.

Past additions:
- Script parse check, added after a `\'` escape bug.
- DOM target resolution, added after a missing-ID bug caused silent nav failure.
- `font-size` vs declared scale, added to enforce typographic discipline.
- Palette CSS-vs-brief diff, added to catch neon-drift edge cases.
- Section count parameterized from brief (section 8), added so non-pitch types (sales, keynote, etc.) can declare their own targets.
- Forbidden class-name leaks parameterized from brief (section 3), type-pack-canonical brand-ism check now generic across types.
- Hidden-content filler check (section 11b), automatic hard fail on any inline hide token.
- Inline center-overflow check (section 11c), automatic hard fail.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
