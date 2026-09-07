#!/usr/bin/env python3
"""PreToolUse guard: block oversized files and hardcoded secrets before they land.

Two checks only, both deterministic. Function length and nesting depth need a
real parser per language — those stay with the linter that the
engineering-standards-ci skill configures (max-lines-per-function, max-depth).
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hooklib  # noqa: E402

SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "GitHub token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key"),
    (re.compile(r"sk-[A-Za-z0-9]{32,}"), "OpenAI-style secret key"),
    (
        # A leading \b would not fire on DB_PASSWORD or AWS_SECRET_ACCESS_KEY:
        # underscore is a word character, so there is no boundary after it. The
        # prefix class matches the namespace instead. Suffixes are deliberately
        # NOT allowed, which keeps identifiers like `secretName` out of scope.
        re.compile(
            r"""(?i)[a-z0-9_.\-]*"""
            r"""(secret[_-]?access[_-]?key|access[_-]?key|client[_-]?secret"""
            r"""|auth[_-]?token|api[_-]?key|private[_-]?key"""
            r"""|password|passwd|secret|token|credential)s?\s*"""
            r"""[:=]\s*["'][^"'\s]{12,}["']"""
        ),
        "credential assigned a literal value",
    ),
]

# Lines that clearly reference a secret without containing one.
PLACEHOLDER = re.compile(
    r"(?i)(process\.env|os\.environ|getenv|secrets?\.|vault|\$\{|\$\(|<[a-z_]+>"
    r"|your[_-]|example|changeme|placeholder|redacted|dummy|fake|sample|xxx+|\*{4,})"
)

SECRET_EXEMPT = re.compile(r"(?i)(\.example$|\.sample$|\.template$|/testdata/|/fixtures?/|/__mocks__/)")


def find_secret(text, path):
    """First (label, line) that looks like a real credential, else None."""
    if SECRET_EXEMPT.search(path or ""):
        return None
    for line in text.splitlines():
        if PLACEHOLDER.search(line):
            continue
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(line):
                return label, line.strip()[:120]
    return None


def oversized_write(tool_input, path):
    """Line count when this call writes a whole file over the limit, else None."""
    content = tool_input.get("content")
    if not content or not hooklib.is_size_checked(path):
        return None
    count = len(content.splitlines())
    return count if count > hooklib.MAX_FILE_LINES else None


def size_reason(count, path):
    return (
        f"Blocked by engineering-standards: this would write {count} lines to {path}, "
        f"over the {hooklib.MAX_FILE_LINES}-line hard limit.\n"
        "Plan the module split BEFORE writing — separate the file by responsibility "
        "(domain / application / edges), then write each part. "
        "Working-but-unmaintainable is a failed output, so do not retry this as one file."
    )


def secret_reason(label, snippet, path):
    return (
        f"Blocked by engineering-standards: {label} detected in content headed for {path}.\n"
        f"  {snippet}\n"
        "Secrets never go in source. Read it from the environment or a secret manager, "
        "and document the variable in .env.example instead."
    )


def main():
    payload = hooklib.read_payload()
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""

    count = oversized_write(tool_input, path)
    if count:
        hooklib.deny(size_reason(count, path))
        return

    found = find_secret(hooklib.incoming_text(tool_input), path)
    if found:
        hooklib.deny(secret_reason(found[0], found[1], path))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # fail open
