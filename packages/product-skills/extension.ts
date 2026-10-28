import { defineExtension } from "@grok/agent-sdk/extensions";

/**
 * Product skills + references (PRD, backlog). Mount from `agents/product`
 * as `bot/extensions/productSkills.ts` so skills appear as
 * `productSkills__draft-prd`, `productSkills__post-prd-to-jira`, and
 * `productSkills__manage-backlog`.
 */
export default defineExtension({
  root: import.meta.dirname,
  description: "Product skills: draft PRD, post to Jira, manage backlog.",
});
