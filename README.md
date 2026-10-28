# software-factory

Cursor talks to an **orchestrator** Agent SDK peer. The orchestrator routes Jira tickets through specialist peers. Specialists own their skills and MCP tools. Jira is the source of truth; humans approve at review gates.

```text
agents/
  orchestrator/   # entry peer (real)
  product/        # PRD draft + Jira post + backlog triage (real)
  design/         # stub
  architect/      # stub
  implementer/    # stub
  reviewer/       # stub
```

Requires **Node 22.13+** (never Bun).

## Serve the network

```bash
# Install each agent once (or after lockfile changes)
for d in agents/*/; do (cd "$d" && npm install); done

# Preferred: sign in so model turns and Atlassian MCP work
npx --yes "@grok/agent-sdk@0.4.0" login
# or: export CURSOR_API_KEY=...

npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev
# Playground index: http://127.0.0.1:3000/
# Orchestrator:     http://127.0.0.1:3000/orchestrator/playground

# Local bring-up without a Cursor credential (validate stays green either way).
# Product's Atlassian connection is optional; Jira tools stay unavailable until you sign in.
npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev \
  --allow-anonymous --allow-anonymous-cursor-account-mcp
```


Talk to the **orchestrator** only. Example:

> Ticket ASF-12 is in `prd_draft`. Route it through the factory.

The orchestrator asks the `product` peer, then stops at **`prd_review`** for a human gate.

```bash
npx --yes "@grok/agent-sdk@0.4.0" chat \
  --url http://127.0.0.1:3000/orchestrator \
  --message "Route ASF-12 (prd_draft): add dark mode to settings."
```

## Validate

```bash
npx --yes "@grok/agent-sdk@0.4.0" validate --dir ./agents
# or: npm run validate
```

Validate does not need a Cursor API key. Model turns (`run` / `eval` / chat) do.

## Stage labels (Jira)

Exactly one factory stage label on the ticket:

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

- Submit: draft → matching review  
- Approve: review → next draft (or `done`)  
- Reject: review → same draft (with notes)

## Jira / Atlassian auth

Product uses `defineConnection({ cursorAccount: true, servers: ["Atlassian"], optional: true })` in `agents/product/bot/mcp-connections/account.ts`.

1. Connect **Atlassian** in the Cursor dashboard (MCP connectors).
2. Sign the serve host in (`agent-sdk login` or `CURSOR_API_KEY`).
3. For hosted deploys, connect Atlassian under Deployed Agents connectors.

Without Atlassian auth, product still drafts the PRD in its reply and reports that a live Jira post needs OAuth. `optional: true` keeps **validate** green when the connector is missing. A normal `serve` with this connection needs a Cursor credential; for unsigned local playground use `--allow-anonymous --allow-anonymous-cursor-account-mcp` (trusted networks only).

### Product skills

| Skill | Role |
| --- | --- |
| `draft-prd` | Fill the PRD contract for a ticket |
| `post-prd-to-jira` | Comment PRD + set stage label `prd_review` |
| `manage-backlog` | Board triage (buckets, next steps); moves only when asked |

Backlog scope defaults: `JIRA_PROJECT_KEY` / `FACTORY_JIRA_PROJECT` (optional `JIRA_FILTER_ID` / `JIRA_BOARD_ID`). Status → bucket map and stale days: see `agents/product/bot/skills/manage-backlog/references/status-buckets.md` (`FACTORY_BACKLOG_STATUS_MAP`, `FACTORY_BACKLOG_STALE_DAYS`).

## What is stubbed

| Peer | This slice |
| --- | --- |
| design | Replies `not implemented` |
| architect | Replies `not implemented` |
| implementer | Replies `not implemented` (no GitHub MCP yet) |
| reviewer | Replies `not implemented` |

Orchestrator still has peer connections to every specialist so routing stays testable.

## Evals

```bash
npx --yes "@grok/agent-sdk@0.4.0" eval --dir ./agents/orchestrator --list
npx --yes "@grok/agent-sdk@0.4.0" eval --dir ./agents/orchestrator
```

Orchestrator smoke asserts routing intent toward product / stop at PRD review (fixture ticket text; no live Jira). Needs a Cursor credential. Skip running evals if unsigned; scaffolding remains under each agent's `evals/`.

## Layout notes

- Peers: `bot/mcp-connections/*.ts` with `defineConnection({ agent: "<slug>" })`
- Skills: `bot/skills/*/SKILL.md` (and flat `.md` where enough)
- Package: `@grok/agent-sdk` — Node, not Bun
