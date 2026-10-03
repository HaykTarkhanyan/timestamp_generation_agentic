# Verifier `--audit-boundaries` output is two concatenated objects

`scripts/verify_timestamps.py --audit-boundaries` prints two distinct sections to stdout:
1. The structural-check JSON report (with `contexts`).
2. A `--- BOUNDARY AUDIT ---` plaintext section showing per-chapter ±10s windows.

`json.load()` chokes because section 2 is not JSON. To parse just the report: read the whole thing as text, find the closing brace of the first JSON object, slice. Or just `grep` the audit section for the timestamp you care about.
