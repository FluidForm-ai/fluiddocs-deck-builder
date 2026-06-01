# Contributing to FluidDocs Deck Builder

Thanks for considering a contribution. This project is maintained by FluidDocs, but PRs from the community are welcome and we want this to feel like a real OSS project, not a vanity drop.

## Quick orientation

This repo ships **8 skills** that turn a coding agent (Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI, anything that reads `SKILL.md`) into a deck builder.

- `skills/deck-builder/` is the core. Owns the 5-phase pipeline, the canvas, the reviewer specs, the shell, the brief template.
- `skills/deck-pitch/`, `skills/deck-sales/`, `skills/deck-launch/`, `skills/deck-keynote/`, `skills/deck-all-hands/` are type packs. Each declares only what is type-specific.
- `skills/deck-import/` handles PDF and PPTX import.
- `skills/deck-critique-lite/` produces 5 to 7 observations on a pitch deck.

`templates/` ships 8 ready-to-fork starting decks. `scripts/` holds the local save fallback and the PPTX extractor. `examples/` holds end-to-end demo runs.

---

## Filing issues

We accept four issue types. Pick the matching label when you open the issue.

1. **bug.** A skill produced wrong output, a template renders broken, a script throws. Include the input (or a small repro), the expected output, the actual output, and the agent you ran it on.
2. **feature.** A capability the pack does not have today. Tell us the use case, not the implementation. We will figure out the where.
3. **template request.** You want a specific brand or category template that does not exist yet (e.g., "Notion all-hands template," "Linear sales template"). Include 2 or 3 reference screenshots from the source brand so a contributor can build against a clear target.
4. **deck-type request.** You want a new deck type beyond the 5 we ship (pitch, sales, launch, keynote, all-hands). Tell us the deck type, the audience, the spine you would expect (5 to 14 slides), and a sample brief.

Reproduction steps are appreciated but not required for any issue type. We would rather have an imperfect issue than no issue.

---

## Proposing a new template

Templates are single self-contained HTML files. No external dependencies, no build step, no framework. The pattern is mechanical once you have seen it done.

1. **Clone an existing template** that is closest to what you want. For brand pitch templates, start from `templates/airbnb/airbnb-pitch.html`. For deck-type defaults, start from `templates/sales-default/sales-default.html`.
2. **Swap the brand tokens** at the top of the `<style>` block. Look for the `/* === BRAND TOKENS ... === */` marker. Replace color hexes, font family, font sizes, spacing scale. The rest of the template inherits.
3. **Replace the content** slide by slide. Keep the slide count and structure. Swap copy, swap images, swap logo SVG.
4. **Verify the inline-edit module still works.** Press E to toggle edit mode, edit any text, refresh the page, confirm the edit persisted in localStorage. Press Ctrl+S (or Cmd+S on macOS) and confirm the download triggers.
5. **Run the 3 reviewers manually** (or via the agent). Brand for token consistency, Copy for tone and density, Layout for slide-by-slide visual hierarchy. See `skills/deck-builder/reviewers/` for the specs.
6. **Open a PR.** Add a folder under `templates/<your-template-name>/` with the single HTML file. Update `templates/index.html` to include your template card.

File size guideline: 60 KB to 180 KB. Under 60 KB usually means thin content. Over 180 KB usually means inline images that should be hosted externally.

---

## Proposing a new deck type

A new deck type is more work than a new template because you are extending the type-pack architecture, not adding a leaf. The pattern is documented in `PORTING-RECIPE.md` (sections on Pattern 5 and the per-skill checklist).

1. **Create the type pack directory** at `skills/deck-<your-type>/`.
2. **Write `SKILL.md`.** Use `skills/deck-sales/SKILL.md` as the template. Declare the deck type, the agent's behavior, the 5-phase pipeline invocation, the auto-preview step, the demo handling (if your type has a demo slide).
3. **Write `references/content-spine.md`.** This is the slide-by-slide spine for your deck type. Slide count, slide titles, what each slide should contain, what is required vs optional.
4. **Write `references/visual-components.md`.** This is the visual vocabulary for your type. Card patterns, layout grids, hero treatments, typographic anchors.
5. **Write `references/demo-patterns.md`** if your type has a demo slide. For OSS, demo slides are static screenshots. Document the framing, the composition, and what the screenshot should contain.
6. **Add a default template** at `templates/<your-type>-default/<your-type>-default.html`. The template is the proof that the spine works end-to-end.
7. **Open a PR.** We will review the spine for redundancy with existing types, the visual vocabulary for distinctness, and the default template for shipped quality.

Adding a new type is a multi-week effort. Open an issue first so we can sanity-check the type before you build it.

---

## The 3-reviewer model

Every deck this pack produces passes through 3 reviewers in parallel during Phase 3. PRs that tighten any reviewer's prompt are high-leverage.

- **Brand reviewer** (`skills/deck-builder/reviewers/brand.md`) checks that the CSS custom properties in `:root` match the declared brief, that brand-letter shapes match the source brand's actual logo, that no foreign colors leaked into the deck.
- **Copy reviewer** (`skills/deck-builder/reviewers/copy.md`) checks that no slide carries more than its density target, that tone matches the deck type, that headlines are specific (not "Our Solution"), that data points cite a source.
- **Layout reviewer** (`skills/deck-builder/reviewers/layout.md`) checks the deck-median visual density rule, the 7-distinct-font-size cap, the inline `display:none` and `justify-content:center` anti-gaming rules, the per-slide visual hierarchy.

When you contribute a reviewer change, run it against 3 existing templates and confirm the new rule does not regress any of them.

---

## Project conventions

- **No em dashes, no en dashes.** Project-wide. Use comma, middot, or period. Applies to all skill prompts, all reference files, all docs in this repo.
- **Light theme always.** Default to white background, gray text, color accents per the template's brand tokens. No dark mode in templates.
- **No emoji.** In skill prompts, in reference files, in template content. The icon library at `skills/deck-builder/references/icon-library.md` provides inline SVG alternatives.
- **Skill prompts read like a smart colleague**, not a form. Conversational tone in user-facing prompts, declarative tone in reference files.
- **Single-file output.** No external dependencies in generated decks. CSS and JS inline. Images either inline (SVG) or referenced as user-hosted URLs.

---

## Development setup

```bash
git clone https://github.com/FluidForm-ai/fluiddocs-deck-builder.git
cd fluiddocs-deck-builder

# Install the skills locally to test
cp -r skills/* ~/.claude/skills/

# Invoke via Claude Code
/deck-builder
```

For PPTX import, you'll also need:

```bash
pip install python-pptx
```

---

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) v2.1. Be kind, assume good faith, focus on the work. Harassment, discrimination, or personal attacks will not be tolerated. Report concerns to the maintainer email in the repo About.

A full `CODE_OF_CONDUCT.md` will be added to the repo. Until then, the Contributor Covenant text linked above is the operative policy.

---

## License

By contributing, you agree your contributions are licensed under MIT.

## Maintained by

[FluidDocs](https://fluiddocs.ai). Primary maintainer: [@nishant-aggarwal](https://github.com/nishant-aggarwal).
