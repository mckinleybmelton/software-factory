import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Routing intent smoke: orchestrator should delegate PRD draft work to the
 * product peer and stop at the human PRD review gate.
 *
 * Needs a Cursor credential (`CURSOR_API_KEY` or `agent-sdk login`). Skip live
 * Jira — this case uses a fixture ticket description in the prompt only.
 */
export default defineEval({
  tags: ["smoke", "routing"],
  description:
    "Routes a new ticket to product and stops at prd_review without approving.",
  async test(t) {
    await t.send(
      [
        "Factory ticket ASF-42 is in prd_draft.",
        "Summary: Add a dark-mode toggle to the settings page.",
        "Route this ticket. Ask the product peer to draft the PRD.",
        "Do not approve the PRD yourself. Stop when the work reaches prd_review.",
        "If product or Jira tools are unavailable, still state that you would ask product and stop at prd_review.",
      ].join(" "),
    );
    t.succeeded();
    // Soft: peer tool names are connection-scoped; narration is enough without live peers.
    t.check(
      t.reply,
      includes(/product|prd_review|PRD review|human/i),
    );
  },
});
