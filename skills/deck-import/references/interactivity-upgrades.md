# Interactivity Upgrades, Turning Static Conversions Into Live Surfaces

SKILL.md Phase 3 rule #4 says: "Do NOT fabricate an interactive demo." That rule stands for the demo slide proper, a claimed product demo in the HTML must match the source, which usually means a static screenshot.

BUT: many conversion slides have obvious candidates for lightweight interactivity that don't fabricate product behavior, they simply upgrade a static rendering into a live one using the same content. These are "reveal-only" interactions that the source couldn't express.

This file lists the specific upgrade patterns, when each applies, and the code shape.

---

## Decision framework: when to add interactivity

Apply interactivity IF all of these hold:

- The element is visible-only in the source (form field, button, mode selector, tab).
- The rebuilt HTML preserves the same visual.
- Making it interactive doesn't claim product behavior that doesn't exist.
- The interaction is obvious from the source (the source designer clearly intended a toggle / form / button).

Do NOT add interactivity IF:

- The source implies a product workflow ("click here to sign in"), that would fabricate demo behavior.
- The element is a screenshot of a third-party tool (don't make their UI clickable).
- Adding interactivity requires fabricating content (e.g., a dropdown with made-up options).

---

## Pattern 1, Form fields become real `<input>`s

**When**: the source shows a form slide with labeled rows (Name, DOB, SSN, etc.) where the values appear filled in.

**Source rendering**: labels on left, values on right in a lightly-bordered pill.

**Static HTML (before)**:
```html
<div class="demo-row">
  <div class="demo-label">Name</div>
  <div class="demo-val">Ricardo Pacheco</div>
</div>
```

**Interactive HTML (after)**:
```html
<div class="demo-row">
  <div class="demo-label">Name</div>
  <input class="demo-val" value="Ricardo Pacheco" />
</div>
```

**CSS adjustments**:
```css
input.demo-val {
  font: inherit;
  color: inherit;
  border: 0;
  outline: 0;
  background: transparent;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 180ms;
}
input.demo-val:focus {
  background: rgba(249,115,22,0.06);
  box-shadow: inset 0 0 0 1px rgba(249,115,22,0.35);
}
input.demo-val.has-val { /* styling when filled */ }
```

**JS (inside the IIFE)**:
```js
document.querySelectorAll('input.demo-val').forEach(function(el){
  el.addEventListener('input', function(){
    el.classList.toggle('has-val', el.value.length > 0);
  });
});
```

Why this works: the user can tab through the form, backspace a value, retype. They're not submitting anywhere, the form is illustrative, but it FEELS real, which is the whole conversion upgrade thesis.

---

## Pattern 2, Mode selectors become toggleable `<button>`s

**When**: the source has pill-style tabs ("Classic", "Chat", "Phone", "Sign") where one is visually highlighted.

**Static HTML (before)**:
```html
<div class="s08-card">
  <span class="s08-mode">Classic</span>
  <span class="s08-mode s08-mode-active">Chat</span>
  <span class="s08-mode">Phone</span>
  <span class="s08-mode">Sign</span>
</div>
```

**Interactive HTML (after)**:
```html
<div data-s08>
  <div class="s08-card" data-s08-card="chat">
    <button data-mode="classic" class="s08-mode">Classic</button>
    <button data-mode="chat" class="s08-mode s08-mode-active">Chat</button>
    <button data-mode="phone" class="s08-mode">Phone</button>
    <button data-mode="sign" class="s08-mode">Sign</button>
  </div>
</div>
```

**CSS**:
```css
.s08-mode {
  border: 0;
  background: transparent;
  cursor: pointer;
  transition: background 180ms, transform 120ms;
  /* ... existing visual styles ... */
}
.s08-mode:hover {
  background: #E5E7EB;
  transform: translateY(-1px);
}
.s08-mode-active {
  background: var(--ink);
  color: #fff;
}
```

**JS**:
```js
document.querySelectorAll('[data-s08] [data-s08-card]').forEach(function(card){
  card.querySelectorAll('[data-mode]').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      card.querySelectorAll('[data-mode]').forEach(function(b){ b.classList.remove('s08-mode-active'); });
      btn.classList.add('s08-mode-active');
    });
  });
});
```

Why the per-card scope: multiple cards on the same slide (e.g., "Chat Form Mode" next to "Phone Call Mode") need independent active states. Scope every handler to its card container.

---

## Pattern 3, Card hover elevation

**When**: pricing, feature, or use-case cards arranged in a grid.

**CSS-only upgrade**, no JS needed:
```css
.s12-card {
  transition:
    transform 260ms cubic-bezier(.2,.7,.2,1),
    box-shadow 260ms ease,
    border-color 260ms ease;
  cursor: pointer;
}
.s12-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 48px rgba(249,115,22,0.18);
  border-color: rgba(249,115,22,0.55);
}
```

Apply to pricing tier cards (Slide 12-style), feature cards, use-case cards. Don't apply to cards that are purely informational with no obvious CTA.

---

## Pattern 4, Row-hover on matrix / comparison tables

**When**: competition matrix, feature comparison table, spec sheet.

Subtle row-hover helps a reader follow across a wide matrix:

```css
.comp-matrix tbody tr:hover {
  background: rgba(249,115,22,0.04);
}
.comp-matrix tbody tr:hover td:first-child {
  font-weight: 600;
}
```

---

## Pattern 5, Placeholder input for "ask me anything" areas

**When**: source has a "Need a hand?" or "Ask me" text area as a static illustration.

Convert the rendered text into a real `<input placeholder>`:

```html
<input class="demo-ask-input" placeholder="Need a hand? Ask me any questions about this form" />
```

```css
.demo-ask-input {
  width: 100%;
  padding: 12px 16px;
  font: inherit;
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 12px;
  background: #fff;
  outline: 0;
}
.demo-ask-input:focus {
  border-color: rgba(249,115,22,0.6);
  box-shadow: 0 0 0 4px rgba(249,115,22,0.12);
}
```

The input goes nowhere, it's illustrative, but feels responsive.

---

## What this is NOT

- **Not a live demo**. The demo slide (as defined in the brief) stays static unless the user requests a full interactive demo upgrade. The OSS pack does not bundle a working interactive demo builder.
- **Not fabricated functionality**. We don't write fake API calls, fake dropdowns with made-up options, or fake authentication flows.
- **Not mandatory**. If the source is text-heavy and has no form/toggle/card elements, skip this file entirely.

---

## When to mention interactivity in the Release message

If you added interactivity via any of these patterns, note it in the Release message:

> "I upgraded a few static elements to live interactivity, the applicant form on slide 20 accepts typing; the mode toggles on slide 8 switch; cards on slide 12 have a hover elevation. These are illustrative, not a live demo, just the conversion polish that a source file can't express."

That framing (a) credits the upgrade and (b) manages expectations (it's polish, not product).

