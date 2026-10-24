#!/usr/bin/env bash
# Codex review of Ashot info theory lessons, one at a time (read-only, everything inline in the prompt).
# Writes codex_info/review_N.md and codex_info/log_N.txt. ~2-3 min per lesson (Tserunyan's took ~90 s each).
S=/c/Users/hayk_/AppData/Local/Temp/claude/C--Users-hayk--OneDrive-Desktop-timestamp-generation-agentic/c21199d8-4430-445f-9d94-04f6e2dc74d0/scratchpad/codex_info
all=$(date +%s)
for n in "$@"; do
  start=$(date +%s)
  codex exec -s read-only --skip-git-repo-check --ephemeral -C "$S" \
    -o "$S/review_$n.md" - < "$S/prompt_$n.md" > "$S/log_$n.txt" 2>&1
  code=$?
  echo "Das $n exit=$code $(( $(date +%s) - start )) s, $(wc -l < "$S/review_$n.md" 2>/dev/null || echo 0) lines, $(( $(date +%s) - all )) s total"
done
