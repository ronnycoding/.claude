# xcrun simctl Command Reference

## Device Management

| Action | Command |
|---|---|
| List all devices | `xcrun simctl list devices` |
| List booted | `xcrun simctl list devices \| grep Booted` |
| Boot device | `xcrun simctl boot "<name or UDID>"` |
| Shutdown device | `xcrun simctl shutdown booted` |
| Open Simulator app | `open -a Simulator` |
| Erase device | `xcrun simctl erase booted` |

## App Management

| Action | Command |
|---|---|
| List installed apps | `xcrun simctl listapps booted` |
| Launch app | `xcrun simctl launch booted <bundle-id>` |
| Terminate app | `xcrun simctl terminate booted <bundle-id>` |
| Install .app | `xcrun simctl install booted <path>.app` |
| Uninstall | `xcrun simctl uninstall booted <bundle-id>` |

## Navigation & URLs

| Action | Command |
|---|---|
| Open URL/deep link | `xcrun simctl openurl booted "<url>"` |
| Expo dev route | `xcrun simctl openurl booted "exp://localhost:8081/--/<route>"` |
| Open Safari URL | `xcrun simctl openurl booted "https://example.com"` |

## Media & IO

| Action | Command |
|---|---|
| Screenshot (PNG) | `xcrun simctl io booted screenshot /tmp/screen.png` |
| Screenshot (JPEG) | `xcrun simctl io booted screenshot --type jpeg /tmp/screen.jpg` |
| Record video | `xcrun simctl io booted recordVideo /tmp/video.mov` |
| Add photo to library | `xcrun simctl addmedia booted /path/image.png` |

## Status Bar

| Action | Command |
|---|---|
| Set demo bar | `xcrun simctl status_bar booted override --time "9:41" --batteryState charged --batteryLevel 100 --wifiBars 3` |
| Clear overrides | `xcrun simctl status_bar booted clear` |

## Other

| Action | Command |
|---|---|
| Set location | `xcrun simctl location booted set <lat> <lon>` |
| Push notification | `xcrun simctl push booted <bundle-id> payload.json` |
| Paste text | `xcrun simctl pbpaste booted` |
| Copy to clipboard | `echo "text" \| xcrun simctl pbcopy booted` |
| Privacy grant | `xcrun simctl privacy booted grant camera <bundle-id>` |

## Expo Router Deep Link Routes (this project)

| Screen | Deep Link |
|---|---|
| Your Day | `exp://localhost:8081/--/your-day` |
| Training | `exp://localhost:8081/--/training` |
| Nutrition | `exp://localhost:8081/--/nutrition` |
| Health | `exp://localhost:8081/--/health` |
| Plan | `exp://localhost:8081/--/plan` |
| Profile | `exp://localhost:8081/--/profile` |
| Settings | `exp://localhost:8081/--/settings` |
| Auth | `exp://localhost:8081/--/auth` |
| AI Plan | `exp://localhost:8081/--/ai-plan` |
| Supplements | `exp://localhost:8081/--/supplements` |
| Body Metrics | `exp://localhost:8081/--/body-metrics` |
| Recipes | `exp://localhost:8081/--/recipes` |
