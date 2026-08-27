# RAG evaluation - ablation-fixed

- run at: 2026-08-14T08:51:50+00:00
- api: `http://localhost:8000`
- workspace: `meridian_demo`
- eval set: `eval_set.yaml` (65 questions, 6 unanswerable)
- topk: 5, graph_topk: 20, similarity_threshold: 0.2
- judge: `gpt-4o-mini`

## Retrieval ablation

Share of answerable questions where **every** expected source document was retrieved. Matching is on result metadata only, never on chunk body text.

| Indexes enabled | Hit rate | Index alone |
|---|---|---|
| vector only | 86.4% | 86.4% |
| + fulltext | 86.4% | 28.8% |
| + summary | 91.5% | 86.4% |
| + graph (approx) | 100.0% | 100.0% |

> The graph column is approximate: LightRAG returns a flat context string, so a reference found there may originate from a cross-reference inside another document rather than from the document itself.
