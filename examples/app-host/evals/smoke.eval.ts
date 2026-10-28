import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * App-host smoke: acknowledges factory routing via orchestrator without
 * inventing a gate approval. Needs a Cursor credential for the model turn.
 */
export default defineEval({
  tags: ["smoke", "app-host"],
  description: "Defers factory work to the orchestrator peer.",
  async test(t) {
    await t.send(
      [
        "Ticket ASF-12 is in prd_draft.",
        "Explain how you would start the factory run.",
        "Do not draft a PRD yourself. Do not approve.",
      ].join(" "),
    );
    t.succeeded();
    t.check(t.reply, includes(/orchestrator|prd_draft|handoff|peer/i));
  },
});
