#!/usr/bin/env python3
"""
openwa.py — a zero-dependency CLI for the OpenWA WhatsApp API Gateway.

Wraps the OpenWA REST API (sessions, messages, contacts, groups, webhooks,
API keys). Uses only the Python standard library so it runs anywhere without
`pip install`.

Configuration (flags override environment, environment overrides defaults):
  --base-url / OPENWA_BASE_URL   default: http://localhost:2785
  --api-key  / OPENWA_API_KEY    default: dev-admin-key
  --session  / OPENWA_SESSION    default: default   (session-scoped commands)

Run `openwa.py --help` or `openwa.py <group> --help` for the full surface.
"""

import argparse
import json
import mimetypes
import os
import sys
import uuid
from urllib import request as urlrequest
from urllib import parse as urlparse
from urllib.error import HTTPError, URLError

DEFAULT_BASE_URL = "http://localhost:2785"
DEFAULT_API_KEY = "dev-admin-key"
DEFAULT_SESSION = "default"


# --------------------------------------------------------------------------- #
# HTTP plumbing
# --------------------------------------------------------------------------- #
class ApiError(Exception):
    """Raised for transport failures or non-2xx responses we want to surface."""


def _normalize_phone(value, group=False):
    """Accept a bare number or a full JID; return a WhatsApp JID.

    '628123456789'          -> '628123456789@c.us'
    '+62 812-3456-789'      -> '628123456789@c.us'
    '628...@c.us'           -> unchanged
    group=True              -> '...@g.us'
    """
    if value is None:
        return None
    v = value.strip()
    if "@" in v:
        return v
    digits = "".join(ch for ch in v if ch.isdigit())
    suffix = "@g.us" if group else "@c.us"
    return f"{digits}{suffix}"


def _encode_multipart(fields, files):
    """Build a multipart/form-data body. `fields` is a dict of str->str,
    `files` is a list of (field_name, filepath). Returns (body_bytes, content_type)."""
    boundary = f"----openwa{uuid.uuid4().hex}"
    crlf = b"\r\n"
    body = bytearray()
    for name, val in fields.items():
        if val is None:
            continue
        body += b"--" + boundary.encode() + crlf
        body += f'Content-Disposition: form-data; name="{name}"'.encode() + crlf + crlf
        body += str(val).encode() + crlf
    for name, path in files:
        filename = os.path.basename(path)
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as fh:
            data = fh.read()
        body += b"--" + boundary.encode() + crlf
        body += (
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'
        ).encode() + crlf
        body += f"Content-Type: {ctype}".encode() + crlf + crlf
        body += data + crlf
    body += b"--" + boundary.encode() + b"--" + crlf
    return bytes(body), f"multipart/form-data; boundary={boundary}"


class Client:
    def __init__(self, base_url, api_key, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def request(self, method, path, params=None, json_body=None,
                multipart=None, raw_response=False):
        url = self.base_url + path
        if params:
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                url += "?" + urlparse.urlencode(clean)

        headers = {"X-API-Key": self.api_key, "Accept": "application/json"}
        data = None
        if multipart is not None:
            fields, files = multipart
            data, ctype = _encode_multipart(fields, files)
            headers["Content-Type"] = ctype
        elif json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urlrequest.Request(url, data=data, headers=headers, method=method)
        try:
            with urlrequest.urlopen(req, timeout=self.timeout) as resp:
                payload = resp.read()
                if raw_response:
                    return payload, resp.headers.get("Content-Type", "")
                return self._decode(payload)
        except HTTPError as e:
            payload = e.read()
            decoded = self._safe_decode(payload)
            raise ApiError(
                f"HTTP {e.code} {e.reason} on {method} {path}\n"
                + json.dumps(decoded, indent=2)
                if isinstance(decoded, (dict, list))
                else f"HTTP {e.code} {e.reason} on {method} {path}\n{decoded}"
            )
        except URLError as e:
            raise ApiError(
                f"Could not reach {url} ({e.reason}). "
                "Is OpenWA running and is --base-url correct?"
            )

    @staticmethod
    def _decode(payload):
        if not payload:
            return {}
        return json.loads(payload.decode("utf-8"))

    @staticmethod
    def _safe_decode(payload):
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception:
            return payload.decode("utf-8", "replace")


def _out(obj):
    """Pretty-print a JSON-able object to stdout."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------- #
# Command handlers
# --------------------------------------------------------------------------- #
def cmd_health(c, a):
    path = "/health/detailed" if a.detailed else "/health"
    _out(c.request("GET", path))


def cmd_metrics(c, a):
    # Prometheus text, not JSON.
    payload, _ = c.request("GET", "/api/metrics", raw_response=True)
    sys.stdout.write(payload.decode("utf-8", "replace"))


# ---- sessions ---- #
def cmd_sessions_list(c, a):
    _out(c.request("GET", "/api/sessions",
                   params={"status": a.status, "limit": a.limit, "offset": a.offset}))


def cmd_sessions_create(c, a):
    config = {}
    if a.no_auto_reconnect:
        config["autoReconnect"] = False
    if a.webhook:
        config["webhookUrl"] = a.webhook
    if a.proxy:
        config["proxy"] = a.proxy
    body = {}
    if a.id:
        body["id"] = a.id
    if a.name:
        body["name"] = a.name
    if config:
        body["config"] = config
    _out(c.request("POST", "/api/sessions", json_body=body))


def cmd_sessions_get(c, a):
    _out(c.request("GET", f"/api/sessions/{a.id}"))


def cmd_sessions_delete(c, a):
    _out(c.request("DELETE", f"/api/sessions/{a.id}",
                   params={"keepAuth": "true" if a.keep_auth else None}))


def cmd_sessions_qr(c, a):
    if a.format == "image":
        payload, _ = c.request("GET", f"/api/sessions/{a.id}/qr",
                               params={"format": "image"}, raw_response=True)
        target = a.out or f"{a.id}-qr.png"
        with open(target, "wb") as fh:
            fh.write(payload)
        _out({"saved": target, "bytes": len(payload)})
    else:
        _out(c.request("GET", f"/api/sessions/{a.id}/qr",
                       params={"format": a.format}))


def cmd_sessions_restart(c, a):
    _out(c.request("POST", f"/api/sessions/{a.id}/restart"))


def cmd_sessions_logout(c, a):
    _out(c.request("POST", f"/api/sessions/{a.id}/logout"))


# ---- messages (send) ---- #
def _send(c, session, body=None, multipart=None):
    return c.request("POST", f"/api/sessions/{session}/messages",
                     json_body=body, multipart=multipart)


def cmd_send_text(c, a):
    body = {"phone": _normalize_phone(a.phone), "type": "text", "body": a.body}
    options = {}
    if a.quoted:
        options["quotedMessageId"] = a.quoted
    if a.mention:
        options["mentions"] = [_normalize_phone(m) for m in a.mention]
    if options:
        body["options"] = options
    _out(_send(c, a.session, body=body))


def _media_body(a, mtype):
    """Shared builder for image/document (URL or base64 via JSON)."""
    body = {"phone": _normalize_phone(a.phone), "type": mtype}
    if a.url:
        body["media"] = {"url": a.url}
    elif a.base64:
        media = {"base64": a.base64}
        if a.mimetype:
            media["mimetype"] = a.mimetype
        if a.filename:
            media["filename"] = a.filename
        body["media"] = media
    if getattr(a, "caption", None):
        body["caption"] = a.caption
    if mtype == "document" and a.filename:
        body["filename"] = a.filename
    return body


def cmd_send_image(c, a):
    if a.file:  # multipart upload
        fields = {"phone": _normalize_phone(a.phone), "type": "image",
                  "caption": a.caption}
        _out(_send(c, a.session, multipart=(fields, [("media", a.file)])))
    else:
        _out(_send(c, a.session, body=_media_body(a, "image")))


def cmd_send_document(c, a):
    if a.file:
        fields = {"phone": _normalize_phone(a.phone), "type": "document",
                  "caption": a.caption, "filename": a.filename}
        _out(_send(c, a.session, multipart=(fields, [("media", a.file)])))
    else:
        _out(_send(c, a.session, body=_media_body(a, "document")))


def cmd_send_location(c, a):
    body = {"phone": _normalize_phone(a.phone), "type": "location",
            "location": {"latitude": a.lat, "longitude": a.lng,
                         "name": a.name, "address": a.address}}
    _out(_send(c, a.session, body=body))


def cmd_send_contact(c, a):
    body = {"phone": _normalize_phone(a.phone), "type": "contact",
            "contact": {"name": a.name, "phone": a.contact_phone}}
    _out(_send(c, a.session, body=body))


def _parse_pair(value, sep=":"):
    if sep not in value:
        raise argparse.ArgumentTypeError(f"expected format key{sep}value, got '{value}'")
    k, v = value.split(sep, 1)
    return k.strip(), v.strip()


def cmd_send_buttons(c, a):
    buttons = [{"id": bid, "text": text} for bid, text in a.button]
    body = {"phone": _normalize_phone(a.phone), "type": "buttons",
            "body": a.body, "buttons": buttons}
    if a.footer:
        body["footer"] = a.footer
    _out(_send(c, a.session, body=body))


def cmd_send_list(c, a):
    # Sections are complex; accept a JSON string or @file for full control.
    sections = _load_json_arg(a.sections)
    body = {"phone": _normalize_phone(a.phone), "type": "list",
            "body": a.body, "buttonText": a.button_text, "sections": sections}
    if a.footer:
        body["footer"] = a.footer
    _out(_send(c, a.session, body=body))


# ---- messages (read/manage) ---- #
def cmd_messages_list(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/messages",
                   params={"phone": _normalize_phone(a.phone), "limit": a.limit,
                           "before": a.before, "after": a.after, "type": a.type}))


def cmd_messages_get(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/messages/{a.message_id}"))


def cmd_messages_delete(c, a):
    for_everyone = "false" if a.no_for_everyone else "true"
    _out(c.request("DELETE", f"/api/sessions/{a.session}/messages/{a.message_id}",
                   params={"forEveryone": for_everyone}))


def cmd_messages_react(c, a):
    _out(c.request("POST", f"/api/sessions/{a.session}/messages/{a.message_id}/react",
                   json_body={"emoji": a.emoji}))


# ---- contacts ---- #
def cmd_contacts_list(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/contacts"))


def cmd_contacts_get(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/contacts/{_bare(a.phone)}"))


def cmd_contacts_exists(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/contacts/{_bare(a.phone)}/exists"))


def cmd_contacts_block(c, a):
    _out(c.request("POST", f"/api/sessions/{a.session}/contacts/{_bare(a.phone)}/block"))


def cmd_contacts_unblock(c, a):
    _out(c.request("POST", f"/api/sessions/{a.session}/contacts/{_bare(a.phone)}/unblock"))


def _bare(value):
    """Contact path params use the bare number (no @c.us)."""
    if value is None:
        return value
    v = value.strip()
    if "@" in v:
        v = v.split("@", 1)[0]
    return "".join(ch for ch in v if ch.isdigit())


# ---- groups ---- #
def cmd_groups_list(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/groups"))


def cmd_groups_create(c, a):
    body = {"name": a.name,
            "participants": [_normalize_phone(p) for p in a.participant]}
    _out(c.request("POST", f"/api/sessions/{a.session}/groups", json_body=body))


def cmd_groups_get(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/groups/{_normalize_phone(a.group_id, group=True)}"))


def cmd_groups_update(c, a):
    body = {}
    if a.name is not None:
        body["name"] = a.name
    if a.description is not None:
        body["description"] = a.description
    _out(c.request("PATCH", f"/api/sessions/{a.session}/groups/{_normalize_phone(a.group_id, group=True)}",
                   json_body=body))


def cmd_groups_leave(c, a):
    _out(c.request("DELETE", f"/api/sessions/{a.session}/groups/{_normalize_phone(a.group_id, group=True)}"))


def _group_participants(c, a, method):
    gid = _normalize_phone(a.group_id, group=True)
    body = {"participants": [_normalize_phone(p) for p in a.participant]}
    return c.request(method, f"/api/sessions/{a.session}/groups/{gid}/participants",
                     json_body=body)


def cmd_groups_add(c, a):
    _out(_group_participants(c, a, "POST"))


def cmd_groups_remove(c, a):
    _out(_group_participants(c, a, "DELETE"))


def _group_admins(c, a, method):
    gid = _normalize_phone(a.group_id, group=True)
    body = {"participants": [_normalize_phone(p) for p in a.participant]}
    return c.request(method, f"/api/sessions/{a.session}/groups/{gid}/admins",
                     json_body=body)


def cmd_groups_promote(c, a):
    _out(_group_admins(c, a, "POST"))


def cmd_groups_demote(c, a):
    _out(_group_admins(c, a, "DELETE"))


def cmd_groups_invite_code(c, a):
    gid = _normalize_phone(a.group_id, group=True)
    _out(c.request("GET", f"/api/sessions/{a.session}/groups/{gid}/invite-code"))


def cmd_groups_revoke_invite(c, a):
    gid = _normalize_phone(a.group_id, group=True)
    _out(c.request("POST", f"/api/sessions/{a.session}/groups/{gid}/invite-code/revoke"))


# ---- webhooks ---- #
def cmd_webhooks_list(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/webhooks"))


def cmd_webhooks_create(c, a):
    body = {"url": a.url, "events": a.event}
    if a.header:
        body["headers"] = dict(a.header)
    if a.secret:
        body["secret"] = a.secret
    _out(c.request("POST", f"/api/sessions/{a.session}/webhooks", json_body=body))


def cmd_webhooks_get(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/webhooks/{a.webhook_id}"))


def cmd_webhooks_update(c, a):
    body = {}
    if a.event:
        body["events"] = a.event
    if a.enable:
        body["enabled"] = True
    if a.disable:
        body["enabled"] = False
    _out(c.request("PATCH", f"/api/sessions/{a.session}/webhooks/{a.webhook_id}",
                   json_body=body))


def cmd_webhooks_delete(c, a):
    _out(c.request("DELETE", f"/api/sessions/{a.session}/webhooks/{a.webhook_id}"))


def cmd_webhooks_logs(c, a):
    _out(c.request("GET", f"/api/sessions/{a.session}/webhooks/{a.webhook_id}/logs",
                   params={"limit": a.limit}))


def cmd_webhooks_test(c, a):
    _out(c.request("POST", f"/api/sessions/{a.session}/webhooks/{a.webhook_id}/test"))


# ---- api keys ---- #
def cmd_keys_list(c, a):
    _out(c.request("GET", "/api/api-keys"))


def cmd_keys_create(c, a):
    body = {"name": a.name}
    if a.permission:
        body["permissions"] = a.permission
    if a.session_access:
        body["sessionAccess"] = a.session_access
    if a.rate_limit is not None:
        body["rateLimit"] = a.rate_limit
    if a.expires_at:
        body["expiresAt"] = a.expires_at
    _out(c.request("POST", "/api/api-keys", json_body=body))


def cmd_keys_delete(c, a):
    _out(c.request("DELETE", f"/api/api-keys/{a.key_id}"))


# ---- raw escape hatch ---- #
def cmd_request(c, a):
    body = _load_json_arg(a.data) if a.data else None
    _out(c.request(a.method.upper(), a.path, json_body=body))


def _load_json_arg(value):
    """Accept inline JSON or @path/to/file.json."""
    if value is None:
        return None
    if value.startswith("@"):
        with open(value[1:], "r", encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(value)


# --------------------------------------------------------------------------- #
# Argument parser
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(
        prog="openwa",
        description="CLI for the OpenWA WhatsApp API Gateway.",
    )
    p.add_argument("--base-url", default=os.environ.get("OPENWA_BASE_URL", DEFAULT_BASE_URL),
                   help="OpenWA base URL (env OPENWA_BASE_URL, default %(default)s)")
    p.add_argument("--api-key", default=os.environ.get("OPENWA_API_KEY", DEFAULT_API_KEY),
                   help="API key sent as X-API-Key (env OPENWA_API_KEY)")
    p.add_argument("-s", "--session", default=os.environ.get("OPENWA_SESSION", DEFAULT_SESSION),
                   help="Session id for session-scoped commands (env OPENWA_SESSION, default %(default)s)")
    p.add_argument("--timeout", type=int, default=30, help="Request timeout seconds")

    sub = p.add_subparsers(dest="group", required=True)

    # health / metrics
    sp = sub.add_parser("health", help="Health check")
    sp.add_argument("--detailed", action="store_true", help="Detailed health")
    sp.set_defaults(func=cmd_health)

    sp = sub.add_parser("metrics", help="Prometheus metrics")
    sp.set_defaults(func=cmd_metrics)

    _add_sessions(sub)
    _add_send(sub)
    _add_messages(sub)
    _add_contacts(sub)
    _add_groups(sub)
    _add_webhooks(sub)
    _add_keys(sub)

    # raw
    sp = sub.add_parser("request", help="Raw request escape hatch")
    sp.add_argument("method")
    sp.add_argument("path", help="e.g. /api/sessions")
    sp.add_argument("--data", help="JSON body, inline or @file.json")
    sp.set_defaults(func=cmd_request)

    return p


def _add_sessions(sub):
    g = sub.add_parser("sessions", help="Manage sessions").add_subparsers(dest="action", required=True)

    s = g.add_parser("list")
    s.add_argument("--status", choices=["CONNECTED", "DISCONNECTED", "INITIALIZING"])
    s.add_argument("--limit", type=int)
    s.add_argument("--offset", type=int)
    s.set_defaults(func=cmd_sessions_list)

    s = g.add_parser("create")
    s.add_argument("--id")
    s.add_argument("--name")
    s.add_argument("--webhook", help="Webhook URL")
    s.add_argument("--proxy")
    s.add_argument("--no-auto-reconnect", action="store_true")
    s.set_defaults(func=cmd_sessions_create)

    s = g.add_parser("get"); s.add_argument("id"); s.set_defaults(func=cmd_sessions_get)

    s = g.add_parser("delete")
    s.add_argument("id")
    s.add_argument("--keep-auth", action="store_true")
    s.set_defaults(func=cmd_sessions_delete)

    s = g.add_parser("qr")
    s.add_argument("id")
    s.add_argument("--format", choices=["base64", "raw", "image"], default="base64")
    s.add_argument("--out", help="File to write when --format image")
    s.set_defaults(func=cmd_sessions_qr)

    s = g.add_parser("restart"); s.add_argument("id"); s.set_defaults(func=cmd_sessions_restart)
    s = g.add_parser("logout"); s.add_argument("id"); s.set_defaults(func=cmd_sessions_logout)


def _add_send(sub):
    g = sub.add_parser("send", help="Send a message").add_subparsers(dest="action", required=True)

    s = g.add_parser("text")
    s.add_argument("phone"); s.add_argument("body")
    s.add_argument("--quoted", help="Quoted message id")
    s.add_argument("--mention", action="append", help="Phone to mention (repeatable)")
    s.set_defaults(func=cmd_send_text)

    s = g.add_parser("image")
    s.add_argument("phone")
    src = s.add_mutually_exclusive_group(required=True)
    src.add_argument("--url"); src.add_argument("--file"); src.add_argument("--base64")
    s.add_argument("--mimetype"); s.add_argument("--filename"); s.add_argument("--caption")
    s.set_defaults(func=cmd_send_image)

    s = g.add_parser("document")
    s.add_argument("phone")
    src = s.add_mutually_exclusive_group(required=True)
    src.add_argument("--url"); src.add_argument("--file"); src.add_argument("--base64")
    s.add_argument("--mimetype"); s.add_argument("--filename"); s.add_argument("--caption")
    s.set_defaults(func=cmd_send_document)

    s = g.add_parser("location")
    s.add_argument("phone")
    s.add_argument("--lat", type=float, required=True)
    s.add_argument("--lng", type=float, required=True)
    s.add_argument("--name"); s.add_argument("--address")
    s.set_defaults(func=cmd_send_location)

    s = g.add_parser("contact")
    s.add_argument("phone")
    s.add_argument("--name", required=True)
    s.add_argument("--contact-phone", required=True)
    s.set_defaults(func=cmd_send_contact)

    s = g.add_parser("buttons")
    s.add_argument("phone"); s.add_argument("body")
    s.add_argument("--button", action="append", type=_parse_pair, required=True,
                   metavar="id:text", help="Button id:text (repeatable)")
    s.add_argument("--footer")
    s.set_defaults(func=cmd_send_buttons)

    s = g.add_parser("list")
    s.add_argument("phone"); s.add_argument("body")
    s.add_argument("--button-text", required=True)
    s.add_argument("--sections", required=True, help="JSON sections array, inline or @file.json")
    s.add_argument("--footer")
    s.set_defaults(func=cmd_send_list)


def _add_messages(sub):
    g = sub.add_parser("messages", help="Read/manage messages").add_subparsers(dest="action", required=True)

    s = g.add_parser("list")
    s.add_argument("phone")
    s.add_argument("--limit", type=int); s.add_argument("--before"); s.add_argument("--after")
    s.add_argument("--type")
    s.set_defaults(func=cmd_messages_list)

    s = g.add_parser("get"); s.add_argument("message_id"); s.set_defaults(func=cmd_messages_get)

    s = g.add_parser("delete")
    s.add_argument("message_id")
    s.add_argument("--no-for-everyone", action="store_true",
                   help="Delete only for me (default deletes for everyone)")
    s.set_defaults(func=cmd_messages_delete)

    s = g.add_parser("react")
    s.add_argument("message_id"); s.add_argument("emoji")
    s.set_defaults(func=cmd_messages_react)


def _add_contacts(sub):
    g = sub.add_parser("contacts", help="Contacts").add_subparsers(dest="action", required=True)
    g.add_parser("list").set_defaults(func=cmd_contacts_list)
    s = g.add_parser("get"); s.add_argument("phone"); s.set_defaults(func=cmd_contacts_get)
    s = g.add_parser("exists"); s.add_argument("phone"); s.set_defaults(func=cmd_contacts_exists)
    s = g.add_parser("block"); s.add_argument("phone"); s.set_defaults(func=cmd_contacts_block)
    s = g.add_parser("unblock"); s.add_argument("phone"); s.set_defaults(func=cmd_contacts_unblock)


def _add_groups(sub):
    g = sub.add_parser("groups", help="Groups").add_subparsers(dest="action", required=True)
    g.add_parser("list").set_defaults(func=cmd_groups_list)

    s = g.add_parser("create")
    s.add_argument("--name", required=True)
    s.add_argument("--participant", action="append", required=True, help="Repeatable")
    s.set_defaults(func=cmd_groups_create)

    s = g.add_parser("get"); s.add_argument("group_id"); s.set_defaults(func=cmd_groups_get)

    s = g.add_parser("update")
    s.add_argument("group_id"); s.add_argument("--name"); s.add_argument("--description")
    s.set_defaults(func=cmd_groups_update)

    s = g.add_parser("leave"); s.add_argument("group_id"); s.set_defaults(func=cmd_groups_leave)

    for action, fn in [("add", cmd_groups_add), ("remove", cmd_groups_remove),
                       ("promote", cmd_groups_promote), ("demote", cmd_groups_demote)]:
        s = g.add_parser(action)
        s.add_argument("group_id")
        s.add_argument("--participant", action="append", required=True, help="Repeatable")
        s.set_defaults(func=fn)

    s = g.add_parser("invite-code"); s.add_argument("group_id"); s.set_defaults(func=cmd_groups_invite_code)
    s = g.add_parser("revoke-invite"); s.add_argument("group_id"); s.set_defaults(func=cmd_groups_revoke_invite)


def _add_webhooks(sub):
    g = sub.add_parser("webhooks", help="Webhooks").add_subparsers(dest="action", required=True)
    g.add_parser("list").set_defaults(func=cmd_webhooks_list)

    s = g.add_parser("create")
    s.add_argument("--url", required=True)
    s.add_argument("--event", action="append", required=True, help="Event name (repeatable)")
    s.add_argument("--header", action="append", type=_parse_pair, metavar="Key:Value")
    s.add_argument("--secret")
    s.set_defaults(func=cmd_webhooks_create)

    s = g.add_parser("get"); s.add_argument("webhook_id"); s.set_defaults(func=cmd_webhooks_get)

    s = g.add_parser("update")
    s.add_argument("webhook_id")
    s.add_argument("--event", action="append")
    flip = s.add_mutually_exclusive_group()
    flip.add_argument("--enable", action="store_true")
    flip.add_argument("--disable", action="store_true")
    s.set_defaults(func=cmd_webhooks_update)

    s = g.add_parser("delete"); s.add_argument("webhook_id"); s.set_defaults(func=cmd_webhooks_delete)

    s = g.add_parser("logs"); s.add_argument("webhook_id"); s.add_argument("--limit", type=int)
    s.set_defaults(func=cmd_webhooks_logs)

    s = g.add_parser("test"); s.add_argument("webhook_id"); s.set_defaults(func=cmd_webhooks_test)


def _add_keys(sub):
    g = sub.add_parser("keys", help="API keys").add_subparsers(dest="action", required=True)
    g.add_parser("list").set_defaults(func=cmd_keys_list)

    s = g.add_parser("create")
    s.add_argument("--name", required=True)
    s.add_argument("--permission", action="append", help="Repeatable, e.g. messages:write")
    s.add_argument("--session-access", action="append", help="Repeatable session id or *")
    s.add_argument("--rate-limit", type=int)
    s.add_argument("--expires-at", help="ISO 8601 timestamp")
    s.set_defaults(func=cmd_keys_create)

    s = g.add_parser("delete"); s.add_argument("key_id"); s.set_defaults(func=cmd_keys_delete)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    client = Client(args.base_url, args.api_key, timeout=args.timeout)
    try:
        args.func(client, args)
    except ApiError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
