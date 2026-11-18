# [06] MCP, skills, orchestration - correctness review (Opus 5.5, 2026-11-18)

Sources: the deck `llms/tools_agents/xx_tools_2.tex`, `xx_tools_2_solution.ipynb`, `results/tools_2_run.json`
(course repo, commit 59baee7b), the recording's own screens, and web sources for the dated facts.

## Clear mistakes

None found.

## The question asked on camera (~10:10, raw 1:27:52)

"Skills are an Anthropic standard - or was someone first? Claude, put the right fact in the description."
Anthropic introduced Agent Skills on 16 October 2025, and on 18 December 2025 published the format as an open
standard (agentskills.io, which calls it "originally developed by Anthropic"). So "an Anthropic standard" was
right; nobody had it first. This went into the abstract (the cut of the doubt was removed by the user, so it stays
on camera).

## Checked and correct

- MCP began at Anthropic and is now run by a foundation: the slide's "governed by the Linux Foundation" (the Agentic
  AI Foundation, December 2025).
- "The second version came out": the MCP Python SDK v2 is the stable line (2.0.0 on 2026-07-28, 2.3.0 in October;
  the notebook pins mcp==2.3.0).
- The poisoned currency tool: "didn't even work on Llama 3.1 8B" - the slide: neither GPT-4o mini nor Llama 3.1 8B
  obeyed it (one run each).
- Context7 exposes two tools, resolve-library-id and query-docs (the notebook's list_tools output).
- The wrap-session skill "allows six tools" (the screen: "Loaded skill · 6 tools allowed").
- "No Gmail send tool, only drafts, blocked by hooks": the connector itself offers send_message, but the PreToolUse
  hook `~/.claude/hooks/gmail_guard.sh` lets only the read and draft tools through, so in effect it is as said.
