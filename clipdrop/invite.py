"""Channel invites: one line a server admin pastes in Discord so friends can add the channel in one click.

An invite is the channel's name, webhook link and upload limit packed into a code like
`clipmunk-invite:eyJu...`. Anyone with it can post to that channel, the same as with the webhook link,
so admins should only share it where they'd share the webhook.
"""
import base64
import json
import re

from . import share

PREFIX = "clipmunk-invite:"
# Base64 without "_" (Discord turns _text_ into italics), so "." stands in for it.
INVITE_RE = re.compile(r"clipmunk-invite:([A-Za-z0-9.\-]{20,})")


def make_invite(channel):
    data = {"n": channel["name"], "u": channel["url"], "l": float(channel.get("limit_mb") or 20)}
    raw = base64.urlsafe_b64encode(json.dumps(data, separators=(",", ":")).encode()).decode()
    return PREFIX + raw.rstrip("=").replace("_", ".")


def invite_message(channel):
    """What 'Copy invite' puts on the clipboard: ready to paste into Discord as-is."""
    return (f"Clipmunk invite for #{channel['name']}: copy this whole message, then open Clipmunk "
            f"`{make_invite(channel)}`")


def parse_invite(text):
    """The channel inside an invite found anywhere in `text`, or None if there isn't a valid one."""
    m = INVITE_RE.search(text or "")
    if not m:
        return None
    raw = m.group(1).replace(".", "_")
    try:
        data = json.loads(base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4)))
        name = str(data["n"]).strip().lstrip("#")[:40]
        url = str(data["u"]).strip()
        limit = float(data.get("l") or 20)
    except (ValueError, KeyError, TypeError):
        return None
    if not name or not share.is_webhook_url(url) or limit not in (20, 50, 100):
        return None
    return {"name": name, "url": url, "limit_mb": limit}
