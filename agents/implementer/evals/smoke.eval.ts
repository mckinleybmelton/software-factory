import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Implementer smoke without live GitHub/Jira: acknowledge implementation stage,
 * architecture + AC, and hand back without self-approval / merge.
 * Needs a Cursor credential to run.
 */
export default defineEval({
  tags: ["smoke", "implementer"],
  description:
    "Plans implementation from architecture + AC and hands toward pr_review without merging.",
  async test(t) {
    await t.send(
      [
        "Ticket: ASF-42",
        "Stage: implementation",
        "Product repo: example/product (config fixture; do not invent another).",
        "Approved PRD acceptance criteria:",
        "- Toggle in settings switches light/dark theme for the session.",
        "Approved architecture:",
        "## Architecture",
        "### Summary",
        "Settings UI toggles theme store; theme provider applies CSS class.",
        "### Components",
        "| Component | Responsibility |",
        "| SettingsToggle | UI control |",
        "| ThemeStore | Session theme state |",
        "### Boundaries",
        "- UI may not persist theme server-side in this ticket.",
        "### Dependency graph",
        "SettingsToggle --> ThemeStore",
        "Task: Stage is already implementation. Implement against the architecture and acceptance criteria, open one PR in the product repo if GitHub is available, comment the PR link on Jira, set label to pr_review only after the PR exists, and hand back. Do not apply implementation. Do not merge. Do not approve.",
        "If GitHub or Jira tools are unavailable, include the implementation plan (branch, changes, tests) in your reply and note auth is required. Never claim Stage: pr_review without a real PR.",
      ].join(" "),
    );
    t.succeeded();
    t.check(
      t.reply,
      includes(/implementation|pr_review|Handoff|branch|PR|test/i),
    );
    t.check(t.reply, includes(/do not merge|not merge|never merge|awaiting human|auth required|pr_review/i));
  },
});
