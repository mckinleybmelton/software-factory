import { defineConnection } from "@grok/agent-sdk/connections";

export default defineConnection({
  agent: "product",
  description: "Product peer: drafts PRDs and posts them to Jira.",
});
