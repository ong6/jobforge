---
name: setup
description: Create the jobforge state files in $JOBFORGE_HOME and set a target date. Use for /jobforge:setup, "set up jobforge", or when a drill finds no state directory.
disable-model-invocation: false
---

# Setup

Creates `$JOBFORGE_HOME` (default `~/jobforge/`) from [`../../templates/`](../../templates/).

1. Resolve `$JOBFORGE_HOME`. If it already exists with a `rep-log.md`, stop and say so — never
   overwrite a log.
2. Refuse to write inside a git repository that has a public remote. Ask for a different path
   instead. This directory will accumulate a resume, a target list and a record of what you cannot
   do; it does not belong in a repo you push.
3. Copy `templates/rep-log.md` and `templates/bank.md`, create `interviews/`.
4. Ask for a target date — the date the search ends, not a guess at when you will be ready. Write it
   to `target_date` in `rep-log.md` frontmatter. The banner goes silent after it.
5. Say the one sentence that matters: **if this machine is managed by your employer, put
   `JOBFORGE_HOME` on a personal volume.**
6. Offer the first drill.
