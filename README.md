# Course Syllabus

## Building a Reliable Company RAG QA Chatbot

**Format:** 16 short, project-based lessons  
**Pace:** Self-paced. Start at any lesson, in any order, whenever suits you — no calendar, and no per-learner progress or dates tracked in this repo.  
**Language scope:** English/Chinese now; French planned but paused
**Learning environment:** `rag-formation`  
**Demo environment:** `demo`

## Course mission

Build a reliable technical prototype for employees, QA and regulatory teams, customer support, suppliers, and auditors. The prototype should answer SOP and policy questions with citations, search supplier questionnaires, and refuse questions that are not supported by the indexed documents.
为员工、QA（质量保证）与合规团队、客户支持人员、供应商及审计人员构建一个可靠的技术原型。该原型应能基于引用来源回答有关标准作业程序（SOP）和政策的问题，支持对供应商问卷进行检索，并拒绝回答索引文档中未涵盖的问题。

This chatbot is the course's worked example, not its audience — the course itself is taught to beginners learning to build enterprise-grade RAG systems. 
这款聊天机器人是本课程的一个实战案例，而非课程的受众——本课程旨在教授初学者如何构建企业级 RAG 系统。

## How the course works

Each lesson is short and produces one concrete result:

1. Learn only the concepts needed for the current task.
2. Practice using the sanitized Meridian Labs demo corpus.
3. Inspect evidence and evaluation results.
4. Apply the insight to the next engineering decision.
1. 仅学习当前任务所需的概念。
2. 练习使用经脱敏处理的 Meridian Labs 演示语料库。
3. 检查证据与评估结果。
4. 将所得洞察应用于下一个工程决策。

Keep your own notes as you go, in whatever form works for you — this repo doesn't track per-learner progress, dates, or completion state; nothing here assumes you're on any particular lesson at any particular time.
请根据自己的进度做笔记，形式不限——本仓库不会追踪每位学习者的进度、日期或完成状态；其中的内容也不预设你在特定时间学习特定课程。

The course deliberately evaluates **retrieval**, **generation**, **citations**, **refusal behavior**, and **operations** separately.
该课程有意将**检索**、**生成**、**引用**、**拒绝行为**及**操作**分别进行评估。
---

## Phase 1 — Foundations and measurement - 第一阶段——基础与衡量

### Lesson 1 — From employee question to cited answer - 第 1 课 —— 从员工提问到引用式回答

**Goal:** Understand RAG as a pipeline and distinguish retrieval failures from generation failures.  
**Practice:** Run `eval.py verify` and `test_scoring.py`; diagnose q30 and q01.  
**Artifact:** First lesson and quality cheat sheet.

**目标：** 将 RAG 理解为一个流水线（pipeline），并区分检索失败与生成失败。
**实践：** 运行 `eval.py verify` 和 `test_scoring.py`；诊断 q30 和 q01。
**产出：** 第一课内容及质量评估速查表。

### Lesson 2 — Trace one question through the real code - 课程 2 —— 追踪单个问题的完整处理流程

**Goal:** Follow a question through the API, search functions, context assembly, prompt, and response.  
**Practice:** Reconstruct the call chain (`routes/qa.py` → `qa_service.py` → `search.py` → `utils.py`) from the request-path diagram, then verify it against the running demo API.  
**Artifact:** A one-page system trace for one question.  
**Lesson:** [Open Lesson 2](lessons/0002-trace-one-question.html)

**目标：** 追踪一个问题在 API、搜索函数、上下文组装、提示词（Prompt）及响应生成各环节的处理过程。
**练习：** 根据请求路径图还原调用链（`routes/qa.py` → `qa_service.py` → `search.py` → `utils.py`），并对照运行中的演示 API 进行验证。
**产出物：** 单个问题的系统追踪记录（单页）。
**课程：** [打开课程 2](lessons/0002-trace-one-question.html)

### Lesson 3 — Build a trustworthy evaluation set - 第 3 课 —— 构建可信的评估集

**Goal:** Understand ground truth, answerable versus unanswerable questions, expected sources, and required facts.  
**Practice:** Inspect `eval_set.yaml` and explain why metadata-only retrieval matching avoids cross-reference false positives.  
**Artifact:** Evaluation-set design checklist.  
**Lesson:** [Open Lesson 3](lessons/0003-build-a-trustworthy-evaluation-set.html)

**目标：** 理解“真值”（ground truth）、可回答与不可回答的问题、预期信息源以及所需事实。
**实践：** 检查 `eval_set.yaml`，并解释为何仅基于元数据的检索匹配能避免交叉引用带来的误报（false positives）。
**产出物：** 评估集设计核对清单。
**课程：** [打开第 3 课](lessons/0003-build-a-trustworthy-evaluation-set.html)

### Lesson 4 — Establish the MVP baseline - 第4课 —— 确立MVP基准

**Goal:** Run a live evaluation and read the report as an engineer.  
**Practice:** Start the isolated demo stack, run retrieval and answer evaluations, and compare results with the historical baseline.  
**Artifact:** A current baseline report with known failure cases.  
**Lesson:** [Open Lesson 4](lessons/0004-establish-the-mvp-baseline.html)

**目标：** 以工程师身份进行实时评估并解读评估报告。
**实践：** 启动独立的演示技术栈，运行检索与回答评估，并将结果与历史基线进行对比。
**产出物：** 包含已知失败案例的最新基线报告。
**课程：** [打开第 4 课](lessons/0004-establish-the-mvp-baseline.html)

**Phase 1 milestone:** You can explain what the system does and support every quality claim with a metric.
**第一阶段里程碑：** 能够阐述系统的功能，并用量化指标支持每一项关于质量的声明。
---

## Phase 2 — Retrieval engineering - 第二阶段——检索工程

### Lesson 5 — Semantic search, keyword search, and hybrid retrieval - 第 5 课 —— 语义搜索、关键词搜索与混合检索

**Goal:** Understand why SOP identifiers, acronyms, names, dates, and concepts need different retrieval signals.  
**Practice:** Compare Qdrant vector results with Meilisearch full-text results using the retrieval mode.  
**Artifact:** A retrieval-method comparison table.  
**Lesson:** [Open Lesson 5](lessons/0005-semantic-keyword-and-hybrid-retrieval.html) · [Reference](reference/semantic-keyword-and-hybrid-retrieval-cheatsheet.html)

**目标：** 理解为何 SOP 标识符、缩写、名称、日期和概念需要不同的检索信号。
**实践：** 利用检索模式，比较 Qdrant 向量检索结果与 Meilisearch 全文检索结果。
**产出物：** 检索方法对比表。
**课程：** [打开第 5 课](lessons/0005-semantic-keyword-and-hybrid-retrieval.html) · [参考资料](reference/semantic-keyword-and-hybrid-retrieval-cheatsheet.html)

### Lesson 6 — Chunking and document structure - 第 6 课 —— 分块与文档结构

**Goal:** Learn how chunk size, overlap, headings, tables, and document boundaries affect retrieval.  
**Practice:** Inspect a failing question and its indexed chunks; connect the failure to the ingestion pipeline.  
**Artifact:** Chunking decision record for the demo corpus.  
**Lesson:** [Open Lesson 6](lessons/0006-chunking-and-document-structure.html) · [Reference](reference/chunking-and-document-structure-cheatsheet.html)

**目标：** 了解分块大小、重叠、标题、表格及文档边界如何影响检索效果。
**实践：** 检查一个检索失败的问题及其对应的索引分块；分析检索失败与数据摄入流水线之间的关联。
**产出物：** 针对演示语料库的分块决策记录。
**课程：** [打开第 6 课](lessons/0006-chunking-and-document-structure.html) · [参考资料](reference/chunking-and-document-structure-cheatsheet.html)

### Lesson 7 — Metadata, filters, and access boundaries - 第 7 课 —— 元数据、过滤器与访问边界

**Goal:** Understand why company, department, document type, classification, version, and effective-date metadata are essential for a company chatbot.  
**Practice:** Map current labels and design filters for employee, supplier, QA, and auditor views.  
**Artifact:** Metadata and access-control matrix.  
**Lesson:** [Open Lesson 7](lessons/0007-metadata-filters-and-access-boundaries.html) · [Reference](reference/metadata-filters-and-access-boundaries-cheatsheet.html)

**目标：** 理解为何公司、部门、文档类型、分类、版本及生效日期等元数据对于企业聊天机器人至关重要。
**实践：** 映射现有标签，并针对员工、供应商、质量保证（QA）人员及审计人员的视图设计相应的筛选条件。
**产出物：** 元数据与访问控制矩阵。
**课程：** [打开第 7 课](lessons/0007-metadata-filters-and-access-boundaries.html) · [参考资料](reference/metadata-filters-and-access-boundaries-cheatsheet.html)

### Lesson 8 — Query handling and reranking - 第8课 —— 查询处理与重排序

**Goal:** Improve difficult queries without hiding retrieval failures behind a larger `topk`.  
**Practice:** Test query normalization, reference lookup, query rewriting, result deduplication, and reranking hypotheses.  
**Artifact:** A small retrieval experiment plan with a measurable hypothesis.  
**Lesson:** [Open Lesson 8](lessons/0008-query-handling-and-reranking.html) · [Reference](reference/query-handling-and-reranking-cheatsheet.html)

**目标：** 改进困难查询，同时避免因设置过大的 `topk` 值而掩盖检索失败的问题。
**实践：** 针对查询归一化、参考资料查找、查询重写、结果去重及重排序等环节，测试相关假设。
**产出物：** 一份包含可衡量假设的小型检索实验计划。
**课程：** [打开第 8 课](lessons/0008-query-handling-and-reranking.html) · [参考资料](reference/query-handling-and-reranking-cheatsheet.html)

**Phase 2 milestone:** You can explain why a source was or was not retrieved and choose a targeted retrieval improvement.
**第二阶段里程碑：** 您能够解释为何检索到了（或未检索到）某项来源，并选择一项针对性的检索改进措施。
---

## Phase 3 — Grounded answer generation - 阶段 3 —— 基于事实依据的答案生成

### Lesson 9 — Context assembly and evidence budgets - 第9课 —— 上下文组装与证据预算

**Goal:** Understand how retrieved results become model context and how truncation can remove evidence.  
**Practice:** Inspect `build_context()`, source survival, ordering, and `max_context_chars`.  
**Artifact:** Context assembly diagram and evidence-budget recommendation.  
**Lesson:** [Open Lesson 9](lessons/0009-context-assembly-and-evidence-budgets.html) · [Reference](reference/context-assembly-and-evidence-budgets-cheatsheet.html)

**目标：** 了解检索结果如何转化为模型上下文，以及截断操作如何导致关键证据丢失。
**实践：** 检查 `build_context()` 函数，分析源内容的保留情况、排序逻辑及 `max_context_chars` 参数的影响。
**产出物：** 上下文组装示意图与证据容量（evidence-budget）建议。
**课程：** [打开第 9 课](lessons/0009-context-assembly-and-evidence-budgets.html) · [参考资料](reference/context-assembly-and-evidence-budgets-cheatsheet.html)

### Lesson 10 — Prompts that answer only from evidence - 第10课 —— 仅依据证据进行回答的提示词

**Goal:** Design instructions for grounded answers, uncertainty, concise responses, and explicit refusal.  
**Practice:** Compare a baseline prompt with a structured answer prompt against the evaluation set.  
**Artifact:** Versioned QA prompt specification.  
**Lesson:** [Open Lesson 10](lessons/0010-prompts-that-answer-only-from-evidence.html) · [Reference](reference/prompts-that-answer-only-from-evidence-cheatsheet.html)

**目标：** 设计指令，以确保回答基于既定依据、处理不确定性、保持回答简洁并明确拒绝回答。
**实践：** 在评估集上对比基准提示词与结构化回答提示词的效果。
**产出物：** 带有版本记录的问答（QA）提示词规范。
**课程：** [打开第 10 课](lessons/0010-prompts-that-answer-only-from-evidence.html) · [参考资料](reference/prompts-that-answer-only-from-evidence-cheatsheet.html)

### Lesson 11 — Citation design and source fidelity - 第11课 —— 引用设计与来源忠实度

**Goal:** Make citations useful, stable, and tied to evidence actually shown to the model.  
**Practice:** Check document identity, chunk identity, source deduplication, and multi-document answers.  
**Artifact:** Citation contract for the MVP.  
**Lesson:** [Open Lesson 11](lessons/0011-citation-design-and-source-fidelity.html) · [Reference](reference/citation-design-and-source-fidelity-cheatsheet.html)

**目标：** 确保引用内容实用、稳定，并与实际呈现给模型的信息（证据）相对应。
**实践：** 验证文档标识与数据块（chunk）标识，进行源去重处理，并处理多文档回答场景。
**产出物：** MVP（最小可行性产品）阶段的引用规范。
**课程：** [打开课程 11](lessons/0011-citation-design-and-source-fidelity.html) · [参考资料](reference/citation-design-and-source-fidelity-cheatsheet.html)

### Lesson 12 — Refusal, uncertainty, and hallucination control - 第12课 —— 拒绝、不确定性与幻觉控制

**Goal:** Build behavior appropriate for QA, regulatory, and audit scenarios when the corpus lacks an answer.  
**Practice:** Analyze the six unanswerable questions and test refusal wording, evidence thresholds, and unsupported claims.  
**Artifact:** Refusal policy and safety test cases.  
**Lesson:** [Open Lesson 12](lessons/0012-refusal-uncertainty-and-hallucination-control.html) · [Reference](reference/refusal-uncertainty-and-hallucination-control-cheatsheet.html)

**目标：** 针对语料库中缺失答案的情况，构建符合质量保证（QA）、合规监管及审计要求的行为模式。
**实践：** 分析六类无法回答的问题，并测试拒绝回答的措辞、证据阈值以及针对无依据主张的处理方式。
**产出物：** 拒绝回答策略与安全性测试用例。
**课程：** [打开课程 12](lessons/0012-refusal-uncertainty-and-hallucination-control.html) · [参考资料](reference/refusal-uncertainty-and-hallucination-control-cheatsheet.html)

**Phase 3 milestone:** You can produce an answer that is concise, grounded, cited, and appropriately uncertain.
**第三阶段里程碑：** 你能够给出简洁、有据可依、附带引用且表达了适度不确定性的回答。
---

## Phase 4 — Reliability and product readiness - 第四阶段——可靠性与产品就绪状态

### Lesson 13 — Failure isolation and graceful degradation - 第 13 课 —— 故障隔离与优雅降级

**Goal:** Understand what should happen when Qdrant, Meilisearch, LightRAG, embeddings, or the LLM fails.  
**Practice:** Trace the current exception-handling paths and classify acceptable partial-service behavior.  
**Artifact:** Dependency failure matrix.  
**Lesson:** [Open Lesson 13](lessons/0013-failure-isolation-and-graceful-degradation.html) · [Reference](reference/failure-isolation-and-graceful-degradation-cheatsheet.html)

**目标：** 明确当 Qdrant、Meilisearch、LightRAG、Embedding（向量化）或 LLM 发生故障时应采取的应对措施。
**实践：** 追踪当前的异常处理流程，并对可接受的部分服务行为进行分类。
**产出物：** 依赖故障矩阵。
**课程：** [打开第 13 课](lessons/0013-failure-isolation-and-graceful-degradation.html) · [参考资料](reference/failure-isolation-and-graceful-degradation-cheatsheet.html)

### Lesson 14 — Latency, cost, and observability - 第 14 课 —— 延迟、成本与可观测性

**Goal:** Balance answer quality with response time, token cost, graph calls, and operational visibility.  
**Practice:** Read p50/p95 latency, backend counts, context size, and model statistics from evaluation reports.  
**Artifact:** MVP performance budget and telemetry checklist.  
**Lesson:** [Open Lesson 14](lessons/0014-latency-cost-and-observability.html) · [Reference](reference/latency-cost-and-observability-cheatsheet.html)

**目标：** 在回答质量与响应时间、Token 成本、图（Graph）调用及运维可观测性之间取得平衡。
**实践：** 从评估报告中读取 p50/p95 延迟、后端调用次数、上下文大小及模型统计数据。
**产出物：** MVP 性能预算与遥测检查清单。
**课程：** [打开第 14 课](lessons/0014-latency-cost-and-observability.html) · [参考资料](reference/latency-cost-and-observability-cheatsheet.html)

### Lesson 15 — Security, permissions, and deployment boundaries - 第 15 课 —— 安全性、权限与部署边界

**Goal:** Prevent the chatbot from exposing documents to the wrong users or leaking secrets and client data.  
**Practice:** Review tenant labels, API boundaries, CORS, environment files, logging, and demo/production isolation.  
**Artifact:** MVP threat and permission checklist.  
**Lesson:** [Open Lesson 15](lessons/0015-security-permissions-and-deployment-boundaries.html) · [Reference](reference/security-permissions-and-deployment-boundaries-cheatsheet.html)

**目标：** 防止聊天机器人向错误的用户暴露文档，或泄露机密信息及客户数据。
**实践：** 审查租户标签、API 边界、CORS、环境变量文件、日志记录以及演示环境与生产环境的隔离措施。
**产出物：** MVP 阶段的威胁与权限检查清单。
**课程：** [打开第 15 课](lessons/0015-security-permissions-and-deployment-boundaries.html) · [参考资料](reference/security-permissions-and-deployment-boundaries-cheatsheet.html)

### Lesson 16 — Pilot review and 30-day implementation plan - 第16课 —— 试点评估与30天实施计划

**Goal:** Turn evaluation evidence into a prioritized implementation backlog and pilot plan.  
**Practice:** Select the highest-value fixes, rerun the evaluation, document limitations, and define go/no-go criteria.  
**Artifact:** Prototype readiness report and next-30-day roadmap.  
**Lesson:** [Open Lesson 16](lessons/0016-pilot-review-and-30-day-implementation-plan.html) · [Reference](reference/pilot-review-and-30-day-implementation-plan-cheatsheet.html)

**目标：** 将评估结果转化为按优先级排序的实施待办事项列表及试点计划。
**实践：** 筛选出价值最高的改进项，重新进行评估，记录局限性，并明确“继续/终止”（go/no-go）的决策标准。
**产出物：** 原型就绪度报告与未来 30 天实施路线图。
**课程：** [打开课程 16](lessons/0016-pilot-review-and-30-day-implementation-plan.html) · [参考资料](reference/pilot-review-and-30-day-implementation-plan-cheatsheet.html)

**Phase 4 milestone:** You have a defensible prototype plan, measurable acceptance criteria, and a prioritized path toward production reliability.

---

## Recommended order

The four phases build on each other conceptually, so working through 1 → 16 in order is the easiest path the first time through. But nothing enforces that: every lesson links what it assumes back to earlier material, so it's fine to jump straight to whichever one you need — looking something up, picking up mid-course, or skipping ahead to a topic you care about.

这四个阶段在概念上层层递进，因此初次学习时，按顺序从第1课学到第16课是最轻松的路径。不过，这并非强制要求：每一课都会将涉及的基础知识与先前的内容联系起来，所以你可以直接跳转到所需的任何一课——无论是为了查阅资料、从课程中途继续学习，还是直接跳到你感兴趣的主题。

| Phase | Lessons | Focus |
|---|---:|---|
| 1 | 1–4 | Foundations and baseline |
| 2 | 5–8 | Retrieval |
| 3 | 9–12 | Grounded answers and citations |
| 4 | 13–16 | Reliability, security, and pilot |

| 阶段 | 课程 | 重点 |
|---|---:|---|
| 1 | 1–4 | 基础与基准 |
| 2 | 5–8 | 检索 |
| 3 | 9–12 | 基于事实的回答与引用 |
| 4 | 13–16 | 可靠性、安全性与试点 |

There's no expected rhythm — one lesson in an afternoon or one a month both work. - 没有预设的节奏——无论是下午上一节课，还是一个月上一节课，都行得通

## Completion criteria - 完成标准

The course is complete when you can:

- Explain the complete RAG request path.
- Diagnose retrieval versus generation failures.
- Run and trust the evaluation harness.
- Report strict accuracy, source hit rate, refusal accuracy, hallucination rate, and latency separately.
- Explain how chunking, metadata, hybrid search, context assembly, and prompting affect quality.
- Define citation and refusal behavior for the company use case.
- Produce a prioritized MVP backlog based on measured failures.

- 阐述完整的 RAG 请求处理流程。
- 诊断检索环节与生成环节的故障。
- 运行并信任评估框架。
- 分别报告严格准确率、源命中率、拒答准确率、幻觉率及延迟指标。
- 解释分块（chunking）、元数据、混合检索、上下文组装及提示词（prompting）如何影响质量。
- 针对公司具体应用场景，定义引用与拒答行为规范。
- 根据实测的故障情况，制定优先级明确的 MVP（最小可行性产品）待办事项列表。

## Primary reference files

- [Resources](RESOURCES.md)
- [RAG quality cheat sheet](reference/rag-quality-cheatsheet.html)
- [Lesson 1](lessons/0001-from-question-to-cited-answer.html)
- [Demo harness README](../demo/README.md)


