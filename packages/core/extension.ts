import { defineExtension } from "@grok/agent-sdk/extensions";

/**
 * Shared factory conventions: stage labels, handoff shape, and reference
 * templates. Mount under `bot/extensions/` (e.g. `factory.ts`).
 */
export default defineExtension({
  root: import.meta.dirname,
  description:
    "Software factory stage labels, handoff conventions, and shared references.",
});
