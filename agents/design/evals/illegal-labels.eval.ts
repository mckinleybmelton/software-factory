import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Design must refuse generic label applies and draft-label writes; only
 * design_review via post after a real draft. Fixture prompts; needs credential.
 */
export default defineEval({
  tags: ["gate", "hardening", "illegal-labels"],
  cases: [
    {
      id: "refuse-design-draft-apply",
      description: "Refuses apply-design_draft / generic label asks.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Task: Apply factory stage labels only — remove prd_review, add design_draft.",
            "Confirm the resulting stage. Do not draft UX.",
            "If this is product's job, refuse with blocked_wrong_ask and hand back to orchestrator.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_wrong_ask|refuse|product|orchestrator|not a generic|wrong ask/i),
        );
        t.check(
          t.reply,
          includes(/Handoff|Stage:|Status:/i),
        );
      },
    },
    {
      id: "refuse-wrong-stage-review-claim",
      description: "Wrong stage ask does not claim design_review.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Stage: prd_draft",
            "Task: Draft design and set design_review.",
            "If stage is wrong, abort blocked_wrong_stage and do not claim Stage: design_review.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_wrong_stage|wrong stage|prd_draft|abort/i),
        );
      },
    },
  ],
});
