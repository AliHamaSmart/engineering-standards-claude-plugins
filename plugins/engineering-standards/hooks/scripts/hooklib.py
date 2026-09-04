"""Shared helpers for engineering-standards hooks.

Every hook fails OPEN: a malformed payload, a missing file, or an unexpected
error must never block the user's session. A broken guard is worse than no
guard, because it erodes trust in the whole plugin.
"""

import json
import re
import sys

MAX_FILE_LINES = 550
ADVISORY_FILE_LINES = 450

# The limits target hand-written source. Data, docs, generated output, and
# migrations are legitimately long; blocking them would train the user to
# distrust the hook.
_UNCHECKED_PATH = re.compile(
    r"(?i)("
    r"\.(md|mdx|json|ya?ml|toml|ini|csv|tsv|txt|svg|snap|lock|sql|ipynb)$"
    r"|\.min\.[a-z]+$"
    r"|(^|/)(migrations?|testdata|fixtures?|__mocks__|vendor|node_modules|dist|build)/"
    r"|(^|/)package-lock\.json$"
    r")"
)


def is_size_checked(path):
    """True when file-size limits apply to this path."""
    return bool(path) and not _UNCHECKED_PATH.search(path)


def read_payload():
    """Hook input as a dict; empty dict when anything is off."""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def _emit(payload):
    print(json.dumps(payload))


def deny(reason):
    """Block the pending tool call and tell Claude why."""
    _emit({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    })


def add_context(event, text):
    """Feed a note back to Claude without blocking anything."""
    _emit({
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": text,
        }
    })


def incoming_text(tool_input):
    """All text a Write/Edit/MultiEdit call would introduce."""
    parts = [tool_input.get("content"), tool_input.get("new_string")]
    for edit in tool_input.get("edits") or []:
        parts.append(edit.get("new_string"))
    return "\n".join(part for part in parts if part)
