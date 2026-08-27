---
name: status
description: Show the jobforge streak, what is due, and which required element keeps breaking across patterns. Use for /jobforge:status, "what's due", "how's my streak".
---

# Status

Read `rep-log.md` and `bank.md`. Nothing else.

Report, in this order and nothing more:

1. Streak, and whether today is logged. A day counts only if the minutes cell has a digit and does
   not say `MISSED`; the day boundary is 3am.
2. What is due — pattern and how many days overdue, Tier A first.
3. **The element histogram.** Count `missing` element ids across the last 60 days of rows. Name the
   top one with the count and the patterns it appeared under.

That third line is the point of the whole system. `base-case` missing on five structurally unrelated
patterns is a fact no per-problem tracker can produce, and it names what to fix.

Then stop. No encouragement, no plan for the week, nothing about the resume or the pipeline.
