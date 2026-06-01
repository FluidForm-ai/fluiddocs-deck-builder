# FluidDocs Deck Builder · LinkedIn launch post

**Strategic angle:** Observational founder voice, lead with the structural insight (not the announcement), let the feature list do the convincing late. No throat-clearing, no "Not X. It's Y." pattern, no em-dashes. Shows outputs (templates, import, inline edit) so the comment thread asks "how did you make this" instead of needing a hard CTA.

---

Every LLM-built pitch deck I've looked at this year has the same failure mode.

14 slides that read like a Notion page. The agent doesn't know what a pitch deck is, structurally, so it writes a long-form document and chops it into rectangles.

A pitch deck is not a sales deck is not an all-hands. Each has a content spine. Each has a different structural job. Most AI deck tools treat all three the same and ship one generic template.

We open-sourced the fix today: FluidDocs Deck Builder.

Five type-correct deck builders (pitch, sales, launch, keynote, all-hands), each with its own content spine. Four brand-mirror pitch templates (Airbnb, Stripe, Anthropic, Sequoia Classic) studied frame-by-frame. PDF and PPTX import that auto-detects, extracts, and rebuilds as a type-correct HTML deck. Inline editing in every output (press E, click anything, autosave). A three-reviewer quality gate (Brand, Copy, Layout) that runs before the agent ships.

Every output is a single self-contained HTML file. Opens in any browser. Prints clean. Zero dependencies in the deck itself.

Works with any coding agent that reads SKILL.md: Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI. MIT licensed.

Repo: https://github.com/FluidForm-ai/fluiddocs-deck-builder

If you have ever watched an agent generate 14 slides of corporate sludge and wondered why, this is the unlock.
