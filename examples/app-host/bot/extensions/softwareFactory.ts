import { cursorPlugin } from "@grok/agent-sdk/extensions";

/**
 * Mount the vendored Cursor plugin. In this monorepo the path reaches the
 * repo-root plugin; consumers copy or submodule `plugins/software-factory`
 * and point `path` at that directory relative to their project root.
 */
export default cursorPlugin({
  path: "../../plugins/software-factory",
});
