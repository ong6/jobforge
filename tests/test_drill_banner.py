#!/usr/bin/env python3
"""Banner behaviour, including the two parsing bugs that narrowed the streak rule."""

import datetime
import importlib.util
import pathlib
import unittest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "hooks" / "drill-banner.py"
_spec = importlib.util.spec_from_file_location("drill_banner", HOOK)
db = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(db)

HEAD = "---\ntarget_date: 2026-10-15\ntone: neutral\n---\n\n| date | minutes | reps | notes |\n|---|---|---|---|\n"
AS_OF = datetime.date(2026, 8, 27)


def log(*rows):
    return HEAD + "".join(rows)


class Streak(unittest.TestCase):
    def test_counts_consecutive_days(self):
        rows = db.parse_rows(
            log(
                "| 2026-08-26 | 24 | 3 | dp-1d |\n",
                "| 2026-08-25 | 31 | 4 | graphs |\n",
                "| 2026-08-24 | 20 | 2 | heaps |\n",
            )
        )
        self.assertEqual(db.streak(rows, AS_OF), 3)

    def test_missed_minutes_cell_breaks_streak(self):
        rows = db.parse_rows(
            log("| 2026-08-26 | MISSED | 0 | travel |\n", "| 2026-08-25 | 31 | 4 | graphs |\n")
        )
        self.assertEqual(db.streak(rows, AS_OF), 0)

    def test_missed_in_notes_does_not_break_streak(self):
        """Bug 2: 'MISSED' in a notes cell about a missed question once killed a live streak."""
        rows = db.parse_rows(
            log(
                "| 2026-08-26 | 24 | 3 | MISSED the follow-up on iteration order |\n",
                "| 2026-08-25 | 31 | 4 | graphs |\n",
            )
        )
        self.assertEqual(db.streak(rows, AS_OF), 2)

    def test_placeholder_row_without_digits_does_not_count(self):
        """Bug 1: a placeholder row that merely mentioned a date once counted as a rep."""
        rows = db.parse_rows(log("| 2026-08-26 | - | - | plan to restart on 2026-08-27 |\n"))
        self.assertEqual(db.streak(rows, AS_OF), 0)


class Banner(unittest.TestCase):
    def test_silent_when_today_already_logged(self):
        self.assertEqual(db.banner(log("| 2026-08-27 | 22 | 3 | dp |\n"), AS_OF), "")

    def test_silent_past_target_date(self):
        text = log("| 2026-08-26 | 22 | 3 | dp |\n").replace("2026-10-15", "2026-08-01")
        self.assertEqual(db.banner(text, AS_OF), "")

    def test_silent_when_not_installed(self):
        self.assertEqual(db.banner("", AS_OF), "")

    def test_fires_with_streak_and_one_fact(self):
        out = db.banner(log("| 2026-08-26 | 24 | 3 | dp-1d |\n"), AS_OF)
        self.assertIn("/jobforge:drill", out)
        self.assertIn("1-day streak", out)
        self.assertLessEqual(len(out.splitlines()), 2)

    def test_fact_rotates_across_days(self):
        text = log(
            "| 2026-08-26 | 24 | 3 | dp-1d |\n",
            "| 2026-08-24 | MISSED | 0 | travel |\n",
        )
        seen = {
            db.rotating_fact(db.parse_rows(text), AS_OF + datetime.timedelta(days=d), 10)
            for d in range(4)
        }
        self.assertGreater(len(seen), 1)


class DayBoundary(unittest.TestCase):
    def test_two_am_belongs_to_previous_day(self):
        self.assertEqual(db.today(datetime.datetime(2026, 8, 27, 2, 0)), datetime.date(2026, 8, 26))
        self.assertEqual(db.today(datetime.datetime(2026, 8, 27, 3, 1)), datetime.date(2026, 8, 27))


if __name__ == "__main__":
    unittest.main()
