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

## Stage labels

Exactly one factory stage label on the ticket:

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

## Knowledge layers

Workspace `AGENTS.md` → agent `bot/instructions.md` → skills → `references/` → external MCP. Details: Project doc `docs/knowledge-layer.md`.
