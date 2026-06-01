# Brand Authenticity Reviewer, Spec

**Owner**: Brand Reviewer (Phase 3).
**Categories owned**: brand authenticity drift + era accuracy / scope drift on historical decks.

Goal: catch the neon-that-isn't-in-the-brand bug, the iPhone-6-on-a-2009-deck bug, the "competitor didn't exist yet" bug. Everything a savvy investor would immediately recognize as wrong.

---

## Mode A (real-brand template) checks

### 1. Palette drift, declared vs shipped

Diff the brief's section 4 palette against the `.html`'s `:root` custom properties.

```bash
# Extract :root from the deck
grep -A 20 ':root {' "$DECK" | grep -E '^\s*--' | grep -oE '#[0-9a-fA-F]{3,8}'
# Compare to hexes in brief section 4
```

Fail if any CSS hex does not appear in the brief. Shade variants (e.g., `#E0484D` darker variant of Rausch `#FF5A5F`) are fine; net-new hues are not.

**Example case**: brief declared `#000000 / #FFFFFF / #6E6E6E / #F2F2F2`. If shipped deck has `#E6FF5E`, that's a fail.

### 2. Live brand-page verification

Before approving Phase 1, the Phase 1 author fetched the brand page. This check repeats it independently.

For each canonical brand the OSS pack ships templates for, the canonical source URL:

| Brand | Source URL |
|---|---|
| Airbnb | airbnb.com (no public brand kit, use press.airbnb.com) |
| Anthropic | anthropic.com (+ claude.com for Claude brand specifics) |
| Sequoia | sequoiacap.com (observe site typography + color) |
| Stripe | stripe.com/newsroom |

Fetch the brand page, extract primary color + display font, diff against what shipped.

If the agent's web-fetch tool is not available or the domain is blocked, check `brandfetch.com/<brand>` as a secondary source. Flag a WARN, not a FAIL, if live fetch fails.

### 3. Logo shape verification

The brand's actual mark, not what we remember. The canonical shape for each shipped template:

- Airbnb: Bélo (A-loop heart)
- Anthropic: 8-pointed A-star
- Sequoia: wordmark in Tiempos serif
- Stripe: "S" bug or Stripe wordmark

If shipped logo doesn't match, fail. Common wrong renderings:

- Anthropic star rendered as a generic sun or asterisk
- Stripe rendered as plain text without the brand's letterspacing
- Sequoia rendered in a sans serif

### 4. Era anachronism scan

For Mode A historical decks, read the content content-by-content and flag anything that post-dates the brief's declared era.

Patterns to grep (examples; extend per era):

```bash
era=$(grep -oE 'Era being depicted:\s*[0-9]{4}' "$BRIEF" | grep -oE '[0-9]{4}')

# iPhone generation claims
grep -nE 'iPhone\s*([0-9]+|X|SE|Pro|Plus|Max|mini)' "$DECK"
# Rule: if era < 2010, no iPhone past 3GS. Era < 2012, no iPhone 5+. Era < 2014, no iPhone 6+. Era < 2017, no iPhone X.

# Competitor names vs era
grep -inE '(Lyft|Sidecar|Waymo|Didi)' "$DECK"
# Rule: Lyft launched 2012, Sidecar 2012, Waymo 2016 (Google self-driving before). If era < these, fail.

# Raise-size anachronism
grep -nE '\$[0-9]+M\s*(seed|Series A|Series B)' "$DECK"
# Rule: pre-2012 seeds typically $500K to $2M; 2012 to 2017 $1 to 5M; post-2020 $2 to 15M. Out-of-band = flag.

# Cloud / platform anachronism
grep -inE '(AWS Lambda|serverless|containers|Kubernetes|edge compute)' "$DECK"
# Rule: Lambda 2014, Kubernetes 2014 public, common use 2016+. Pre-2014 claim = flag.
```

Extend per brand. Store per-brand anachronism lists in `brand-tokens.md` historical anchor sections.

### 5. VC-firm-era mismatch

If the Ask slide lists investors, check they existed + were active at that stage in that era.

- a16z: founded 2009, no pre-2009 investments.
- Sequoia: existed since 1972, fine for any era, but era-appropriate partners (Don Valentine, Mike Moritz, Roelof Botha).
- Benchmark: founded 1995.
- Accel: early-stage since 1983.
- USV: founded 2003.

Flag any investor-era mismatch.

---

## Mode B (fictitious or real-startup deck) checks

Mode B has no external brand to verify against. Instead:

### 1. Declared palette matches shipped

Same as Mode A check #1. Diff brief section 4 against CSS `:root`.

### 2. Declared logo approach matches shipped

Did the brief say "inline user-provided SVG"? Then verify the inlined SVG is present, not a hand-crafted substitute.
Did the brief say "`<text>`-in-`<rect>` fallback because no logo asset"? Then verify that's what's in the markup, not an invented mark.

### 3. No accidental real-brand borrowing

Cross-check the shipped Mode B deck against well-known canonical brand palettes. If the deck's primary color is within `#5` of Stripe Indigo or Uber Blue or Airbnb Rausch, flag as a warning, the user may not realize they accidentally landed on a canonical palette.

### 4. Founder credentials consistency

If the brief says "3 founders, each ex-[something]," verify every founder card in the Team slide has that framing. No missing credential. No invented extra credential.

### 5. Tone consistency

The brief sets tone (actual pitch vs illustrative-fictional). Verify `[REPLACE]` marker density matches the declared tone, an actual-pitch deck with 40 `[REPLACE]` markers is wrong; an illustrative deck with 0 is also wrong.

---

## Pass/fail report format

```
Brand Reviewer: PASS / FAIL

Mode: A, Uber (2010 UberCab seed era)

[PASS] Palette matches brief
[PASS] Live brand page fetched; current Uber palette matches brief (WARN: brand.uber.com primary is #000, Uber Blue #276EF1 is now data-accent only, brief captures this correctly)
[PASS] Logo shape: text-based "U" glyph, not bracket
[FAIL] Era anachronism: slide 7 mentions "iPhone app distribution" (fine), but slide 9 mentions "Kubernetes-style orchestration" (2014+ tech on a 2010 deck)
[PASS] VC era: Benchmark + First Round + SV Angel all active pre-2010

Action: remove slide 9 Kubernetes claim or change era in brief.
```

---

## Extending this reviewer

Every time a user flags a brand-authenticity issue that wasn't caught:

1. Log in `learnings-log.md` with date + build + brand category.
2. Add the specific check to this file.
3. If the check generalizes (e.g., "any deck mentioning a 2020+ tech on a pre-2020 era"), add a grep pattern to check #4.
4. If the check is brand-specific (e.g., "the Databricks red has shifted to `#FF3621` from the older `#E53935`"), update `brand-tokens.md` and reference it here.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
