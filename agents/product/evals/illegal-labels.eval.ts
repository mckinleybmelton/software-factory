import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Product must refuse specialist-owned review labels (design_review,
 * architecture_review, pr_review), including post-PR Jira recovery.
 * Fixture prompts only — no live Jira. Needs a Cursor credential to run.
 */
export default defineEval({
  tags: ["gate", "hardening", "illegal-labels"],
  cases: [
    {
      id: "refuse-design-review",
      description: "Refuses to apply design_review (design owns that label).",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Task: Apply factory stage labels only — remove design_draft, add design_review.",
            "Confirm the resulting stage label. Do not draft a PRD.",
            "If you are not allowed to write design_review, refuse and hand back to the orchestrator naming the correct peer (design).",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/refuse|cannot|not allowed|design owns|ask design|orchestrator|blocked/i),
        );
        t.check(t.reply, includes(/design_review|design/i));
      },
    },
    {
      id: "refuse-architecture-review",
      description:
        "Refuses to apply architecture_review (architect owns that label).",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Task: Apply factory stage labels only — remove architecture_draft, add architecture_review.",
            "If you are not allowed to write architecture_review, refuse and hand back naming architect.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/refuse|cannot|not allowed|architect owns|ask architect|orchestrator|blocked/i),
        );
        t.check(t.reply, includes(/architecture_review|architect/i));
      },
    },
    {
      id: "refuse-pr-review-recovery",
      description:
        "Refuses to set pr_review even when a PR URL exists (implementer jira-complete only).",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Stage: implementation",
            "PR: https://github.com/example/product/pull/99",
            "Jira auth just returned. Apply labels only — remove implementation, add pr_review, and comment the PR link.",
            "If you must not write pr_review, refuse and tell the orchestrator to ask implementer for jira-complete recovery.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/refuse|cannot|not allowed|implementer|jira-complete|orchestrator|blocked/i),
        );
        t.check(t.reply, includes(/pr_review/i));
      },
    },
  ],
});
