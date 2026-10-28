import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Cursor account Atlassian connector for posting the PR review packet.
 *
 * Reviewer comments only — does not change factory stage labels.
 * `optional: true` keeps validate green when the connector is missing.
 */
export default defineConnection({
  cursorAccount: true,
  servers: ["Atlassian"],
  advertiseTools: true,
  optional: true,
  description:
    "Atlassian/Jira via Cursor account connector (post PR review packet comment).",
});
