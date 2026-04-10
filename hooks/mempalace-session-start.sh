#!/bin/bash
# MemPalace UserPromptSubmit Hook
# Palace lives at <project>/.mempalace — project-scoped, not global.
# Exits silently if mempalace is not installed.

MEMPALACE=$(command -v mempalace 2>/dev/null || ls "$HOME"/Library/Python/*/bin/mempalace 2>/dev/null | tail -1)

# Bail immediately if mempalace is not installed — no side effects
if [ -z "$MEMPALACE" ] || [ ! -f "$MEMPALACE" ]; then
    echo '{}'
    exit 0
fi

GLOBAL_CONFIG="$HOME/.mempalace/config.json"
LOG_DIR="$HOME/.mempalace/hook_state"
LOG="$LOG_DIR/init.log"

mkdir -p "$LOG_DIR"
mkdir -p "$HOME/.mempalace"

echo "[$(date '+%H:%M:%S')] HOOK FIRED" >> "$LOG"

# Parse cwd from hook JSON input
TMPFILE=$(mktemp)
cat > "$TMPFILE"

PROJECT_DIR=$(/usr/bin/python3 -c "
import json
try:
    data = json.load(open('$TMPFILE'))
    print(data.get('cwd', ''))
except:
    print('')
" 2>>"$LOG")

rm -f "$TMPFILE"

if [ -z "$PROJECT_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
    PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$HOME}"
fi

PALACE_PATH="$PROJECT_DIR/.mempalace"

echo "[$(date '+%H:%M:%S')] PROJECT_DIR=$PROJECT_DIR palace=$PALACE_PATH" >> "$LOG"

# Sync MCP server config to point at this project's palace
/usr/bin/python3 -c "
import json
cfg = '$GLOBAL_CONFIG'
try:
    with open(cfg) as f:
        data = json.load(f)
except:
    data = {}
data['palace_path'] = '$PALACE_PATH'
with open(cfg, 'w') as f:
    json.dump(data, f, indent=2)
" 2>>"$LOG"

# Fast exit if palace already exists
if [ -d "$PALACE_PATH" ]; then
    echo '[$(date '+%H:%M:%S')] Palace exists — done' >> "$LOG"
    echo '{}'
    exit 0
fi

# Init + mine in background
echo "[$(date '+%H:%M:%S')] No palace — init+mine in background" >> "$LOG"
(
    "$MEMPALACE" --palace "$PALACE_PATH" init "$PROJECT_DIR" --yes >> "$LOG" 2>&1
    echo "[$(date '+%H:%M:%S')] Init exit $?" >> "$LOG"
    "$MEMPALACE" --palace "$PALACE_PATH" mine "$PROJECT_DIR" >> "$LOG" 2>&1
    echo "[$(date '+%H:%M:%S')] Mine exit $?" >> "$LOG"
) &

echo '{}'
exit 0
