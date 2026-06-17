---
name: ios-simulator
description: Control the iOS Simulator using xcrun simctl. Use when asked to take a screenshot of the simulator, navigate to a screen, open a deep link, launch or kill an app, control the status bar, list simulators, or interact with the running iOS simulator. Trigger terms: simulator, xcrun, simctl, screenshot simulator, deep link, open app, navigate mobile.
allowed-tools: Bash, Read, Glob
---

# iOS Simulator Control

Controls the iOS Simulator via `xcrun simctl`. All commands target the booted device unless a UDID is specified.

## Quick Reference

See [commands.md](commands.md) for the full command reference.

## Core Workflow

### 1. Verify a simulator is booted

```bash
xcrun simctl list devices | grep Booted
```

If nothing is booted, boot one:

```bash
# List available devices first
xcrun simctl list devices available

# Boot by UDID or name
xcrun simctl boot "iPhone 16"
open -a Simulator
```

### 2. Take a screenshot

```bash
xcrun simctl io booted screenshot /tmp/screen.png
```

Then read the image to show it to the user:
```bash
# After running the screenshot command, use the Read tool on the file path
```

Always show the screenshot to the user after taking it.

### 3. Navigate via deep link

**Expo dev build (Metro running on 8081):**
```bash
xcrun simctl openurl booted "exp://localhost:8081/--/<route>"
```

Examples:
```bash
xcrun simctl openurl booted "exp://localhost:8081/--/training"
xcrun simctl openurl booted "exp://localhost:8081/--/nutrition"
xcrun simctl openurl booted "exp://localhost:8081/--/profile"
```

**Production / preview build (custom scheme):**
```bash
xcrun simctl openurl booted "myheavyduty://training"
```

**Generic web URL:**
```bash
xcrun simctl openurl booted "https://example.com"
```

> **Important:** Custom app schemes (`myheavyduty://`) fail in Expo dev mode with LSApplicationWorkspaceErrorDomain error 115. Always use `exp://localhost:8081/--/<path>` for development.

### 4. Launch / terminate an app

```bash
# Find the bundle ID
xcrun simctl listapps booted | grep -A3 "MyHeavyDuty\|heavyduty"

# Launch
xcrun simctl launch booted <bundle-id>

# Terminate
xcrun simctl terminate booted <bundle-id>
```

### 5. Status bar overrides

```bash
# Set clean demo status bar
xcrun simctl status_bar booted override \
  --time "9:41" \
  --batteryState charged \
  --batteryLevel 100 \
  --wifiBars 3 \
  --cellularMode active \
  --cellularBars 4

# Clear overrides (restore real status bar)
xcrun simctl status_bar booted clear
```

## What Does NOT Exist

- `xcrun simctl tap` — not a valid subcommand
- `xcrun simctl io booted tap` — not a valid io operation
- Gesture simulation (swipe, pinch, long press) — requires Detox or accessibility access

## Tapping / Gestures

`simctl` cannot simulate taps. Alternatives:

1. **AppleScript** (requires Terminal to have Accessibility permission in System Settings → Privacy):
```bash
osascript -e 'tell application "System Events" to tell process "Simulator" to click at {x, y}'
```

2. **Deep link** — preferred: navigate directly instead of tapping.

3. **Detox** — for full E2E tap automation.

## Common Patterns

### Screenshot after navigation
```bash
xcrun simctl openurl booted "exp://localhost:8081/--/training"
sleep 2
xcrun simctl io booted screenshot /tmp/training.png
```
Then use Read tool to show `/tmp/training.png`.

### Check what's installed
```bash
xcrun simctl listapps booted | grep -i heavy
```

### Device info
```bash
xcrun simctl list devices | grep Booted
```
