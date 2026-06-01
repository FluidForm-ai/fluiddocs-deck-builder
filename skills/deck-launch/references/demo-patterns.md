# Demo Patterns, Static Product Screenshots for Launch Decks

Slide 5 is the Demo slot. In OSS, it ships as a high-quality static product screenshot with a small **"Powered by FluidDocs" attribution mark** (the FluidDocs logo as inline SVG, opacity ~0.7, linking to fluiddocs.ai) in the bottom-right corner. This file covers composition recipes for the screenshot by product category.

Launch screenshots differ from generic product shots in one key way. They must communicate the core action in the first second. A launch slide is a 45-second narrative beat, not a brochure. The screenshot is the proof point.

Premium discovery (working interactive demos, hosting) is surfaced in the Phase 4 Release message, not in the deck output. The user's launch deck should not carry marketing copy for our hosted service.

---

## Attribution mark (every Slide 5)

Drop the FluidDocs attribution mark in the bottom-right of Slide 5 in every launch deck OSS builds. Use the standard inline-SVG snippet:

```html
<a href="https://fluiddocs.ai" target="_blank" rel="noopener" style="display:inline-block;opacity:.7;text-decoration:none">
  <svg viewBox="0 0 260 38" height="20" role="img" aria-label="Powered by FluidDocs" style="display:inline-block;vertical-align:middle">
    <path d="M0 2 Q0 0 2 0 L16 0 Q17.5 0 17.5 1.5 Q17.5 3 16 3 L5 3 L5 12 L14 12 Q15.5 12 15.5 13.5 Q15.5 15 14 15 L5 15 L5 26 Q5 28 2.5 28 Q0 28 0 26 Z" fill="#9CA3AF"/>
    <path d="M22 2 Q22 0 24.5 0 Q27 0 27 2 L27 24.5 L38 24.5 Q39.5 24.5 39.5 26 Q39.5 28 38 28 L24.5 28 Q22 28 22 25.5 Z" fill="#9CA3AF"/>
    <path d="M44 2 Q44 0 46.5 0 Q49 0 49 2 L49 22 Q49 33 56.5 33 Q64 33 64 22 L64 2 Q64 0 66.5 0 Q69 0 69 2 L69 22.5 Q69 38 56.5 38 Q44 38 44 22.5 Z" fill="#9CA3AF"/>
    <path d="M75 2 Q75 0 77.5 0 Q80 0 80 2 L80 26 Q80 28 77.5 28 Q75 28 75 26 Z" fill="#9CA3AF"/>
    <path d="M86 2 Q86 0 88 0 L97 0 Q108 0 108 14 Q108 28 97 28 L88 28 Q86 28 86 26 Z M91 3.5 L91 24.5 L96.5 24.5 Q103 24.5 103 14 Q103 3.5 96.5 3.5 Z" fill="#9CA3AF"/>
    <rect x="118" y="0" width="3" height="28" rx="1.5" fill="#F97316"/>
    <text x="132" y="22" font-family="Inter, -apple-system, BlinkMacSystemFont, sans-serif" font-weight="500" font-size="22" letter-spacing="2" fill="#9CA3AF">docs</text>
  </svg>
</a>
```

It is the canonical OSS pattern for this slot. Reviewers check that it is present.

---

## General rules

1. **One complete, obvious view.** A first-time viewer should understand what the product does in 10 seconds of looking.
2. **Real data, real names.** No "Lorem ipsum." Use realistic product names, users, and results that someone would actually see in production.
3. **Brand-native chrome.** The screenshot shows the product's real UI, in its real branding. No mockups, no Figma frames pretending to be screenshots.
4. **No fake metrics.** If numbers appear (growth, savings, adoption), they should be realistic defaults an early-stage product would actually show.
5. **High resolution.** Capture at 2x retina minimum. Compress for file size but keep type crisp.
6. **Fits one slide.** Composition fits inside the 1400x788 content area comfortably with the footnote below.
7. **No emojis in the surrounding labels.** Use SVG icons from `deck-builder/references/icon-library.md` for any callout glyphs.

---

## 1. Marketplace / Two-Sided Products (Rental, Labor, Services)

**Composition**: A results view with input context above. The browse step is the most legible single-frame story.

**Example: Accommodation rental marketplace**
- Top bar: Search context (Location, Check-in date, Check-out date, Guests), with a couple of active filter pills (Price range, Amenities)
- Main: Results grid, 4 to 6 listing cards with image, title, price/night, rating, favorite affordance
- Optional secondary frame: Detail modal mocked beside the grid (photo carousel, amenities, price breakdown, Reserve button)

**Watch for**: Show the grid populated with real-looking listings (real cities, real photos, plausible prices). Empty states or "no results" are not screenshot material.

---

## 2. Creator / Content Tools (Design, Writing, Video)

**Composition**: Editor with a live preview visible. The "input plus output" framing is what readers expect from a creator tool.

**Example: Social media post builder**
- Left panel: Template picker (3 categories visible: Instagram, Twitter, LinkedIn)
- Central canvas: A finished-looking Instagram post (1080x1350px), real headline and image
- Right panel: Quick-edit controls (headline text, color picker, font dropdown)
- Bottom: Download/Share affordances visible

**Example: AI writing assistant**
- Left: Prompt area with a real, complete prompt typed in
- Right: A finished response (5 to 10 lines of plausible output text), with Copy and Regenerate buttons visible
- Optional: Two-column mode with prompt left and output right

---

## 3. Business Productivity / Workflow Tools

**Composition**: A dashboard or board view with real-looking entries. Pick the screen that shows the most product surface area in one frame.

**Example: Project management tool**
- Sidebar: Project list (3 projects visible with realistic names)
- Main: Kanban board (To Do, In Progress, Done columns) with 6 to 8 task cards across columns
- Each card has a real-looking title, assignee avatar, and due date
- Optional inset: Task detail card visible to the right

**Example: Data analytics dashboard**
- Top row: KPI cards (Signups 1,234, Revenue $45K, Churn 2.1%) with realistic deltas
- Middle: Line chart (weekly signups) with realistic curve
- Bottom: Table of recent entries (name, email, signup date)
- Top-right: Filter dropdown visible (region, plan, date range)

---

## 4. Infrastructure / Developer Tools

**Composition**: Config plus result, side by side. The "I configured X and got Y" reading is what developers expect.

**Example: API or CLI tool**
- Left panel: Code/config editor with real JSON or YAML, syntax highlighted
- Right panel: Live response or output, color-coded status (success/error/warning), realistic payload
- Optional: A Copy response affordance visible in the response area

**Example: Database migration tool**
- Top: Source selector (PostgreSQL) and Destination selector (MongoDB) shown
- Middle: Schema mapping preview (source tables to destination collections)
- Bottom: Result card "Migrated 2.3M rows in 42 seconds" or progress bar mid-migration

---

## 5. Consumer AI / Chat Products

**Composition**: A conversation in progress, with both user and assistant messages visible. The reader needs to see one full exchange to understand the product.

**Example: AI chatbot or assistant**
- Chat window with 2 to 3 messages of history visible
- Most recent. A real-looking user question and a complete assistant response (5 to 10 lines of plausible text)
- Input box at the bottom with a follow-up question typed but not yet sent
- Optional: Suggested follow-up prompts visible below the response

**Example: Code generation / documentation tool**
- Left or top: A real prompt ("Generate a React component for a pricing table")
- Right or below: A code block of plausible generated output, syntax highlighted
- Copy code affordance visible on the code block

---

## 6. E-commerce / Fulfillment

**Composition**: The product detail or cart view tells the story best. Browse and checkout are too generic.

**Example: Product discovery and pre-order**
- Hero product detail view (photo, title, price, Pre-order button as primary action)
- Optional secondary frame: Cart with 2 items visible and a subtotal
- Optional: Confirmation card overlay ("Order #12345 confirmed, ships March 15")

---

## 7. Collaboration / Communication

**Composition**: A populated channel or thread, not an empty inbox.

**Example: Team messaging or async collaboration**
- Sidebar: Channel/thread list with 4 to 6 real-looking entries
- Main: Conversation thread with 3 to 4 messages from different people, real avatars and names
- Input box at the bottom with a draft message typed
- Optional: Notification bell with unread count badge

**Example: Feedback / survey tool**
- Survey preview with 3 to 5 questions visible
- One question partially answered (rating slider mid-drag, or one multiple-choice option selected)
- Submit affordance visible at the bottom

---

## 8. Analytics / Reporting

**Composition**: A dashboard with multiple chart types visible. Pick the screen that shows the most variety of viz in one frame.

**Example: Simple metrics dashboard**
- Top row: 3 to 4 KPI cards (current value, trend arrow, sparkline)
- Middle: Line chart (daily signups) and bar chart (revenue by product)
- Bottom: Small data table (top 5 items by metric)
- Top-right: Date range picker visible (e.g., "Last 30 days" selected)

---

## 9. Healthcare / Wellness

**Composition**: A personalized result or recommendation, not the input form.

**Example: Fitness or nutrition tool**
- Left or top: User context (Weight, height, activity level, summarized)
- Right or main: Personalized output (BMI, daily calorie target, 3 to 5 tips)
- Optional: Progress chart (current vs. goal) visible

**Example: Appointment or telemedicine booking**
- Provider card (name, specialty, available slots badge) as the hero
- Date/time picker showing real slots
- Booking summary panel with provider name, date, and time

---

## 10. Other / Custom Products

For any product not fitting the above:

1. **Identify the core action**: What does this product let someone do in 30 seconds?
   - Book a thing? Show the picked-result state, not the search box.
   - Create a thing? Show a finished-looking artifact in the editor.
   - Analyze a thing? Show the dashboard/results view, not the upload screen.
   - Send/connect with people? Show a populated conversation or contact list.

2. **Capture that screen end-to-end**: The screenshot should show the product mid-use, not pre-use.

3. **Add minimal callouts only if essential**: Nav header, sidebar, filters. Only what makes the action legible.

4. **Keep it to one or two stitched screens max** so it fits one slide without scrolling.

---

## Launch screenshot implementation checklist

- [ ] **Real data.** No "Lorem ipsum," "Sample," "Test," or placeholder names anywhere in the frame.
- [ ] **One complete view.** A first-time viewer can read the product's purpose from the screenshot alone.
- [ ] **Brand-native chrome.** The screenshot is from the actual product, not a Figma mock.
- [ ] **High resolution.** 2x retina capture, crisp type when scaled to the slide.
- [ ] **No emojis in callouts.** All glyphs via SVG icons from `deck-builder/references/icon-library.md`.
- [ ] **No fake metrics.** Numbers are realistic defaults the product would actually show.
- [ ] **Composition fits.** Screenshot plus caption plus attribution mark all fit inside 1400x788 without crowding.
- [ ] **Accessibility basics.** Alt text on the screenshot image. Captions readable at 16pt minimum.
- [ ] **Attribution present.** The FluidDocs logo (inline SVG, ~20px, opacity ~0.7, linking to fluiddocs.ai) appears in the bottom-right of the slide.

---

## Reference: Composition gold standard

The single-hero-screenshot composition is the default for the OSS launch demo slot. A populated marketplace grid, a chat with one complete exchange, or a dashboard with real numbers each work. Pick the screen that tells the whole product story in one frame, capture at 2x, and add the FluidDocs attribution mark in the bottom-right. If the screenshot needs more than one inset to be legible, the screen choice is probably wrong, pick a simpler view.
