# 🔨 jobforge

**Hard reps, easy job.** A Claude Code plugin that grades the plan you say out loud, not the code
you submit.

TODO(owner): personal voice paragraph goes here — why you built this, in your own words. Do not
let an agent write it.

## What it grades

Every mistake-classifier in this space fires on a rejected submission. That means none of them can
fire when you wrote correct code for the wrong reason, and none of them has any notion of a plan you
stated before typing.

jobforge asks for the plan first and grades that, against a required-elements checklist for the
pattern:

- Is the recurrence stated as a formula, or did you say "then I fill in the table"?
- Which cells are seeded, with what value, before the loop runs?
- Why that iteration order — what does each step need already computed?

Each element is marked **present**, **vague**, or **missing**, and a mark of *present* requires a
quotable span of your own words. "I'll build up the table" is a vague `transition`; it passes casual
listening, and it is the exact failure that shows up as a stall in an interview.

The element you missed is what gets scheduled. Miss `base-case` and the next rep is a different
pattern that also depends on seeding it, not the same problem again in three days.

## Interviews you actually sat are data

`/jobforge:interview-debrief` records a real interview as structured state: round, outcome, what was asked, which
pattern each question wanted, and which elements broke. It uses the same element vocabulary as
practice grading.

Every failed question is then appended to the review queue with a due date three days out, the same
interval a failed practice rep gets. A question you lost an onsite to is better evidence than a
question you fumbled alone at 11pm, and it is the one that normally gets thrown away as "that went
badly".

## One banner, one subject

A SessionStart hook prints one line when you have not drilled today. It reads `rep-log.md` and
nothing else — no code path to the resume, the target list, or the bank. That is enforced in
[`tests/test_push_pull_boundary.py`](tests/test_push_pull_boundary.py), which fails the build if the
hook learns a second filename.

The first time a banner can also say *your LinkedIn headline is stale*, it stops being an
instruction and becomes wallpaper. Everything else in this plugin waits to be asked.

The banner is silent on a day you already logged, silent past your target date, and silent if you
have not set it up.

## What it does not try to be

- **A submission capture tool.** A browser extension sits at the moment you hit submit and can
  interrupt you. A CLI agent only exists when you invoke it. If you want your accepted submissions
  auto-captured and FSRS-scheduled, use one of the extensions built for that; several are good.
- **A problem bank.** No problems ship with this repo. They are generated per session from a
  taxonomy entry, never from a problem title, and nothing generated is written to disk. The state
  files hold a pattern, a verdict, an element id and a date — never a paraphrase.
- **A grader of your code.** The bundled Python harness runs your solution so you can check it. The
  grade comes from the plan.

## Install

```
/plugin marketplace add ong6/jobforge
/plugin install jobforge
```

Then `/jobforge:setup`, which writes `~/jobforge/` from [`templates/`](templates/).

## Commands

| | |
|---|---|
| `/jobforge:drill` | One graded rep against a due pattern |
| `/jobforge:interview-debrief` | Record an interview and queue what broke |
| `/jobforge:status` | Streak, what is due, which element keeps breaking |
| `/jobforge:sysdesign` | Walk a reference design on a local Excalidraw canvas |
| `/jobforge:setup` | Create the state files and set a target date |
| `/jobforge:archive` | Stop. Past your target date, this is the intended ending. |

## Your data

Everything lives in `$JOBFORGE_HOME` (default `~/jobforge/`) as markdown you can read, edit and
delete with `rm -rf`. Not in a plugin-private directory — you should be able to destroy this on the
day you want it gone, without remembering a `--keep-data` flag.

No telemetry. There is no code in this plugin that sends anything anywhere, so there is no setting
to turn off.

**If your employer manages this machine, put `JOBFORGE_HOME` on a personal volume.** Taken together,
a resume, a target list, a departure date and a log of your technical weaknesses is a document that
could cost you your current job. A tool that knows you are leaving owes you that sentence.

## Tone

Default is `neutral`. Set `tone: blunt` in `rep-log.md` for the version with no cushioning. Blunt is
the mode every constant here was tuned under. It also reads as hostile to someone who did not ask
for it, which is why you have to ask.

## The constants are tunable and n=1

Three-day and fourteen-day intervals, the twenty-minute floor, the 3am day boundary, Tier A before
Tier B — all observed from one person's log over one job search, not derived from a study. They are
in `rep-log.md` frontmatter. Change them.

Two of them are worth keeping as they are. The twenty-minute floor, because a recognition rep costs
about a third of a solving rep per minute and that is what makes a bad day payable. And no make-up
doubling: a missed day costs one rep, a doubled make-up target costs the next three.

## Credit

The eight system-design reference designs, the coding test harness, the Excalidraw canvas and its
local server are derived from [`kirilxd/swe-interview-coach`](https://github.com/kirilxd/swe-interview-coach),
MIT licensed, and remain the clearest treatment of behavioural and system-design prep in a Claude
Code plugin. Attribution is preserved per file and in [`NOTICE`](NOTICE). Behavioural and
system-design rounds are that project's ground; if that is what you need, install it.

Not carried over: its `/coding-import` fallback to a third-party API mirror, which routed a user's
problem requests through someone else's server.

The pattern taxonomy, the grading mechanism, the hooks, the bank and the interview schema are new
here.

## Licence

MIT. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
