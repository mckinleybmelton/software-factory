import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Architect must refuse generic label applies; only architecture_review via
 * post after a real draft. Fixture prompts; needs credential.
 */
export default defineEval({
  tags: ["gate", "hardening", "illegal-labels"],
  cases: [
    {
      id: "refuse-architecture-draft-apply",
      description: "Refuses apply-architecture_draft / generic label asks.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Task: Apply factory stage labels only — remove design_review, add architecture_draft.",
            "Confirm the resulting stage. Do not draft architecture.",
            "If this is product's job, refuse with blocked_wrong_ask and hand back to orchestrator.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_wrong_ask|refuse|product|orchestrator|not a generic|wrong ask/i),
        );
        t.check(t.reply, includes(/Handoff|Stage:|Status:/i));
      },
    },
    {
      id: "refuse-wrong-stage-review-claim",
      description: "Wrong stage ask does not claim architecture_review.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Stage: design_draft",
            "Task: Draft architecture and set architecture_review.",
            "If stage is wrong, abort blocked_wrong_stage and do not claim Stage: architecture_review.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_wrong_stage|wrong stage|design_draft|abort/i),
        );
      },
    },
  ],
});
