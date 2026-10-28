import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Cursor account Atlassian connector for Jira read/comment/label.
 *
 * Authorize Atlassian in the Cursor dashboard (or Deployed Agents connectors)
 * before live runs. `optional: true` keeps validate and local bring-up green
 * when the connector is missing or the host is not yet signed in for tool use;
 * serve still needs a Cursor credential when this connection is present
 * (`agent-sdk login` or CURSOR_API_KEY). See the repo README.
 */
export default defineConnection({
  cursorAccount: true,
  servers: ["Atlassian"],
  advertiseTools: true,
  optional: true,
  description:
    "Atlassian/Jira via Cursor account connector (ticket read, comment, labels).",
});
