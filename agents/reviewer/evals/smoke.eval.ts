import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Reviewer smoke without live GitHub/Jira: produce a review packet shape from
 * fixtures and hand back at pr_review without approving or merging.
 * Needs a Cursor credential to run.
 */
export default defineEval({
  tags: ["smoke", "reviewer"],
  description:
    "Drafts a PR review packet (matches/gaps/PR link) and hands back without merge.",
  async test(t) {
    await t.send(
      [
        "Ticket: ASF-42",
        "Stage: pr_review",
        "PR: https://github.com/example/product/pull/99",
        "Approved PRD acceptance criteria:",
        "- Toggle in settings switches light/dark theme for the session.",
        "Approved architecture:",
        "## Architecture",
        "### Summary",
        "Settings UI toggles theme store; theme provider applies CSS class.",
        "### Components",
        "| SettingsToggle | ThemeStore |",
        "PR diff summary (fixture): SettingsToggle calls ThemeStore.setTheme; session CSS class updates; unit test for toggle included. CI: unknown.",
        "Task: Stage is already pr_review. Review the PR against acceptance criteria and architecture. Post a review packet to Jira if available (matches, gaps, PR link). Do not change stage labels. Do not write product code. Do not approve. Do not merge.",
        "If Jira tools are unavailable, include the full review packet in your reply and note auth is required.",
      ].join(" "),
    );
    t.succeeded();
    t.check(
      t.reply,
      includes(/## PR review|### Matches|### Gaps|pr_review|Handoff/i),
    );
    t.check(t.reply, includes(/pull\/99|example\/product|PR:/i));
  },
});
