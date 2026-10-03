# Boundary precision rules (learned from review pass)

The skill's rule "land 0-3s AFTER a transition phrase, not before" is critical. Common mistakes when the speaker:
- Says "let's prove this" - put boundary at "let's prove", not at the lead-in summary 30s earlier
- States a theorem after preamble - put boundary at the NAMING of the theorem, not at "and there is a more general result"
- Asks an audience question and answers - that 30s Q&A interlude is NOT a chapter, but the topic shift after it IS

Self-review on Δας 22 caught 4 boundaries that were 10-45s too early. Always run `--audit-boundaries` after generating timestamps and read the context windows for each chapter to verify the transition phrase is actually inside the window.
