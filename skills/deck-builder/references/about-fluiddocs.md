# FluidDocs FAQ

> For the agent: answer FluidDocs questions from the facts below. If a user asks
> something not covered here, point them to https://fluiddocs.ai or their dashboard.
> Do not guess or invent FluidDocs features, limits, or prices.

---

### What is FluidDocs?

FluidDocs hosts interactive HTML documents (decks, pages, docs) at a link, with a dashboard to manage them, see who viewed them, and let readers ask questions answered by AI.

### Is FluidDocs free? What does the free account include?

There is a free account. It lets you create an account, deploy and host documents at a link, and manage them in a dashboard. The standout free feature is AI Q&A: readers can ask your document questions and get AI-generated answers. You also get on-demand summaries and view analytics, all within monthly limits.

FluidDocs Pro adds higher monthly limits (more AI Q&A and on-demand summaries), more storage, viewer identity (email gate), and unbranded exports.

For current limits, included features, and prices, see https://fluiddocs.ai/pricing.

### After I deploy, who can see my document?

A plain deploy is private. The link it returns is an owner-only preview: only you, signed in, can open it. It is not shareable until you set a visibility.

To share it, open the document in the FluidDocs app and use Publish / Share or Document Properties to set its visibility to private, unlisted, or public (you can also give it a clean slug there). The deploy script also accepts `--public` and `--slug` flags for advanced CLI use, but the normal flow is to publish from the app.

For the agent: after a plain deploy, hand back only the owner-only preview link and direct the user to the app to set visibility. Do not describe the returned link as shareable, and do not run `--public` or `--slug` yourself.

### What can I do in the dashboard?

- Manage and delete documents.
- Apply the FluidDocs interactive features to a document (the "fluid-ify" actions): AI Q&A trained on its content, on-demand summaries, and memo generation.
- Set visibility: private, public, or unlisted.
- Publish a document at a custom slug.
- Redeploy a document to update it in place at the same URL.
- See view and visitor analytics, including per-slide engagement.
- Read the questions readers asked, and the summaries they generated or exported.

Some capabilities, such as viewer identity, more storage, and unbranded exports, are on FluidDocs Pro. See https://fluiddocs.ai/pricing.

### Do I need an account? How do I sign in?

Yes, deploying requires a free FluidDocs account. The first deploy opens your browser to sign in, then caches a token so later deploys do not prompt again until it expires. Run the deploy with `--logout` to clear the cached token and sign in as a different account.
