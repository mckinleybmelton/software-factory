import { defineConnection } from "@grok/agent-sdk/connections";

export default defineConnection({
  agent: "design",
  description:
    "Design peer: UX flows and screens/interfaces after PRD approval; posts to Jira at design_review.",
});
