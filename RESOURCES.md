# Resources

Resources are selected for this course because they explain RAG quality, retrieval, citations, and evaluation using primary or high-trust technical material.

Also available in [French](RESOURCES_FR.md) and [Chinese](RESOURCES_ZH.md).

## Primary resources

1. [OpenAI — Optimizing LLM Accuracy](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)
   - Why: clearly separates retrieval quality from generation quality and explains RAG as retrieval plus augmented generation.
   - Used in: Lesson 1.

2. [OpenAI — Evaluation Best Practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
   - Why: explains why nondeterministic AI applications require structured evaluations and how to design them.
   - Used in: Lessons 1 and 4.

3. [Qdrant — Filtering](https://qdrant.tech/documentation/search/filtering)
   - Why: relevant to document access boundaries, company labels, departments, document types, and regulated-data retrieval.
   - Used in: Week 2.

4. [Qdrant — Hybrid Search](https://qdrant.tech/documentation/search/text-search/hybrid-search)
   - Why: explains combining semantic and lexical retrieval, which maps directly to the demo's Qdrant + Meilisearch design.
   - Used in: Week 2.

5. [Anthropic — RAG glossary entry](https://docs.anthropic.com/en/docs/resources/glossary)
   - Why: concise definition of RAG and its dependence on the quality and relevance of retrieved knowledge.
   - Used in: Lesson 1.

6. [Anthropic — Search results with citations](https://docs.anthropic.com/en/docs/build-with-claude/search-results)
   - Why: useful reference for treating source attribution as a first-class response capability.
   - Used in: Week 3.

7. [RAGAS paper — Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217)
   - Why: foundational reference for evaluating retrieval-augmented systems rather than judging only final prose.
   - Used in: Week 3 and Week 4.

## Local project resources

- [`demo/README.md`](../demo/README.md) — demo corpus, isolated stack, eval methodology, and metric limitations.
- [`demo/eval.py`](../demo/eval.py) — scoring implementation.
- [`demo/eval_set.yaml`](../demo/eval_set.yaml) — 65-question ground-truth set.
- [`demo/reports/demo-fixed.md`](../demo/reports/demo-fixed.md) — an example baseline report.
- [Request-path cheat sheet](reference/en/request-path-cheatsheet.html) — the query pipeline's architecture (hybrid retrieval, context assembly, answer generation), stage by stage. The implementation (`api/`) is the paid reference build, not part of the free course — see `rag-formation/CLAUDE.md`.
- [Terminology glossary](reference/en/glossary-cheatsheet.html) — locked EN/ZH wording for chunking, reranking, hallucination, grounding, and refusal; every lesson, cheatsheet, and animation must match it.
