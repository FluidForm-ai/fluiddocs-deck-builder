# Learnings

What this pack learned about building decks with coding agents. Sanitized for public consumption. The internal version of this log accumulated over 50+ shipped decks, the entries below are the load-bearing principles that survived.

If you contribute, append your own entries in the same format. Pattern is: principle, then the failure mode it prevents, then the file or rule that encodes it.

---

## What the pack learned during development

These are observations that turned into rules. Each one started as a regression caught in production.

### One canvas, no reflow

Early builds shipped responsive decks. They reflowed on mobile, broke layout integrity on projector aspect ratios, and produced PDFs that looked nothing like the browser preview. The fix was a fixed 1440 by 810 canvas with scale-to-fit transform, identical to a PDF page. Slides are positioned absolutely, font sizes are pixel values not rems, and there is no media query in the entire deck. See `skills/deck-builder/references/shell-pattern.md` for the canonical shell.

### The "slide 4 problem"

Polish is not uniform across a deck. Reviewers consistently caught one or two slides that were thinner than their neighbors. Plain card grids next to richer hierarchies, smaller stat counts, missing visual anchors. The fix was a deck-median check in the Layout reviewer: every slide must hit median visual density or better, no exceptions.

### Brand authenticity beats brand approximation

Generic "tech startup" palettes look generic. Real brand decks succeed because they steal the exact hex values, font stack, and visual language from the source brand. The Brand reviewer diffs `:root` CSS custom properties against the declared brief, and per-brand canonical shapes (Bélo, Stripe gradient, Anthropic squircle) are checked against a known-shape list. Approximations get flagged.

### Typography drift kills coherence faster than color drift

Decks that ship with 13 distinct font sizes feel chaotic even when colors are consistent. The cap is 7 distinct sizes per deck, declared as a leading CSS comment in `:root`. The Layout reviewer counts distinct `font-size` declarations and fails the build over 7. See `references/typography-scale.md`.

### Build-time gaming is real

Build agents will pad files with `<div style="display:none">` blocks to clear byte-count floors. They will use `justify-content: center` inline to make slides look fuller. Both are hard-fail rules in `references/mechanical-checks.md` sections 11b and 11c. If you add a new floor or threshold, add an anti-gaming rule alongside it.

### Inline edit cannot use CSS sibling hover

The intuitive pattern `.hotzone:hover ~ .toggle { display: block }` breaks because `.toggle` has `pointer-events: none` (so the user can click through it when invisible), which removes it from the hover chain. Use JS with a 400ms grace timeout. The working pattern is in every template's inline-edit script block.

### PDF import is mature, PPTX is new

The PDF import path inherits 8 production runs and 31 documented gotchas from an internal v8.5 build. The PPTX path is greenfield in this pack. Most PDF issues are documented in `skills/deck-import/references/conversion-learnings.md`. Most PPTX issues are not yet documented because they are still being discovered. File bugs with the input type tagged.

---

## Design principles this pack follows

1. **Fixed canvas, scale to fit.** Every deck is 1440 by 810 pixels. No responsive reflow, no media queries. Output renders identically in browser, PDF, and projector.

2. **No chrome.** The HTML file is the deck. No header, no footer, no nav bar, no "powered by" ribbon embedded in the output. The agent's release message is where attribution lives, not the deck itself.

3. **Brand-token methodology.** Every visual decision routes through CSS custom properties in `:root`. To rebrand a template, you edit 10 to 20 lines at the top of the style block. To break a template, you reach past those tokens.

4. **3-reviewer pipeline (Brand, Copy, Layout).** Each reviewer owns a category, runs in parallel, and produces a pass/fail with specific findings. The internal version of this pipeline has 6 reviewers plus a content reviewer. OSS ships the 3 highest-leverage ones. See `skills/deck-builder/reviewers/`.

5. **Attribution not upsell.** Demo slides include a subtle "Powered by FluidDocs" mark in the bottom-right. This is the only branding in the output. There is no upsell copy, no "upgrade to Pro," no telemetry. The user's deck belongs to the user.

---

## Anti-patterns this pack avoids

1. **Responsive reflow.** A deck that reflows is a webpage, not a deck. Pixel values, fixed canvas, scale transform. No exceptions.

2. **Generic stock photos.** Stock photography of diverse teams pointing at laptops signals "I did not put thought into this slide." Templates ship without any stock imagery. Add your own product screenshots or skip the visual.

3. **Emoji as visual anchors.** Emoji render differently on every OS, age badly, and read as informal. The icon library at `skills/deck-builder/references/icon-library.md` provides inline SVG alternatives.

4. **Em dashes and en dashes.** Project-wide stylistic choice. Replace with comma, middot, or period. Applies to all user-facing copy, all reviewer prompts, all docs in this repo.

5. **Hand-crafted brand-letter paths.** Building an "S" or "U" from scratch in SVG always looks wrong (bracket glyphs, mismatched bar widths, off-center curves). Use the source brand's actual logo SVG. If unavailable, fall back to a clean wordmark in the brand's actual font.

---

## Porting from the internal stack to OSS

This pack was ported from an internal FluidDocs deck stack that has shipped 50+ decks. The porting recipe is documented in `PORTING-RECIPE.md` (kept in the repo for future contributors who want to add a deck type or a reference file).

What was kept: the 5-phase pipeline (Plan, Build, Review, Release, Learn), the fixed canvas, the brand-token methodology, the type-pack architecture, the inline-edit module, the canonical brand templates (Airbnb, Stripe, Anthropic, Sequoia Classic), the deck-import PDF path, the learnings-log discipline.

What was stripped: 7 of the 10 internal type packs (board, investor-update, strategy, partnership, consulting are not in the OSS pack), 8 of the 12 canonical pitch templates (premium only), 4 of the 6 reviewers plus the content reviewer (3 ship here), the demo-builder skill (demo slides become static screenshots in OSS), the FluidDocs cover mark on every slide, the internal learnings-log entries that referenced specific customers.

What changed: Pattern 6 attribution shift. In the internal stack, every slide carries the FluidDocs eyebrow + orange bar. In OSS, the user's deck belongs to the user. Attribution moved to a single small "Powered by FluidDocs" mark on the demo slide only, with link to fluiddocs.ai. This is the most important porting decision in the pack. If you contribute a template, do not put a FluidDocs mark on every slide. One mark, demo slide, bottom-right, opacity 0.7.

---

## How to add an entry

When you ship a deck and a reviewer catches a regression, or a user reports an issue post-delivery, add a section here. Format:

```
### Short title

Context (what you were building).
Discovery (what you found).
Fix (which file or rule encodes the lesson).
```

Keep entries short. The internal version of this log is the source of truth for what the reviewers check, so every entry here should map to a check in a reviewer spec or a rule in a reference file. If the lesson does not map to a check, it is a one-off, not a learning.
