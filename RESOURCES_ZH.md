# 资源

本课程选择这些资源，是因为它们使用主要来源或高可信技术材料，解释了 RAG 质量、检索、引用和评估。

也提供[英文版](RESOURCES.md)和[法文版](RESOURCES_FR.md)。

## 主要资源

1. [OpenAI — Optimizing LLM Accuracy](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)
   - 中文：清楚地区分检索质量和生成质量，并将 RAG 解释为"检索 + 增强生成"。
   - 用于：第 1 课。

2. [OpenAI — Evaluation Best Practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
   - 中文：解释为什么非确定性的 AI 应用需要结构化评估，以及如何设计评估。
   - 用于：第 1 课和第 4 课。

3. [Qdrant — Filtering](https://qdrant.tech/documentation/search/filtering)
   - 中文：与文档访问边界、公司标签、部门、文档类型和受监管数据检索直接相关。
   - 用于：第 2 周。

4. [Qdrant — Hybrid Search](https://qdrant.tech/documentation/search/text-search/hybrid-search)
   - 中文：解释如何组合语义检索和词法检索，与演示系统的 Qdrant + Meilisearch 设计直接对应。
   - 用于：第 2 周。

5. [Anthropic — RAG glossary entry](https://docs.anthropic.com/en/docs/resources/glossary)
   - 中文：简洁定义 RAG，并说明其效果取决于检索知识的质量和相关性。
   - 用于：第 1 课。

6. [Anthropic — Search results with citations](https://docs.anthropic.com/en/docs/build-with-claude/search-results)
   - 中文：说明为什么应该把来源归因作为回答的一等能力。
   - 用于：第 3 周。

7. [RAGAS paper — Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217)
   - 中文：评估检索增强系统的基础参考资料，强调不能只评价最终生成的文字。
   - 用于：第 3 周和第 4 周。

## 本地项目资源

- [`demo/README.md`](../demo/README.md) — 演示语料库、独立运行栈、评估方法及指标局限性。
- [`demo/eval.py`](../demo/eval.py) — 评分逻辑实现。
- [`demo/eval_set.yaml`](../demo/eval_set.yaml) — 包含 65 个问题的标准答案（ground-truth）数据集。
- [`demo/reports/demo-fixed.md`](../demo/reports/demo-fixed.md) — 基准评估报告示例。
- [请求路径速查表](reference/zh/request-path-cheatsheet.html) — 分阶段展示查询流水线架构（混合检索、上下文组装、答案生成）。其中的实现代码（位于 `api/` 目录下）属于付费参考构建版本，不包含在免费课程内容中 —— 详情请参阅 `rag-formation/CLAUDE.md`。
- [术语词汇表](reference/zh/glossary-cheatsheet.html) — 锁定分块、重排序、幻觉、有依据、拒答的中英文译法；所有课程内容、速查表、动画都必须与此一致。
