# implementer

Factory specialist peer. Served prompt: `bot/instructions.md`. Skills load on demand — do not paste skill bodies into instructions.

## Conventions

- Peer slug: `implementer`
- Skills: `implement-change`, `open-pr`
- Runs only when stage is already `implementation`; sole writer of `pr_review` (after PR exists; includes jira-complete reuse of an existing PR)
- Never approves or merges; product-repo config via env (see skill `references/`)
- Stage labels and peer ownership: see root `AGENTS.md`
