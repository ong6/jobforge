# State schema

Everything jobforge remembers lives in `$JOBFORGE_HOME` (default `~/jobforge/`) as markdown you can
read, edit and delete. No database, no plugin-private directory, no telemetry.

```
$JOBFORGE_HOME/
  rep-log.md        one row per practice day — the only file the SessionStart hook can read
  bank.md           one append-only row per graded rep: pattern, verdict, missing element, due date
  interviews/       one file per real or mock interview you sat
```

## Element ids — the shared vocabulary

Grading, the bank, and the interview schema all speak these ids. They are **global, not
per-pattern**, and that is the point: after sixty days the bank can show that `base-case` was the
missing element on five structurally unrelated patterns.

| id | The probe it answers |
|---|---|
| `problem-restated` | Did you restate the problem and its return shape before planning? |
| `discriminator` | Did you name the property that selects this pattern, not just the pattern? |
| `state-definition` | Is the thing being tracked defined exactly — index, count, set, table cell? |
| `invariant` | What is true at every step, and what restores it when it breaks? |
| `base-case` | Which entries are seeded, with what value, before the loop runs? |
| `transition` | Is the recurrence or update rule stated as a formula, not "then I update it"? |
| `iteration-order` | Why this order — what does each step depend on already being computed? |
| `boundary-update` | How does each pointer, window edge or bound move, and why does it terminate? |
| `termination` | What ends the loop or recursion, and why can it not run forever? |
| `dedup` | How are repeats, revisits or already-seen states excluded? |
| `complexity-target` | Was a time and space target stated before coding, with the brute force named? |

A pattern entry in `content/patterns/` lists the subset it requires as
`required_elements: [state-definition, base-case, transition, iteration-order]`.

## Verdicts

| verdict | Means | Next due |
|---|---|---|
| `failed` | Wrong pattern, or a required element missing | +3 days |
| `half` | Right pattern, every element present but one or more vague | +3 days |
| `coded` | Plan complete and the code ran | +14 days |
| `named-clean` | Plan complete on first statement, no prompting | +14 days |

Due dates are written **into the row at grading time**. There is no scheduler and no queue file —
what is due is recomputed by reading the bank, so there is nothing to desynchronise.

## `bank.md` row

Append-only narrative. Pipe table, one row per graded rep. The notes cell is prose on purpose: a
`status:` enum would throw away the part that matters.

```
| date | pattern | verdict | missing | due | notes |
|---|---|---|---|---|---|
| 2026-08-27 | monotonic-stack | half | iteration-order | 2026-08-30 | proposed a stack of end times, needed a min-heap; said O(n), it was O(n log n). Regression from named-clean 08-19. |
```

- `missing` holds one or more element ids, comma-separated, or `-`.
- Never write a paraphrase of the problem here. Pattern, verdict, element, date, and what broke in
  your reasoning. Nothing that reconstructs a problem statement.

## `rep-log.md` row

One row per day, plus the only two settings the banner needs. The hook reads this file and nothing
else — target date lives in this file's frontmatter precisely so the hook never needs a second open.

```
---
target_date: 2026-10-15
tone: neutral        # neutral | blunt
---

| date | minutes | reps | notes |
|---|---|---|---|
| 2026-08-27 | 24 | 3 | two-pointers, sliding-window, dp-1d |
| 2026-08-26 | MISSED | 0 | travel |
```

Streak parsing, narrowed by two real bugs:

- A day counts only if the **minutes cell** contains a digit and does not contain `MISSED`. Scan the
  whole row and a placeholder that merely mentions a date counts as a rep, and a notes cell saying
  "MISSED the follow-up question" breaks a live streak.
- **Day boundary is 3am local.** Any hook or stamp that writes a date uses the same offset.

## `interviews/<date>-<company-slug>.md`

The interview you actually sat, as first-class data. Frontmatter is machine-read by the bridge.

```yaml
---
date: 2026-09-14
kind: real            # real | mock
round: phone-screen   # phone-screen | onsite | final | take-home
outcome: rejected     # passed | rejected | pending | withdrawn
asked:
  - pattern: monotonic-stack
    result: failed        # solved | partial | failed
    broke_on: [iteration-order, complexity-target]
  - pattern: graph-bfs
    result: solved
    broke_on: []
---
```

Free prose below the frontmatter is yours. The company name is a slug you choose and never leaves
your disk.

## The bridge

Every `broke_on` element in an interview file re-enters the review queue: `/jobforge:interview-debrief` appends one
bank row per failed question with verdict `failed`, the interview's date, the element ids from
`broke_on`, and a due date three days out. A real-interview failure is scheduled exactly like a
practice failure, because it is better evidence than one.
