# Style Presets

Six named aesthetic presets for Mode B users who don't have a brand of their own yet. Each preset is a self-contained set of CSS custom-property defaults (brand tokens) plus a typography family plus a one-line character description.

When to use:
- The user is in Mode B (their own deck, not a brand mirror).
- The user has no brand identity yet, no logo, no palette declared.
- Phase 1 reaches the palette-approach question and the user says "I don't have one, pick something."
- Phase 2 auto-preview generates 3 first-slide previews. Pick the 3 most contextually fitting presets from this file (one safe, one bold, one wildcard) and render the preview slide in each.

Presets are deliberately distinct from each other and from the styles in popular OSS alternatives. They are calibrated for startup pitch decks, B2B sales decks, product launches, keynotes, and all-hands. They are NOT a substitute for a real brand. If the user has any brand assets at all, use those.

Every preset assumes light theme by default. Dark variants are noted where they make sense (rarely).

---

## Preset 1 · Founder Default

The safe pick. Clean, modern, monochrome with a single accent. Reads serious without being severe.

```css
:root {
  --brand-primary: #111111;
  --brand-accent:  #FF5722;
  --brand-text:    #1A1A1A;
  --brand-muted:   #6B6B6B;
  --brand-bg:      #FFFFFF;
  --brand-surface: #FAFAFA;
  --brand-border:  #E5E5E5;
  --font-display:  'Inter', system-ui, sans-serif;
  --font-body:     'Inter', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', 'SF Mono', monospace;
}
```

Character: confident, restrained, contemporary. Inspired by the "modern minimalist startup" aesthetic. Works for almost everything. Default fallback if no preset is requested.

When to recommend: first-time founders, B2B SaaS pitching to enterprise buyers, anything where the user says "I want it to look professional."

**Typographic scale** (validated against a real 14-slide pitch build):

```
11, 12, 14, 16, 18, 22, 28, 36, 48, 64, 96, 128 px
```

Role mapping:
- 11 px · footnotes, slide-meta counters
- 12 px · monospace labels, fine print
- 14 px · card body text
- 16 px · body paragraphs
- 18 px · lead paragraphs, eyebrow text
- 22 px · section heads, sub-h3
- 28 px · slide h2
- 36 px · large h2, secondary hero
- 48 px · primary hero stat
- 64 px · focal numbers (bottom-up calc, ARR)
- 96 px · brand-mark square on cover
- 128 px · cover wordmark

---

## Preset 2 · Quiet Confident

Sage green plus warm slate. Mature, established, lived-in. Reads like a company that has been around a while.

```css
:root {
  --brand-primary: #4A5D4F;
  --brand-accent:  #8B6F47;
  --brand-text:    #2D3A2F;
  --brand-muted:   #6E7B70;
  --brand-bg:      #FAF8F3;
  --brand-surface: #F2EFE7;
  --brand-border:  #D9D4C5;
  --font-display:  'Source Serif Pro', 'Georgia', serif;
  --font-body:     'Inter', system-ui, sans-serif;
}
```

Character: warm, sustainable, considered. Slightly editorial. Inspired by the modern wellness, food, sustainability, and quiet-luxury brand families.

When to recommend: consumer brands, wellness, sustainability, hospitality, anything where "calm" is a positive signal.

**Typographic scale** (tighter than Founder Default, leans editorial-quiet, no extreme top end):

```
11, 13, 14, 16, 18, 22, 28, 34, 42, 56, 80, 104 px
```

Role mapping:
- 11 px · footnotes, slide-meta counters
- 13 px · card body text (slightly larger for the serif body face)
- 14 px · body annotations
- 16 px · body paragraphs
- 18 px · lead paragraphs
- 22 px · eyebrow text, section heads
- 28 px · slide h2 (smaller than Founder Default; serif reads larger at same px)
- 34 px · secondary hero
- 42 px · primary hero stat
- 56 px · focal numbers
- 80 px · brand-mark square on cover
- 104 px · cover wordmark (smaller top end; preset is intentionally restrained)

---

## Preset 3 · Studio Bold

High-contrast cobalt blue on warm cream. Display headlines. Premium consumer energy.

```css
:root {
  --brand-primary: #0B3D91;
  --brand-accent:  #F2B705;
  --brand-text:    #0B0B0B;
  --brand-muted:   #4A4A4A;
  --brand-bg:      #FBF7EE;
  --brand-surface: #FFFFFF;
  --brand-border:  #D9CDB4;
  --font-display:  'Playfair Display', 'Didot', 'Georgia', serif;
  --font-body:     'Inter', system-ui, sans-serif;
}
```

Character: premium, editorial, magazine-cover energy. Big type, generous whitespace, deliberate.

When to recommend: consumer pitches that want to feel premium, lifestyle brands, anything aimed at a sophisticated buyer.

**Typographic scale** (larger top end than Founder Default; this preset wants the headline to dominate):

```
11, 12, 14, 16, 20, 26, 34, 44, 60, 84, 112, 160 px
```

Role mapping:
- 11 px · footnotes
- 12 px · monospace labels
- 14 px · card body text
- 16 px · body paragraphs
- 20 px · lead paragraphs (slightly larger; preset prefers airy text)
- 26 px · eyebrow / sub-h3
- 34 px · slide h2 (display-face serif reads big)
- 44 px · large h2, hero stat
- 60 px · focal numbers
- 84 px · secondary cover element
- 112 px · brand-mark square on cover
- 160 px · cover wordmark (oversized; this is the preset's signature move)

---

## Preset 4 · Editorial Serif

Charcoal plus deep red accent. Tall serif hierarchy. For thoughtful, research-led decks.

```css
:root {
  --brand-primary: #1F1F1F;
  --brand-accent:  #A0344B;
  --brand-text:    #1F1F1F;
  --brand-muted:   #5C5C5C;
  --brand-bg:      #FFFCF7;
  --brand-surface: #F5F1E8;
  --brand-border:  #D8D1C3;
  --font-display:  'Lora', 'Source Serif Pro', 'Georgia', serif;
  --font-body:     'Source Serif Pro', 'Georgia', serif;
}
```

Character: serious, considered, opinion-led. New Yorker meets a quiet research firm.

When to recommend: keynotes, conference talks, deep-dive content, anything where the user has a strong point of view they want to defend at length.

**Typographic scale** (more dramatic ratios; the jumps between sizes are intentionally larger to emphasize hierarchy):

```
11, 13, 15, 17, 21, 28, 38, 52, 72, 100, 136, 184 px
```

Role mapping:
- 11 px · footnotes
- 13 px · card body text
- 15 px · body annotations
- 17 px · body paragraphs
- 21 px · lead paragraphs
- 28 px · eyebrow / sub-h3
- 38 px · slide h2
- 52 px · large h2
- 72 px · primary hero stat
- 100 px · secondary cover element
- 136 px · brand-mark square on cover
- 184 px · cover wordmark (most dramatic top end of any preset; serif demands it)

---

## Preset 5 · Tech Crisp

White plus cyan plus jet black. Geometric sans. Optimistic infrastructure energy.

```css
:root {
  --brand-primary: #0F0F0F;
  --brand-accent:  #00B3FF;
  --brand-text:    #0F0F0F;
  --brand-muted:   #5C5C5C;
  --brand-bg:      #FFFFFF;
  --brand-surface: #F6F8FB;
  --brand-border:  #E1E6EE;
  --font-display:  'Space Grotesk', 'Inter', system-ui, sans-serif;
  --font-body:     'Inter', system-ui, sans-serif;
  --font-mono:     'JetBrains Mono', 'SF Mono', monospace;
}
```

Character: developer-friendly, modern infrastructure, "we ship fast." Confident without being loud.

When to recommend: dev tools, API companies, AI infrastructure, data tools, anything technical.

**Typographic scale** (close to Founder Default, slightly geometric; works well with Space Grotesk display):

```
11, 12, 14, 16, 18, 22, 28, 36, 48, 64, 96, 128 px
```

Role mapping:
- 11 px · footnotes, slide-meta counters
- 12 px · monospace labels (mono face common in tech decks)
- 14 px · card body text
- 16 px · body paragraphs
- 18 px · lead paragraphs, eyebrow text
- 22 px · section heads
- 28 px · slide h2
- 36 px · large h2
- 48 px · primary hero stat
- 64 px · focal numbers (ARR, request counts, latency)
- 96 px · brand-mark square on cover
- 128 px · cover wordmark

---

## Preset 6 · Warm Brand

Peach plus terracotta plus cream. Rounded sans. Friendly, approachable, consumer-facing.

```css
:root {
  --brand-primary: #C84E2C;
  --brand-accent:  #F5C26B;
  --brand-text:    #2A1F1A;
  --brand-muted:   #6E5A50;
  --brand-bg:      #FFF6EC;
  --brand-surface: #FFEDD9;
  --brand-border:  #F0D7B4;
  --font-display:  'Manrope', 'Inter', system-ui, sans-serif;
  --font-body:     'Manrope', 'Inter', system-ui, sans-serif;
}
```

Character: warm, friendly, human. Soft corners. Reads like a brand that cares about the customer.

When to recommend: consumer apps, hospitality, food and beverage, wellness, education, anything where warmth is the differentiator.

**Typographic scale** (rounded sans wants slightly softer ratios; no extreme top end):

```
11, 13, 14, 16, 18, 22, 28, 36, 46, 60, 88, 112 px
```

Role mapping:
- 11 px · footnotes
- 13 px · card body text
- 14 px · body annotations
- 16 px · body paragraphs
- 18 px · lead paragraphs, eyebrow text
- 22 px · section heads
- 28 px · slide h2
- 36 px · large h2
- 46 px · primary hero stat
- 60 px · focal numbers
- 88 px · brand-mark square on cover
- 112 px · cover wordmark (intentionally restrained; warmth reads better at moderate sizes)

---

## How auto-preview Phase 2 uses these

When the user has no brand and reaches the preview step, the skill picks 3 presets:

1. **Safe**, contextually fitting. Default: Preset 1 (Founder Default).
2. **Bold**, contrasts the safe pick. Default: Preset 3 (Studio Bold) or Preset 5 (Tech Crisp), whichever fits the sector better.
3. **Wildcard**, something the user wouldn't have picked themselves but might love. Default: Preset 4 (Editorial Serif) or Preset 6 (Warm Brand).

The skill generates one first-slide preview HTML per preset, saves them to `.skill-temp/`, opens all 3 in the browser, then asks the user to pick.

---

## What's NOT in here (and why)

- **Dark mode default presets.** Generated decks default to light theme. A dark variant is only generated if the user explicitly asks for one.
- **Neon, terminal, cyberpunk aesthetics.** These are well-served by other OSS skill packs. We focus on presets that work for serious business decks.
- **Brand-mirror presets.** Brand mirrors (Airbnb, Stripe, Anthropic, Sequoia Classic) live in `templates/`, not here. Style presets are for users who don't want to mirror a real brand.

---

## Adding a new preset

PRs welcome. Requirements:

- All 8 brand tokens declared (primary, accent, text, muted, bg, surface, border, plus one display font and one body font).
- Color tokens accessible at WCAG AA on the bg surface (use Stark or Contrast Ratio Checker to verify).
- Distinct from existing presets at a 2-second glance (no near-duplicates).
- Named in 2 to 3 words. Skip product-name-style branding.
- One-line character description that helps the agent pick when to recommend it.

See `references/build-a-type-pack.md` for the broader contribution pattern.
