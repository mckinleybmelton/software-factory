# architect

Factory specialist peer. Served prompt: `bot/instructions.md`. Skills load on demand — do not paste skill bodies into instructions.

## Conventions

- Peer slug: `architect`
- Skills: `draft-architecture`, `post-architecture-to-jira`
- Runs only when stage is already `architecture_draft`; sole writer of `architecture_review`
- Not a generic Jira peer — stage lookups / draft labels belong to `product`
- Stage labels and peer ownership: see root `AGENTS.md`
