#!/usr/bin/env python3
"""SessionStart banner for the jobforge daily drill.

PUSH/PULL BOUNDARY — READ BEFORE EDITING.

This hook is the only jobforge surface that speaks before the user does, and the daily drill is the
only thing it is allowed to speak about. The enforcement is not a convention: `rep_log_path()` is
the single function in this file that produces a path, it appends one hard-coded filename, and
`_read()` refuses any path that is not the one it returns. There is no code path from here to the
resume, the target list, the profile, or even the bank. The hook cannot nag about them because it
cannot open them.

Adding a second file here is the most expensive change available to this design. A banner that can
also say "your LinkedIn is stale" is a banner the user learns to skim, and the drill loop dies with
it. `tests/test_push_pull_boundary.py` fails the build if this file learns a second filename.

Output: one short block on stdout, exit 0. Silent (no output) when there is nothing actionable.
"""

import datetime
import os
import re
import sys

REP_LOG_FILENAME = "rep-log.md"  # the only filename this process may ever open
DAY_BOUNDARY_HOUR = 3  # a rep logged at 1am belongs to the previous day
FLOOR_MINUTES = 20


def jobforge_home() -> str:
    return os.path.expanduser(os.environ.get("JOBFORGE_HOME") or "~/jobforge")


def rep_log_path() -> str:
    """The only path-producing function in this module."""
    return os.path.join(jobforge_home(), REP_LOG_FILENAME)


def _read() -> str:
    path = rep_log_path()
    if os.path.basename(path) != REP_LOG_FILENAME:
        return ""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def today(now: datetime.datetime | None = None) -> datetime.date:
    now = now or datetime.datetime.now()
    return (now - datetime.timedelta(hours=DAY_BOUNDARY_HOUR)).date()


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.split("#")[0].strip().strip("'\"")
    return out


ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$")


def parse_rows(text: str) -> list[dict]:
    """Rows of the rep log, newest first. Only the minutes cell decides whether a day counts."""
    rows = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group("cells").split("|")]
        if len(cells) < 2:
            continue
        date_cell, minutes_cell = cells[0], cells[1]
        try:
            date = datetime.date.fromisoformat(date_cell)
        except ValueError:
            continue  # header row, separator row, or a note that merely mentions a date
        counted = bool(re.search(r"\d", minutes_cell)) and "MISSED" not in minutes_cell.upper()
        minutes = 0
        if counted:
            digits = re.search(r"\d+", minutes_cell)
            minutes = int(digits.group()) if digits else 0
        rows.append(
            {
                "date": date,
                "counted": counted,
                "minutes": minutes,
                "notes": cells[3] if len(cells) > 3 else "",
                "reps": cells[2] if len(cells) > 2 else "",
            }
        )
    rows.sort(key=lambda r: r["date"], reverse=True)
    return rows


def streak(rows: list[dict], as_of: datetime.date) -> int:
    """Consecutive counted days ending today or yesterday. A gap of one full day ends it."""
    by_date = {r["date"]: r for r in rows}
    day = as_of
    if not (by_date.get(day) or {}).get("counted"):
        day = as_of - datetime.timedelta(days=1)
        if not (by_date.get(day) or {}).get("counted"):
            return 0
    n = 0
    while (by_date.get(day) or {}).get("counted"):
        n += 1
        day -= datetime.timedelta(days=1)
    return n


def rotating_fact(rows: list[dict], as_of: datetime.date, days_left: int | None) -> str:
    """One specific fact, rotated by day so the banner does not become wallpaper."""
    counted = [r for r in rows if r["counted"]]
    facts = []
    if days_left is not None:
        facts.append(f"{days_left} days to your target date.")
    if counted:
        total = sum(r["minutes"] for r in counted)
        facts.append(f"{len(counted)} days logged, {total} minutes total.")
        last = counted[0]
        if last["notes"]:
            facts.append(f"Last session: {last['notes']}.")
        median = sorted(r["minutes"] for r in counted)[len(counted) // 2]
        facts.append(f"Median session {median} min — the floor is {FLOOR_MINUTES}.")
    missed = [r for r in rows if not r["counted"]]
    if missed:
        facts.append(f"Last missed day: {missed[0]['date'].isoformat()}. No make-up doubling.")
    if not facts:
        return ""
    return facts[as_of.toordinal() % len(facts)]


def banner(text: str, as_of: datetime.date) -> str:
    if not text.strip():
        return ""  # not set up; say nothing rather than sell something
    meta = parse_frontmatter(text)
    days_left = None
    target = meta.get("target_date")
    if target:
        try:
            days_left = (datetime.date.fromisoformat(target) - as_of).days
        except ValueError:
            days_left = None
    if days_left is not None and days_left < 0:
        return ""  # time-boxed: past the target date the tool stops talking

    rows = parse_rows(text)
    if any(r["date"] == as_of and r["counted"] for r in rows):
        return ""  # already drilled today; never fire on a logged day

    n = streak(rows, as_of)
    blunt = meta.get("tone") == "blunt"
    if n == 0:
        head = "No streak. Start one: /jobforge:drill" if blunt else f"/jobforge:drill — {FLOOR_MINUTES} minutes restarts the streak."
    else:
        head = f"{n}-day streak, not yet logged today. /jobforge:drill"
    fact = rotating_fact(rows, as_of, days_left)
    return f"🔨 {head}\n   {fact}".rstrip()


def main() -> int:
    out = banner(_read(), today())
    if out:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
