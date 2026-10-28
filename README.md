# software-factory

Cursor talks to an **orchestrator** Agent SDK peer. The orchestrator routes Jira tickets through specialist peers. Specialists own their skills and MCP tools. Jira is the source of truth; humans approve at review gates.

```text
agents/                 # runtime: six peer agents (unchanged)
packages/
  core/                 # @software-factory/core — stage labels + handoff
  product-skills/       # @software-factory/product-skills — PRD + backlog
plugins/software-factory/  # Cursor plugin adapter (cursorPlugin mount)
examples/app-host/      # thin consumer host + install docs
```

Requires **Node 22.13+** (never Bun). Packaging adds install surfaces; it does **not** replace the six peers with one mega-agent.

## Install paths

### GitHub clone (serve the peer network)

```bash
git clone https://github.com/mckinleybmelton/software-factory.git
cd software-factory
npm install
# or per-agent: for d in agents/*/; do (cd "$d" && npm install); done

# Preferred: sign in so model turns and Atlassian/GitHub MCP work
npx --yes "@grok/agent-sdk@0.4.0" login
# or: export CURSOR_API_KEY=...

npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev
# Playground index: http://127.0.0.1:3000/
# Orchestrator:     http://127.0.0.1:3000/orchestrator/playground

# Local bring-up without a Cursor credential (validate stays green either way).
npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev \
  --allow-anonymous --allow-anonymous-cursor-account-mcp
```

Talk to the **orchestrator** only. Examples:

> Ticket ASF-12 is in `prd_draft`. Route it through the factory.

The orchestrator asks the `product` peer, then stops at **`prd_review`** for a human gate.

```bash
npx --yes "@grok/agent-sdk@0.4.0" chat \
  --url http://127.0.0.1:3000/orchestrator \
  --message "Route ASF-12 (prd_draft): add dark mode to settings."
```

### Extension mount

Install packages (workspace / `file:` today; npm publish later) and add mounts:

```ts
// bot/extensions/factory.ts
import factory from "@software-factory/core";
export default factory();
```

```ts
// bot/extensions/productSkills.ts  (product-shaped agents)
import productSkills from "@software-factory/product-skills";
export default productSkills();
// skills: productSkills__draft-prd, productSkills__post-prd-to-jira,
//         productSkills__manage-backlog
```

See `examples/app-host/` for a full thin host.

### Cursor plugin

Copy or submodule `plugins/software-factory`, then:

```ts
// bot/extensions/softwareFactory.ts
import { cursorPlugin } from "@grok/agent-sdk/extensions";
export default cursorPlugin({ path: "plugins/software-factory" });
```

Plugin contributes skills/commands/agent stubs. Full peer network still runs via `serve` or hosted deploy slugs.

### Deploy slugs (hosted)

```bash
agent-sdk deploy --dir ./agents/orchestrator --slug orchestrator
agent-sdk deploy --dir ./agents/product --slug product
agent-sdk deploy --dir ./agents/design --slug design
agent-sdk deploy --dir ./agents/architect --slug architect
agent-sdk deploy --dir ./agents/implementer --slug implementer
agent-sdk deploy --dir ./agents/reviewer --slug reviewer
```

Peer connections use the lowercase deploy slug: `defineConnection({ agent: "orchestrator" })`. Details: [`examples/app-host/README.md`](examples/app-host/README.md).

## Validate

```bash
npx --yes "@grok/agent-sdk@0.4.0" validate --dir ./agents
npx --yes "@grok/agent-sdk@0.4.0" validate --dir ./examples/app-host
# or: npm run validate
```

Validate does not need a Cursor API key. Model turns (`run` / `eval` / chat) do.

## Stage labels (Jira)

Exactly one factory stage label on the ticket:

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

- Submit: draft → matching review (implementer sets `pr_review` only after a PR exists)
- Approve: review → next draft / `implementation` / `done`
- Reject / changes_requested: review → same draft (or `implementation` for PR reject) with notes

Shared reference: `packages/core` (`factory__factory-stages`).

## Jira / Atlassian / GitHub auth

Product, design, and architect use `defineConnection({ cursorAccount: true, servers: ["Atlassian"], optional: true })`.

Implementer and reviewer add GitHub (`servers: ["GitHub"]`) plus Atlassian for ticket comments. Implementer alone writes `pr_review` after the PR exists; reviewer posts the review packet and does not change stage labels.

1. Connect **Atlassian** and **GitHub** in the Cursor dashboard (MCP connectors).
2. Sign the serve host in (`agent-sdk login` or `CURSOR_API_KEY`).
3. For hosted deploys, connect those servers under Deployed Agents connectors.
4. Set product-repo config for the implementer: `FACTORY_PRODUCT_REPO` / `PRODUCT_REPO` (`owner/name`), optional `FACTORY_PRODUCT_REPO_PATH`, optional `FACTORY_PRODUCT_DEFAULT_BRANCH` (default `main`).

Without connector auth, specialists still draft artifacts in the reply and report that a live post needs OAuth. `optional: true` keeps **validate** green when a connector is missing. A normal `serve` with these connections needs a Cursor credential; for unsigned local playground use `--allow-anonymous --allow-anonymous-cursor-account-mcp` (trusted networks only).

### Product skills

Mounted from `@software-factory/product-skills` (namespace `productSkills`):

| Skill | Role |
| --- | --- |
| `productSkills__draft-prd` | Fill the PRD contract for a ticket |
| `productSkills__post-prd-to-jira` | Comment PRD + set stage label `prd_review` |
| `productSkills__manage-backlog` | Board triage (buckets, next steps); moves only when asked |

Backlog scope defaults: `JIRA_PROJECT_KEY` / `FACTORY_JIRA_PROJECT` (optional `JIRA_FILTER_ID` / `JIRA_BOARD_ID`). Status → bucket map and stale days: see `packages/product-skills/skills/manage-backlog/references/status-buckets.md` (`FACTORY_BACKLOG_STATUS_MAP`, `FACTORY_BACKLOG_STALE_DAYS`).

### Design skills

| Skill | Role |
| --- | --- |
| `draft-design` | User flows + screens/interfaces from the approved PRD |
| `post-design-to-jira` | Comment design + set stage label `design_review` |

### Architect skills

| Skill | Role |
| --- | --- |
| `draft-architecture` | Components, boundaries, dependency graph from approved PRD + design |
| `post-architecture-to-jira` | Comment architecture + set stage label `architecture_review` |

### Implementer skills

| Skill | Role |
| --- | --- |
| `implement-change` | Code + tests in the configured product repo (worktree isolation) |
| `open-pr` | Open one PR (GitHub MCP or `gh`), comment PR link on Jira, set `pr_review` only after the PR exists; reuse existing PR for jira-complete recovery |

Implementer never approves or merges. Prefer GitHub MCP; fall back to `gh` when needed.

### Reviewer skills

| Skill | Role |
| --- | --- |
| `review-pr` | Read PR diff/CI vs approved PRD + architecture |
| `post-review-packet` | Comment matches / gaps / PR link on Jira (no label write) |

Reviewer never writes product code and never merges. Human still approves at the PR gate.

## Race-safe routing (verify-before-ask)

Product (or human) applies draft/implementation/`done` labels after a gate decision. Orchestrator **verifies** the stage before asking the specialist. Specialists alone write their review labels (`design_review`, `architecture_review`, `pr_review`) after the artifact (or PR) exists. Generic Jira stage reads/label applies stay with **product**.

## Evals

```bash
npx --yes "@grok/agent-sdk@0.4.0" eval --dir ./agents/orchestrator --list
npx --yes "@grok/agent-sdk@0.4.0" eval --dir ./agents/orchestrator
```

Orchestrator smoke asserts routing intent toward product / stop at PRD review (fixture ticket text; no live Jira). Design / architect / implementer / reviewer smokes assert artifact handoffs without self-approval. Needs a Cursor credential. Skip running evals if unsigned; scaffolding remains under each agent's `evals/`.

## Layout notes

- Peers: `bot/mcp-connections/*.ts` with `defineConnection({ agent: "<slug>" })`
- Skills: `bot/skills/*/SKILL.md` or mounted extensions under `bot/extensions/`
- Packages: `packages/*` via `defineExtension`; plugin via `cursorPlugin`
- Runtime package: `@grok/agent-sdk` — Node, not Bun
- Knowledge layers (thin `AGENTS.md` / instructions → on-demand skills → `references/` → MCP): see Project doc [`docs/knowledge-layer.md`](/cursor/stores/self/docs/knowledge-layer.md).
