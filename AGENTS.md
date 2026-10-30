# software-factory

Factory conventions only. Skills load on demand — never paste skill bodies into `bot/instructions.md`.

## Peer slugs

| Slug | Owns |
| --- | --- |
| `orchestrator` | Routing and gate recording only |
| `product` | PRDs, backlog, stage lookups / label applies |
| `design` | UX draft; sole writer of `design_review` |
| `architect` | Architecture draft; sole writer of `architecture_review` |
| `implementer` | Code + one PR; sole writer of `pr_review` (after PR exists) |
| `reviewer` | PR review packet comment only (no label writes) |

Specialists return to the orchestrator; they do not call each other.

Runtime stays these six peers under `agents/`. Shareable packages live in `packages/` (`defineExtension`); Cursor adapter in `plugins/software-factory`; consumer template in `examples/app-host/`.

## Stage labels

Exactly one factory stage label on the ticket:

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

## Knowledge layers

Workspace `AGENTS.md` → agent `bot/instructions.md` → skills → `references/` → external MCP. Details: Project doc `docs/knowledge-layer.md`.

## Cursor Cloud specific instructions

Use Node.js 22.13 or newer. Do not use Bun.

- Install from the repo root with `./scripts/install-env.sh` (`npm ci` for `packages/*`, `agents/*`, and `examples/*`).
- Boot the peer network with `./scripts/setup-env.sh`.
- `npm run validate` checks every peer and `examples/app-host`. `npm run check` runs `tsc --noEmit` for the same set. Both commands complete without a Cursor API key.
- The peer network listens on `127.0.0.1:3000`. Health is `http://127.0.0.1:3000/v1/health` (six slugs). The host index is `http://127.0.0.1:3000/`. The orchestrator playground is `http://127.0.0.1:3000/orchestrator/playground`.
- Unsigned local serve uses `--allow-anonymous --allow-anonymous-cursor-account-mcp`. `run`, `eval`, and `chat` need `CURSOR_API_KEY` or `agent-sdk login`. Skip those when unsigned. Atlassian and GitHub connectors stay optional for validate.
