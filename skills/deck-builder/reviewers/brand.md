# Brand Reviewer

Owns: brand drift plus visual character coherence.

Runs after Phase 2 build, before Phase 4 release. Bounces the deck back to Phase 2 if any check fails.

## What this reviewer reads

1. The build brief (Phase 1 output).
2. The final CSS `:root` block of the generated deck.
3. Every slide's content.
4. Mode A only: the brand's actual website (re-fetched fresh, not from the brief's cached palette).

## Checks (Mode A: real-brand mirror)

- **Declared palette matches final CSS tokens.** Brief said `--brand-primary: #FF5A5F`? Final CSS has the same value? If they diverged, flag.
- **Re-fetched brand still matches.** Visit the brand's homepage. Pull dominant colors. Compare to what shipped. If the brand has refreshed since the brief was written, the deck should reflect the current brand (or the user should be asked which version they want).
- **Era anachronisms.** Brief declared era 2008-2010 (e.g., early Airbnb)? Check content for anachronisms: no mention of post-era competitors, no post-era business-model terms, no post-era market sizing.
- **Logo shape matches reality.** The brand's logo on their current site matches the logo shape in the deck cover.
- **Forbidden class names absent.** Brief's forbidden-classname list (e.g., `comp-matrix`, `listing-grid` for a non-Airbnb pitch) does not appear in the deck CSS.

## Checks (Mode B: user's own brand or style preset)

- **Declared palette matches final CSS tokens.** Same check as Mode A.
- **Style preset coherence.** If the user picked a named preset (e.g., "Founder Default"), verify the final tokens still match the preset's declared values. The build phase should not have drifted.
- **Typography family is present in the declared scale.** No font families introduced beyond what the brief declared.
- **Logo handling.** If the user supplied a logo, it's used. If they didn't, the cover uses the `<text>`-in-`<rect>` brand mark pattern from `references/brand-methodology.md`, never a hand-crafted `<path>` approximation.

## Checks (universal, both modes)

- **Zero pack branding in generated output, with exactly one allowed exception.** No FluidDocs cover marks, no watermarks, no footer logos, no meta tags identifying the pack. The ONLY permitted FluidDocs reference is a single small "Powered by FluidDocs" attribution mark on the demo slide (pitch slide 6, launch slide 5), and it must sit in the **bottom-right corner** (`text-align: right` or right/bottom absolute positioning), muted, ~20px tall. It must NOT be centered, must NOT appear on the cover or any non-demo slide, and must NOT be duplicated. Grep the final HTML for `fluiddocs` (case-insensitive): for deck types with a demo slot, expect exactly the one demo-slide mark and verify it is bottom-right; for types with no demo slot (sales, keynote, all-hands), expect zero hits. A centered mark, a mark on the wrong slide, more than one mark, or any other FluidDocs branding is a FAIL.
- **No third-party brand leaks.** A pitch deck for Company X should not accidentally contain Stripe's purple gradient or Airbnb's "Belo" shape unless the brief explicitly declared them.

## Pass criteria

Every check returns clean. If any check fails, report the specific failure (the actual color, the actual class name, the actual file location) and bounce to Phase 2.

## Failure modes seen historically

- Final CSS uses brand-correct colors but the canvas background drifts to off-white when the brief said pure white.
- Mode A deck uses a logo shape from the brand's previous identity refresh, not the current one.
- Mode B "Founder Default" preset got drifted by an enthusiastic Phase 2 pass adding accent colors not in the preset.
- Hand-crafted `<path>` brand letter introduced when the real logo CDN failed.

When you see one of these, add a new line to `references/learnings-log.md` so the next reviewer pass catches it earlier.

## Output format

```
Brand Reviewer: PASS
(or)
Brand Reviewer: FAIL · 2 items
  1. CSS token `--brand-primary` is #FF5722 but brief declared #FF5A5F. Slide 1, line 47 of CSS.
  2. Forbidden class `listing-grid` appears on Slide 5. Brief forbids this (Airbnb-leak). Use the type pack's recommended grid pattern instead.
```

Reviewers do not write apologies or summaries. They report findings and stop.
