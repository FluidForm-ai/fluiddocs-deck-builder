# FluidDocs Deck Builder · X launch thread

**Strategic angle:** Hook on the universal pain (LLMs write decks that read like Notion pages), then show outputs. Each tweet under 280 chars. Repo URL lands on the last tweet. No em-dashes, no en-dashes.

---

**Tweet 1 (hook)**

every LLM-built pitch deck has the same tell.

14 slides that read like a Notion page. no structure. no spine. no idea what a pitch deck actually is.

we open-sourced the fix today.

---

**Tweet 2**

a pitch deck is not a sales deck is not an all-hands.

each has a content spine. each has a different structural job.

most AI deck tools ship one generic template and hope.

FluidDocs Deck Builder ships five type-correct builders.

---

**Tweet 3**

· deck-pitch · 14 slides
· deck-sales · 11 slides
· deck-launch · 12 slides
· deck-keynote · 20 to 35 slides
· deck-all-hands · 15 slides

drop one in front of your coding agent. it knows what the deck is supposed to be.

---

**Tweet 4**

every deck output is a single self-contained HTML file.

1440 by 810 canvas, scale-to-fit, chrome-free, renders like a PDF in the browser.

no build step. no dependencies in the deck itself. opens in any browser. prints clean.

---

**Tweet 5**

we shipped four brand-mirror templates for pitch:

· Airbnb
· Stripe
· Anthropic
· Sequoia Classic

each one studied frame-by-frame. typography, palette, slide rhythm. use as-is or fork.

---

**Tweet 6**

inline editing built in.

press E or hover the top-left hotzone. click any element. edit in place. autosaves to localStorage. Ctrl+S downloads the new HTML.

every deck ships with this for free. no editor app required.

---

**Tweet 7**

drop a PDF or PPTX in. get back an interactive HTML deck.

the import path auto-detects, extracts text, screenshots, layout. rebuilds it as a type-correct HTML deck you can edit inline.

most painful step in the deck workflow, gone.

---

**Tweet 8**

three-reviewer quality gate runs before output:

· Brand · is the visual language consistent
· Copy · is every line load-bearing
· Layout · does anything overflow the canvas

the agent doesn't ship until all three pass.

---

**Tweet 9**

works with any coding agent that reads SKILL.md.

Claude Code, Codex, Kimi Code, OpenCode, Gemini CLI. clone the repo, point your agent at it, invoke deck-builder.

MIT licensed. PRs welcome. translation PRs especially.

---

**Tweet 10**

if you have ever asked an LLM for a pitch deck and got back 14 slides of corporate sludge, this is the unlock.

https://github.com/FluidForm-ai/fluiddocs-deck-builder
