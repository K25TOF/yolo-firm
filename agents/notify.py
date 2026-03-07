"""Pushover notification module for YOLO research operations.

Sends notifications to PO via Pushover API. Fails silently if keys
are not configured — notification is best-effort, never a blocker.

Usage:
    from notify import send_pushover
    send_pushover("Title", "Message body", priority=0)
"""

from __future__ import annotations

import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"


def send_pushover(title: str, message: str, priority: int = 0) -> bool:
    """Send a Pushover notification to PO.

    Args:
        title: Notification title.
        message: Notification body.
        priority: -1 (low), 0 (normal), 1 (high), 2 (emergency).

    Returns:
        True if sent successfully, False otherwise.
    """
    user_key = os.environ.get("PUSHOVER_USER_KEY", "")
    app_token = os.environ.get("PUSHOVER_APP_TOKEN", "")

    if not user_key or not app_token:
        logger.warning("Pushover keys not configured — skipping notification")
        return False

    params: dict[str, str | int] = {
        "token": app_token,
        "user": user_key,
        "title": title,
        "message": message,
        "priority": priority,
    }

    # Emergency priority requires retry and expire
    if priority == 2:
        params["retry"] = 30
        params["expire"] = 300

    try:
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(PUSHOVER_URL, data=data)
        with urllib.request.urlopen(req) as resp:
            resp.read()
        return True
    except Exception:
        logger.exception("Pushover notification failed")
        return False
