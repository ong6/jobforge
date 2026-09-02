#!/usr/bin/env bash
# Derived from kirilxd/swe-interview-coach (MIT). See NOTICE at the repo root.
# Dispatch a candidate solution to the right per-language adapter and run it
# against a cases file. Locates its adapter relative to THIS script (NOT via
# ${CLAUDE_PLUGIN_ROOT}, which is substituted into command text but is not
# exported into spawned-process environments — same gotcha ensure-canvas.sh notes).
# Usage: run-solution.sh <lang> <solution-file> <cases-file>
# Prints the adapter's JSON result to stdout; exit 0 iff all cases pass.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LANG_ID="${1:-}"; SOLUTION="${2:-}"; CASES="${3:-}"

emit_err() {
  # Escape backslashes and double quotes so a path containing either stays valid JSON.
  local msg; msg=$(printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g')
  printf '{"passed":0,"total":0,"cases":[],"harness_error":"%s"}\n' "$msg"
}

# Run an adapter; if it dies without printing its JSON line (segfault, OOM kill,
# recursion crash in C) still emit a valid result instead of empty stdout.
run_adapter() {
  local out rc
  out=$("$@"); rc=$?
  if [ -n "$out" ]; then printf '%s\n' "$out"; exit "$rc"; fi
  emit_err "adapter exited with status $rc and no output (crashed?)"; exit 1
}

{ [ -n "$LANG_ID" ] && [ -n "$SOLUTION" ] && [ -n "$CASES" ]; } || {
  emit_err "usage: run-solution.sh <lang> <solution-file> <cases-file>"; exit 2; }
[ -f "$SOLUTION" ] || { emit_err "solution file not found: $SOLUTION"; exit 2; }
[ -f "$CASES" ]    || { emit_err "cases file not found: $CASES"; exit 2; }

case "$LANG_ID" in
  python|python3|py)
    command -v python3 >/dev/null 2>&1 || { emit_err "python3 not found on PATH"; exit 3; }
    run_adapter python3 "$HERE/harness/python_runner.py" "$SOLUTION" "$CASES"
    ;;
  *)
    emit_err "unsupported language: $LANG_ID (jobforge v0 ships python only)"; exit 3
    ;;
esac
