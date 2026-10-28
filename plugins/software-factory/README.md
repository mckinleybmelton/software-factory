# software-factory Cursor plugin

Vendored Cursor plugin for IDE install or Agent SDK `cursorPlugin` mounts.

```ts
// bot/extensions/softwareFactory.ts
import { cursorPlugin } from "@grok/agent-sdk/extensions";

export default cursorPlugin({
  path: "plugins/software-factory", // project-relative; copy or submodule this directory
});
```

Contributes skills, commands, and agent stubs. The full peer network still runs via `agent-sdk serve --dir ./agents` or hosted deploy slugs — this plugin does not replace the six peers.
