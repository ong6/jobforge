---
name: drill
description: Run a jobforge daily drill — generate a problem for a due pattern, grade the spoken plan against that pattern's required-elements checklist, and write the graded row with its next due date. Use for /jobforge:drill, "run my drill", "give me a rep"; not for mock interviews, resume work or interview debriefs.
---

# Drill

One rep: a generated problem, a plan stated out loud, a grade on the plan, a row written. Twenty
minutes is a complete session.

## What you may read

The drill sees `rep-log.md`, `bank.md`, and `content/patterns/`. It does not open the resume, the
target list, the interview files' prose, or anything else under `$JOBFORGE_HOME`. That is a tiering
rule, not a performance one: a tool that reads a résumé to pick a graph problem has no reason to,
and the user cannot audit what it never opened.

`$JOBFORGE_HOME` defaults to `~/jobforge`. If it does not exist, run setup from
[`../../templates/`](../../templates/) and stop.

## 1. Is there a rep today

Read the rep log's `target_date`. Past it, say so once and offer `/jobforge:archive`. A tool that outlives
its purpose is one the user uninstalls angry.

Already a counted row for today? Confirm the rep is done and offer a second one only if asked. Never
propose a double session to make up a missed day. Doubling is how streaks die twice: the missed day
costs one rep, the make-up target costs the next three.

## 2. Pick the pattern

Read `bank.md`. Compute what is due — any row whose `due` date is today or earlier and which has no
later row for the same pattern. No scheduler, no queue file; the due date lives in the row.

Selection order:

1. Overdue Tier A patterns, oldest due date first.
2. Overdue Tier B.
3. Patterns with no row at all, Tier A first.
4. Nothing due: the pattern with the most `failed`/`half` history in the last 30 days.

**Never the same pattern as the previous row in the log.** Interleaving builds discrimination.
Blocked practice builds a fluency illusion that reads as mastery and collapses in an interview,
which is the only place it is measured.

Announce the pattern only after grading. Naming it up front hands over the `discriminator` element,
which is one of the things being graded.

## 3. Generate the problem

Read `content/patterns/<id>.md`. Generate from the **discriminator**, never from a problem title.
Six rules, all enforced here:

1. The prompt is built from the taxonomy entry. A known problem's name never enters the generation
   context.
2. Re-skin to a domain the user works in. Non-infringing, and better prep than a puzzle about a
   robot in a grid.
3. Structural cues only. Never restate a known problem's setup in different words.
4. Similarity gate — before showing it, check whether the result is recognisable as a known problem.
   If it is, change the **structure**: what gets returned, a constraint that moves the complexity
   target, produce-versus-count. Renaming the variables is a copy.
5. Never persist a paraphrase. Nothing generated is written to disk. The bank stores pattern,
   verdict, missing elements, due date and a note about the reasoning.
6. If a reference solution is needed, write it fresh and run it through
   [`../../scripts/run-solution.sh`](../../scripts/run-solution.sh):
   `bash "${CLAUDE_PLUGIN_ROOT}/scripts/run-solution.sh" python <solution.py> <cases.json>`, where
   the cases file is `{"function": "<top-level fn>", "unordered": false, "cases": [{"args": [...],
   "expected": ...}]}` and both files live in a temp dir, never in `$JOBFORGE_HOME`. Standard
   algorithms are not copyrightable; editorial prose is, and none is reproduced.

Then ask for the plan, in words, before any code:

> Before you write anything: what are you going to do, and why that?

## 4. Grade the plan, not the code

This is the whole mechanism. Every other grader in this category fires on a judge rejection, which
means it cannot fire when the user wrote correct code for the wrong reason. This one grades the
sentence that came before the code.

For each id in the pattern's `required_elements`:

| Mark | Rule |
|---|---|
| **present** | You can quote the user's own words that state it, and the statement is specific enough to implement from. |
| **vague** | The user gestured at it. "I'll build up the table" is a vague `transition`. It sounds complete and is not. |
| **missing** | No quotable span. |

**The evidence rule: no quote, not present.** Write the quoted span next to each mark before
deciding the verdict. Grading from your impression of the conversation is how a grader drifts into
rewarding confidence.

Use the pattern file's "what a complete statement sounds like" / "what a vague statement sounds
like" columns as the calibration. They exist so this is repeatable across sessions, not a mood.

Verdict:

| | |
|---|---|
| Wrong pattern, or any element **missing** | `failed` |
| Right pattern, all present, one or more **vague** | `half` |
| All present, and the code ran | `coded` |
| All present on the first statement, no prompting | `named-clean` |

Then say which element broke, in one line, quoting them:

> `iteration-order` was missing. You said "then I fill in the table" — fill it in which direction,
> and what does each cell need already computed?

If a required element was missing, prompt for it and let them recover. The recovery does not change
the verdict. The verdict records what they produced unprompted, because that is what an interview
measures.

## 5. Write the rows

Append one row to `bank.md` in the schema's shape ([`../../docs/state-schema.md`](../../docs/state-schema.md)).
Compute `due` at grading time: `failed`/`half` → +3 days, `coded`/`named-clean` → +14 days. Both are
tunable in the rep log's frontmatter; both are generalised from one person's log and are not sacred.

The notes cell is narrative and append-only. Write what actually broke and what it regressed from:

> proposed a stack of end times, needed a min-heap; said O(n), it was O(n log n). Regression from
> named-clean 08-19.

An enum in that cell would discard the only part that reads usefully sixty days later.

Then append or update today's `rep-log.md` row: date, minutes, rep count, the patterns drilled.
Minutes must contain a digit or the day does not count. Day boundary is 3am.

## 6. Close

One line: verdict, the element that broke, when it is next due. Then stop. Do not summarise the
session, do not suggest the resume, do not mention anything outside the drill.

If the same element id has now failed on three or more structurally unrelated patterns, say that
once. It is the only cross-session claim worth interrupting for, and it is what the bank is for.
