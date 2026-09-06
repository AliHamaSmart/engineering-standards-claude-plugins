#!/usr/bin/env python3
"""Contract tests for the engineering-standards hook scripts.

Each script is invoked the way the harness invokes it — a JSON payload on
stdin, a decision on stdout — so these test the actual contract rather than
internal functions. Standard library only: the plugin promises no dependencies
beyond python3, and its own tests must honour that.

Run: python3 tests/test_hooks.py
"""

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / (
    "plugins/engineering-standards/hooks/scripts"
)


def run_hook(script, payload):
    """Invoke a hook with a payload; return (stdout, exit code)."""
    text = payload if isinstance(payload, str) else json.dumps(payload)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script)],
        input=text,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout.strip(), result.returncode


def write_payload(path, content):
    return {"tool_name": "Write", "tool_input": {"file_path": path, "content": content}}


def lines_of(count):
    return "\n".join(f"const x{i} = {i};" for i in range(count))


def decision(stdout):
    """The permissionDecision in a hook's output, or None when silent."""
    if not stdout:
        return None
    return json.loads(stdout)["hookSpecificOutput"].get("permissionDecision")


class PreWriteSizeGuard(unittest.TestCase):
    SCRIPT = "pre_write_guard.py"

    def test_blocks_source_file_over_limit(self):
        out, code = run_hook(self.SCRIPT, write_payload("/x/src/a.ts", lines_of(600)))
        self.assertEqual(decision(out), "deny")
        self.assertEqual(code, 0)
        self.assertIn("550", out)

    def test_allows_source_file_at_limit(self):
        out, _ = run_hook(self.SCRIPT, write_payload("/x/src/a.ts", lines_of(550)))
        self.assertEqual(out, "")

    def test_allows_long_markdown(self):
        out, _ = run_hook(self.SCRIPT, write_payload("/x/docs/big.md", lines_of(900)))
        self.assertEqual(out, "", "docs are not source and must not be blocked")

    def test_allows_long_migration(self):
        out, _ = run_hook(self.SCRIPT, write_payload("db/migrations/001.py", lines_of(900)))
        self.assertEqual(out, "", "migrations are legitimately long")

    def test_allows_long_lockfile(self):
        out, _ = run_hook(self.SCRIPT, write_payload("package-lock.json", lines_of(9000)))
        self.assertEqual(out, "")


class PreWriteSecretGuard(unittest.TestCase):
    SCRIPT = "pre_write_guard.py"

    def assert_blocked(self, path, content):
        out, _ = run_hook(self.SCRIPT, write_payload(path, content))
        self.assertEqual(decision(out), "deny", f"should have blocked: {content[:60]}")

    def assert_allowed(self, path, content):
        out, _ = run_hook(self.SCRIPT, write_payload(path, content))
        self.assertEqual(out, "", f"should have allowed: {content[:60]}")

    def test_blocks_aws_access_key(self):
        self.assert_blocked("/x/src/a.ts", 'const k = "AKIAQ7RZBM4XKPLDW2VC";')

    def test_blocks_private_key_block(self):
        self.assert_blocked("/x/src/a.go", "-----BEGIN EC PRIVATE KEY-----")

    def test_blocks_github_token(self):
        token = "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        self.assert_blocked("/x/src/a.js", f'const t = "{token}";')

    def test_blocks_literal_password(self):
        self.assert_blocked("/x/src/a.py", 'password = "hunter2supersecret"')

    def test_blocks_secret_in_edit_new_string(self):
        payload = {
            "tool_name": "Edit",
            "tool_input": {"file_path": "/x/a.py", "new_string": 'api_key = "k9Xm2Qp7Lw4Rt8Zn"'},
        }
        out, _ = run_hook(self.SCRIPT, payload)
        self.assertEqual(decision(out), "deny")

    def test_blocks_secret_in_multiedit(self):
        payload = {
            "tool_name": "MultiEdit",
            "tool_input": {
                "file_path": "/x/a.py",
                "edits": [{"new_string": 'token = "aB3dE5fG7hJ9kL1mN3pQ"'}],
            },
        }
        out, _ = run_hook(self.SCRIPT, payload)
        self.assertEqual(decision(out), "deny")

    def test_allows_environment_lookup(self):
        self.assert_allowed("/x/src/a.py", 'password = os.environ["DB_PASSWORD"]')

    def test_allows_secret_manager_reference(self):
        self.assert_allowed("/x/src/a.ts", 'const password = await vault.read("db/pw");')

    def test_allows_env_example_file(self):
        self.assert_allowed("/x/.env.example", "API_KEY=sk-1234567890abcdefghij1234567890abcd")

    def test_allows_identifier_named_secret(self):
        self.assert_allowed("/x/src/a.ts", 'const secretName = "billing-cred-ref";')

    def test_allows_documented_placeholder(self):
        self.assert_allowed("/x/src/a.py", 'password = "your-password-here"')


class PostWriteCheck(unittest.TestCase):
    SCRIPT = "post_write_check.py"

    def check_file(self, name, count):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / name
            path.write_text(lines_of(count))
            payload = {"tool_name": "Edit", "tool_input": {"file_path": str(path)}}
            return run_hook(self.SCRIPT, payload)[0]

    def test_reports_over_hard_limit(self):
        out = self.check_file("big.ts", 600)
        self.assertIn("over the 550-line hard limit", out)

    def test_reports_advisory_below_limit(self):
        out = self.check_file("mid.ts", 480)
        self.assertIn("approaching", out)

    def test_silent_for_small_file(self):
        self.assertEqual(self.check_file("ok.ts", 10), "")

    def test_silent_for_missing_file(self):
        payload = {"tool_name": "Edit", "tool_input": {"file_path": "/nonexistent/x.ts"}}
        self.assertEqual(run_hook(self.SCRIPT, payload)[0], "")


class SessionStart(unittest.TestCase):
    def test_injects_digest(self):
        out, code = run_hook("session_standards.py", {"source": "startup"})
        payload = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(payload["hookEventName"], "SessionStart")
        self.assertIn("550", payload["additionalContext"])
        self.assertEqual(code, 0)


class FailOpen(unittest.TestCase):
    """A broken guard must never break the session."""

    CASES = ["pre_write_guard.py", "post_write_check.py", "session_standards.py"]

    def test_malformed_json_exits_zero(self):
        for script in self.CASES:
            with self.subTest(script=script):
                self.assertEqual(run_hook(script, "not json at all")[1], 0)

    def test_empty_stdin_exits_zero(self):
        for script in self.CASES:
            with self.subTest(script=script):
                self.assertEqual(run_hook(script, "")[1], 0)

    def test_missing_tool_input_exits_zero(self):
        for script in self.CASES:
            with self.subTest(script=script):
                self.assertEqual(run_hook(script, {"tool_name": "Write"})[1], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
