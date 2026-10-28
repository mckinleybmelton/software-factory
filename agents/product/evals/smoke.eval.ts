import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Product smoke without live Jira: draft a PRD from fixture context and hand
 * back at prd_review. Needs a Cursor credential to run the model turn.
 */
export default defineEval({
  tags: ["smoke", "prd"],
  description: "Drafts a PRD and hands back at prd_review without self-approval.",
  async test(t) {
    await t.send(
      [
        "Ticket: ASF-42",
        "Stage: prd_draft",
        "Task: Draft the PRD for adding a dark-mode toggle to settings.",
        "Users: end users who prefer dark UI.",
        "If Jira tools are unavailable, include the full PRD in your reply and note auth is required.",
        "Hand back at prd_review. Do not approve.",
      ].join(" "),
    );
    t.succeeded();
    t.check(t.reply, includes(/## PRD|### Problem|prd_review|Handoff/i));
    t.check(t.reply, includes(/acceptance criteria|Acceptance criteria/i));
  },
});
