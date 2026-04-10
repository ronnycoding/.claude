#!/bin/bash
# MemPalace UserPromptSubmit Hook

MEMPALACE=$(command -v mempalace 2>/dev/null || ls "$HOME"/Library/Python/*/bin/mempalace 2>/dev/null | tail -1)
GLOBAL_CONFIG="$HOME/.mempalace/config.json"
LOG_DIR="$HOME/.mempalace/hook_state"
LOG="$LOG_DIR/init.log"

mkdir -p "$LOG_DIR"

# Bail early if mempalace is not installed
if [ ! -f "$MEMPALACE" ]; then
    echo '{}'
    exit 0
fi

mkdir -p "$HOME/.mempalace"

# Log immediately to confirm the hook fired
echo "[$(date '+%H:%M:%S')] HOOK FIRED" >> "$LOG"

# Read and save input to a temp file (avoids quoting issues in subshells)
TMPFILE=$(mktemp)
cat > "$TMPFILE"

# Log raw input for debugging
echo "[$(date '+%H:%M:%S')] INPUT: $(cat $TMPFILE)" >> "$LOG"

# Parse cwd
PROJECT_DIR=$(/usr/bin/python3 -c "
import sys, json
try:
    data = json.load(open('$TMPFILE'))
    print(data.get('cwd', ''))
except Exception as e:
    print('')
" 2>>"$LOG")

rm -f "$TMPFILE"

echo "[$(date '+%H:%M:%S')] PROJECT_DIR=$PROJECT_DIR" >> "$LOG"

# Fallbacks
if [ -z "$PROJECT_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
    PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$HOME}"
    echo "[$(date '+%H:%M:%S')] Fallback PROJECT_DIR=$PROJECT_DIR" >> "$LOG"
fi

PALACE_PATH="$PROJECT_DIR/.mempalace"

# Sync MCP config
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

# Exit immediately if palace already exists
if [ -d "$PALACE_PATH" ]; then
    echo "[$(date '+%H:%M:%S')] Palace exists at $PALACE_PATH — done" >> "$LOG"
    echo '{}'
    exit 0
fi

# Init + mine in background
echo "[$(date '+%H:%M:%S')] No palace — starting init+mine in background for $PALACE_PATH" >> "$LOG"
(
    "$MEMPALACE" --palace "$PALACE_PATH" init "$PROJECT_DIR" --yes >> "$LOG" 2>&1
    echo "[$(date '+%H:%M:%S')] Init exit $?" >> "$LOG"
    "$MEMPALACE" --palace "$PALACE_PATH" mine "$PROJECT_DIR" >> "$LOG" 2>&1
    echo "[$(date '+%H:%M:%S')] Mine exit $?" >> "$LOG"
) &

echo '{}'
exit 0
