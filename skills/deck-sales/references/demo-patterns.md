# Demo Patterns · Sales Deck (Optional)

Sales decks sometimes include a product walkthrough on Slide 6 (How It Works). In the OSS pack, that slide ships as a **static screenshot sequence**, not a working interactive demo. A small "Powered by FluidDocs" attribution mark (FluidDocs logo as inline SVG, ~20px tall, opacity ~0.7, linking to fluiddocs.ai) sits in the bottom-right of the slide. The patterns below describe what the screenshot sequence should depict for typical sales scenarios. No upsell appears in the deck output.

---

## When to include a screenshot sequence

Include a screenshot sequence on Slide 6 if:
- **The product is easy to understand in motion.** If the workflow is abstract or complex, a static diagram (Pattern C or D in `visual-components.md` for Slide 6) is often clearer than a screenshot sequence.
- **The prospect's pain point has a visual outcome.** (e.g., "transforms messy data into a clean report" is screenshot-worthy; "integrates with your system" is not)
- **You have current, presentable product screenshots.** Out-of-date or in-development screenshots erode credibility.
- **Time allows (8-min meeting minimum, ideally 10+).** A walkthrough in a 6-min pitch meeting feels rushed and backfires.

**Do NOT include a screenshot sequence if**:
- The prospect is in discovery mode and hasn't expressed pain yet.
- The product is complex and requires 5+ minutes of explanation.
- Your screenshots are stale or contain placeholder data. Update them first.

---

## Screenshot setup (universal)

1. **Sequence 3-5 screenshots maximum.** Each screenshot should show one distinct step of the workflow. More than 5 starts to feel like a manual.

2. **Anonymized data, never production.** Use synthetic data. Never show real customer names, PII, or company information.

3. **Caption each screenshot** with a one-line label below it (12-14pt):
   - "Upload step: your file goes here"
   - "Processing: automated in 30 seconds"
   - "Output: clean data ready to use"

4. **Number the sequence** (1, 2, 3, 4) with subtle overlays so the order is obvious without narration.

5. **Show outcome, not configuration.** Skip settings menus and admin panels. The buyer cares about what they get, not what they set up.

6. **Outcome callout on the final screenshot.** A small badge or annotation (e.g., "95% automatic match rate") on the last screenshot makes the value land.

---

## Pattern 1 · Linear workflow walkthrough

**When to use**: The product's core value is "a 5-step workflow that solves a pain point."

**Example products**: data pipelines, survey tools, reporting platforms, workflow automation.

**Screenshot sequence**:
1. Start screen (empty state or dashboard)
2. User input (upload file, fill form, connect data source)
3. Processing (show status, maybe a progress indicator)
4. Output (final report, dashboard, or decision)
5. Export or share action (show how they get the result)

**Key moments to capture**:
- The "before" state (their pain: messy data, manual effort)
- The input step (where they interact, should feel intuitive)
- The output (the outcome that solves their pain)
- A speed annotation: "This is your data cleaned up in 30 seconds. Normally this takes your team 2 hours"

**What NOT to show**:
- Settings or advanced features.
- Error cases (unless the error handling is the value).
- UI polish details. Focus on outcome.

**Recommended on-deck timing**: 30-60 seconds of presenter narration over 3-5 screenshots.

---

## Pattern 2 · Before/after comparison

**When to use**: The value is clearest when you show the customer's current pain (messy, manual, slow) vs. the new state (clean, automated, fast).

**Example products**: data cleaners, automation tools, consolidation platforms (merging disparate tools into one).

**Screenshot sequence**:
1. Their current state (their spreadsheet, multiple tools, manual process)
2. Your solution taking input from that state
3. The clean output
4. (Optional) How they'd use the output (share, build on it, etc.)

**Key moments to capture**:
- Empathy: "I see your team manages X across these 3 tools. Our platform brings it all here."
- Speed: "Normally this takes you 30 minutes every Friday. Here, it's automatic."
- Quality: "No more transcription errors or mismatched data."

**What NOT to show**:
- Mockery of their current process. Stay factual.
- Incomplete data from their tools (you're comparing apples/oranges).
- Oversold speed (if it takes 3 minutes, don't claim 30-second miracles).

**Recommended on-deck timing**: 30-60 seconds.

---

## Pattern 3 · Real-time data interaction

**When to use**: The product's value is in interactivity, filtering, slicing, exploring data dynamically.

**Example products**: BI tools, analytics platforms, search/discovery tools.

**Screenshot sequence**:
1. Dashboard or table with data
2. After 1-2 interactive actions (filter by segment, change date range, drill into a metric)
3. The updated view post-interaction
4. An insight that the interactivity revealed ("last quarter we had churn in the West region; this quarter it's East")

**Key moments to capture**:
- Speed of interaction: "This view updates in milliseconds. Your team can answer questions in real-time instead of waiting for reports."
- Exploration: "Notice how filtering by region instantly shows the relevant cohort. No pre-computed reports needed."
- Insight: "Now they see patterns they never saw when data was stuck in a spreadsheet."

**What NOT to show**:
- 10+ clicks worth of interaction in the screenshot sequence (viewers lose focus).
- Ambiguity about what changed (highlight the update visually with an annotation arrow).
- Lag or slow rendering. Pick a snappy state to capture.

**Recommended on-deck timing**: 30-60 seconds.

---

## Pattern 4 · Integration / system-to-system flow

**When to use**: The value is "your system talks to their system without human effort."

**Example products**: API tools, connectors, middleware, data sync platforms.

**Screenshot sequence**:
1. Source system (their data in System A)
2. Integration trigger (connect System A to your platform)
3. Target system (data appearing in System B)
4. Use case (their team uses the data in System B without manual re-entry)

**Key moments to capture**:
- Effort: "This sync would normally require a developer to write a script and maintain it. Here, you click 'connect' and it just works."
- Trust: "Your System A data appears in System B instantly. No data loss, no manual steps."
- Hands-off: "After setup, it's automatic. Your team doesn't touch it again."

**What NOT to show**:
- 30 minutes of API configuration (that's a technical audience, not a sales meeting).
- Mockery of their current manual process.
- Latency promises if your network is slow. Capture a known-good state.

**Recommended on-deck timing**: 30-60 seconds.

---

## Pattern 5 · Configurability / template-based customization

**When to use**: The value is "flexible enough for your unique workflow without custom engineering."

**Example products**: no-code tools, workflow builders, reporting platforms with custom templates.

**Screenshot sequence**:
1. A template or default configuration
2. One customization applied (change a column name, reorder fields, adjust a calculation)
3. The customization in effect
4. (Optional) A second configuration for a different use case (shows the flexibility without spending 10 minutes on it)

**Key moments to capture**:
- Control: "This is built for your specific workflow. We didn't hard-code anything."
- Speed: "Changes take effect instantly. No dev sprints, no waiting."
- Breadth: "One tool handles both use cases (sales reporting plus operations metrics) without two separate platforms."

**What NOT to show**:
- Advanced configuration options (keep it simple).
- The settings menu. Show the outcome of configuration (a report that looks like their format, not a form with 50 toggles).
- Overselling. If customization requires manual setup the first time, say so.

**Recommended on-deck timing**: 30-60 seconds.

---

## Fallback: minimal screenshot sequence

If you cannot put together 3-5 distinct screenshots, use the minimum viable sequence:

```
Screenshot 1: Starting state (empty or with sample data)
Screenshot 2: After step N (showing progress)
Screenshot 3: Final output (the value)
[Optional] Screenshot 4: Alternative outcome (flexibility)
```

Caption each one with a one-line label. The Layout Reviewer will flag the slide if it ships with only a single screenshot and no captions.

---

## Common pitfalls in sales-meeting screenshot walkthroughs

1. **Stale screenshots.** UI from 18 months ago undermines the product. Update before the meeting.
2. **Showing admin or setup mode.** Buyers care about the output, not the configuration interface. Skip the settings menu.
3. **Real customer data visible.** Prospects see customer names or metrics and lose focus. Use anonymized synthetic data only.
4. **No annotations.** A screenshot without a caption or callout asks the buyer to figure out what they're looking at. Always annotate.
5. **Too many screenshots.** 6+ steps starts to feel like a user manual. Pick the 3-5 most load-bearing moments.
6. **No outcome callout.** End the sequence with a visible badge or annotation that names the result ("95% automatic match", "$12K saved in week 1").
