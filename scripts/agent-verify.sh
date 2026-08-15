#!/usr/bin/env bash
set -euo pipefail

if [[ -x .venv/bin/python ]]; then
  export PATH="$PWD/.venv/bin:$PATH"
fi
elp_pycache_dir="$(mktemp -d /tmp/elp-pycache.XXXXXX)"
trap 'rm -rf -- "$elp_pycache_dir"' EXIT
export PYTHONPYCACHEPREFIX="$elp_pycache_dir"

elp_node_supports_frontend() {
  "$1" -e '
    const [major, minor] = process.versions.node.split(".").map(Number);
    process.exit(
      (major === 20 && minor >= 19) ||
      (major === 22 && minor >= 12) ||
      major > 22 ? 0 : 1
    );
  ' >/dev/null 2>&1
}

elp_select_frontend_node() {
  local current_node candidate data_home

  current_node="$(command -v node 2>/dev/null || true)"
  if [[ -n "$current_node" ]] && elp_node_supports_frontend "$current_node"; then
    return
  fi

  data_home="${XDG_DATA_HOME:-${HOME:-}/.local/share}"
  for candidate in \
    "${ELP_NODE_BIN:-}" \
    "$data_home"/node-v*/bin/node; do
    if [[ -n "$candidate" && -x "$candidate" ]] && \
      elp_node_supports_frontend "$candidate"; then
      export PATH="$(dirname "$candidate"):$PATH"
      echo "INFO: frontend verification selected Node $(node --version) from $(command -v node)." >&2
      return
    fi
  done

  echo "ERROR: frontend verification requires Node ^20.19.0 or >=22.12.0; found ${current_node:-none}." >&2
  echo "Set ELP_NODE_BIN to a compatible Node executable or install the CI Node 22 runtime." >&2
  exit 2
}

mode="${1:-full}"
case "$mode" in
  contract)
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
      python3 -B -m pytest -q \
        apps/api/tests/test_contract.py \
        apps/api/tests/test_catalog.py \
        apps/api/tests/test_revision.py \
        apps/api/tests/test_runtime.py
    ;;
  quick)
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=apps/api/src \
      python3 -B -m pytest -q apps/api/tests
    ;;
  full)
    elp_select_frontend_node
    ./scripts/verify.sh
    ;;
  *)
    echo "usage: $0 {contract|quick|full}" >&2
    exit 2
    ;;
esac
