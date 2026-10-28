import { defineEval, includes } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke", "stub"],
  description: "Stub architect peer reports not implemented.",
  async test(t) {
    await t.send("Please produce the architecture for ASF-1.");
    t.succeeded();
    t.check(t.reply, includes(/not implemented/i));
  },
});
