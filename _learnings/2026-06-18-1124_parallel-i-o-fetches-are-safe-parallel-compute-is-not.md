# Parallel I/O fetches are safe; parallel compute is not

The CLAUDE.md heavy-compute warning is about CPU-pegging numerics (Monte Carlo, dense grid sweeps). It does NOT apply to I/O-bound fan-out like running 5-6 yt-dlp subtitle fetches in parallel via Bash `&`. Each yt-dlp call is a small HTTP request + a brief CPU pass. Six in parallel completed in ~30s on this machine without CPU spike.

Rule of thumb: parallel HTTP/disk/LLM API calls = safe. Parallel `numpy` / matplotlib rendering / sympy / numerical sims = ask first.
