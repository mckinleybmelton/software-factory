---
description: Use when deciding the next factory action for a Jira ticket (stage, peer, and next step).
---

# Route a ticket

## Inputs

- Ticket key (e.g. `ASF-12`)
- Current factory stage label on the ticket (if unknown, ask the human or have **`product`** read Jira — **never** ask `design`, `architect`, `implementer`, or `reviewer` for stage lookup or generic label updates)
- Human intent: start, continue, approve, reject, status

## Stage → peer

| Stage label | Peer to ask | Action |
| --- | --- | --- |
| `prd_draft` | `product` | Ask product to draft PRD and post to Jira |
| `prd_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `design_draft` | `design` | Ask design to draft UX and post to Jira (**only** after stage is confirmed `design_draft`) |
| `design_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `architecture_draft` | `architect` | Ask architect to draft architecture and post to Jira (**only** after stage is confirmed `architecture_draft`) |
| `architecture_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `implementation` | `implementer` | Ask implementer to implement + open PR (**only** after stage is confirmed `implementation`) |
| `pr_review` | `reviewer` | Ask reviewer to post review packet (**only** after stage is confirmed `pr_review`) |
| `done` | _(none)_ | Report complete; no further routing |

## Jira ownership

| Need | Who |
| --- | --- |
| Stage lookup / label apply (including post-gate drafts, return-to-draft, `done`) | **`product`** or human |
| UX draft + post → `design_review` | **`design`** only, and only when stage is already `design_draft` |
| Architecture draft + post → `architecture_review` | **`architect`** only, and only when stage is already `architecture_draft` |
| Implement + open PR → comment PR link + `pr_review` | **`implementer`** only, and only when stage is already `implementation` (sets `pr_review` **after** PR exists) |
| PR review packet comment (no label write) | **`reviewer`** only, and only when stage is already `pr_review` |

Do **not** send generic Jira reads or label updates to `design`, `architect`, `implementer`, or `reviewer`. They are not catch-all Jira peers.

## Procedure

1. Resolve the ticket key and current stage label (human or **product** Jira read).
2. If stage is a `*_review` gate, do **not** ask a specialist to approve. For `prd_review` / `design_review` / `architecture_review`, summarize and wait for the human. For `pr_review`, ask **`reviewer`** only after stage is verified `pr_review`, then stop for the human merge decision after the packet is posted (or if reviewer already posted, wait for the human).
3. If stage is a draft/implementation stage, ask the matching peer with scoped context: ticket key, stage, relevant notes, rejection feedback if any.
4. Before asking `design`, confirm the ticket stage is already `design_draft`. If a gate decision just advanced labels, wait until product (or human) confirms the label landed — do not race a deferred `design_draft` write against design's `design_review` post.
5. Before asking `architect`, confirm the ticket stage is already `architecture_draft`. Same verify-before-ask rule as design — do not race a deferred `architecture_draft` write against architect's `architecture_review` post.
6. Before asking `implementer`, confirm the ticket stage is already `implementation`. Same verify-before-ask rule — do not race a deferred `implementation` write against implementer's `pr_review` post.
7. Before asking `reviewer`, confirm the ticket stage is already `pr_review` (which implies a PR should exist — implementer only sets that label after opening the PR). Do not ask reviewer from `implementation`.
8. After the peer returns, report status:
   - Product success (PRD post) → expect `prd_review` and **stop** for human review.
   - Design success → expect `design_review` and **stop** for human review.
   - Architect success → expect `architecture_review` and **stop** for human review.
   - Implementer success → expect `pr_review` and **stop** for human PR review (after asking reviewer when stage is verified, or ask reviewer next then stop).
   - Design **abort** / `blocked_*` → do **not** treat as `design_review`. Handle **only** by the specific status below (do not collapse them into one path):
     - `blocked_wrong_stage`: have **product** read the actual stage **now**. Route **only** from that live stage (human `*_review` → stop; draft/implementation → matching peer). Do **not** apply `design_draft` because an earlier turn once approved PRD/design — a stale authorize must not rewind `architecture_*` / later stages. Resume a pending label apply **only** inside the same in-progress `record-gate-decision` flow when the live stage is still that gate's "from" label (e.g. still `prd_review` after this approve, or still `design_review` after this reject); then verify before asking design.
     - `blocked_wrong_ask`: ask **product** (or human) for the Jira read/label work; **no** stage change; **do not** re-ask design.
     - `blocked_missing_prd`: **no** label rewrite. If live stage is `design_draft`, supply the approved PRD (or have product fetch it), verify stage is still `design_draft`, then re-ask design. If live stage is anything else, route from that stage instead of re-asking design.
   - Design `design_ready_jira_auth_required` → stage remains `design_draft`; do not open the human design gate until a real post sets `design_review`.
   - Architect **abort** / `blocked_*` → do **not** treat as `architecture_review`. Handle **only** by the specific status below:
     - `blocked_wrong_stage`: have **product** read the actual stage **now**. Route **only** from that live stage. Do **not** apply `architecture_draft` from a stale earlier approve — that must not rewind `implementation` / later stages. Resume a pending label apply **only** inside the same in-progress `record-gate-decision` flow when the live stage is still that gate's "from" label (e.g. still `design_review` after this approve, or still `architecture_review` after this reject); then verify before asking architect.
     - `blocked_wrong_ask`: ask **product** (or human) for the Jira read/label work; **no** stage change; **do not** re-ask architect.
     - `blocked_missing_prd` / `blocked_missing_design`: **no** label rewrite. If live stage is `architecture_draft`, supply the approved PRD and/or design (or have product fetch them), verify stage is still `architecture_draft`, then re-ask architect. If live stage is anything else, route from that stage instead of re-asking architect.
   - Architect `architecture_ready_jira_auth_required` → stage remains `architecture_draft`; do not open the human architecture gate until a real post sets `architecture_review`.
   - Implementer **abort** / `blocked_*` → do **not** treat as `pr_review`. Handle **only** by the specific status below:
     - `blocked_wrong_stage`: have **product** read the actual stage **now**. Route **only** from that live stage. Do **not** apply `implementation` from a stale earlier approve — that must not rewind `pr_review` / `done`. Resume a pending label apply **only** inside the same in-progress `record-gate-decision` flow when the live stage is still that gate's "from" label (e.g. still `architecture_review` after this approve, or still `pr_review` after this reject); then verify before asking implementer.
     - `blocked_wrong_ask`: ask **product** (or human) for the Jira read/label work; **no** stage change; **do not** re-ask implementer.
     - `blocked_missing_architecture` / `blocked_missing_acceptance_criteria` / `blocked_missing_product_repo`: **no** label rewrite. If live stage is `implementation`, supply the missing inputs (or have product fetch artifacts / confirm repo config), verify stage is still `implementation`, then re-ask implementer. If live stage is anything else, route from that stage instead of re-asking implementer.
   - Implementer `implementation_ready_*_auth_required` → stage remains `implementation`; do not open the human PR gate / ask reviewer until a real PR exists and `pr_review` is set.
   - Reviewer **abort** / `blocked_*` → do **not** treat as human approval. Handle by status:
     - `blocked_wrong_stage`: product reads live stage; route from that stage only.
     - `blocked_wrong_ask`: ask product/human for Jira work; do not re-ask reviewer for that work.
     - `blocked_missing_pr` / `blocked_missing_architecture` / `blocked_missing_acceptance_criteria`: if live stage is `pr_review`, supply the missing PR/artifacts, verify stage, re-ask reviewer; else route from live stage.
   - Reviewer `pr_review_ready_jira_auth_required` → stage remains `pr_review`; human gate can still proceed once the packet is available in-chat, but prefer a real Jira post when auth returns.
9. On reject (via `record-gate-decision`), product/human returns stage to the draft/implementation label; **verify** that label, then re-ask that peer with the rejection notes. Never race a deferred draft-label write against a specialist post.

## Peer ask shapes

When asking `product` to **apply a stage label** (after a gate decision), include at least:

```text
Ticket: <KEY>
Task: Apply factory stage labels only — remove <old_stage> (and any other factory stage labels), add <new_stage>. Confirm the resulting stage label. Do not draft a PRD, design, or architecture.
```

When asking `product` to **read stage**, include at least:

```text
Ticket: <KEY>
Task: Read the ticket and report the current factory stage label only.
```

When asking `product` for a PRD draft, include at least:

```text
Ticket: <KEY>
Stage: prd_draft
Task: Draft the PRD (problem, users, scope, out of scope, acceptance criteria, open questions), post it to Jira, set label to prd_review, and hand back. Do not approve.
```

When asking `design`, include at least:

```text
Ticket: <KEY>
Stage: design_draft
Task: Stage is already design_draft. Read the approved PRD only. Draft design (user flows, screens/interfaces), post it to Jira, set label to design_review, and hand back. Do not approve. Do not apply design_draft.
```

Include the approved PRD body (or a pointer to the Jira PRD comment) and any prior `design_review` rejection notes.

When asking `architect`, include at least:

```text
Ticket: <KEY>
Stage: architecture_draft
Task: Stage is already architecture_draft. Read the approved PRD and design. Draft architecture (components, boundaries, dependency graph), post it to Jira, set label to architecture_review, and hand back. Do not approve. Do not apply architecture_draft.
```

Include the approved PRD and design bodies (or pointers to the Jira comments) and any prior `architecture_review` rejection notes.

When asking `implementer`, include at least:

```text
Ticket: <KEY>
Stage: implementation
Task: Stage is already implementation. Read the approved architecture and acceptance criteria. Implement in the configured product repo (worktree isolation), open one PR, comment the PR link on Jira, set label to pr_review only after the PR exists, and hand back. Do not approve. Do not merge. Do not apply implementation.
```

Include the approved architecture, acceptance criteria, product-repo config if known, and any prior `pr_review` rejection notes.

When asking `reviewer`, include at least:

```text
Ticket: <KEY>
Stage: pr_review
Task: Stage is already pr_review. Read the PR diff and CI if available, plus approved PRD and architecture. Post a review packet on the ticket (matches, gaps, PR link). Do not change stage labels. Do not write product code. Do not approve. Do not merge.
```

Include the PR URL, approved PRD/architecture pointers, and any human notes.
