# LLM [08] RAG retrieval: correctness review

Source: raw transcript (YouTube auto-captions, hy) checked against the deck `llms/04_rag/08_rag_retrieval.tex`.
Minutes are on the planned timeline (`studio_cuts_v1_plan.txt`); they move with the final cut list.

## Clear mistakes

| raw time | planned | what was said | what is correct | evidence | category |
|---|---|---|---|---|---|
| 1:01:08 | 52:49 (min 53) | cross-encoder: "the number of pairs grows quadratically, n items give n(n-1)/2" | For retrieval a cross-encoder scores (query, chunk) pairs: N per query, linear in the corpus. What makes it expensive is a full forward pass per pair with nothing precomputable (no stored chunk vectors). n(n-1)/2 is the count of all chunk-chunk pairs, which search never needs | deck slide "Two shapes": "must run once per pair - so it cannot search a million chunks" (pair = query + chunk) | wrong reasoning |

## Framing (not proposed as corrections)

| raw time | what was said | note |
|---|---|---|
| 0:53:52 | "I haven't heard of any system that keeps BM25 as its main algorithm" | Personal experience, stated as such. Plenty of search systems rank with BM25 alone (it is the default in Lucene / Elasticsearch / OpenSearch); in RAG it is usually the keyword half of a hybrid. Fine as an opinion |
| 0:12:59 | "10,000 laws ... pay for those 10,000 tokens every time" | 10,000 laws would be far more than 10,000 tokens; reads as a slip of the noun, the point (paying for everything on every question) stands |

## Checked and correct

- multilingual-e5: 512-token input; Qwen3-Embedding: 32K context; mE5 as ATE-2's base, 10,000 machine-translated Reddit pairs (deck, "The recipe is smaller than you would guess").
- BM25 from the 90s search engines (Okapi BM25, TREC 1994); IDF formula log((N - n_t + 0.5)/(n_t + 0.5)) as on the slide.
- Recall ceiling 72 / 68 / 65 / 61 % as on the slide, called illustrative on camera.
- LangChain's recursive character text splitter; e5's "query: " / "passage: " prefixes; `normalize_embeddings=True`.
- CLIP is from 2021 ("five years ago"), correct.
- "matrix - no, vector, sorry" (raw 0:52:00) is corrected on camera.
