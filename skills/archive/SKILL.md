---
name: archive
description: Stop jobforge cleanly after the search ends. Use for /jobforge:archive, "I got the job", "I'm done with this", "turn the banner off".
---

# Archive

The intended ending. Someone who stops because they got the job is a success, and the tool should
say so and get out of the way.

1. Set `target_date` in `rep-log.md` to yesterday. The banner goes silent immediately, with no
   uninstall required.
2. Offer a one-screen summary from `bank.md` and `interviews/`: days logged, reps graded, the
   element histogram, and what the last interview said. Then stop.
3. Tell them where the files are and that `rm -rf $JOBFORGE_HOME` is the complete removal.

Never ask them to reconsider, never mention a streak they are ending, never offer a lighter cadence
unless they ask for one. Guilt is not a retention mechanism worth having.
