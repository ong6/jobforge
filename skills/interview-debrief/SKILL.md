---
name: interview-debrief
description: Record an interview you actually sat — real or mock — as structured data, then feed every question that broke back into the drill queue. Use for /jobforge:interview-debrief, "I just had an interview", "log my onsite", "that phone screen went badly"; not for practice reps, which /jobforge:drill grades.
---

# Interview debrief

An interview is the best evidence you will ever get about what you cannot do under pressure, and it
is normally thrown away — recalled as "it went badly" and never scheduled against. This records it
in the same vocabulary the drill grades in, and puts the failures back in the queue.

Run it the same day. Recall of *why* an answer broke decays within hours; recall of *that* it broke
does not, which is why unrecorded interviews turn into vague dread.

## 1. Take the account

Ask in this order and stop when you have it. Do not interrogate someone who has just been rejected.

- Date, round (`phone-screen` / `onsite` / `final` / `take-home`), real or mock.
- Outcome if known: `passed`, `rejected`, `pending`, `withdrawn`. `pending` is normal and gets
  updated later.
- Per question: what pattern it turned out to want, and whether they solved it, half-solved it, or
  did not.

Then the part that matters, per question that did not go cleanly:

> What did you say you were going to do, and what was wrong with it?

Map their answer onto element ids from [`../../docs/state-schema.md`](../../docs/state-schema.md).
Same vocabulary as the drill, so a failure here is comparable with a failure there. If nothing maps,
leave `broke_on: []` and put the reason in the prose. Do not force a fit.

## 2. Write the file

`$JOBFORGE_HOME/interviews/<date>-<slug>.md`, frontmatter exactly as the schema specifies. The
company slug is whatever the user calls it, stays on their disk, and is never transmitted.

Below the frontmatter, their own words. Never rewrite them, never summarise them into bullets.

## 3. The bridge

For every question with `result: failed` or `partial`, append one row to `bank.md`:

- `date` — the interview date, not today.
- `pattern` — the pattern the question wanted.
- `verdict` — `failed`.
- `missing` — the `broke_on` element ids.
- `due` — interview date + 3 days, the same interval a failed practice rep gets.
- notes — one line, from their account, marked as coming from an interview.

```
| 2026-09-14 | monotonic-stack | failed | iteration-order,complexity-target | 2026-09-17 | real interview, phone screen. Described a stack scan but never said which direction; quoted O(n) for an O(n log n) plan. |
```

A real failure is scheduled exactly like a practice failure. It is better evidence than a practice
failure, and treating it as a lesser signal is what leaves people failing the same question twice.

## 4. Close

Name the elements that now enter the queue and when. If any of them already appear in the bank from
practice, say so with the dates. That sentence — "this is the third time `base-case` has been the
thing" — is the reason the file exists.

Nothing about the resume, the pipeline, or what to apply to next. Those are other commands, and the
user did not ask for them.
