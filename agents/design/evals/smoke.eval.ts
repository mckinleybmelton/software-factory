import { defineEval, includes } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke", "stub"],
  description: "Stub design peer reports not implemented.",
  async test(t) {
    await t.send("Please produce the design artifact for ASF-1.");
    t.succeeded();
    t.check(t.reply, includes(/not implemented/i));
  },
});
