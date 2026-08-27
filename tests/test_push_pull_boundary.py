#!/usr/bin/env python3
"""The PUSH/PULL line, enforced as a test.

If the SessionStart hook ever learns the name of a second state file, this fails. That is the
whole point: the banner is allowed to talk about the daily drill and nothing else, and the
enforcement has to survive a future contributor who thinks one more line would be helpful.
"""

import pathlib
import re
import unittest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "hooks" / "drill-banner.py"
FORBIDDEN = [
    "resume",
    "targets.md",
    "profile",
    "bank.md",
    "interviews",
    "linkedin",
    "applications",
    "cover-letter",
]


class PushPullBoundary(unittest.TestCase):
    def setUp(self):
        self.src = HOOK.read_text(encoding="utf-8")
        self.code = "\n".join(
            line for line in self.src.splitlines() if not line.lstrip().startswith("#")
        )
        # Strip the module docstring so prose about the boundary is not mistaken for a code path.
        self.code = re.sub(r'^"""(?:.|\n)*?"""', "", self.code.strip(), count=1)

    def test_no_second_filename(self):
        for word in FORBIDDEN:
            self.assertNotIn(word, self.code.lower(), f"hook references {word!r}")

    def test_only_one_markdown_filename(self):
        names = set(re.findall(r'"[^"]*\.(?:md|json|ya?ml|txt)"', self.code))
        self.assertEqual(names, {'"rep-log.md"'}, f"hook names extra files: {names}")

    def test_single_open_call(self):
        self.assertEqual(len(re.findall(r"\bopen\(", self.code)), 1)

    def test_single_path_producer(self):
        self.assertEqual(len(re.findall(r"os\.path\.join\(", self.code)), 1)

    def test_no_network(self):
        for mod in ("requests", "urllib", "http.client", "socket", "subprocess"):
            self.assertNotIn(mod, self.code)


if __name__ == "__main__":
    unittest.main()
