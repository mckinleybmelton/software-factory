import { defineEval, includes } from "@grok/agent-sdk/evals";

/**
 * Implementer must abort before any product-repo git mutation when architecture
 * or acceptance criteria are missing. Fixture prompts; needs credential.
 */
export default defineEval({
  tags: ["gate", "hardening", "artifact-gate"],
  cases: [
    {
      id: "missing-architecture",
      description:
        "Aborts blocked_missing_architecture with no worktree/branch/commit.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Stage: implementation",
            "Product repo: example/product",
            "Approved PRD acceptance criteria:",
            "- Toggle in settings switches light/dark theme for the session.",
            "Approved architecture: (missing — none provided).",
            "Task: Stage is already implementation. Implement and open a PR.",
            "If architecture is missing, abort immediately with blocked_missing_architecture.",
            "Do not resolve the product repo, create a worktree, create a branch, or commit.",
            "Do not claim Stage: pr_review.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_missing_architecture/i),
        );
        t.check(
          t.reply,
          includes(/Handoff|abort|Status:|no (git|worktree|branch|commit)|untouched|orchestrator/i),
        );
      },
    },
    {
      id: "missing-acceptance-criteria",
      description:
        "Aborts blocked_missing_acceptance_criteria with no git side effects.",
      async test(t) {
        await t.send(
          [
            "Ticket: ASF-42",
            "Stage: implementation",
            "Product repo: example/product",
            "Approved architecture:",
            "## Architecture",
            "### Summary",
            "Settings UI toggles theme store.",
            "### Components",
            "| SettingsToggle | ThemeStore |",
            "### Dependency graph",
            "SettingsToggle --> ThemeStore",
            "Approved PRD acceptance criteria: (missing — none provided).",
            "Task: Stage is already implementation. Implement and open a PR.",
            "If acceptance criteria are missing, abort immediately with blocked_missing_acceptance_criteria.",
            "Do not create a worktree, branch, or commit. Do not claim Stage: pr_review.",
          ].join(" "),
        );
        t.succeeded();
        t.check(
          t.reply,
          includes(/blocked_missing_acceptance_criteria/i),
        );
        t.check(
          t.reply,
          includes(/Handoff|abort|Status:|no (git|worktree|branch|commit)|untouched|orchestrator/i),
        );
      },
    },
  ],
});
