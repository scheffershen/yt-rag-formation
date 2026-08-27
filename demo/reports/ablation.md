# RAG evaluation - ablation

- run at: 2026-08-13T16:05:10+00:00
- api: `http://localhost:8000`
- workspace: `meridian_demo`
- eval set: `eval_set.yaml` (44 questions, 6 unanswerable)
- topk: 5, graph_topk: 20, similarity_threshold: 0.2
- judge: `gpt-4o-mini`

## Retrieval ablation

Share of answerable questions where **every** expected source document was retrieved. Matching is on result metadata only, never on chunk body text.

| Indexes enabled | Hit rate | Index alone |
|---|---|---|
| vector only | 94.7% | 94.7% |
| + fulltext | 94.7% | 5.3% |
| + summary | 97.4% | 89.5% |
| + graph (approx) | 100.0% | 100.0% |

> The graph column is approximate: LightRAG returns a flat context string, so a reference found there may originate from a cross-reference inside another document rather than from the document itself.
