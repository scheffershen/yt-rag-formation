# 课程大纲

## 构建可靠的企业级 RAG 问答聊天机器人

**形式：** 16 节短小、以项目为基础的课程
**节奏：** 自定进度。可以从任意一课开始，按任意顺序，随时学习——本仓库不追踪任何日历安排，也不记录每位学习者的进度或日期。
**语言范围：** 英语、法语、中文 —— 参见 [README.md](README.md) 和 [README_FR.md](README_FR.md)
**学习环境：** `rag-formation`
**演示环境：** `demo`

## 课程使命

为员工、QA（质量保证）与合规团队、客户支持人员、供应商及审计人员构建一个可靠的技术原型。该原型应能基于引用来源回答有关标准作业程序（SOP）和政策的问题，支持对供应商问卷进行检索，并拒绝回答索引文档中未涵盖的问题。

这款聊天机器人是本课程的一个实战案例，而非课程的受众——本课程旨在教授初学者如何构建企业级 RAG 系统。

## 课程如何运作

每一课都很短，并产出一个具体成果：

1. 仅学习当前任务所需的概念。
2. 练习使用经脱敏处理的 Meridian Labs 演示语料库。
3. 检查证据与评估结果。
4. 将所得洞察应用于下一个工程决策。

请根据自己的进度做笔记，形式不限——本仓库不会追踪每位学习者的进度、日期或完成状态；其中的内容也不预设你在特定时间学习特定课程。

该课程有意将**检索**、**生成**、**引用**、**拒绝行为**及**操作**分别进行评估。

---

## 第一阶段——基础与衡量

### 第 1 课 —— 从员工提问到引用式回答

**目标：** 将 RAG 理解为一个流水线（pipeline），并区分检索失败与生成失败。
**实践：** 运行 `eval.py verify` 和 `test_scoring.py`；诊断 q30 和 q01。
**产出：** 第一课内容及质量评估速查表。

### 第 2 课 —— 追踪单个问题的完整处理流程

**目标：** 追踪一个问题在 API、搜索函数、上下文组装、提示词（Prompt）及响应生成各环节的处理过程。
**练习：** 根据请求路径图还原调用链（`routes/qa.py` → `qa_service.py` → `search.py` → `utils.py`），并对照运行中的演示 API 进行验证。
**产出物：** 单个问题的系统追踪记录（单页）。
**课程：** [打开第 2 课](lessons/zh/0002-trace-one-question.html)

### 第 3 课 —— 构建可信的评估集

**目标：** 理解"真值"（ground truth）、可回答与不可回答的问题、预期信息源以及所需事实。
**实践：** 检查 `eval_set.yaml`，并解释为何仅基于元数据的检索匹配能避免交叉引用带来的误报（false positives）。
**产出物：** 评估集设计核对清单。
**课程：** [打开第 3 课](lessons/zh/0003-build-a-trustworthy-evaluation-set.html)

### 第4课 —— 确立MVP基准

**目标：** 以工程师身份进行实时评估并解读评估报告。
**实践：** 启动独立的演示技术栈，运行检索与回答评估，并将结果与历史基线进行对比。
**产出物：** 包含已知失败案例的最新基线报告。
**课程：** [打开第 4 课](lessons/zh/0004-establish-the-mvp-baseline.html)

**第一阶段里程碑：** 能够阐述系统的功能，并用量化指标支持每一项关于质量的声明。

---

## 第二阶段——检索工程

### 第 5 课 —— 语义搜索、关键词搜索与混合检索

**目标：** 理解为何 SOP 标识符、缩写、名称、日期和概念需要不同的检索信号。
**实践：** 利用检索模式，比较 Qdrant 向量检索结果与 Meilisearch 全文检索结果。
**产出物：** 检索方法对比表。
**课程：** [打开第 5 课](lessons/zh/0005-semantic-keyword-and-hybrid-retrieval.html) · [参考资料](reference/zh/semantic-keyword-and-hybrid-retrieval-cheatsheet.html)

### 第 6 课 —— 分块与文档结构

**目标：** 了解分块大小、重叠、标题、表格及文档边界如何影响检索效果。
**实践：** 检查一个检索失败的问题及其对应的索引分块；分析检索失败与数据摄入流水线之间的关联。
**产出物：** 针对演示语料库的分块决策记录。
**课程：** [打开第 6 课](lessons/zh/0006-chunking-and-document-structure.html) · [参考资料](reference/zh/chunking-and-document-structure-cheatsheet.html)

### 第 7 课 —— 元数据、过滤器与访问边界

**目标：** 理解为何公司、部门、文档类型、分类、版本及生效日期等元数据对于企业聊天机器人至关重要。
**实践：** 映射现有标签，并针对员工、供应商、质量保证（QA）人员及审计人员的视图设计相应的筛选条件。
**产出物：** 元数据与访问控制矩阵。
**课程：** [打开第 7 课](lessons/zh/0007-metadata-filters-and-access-boundaries.html) · [参考资料](reference/zh/metadata-filters-and-access-boundaries-cheatsheet.html)

### 第8课 —— 查询处理与重排序

**目标：** 改进困难查询，同时避免因设置过大的 `topk` 值而掩盖检索失败的问题。
**实践：** 针对查询归一化、参考资料查找、查询重写、结果去重及重排序等环节，测试相关假设。
**产出物：** 一份包含可衡量假设的小型检索实验计划。
**课程：** [打开第 8 课](lessons/zh/0008-query-handling-and-reranking.html) · [参考资料](reference/zh/query-handling-and-reranking-cheatsheet.html)

**第二阶段里程碑：** 您能够解释为何检索到了（或未检索到）某项来源，并选择一项针对性的检索改进措施。

---

## 阶段 3 —— 基于事实依据的答案生成

### 第9课 —— 上下文组装与证据预算

**目标：** 了解检索结果如何转化为模型上下文，以及截断操作如何导致关键证据丢失。
**实践：** 检查 `build_context()` 函数，分析源内容的保留情况、排序逻辑及 `max_context_chars` 参数的影响。
**产出物：** 上下文组装示意图与证据容量（evidence-budget）建议。
**课程：** [打开第 9 课](lessons/zh/0009-context-assembly-and-evidence-budgets.html) · [参考资料](reference/zh/context-assembly-and-evidence-budgets-cheatsheet.html)

### 第10课 —— 仅依据证据进行回答的提示词

**目标：** 设计指令，以确保回答基于既定依据、处理不确定性、保持回答简洁并明确拒绝回答。
**实践：** 在评估集上对比基准提示词与结构化回答提示词的效果。
**产出物：** 带有版本记录的问答（QA）提示词规范。
**课程：** [打开第 10 课](lessons/zh/0010-prompts-that-answer-only-from-evidence.html) · [参考资料](reference/zh/prompts-that-answer-only-from-evidence-cheatsheet.html)

### 第11课 —— 引用设计与来源忠实度

**目标：** 确保引用内容实用、稳定，并与实际呈现给模型的信息（证据）相对应。
**实践：** 验证文档标识与数据块（chunk）标识，进行源去重处理，并处理多文档回答场景。
**产出物：** MVP（最小可行性产品）阶段的引用规范。
**课程：** [打开课程 11](lessons/zh/0011-citation-design-and-source-fidelity.html) · [参考资料](reference/zh/citation-design-and-source-fidelity-cheatsheet.html)

### 第12课 —— 拒绝、不确定性与幻觉控制

**目标：** 针对语料库中缺失答案的情况，构建符合质量保证（QA）、合规监管及审计要求的行为模式。
**实践：** 分析六类无法回答的问题，并测试拒绝回答的措辞、证据阈值以及针对无依据主张的处理方式。
**产出物：** 拒绝回答策略与安全性测试用例。
**课程：** [打开课程 12](lessons/zh/0012-refusal-uncertainty-and-hallucination-control.html) · [参考资料](reference/zh/refusal-uncertainty-and-hallucination-control-cheatsheet.html)

**第三阶段里程碑：** 你能够给出简洁、有据可依、附带引用且表达了适度不确定性的回答。

---

## 第四阶段——可靠性与产品就绪状态

### 第 13 课 —— 故障隔离与优雅降级

**目标：** 明确当 Qdrant、Meilisearch、LightRAG、Embedding（向量化）或 LLM 发生故障时应采取的应对措施。
**实践：** 追踪当前的异常处理流程，并对可接受的部分服务行为进行分类。
**产出物：** 依赖故障矩阵。
**课程：** [打开第 13 课](lessons/zh/0013-failure-isolation-and-graceful-degradation.html) · [参考资料](reference/zh/failure-isolation-and-graceful-degradation-cheatsheet.html)

### 第 14 课 —— 延迟、成本与可观测性

**目标：** 在回答质量与响应时间、Token 成本、图（Graph）调用及运维可观测性之间取得平衡。
**实践：** 从评估报告中读取 p50/p95 延迟、后端调用次数、上下文大小及模型统计数据。
**产出物：** MVP 性能预算与遥测检查清单。
**课程：** [打开第 14 课](lessons/zh/0014-latency-cost-and-observability.html) · [参考资料](reference/zh/latency-cost-and-observability-cheatsheet.html)

### 第 15 课 —— 安全性、权限与部署边界

**目标：** 防止聊天机器人向错误的用户暴露文档，或泄露机密信息及客户数据。
**实践：** 审查租户标签、API 边界、CORS、环境变量文件、日志记录以及演示环境与生产环境的隔离措施。
**产出物：** MVP 阶段的威胁与权限检查清单。
**课程：** [打开第 15 课](lessons/zh/0015-security-permissions-and-deployment-boundaries.html) · [参考资料](reference/zh/security-permissions-and-deployment-boundaries-cheatsheet.html)

### 第16课 —— 试点评估与30天实施计划

**目标：** 将评估结果转化为按优先级排序的实施待办事项列表及试点计划。
**实践：** 筛选出价值最高的改进项，重新进行评估，记录局限性，并明确"继续/终止"（go/no-go）的决策标准。
**产出物：** 原型就绪度报告与未来 30 天实施路线图。
**课程：** [打开课程 16](lessons/zh/0016-pilot-review-and-30-day-implementation-plan.html) · [参考资料](reference/zh/pilot-review-and-30-day-implementation-plan-cheatsheet.html)

**第四阶段里程碑：** 你已拥有一份站得住脚的原型计划、可衡量的验收标准，以及一条通往生产可靠性的优先路径。

---

## 推荐顺序

这四个阶段在概念上层层递进，因此初次学习时，按顺序从第1课学到第16课是最轻松的路径。不过，这并非强制要求：每一课都会将涉及的基础知识与先前的内容联系起来，所以你可以直接跳转到所需的任何一课——无论是为了查阅资料、从课程中途继续学习，还是直接跳到你感兴趣的主题。

| 阶段 | 课程 | 重点 |
|---|---:|---|
| 1 | 1–4 | 基础与基准 |
| 2 | 5–8 | 检索 |
| 3 | 9–12 | 基于事实的回答与引用 |
| 4 | 13–16 | 可靠性、安全性与试点 |

没有预设的节奏——无论是下午上一节课，还是一个月上一节课，都行得通。

## 完成标准

达到以下要求即可视为完成本课程：

- 阐述完整的 RAG 请求处理流程。
- 诊断检索环节与生成环节的故障。
- 运行并信任评估框架。
- 分别报告严格准确率、源命中率、拒答准确率、幻觉率及延迟指标。
- 解释分块（chunking）、元数据、混合检索、上下文组装及提示词（prompting）如何影响质量。
- 针对公司具体应用场景，定义引用与拒答行为规范。
- 根据实测的故障情况，制定优先级明确的 MVP（最小可行性产品）待办事项列表。

## 继续学习（不在 16 课大纲之内）

### 第 17 课——试点之后该做什么

- 目标：试点一旦上线，真实用户、反馈和失败案例开始出现之后，知道接下来该往哪走。
- 练习：把自己试点最薄弱的环节，对应到 `rag-formation-continue`（一套独立、免费、基于真实生产经验写成的后续教程）里正确的一章。
- 产出：下一个你会做的生产就绪改动，并且落到 Lesson 16 工作表里一个具体的缺口上。
- 课程：[打开第 17 课](lessons/zh/0017-what-comes-after-the-pilot.html) · [GitHub 上的 rag-formation-continue](https://github.com/scheffershen/rag-formation-continue)

这一课不计入上面第 1 到第 4 阶段的编号，也不是下面完成标准的必需项——它只是指明课程本身结束之后接下来该读什么，不是课程里又多出来的一个考核步骤。

这套教程里有两章连同配图一起收录在本仓库中：

- [从零开始搭建你自己的 RAG 聊天机器人](lessons/zh/continue/02-build-your-rag-from-zero.html)——一份可复制粘贴的搭建提示词和检查清单，用于搭建带引用回答的四通道基线。
- [把 RAG 反馈转化为改进计划](lessons/zh/continue/01-improve-your-rag.html)——日志记录、用户反馈，以及配合 Claude Code 或 Codex 的从归类到修复流程。

## 主要参考文件

- [资源](RESOURCES_ZH.md)
- [RAG 质量速查表](reference/zh/rag-quality-cheatsheet.html)
- [第 1 课](lessons/zh/0001-from-question-to-cited-answer.html)
- [演示程序 README](../demo/README.md)
