#!/bin/bash
# ~/.claude/setup.sh
# Run once after cloning this repo on a new machine.

set -e

echo "Setting up ~/.claude dependencies..."

# Install mempalace globally
if command -v mempalace &>/dev/null; then
    echo "mempalace already installed: $(mempalace --version 2>/dev/null || echo 'ok')"
else
    echo "Installing mempalace..."
    pip3 install mempalace
    echo "mempalace installed."
fi

# Copy settings.local.json from example if it doesn't exist
if [ ! -f "$HOME/.claude/settings.local.json" ]; then
    cp "$HOME/.claude/settings.local.json.example" "$HOME/.claude/settings.local.json"
    echo "settings.local.json created from example."
else
    echo "settings.local.json already exists — skipping."
fi

# Make hooks executable
chmod +x "$HOME/.claude/hooks/"*.sh 2>/dev/null && echo "Hooks marked executable."

echo ""
echo "Done. Restart Claude Code to activate hooks."
