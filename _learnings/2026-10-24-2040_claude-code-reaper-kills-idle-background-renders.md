# Claude Code's memory-pressure reaper killed a long render running in a background shell

**Symptom:** the 1080p render of Ashot's Դաս 8 (`scripts/render_lecture.py`, ~1 h, all cores) stopped at
56.3 of 58.2 output minutes on 2026-10-24, with no error from ffmpeg or the script. The user's first question
was whether Claude had stopped it.

**Cause:** Claude Code reaps background shells under RAM pressure once the session has been idle for about
30 minutes (no user interaction). The render was a `run_in_background` shell, the laptop was near its 16 GB,
and nobody had typed for a while. The idle window is not configurable.

**Consequences / what works:**
- Opt-out for later sessions: `"CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP": "1"` in the `env` block of
  `~/.claude/settings.json` (added 2026-10-24; it applies to sessions started after the change).
- A render started as a detached process (not a shell the session owns) survived both the reaper and a
  restart of the session: the Դաս 6 render kept going while the user backgrounded and resumed Claude Code,
  and a separate watcher shell only read `logs/render_lecture.log`.
- Never restart a reaped job on your own: the user decides (they restarted Դաս 8, "this time ill be careful
  with other processes").
- Write the output as `<name>.part.mp4` and rename only after the duration check, so a killed render never
  leaves a file that looks finished (`render_lecture.py` does this).
