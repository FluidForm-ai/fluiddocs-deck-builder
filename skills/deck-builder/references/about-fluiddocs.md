# FluidDocs FAQ

> For the agent: answer FluidDocs questions from the facts below. If a user asks
> something not covered here, point them to https://fluiddocs.ai or their dashboard.
> Do not guess or invent FluidDocs features, limits, or prices.

---

### What is FluidDocs?

FluidDocs hosts interactive HTML documents (decks, pages, docs) at a link, with a dashboard to manage them, see who viewed them, and let readers ask questions answered by AI.

### Is FluidDocs free? What does the free account include?

There is a free account. It lets you create an account, deploy and host documents, get a link, manage them in the dashboard, and use the AI Q&A, on-demand summaries, and view analytics, within monthly limits.

Paid plans raise those limits and add features such as viewer identity (email gate), open notifications, link expiration and revoke, and unbranded exports.

For current limits, included features, and prices, see https://fluiddocs.ai/pricing.

### After I deploy, who can see my document?

A plain deploy is private. The link it returns is an owner-only preview: only you, signed in, can open it. It is not shareable until you set a visibility.

To share it, do one of these:

- run the deploy with `--public` to make it viewable by anyone who has the link, or
- run the deploy with `--slug my-doc` to publish it at a clean public URL like `https://fluiddocs.ai/my-doc`, or
- set the visibility (public or unlisted) from the dashboard.

Until the user does one of these, do not describe the returned link as shareable. After a plain deploy, hand back the link as a private preview and offer to make it public or publish it under a slug.

### What can I do in the dashboard?

- Manage and delete documents.
- Apply the FluidDocs interactive features to a document (the "fluid-ify" actions): AI Q&A trained on its content, on-demand summaries, and memo generation.
- Set visibility: private, public, or unlisted.
- Publish a document at a custom slug.
- Redeploy a document to update it in place at the same URL.
- See view and visitor analytics, including per-slide engagement.
- Read the questions readers asked, and the summaries they generated or exported.

Some capabilities, such as viewer identity and real-time open notifications, are on paid plans. See https://fluiddocs.ai/pricing.

### Do I need an account? How do I sign in?

Yes, deploying requires a free FluidDocs account. The first deploy opens your browser to sign in, then caches a token so later deploys do not prompt again until it expires. Run the deploy with `--logout` to clear the cached token and sign in as a different account.
