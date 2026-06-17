---
name: openwa
description: >-
  Control a self-hosted OpenWA WhatsApp API Gateway from the command line.
  Use this skill whenever the user wants to send WhatsApp messages (text, image,
  document, location, contact, interactive buttons/lists), read or react to
  messages, manage WhatsApp sessions and QR-code login, look up or block
  contacts, create and administer groups, set up webhooks, or manage API keys
  against an OpenWA instance. Trigger it any time OpenWA, a "WhatsApp gateway",
  "WhatsApp API", a local WhatsApp server on port 2785, or sending/automating
  WhatsApp from scripts comes up — even if the user doesn't name the script
  explicitly. Covers the full OpenWA REST API.
---

# OpenWA CLI

`scripts/openwa.py` is a zero-dependency Python CLI (standard library only — no
`pip install` needed) that wraps the entire OpenWA REST API. Prefer it over
hand-writing `curl`: it handles auth, phone-number formatting, JSON bodies,
multipart file uploads, and query params, and it returns pretty-printed JSON.

## Setup & configuration

Configuration resolves as **flag → environment variable → default**:

| Setting | Flag | Env var | Default |
| --- | --- | --- | --- |
| Base URL | `--base-url` | `OPENWA_BASE_URL` | `http://localhost:2785` |
| API key | `--api-key` | `OPENWA_API_KEY` | `dev-admin-key` |
| Session id | `-s` / `--session` | `OPENWA_SESSION` | `default` |

For real use, export the key once rather than passing it each time:

```bash
export OPENWA_API_KEY="dev-admin-key"     # use the instance's real key in production
export OPENWA_BASE_URL="http://localhost:2785"
python3 scripts/openwa.py health
```

Always confirm connectivity with `health` before assuming a command failure is
your fault — a transport error tells the user the instance is down or the URL is
wrong, which is a different problem than a 4xx from the API.

## Mental model

OpenWA is multi-session: one running gateway can host several linked WhatsApp
numbers, each identified by a **session id**. Almost every command operates on a
session (default `default`). To act as a different number, pass `-s <session>`.

A brand-new session is `INITIALIZING` and must be authenticated by scanning a QR
code in the phone's WhatsApp app (Linked Devices). Typical bring-up:

```bash
python3 scripts/openwa.py sessions create --id sales --name "Sales line"
python3 scripts/openwa.py sessions qr sales --format image --out sales-qr.png   # scan this
python3 scripts/openwa.py sessions get sales                                    # status -> CONNECTED
```

Phone numbers can be passed bare (`628123456789`) or as full JIDs
(`628123456789@c.us`); the CLI normalizes them, including stripping `+`, spaces,
and dashes. Group ids get `@g.us` appended automatically.

## Common tasks

```bash
# Send a text message
python3 scripts/openwa.py send text 628123456789 "Hello from OpenWA!"

# Send an image (by URL, by local file via multipart, or base64)
python3 scripts/openwa.py send image 628123456789 --url https://x/p.jpg --caption "Hi"
python3 scripts/openwa.py send image 628123456789 --file ./photo.jpg --caption "Hi"

# Reply quoting a message and mention someone
python3 scripts/openwa.py send text 628123456789 "see above" --quoted MSG_ABC --mention 628111222333

# Read recent chat history, then react
python3 scripts/openwa.py messages list 628123456789 --limit 20
python3 scripts/openwa.py messages react MSG_ABC 👍

# Check a number is on WhatsApp before messaging
python3 scripts/openwa.py contacts exists 628123456789

# Create a group and add people
python3 scripts/openwa.py groups create --name "Project X" --participant 628111 --participant 628222
python3 scripts/openwa.py groups invite-code 120363123456789

# Subscribe a webhook to incoming messages
python3 scripts/openwa.py webhooks create --url https://my.server/wh \
  --event message.received --event message.ack
```

Interactive **list** messages take a JSON `sections` array — write it to a file
and pass `--sections @sections.json` for readability.

Every command and its flags are discoverable: `python3 scripts/openwa.py --help`
and `python3 scripts/openwa.py <group> --help` (e.g. `send --help`). For the full
endpoint map, body shapes, and CLI-to-endpoint mapping, read
[`references/api.md`](references/api.md).

## Output, errors, and scripting

Output is pretty-printed JSON on success. On failure the tool prints the API's
error envelope (or a transport message) to stderr and exits non-zero, so it
composes in shell pipelines. To post-process, pipe stdout to `jq`:

```bash
python3 scripts/openwa.py sessions list | jq '.data[] | {id, status}'
```

For any endpoint not covered by a dedicated subcommand, use the raw escape hatch:

```bash
python3 scripts/openwa.py request GET /api/sessions/default/messages \
  --data '{"phone":"628123456789@c.us"}'
```

## Safety notes

- **Sending is real and irreversible.** Messages go to live WhatsApp recipients.
  When the user's intent or the recipient is ambiguous, confirm the number and
  body before sending, and prefer `contacts exists` first.
- `messages delete` defaults to deleting **for everyone**; pass `--no-for-everyone`
  to remove only on this side.
- `sessions logout` / `sessions delete` clear auth and require re-scanning a QR
  to restore the number — don't run them casually on a connected session.
- Treat the API key as a secret: keep it in `OPENWA_API_KEY`, not in committed
  files or shared command logs.
