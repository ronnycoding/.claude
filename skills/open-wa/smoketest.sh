#!/usr/bin/env bash
# OpenWA skill smoke test — run on the machine where OpenWA :2785 is reachable.
#
# Usage:
#   export OPENWA_API_KEY="dev-admin-key"
#   export TEST_PHONE="628xxxxxxxxx"     # a number YOU control (we send it one msg)
#   bash smoketest.sh /path/to/openwa/scripts/openwa.py
#
set -uo pipefail
CLI="${1:?pass the path to openwa.py}"
PY="$(command -v python3 || command -v python)"
run() { echo; echo "### $*"; "$PY" "$CLI" "$@"; echo "--- exit=$? ---"; }

run health
run health --detailed
run sessions list
run -s default sessions get default        # adjust 'default' if your session id differs
run contacts list
run groups list

if [[ -n "${TEST_PHONE:-}" ]]; then
  run contacts exists "$TEST_PHONE"
  run send text "$TEST_PHONE" "OpenWA skill smoke test ✅"
else
  echo; echo "(skipping send — set TEST_PHONE to test an outgoing message)"
fi

echo; echo "=== smoke test done ==="
