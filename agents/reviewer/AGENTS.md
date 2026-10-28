# reviewer

Factory specialist peer. Served prompt: `bot/instructions.md`. Skills load on demand — do not paste skill bodies into instructions.

## Conventions

- Peer slug: `reviewer`
- Skills: `review-pr`, `post-review-packet`
- Runs only when stage is already `pr_review`; comments only — no stage label writes
- Never writes product code, never approves merge, never merges
- Stage labels and peer ownership: see root `AGENTS.md`
