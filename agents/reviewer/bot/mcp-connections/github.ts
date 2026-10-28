import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Cursor account GitHub connector for read-only PR/CI inspection.
 *
 * Reviewer must not push product code or merge. Prefer these tools; skills
 * may fall back to `gh` for read when MCP is unavailable.
 * `optional: true` keeps validate green when the connector is missing.
 */
export default defineConnection({
  cursorAccount: true,
  servers: ["GitHub"],
  advertiseTools: true,
  optional: true,
  description:
    "GitHub via Cursor account connector (read PR diff and checks).",
});
