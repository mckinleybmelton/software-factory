import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Cursor account Atlassian connector for Jira comment + stage label.
 *
 * Used after a PR exists: comment the PR link, then set `pr_review`.
 * `optional: true` keeps validate and local bring-up green when the
 * connector is missing. See the repo README.
 */
export default defineConnection({
  cursorAccount: true,
  servers: ["Atlassian"],
  advertiseTools: true,
  optional: true,
  description:
    "Atlassian/Jira via Cursor account connector (PR-link comment, pr_review label).",
});
