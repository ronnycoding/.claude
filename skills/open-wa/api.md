# OpenWA API — endpoint reference

Condensed map of the OpenWA WhatsApp API Gateway. Use this to look up the exact
endpoint, body shape, or CLI command for a task. Source of truth is the running
instance; this mirrors the published spec.

- **Base URL:** `http://localhost:2785` (dev). Override with `--base-url` / `OPENWA_BASE_URL`.
- **Auth:** header `X-API-Key: <key>` on every endpoint except `GET /health`.
- **Phone format:** WhatsApp JID `628123456789@c.us` (contacts) / `...@g.us` (groups).
  The CLI auto-appends the suffix if you pass a bare number, and strips `+`/spaces/dashes.
- **Success envelope:** `{ "success": true, "data": ..., "meta": {...} }`
- **Error envelope:** `{ "success": false, "error": { "code", "message", "details" } }`

## Contents
1. Health & system
2. Sessions
3. Messages (send / read / manage)
4. Contacts
5. Groups
6. Webhooks
7. API keys

---

## 1. Health & system
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/health` | `health` |
| GET | `/health/detailed` | `health --detailed` |
| GET | `/api/metrics` (Prometheus text) | `metrics` |

## 2. Sessions
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/sessions` | `sessions list [--status --limit --offset]` |
| POST | `/api/sessions` | `sessions create [--id --name --webhook --proxy --no-auto-reconnect]` |
| GET | `/api/sessions/:id` | `sessions get <id>` |
| DELETE | `/api/sessions/:id` | `sessions delete <id> [--keep-auth]` |
| GET | `/api/sessions/:id/qr` | `sessions qr <id> [--format base64\|raw\|image] [--out file]` |
| POST | `/api/sessions/:id/restart` | `sessions restart <id>` |
| POST | `/api/sessions/:id/logout` | `sessions logout <id>` |

Create body: `{ id?, name?, config: { autoReconnect?, webhookUrl?, proxy? } }`.
A new session starts `INITIALIZING`; fetch the QR to authenticate by scanning it
in WhatsApp → Linked Devices.

## 3. Messages
Send endpoint is shared: `POST /api/sessions/:id/messages`, with `type` selecting the shape.

| Type | Key body fields | CLI |
| --- | --- | --- |
| text | `body`, `options.{quotedMessageId, mentions[]}` | `send text <phone> <body> [--quoted --mention]` |
| image | `media.{url\|base64+mimetype+filename}`, `caption` | `send image <phone> (--url\|--file\|--base64) [--caption ...]` |
| document | `media.{url\|base64}`, `filename`, `caption` | `send document <phone> (--url\|--file\|--base64) [--filename --caption]` |
| location | `location.{latitude, longitude, name, address}` | `send location <phone> --lat --lng [--name --address]` |
| contact | `contact.{name, phone}` | `send contact <phone> --name --contact-phone` |
| buttons | `body`, `buttons[].{id,text}`, `footer` | `send buttons <phone> <body> --button id:text [--footer]` |
| list | `body`, `buttonText`, `sections[]`, `footer` | `send list <phone> <body> --button-text --sections @file.json [--footer]` |

`--file` uses multipart upload; `--url`/`--base64` send JSON. `sections` for lists
is a JSON array (`[{title, rows:[{id,title,description}]}]`) — pass inline or `@file.json`.

Read / manage:
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/sessions/:id/messages?phone=&limit=&before=&after=&type=` | `messages list <phone> [--limit --before --after --type]` |
| GET | `/api/sessions/:id/messages/:messageId` | `messages get <messageId>` |
| DELETE | `/api/sessions/:id/messages/:messageId?forEveryone=` | `messages delete <messageId> [--no-for-everyone]` |
| POST | `/api/sessions/:id/messages/:messageId/react` | `messages react <messageId> <emoji>` |

## 4. Contacts
Path param is the **bare number** (no `@c.us`); the CLI strips it for you.
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/sessions/:id/contacts` | `contacts list` |
| GET | `/api/sessions/:id/contacts/:phone` | `contacts get <phone>` |
| GET | `/api/sessions/:id/contacts/:phone/exists` | `contacts exists <phone>` |
| POST | `/api/sessions/:id/contacts/:phone/block` | `contacts block <phone>` |
| POST | `/api/sessions/:id/contacts/:phone/unblock` | `contacts unblock <phone>` |

## 5. Groups
Group id is a `...@g.us` JID (CLI appends `@g.us` to a bare id).
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/sessions/:id/groups` | `groups list` |
| POST | `/api/sessions/:id/groups` | `groups create --name --participant ...` |
| GET | `/api/sessions/:id/groups/:gid` | `groups get <gid>` |
| PATCH | `/api/sessions/:id/groups/:gid` | `groups update <gid> [--name --description]` |
| DELETE | `/api/sessions/:id/groups/:gid` (leave) | `groups leave <gid>` |
| POST | `/api/sessions/:id/groups/:gid/participants` | `groups add <gid> --participant ...` |
| DELETE | `/api/sessions/:id/groups/:gid/participants` | `groups remove <gid> --participant ...` |
| POST | `/api/sessions/:id/groups/:gid/admins` | `groups promote <gid> --participant ...` |
| DELETE | `/api/sessions/:id/groups/:gid/admins` | `groups demote <gid> --participant ...` |
| GET | `/api/sessions/:id/groups/:gid/invite-code` | `groups invite-code <gid>` |
| POST | `/api/sessions/:id/groups/:gid/invite-code/revoke` | `groups revoke-invite <gid>` |

## 6. Webhooks
Session-scoped. Available events: `message.received`, `message.sent`,
`message.ack`, `message.revoked`, `session.status`, `session.qr`,
`session.authenticated`, `session.disconnected`, `group.join`, `group.leave`,
`group.update`.
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/sessions/:id/webhooks` | `webhooks list` |
| POST | `/api/sessions/:id/webhooks` | `webhooks create --url --event ... [--header K:V --secret]` |
| GET | `/api/sessions/:id/webhooks/:wid` | `webhooks get <wid>` |
| PATCH | `/api/sessions/:id/webhooks/:wid` | `webhooks update <wid> [--event ... --enable\|--disable]` |
| DELETE | `/api/sessions/:id/webhooks/:wid` | `webhooks delete <wid>` |
| GET | `/api/sessions/:id/webhooks/:wid/logs` | `webhooks logs <wid> [--limit]` |
| POST | `/api/sessions/:id/webhooks/:wid/test` | `webhooks test <wid>` |

## 7. API keys
Not session-scoped. The full key value is returned **only once** at creation.
Permissions: `*`, `sessions:read|write`, `messages:read|write`,
`contacts:read|write`, `groups:read|write`, `webhooks:read|write`,
`api-keys:read|write`.
| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/api-keys` | `keys list` |
| POST | `/api/api-keys` | `keys create --name [--permission ... --session-access ... --rate-limit --expires-at]` |
| DELETE | `/api/api-keys/:id` | `keys delete <id>` |

## Escape hatch
For anything not wrapped above: `request <METHOD> <PATH> [--data '<json>' | --data @file.json]`.
