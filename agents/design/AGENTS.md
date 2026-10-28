# design

Factory specialist peer. Served prompt: `bot/instructions.md`. Skills load on demand — do not paste skill bodies into instructions.

## Conventions

- Peer slug: `design`
- Skills: `draft-design`, `post-design-to-jira`
- Runs only when stage is already `design_draft`; sole writer of `design_review`
- Not a generic Jira peer — stage lookups / draft labels belong to `product`
- Stage labels and peer ownership: see root `AGENTS.md`
