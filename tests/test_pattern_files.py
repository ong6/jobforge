#!/usr/bin/env python3
"""The taxonomy is a grading contract, so it gets validated like one.

Every `required_elements` id must exist in the schema's global vocabulary, or the drill will grade
against an element nothing defines and the bank will accumulate ids that `/jobforge:status` cannot
count.
"""

import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "content" / "patterns"
SCHEMA = ROOT / "docs" / "state-schema.md"

EXPECTED_IDS = {
    "two-pointers", "sliding-window", "binary-search-on-answer", "hashing", "prefix-sum",
    "monotonic-stack", "heap-top-k", "intervals", "linked-list-pointers", "graph-bfs",
    "graph-dfs", "topological-sort", "union-find", "backtracking", "dp-1d", "dp-2d",
}
REQUIRED_SECTIONS = [
    "## Discriminator",
    "## Confusable with",
    "## Required elements",
    "## Complexity",
    "## Failure modes",
    "## Template",
]


def vocabulary() -> set:
    text = SCHEMA.read_text(encoding="utf-8")
    table = text.split("## Element ids")[1].split("## Verdicts")[0]
    return set(re.findall(r"^\| `([a-z-]+)` \|", table, re.M))


def frontmatter(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    block = text.split("---", 2)[1]
    out = {}
    for line in block.strip().splitlines():
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


class PatternFiles(unittest.TestCase):
    def setUp(self):
        self.files = sorted(p for p in PATTERNS.glob("*.md") if p.name != "README.md")
        self.vocab = vocabulary()

    def test_vocabulary_is_not_empty(self):
        self.assertGreaterEqual(len(self.vocab), 8)

    def test_every_expected_pattern_exists(self):
        self.assertEqual({p.stem for p in self.files}, EXPECTED_IDS)

    def test_frontmatter_contract(self):
        for path in self.files:
            fm = frontmatter(path)
            with self.subTest(pattern=path.stem):
                self.assertEqual(fm.get("id"), path.stem)
                self.assertIn(fm.get("tier"), {"A", "B"})
                ids = [i.strip() for i in fm["required_elements"].strip("[]").split(",")]
                self.assertGreaterEqual(len(ids), 3)
                for element in ids:
                    self.assertIn(element, self.vocab, f"{path.stem}: unknown element {element!r}")

    def test_required_sections_present(self):
        for path in self.files:
            body = path.read_text(encoding="utf-8")
            for section in REQUIRED_SECTIONS:
                with self.subTest(pattern=path.stem, section=section):
                    self.assertIn(section, body)

    def test_every_required_element_has_a_calibration_row(self):
        """The drill grades against the complete/vague columns. A missing row means no calibration."""
        for path in self.files:
            body = path.read_text(encoding="utf-8")
            table = body.split("## Required elements")[1].split("##")[0]
            for element in [i.strip() for i in frontmatter(path)["required_elements"].strip("[]").split(",")]:
                with self.subTest(pattern=path.stem, element=element):
                    self.assertIn(element, table)

    def test_index_lists_every_pattern(self):
        index = (PATTERNS / "README.md").read_text(encoding="utf-8")
        for pattern in EXPECTED_IDS:
            self.assertIn(pattern, index)


if __name__ == "__main__":
    unittest.main()
