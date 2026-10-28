# orchestrator

Factory entry peer. Served prompt: `bot/instructions.md`. Skills load on demand — do not paste skill bodies into instructions.

## Conventions

- Peer slug: `orchestrator`
- Skills: `route-ticket`, `record-gate-decision`
- Asks peers only via MCP (`ask` / `check`): `product`, `design`, `architect`, `implementer`, `reviewer`
- Never drafts PRD, design, architecture, or code; never invents gate approvals
- Stage labels and peer ownership: see root `AGENTS.md`
