# LLM [04] LLM APIs - correctness review (2026-11-12)

Sources: the screen in the recording (frames at the raw times below; the in-class run, not the notebook on disk),
`llms/02_decoding/04_llm_api.ipynb`, web search for news. Times: edited (raw in brackets).

## Clear mistakes

| time | said | correct | evidence | category |
|---|---|---|---|---|
| 38:56 (raw 52:54-53:21) | "the total tokens include the reading (prompt) tokens too, so Lilit isn't 56 or 46... 44... I counted with two, I said it wrong" | `completion_tokens` (110) are output only; 110 - 64 reasoning = 46, as first said at 37:5x. 44 is the high-effort row (300 - 256) | 8b table on screen at raw 52:20: low 110 / 64 / $0.000045, high 300 / 256 / $0.000121 | self-correction that is itself wrong (the user kept it in the edit) |

## News (optional)

| time | said | correct | evidence |
|---|---|---|---|
| 1:47 (raw 11:44) | "Stripe wants to buy OpenRouter or already bought it, not sure" | Stripe announced on 2026-08-19 that it agreed to acquire OpenRouter (reported over $7B); closing not confirmed in the sources | https://fortune.com/2026/08/16/stripe-7-billion-deal-ai-firm-openrouter-acquisition/ , https://www.orrick.com/en/News/2026/08/OpenRouter-to-be-Acquired-by-Stripe-to-Help-Businesses-Optimize-Token-Routing-and-Usage |

## Maybe ASR (not in the corrections unless the user confirms)

| time | captions | screen |
|---|---|---|
| 40:23 (raw 54:27) | "66 calls cost us 0.2 ... two cents" | "66 calls; the ledger says $0.00294" = 0.29 cents; the account total moved $0.00117. If "two cents" was said, it is ~7x too high; "0.2 cents" would be close to the first digits of $0.0029 |

## Checked and correct

- First call usage: prompt 20, completion 39, cost 2.64e-05 (raw 22:44 frame).
- Prices: Llama 3.1 8B $0.05 in / $0.08 out per 1M, cached $0.025; GPT-4o mini 0.15 / 0.60 (4x); GPT-5 nano cached 0.005 (10x cheaper); contexts 131072, 128000, 1,000,000, 400,000 (raw 26:12).
- GPT-4o mini takes temperature but no top-k; Haiku 5.5 takes no temperature (same table).
- Armenian sentence: GPT-4o mini 22 tokens, Llama 105 (19 English each): ~5x; "5/3 more expensive, not 3x cheaper" on input prices (0.05 vs 0.15) (raw 30:20).
- Logprobs: Llama 'mat' 96.1%, GPT-4o mini 99.9%; GPT-2's 'floor' 7.6% from LLM-2 (raw 33:52).
- Llama T = 2 gibberish; Haiku T = 2 normal text (knob dropped, no error) (raw 36:55, 50:20).
- Stop strings: without one Llama wrote "Observation: According to Wikipedia ... approximately 107,000"; Wikipedia's 2022 figure 112,301 shown live (raw 40:47, 41:08).
- Reasoning: low effort 64 of 110 completion tokens reasoning; the first "56... or 46, 46" lands on 46.
- Error codes 400 / 401 / 402 / 404 / 429 / 5xx described correctly.
- No secret on screen: the key is read from `.env` with `load_dotenv`, never printed.
