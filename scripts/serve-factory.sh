#!/usr/bin/env bash
# Load .env.factory (from setup-factory.sh) and serve the peer network.
#
# Usage:
#   ./scripts/serve-factory.sh
#   ./scripts/serve-factory.sh --allow-anonymous

set -euo pipefail

BDK_PKG="@grok/agent-sdk@0.4.0"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT}/.env.factory"
ALLOW_ANON=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --allow-anonymous) ALLOW_ANON=1; shift ;;
    -h|--help)
      echo "Usage: $0 [--allow-anonymous]"
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

cd "${ROOT}"

if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
  echo "==> Loaded ${ENV_FILE}"
  echo "    FACTORY_PRODUCT_REPO=${FACTORY_PRODUCT_REPO:-"(unset)"}"
else
  echo "warning: ${ENV_FILE} missing — run ./scripts/setup-factory.sh first" >&2
fi

echo "==> Orchestrator playground: http://127.0.0.1:3000/orchestrator/playground"
echo "==> Talk only to the orchestrator. See docs/smoke-e2e.md"

if [[ "${ALLOW_ANON}" -eq 1 ]]; then
  exec npx --yes "${BDK_PKG}" serve --dir ./agents --dev \
    --allow-anonymous --allow-anonymous-cursor-account-mcp
fi

exec npx --yes "${BDK_PKG}" serve --dir ./agents --dev
