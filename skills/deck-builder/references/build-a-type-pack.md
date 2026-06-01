# Build-a-Type-Pack, canonical recipe

**This file is the ground truth for building a new type pack.** Every new deck type follows this recipe. The OSS pack ships five type packs (pitch, sales, launch, keynote, all-hands); the same method applies if you want to fork a new type for an internal use case.

If you are a sub-agent building a type pack, read this file top to bottom before writing any code. The recipe is deterministic, if you follow it, the output passes.

---

## Pre-flight

Confirm the `deck-builder` core skill is installed. Confirm the source exists and `references/build-brief-template.md` is readable. If not, stop, the core must exist first.

---

## Step 1: Look up the type's parameters

Find the row for your `deck_type` in the **Type Parameter Table** below. Every row defines the four parameters that drive the build:

1. `deck_type` , string, lowercase, kebab-case (e.g. `sales`)
2. `Target slide count` , integer (default the brief locks in)
3. `Catalog directory` , where shipped decks land
4. `Interactive demo required` , yes / no / optional (in the OSS pack, demos are static screenshots, see Step 6)

### Type Parameter Table (OSS pack)

| deck_type | Slide count | Catalog directory | Demo |
|---|---|---|---|
| pitch | 14 | <user-chosen> | yes (static screenshot on slide 6) |
| sales | 11 | <user-chosen> | optional |
| launch | 12 | <user-chosen> | yes (static screenshot on slide 5) |
| keynote | 28 | <user-chosen> | optional |
| all-hands | 15 | <user-chosen> | no |

If your `deck_type` is not in this table, you are adding a new type pack to the OSS pack. Either propose it upstream, or fork and add it as a private type pack alongside.

---

## Step 2: Create the source tree

Create the directory `<your-workspace>/deck-<deck_type>-v1/` (e.g. `<workspace>/deck-sales-v1/`). Create a `references/` subdirectory inside it.

---

## Step 3: Write SKILL.md

File: `<workspace>/deck-<deck_type>-v1/SKILL.md`

Template below. Fill in `<DECK_TYPE>`, `<DECK_TYPE_TITLE>`, `<ROLE_DESCRIPTION>`, `<TRIGGER_PHRASES>`, `<TYPE_SPECIFIC_DECLARATION>`, `<SLIDE_COUNT>`, `<CATALOG_DIR>`, `<FORBIDDEN_LEAKS>`, and `<DEMO_RULE>`.

**The description must be under 1024 characters.** Count before shipping. Aim for the pitch pack's range (~900 to 1000 chars).

```markdown
---
name: deck-<deck_type>
description: <Short 900 to 1000 char description, what this pack builds, trigger phrases, one-line dependency note on deck-builder core, one-line statement of what's type-specific>
---

# Deck <DECK_TYPE_TITLE>, a type pack for the `deck-builder` core

This skill builds **<ROLE_DESCRIPTION>**. It is a thin type pack that inherits the full pipeline from the `deck-builder` core skill. Read `deck-builder/SKILL.md` first for the 5-phase pipeline, 3-reviewer gate, fixed-canvas shell, brand-tokens methodology, and learnings log. This file only declares what's **<deck_type>-specific**.

---

## What's type-specific (defined in this pack)

**References in `references/`**:
- `content-spine.md` , the canonical <SLIDE_COUNT>-slide <deck_type> spine
- `visual-components.md` , per-slide brand-native patterns
- <Additional type-specific references as needed>

**Declarations the brief locks in for <deck_type> builds**:
- `deck_type: <deck_type>`
- `Target slide count`: <SLIDE_COUNT>
- `Catalog directory ($CATALOG)`: <CATALOG_DIR>
- `Forbidden class-name leaks`: <FORBIDDEN_LEAKS>
- Demo: <DEMO_RULE>

---

## What this type pack inherits from `deck-builder` core

**Pipeline**: `deck-builder/SKILL.md`, 5-phase Plan, Build, Review, Release, Learn; 3 reviewer gates (Brand, Copy, Layout).

**Phase 1 artifact**: `deck-builder/references/build-brief-template.md`, fill in `deck_type: <deck_type>` plus the other <deck_type>-specific fields listed above.

**Phase 2 implementation**:
- `deck-builder/references/shell-pattern.md`, chrome-free nav shell + 1440x810 canvas scale, inline-edit module
- `deck-builder/references/icon-library.md`, inline SVG icon set replacing every emoji
- `deck-builder/references/brand-methodology.md`, source-verify brand tokens protocol + logo safety

**Phase 3 reviewer specs** (all in `deck-builder/reviewers/`):
- `brand.md`, `copy.md`, `layout.md`

Deeper-dive references the reviewers may consult: `deck-builder/references/brand-authenticity.md`, `rendering-checks.md`, `mechanical-checks.md`, `typography-scale.md`, `polish-rubric.md`, `visual-variety.md`.

**Phase 5 learnings**: `deck-builder/references/learnings-log.md` (shared; filter by `Deck type = <deck_type>`).

---

## Output expectations (<deck_type>-specific)

Phase 4 deliverable:

1. The `.html` file at `<CATALOG_DIR>/<Brand or Client>-Deck.html` (Mode A) or a user-specified path (Mode B).
2. The brief alongside it: `<Brand or Client>-Brief.md`.
3. The absolute path to the file (or a tool-specific link such as `computer://...` when the agent runs in an environment that resolves it).
4. A one-paragraph design/content summary.
5. The compact audit report (3 reviewers, one line each).

Do not write walls of explanation. The file is the deliverable.

---

## Hard rules specific to <deck_type> decks

<TYPE_SPECIFIC_DECLARATION, 3 to 6 bullet rules that matter for this deck type. See examples below.>

All other rules come from `deck-builder/SKILL.md` Universal Design Rules.
```

---

## Step 4: Write content-spine.md

File: `<workspace>/deck-<deck_type>-v1/references/content-spine.md`

The content spine is the canonical slide-by-slide structure for this type. Use the **Content Spines** reference at the bottom of this recipe to find the spine for your `deck_type`. Each slide entry should include:

- Slide number and name
- Purpose (one sentence)
- Required elements (3 to 5 bullets)
- What NOT to do (failure modes)
- Optional: stage or context adjustments

Aim for the spine to fit within the slide-count target (+/-1). Slide 1 is always Cover; the final slide is a natural closer (Ask, CTA, Contact, Next Steps, Q&A, type-appropriate).

The spine must end with:

- "## Hard constraints" listing the minimum/maximum slide count, the max-reading-time rule (45 sec/slide), no-emoji rule, the three universal anti-gaming rules below, and any type-specific hard rules.

### Universal anti-gaming rules (must appear in every pack's Hard Constraints)

These three rules are absolute across every deck type. The Layout Reviewer (mechanical-checks sections 11b, 11c) enforces them as automatic hard fails. Spines written without them get caught at the brief-approval gate.

1. **No hidden-content filler.** Zero `display: none`, `visibility: hidden`, `opacity: 0`, or `height: 0` declarations outside the two base `.slide` rules (`{ display: none }` toggle or `{ opacity: 0 }` transition). If the deck is short of the 60K file-size floor, add **real visible content** across slides, do NOT add hidden blocks to pad bytes. This is an automatic HARD FAIL.

2. **No inline `justify-content: center` on `<section class="slide">`.** Centering an 810px flex column causes content-taller-than-canvas to overflow symmetrically above the top padding, hiding behind the absolute-positioned brand-mark. If a slide needs centered content (cover, thanks, closing), use a dedicated CSS class (`.s-cover`, `.s-closing`), never inline.

3. **Typography scale declared in CSS.** The first line of the deck's CSS `<style>` block MUST include a comment declaring the scale, e.g. `/* Typography scale (7 sizes): 10px, 14px, 18px, 24px, 32px, 48px, 56px */`. The Layout Reviewer enforces that every `font-size` value in the file matches one of the declared sizes, and that the count is <=7.

### Recommended pattern: opacity-based slide hiding

When writing your type pack's shell, prefer the opacity-based hiding pattern (all slides rendered in DOM, `.slide { opacity: 0 }` base + `.slide.active { opacity: 1 }` toggle) over the display-none pattern. Rationale: with opacity-based hiding, the file should contain **zero** `display: none` declarations, which turns the anti-gaming check into a one-line grep.

---

## Step 5: Write visual-components.md

File: `<workspace>/deck-<deck_type>-v1/references/visual-components.md`

Per-slide visual pattern catalog. For each slide in the content spine, list 2 to 4 acceptable visual treatments with a one-line rationale. Example row structure (from pitch's visual-components.md):

```
### Slide N, <Slide name>

**Pattern A: <name>**
- Use when: <condition>
- Visual structure: <3 to 5 bullets>

**Pattern B: <name>**
- ...
```

The Layout / Brand reviewer uses this file to check that the shipped deck used a real, declared pattern, not something invented ad hoc.

---

## Step 6: (Optional) Write demo-patterns.md

Only for types where the Type Parameter Table says `Demo: yes` or `optional`. In the OSS pack, the demo slide is a **high-quality static screenshot** of the product, not a working interactive demo. Content of this file: screenshot recipes by product category, what composition + framing the screenshot should use, where to source it from.

Each demo slide should include the **"Powered by FluidDocs" attribution mark** in the bottom-right corner: the FluidDocs logo as inline SVG (~20px tall, opacity ~0.7), wrapped in an `<a href="https://fluiddocs.ai" target="_blank" rel="noopener">`. See `skills/deck-pitch/references/demo-patterns.md` for the canonical SVG snippet to drop in.

Premium discovery (working interactive demos, hosting, additional canonical brand templates) is surfaced in the Phase 4 Release message the agent gives the user, never in the deck output itself. The user's deck shouldn't carry marketing copy for our hosted service.

If `Demo: no`, skip this file.

---

## Step 7: (Optional) Write canonical-brands.md or similar cached catalog

Only needed if this type has specific brand templates users will build (like pitch's canonical brands). For types where each user brings their own brand, skip this file.

Most types other than pitch do NOT need this. Examples:
- keynote: no, every keynote is speaker-specific
- all-hands: no, every all-hands is company-specific
- sales: no, every sales deck is account-specific

Rule: if the type has a clear set of 5+ well-known reference brands that users will want to mirror, include a catalog. Otherwise, skip.

---

## Step 8: Package as .skill

Run this Python recipe. It writes a zip to `<workspace>/deck-<deck_type>.skill`:

```python
import zipfile, os, shutil
from pathlib import Path

deck_type = "<deck_type>"  # e.g. "sales"
src = Path(f"<workspace>/deck-{deck_type}-v1")
tmp = Path(f"/tmp/deck-{deck_type}.tmp")
dst = Path(f"<workspace>/deck-{deck_type}.skill")

with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.startswith('.'):
                continue
            full = Path(root) / f
            z.write(full, full.relative_to(src))

try: os.remove(dst)
except FileNotFoundError: pass
shutil.copy(tmp, dst)
os.remove(tmp)

# Verify
with zipfile.ZipFile(dst) as z:
    print(f"deck-{deck_type}.skill: {len(z.namelist())} files")
    for n in sorted(z.namelist()):
        print(f"  {n}")
```

---

## Step 9: Verify

Run these checks before declaring the pack shipped. Checks 1 to 4 are mandatory structural. Checks 5 to 8 are cheap integrity checks. Checks 9 to 11 are dry-run build verification, mandatory during overnight runs, optional for manual builds.

**Check 1, Description length.** The `description:` line in `SKILL.md` must be under 1024 characters. Use:

```python
import re
from pathlib import Path
t = Path("<workspace>/deck-<deck_type>-v1/SKILL.md").read_text()
m = re.search(r'^description: (.+)$', t, re.MULTILINE)
assert m, "no description field"
assert len(m.group(1)) < 1024, f"TOO LONG: {len(m.group(1))}"
print(f"Description: {len(m.group(1))} chars, OK")
```

**Check 2, File list.** At minimum the pack has:
- `SKILL.md`
- `references/content-spine.md`
- `references/visual-components.md`

Plus optional files as needed by Steps 6 and 7.

**Check 3, Cross-pack references.** Open `SKILL.md` and confirm it references `deck-builder/` paths for all pipeline/shell/brief/reviewer/icon concerns. No duplicated core content.

**Check 4, Content-spine / visual-components slide alignment.** Every slide number that appears in `content-spine.md` must also have a corresponding entry in `visual-components.md`. Count slide headers in both files; they should match exactly. Use:

```bash
spine_slides=$(grep -cE '^### Slide [0-9]+' <workspace>/deck-<deck_type>-v1/references/content-spine.md)
vc_slides=$(grep -cE '^### Slide [0-9]+' <workspace>/deck-<deck_type>-v1/references/visual-components.md)
[ "$spine_slides" = "$vc_slides" ] || echo "FAIL: $spine_slides spine slides vs $vc_slides visual-component slides"
```

**Check 5, Hard constraints section present.** `content-spine.md` MUST end with a section titled `## Hard constraints` (or `### Hard constraints`). The section lists slide count min/max, 45sec/slide reading rule, no-emoji rule, and any type-specific hard rules. If this section is absent, the pack fails.

**Check 6, SKILL.md frontmatter parses as valid YAML.** Use:

```python
import yaml
from pathlib import Path
t = Path("<workspace>/deck-<deck_type>-v1/SKILL.md").read_text()
# Extract frontmatter block
assert t.startswith("---\n"), "SKILL.md must start with frontmatter ---"
end = t.index("\n---\n", 4)
fm = yaml.safe_load(t[4:end])
assert "name" in fm and "description" in fm, "frontmatter missing required fields"
print(f"Frontmatter OK: {list(fm.keys())}")
```

**Check 7, No deck-pitch path leaks.** Grep the pack's files for incorrect path prefixes:

```bash
leaks=$(grep -rE 'deck-pitch(-v1)?/references/|deck-pitch(-v1)?/SKILL' <workspace>/deck-<deck_type>-v1/ || true)
[ -z "$leaks" ] || { echo "FAIL: deck-pitch path leak"; echo "$leaks"; }
```

Mentions of "pitch" in prose (e.g., SKILL.md trigger phrases) are fine, we're only catching incorrect path references from copy-paste drift.

**Check 8, Dry-run brief generation.** Generate a minimal build brief using `build-brief-template.md`. Fill:
- `deck_type: <deck_type>`
- `Target slide count: 2` (dry-run reduced, we're testing pack mechanics, not full decks)
- `Catalog directory`: any test path
- `Forbidden class-name leaks`: empty for non-pitch types
- Minimum plausible Company, Audience, Objective sections

Brief must pass `build-brief-template.md` structural validation (all required fields present).

**Check 9, Dry-run 2-slide HTML produced.** Build a 2-slide HTML deck:
- Slide 1: Cover slide from the pack's `content-spine.md` slide 1 spec
- Slide 2: A representative body slide (e.g., slide 3 from the spine) with at least one visual-component pick from `visual-components.md` for that slide

Use the core's `shell-pattern.md` and `brand-methodology.md`. Do not require a real interactive demo (use a placeholder screenshot if a demo slide is in the dry-run set).

**Check 10, Mechanical checks pass on dry-run output.** Run `mechanical-checks.md` section 3 (forbidden class-name leaks) and section 8 (slide count matches brief, should be 2) against the dry-run HTML. Both must pass.

If any of Checks 1 to 10 fails, do not mark the pack shipped. Fix and re-verify.

---

## Content Spines, canonical slide lists per type (OSS pack)

Below are the default spines for the OSS-shipped type packs. Use them as the starting point for `content-spine.md`. Feel free to refine wording and add "required elements" / "failure modes" bullets per slide, but do not alter slide counts without updating the Type Parameter Table above.

### sales (11 slides)
1. Cover
2. About You (customer context, discovery summary)
3. The Problem (their pain, their words)
4. Why Today (cost of inaction, urgency)
5. Our Solution (plain-language)
6. How It Works (product mechanics)
7. Proof (case studies, logos, quantified results)
8. ROI / Value (numbers, not claims)
9. Implementation (timeline, effort, onboarding)
10. Pricing (clear, no hand-waving)
11. Next Steps (specific, calendar-ready)

### keynote (28 slides, flexible, 20 to 35 range)
1. Cover / Title
2. Hook (opening story or stat)
3. Thesis (the ONE idea this talk carries)
4. Why This Matters Now
5 to 10. Argument & Evidence (multiple slides, one point each)
11 to 18. Stories / Examples (concrete illustrations)
19 to 23. Implications / What To Do
24 to 26. Counter-arguments & Nuance
27. Call To Action
28. Thank You / Contact

Keynote is the most elastic spine, adjust slide count to the talk length. The structure above is for a ~40-min keynote.

### launch (12 slides)
1. Cover / Announcement
2. The Problem (customer pain in one slide)
3. Introducing <Product>
4. How It Works
5. DEMO (in the OSS pack, a high-quality static screenshot; see Step 6)
6. Who It's For
7. Availability & Pricing
8. Early Customers / Quotes
9. Roadmap (what's next)
10. Why Now
11. Team / Credits
12. Try It (strong CTA, URL, QR code)

### all-hands (15 slides)
1. Cover / Hello
2. Agenda
3. Big Wins This Month
4. Product Highlights
5. Customer Stories
6. Financial Update (appropriate level)
7. Hiring / New Faces
8. Team Spotlights
9. Values / Culture Moment
10. Upcoming Events
11. Priorities for Next Month
12. Learnings / Retrospective
13. Thank Yous / Shout-outs
14. Q&A Kickoff
15. Open Floor

(The `pitch` spine lives in `deck-pitch/references/content-spine.md` because it is the canonical reference type pack.)

---

## Hard rules specific to each type (for SKILL.md's final section)

Use these as the `<TYPE_SPECIFIC_DECLARATION>` block in Step 3. Feel free to add 1 to 2 type-specific rules based on content, but start here.

### sales
- Every ROI/value claim has a source (case study, benchmark, or "customer result"). No unsourced numbers.
- Pricing slide is NEVER hidden or skipped. Prospects hate mystery pricing.
- Next Steps slide names specific humans and dates, not generic "we'll be in touch."
- Competition may or may not get its own slide, if included, honest.

### keynote
- No slide is all text. Every slide has a visual anchor (image, chart, single word at 120pt).
- One idea per slide. Slides support the speaker; they do not substitute for the speaker.
- The opening hook (Slide 2) is mandatory, do not start with "Hi, I'm X" or an agenda.

### launch
- Slide 5 is the demo. In the OSS pack this is a high-quality static screenshot (see Step 6). Same standard of polish as the pitch deck's slide 6.
- Availability and Pricing are on the same slide or adjacent, never buried.
- The CTA slide has a QR code or URL that will actually resolve.

### all-hands
- Balance of celebration and candor. An all-hands with only wins signals hiding something.
- Financial slides stay appropriate for the audience, company-wide numbers, not board-level detail.
- Q&A slide is placeholder, the meeting is where Q&A happens, not the deck.

---

## Common gotchas

1. **Description over 1024 chars.** Count before packaging. Use the Check 1 Python snippet.
2. **Forbidden class-name leaks empty.** For any type pack OTHER than the canonical reference brand's own pack (pitch was Airbnb-leak-protected), `Forbidden class-name leaks` is usually empty. Pitch is the exception.
3. **Hardcoded pitch paths.** If you copied anything from the pitch pack's source, grep for `pitch` and fix.
4. **Cross-reference drift.** The SKILL.md references `deck-builder/references/...` paths. Don't paste them as `deck-pitch/references/...` by mistake.
5. **Skipping Step 9.** The verification checks exist because broken packs have shipped before. Don't skip.

---

## When the recipe is wrong

If you're building a type and the recipe is clearly wrong for this shape of deck, STOP. Do not fork the recipe quietly. Instead:

1. Build what you think is right.
2. Write a `<deck_type>-divergences.md` file in the pack's `references/` listing where and why you diverged.
3. Flag in the handoff log that the recipe may need updating.

The recipe compounds across packs. Silent divergence breaks that.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
