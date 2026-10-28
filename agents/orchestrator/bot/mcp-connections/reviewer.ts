import { defineConnection } from "@grok/agent-sdk/connections";

export default defineConnection({
  agent: "reviewer",
  description: "Reviewer peer (stub this slice): PR review against acceptance criteria.",
});
