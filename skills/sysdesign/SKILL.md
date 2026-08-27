---
name: sysdesign
description: Walk a system-design reference design, optionally on a local Excalidraw canvas. Use for /jobforge:sysdesign, "walk me through a system design", "practice the rate limiter design".
---

# System design walkthrough

Reference designs live in [`../../content/system-design/`](../../content/system-design/), derived
from `kirilxd/swe-interview-coach` (MIT) — see [`../../NOTICE`](../../NOTICE). Their treatment of
system-design rounds is better than anything this project would write from scratch, and it is
credited rather than reimplemented.

1. Pick a design, or take the one named.
2. Start the canvas: `bash scripts/ensure-canvas.sh`. It binds localhost only. Override the port
   with `JOBFORGE_CANVAS_PORT`. If node is missing, skip the canvas and run in text.
3. Walk the design in the file's order: requirements, capacity, high-level, deep dives, tradeoffs.
   Stop at each section and ask before revealing.

This is a PULL surface. It never touches the banner and never writes to `rep-log.md`, because a
system-design walkthrough has no falsifiable unit of completion — "did I understand the fan-out
tradeoff?" is not a rep. Only graded drills go in the log.
