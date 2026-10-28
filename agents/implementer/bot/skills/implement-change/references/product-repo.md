# Product repo config and worktree isolation

## Repo identity (env or ask)

| Source | Meaning |
| --- | --- |
| `FACTORY_PRODUCT_REPO` or `PRODUCT_REPO` | Product GitHub repo as `owner/name` (required for live implement) |
| `FACTORY_PRODUCT_REPO_PATH` or `PRODUCT_REPO_PATH` | Optional local checkout / cache path |
| `FACTORY_PRODUCT_DEFAULT_BRANCH` or `PRODUCT_DEFAULT_BRANCH` | Default base branch (fallback `main`) |
| Orchestrator / human message | Named repo override for that turn |

If none are set, abort with `blocked_missing_product_repo` and ask the orchestrator (or human) to configure the product repo — do not invent a repo.

The factory repo (`software-factory`) is **not** the product repo unless config explicitly points there.

## Worktree isolation

- Create a worktree / ticket branch **only after** stage is `implementation` and approved architecture + acceptance criteria are confirmed. Missing artifacts → abort with no git side effects (`blocked_missing_architecture` / `blocked_missing_acceptance_criteria`).
- Prefer `git worktree add` (or an SDK/local cache checkout dedicated to this ticket) under a per-ticket directory.
- Never share a dirty working tree across tickets.
- Branch naming: include the ticket key (e.g. `factory/<KEY>-short-slug` or the product’s existing convention).
- Push only the ticket branch. Do not push to the default branch. Do not force-push shared branches.

## Permissions

- Implementer may create branches, push the ticket branch, and open **one** PR.
- Implementer has **no** merge rights and must not merge, close as approved, or skip the human PR gate.
