import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Cursor account GitHub connector for product-repo branch and PR writes.
 *
 * Authorize GitHub in the Cursor dashboard (or Deployed Agents connectors)
 * before live runs. Prefer these tools; skills may fall back to `gh` when
 * the connector is unavailable but the CLI is authenticated.
 * `optional: true` keeps validate green when the connector is missing.
 */
export default defineConnection({
  cursorAccount: true,
  servers: ["GitHub"],
  advertiseTools: true,
  optional: true,
  description:
    "GitHub via Cursor account connector (product repo branch + open PR).",
});
