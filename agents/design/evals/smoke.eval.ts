import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Design smoke without live Jira: draft UX artifacts from an approved PRD
 * fixture and hand back at design_review. Needs a Cursor credential to run.
 */
export default defineEval({
  tags: ["smoke", "design"],
  description:
    "Drafts design (flows + screens) and hands back at design_review without self-approval.",
  async test(t) {
    await t.send(
      [
        "Ticket: ASF-42",
        "Stage: design_draft",
        "Approved PRD:",
        "## PRD",
        "### Problem",
        "Users struggle to use the app at night.",
        "### Users",
        "End users who prefer dark UI.",
        "### Scope",
        "Add a dark-mode toggle to settings.",
        "### Out of scope",
        "System-wide theme sync across devices.",
        "### Acceptance criteria",
        "- Toggle in settings switches light/dark theme for the session.",
        "### Open questions",
        "- None.",
        "Task: Draft the design (user flows, screens/interfaces), post to Jira if available, set label to design_review, and hand back.",
        "If Jira tools are unavailable, include the full design in your reply and note auth is required.",
        "Do not approve.",
      ].join(" "),
    );
    t.succeeded();
    t.check(t.reply, includes(/## Design|### User flows|design_review|Handoff/i));
    t.check(t.reply, includes(/screens?|interfaces?/i));
  },
});
