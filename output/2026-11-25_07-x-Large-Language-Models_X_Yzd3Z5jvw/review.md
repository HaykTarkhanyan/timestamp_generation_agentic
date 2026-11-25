# LLM [07] Kargin agent: correctness review (2026-11-26)

Sources: the transcript, `llms/04_kargin_agent/07_kargin_agent_solution.ipynb` (its saved outputs), `07_kargin_agent_OUTLINE.md`,
`sketch_finder/pyproject.toml`, `.env.example`, and web search for news. Times are on the published (edited) video.

## Clear mistakes

None found.

## Framing (not wrong, could mislead a little)

| Time | Said | What the source shows | Evidence |
|---|---|---|---|
| 33:41 | The model first calls run_sql, then the other tool, web_search | Both calls came in the same step: one reply with two tool calls (parallel tool calling) | Notebook cell 43: trace table, step 1 run_sql and step 1 web_search; "2 steps" |
| 47:41 | AI now proves Millennium problems | One problem claimed: OpenAI's Navier-Stokes proof (announced 8 Sept 2026); mathematicians call it technically correct, the Clay prize is not claimed, OpenAI says it is working on another | NPR 22 Sept 2026; Smithsonian; Scientific American |

## Checked and correct

- 558 searchable sketches after dropping 48 duplicates and 96 without dialogue (702 rows): notebook cell output.
- 43 sketches in a hospital; Ashot first after Hayko and Mko; Mko 495, Hayko 483: notebook outputs.
- The minibus run: մարշրուտ/երթուղային 0 matches, then հղի/տեղ տվ/նստեմ 13 matches, id 198 = "sketch 535": cell 39.
- Hayko: 483 sketches, Mayor of Yerevan 2018-2021: cell 43 (Armenpress).
- Final test: Sol 7/10 with 1 wrong, Terra 6/10 with 4 wrong; Sol $0.16 vs Terra $0.10 for the 10 questions, so 60% more; gpt-4o-mini about $0.01: outline table.
- run_sql returns at most 30 rows; search keeps sketches where every pattern matches and a 50-character context each side;
  web_search via Tavily with 3 results; read-only database refusing DROP TABLE: notebook source.
- Dependencies (mcp, openai, python-dotenv, tavily-python; pandas only in a maintainer group) and the two keys in `.env.example`.
- "Tune the prompt on one set, keep another set untouched" (3:35): what the final test did (10 fresh questions).
- Anthropic publishes the claude.ai system prompts, OpenAI does not publish ChatGPT's; the API adds none.
- "A big model costs a few, at most tens of drams per question": $0.016 per question on Sol.

## Not checkable from here

- The Claude phone app saying "optimizing the output for mobile view" because of its system prompt (an anecdote).
- "Trillions of parameters": the labs do not publish sizes; plausible, not confirmed.
- A "600" limit around the agent loop (raw 0:34:50): the captions are too garbled to tell what was meant.
