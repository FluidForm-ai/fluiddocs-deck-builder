---
name: deploy
description: Deploy / publish a single HTML file (deck, page, doc) to FluidDocs hosting using the self-contained scripts/deploy.sh. Handles browser sign-in / re-auth automatically, then opens the live URL in the browser. Trigger on "deploy", "publish", "ship it", "push it live", "put it online", "host this", or any request to make an HTML file publicly viewable.
---

# Deploy

Publish a single HTML file to FluidDocs hosting. `scripts/deploy.sh` is **self-contained**. It handles auth, upload, and project-mapping on its own. Your job is to run it correctly and open the result. Do **not** re-implement, inspect, or second-guess the script. Just run it.

## What the script does (so you don't have to analyze it)

- Finds HTML files in the **current directory only** (`find . -maxdepth 1`). So you must run it from the folder that contains the target file.
- If exactly one HTML file is present, it auto-selects it. If several, it prompts for a number.
- Caches an auth token at `~/.config/fluiddocs/auth.json`. If the token is missing or expired, it prints a sign-in URL, **opens the browser**, and polls for up to 5 minutes while the user authorizes.
- Uploads the file and prints `  ✓ Deployed → <URL>` on success.
- Records the file→project mapping in `./.fluid-docs.json`, so re-deploying the same file **updates the existing project** instead of creating a duplicate. Keep this file; don't delete it.
- Flags: `--name "Friendly Title"` (project name), `--host URL` (alternate server), `--logout` (clear cached creds for a fresh sign-in).

## Procedure

1. **Pick the target file.** If the user names one, use it. Otherwise use the obvious HTML file in context (e.g. the deck you just built). If genuinely ambiguous, ask which file, one short question, then proceed.

2. **Always pass `--name "Friendly Title"`.** Without it the project name defaults to the raw filename slug, which is hard to scan in the dashboard. Derive a clean human title (e.g. `"Mushee · Seed Pitch"`).

3. **Run the script from the file's directory.** The script lives at `${CLAUDE_PLUGIN_ROOT}/scripts/deploy.sh` (or `scripts/deploy.sh` at the repo root). From the directory containing the HTML:

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/deploy.sh" --name "Friendly Title"
   ```

   Run it with network access enabled and a generous timeout (up to 600000 ms). The auth poll can take a few minutes while the user signs in. The script opens the user's browser itself when auth is needed; tell the user to complete the sign-in there.

4. **If the run can't do interactive sign-in** (sandboxed shell with no network, or the browser can't be driven), hand the command to the user to run in-session with the `!` prefix instead, so auth happens in their own browser:

   ```
   ! cd <deck-dir> && bash "<path>/scripts/deploy.sh" --name "Friendly Title"
   ```

5. **On success, open the live URL in the browser.** The script prints but does not open the deployed URL. You do. Capture the URL after `✓ Deployed →` and open it:

   ```bash
   open "<deployed-url>"        # macOS
   # xdg-open "<deployed-url>"  # Linux
   ```

   Then report the live URL to the user.

## Re-auth

If the user wants to switch accounts or the token is broken, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/deploy.sh" --logout` first, then deploy again to trigger a fresh sign-in.

## Hard rules

- Never deploy without `--name`.
- Run from the file's own directory (the script is directory-scoped).
- Preserve `./.fluid-docs.json`. It's what keeps re-deploys updating the same project.
- Deploying publishes the file to a public URL. The user asking to "deploy/publish" is the authorization; don't deploy a file they didn't ask for.

---

*Maintained by [FluidDocs](https://fluiddocs.ai). Source: https://github.com/FluidForm-ai/fluiddocs-deck-builder. MIT licensed.*
