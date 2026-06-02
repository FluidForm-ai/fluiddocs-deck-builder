# FluidDocs Deck Builder

**Drop in your old PDF or PPTX. Get back a polished, interactive HTML deck.**

An open-source deck builder for coding agents. Five type-correct deck spines, four brand-mirror pitch templates, PDF and PPTX import, inline editing, and a multi-reviewer quality pipeline. Single-file HTML output. Zero dependencies in the deck itself.

Maintained by [FluidDocs](https://fluiddocs.ai). MIT licensed.

---

## Try it in 30 seconds, no install

Open [`quick-start.html`](./quick-start.html) in your browser. A live Stripe pitch deck loads in an embedded preview. Press `E` inside the deck to enter edit mode. Edit any heading. Press `Ctrl`/`Cmd`+`S` to download your version.

That is the whole loop. No signup, no CLI, no server. The HTML file you download is yours to ship, host, or fork.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 180" width="800" height="180" role="img" aria-label="Four-step visitor journey: Try, Browse, Install, Generate">
  <style>
    .stepbg { fill: #FFF7ED; stroke: #FED7AA; stroke-width: 1.5; }
    .stepbg-muted { fill: #FAFAF9; stroke: #E5E7EB; stroke-width: 1; }
    .num { font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 12px; fill: #F97316; letter-spacing: 0.08em; }
    .num-muted { font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 12px; fill: #94A3B8; letter-spacing: 0.08em; }
    .verb { font-family: 'Inter', system-ui, sans-serif; font-weight: 700; font-size: 17px; fill: #0F172A; }
    .desc { font-family: 'Inter', system-ui, sans-serif; font-weight: 400; font-size: 11px; fill: #6B7280; }
    .arrow { fill: none; stroke: #FB923C; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
    .icon-active { fill: none; stroke: #F97316; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .icon-muted { fill: none; stroke: #94A3B8; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  </style>

  <!-- Step 1: Try (active) -->
  <g transform="translate(8, 20)">
    <rect class="stepbg" x="0" y="0" width="180" height="140" rx="12"/>
    <g transform="translate(20, 18)">
      <rect class="icon-active" x="0" y="0" width="32" height="24" rx="3"/>
      <line class="icon-active" x1="0" y1="7" x2="32" y2="7"/>
      <circle cx="4" cy="3.5" r="0.8" fill="#F97316"/>
      <circle cx="7" cy="3.5" r="0.8" fill="#F97316"/>
      <circle cx="10" cy="3.5" r="0.8" fill="#F97316"/>
    </g>
    <text class="num" x="20" y="74">STEP 01</text>
    <text class="verb" x="20" y="96">Try</text>
    <text class="desc" x="20" y="116">Open quick-start.html</text>
    <text class="desc" x="20" y="130">in your browser</text>
  </g>

  <!-- Arrow 1 to 2 -->
  <path class="arrow" d="M 195 90 L 218 90"/>
  <path class="arrow" d="M 213 86 L 218 90 L 213 94"/>

  <!-- Step 2: Browse (active) -->
  <g transform="translate(225, 20)">
    <rect class="stepbg" x="0" y="0" width="180" height="140" rx="12"/>
    <g transform="translate(20, 18)">
      <rect class="icon-active" x="0" y="0" width="12" height="12" rx="2"/>
      <rect class="icon-active" x="18" y="0" width="12" height="12" rx="2"/>
      <rect class="icon-active" x="0" y="18" width="12" height="12" rx="2"/>
      <rect class="icon-active" x="18" y="18" width="12" height="12" rx="2"/>
    </g>
    <text class="num" x="20" y="74">STEP 02</text>
    <text class="verb" x="20" y="96">Browse</text>
    <text class="desc" x="20" y="116">Pick a template</text>
    <text class="desc" x="20" y="130">or style preset</text>
  </g>

  <!-- Arrow 2 to 3 -->
  <path class="arrow" d="M 412 90 L 435 90"/>
  <path class="arrow" d="M 430 86 L 435 90 L 430 94"/>

  <!-- Step 3: Install (muted) -->
  <g transform="translate(442, 20)">
    <rect class="stepbg-muted" x="0" y="0" width="180" height="140" rx="12"/>
    <g transform="translate(20, 18)">
      <rect class="icon-muted" x="0" y="0" width="32" height="24" rx="3"/>
      <polyline class="icon-muted" points="6,10 10,14 6,18"/>
      <line class="icon-muted" x1="14" y1="18" x2="22" y2="18"/>
    </g>
    <text class="num-muted" x="20" y="74">STEP 03</text>
    <text class="verb" x="20" y="96">Install</text>
    <text class="desc" x="20" y="116">Add the plugin</text>
    <text class="desc" x="20" y="130">to Claude Code</text>
  </g>

  <!-- Arrow 3 to 4 -->
  <path class="arrow" d="M 629 90 L 652 90" stroke="#CBD5E1"/>
  <path class="arrow" d="M 647 86 L 652 90 L 647 94" stroke="#CBD5E1"/>

  <!-- Step 4: Generate (muted) -->
  <g transform="translate(659, 20)">
    <rect class="stepbg-muted" x="0" y="0" width="133" height="140" rx="12"/>
    <g transform="translate(20, 18)">
      <path class="icon-muted" d="M 16 0 L 19 11 L 30 14 L 19 17 L 16 28 L 13 17 L 2 14 L 13 11 Z"/>
    </g>
    <text class="num-muted" x="20" y="74">STEP 04</text>
    <text class="verb" x="20" y="96">Generate</text>
    <text class="desc" x="20" y="116">/deck-builder</text>
    <text class="desc" x="20" y="130">in Claude Code</text>
  </g>
</svg>
```

---

## Browse templates

Eight templates ready to fork. Four brand-mirror pitch decks (Airbnb, Stripe, Anthropic, Sequoia Classic) and four type defaults (sales, launch, keynote, all-hands).

Open [`templates/index.html`](./templates/index.html) for the full gallery with filters by type.

Six style presets cover the case where you do not have a brand to mirror. Open [`style-presets/index.html`](./style-presets/index.html) to pick one.

---

## Install for real

### One-line install (Claude Code)

```bash
/plugin marketplace add FluidForm-ai/fluiddocs-deck-builder
/plugin install fluiddocs-deck-builder@fluiddocs-deck-builder
```

Then invoke any skill:

```
/fluiddocs-deck-builder:deck-builder
/fluiddocs-deck-builder:deck-pitch
/fluiddocs-deck-builder:deck-import
```

### Manual install (any agent that reads SKILL.md)

Works with Codex, Kimi Code, OpenCode, Gemini CLI, and any other agent that follows the SKILL.md convention.

Claude Code reads personal skills from `~/.claude/skills/<name>/`, so copy the skill folders directly into that directory:

```bash
git clone https://github.com/FluidForm-ai/fluiddocs-deck-builder.git /tmp/fluiddocs-deck-builder
cp -r /tmp/fluiddocs-deck-builder/skills/* ~/.claude/skills/
```

For other agents, clone the repo and point your agent at its `skills/` directory per that tool's own SKILL.md convention.

---

## Generate a new deck from scratch

After install, invoke the deck-builder skill and describe what you want. With the plugin install the command is `/fluiddocs-deck-builder:deck-builder`. With the manual install it is `/deck-builder`.

Sample prompts that work out of the box:

```
Build me a 14-slide seed pitch for Switchboard, an observability layer
for LLM workloads. Use the tech-crisp preset.
```

```
Build a 12-slide launch deck for the v2 release of our analytics product.
Studio Bold preset. Hero, what's new, availability, CTA.
```

```
Import this PDF and rebuild it as an interactive HTML deck with the
original screenshots preserved.
```

The skill walks the brief through intake, builds, runs three reviewers (Brand, Copy, Layout), and ships a single self-contained HTML file.

---

## What's in the pack

Five type-correct deck builders, each with the right slide count and content spine for the job:

| Skill | Slides | Use for |
|---|---|---|
| **deck-pitch** | 14 | Investor pitches. Ships with 4 brand-mirror templates (Airbnb, Stripe, Anthropic, Sequoia Classic). |
| **deck-sales** | 11 | B2B pitch-to-close. Pain, demo, proof, pricing, next steps. |
| **deck-launch** | 12 | Product announcements. Hero, what's new, availability, CTA. |
| **deck-keynote** | 28 | Conference talks. Narrative arc, one idea per slide, mandatory opening hook. |
| **deck-all-hands** | 15 | Town halls. Wins, candor, financials, Q&A placeholder. |

Plus two utilities:

- **deck-import** · point it at a PDF or PPTX, get back a clean interactive HTML deck.
- **deck-critique-lite** · 5 to 7 plain-language observations on a pitch deck. No numerical scoring.

Every generated deck is a single self-contained HTML file. Renders on a fixed 1440 by 810 canvas (PDF-like, chrome-free, scale-to-fit). Edits inline by pressing `E` or hovering the top-left hotzone. Autosaves to localStorage. Press Ctrl/Cmd+S to download.

---

## Why this exists

Three things most LLM-built decks get wrong, and what this pack does about them.

### 1. Type-correct deck spines

A pitch is not a sales deck is not an all-hands. Each has a different audience, different success criteria, different slide order. Most agents write 14 slides that read like a Notion page. This pack ships a content spine per deck type, audited against decks that actually shipped and closed rounds.

### 2. PDF and PPTX import

Most slide tools assume you're starting from a blank canvas. Real users have a deck. They want it cleaned up, made interactive, ported to the web, not rebuilt from scratch. `deck-import` auto-detects the input format, extracts the structure, classifies the slide types, and rebuilds in HTML with your original screenshots preserved.

### 3. Multi-reviewer quality pipeline

Three reviewers (Brand, Copy, Layout) sign off on every deck before release. When the underlying agent supports subagents, each reviewer runs in parallel. When it doesn't, they run sequentially. Either way, you get a deck that's been read by three different lenses before you see it.

---

## Demo GIFs

> TODO. Recording in progress. Placeholders below mark where each GIF will live.

- `docs/gifs/pitch-airbnb.gif` · build the Airbnb-template pitch deck end to end (Phase 1 intake, 3-preview style pick, full build, inline edit).
- `docs/gifs/pdf-import.gif` · drop a PDF, watch it become an interactive HTML deck with screenshots preserved.
- `docs/gifs/pptx-import.gif` · same flow for a PPTX, with the editable text path intact.
- `docs/gifs/inline-edit.gif` · `E` key toggles edit mode, click any text, type, Ctrl+S to save.

---

## Upgrade to FluidDocs hosted

The OSS pack gives you the builder, the templates, and the inline editor. [FluidDocs](https://fluiddocs.ai) is the hosted upgrade: it takes the same HTML output and adds analytics, reader Q&A, live updates without resending a link, reader-adaptive content, and a working interactive product demo slot inside pitch and launch decks (the OSS pack uses static screenshots in that slot). If you want to ship a deck that compounds over time instead of going stale the day you send it, that's the upgrade.

---

## Contributing

PRs welcome. Issues welcome. Translation PRs especially welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the guidelines.

---

## License

MIT. Use it, fork it, ship it.
