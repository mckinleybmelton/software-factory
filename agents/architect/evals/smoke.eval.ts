import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Architect smoke without live Jira: draft architecture (components, boundaries,
 * dependency graph) from approved PRD + design fixtures and hand back at
 * architecture_review. Needs a Cursor credential to run.
 */
export default defineEval({
  tags: ["smoke", "architect"],
  description:
    "Drafts architecture (components + dependency graph) and hands back at architecture_review without self-approval.",
  async test(t) {
    await t.send(
      [
        "Ticket: ASF-42",
        "Stage: architecture_draft",
        "Approved PRD:",
        "## PRD",
        "### Problem",
        "Users struggle to use the app at night.",
        "### Users",
        "End users who prefer dark UI.",
        "### Scope",
        "Add a dark-mode toggle to settings.",
        "### Out of scope",
        "System-wide theme sync across devices.",
        "### Acceptance criteria",
        "- Toggle in settings switches light/dark theme for the session.",
        "### Open questions",
        "- None.",
        "Approved design:",
        "## Design",
        "### Summary",
        "Settings page gains a dark-mode toggle that applies theme for the session.",
        "### User flows",
        "1. Open settings → toggle dark mode → theme updates.",
        "### Screens / interfaces",
        "| Screen | Purpose | Key elements |",
        "| Settings | Change theme | Dark mode toggle |",
        "### Open questions",
        "- None.",
        "Task: Stage is already architecture_draft. Read the approved PRD and design. Draft architecture (components, boundaries, dependency graph), post to Jira if available, set label to architecture_review, and hand back. Do not apply architecture_draft.",
        "If Jira tools are unavailable, include the full architecture in your reply and note auth is required.",
        "Do not approve.",
      ].join(" "),
    );
    t.succeeded();
    t.check(
      t.reply,
      includes(/## Architecture|### Components|dependency|architecture_review|Handoff/i),
    );
    t.check(t.reply, includes(/mermaid|flowchart|-->|depends/i));
  },
});
