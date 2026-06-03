# Confirmation Block Template

This is the UX bridge between automated analysis and user approval. The user just uploaded a deck file, they don't want to answer 20 questions, and they don't want to skim a 200-line brief. They want to see what was detected, correct anything wrong, and approve.

**Design goal**: fit the confirmation block on one screen. A busy founder reads it in 15 seconds. They reply "go" or they reply with three word-level corrections.

The confirmation block is **type-aware**, the detected deck type (pitch, sales, launch, keynote, all-hands) drives which spine the slide roles come from and which `deck-*` skill Phase 3 will hand off to.

---

## The template

Render this to the user as plain text (or lightweight markdown, no tables required). Fill in every `{{placeholder}}`.

```
Extracted your {{page_count}}-slide deck from `{{source_filename}}`. Here's what I detected, reply "go" to build, or tell me what to change:

  PPTX available?  {{pptx_status_line}}
  Build mode       {{build_mode_line}}
  {{prior_imports_line}}

  Deck type      {{deck_type}} ({{type_confidence}} confidence){{alternatives_hint}}
  Handoff skill  {{handoff_skill}}{{mode_a_handoff_note}}

  Company        {{company_name}}
  Context        {{context_line}}
  Slide count    {{page_count}} (preserving 1:1)

  Palette        {{primary_hex}} primary · {{surface_hex}} surface · {{ink_hex}} ink{{accent_line}}{{mode_a_palette_note}}
  Typography     Display: {{display_font}} · Body: {{body_font}}{{mode_a_typography_note}}
  Scale          {{scale_values}}

  Slide roles    {{slide_role_list}}
  {{low_confidence_lines}}

  {{demo_line_if_applicable}}
  {{missing_spine_line}}

Output path      {{output_path}}

Reply "go" to build. Or edit any field (e.g., "reconstruction" to switch from page-image to HTML rebuild, "this is a sales deck not a pitch", "company should be Acme AI", "palette primary is #0066FF", "slide 7 is Integrations", "interactive demo").
```

---

## Placeholder rules

### `{{pptx_status_line}}`, Hard PPTX availability row (PDF input only)

Always show this row when input was PDF. Three states:

- PPTX detected and used: `yes, pulled icons, gradients, custGeom from {{pptx_filename}}`
- Sibling PDF detected, no PPTX: `unknown, drop into uploads to enable 5x fidelity`
- User has already replied "no PPTX available": `no, using PDF-only extraction (lower fidelity on diagrams + icons)`

This row is mandatory because silent PPTX-absent detection cost 3+ iteration rounds in past runs when the user actually had a PPTX they didn't know to share.

When input was PPTX (auto-detect routed to PPTX-only path), omit this row entirely.

### `{{build_mode_line}}`, Hard Build Mode row

Always show this row. Two states:

- Default (Mode A): `page-image (default, pixel-faithful, each slide is the source page)\n                   Reply "reconstruction" to rebuild slides in HTML/CSS instead`
- User opted into Mode B: `reconstruction (HTML/CSS rebuild, editable, palette + typography are load-bearing below)\n                   Reply "page-image" to switch back to source-faithful default`

If Step 0d's prior-output scan pre-filled Mode B because existing imports used reconstruction (rare), explain on the second line: `Matched style of {{prior_file}}.`

### `{{prior_imports_line}}`, optional

Only shown when Step 0d found prior `*-Imported.html` files in the user's workspace whose filename matches the detected company or whose shell signature matches a known mode.

Format: `Prior imports    {{file1}}, {{file2}}\n                   {{summary}}`

Where `{{summary}}` is one of:
- `Both use page-image, matching style.`
- `Both use reconstruction, matching style.`
- `Mixed: {{file_a}} is page-image, {{file_b}} is reconstruction. Defaulting to page-image, reply otherwise to switch.`

Skip this row entirely when no prior imports are found.

### `{{mode_a_handoff_note}}` / `{{mode_a_palette_note}}` / `{{mode_a_typography_note}}`, Mode A demotions

When `build_mode: page-image`, append ` (role-label vocabulary only; Mode A skips HTML handoff)` to the Handoff Skill line, append ` (sampled; informational in Mode A)` to the Palette line, and append ` (informational in Mode A)` to the Typography line. This makes it visible to the user that those fields don't materially affect the build under Mode A.

When `build_mode: reconstruction`, these placeholders resolve to empty strings.

### `{{deck_type}}`
The winning type from the classifier: one of `pitch`, `sales`, `launch`, `keynote`, `all-hands`.

### `{{type_confidence}}`
`high`, `medium`, or `low` from the classifier.

### `{{alternatives_hint}}`
Only shown when confidence is `medium` or `low`. Format: `, or maybe {{alt1}} or {{alt2}} (reply with type to switch)`. This is the escape hatch for ambiguous decks.

### `{{handoff_skill}}`
The matching `deck-*` skill: `deck-pitch`, `deck-sales`, `deck-launch`, `deck-keynote`, `deck-all-hands`. Surfaced so the user sees which pipeline will run and can flag if it's wrong.

### `{{company_name}}`
From metadata.title, or cover-slide largest text. If uncertain, use best guess followed by `(confirm)`.

### `{{context_line}}`
Type-dependent second-line context. Use whichever fits the detected type:

- **pitch**, `Stage {{stage}} · Sector {{sector}}`
- **sales**, `Industry {{industry}} · Deal size {{deal_size}}` (guess-best; skip unknown)
- **launch**, `Product {{product}} · Availability {{availability}}`
- **keynote**, `Venue {{venue}} · Talk length {{minutes}} min` (often unknown; show `Talk {{page_count}} slides` as fallback)
- **all-hands**, `Company size {{size}} · Meeting {{month}}`

Skip fields that can't be inferred. This is a hint, not a form to fill.

### `{{page_count}}`
Integer from metadata.

### `{{primary_hex}}` / `{{surface_hex}}` / `{{ink_hex}}`
From palette detection. Use uppercase hex.

### `{{accent_line}}`
If accent is not null: ` · {{accent_hex}} accent`. Else: empty string.

### `{{display_font}}` / `{{body_font}}`
Use the Google-Font stand-in name. If detected != web, annotate: `Inter (source: Neue Haas Grotesk)`.

### `{{scale_values}}`
Comma-separated list of px values: `13, 15, 19, 24, 32, 48`.

### `{{slide_role_list}}`
Comma-separated list of detected roles in slide order, using the winning type's spine vocabulary. Keep on one line if <=14 slides. If longer (keynotes), break into two lines.

Example for a detected `pitch`:
```
Slide roles    Cover, Problem, Why Now, Solution, Product, Demo, Market, Business Model,
               Traction, Competition, Moat, GTM, Team, Ask
```

Example for a detected `all-hands`:
```
Slide roles    Cover, Agenda, Big Wins, Product Highlights, Customer Stories,
               Financial Update, Hiring, Team Spotlights, Values, Upcoming Events,
               Priorities, Learnings, Shout-outs, Q&A, Open Floor
```

### `{{low_confidence_lines}}`
For each slide with medium or low role confidence, add one line:
```
               Slide {{N}} labeled "{{role}}" (medium confidence), confirm?
               Slide {{N}} labeled "Content" (low confidence), assign a role?
```

### `{{demo_line_if_applicable}}`
Only for types that use a Demo slide (pitch, launch). Shows the default mode AND the opt-in for an interactive build BEFORE Phase 3 runs, this is a first-class choice, not a post-build upgrade hint:

```
Demo slide     Slide {{demo_slide_num}}, static screenshot (default)
               Reply "interactive demo" to build a working one instead
```

If the user previously approved `demo_mode: interactive` and the block is being re-rendered, flip the line:

```
Demo slide     Slide {{demo_slide_num}}, interactive demo (opted in)
               Reply "static demo" to fall back to a screenshot
```

For types without a Demo slide (keynote, all-hands, sales), omit this line entirely, those types don't have a Demo spine role, and fabricating one would be a redesign, not a conversion.

### `{{demo_mode}}` (brief field, not rendered as a separate line)

Recorded in the conversion brief §6. Two legal values:
- `static`, default. Phase 3 renders the demo slide as a static screenshot (or faithful HTML/CSS/SVG reproduction of the source's product state, no interactivity beyond shell/nav).
- `interactive`, user opted in. The OSS pack does not bundle a working interactive demo builder; surface the gap to the user. The demo slide carries the "Powered by FluidDocs" attribution mark (FluidDocs logo SVG, bottom-right). No upsell appears inside the deck.

### `{{missing_spine_line}}`
If any canonical spine roles for the detected type are missing from the deck, add one line:
```
Spine gaps     Your deck doesn't have a {{list of missing roles}} slide, preserving source as-is, not adding.
```

### `{{output_path}}`
Default: `<user-workspace>/{{company}}-{{type}}-Imported.html`. User can override.

---

## Example filled templates

### Pitch deck (high confidence)
```
Extracted your 14-slide deck from `Acme-Pitch-Q2.pdf`. Here's what I detected, reply "go" to build, or tell me what to change:

  Deck type      pitch (high confidence)
  Handoff skill  deck-pitch

  Company        Acme
  Context        Stage Series A · Sector Vertical AI (Legal)
  Slide count    14 (preserving 1:1)

  Palette        #0B1220 primary · #F8FAFC surface · #0B1220 ink · #F97316 accent
  Typography     Display: Playfair Display (source: Tiempos Headline) · Body: Inter
  Scale          13, 15, 19, 24, 32, 48

  Slide roles    Cover, Problem, Why Now, Solution, Product, Demo, Market, Business Model,
                 Traction, Competition, Moat, GTM, Team, Ask

  Demo slide     Slide 6, static screenshot (default)
                 Reply "interactive demo" to build a working one instead

Output path      <user-workspace>/Acme-pitch-Imported.html

Reply "go" to build. Or edit any field.
```

### Sales deck (medium confidence, alternative surfaced)
```
Extracted your 11-slide deck from `Acme-Customer-Deck.pdf`. Here's what I detected, reply "go" to build, or tell me what to change:

  Deck type      sales (medium confidence), or maybe pitch (reply with type to switch)
  Handoff skill  deck-sales

  Company        Acme
  Context        Industry SaaS · Deal size mid-market
  Slide count    11 (preserving 1:1)

  Palette        #111827 primary · #F9FAFB surface · #111827 ink
  Typography     Display: Inter · Body: Inter
  Scale          13, 15, 19, 24, 32, 48

  Slide roles    Cover, About You, Problem, Why Today, Solution, How It Works,
                 Proof, ROI, Implementation, Pricing, Next Steps

Output path      <user-workspace>/Acme-sales-Imported.html

Reply "go" to build. Or edit any field.
```

---

## Handling the user's response

Parse the reply:
- **"go", "ship it", "looks good", "approved", "yes"**, mark brief Approved, move to Phase 3.
- **"this is a <type> deck"** or **"it's actually a <type>"**, override detected type, re-run per-slide classification with the new spine, re-render the block.
- **"interactive demo", "build the demo", "make it interactive"**, flip `demo_mode: interactive` in the brief, re-render the block so the user sees the new demo line before approving. Only valid when detected type is pitch or launch AND a Demo slide was detected; if not, reply politely that the detected type has no Demo slide and interactive demos only apply to pitch / launch.
- **"static demo", "screenshot demo", "undo interactive"**, flip `demo_mode: static`, re-render.
- **"change X to Y"** pattern, update the brief, re-render.
- **A long list of edits**, apply all, re-render once, ask "anything else?"
- **A question**, answer it, don't restart the flow.
- **A new file**, restart from Phase 0.

### Re-render rule

After any edit, re-render the FULL confirmation block with the changes applied, don't just reply "updated". The user needs to see the current state before approving. This prevents drift between what they think they approved and what actually shipped.

### Type override mechanics

When the user overrides the deck type:
1. Look up the target spine in `spine-tables.md`.
2. Re-run per-slide classification using that spine's role keywords (one-liner: re-call `classify_page(..., type_name=new_type)` for each slide).
3. Update the handoff skill.
4. Re-render the whole block.

Don't silently accept the override, show the user the re-classified role list so they can confirm it looks right for the new type.

### Low-friction edits

Accept natural-language phrasing:
- "palette primary should be #0066FF"
- "the company is actually called Acme Legal"
- "slide 7 is Integrations not Product"
- "this is a launch deck, not a pitch"
- "use deck-keynote instead"

---

## What NOT to include

- The canonical spine expectation for the detected type (it's implicit, the user sees their own slide roles above)
- Reviewer details (Phase 4, not surfaced here)
- Technical implementation choices (canvas size, shell variant)
- Type-specific UX decisions already locked by this skill (mirror fidelity, preserve slide count, static demo)

Keep it under 22 lines. If it exceeds 22, detection is too noisy, tighten classification before asking the user.
