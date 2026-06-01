# Shell Pattern · Fixed-Canvas, Chrome-Free

Every template uses the same minimal, brand-native navigation AND the same fixed 1440×810 design canvas. Decks are not responsive, they are PDFs rendered in HTML. The whole composition scales proportionally to fit whatever viewport it's in, letterboxed with brand-neutral bands on the sides or top/bottom.

There are three floating nav elements and one wrapper. Together they produce the "looks identical on every screen" behavior the user expects.

## The wrapper model (this is the most important part)

```
.deck-outer        ← viewport-sized flex centerer (100vw × 100vh), dark neutral background
  └── .deck       ← fixed 1440 × 810, scaled via CSS transform
       ├── .slide.active ← 1440 × 810, absolutely positioned, one visible at a time
       ├── .slide ...
       └── .brand-mark / .slide-meta per slide (positioned absolutely inside slide)
       └── .progress-line / .nav-counter / .nav-arrows ← also scaled (live inside .deck so they scale too)
```

`.deck` has fixed pixel dimensions (1440 × 810). `.deck-outer` uses flexbox to center `.deck` in the viewport, and a JS `setScale()` function sets `.deck`'s `transform: scale(...)` to the smaller of `winW/1440` and `winH/810`. Overflow outside the canvas is hidden (letterboxed by `.deck-outer`).

## Two equivalent navigation variants

The shell supports two interchangeable patterns for moving between slides. Both live inside the same `.deck-outer → .deck` frame; pick based on which feels more natural for the brand.

### Variant A · Toggle (`.slide.active`)

One slide is visible at a time, opacity-cross-faded. Slides are absolutely positioned, all stacked at `inset: 0`. This is the pattern shown in the scaffold below. Use for: editorial/serif brands (Harvey, Sequoia), anywhere a PDF-like single-page feel is wanted, any deck where slides vary visually enough that a cross-fade reads cleaner than a horizontal slide.

```
.deck-outer
  └── .deck          (overflow: hidden)
       ├── .slide.active  ← visible (opacity: 1)
       ├── .slide         ← hidden (display: none, opacity: 0)
       └── .slide ...
       └── .progress-line / .nav-counter / .nav-arrows
```

### Variant B · Horizontal scroll (`.deck-strip` translateX)

All 14 slides always rendered side-by-side in a flex row inside a translating strip; `transform: translateX(-index * 1440px)` on the strip slides them left/right. Use for: brands with kinetic, motion-forward identities, any deck where the "moving through a story" affordance helps narrative flow.

```
.deck-outer
  └── .deck                    (overflow: hidden, this is the clipping window)
       └── .deck-strip         (flex row, width: max-content)
            ├── .slide         (flex: 0 0 1440px)
            ├── .slide
            └── ...
       └── .progress-line / .nav-counter / .nav-arrows   ← siblings of .deck-strip, NOT children
```

Key constraints for Variant B:

- `.deck-strip` gets `display: flex; width: max-content;` and its `transform: translateX(...)` drives navigation. Do NOT use `width: calc(var(--slide-count) * 100vw)`, the canvas is fixed pixels, not vw.
- `.slide` gets `flex: 0 0 1440px; height: 810px;` (no `inset: 0`).
- Navigation JS translates the strip: `deckStrip.style.transform = 'translateX(' + (-index * 1440) + 'px)';`
- `setScale()` still targets `.deck` (the outer 1440×810 box), not the strip. The strip translates inside the already-scaled canvas.
- `.progress-line`, `.nav-counter`, `.nav-arrows`, `.brand-mark`, `.slide-meta` all live as direct children of `.deck` (siblings of `.deck-strip`), so they DON'T translate with the strip. This is the easiest thing to get wrong, see the migration trap below.

### Migration trap (kinetic shell)

Older decks sometimes placed `.brand-mark`, `.nav-counter`, or `.nav-dots` OUTSIDE `.deck` (as siblings of `.deck-outer`, or attached to `body`). When migrating to fixed canvas, these must move INSIDE `.deck` (and outside `.deck-strip` if Variant B) so they scale with the canvas and stay anchored while the strip translates. Symptom when wrong: nav elements stay at a fixed pixel size and sit in the letterbox bands instead of on the deck.

**Why this design**:
- Design once at 1440×810, render everywhere at that exact aspect ratio.
- Mobile portrait shows the deck scaled down, horizontally centered, letterboxed top/bottom, never reflowed.
- Ultrawide shows the deck scaled up to fit height, letterboxed left/right.
- Nav chrome (progress line, counter, arrow buttons) lives inside `.deck` so it scales with the deck, preserving the "PDF-like" feel.
- No `@media` breakpoints. No responsive behavior. Ever.

## The three nav elements

1. **Progress line** · 3px tall bar pinned to top of the 1440×810 canvas. Width scales with current slide position (1/14 = ~7.1%). Background: brand primary color.
2. **Slide counter** · bottom-left of the canvas, monospace, muted grey. Format: `01 / 14`.
3. **Arrow buttons** · bottom-right of the canvas, two circles (~42px). Prev = left-pointing chevron. Next = right-pointing chevron. Border = brand primary; fill = transparent; on hover, fill = brand primary and arrow inverts to white.

All three sit inside `.deck` (not on `.deck-outer`), so they scale with the deck transform. They use `position: absolute` (not `fixed`), their coordinate system is the 1440×810 canvas.

## HTML scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{Brand} · Pitch Deck Template</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={DisplayFont}:wght@400;500;600;700;800&family={BodyFont}:wght@400;500;600&display=swap" rel="stylesheet">
<style>/* === design tokens + slide styles === */</style>
</head>
<body>
  <!-- Inline-edit hotzone + toggle (see "Inline-edit module" below) -->
  <div class="edit-hotzone" aria-hidden="true"></div>
  <button class="edit-toggle" id="editToggle" title="Edit mode (E)" aria-label="Toggle edit mode">Edit</button>

  <div class="deck-outer">
    <div class="deck">
      <section class="slide s-cover active">...</section>
      <section class="slide s-problem">...</section>
      <!-- ... 12 more ... -->
      <section class="slide s-ask">...</section>

      <div class="progress-line"></div>
      <div class="nav-counter"><span class="cur">01</span> / <span class="total">14</span></div>
      <div class="nav-arrows">
        <button class="nav-btn prev" aria-label="Previous slide">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <button class="nav-btn next" aria-label="Next slide">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>
    </div>
  </div>

<script>/* === nav controller + setScale + inline-edit module === */</script>
</body>
</html>
```

## CSS · the critical parts

```css
:root {
  /* Brand tokens, pulled from references/brand-tokens.md */
  --primary: #FF5A5F;        /* swap per brand */
  --ink: #222222;
  --muted: #767676;
  --surface: #FFFFFF;
  --paper: #F7F7F7;
  --border: #DDDDDD;
  --letterbox: #0A0A0A;      /* dark neutral for bands outside canvas; override for light-brand PDFs */
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  height: 100%;
  overflow: hidden;
  background: var(--letterbox);
  color: var(--ink);
  font-family: '{BodyFont}', sans-serif;
}

/* Viewport-sized centerer. Letterbox bands live here. */
.deck-outer {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--letterbox);
  overflow: hidden;
}

/* The fixed design canvas. Scaled by JS via transform. */
.deck {
  position: relative;
  width: 1440px;
  height: 810px;
  background: var(--surface);
  transform-origin: center center;
  /* transform: scale(...) set by setScale() at runtime */
  overflow: hidden;
  flex-shrink: 0;
}

.slide {
  position: absolute;
  inset: 0;
  /* Top padding MUST clear brand-mark (top:32) + its height (~26) + breathing room.
     104px is the proven safe minimum on the 1440×810 canvas. */
  padding: 104px 96px 96px;
  display: none;
  flex-direction: column;
  justify-content: flex-start;  /* CRITICAL, see "The layout bug" section below */
  overflow: hidden;              /* fixed-canvas = no scroll inside slides */
  background: var(--surface);
  opacity: 0;
  transition: opacity 300ms ease;
}
.slide.active { display: flex; opacity: 1; }

/* Cover is the one content slide that SHOULD vertically center, since it always fits */
.s-cover { justify-content: center; padding: 96px 120px; }

/* Floating nav, positioned inside .deck, so transforms scale them with the deck */
.progress-line {
  position: absolute; top: 0; left: 0;
  height: 3px;
  background: var(--primary);
  width: 7.14%; /* updated by JS */
  transition: width 300ms ease;
  z-index: 100;
}
.nav-counter {
  position: absolute; bottom: 24px; left: 32px;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 12px; letter-spacing: 0.08em;
  color: var(--muted);
  z-index: 100;
}
.nav-arrows {
  position: absolute; bottom: 20px; right: 32px;
  display: flex; gap: 10px;
  z-index: 100;
}
.nav-btn {
  width: 42px; height: 42px; border-radius: 50%;
  border: 1.5px solid var(--border);
  background: transparent;
  color: var(--ink);
  cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center;
  transition: all 180ms ease;
}
.nav-btn:hover { border-color: var(--primary); background: var(--primary); color: white; }
.nav-btn svg { width: 16px; height: 16px; }

/* Brand-mark top-left on content slides (NOT cover, cover has its own wordmark hero) */
.brand-mark {
  position: absolute; top: 32px; left: 48px;
  display: flex; align-items: center; gap: 10px;
  z-index: 5;
  color: var(--ink);
  font-family: '{DisplayFont}', sans-serif;
  font-weight: 800; font-size: 1rem;
  letter-spacing: -0.04em;
}
.brand-mark svg { width: 26px; height: 26px; }

.slide-meta {
  position: absolute; top: 32px; right: 48px;
  z-index: 5;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.72rem; color: var(--muted);
  letter-spacing: 0.06em; font-weight: 600;
}

/* ===========================================
   INLINE-EDIT MODULE · hotzone + toggle styles
   Visibility is controlled by JS classes ONLY.
   Do NOT use a CSS `~` sibling selector, see the
   "Inline-edit module" section for why it breaks.
   =========================================== */
.edit-hotzone {
  position: fixed;
  top: 0;
  left: 0;
  width: 40px;
  height: 40px;
  z-index: 10000;
  cursor: pointer;
  /* Invisible, but interactive */
  background: transparent;
}
.edit-toggle {
  position: fixed;
  top: 12px;
  left: 12px;
  z-index: 10001;
  padding: 6px 12px;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  color: var(--ink);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, background 0.15s ease, color 0.15s ease;
}
.edit-toggle.show,
.edit-toggle.active {
  opacity: 1;
  pointer-events: auto;
}
.edit-toggle.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

/* Visual treatment for the editable elements when edit mode is on. */
body.edit-mode [contenteditable="true"] {
  outline: 1px dashed var(--primary);
  outline-offset: 2px;
  cursor: text;
}
body.edit-mode [contenteditable="true"]:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

## JS · the nav controller + setScale

```js
(function() {
  const deck = document.querySelector('.deck');
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  let current = 0;

  const progress = document.querySelector('.progress-line');
  const counter = document.querySelector('.nav-counter .cur');
  const totalEl = document.querySelector('.nav-counter .total');
  const prevBtn = document.querySelector('.nav-btn.prev');
  const nextBtn = document.querySelector('.nav-btn.next');

  totalEl.textContent = String(total).padStart(2, '0');

  // ---------- Fixed-canvas scale-to-fit ----------
  function setScale() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const scale = Math.min(w / 1440, h / 810);
    deck.style.transform = `scale(${scale})`;
  }
  setScale();
  window.addEventListener('resize', setScale);
  window.addEventListener('orientationchange', setScale);

  // ---------- Slide navigation ----------
  function go(to) {
    if (to < 0 || to >= total) return;
    slides[current].classList.remove('active');
    current = to;
    slides[current].classList.add('active');
    progress.style.width = `${((current + 1) / total) * 100}%`;
    counter.textContent = String(current + 1).padStart(2, '0');
  }

  const next = () => go(current + 1);
  const prev = () => go(current - 1);

  prevBtn.addEventListener('click', prev);
  nextBtn.addEventListener('click', next);

  // Keyboard
  document.addEventListener('keydown', (e) => {
    // Don't hijack arrow keys while the user is editing text inline.
    const editingText = e.target && e.target.getAttribute &&
                        e.target.getAttribute('contenteditable') === 'true';
    if (editingText) return;

    if (['ArrowRight', ' ', 'PageDown'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { e.preventDefault(); go(0); }
    else if (e.key === 'End') { e.preventDefault(); go(total - 1); }
  });

  // Touch swipe
  let tx = 0;
  document.addEventListener('touchstart', (e) => { tx = e.changedTouches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 60) dx < 0 ? next() : prev();
  }, { passive: true });
})();
```

## Inline-edit module

This module gives any reader of the rendered HTML a low-friction way to edit the deck in place, autosave to `localStorage`, and download the edited file. The agent ships every deck with it, no Phase 1 opt-in required.

**Why a JS-driven hotzone and not a CSS sibling selector.** A naive implementation puts a tiny invisible hotzone in the top-left and shows an "Edit" toggle button via `.hotzone:hover ~ .toggle { display: block }`. That pattern BREAKS because `.toggle` has `pointer-events: none` while hidden (otherwise it would intercept clicks on the underlying canvas). The first time the user's cursor leaves the hotzone to reach the toggle, the toggle vanishes mid-flight: hover left the hotzone, no `pointer-events` on the toggle to stay in the hover chain, CSS hides it again before the click lands.

The fix: drive show/hide entirely from JS with a 400ms grace timeout. `mouseenter` on the hotzone (or on the toggle itself) clears any pending hide and adds `.show`. `mouseleave` from either element schedules a hide after 400ms. That window is long enough for a normal mouse to bridge the gap between the 40px hotzone and the toggle button.

### Behavior contract

- **Hotzone**: 40px × 40px invisible div pinned to the top-left of the viewport (`position: fixed; top:0; left:0`).
- **Hover-in**: after 0ms, the toggle gets `.show`. (Add the class on `mouseenter`, no delay.)
- **Hover-out**: a 400ms `setTimeout` hides the toggle. Re-entering the hotzone OR entering the toggle button itself clears the pending timeout.
- **E key**: toggles edit mode globally, EXCEPT when focus is inside a `[contenteditable="true"]` element (otherwise the user typing the letter "e" would flip modes).
- **Click on toggle or click on hotzone**: toggles edit mode.
- **Edit mode on**: `<body>` gets `.edit-mode`. The toggle gets `.active`. Every text-bearing element (`h1, h2, h3, h4, p, li, span, .eyebrow, .lead, .fact, .stat-label, .stat-value`, etc.) gets `contenteditable="true"`.
- **Autosave**: on every `input` event inside the deck, debounce by ~500ms then snapshot the entire `<body>` innerHTML to `localStorage` keyed by `location.pathname`. On load, if a saved snapshot exists for this path, restore it before wiring up nav.
- **Ctrl+S / Cmd+S**: prevent the browser save dialog, download the current document HTML as a `.html` file named after the page title.

### Implementation

```js
(function() {
  // ---------- Inline-edit state ----------
  const STORAGE_KEY = 'deck-edits:' + location.pathname;
  const SAVE_DEBOUNCE_MS = 500;
  const HOVER_GRACE_MS = 400;

  const editor = {
    isActive: false,
    saveTimer: null,
    hideTimer: null,
  };

  // List of selectors that become editable when edit mode is on.
  // Tuned to text-bearing slide elements; extend as needed per template.
  const EDITABLE_SELECTORS = [
    '.slide h1', '.slide h2', '.slide h3', '.slide h4',
    '.slide p', '.slide li', '.slide blockquote',
    '.slide .eyebrow', '.slide .lead', '.slide .fact',
    '.slide .stat-label', '.slide .stat-value',
    '.slide .quote', '.slide .attribution',
    '.brand-mark', '.slide-meta'
  ];

  // ---------- Restore prior edits before anything else renders interactively ----------
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      // Replace body innerHTML; the script tags re-execute is intentional
      // for inline-edit + nav re-binding because the IIFE is one-shot.
      // Safer pattern: only restore the .deck subtree.
      const parser = new DOMParser();
      const doc = parser.parseFromString(saved, 'text/html');
      const restoredDeck = doc.querySelector('.deck');
      const liveDeck = document.querySelector('.deck');
      if (restoredDeck && liveDeck) liveDeck.innerHTML = restoredDeck.innerHTML;
    }
  } catch (e) {
    console.warn('Inline-edit restore failed:', e);
  }

  // ---------- Toggle wiring ----------
  const hotzone = document.querySelector('.edit-hotzone');
  const toggle = document.getElementById('editToggle');

  function showToggle() {
    clearTimeout(editor.hideTimer);
    toggle.classList.add('show');
  }
  function scheduleHideToggle() {
    clearTimeout(editor.hideTimer);
    editor.hideTimer = setTimeout(() => {
      if (!editor.isActive) toggle.classList.remove('show');
    }, HOVER_GRACE_MS);
  }

  hotzone.addEventListener('mouseenter', showToggle);
  hotzone.addEventListener('mouseleave', scheduleHideToggle);
  toggle.addEventListener('mouseenter', showToggle);
  toggle.addEventListener('mouseleave', scheduleHideToggle);

  hotzone.addEventListener('click', () => toggleEditMode());
  toggle.addEventListener('click', () => toggleEditMode());

  // ---------- E key (skip when typing) ----------
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'e' && e.key !== 'E') return;
    const inEditable = e.target && e.target.getAttribute &&
                       e.target.getAttribute('contenteditable') === 'true';
    if (inEditable) return;
    // Don't fight modifier combos (Ctrl+E, Cmd+E)
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    e.preventDefault();
    toggleEditMode();
  });

  // ---------- Ctrl+S / Cmd+S download ----------
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      downloadHtml();
    }
  });

  // ---------- Toggle edit mode ----------
  function toggleEditMode() {
    editor.isActive = !editor.isActive;
    document.body.classList.toggle('edit-mode', editor.isActive);
    toggle.classList.toggle('active', editor.isActive);
    toggle.classList.add('show'); // keep visible while editing

    const targets = document.querySelectorAll(EDITABLE_SELECTORS.join(','));
    targets.forEach(el => {
      if (editor.isActive) {
        el.setAttribute('contenteditable', 'true');
        el.setAttribute('spellcheck', 'true');
      } else {
        el.removeAttribute('contenteditable');
        el.removeAttribute('spellcheck');
      }
    });

    if (!editor.isActive) scheduleHideToggle();
  }

  // ---------- Debounced autosave ----------
  document.addEventListener('input', (e) => {
    if (!e.target || !e.target.getAttribute) return;
    if (e.target.getAttribute('contenteditable') !== 'true') return;
    clearTimeout(editor.saveTimer);
    editor.saveTimer = setTimeout(() => {
      try {
        // Snapshot the .deck so we don't persist the toggle / hotzone state.
        const deck = document.querySelector('.deck');
        const wrapper = document.createElement('div');
        const clonedDeck = deck.cloneNode(true);
        wrapper.appendChild(clonedDeck);
        // Persist as a tiny HTML doc with just the deck so restore is symmetric.
        const html = `<!doctype html><html><body>${wrapper.innerHTML}</body></html>`;
        localStorage.setItem(STORAGE_KEY, html);
      } catch (err) {
        console.warn('Inline-edit autosave failed:', err);
      }
    }, SAVE_DEBOUNCE_MS);
  });

  // ---------- Download current HTML ----------
  function downloadHtml() {
    // Build a clean copy: strip contenteditable, remove the toggle/hotzone UI.
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
    clone.querySelectorAll('[spellcheck]').forEach(el => el.removeAttribute('spellcheck'));
    const hotzoneEl = clone.querySelector('.edit-hotzone');
    const toggleEl = clone.querySelector('.edit-toggle');
    if (hotzoneEl) hotzoneEl.remove();
    if (toggleEl) toggleEl.remove();
    clone.querySelector('body').classList.remove('edit-mode');

    const html = '<!DOCTYPE html>\n' + clone.outerHTML;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const title = (document.title || 'deck').replace(/[^a-z0-9-_]+/gi, '-').toLowerCase();
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title}.html`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
})();
```

### Notes on integration

- Place the inline-edit IIFE AFTER the nav-controller IIFE so the keyboard handler order is deterministic. The nav controller already early-returns on `contenteditable`, so the two don't conflict.
- The autosave key is `location.pathname`. If the deck is hosted at the same path under different content (rare), bump the key with a deck-version constant.
- For agent-generated decks where the editable surface is unusual (custom slide structures, embedded SVG text), extend `EDITABLE_SELECTORS` per template rather than expanding it globally.

## The layout bug (READ THIS, it has burned every build)

**Never use `justify-content: center` on a content slide.** Cover only.

Why: `.slide` is a fixed-height flex column (810px). If you set `justify-content: center` and the inner content is taller than 810 minus padding (which happens on almost every real slide with an h2 + lead + grid + chart + footnote), flexbox centers the overflow *symmetrically*, half above the top padding, half below. The top half bleeds under the absolute-positioned brand-mark at `top: 32px`.

Unlike the old responsive shell, there is no scroll bar to recover from this, `.slide` uses `overflow: hidden` now, because the canvas is fixed. Center-overflow will cut content off the top with no way to see it.

The fix is always `justify-content: flex-start` with enough padding-top to clear the brand-mark. Anchor content to the top; let it fill downward inside the 810px budget.

Signs you hit this bug:
- Eyebrow / heading text overlaps the brand-mark top-left
- Slide-meta top-right has text sliding under it
- Content appears "cut off at the top"
- No scroll reveals it (fixed canvas hides it permanently)

The fix is **never** adding more padding or shrinking content via media queries. It's always switching to `flex-start` AND fitting the content inside the 810px budget.

## Small-viewport behavior (no breakpoints needed)

With the fixed-canvas model, small viewports are handled automatically by `setScale()`. You do **not** write any `@media` rules that change layout.

Expected behavior:
- **Phone portrait (390×844)**: deck shows at ~27% scale, horizontally spanning the viewport, with dark letterbox bands top and bottom. Everything is readable (pinch to zoom in on specifics).
- **Tablet portrait (1024×768)**: deck shows at ~71% scale, horizontally spanning, bands top/bottom.
- **Desktop (1440×900)**: deck shows at 100% scale (since height 810 < viewport 900), bands top/bottom of ~45px each.
- **Ultrawide (2560×1080)**: deck shows at ~133% scale (capped by height 810, scaled to 1080, not by width), bands left/right.

No breakpoints. No grid collapse. The layout is identical at every size, just scaled.

## Brand-native variations

The shell structure stays identical, but brand-native details shift:

- **Airbnb**: rausch progress, circular arrows, clean sans
- **Stripe**: indigo gradient progress line, slightly heavier arrow strokes
- **Anthropic**: coral progress, arrow buttons sit in a warm cream surface
- **ElevenLabs**: bold dark product palette, monospace counter feels native
- **Sequoia**: black progress (not colored), serif counter in Fraunces, very editorial
- **Canva**: gradient progress line (purple to teal), playful 44px arrows
- **Databricks**: red progress, slightly chunkier arrow (2px stroke) for enterprise weight

Pick the `--letterbox` color per brand too:
- Light brands (Airbnb, Stripe, OpenAI), `#0A0A0A` or `#111` looks cinematic
- Dark-native brands (ElevenLabs), `#000`
- Editorial brands (Sequoia), `#1A1A1A`

The feel changes; the structure does not.

## What NOT to include in the shell

- A top menu bar
- A bottom bar with keyboard-shortcut hints
- A left thumbnail strip
- A dark-mode toggle (unless the brand is dark-native)
- Speaker notes panel
- Print button
- Share button with social icons
- **`@media` queries that reflow grids or change font sizes**, fixed-canvas means the layout is the layout; mobile zooms, it doesn't reflow

The file is the final artifact an investor would see, rendered with PDF-like integrity. Chrome breaks that illusion. Responsive reflow breaks the "design once, render everywhere" contract.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
