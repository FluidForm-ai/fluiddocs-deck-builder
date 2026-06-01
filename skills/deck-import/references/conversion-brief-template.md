# Conversion Brief Template

A scoped-down version of deck-builder's build-brief-template, specific to PDF-or-PPTX-to-HTML deck conversion. Used by Phase 3 (Build) as the single source of truth, and by Phase 4 (Review) as the diff target.

This brief is **type-parameterized**, the detected deck type drives the spine used for per-slide role labels, the context fields shown in §1, and the handoff skill reviewers consult for type-specific calibration.

Saved as `<Company>-<Type>-Conversion-Brief.md` alongside the output HTML file. Status transitions: Draft (Phase 1), Approved (end of Phase 2), In Build (Phase 3), In Review (Phase 4), Released (Phase 5).

---

## Template

Copy everything below the line into the brief file and fill in. Replace every `{{placeholder}}`. Sections marked `(type-conditional)` should be populated only when the detected type uses them.

---

```markdown
# {{Company}}, Source-to-HTML Conversion Brief

**Source file**: `{{absolute path to source .pdf or .pptx}}`
**Source format**: `{{pdf | pptx}}`
**Extraction timestamp**: `{{ISO 8601}}`
**Output path**: `{{absolute path to output HTML}}`
**Status**: Draft / Approved / In Build / In Review / Released
**User approver**: {{user name}}
**Date approved**: {{YYYY-MM-DD}}

## Deck type + mode

- **Detected deck type**: {{pitch / sales / launch / keynote / all-hands}}
- **Type detection confidence**: {{high / medium / low}}
- **Top alternatives considered** (score-ranked): {{type1 (score), type2 (score)}}
- **Handoff skill**: {{deck-pitch / deck-sales / deck-launch / deck-keynote / deck-all-hands}}
- **Conversion mode**: source-mirror (not a redesign)
- **Build mode**: {{page-image | reconstruction}}
- **Target slide count**: {{N}} (preserving source 1:1)
- **Canonical slide-count band for this type**: {{e.g., pitch 11 to 17, keynote 20 to 35, sales 9 to 13}}, used only as a sanity marker, NOT enforced. We preserve what the source has.
- **Aspect ratio**: {{detected from source}} (letterbox on 1440x810 canvas if not 16:9)

## 1. Context (type-dependent, fill only what applies)

Pick the subsection below matching `Detected deck type` and delete the others.

### 1a. pitch (type-conditional)
- **Stage**: {{pre-seed / seed / Series A / Series B / ...}}
- **Sector**: {{Vertical AI (Legal) / Developer Tools / Marketplace / ...}}
- **One-line positioning** (if extracted, else `[derive from cover]`): {{positioning}}

### 1b. sales (type-conditional)
- **Industry / ICP**: {{buyer industry or persona}}
- **Deal size band**: {{SMB / mid-market / enterprise, if inferable}}
- **ROI claims present**: {{yes/no, if yes, list slide numbers}}

### 1c. launch (type-conditional)
- **Product name**: {{product}}
- **Availability**: {{date / GA / waitlist if inferable}}
- **Pricing present**: {{yes/no}}
- **Demo slide present**: {{yes/no, slide number}}

### 1d. keynote (type-conditional)
- **Venue / event**: {{conference name if inferable}}
- **Talk length**: {{minutes if inferable, else derive from slide count}}
- **Core thesis** (one line, extracted from opening slides): {{thesis}}

### 1e. all-hands (type-conditional)
- **Company size**: {{headcount if known}}
- **Meeting date / cadence**: {{YYYY-MM, monthly / quarterly}}
- **Candor check**: {{any slide mentioning misses/losses, yes/no}} (advisory, only-wins decks flagged in §9)

Skip any subsection that doesn't correspond to the detected type. If type later changes via user override in Phase 2, rebuild this section from the new type's subsection.

## 1.5 Locked tokens (FROZEN after Phase 2 approval)

These values do NOT change after the user replies "go" in Phase 2. They are the canonical reference for every styling decision in Phase 3 and Phase 4. Adjusting them mid-build resets the iteration count, common cause of stylesheet drift and round-after-round breakage.

- **Palette tokens** (hex): see §3, locked
- **Typography scale** (5 to 7 px values): see §4, locked
- **Card styling**: border `{{none / solid Xpx COLOR}}`, padding `{{Y}}px`, radius `{{R}}px`, surface `{{COLOR}}`, locked
- **Photo close-up frame size** (slide 14 etc.): `{{W}}x{{H}}` px @ aspect ratio `{{W:H}}`, locked
- **Product thumbnail frame** (slide 5 etc.): `{{S}}x{{S}}` px square, locked
- **Subject-fill ratio** (when generating thumbs from variable source images): tighten inward by `{{10 to 15}}%` so subject occupies same visual portion across all thumbs, locked

If user feedback requires changing a locked token mid-build, surface the change explicitly: "This will require resetting the styling pass, confirm." Then update the brief, mark prior approval void, regenerate the brief block, get explicit re-approval.

This locked-tokens contract was added after multiple runs where roughly 5 rounds of CSS thrash happened because card border/padding/radius kept getting adjusted alongside positioning. Lock once; iterate only on content/position.

## 2. Source fidelity targets

- **Was OCR fallback triggered?** {{yes/no}}, if yes, role confidence ceilings lowered by one step during classification.
- **Source had hero images on slides**: {{list of slide numbers}}
- **Source cover has extractable company logo image?** {{yes/no}}, if yes, re-embed at `/assets/cover-logo.{{ext}}`. If no, use `<text>` wordmark with detected display font.
- **Source image content classification** (per slide): {{photographic-real / ai-stylized / illustration / chart}}, see §3 of `references/image-sourcing.md`. If any slides are `ai-stylized`, set `imagery_swap_offered: {{yes/no}}` based on user's Phase 2 reply.

## 3. Palette (source-detected)

- **Primary**: `#______` · detection confidence: {{high/medium/low}}
- **Surface**: `#______`
- **Ink**: `#______`
- **Muted**: `#______`
- **Accent (optional)**: `#______` or `null`
- **Border/divider**: `color-mix(in oklab, <ink> 15%, transparent)` (computed)

## 4. Typography (source-detected)

- **Display, detected**: {{name}} · **web stand-in**: {{Google Font}}
- **Body, detected**: {{name}} · **web stand-in**: {{Google Font}}
- **Mono, detected**: {{name or null}} · **web stand-in**: {{Google Font or null}}
- **Typographic scale (px, locked)**: {{list of 5 to 7 values}}, every CSS `font-size` must match one of these.

Minimums: body >=14px, card body >=13.5px, legible metrics >=22px. If the detected scale has a body value below 14px, bump to 14px and note.

## 5. Per-slide role map (type spine + source slides)

The role vocabulary below is the detected type's spine. Do NOT substitute pitch-spine vocabulary into a non-pitch deck. For the full keyword tables per type, see `references/spine-tables.md`.

| # | Role (from {{detected_type}} spine) | Confidence | Source text snippet (first 30 words) | Hero image? | Notes |
|---|---|---|---|---|---|
| 1 | Cover | high | | yes/no | |
| 2 | {{spine role}} | high | | yes/no | |
| 3 | {{spine role}} | medium | | no | flagged in confirmation |
| ... | | | | | |

**Spine coverage** (present vs. missing, advisory):
- Present: {{list}}
- Missing canonical roles for this type: {{list}}, preserving source as-is, not adding.

The "missing roles" list is advisory. We do NOT insert slides to fill gaps in conversion mode, that would be a redesign.

## 6. Demo slide handling (type-conditional)

Demo slides are canonical for **pitch** and **launch** only. For other types, this section is omitted.

- **Does the detected type have a Demo spine role?** {{yes/no}}
- If **no**: skip this section entirely.
- If **yes**:
  - **Demo slide number**: {{N}}
  - **demo_mode**: `{{static | interactive}}`, chosen by user in Phase 2 confirmation. Default is `static`; user flips to `interactive` by replying "interactive demo" in the confirmation block.
  - **If `demo_mode: static`**:
    - Render as static screenshot of page {{N}} as full-bleed hero with caption "Static preview". Or, if the source's product state can be faithfully reproduced in HTML/CSS/SVG (form fields, device frames, bubbles, pricing cards), use that; no fabricated interactivity, state frozen to what the source shows.
    - Drop the "Powered by FluidDocs" attribution mark in the bottom-right of the demo slide (FluidDocs logo as inline SVG, opacity ~0.7, linking to fluiddocs.ai). See `skills/deck-pitch/references/demo-patterns.md` for the canonical SVG snippet.
    - Post-build Release message to the user surfaces "upgrade demo" as a follow-up hook (FluidDocs Premium link). The upsell lives in the release message, never inside the deck.
  - **If `demo_mode: interactive`**:
    - The OSS pack does not bundle a working interactive demo builder. Surface the gap to the user. The demo slide still carries the "Powered by FluidDocs" attribution mark; the Premium upgrade hook is surfaced in the Phase 4 Release message, not inside the deck.

## 7. Build decisions

- **Nav variant**: {{A for editorial/serif, B for kinetic/sans}}, inherited from deck-builder shell-pattern.md.
- **Forbidden class-name leaks**: standard non-Airbnb list, `comp-matrix`, `listing-grid`, `rausch`, `bélo`, `belo-mark`. Plus any class names the source deck's original brand used if known.
- **Content-fidelity policy**: verbatim text from source. Copy-edit only for: OCR artifacts, hyphenation breaks, whitespace. Any meaning change is flagged to user in Release.

## 8. Height budget per slide

| # | Role | Source page height (derived from image) | Target canvas budget | Overflow risk |
|---|---|---|---|---|
| 1 | Cover | {{px}} | 700px (content-area on 900p) | low |
| 2 | {{role}} | {{px}} | 640px | |
| ... | | | | |

Any slide projected >90% of budget, flag for trimming or hero-image resize in Phase 3.

## 9. Known risks for THIS conversion

- **OCR confidence**: {{any flags from Phase 0}}
- **Palette ambiguity**: {{flags from palette detection}}
- **Role classification gaps**: {{list of low-confidence slides}}
- **Missing spine roles for detected type**: {{list}}, preserving source as-is, not adding.
- **Type detection ambiguity**: {{if confidence was medium/low, list the runner-up type(s) and the scores}}.
- **Type-specific red flags** (surface the ones matching the detected type):
  - sales with ROI claims but no sourcing, surface.
  - all-hands that is only wins, no candor, surface.
- **Source aspect ratio**: {{16:9, 4:3, 1:1, other}}, letterbox strategy notes.

These red flags are **advisory**, not blockers. In conversion mode we preserve the source as-is; the role of §9 is to give the user a follow-up list for a separate native-build pass.

## 10. Approval

- [ ] User reviewed confirmation block
- [ ] User approved (reply "go" or explicit edits, re-rendered, approved)
- Date approved: ____

No HTML gets written until this line has a date.
```

---

## How reviewers use this brief in Phase 4

Same contract as deck-builder's build-brief-template, but the targets are type-aware:

- **Brand Reviewer** checks §3 (palette detected vs. CSS tokens vs. source sampled palette, three-way agreement).
- **Layout Reviewer** checks §8 (height budget per slide vs. shipped), §7 (forbidden classes), section count = §0 target.
- **Copy Reviewer** runs the conversion-mode rubric with calibration per handoff skill:
  - `deck-pitch`, working-demo-score SUSPENDED per §6 (static demo is per-brief).
  - `deck-sales`, ROI sourcing check, pricing-present check.
  - `deck-launch`, working-demo SUSPENDED per §6, Availability & Pricing co-located check.
  - `deck-keynote`, one-idea-per-slide check, opening-hook check.
  - `deck-all-hands`, candor balance, company-appropriate financials.

Reviewers consult §9 to understand which risks the user has already been made aware of, those are advisory, not blockers. If any shipped element diverges from the brief, the divergence is the bug.
