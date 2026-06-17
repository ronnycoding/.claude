---
name: penwa
description: Drive the OpenWA WhatsApp HTTP API from the terminal with curl. Use when sending WhatsApp messages (text/image/video/audio/document/location/contact/bulk), managing sessions and QR login, listing contacts/groups/chats, registering webhooks, or managing scoped API keys against an OpenWA server. Triggers on "OpenWA", "penwa", "send WhatsApp via API", "WhatsApp session", or mentions of base URL http://0.0.0.0:2785.
---

# penwa — OpenWA API via curl

Talk to an [OpenWA](https://github.com/rmyndharis/OpenWA) WhatsApp server over its REST API using `curl`. Spec: `docs/06-api-specification.md`.

## Connection

| Setting  | Flag         | Env var           | Default               |
|----------|--------------|-------------------|-----------------------|
| Base URL | `--base-url` | `OPENWA_BASE_URL` | `http://0.0.0.0:2785` |
| API key  | `--api-key`  | `OPENWA_API_KEY`  | `dev-admin-key`       |

- **All API paths are prefixed with `/api`** → e.g. `http://0.0.0.0:2785/api/sessions`.
- **Auth header is `X-API-Key`** (not `Authorization`). Send it on every call except `GET /health`.
- Set up the shell once, then every snippet below works as-is:

```bash
export OPENWA_BASE_URL="${OPENWA_BASE_URL:-http://0.0.0.0:2785}"
export OPENWA_API_KEY="${OPENWA_API_KEY:-dev-admin-key}"
BASE="$OPENWA_BASE_URL/api"
AUTH=(-H "X-API-Key: $OPENWA_API_KEY" -H "Content-Type: application/json")
```

> `chatId` format: individuals `<countrycode><number>@c.us` (e.g. `628123456789@c.us`); groups `<id>@g.us`. No `+`, spaces, or dashes.

## Quick start: verify, log in, send

```bash
# 1. Is the server up? (public, no key)
curl -s "$BASE/health"

# 2. Is my key valid?
curl -s -X POST "$BASE/auth/validate" "${AUTH[@]}"

# 3. Create a session
curl -s -X POST "$BASE/sessions" "${AUTH[@]}" -d '{"name":"main"}'
# -> note the returned sessionId, e.g. sess_abc123

# 4. Get the QR (scan in WhatsApp > Linked devices). Returns an image.
SID=sess_abc123
curl -s "$BASE/sessions/$SID/qr" -H "X-API-Key: $OPENWA_API_KEY" -o qr.png && open qr.png

# 5. Poll until connected
curl -s "$BASE/sessions/$SID" "${AUTH[@]}"   # watch for status: connected

# 6. Send your first message
curl -s -X POST "$BASE/sessions/$SID/messages/send-text" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","text":"Hello from OpenWA!"}'
```

Add `-H "X-Request-ID: req_$(date +%s)"` to any write call for traceable logs. Pipe responses through `| jq` to read them.

## Sessions

```bash
# List (optional ?status= ?page= ?limit=)
curl -s "$BASE/sessions?status=connected&limit=20" "${AUTH[@]}"

# Create with a webhook attached
curl -s -X POST "$BASE/sessions" "${AUTH[@]}" \
  -d '{"name":"sales-bot","webhook":"https://example.com/hook"}'

# Details / QR / logout / delete
curl -s     "$BASE/sessions/$SID"        "${AUTH[@]}"
curl -s     "$BASE/sessions/$SID/qr"     -H "X-API-Key: $OPENWA_API_KEY" -o qr.png
curl -s -X POST   "$BASE/sessions/$SID/logout" "${AUTH[@]}"
curl -s -X DELETE "$BASE/sessions/$SID"        "${AUTH[@]}"
```

## Sending messages

All send endpoints are `POST /sessions/:sessionId/messages/send-<type>`. Media accepts either `{"url":"..."}` or a base64 `{"data":"...","mimetype":"..."}` object — `{"url":...}` shown.

```bash
SEND="$BASE/sessions/$SID/messages"

# Text
curl -s -X POST "$SEND/send-text" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","text":"Hello *world*"}'

# Image (with caption)
curl -s -X POST "$SEND/send-image" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","image":{"url":"https://example.com/pic.jpg"},"caption":"Check this out!"}'

# Video
curl -s -X POST "$SEND/send-video" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","video":{"url":"https://example.com/clip.mp4"},"caption":"demo"}'

# Audio / voice note (ptt:true = push-to-talk bubble)
curl -s -X POST "$SEND/send-audio" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","audio":{"url":"https://example.com/vn.ogg"},"ptt":true}'

# Document
curl -s -X POST "$SEND/send-document" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","document":{"url":"https://example.com/invoice.pdf"},"filename":"invoice.pdf","caption":"Your invoice"}'

# Location
curl -s -X POST "$SEND/send-location" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","latitude":-6.2088,"longitude":106.8456,"description":"Jakarta HQ"}'

# Contact card
curl -s -X POST "$SEND/send-contact" "${AUTH[@]}" \
  -d '{"chatId":"628123456789@c.us","contact":{"name":"Jane","phone":"628987654321"}}'
```

### Bulk send

```bash
# Queue a batch
curl -s -X POST "$SEND/send-bulk" "${AUTH[@]}" -d '{
  "messages":[
    {"chatId":"628111111111@c.us","text":"Hi A"},
    {"chatId":"628222222222@c.us","text":"Hi B"}
  ]
}'
# -> returns a batchId

BID=batch_xyz
curl -s     "$SEND/batch/$BID"        "${AUTH[@]}"   # status/progress
curl -s -X POST "$SEND/batch/$BID/cancel" "${AUTH[@]}"   # cancel
```

### Message history

```bash
curl -s "$BASE/sessions/$SID/chats/628123456789@c.us/messages?limit=50" "${AUTH[@]}"
# ?before=<messageId> to paginate older
```

## Contacts

```bash
curl -s "$BASE/sessions/$SID/contacts" "${AUTH[@]}"
# Does this number have WhatsApp?
curl -s "$BASE/sessions/$SID/contacts/check/628123456789" "${AUTH[@]}"
# Avatar
curl -s "$BASE/sessions/$SID/contacts/628123456789@c.us/profile-picture" "${AUTH[@]}"
```

## Groups

```bash
curl -s "$BASE/sessions/$SID/groups" "${AUTH[@]}"                 # list
curl -s "$BASE/sessions/$SID/groups/120363000000000000@g.us" "${AUTH[@]}"   # info + participants
# Create
curl -s -X POST "$BASE/sessions/$SID/groups" "${AUTH[@]}" \
  -d '{"name":"Project Team","participants":["628111111111@c.us","628222222222@c.us"]}'
```

## Webhooks

```bash
# Register
curl -s -X POST "$BASE/sessions/$SID/webhooks" "${AUTH[@]}" -d '{
  "url":"https://example.com/wa-hook",
  "events":["message.received","message.ack","session.status"],
  "secret":"shhh"
}'
curl -s     "$BASE/sessions/$SID/webhooks"            "${AUTH[@]}"   # list
curl -s -X DELETE "$BASE/sessions/$SID/webhooks/wh_123"  "${AUTH[@]}"   # delete
```

## API key management (admin role)

```bash
# Create a scoped key
curl -s -X POST "$BASE/auth/api-keys" "${AUTH[@]}" \
  -d '{"name":"n8n Integration","role":"operator"}'
# Optional fields: allowedIps[], allowedSessions[], expiresAt (ISO)

curl -s     "$BASE/auth/api-keys"            "${AUTH[@]}"   # list
curl -s     "$BASE/auth/api-keys/key_123"    "${AUTH[@]}"   # details
curl -s -X PUT    "$BASE/auth/api-keys/key_123" "${AUTH[@]}" -d '{"role":"viewer"}'
curl -s -X POST   "$BASE/auth/api-keys/key_123/revoke" "${AUTH[@]}"
curl -s -X DELETE "$BASE/auth/api-keys/key_123" "${AUTH[@]}"
```

## Health

```bash
curl -s "$BASE/health"            # public, no key
curl -s "$BASE/health/detailed" "${AUTH[@]}"   # auth required
```

## Tips & gotchas

- **`/api` prefix** — endpoints in the spec tables omit it; always prepend it (already baked into `$BASE`).
- **QR is binary** — write to a file with `-o qr.png`; don't dump it to the terminal.
- **`X-API-Key`, not Bearer** — a `401` almost always means wrong header name or key.
- **chatId hygiene** — strip `+`/spaces; suffix `@c.us` (person) or `@g.us` (group). Use `contacts/check` before sending to unknown numbers.
- **Debug a call** — add `-i` to see status + headers, or `-w '\n%{http_code}\n'` for just the code.
- **WebSocket** for realtime: `wss://<host>/ws?apiKey=$OPENWA_API_KEY`, then send `{"type":"subscribe","payload":{"sessionId":"...","events":[...]}}`.
- Reach for `jq` to extract fields, e.g. `... | jq -r '.sessionId'` to capture and reuse.
