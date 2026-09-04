#!/usr/bin/env python3
"""PostToolUse check: re-count the file on disk after it was written.

The pre-write guard can only see the text of one call. Edits accumulate, so the
authoritative count is the file itself, after the fact. This never blocks — the
write already happened; it hands Claude the fact so the split happens now
rather than three edits later.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hooklib  # noqa: E402


def count_lines(path):
    """Lines on disk, or None if unreadable."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return None


def verdict(count, path):
    """Note for Claude when the file crossed a threshold, else None."""
    if count > hooklib.MAX_FILE_LINES:
        return (
            f"engineering-standards: {path} is now {count} lines, over the "
            f"{hooklib.MAX_FILE_LINES}-line hard limit. Split it by responsibility "
            "before moving on to anything else — do not defer this to a later change."
        )
    if count > hooklib.ADVISORY_FILE_LINES:
        return (
            f"engineering-standards: {path} is at {count} lines, approaching the "
            f"{hooklib.MAX_FILE_LINES}-line limit. Plan the split point now, while "
            "the responsibilities are still easy to separate."
        )
    return None


def main():
    payload = hooklib.read_payload()
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not hooklib.is_size_checked(path):
        return

    count = count_lines(path)
    if count is None:
        return

    note = verdict(count, path)
    if note:
        hooklib.add_context("PostToolUse", note)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # fail open
