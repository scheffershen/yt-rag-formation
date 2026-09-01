# Resources / 资源

Resources are selected for this course because they explain RAG quality, retrieval, citations, and evaluation using primary or high-trust technical material.

本课程选择这些资源，是因为它们使用主要来源或高可信技术材料，解释了 RAG 质量、检索、引用和评估。

## Primary resources / 主要资源

1. [OpenAI — Optimizing LLM Accuracy](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)
   - Why: clearly separates retrieval quality from generation quality and explains RAG as retrieval plus augmented generation.
   - 中文：清楚地区分检索质量和生成质量，并将 RAG 解释为“检索 + 增强生成”。
   - Used in: Lesson 1.

2. [OpenAI — Evaluation Best Practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
   - Why: explains why nondeterministic AI applications require structured evaluations and how to design them.
   - 中文：解释为什么非确定性的 AI 应用需要结构化评估，以及如何设计评估。
   - Used in: Lessons 1 and 4.

3. [Qdrant — Filtering](https://qdrant.tech/documentation/search/filtering)
   - Why: relevant to document access boundaries, company labels, departments, document types, and regulated-data retrieval.
   - 中文：与文档访问边界、公司标签、部门、文档类型和受监管数据检索直接相关。
   - Used in: Week 2.

4. [Qdrant — Hybrid Search](https://qdrant.tech/documentation/search/text-search/hybrid-search)
   - Why: explains combining semantic and lexical retrieval, which maps directly to the demo's Qdrant + Meilisearch design.
   - 中文：解释如何组合语义检索和词法检索，与演示系统的 Qdrant + Meilisearch 设计直接对应。
   - Used in: Week 2.

5. [Anthropic — RAG glossary entry](https://docs.anthropic.com/en/docs/resources/glossary)
   - Why: concise definition of RAG and its dependence on the quality and relevance of retrieved knowledge.
   - 中文：简洁定义 RAG，并说明其效果取决于检索知识的质量和相关性。
   - Used in: Lesson 1.

6. [Anthropic — Search results with citations](https://docs.anthropic.com/en/docs/build-with-claude/search-results)
   - Why: useful reference for treating source attribution as a first-class response capability.
   - 中文：说明为什么应该把来源归因作为回答的一等能力。
   - Used in: Week 3.

7. [RAGAS paper — Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217)
   - Why: foundational reference for evaluating retrieval-augmented systems rather than judging only final prose.
   - 中文：评估检索增强系统的基础参考资料，强调不能只评价最终生成的文字。
   - Used in: Week 3 and Week 4.

## Local project resources / 本地项目资源

- [`demo/README.md`](../demo/README.md) — demo corpus, isolated stack, eval methodology, and metric limitations.
- [`demo/eval.py`](../demo/eval.py) — scoring implementation.
- [`demo/eval_set.yaml`](../demo/eval_set.yaml) — 65-question ground-truth set.
- [`demo/reports/demo-fixed.md`](../demo/reports/demo-fixed.md) — an example baseline report.
- [Request-path cheat sheet](reference/request-path-cheatsheet.html) — the query pipeline's architecture (hybrid retrieval, context assembly, answer generation), stage by stage. The implementation (`api/`) is the paid reference build, not part of the free course — see `rag-formation/CLAUDE.md`.
- [Terminology glossary](reference/glossary-cheatsheet.html) — locked EN/ZH wording for chunking, reranking, hallucination, grounding, and refusal; every lesson, cheatsheet, and animation must match it.

- [`demo/README.md`](../demo/README.md) — 演示语料库、独立运行栈、评估方法及指标局限性。
- [`demo/eval.py`](../demo/eval.py) — 评分逻辑实现。
- [`demo/eval_set.yaml`](../demo/eval_set.yaml) — 包含 65 个问题的标准答案（ground-truth）数据集。
- [`demo/reports/demo-fixed.md`](../demo/reports/demo-fixed.md) — 基准评估报告示例。
- [请求路径速查表](reference/request-path-cheatsheet.html) — 分阶段展示查询流水线架构（混合检索、上下文组装、答案生成）。其中的实现代码（位于 `api/` 目录下）属于付费参考构建版本，不包含在免费课程内容中 —— 详情请参阅 `rag-formation/CLAUDE.md`。
- [术语词汇表](reference/glossary-cheatsheet.html) — 锁定分块、重排序、幻觉、有依据、拒答的中英文译法；所有课程内容、速查表、动画都必须与此一致。