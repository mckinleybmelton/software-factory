import { defineConnection } from "@grok/agent-sdk/connections";

/**
 * Peer orchestrator. Locally: mount slug from `serve --dir ./agents`.
 * Hosted: lowercase deploy slug (default `orchestrator`).
 *
 * Override with `FACTORY_ORCHESTRATOR_SLUG` when your deploy slug differs.
 */
export default defineConnection({
  agent: process.env.FACTORY_ORCHESTRATOR_SLUG ?? "orchestrator",
  description:
    "Factory orchestrator: routes Jira tickets through specialist peers.",
});
