# Brand Methodology · Source-Verify, Don't Trust Cache

Color palettes, typography, and logos belong to the real brand, not to a cached table in this file. This reference gives you the *method* for establishing brand tokens for any deck; per-type packs (e.g., `deck-pitch/references/canonical-4-brands.md`) maintain their own cached catalogs of specific brands as starting points, but the cache is a lookup convenience, not ground truth.

The rule: **if a deck is Mode A (mirroring a real brand), the brand's own press kit is the source. Cached entries are starting points to be re-verified, not final answers.**

---

## When building for a brand · the research protocol

Whether the brand is in a type pack's cached catalog or not, always:

1. Fetch the company's official brand press kit / design system (or the homepage plus their current marketing site if no press kit exists).
2. Extract the **primary hex** plus 2 to 3 accent hexes. Note which is the "brand red/blue/green" vs. UI chrome vs. data viz.
3. Identify the **display font** and **body font**. If proprietary, pick the closest Google Font stand-in. Note both the real name and the stand-in.
4. Download the **logo as SVG** from the press kit. Inline the SVG in the HTML, never reference external URLs.
5. Verify the viewBox dimensions match the rendered glyph. Render it at the sizes you'll use (corner mark ~26px, cover hero ~120px+) to confirm legibility.
6. If the brand has a strong **dark-theme default** (Linear, Supabase, Vercel, Boom Supersonic), use it; otherwise use light.
7. Write the brand tokens block as CSS custom properties at the top of the file, matching the canonical structure any type pack uses.
8. Choose a visual-component set from the chosen type pack's `visual-components.md` (if one exists) that matches the brand's design voice. **Do not default to the type pack's canonical reference brand** (e.g., don't default to Airbnb patterns for a non-Airbnb pitch deck).

---

## Logo safety (applies to every brand, every deck type)

Two categories of logo appear in every deck:

### 1. The cover wordmark · large, hero placement on the Cover slide

- **Best source**: the company's own SVG download from their brand kit (legally and visually safest).
- **Inline** the full SVG in the HTML; don't reference external URLs.
- **Verify** the viewBox dimensions match the rendered glyph.

### 2. The corner brand-mark · small (~26px) top-left on every content slide

Options in order of safety:

a. The company's monogram / bug mark if they have one (Airbnb Bélo, Dropbox boxes, Stripe S-bug).
b. Their full wordmark at smaller size (works for short wordmarks: Uber, OpenAI).
c. A brand-colored square with the letter in their display font rendered via `<text>`:

```svg
<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="12" fill="#000"/>
  <text x="32" y="34" text-anchor="middle" dominant-baseline="central"
        font-family="Inter, sans-serif" font-size="42" font-weight="900"
        letter-spacing="-2" fill="#fff">U</text>
</svg>
```

### The cardinal rule

**Do NOT hand-craft a `<path>` to approximate a letter.** Letters with enclosed space (B, D, O, P, Q, R, U, A, 8) require multiple subpaths and correct `fill-rule` handling. One past build rendered a U as a `⊐` bracket. When in doubt, use `<text>`.

**Verify the glyph renders correctly** by imagining the viewBox and the stroke. If it looks like a bracket, a chunk, or a box, it's wrong.

### Nested-subpath rule

Any `<path>` with 2 or more `z` terminators (multiple subpaths, the Airbnb bélo, the Stripe wordmark with enclosed curves, any logo with inner cutouts) **must** declare `fill-rule="evenodd"`. Without it, nested shapes stack solid under the default nonzero rule and the logo renders as a blob. The Brand Reviewer catches this (`reviewers/brand.md`).

---

## When a cached catalog entry exists but is stale

Cached entries in type packs (e.g., `deck-pitch/references/canonical-4-brands.md`) are starting points. For Mode A decks:

- Re-fetch the brand's current page in Phase 1.
- If the current brand differs from the cache (new palette, refreshed logo, font swap), **the current brand wins**. Update the brief accordingly and flag the cache as stale for the next maintenance pass.
- Historical-anchor data in the cache (e.g., "UberCab 2010 seed: $1.25M raise, 20% take") does not go stale the same way; that's frozen era data. But double-check era claims against at least one external source before using them.

Past cache drift the protocol caught: ElevenLabs neon-green accents that were wrong (ElevenLabs is strictly monochrome). The cached entry listed `#C0F900` / `#00FF94`; re-verification found those colors were never actually in the ElevenLabs palette. Cache corrected, mechanical check added.

---

## Extension rule: brands not in any cache

When a user asks for a deck for a brand that no type pack has cached:

1. Run the full research protocol above.
2. Record the findings in the build brief (Section 4: Brand tokens).
3. Build the deck. If this is a type the user is likely to rebuild often (e.g., they keep asking for sales decks mirroring Salesforce), propose adding an entry to the type pack's cached catalog after the deck ships.

This keeps the caches small, curated, and trustworthy, rather than sprawling into a guess-table for every brand that ever appeared in a deck.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
