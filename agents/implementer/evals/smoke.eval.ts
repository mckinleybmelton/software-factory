import { defineEval, includes } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke", "stub"],
  description: "Stub implementer peer reports not implemented.",
  async test(t) {
    await t.send("Please implement ASF-1 and open a PR.");
    t.succeeded();
    t.check(t.reply, includes(/not implemented/i));
  },
});
