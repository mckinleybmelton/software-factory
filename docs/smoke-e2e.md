# Live smoke E2E runbook

Run one real Jira ticket through every factory gate. Use this after local
`validate` is green and Atlassian + GitHub connectors work for the peers you
will exercise.

## Preconditions

1. Node 22.13+; from repo root: `npm install` (or per-agent installs).
2. Sign in: `npx --yes "@grok/agent-sdk@0.4.0" login` (or `CURSOR_API_KEY`).
3. Connect **Atlassian** (and **GitHub** before the implementer step) in the
   Cursor dashboard MCP connectors — or Deployed Agents connectors for hosted
   slugs. See [config-checklist.md](./config-checklist.md).
4. Set product-repo env for implementer (`FACTORY_PRODUCT_REPO` / `PRODUCT_REPO`).
5. Serve peers: `npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev`
6. Talk **only** to the orchestrator playground:
   `http://127.0.0.1:3000/orchestrator/playground`

Optional chat:

```bash
npx --yes "@grok/agent-sdk@0.4.0" chat \
  --url http://127.0.0.1:3000/orchestrator \
  --message "Route <KEY> (prd_draft): <one-line summary>."
```

## Ticket setup

1. Create (or pick) a small Jira ticket in the factory project.
2. Apply **exactly one** factory stage label: start at `prd_draft`.
3. Ensure no other factory stage labels are present:
   `prd_draft`, `prd_review`, `design_draft`, `design_review`,
   `architecture_draft`, `architecture_review`, `implementation`,
   `pr_review`, `done`.

Keep the ticket trivial (one clear acceptance criterion) so gates stay readable.

## Happy path (all gates)

At every `*_review` stage the orchestrator must **stop** for a human decision.
Do not invent approvals.

| Step | Stage before | Human / orchestrator prompt | Expected |
| --- | --- | --- | --- |
| 1 | `prd_draft` | Route ticket; draft PRD | Product posts PRD; label → `prd_review`; **stop** |
| 2 | `prd_review` | Approve PRD | Product applies `design_draft`; design drafts + posts; → `design_review`; **stop** |
| 3 | `design_review` | Approve design | Product applies `architecture_draft`; architect posts; → `architecture_review`; **stop** |
| 4 | `architecture_review` | Approve architecture | Product applies `implementation`; implementer opens **one** PR, comments link, → `pr_review`; reviewer posts packet; **stop** |
| 5 | `pr_review` | Approve PR (human merge outside factory if desired) | Product applies `done` |

### Prompt shapes (copy-paste)

**Start / continue draft work**

```text
Ticket <KEY> is in <stage>. Route it through the factory.
```

**Approve a review gate**

```text
Ticket <KEY> is in <review_stage>. I approve. Record the gate decision and continue.
```

**Reject a review gate**

```text
Ticket <KEY> is in <review_stage>. I reject: <notes>. Record the gate decision and continue.
```

### Verify after each specialist return

- Jira has **exactly one** factory stage label matching the expected next stage.
- Artifact (or PR link / review packet) is commented on the ticket when tools
  were authorized.
- Orchestrator reply names ticket, stage, peer asked, and what the human must
  do next — without self-approving.

## Reject path (optional spot-check)

On any review gate, reject with notes once. Expect return to the matching draft
(or `implementation` for PR reject), then re-ask that peer with notes after the
draft/implementation label is **verified**.

## Jira / auth recovery

Specialists may draft in-chat when MCP auth is missing. Stage labels that require
a live post must **not** advance until auth succeeds.

| Symptom | Status / handoff | Recovery |
| --- | --- | --- |
| Product drafted PRD; Jira post failed | Stage stays `prd_draft`; auth required | Authorize Atlassian for **product**; re-ask product to post + set `prd_review` |
| Design draft ready; Jira failed | `design_ready_jira_auth_required`; stage `design_draft` | Auth Atlassian for **design**; re-ask design to post → `design_review` |
| Architecture draft ready; Jira failed | `architecture_ready_jira_auth_required`; stage `architecture_draft` | Auth Atlassian for **architect**; re-ask architect to post → `architecture_review` |
| PR opened on GitHub; Jira comment/label failed | `implementation_ready_jira_auth_required`; stage stays `implementation`; handoff includes `PR: <url>` | Auth Atlassian for **implementer**; re-ask implementer **jira-complete only** (reuse PR; comment + set `pr_review`). **Never** ask product to set `pr_review` |
| No PR yet; GitHub auth missing | `implementation_ready_github_auth_required` / `implementation_ready_auth_required` | Auth GitHub (and Jira); re-ask implementer implement + open-PR |
| Reviewer packet ready; Jira failed | `pr_review_ready_jira_auth_required`; stage stays `pr_review` | Auth Atlassian for **reviewer**; re-ask reviewer to post packet (no label write) |

### Implementer jira-complete ask (after PR exists)

```text
Ticket: <KEY>
Stage: implementation
PR: <url>
Task: Stage is already implementation. PR already exists at <url>. Do not open a new PR. Do not re-implement. Comment the PR link on Jira and set label to pr_review only (jira-complete). Hand back. Do not approve. Do not merge.
```

## Race-safe checks (while smoking)

- After a gate approve, confirm the **draft/implementation** label landed before
  the next specialist is asked (verify-before-ask).
- Design alone writes `design_review`; architect alone `architecture_review`;
  implementer alone `pr_review` (after a real PR); reviewer never writes stage
  labels; product never writes those three review labels.
- Missing architecture or acceptance criteria: implementer must abort with
  `blocked_missing_*` and **no** worktree/branch/commit.

## Pass criteria

- One ticket traversed `prd_draft` → … → `done` (or deliberately stopped after
  demonstrating every gate stop + one recovery path).
- No invented approvals; every review gate waited for a human.
- At least one auth-recovery path exercised or documented as N/A with connectors
  already healthy.
- `npx --yes "@grok/agent-sdk@0.4.0" validate --dir ./agents` still green.

## Related

- [config-checklist.md](./config-checklist.md) — env + connectors
- [deploy-slugs.md](./deploy-slugs.md) — hosted peers + app-host wiring
- Root [README.md](../README.md) — serve, stages, skills
