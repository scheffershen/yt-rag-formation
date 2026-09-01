# Course Syllabus

## Building a Reliable Company RAG QA Chatbot

**Format:** 16 short, project-based lessons  
**Pace:** Self-paced. Start at any lesson, in any order, whenever suits you — no calendar, and no per-learner progress or dates tracked in this repo.  
**Language scope:** English/Chinese now; French planned but paused
**Learning environment:** `rag-formation`  
**Demo environment:** `demo`

## Course mission

Build a reliable technical prototype for employees, QA and regulatory teams, customer support, suppliers, and auditors. The prototype should answer SOP and policy questions with citations, search supplier questionnaires, and refuse questions that are not supported by the indexed documents.

This chatbot is the course's worked example, not its audience — the course itself is taught to beginners learning to build enterprise-grade RAG systems. 

## How the course works

Each lesson is short and produces one concrete result:

1. Learn only the concepts needed for the current task.
2. Practice using the sanitized Meridian Labs demo corpus.
3. Inspect evidence and evaluation results.
4. Apply the insight to the next engineering decision.

Keep your own notes as you go, in whatever form works for you — this repo doesn't track per-learner progress, dates, or completion state; nothing here assumes you're on any particular lesson at any particular time.

The course deliberately evaluates **retrieval**, **generation**, **citations**, **refusal behavior**, and **operations** separately.
---

## Phase 1 — Foundations and measurement

### Lesson 1 — From employee question to cited answer

**Goal:** Understand RAG as a pipeline and distinguish retrieval failures from generation failures.  
**Practice:** Run `eval.py verify` and `test_scoring.py`; diagnose q30 and q01.  
**Artifact:** First lesson and quality cheat sheet.

### Lesson 2 — Trace one question through the real code

**Goal:** Follow a question through the API, search functions, context assembly, prompt, and response.  
**Practice:** Reconstruct the call chain (`routes/qa.py` → `qa_service.py` → `search.py` → `utils.py`) from the request-path diagram, then verify it against the running demo API.  
**Artifact:** A one-page system trace for one question.  
**Lesson:** [Open Lesson 2](lessons/0002-trace-one-question.html)

### Lesson 3 — Build a trustworthy evaluation set 

**Goal:** Understand ground truth, answerable versus unanswerable questions, expected sources, and required facts.  
**Practice:** Inspect `eval_set.yaml` and explain why metadata-only retrieval matching avoids cross-reference false positives.  
**Artifact:** Evaluation-set design checklist.  
**Lesson:** [Open Lesson 3](lessons/0003-build-a-trustworthy-evaluation-set.html)

### Lesson 4 — Establish the MVP baseline

**Goal:** Run a live evaluation and read the report as an engineer.  
**Practice:** Start the isolated demo stack, run retrieval and answer evaluations, and compare results with the historical baseline.  
**Artifact:** A current baseline report with known failure cases.  
**Lesson:** [Open Lesson 4](lessons/0004-establish-the-mvp-baseline.html)

**Phase 1 milestone:** You can explain what the system does and support every quality claim with a metric.
---

## Phase 2 — Retrieval engineering

### Lesson 5 — Semantic search, keyword search, and hybrid retrieval 

**Goal:** Understand why SOP identifiers, acronyms, names, dates, and concepts need different retrieval signals.  
**Practice:** Compare Qdrant vector results with Meilisearch full-text results using the retrieval mode.  
**Artifact:** A retrieval-method comparison table.  
**Lesson:** [Open Lesson 5](lessons/0005-semantic-keyword-and-hybrid-retrieval.html) · [Reference](reference/semantic-keyword-and-hybrid-retrieval-cheatsheet.html)

### Lesson 6 — Chunking and document structure

**Goal:** Learn how chunk size, overlap, headings, tables, and document boundaries affect retrieval.  
**Practice:** Inspect a failing question and its indexed chunks; connect the failure to the ingestion pipeline.  
**Artifact:** Chunking decision record for the demo corpus.  
**Lesson:** [Open Lesson 6](lessons/0006-chunking-and-document-structure.html) · [Reference](reference/chunking-and-document-structure-cheatsheet.html)

### Lesson 7 — Metadata, filters, and access boundaries

**Goal:** Understand why company, department, document type, classification, version, and effective-date metadata are essential for a company chatbot.  
**Practice:** Map current labels and design filters for employee, supplier, QA, and auditor views.  
**Artifact:** Metadata and access-control matrix.  
**Lesson:** [Open Lesson 7](lessons/0007-metadata-filters-and-access-boundaries.html) · [Reference](reference/metadata-filters-and-access-boundaries-cheatsheet.html)

### Lesson 8 — Query handling and reranking

**Goal:** Improve difficult queries without hiding retrieval failures behind a larger `topk`.  
**Practice:** Test query normalization, reference lookup, query rewriting, result deduplication, and reranking hypotheses.  
**Artifact:** A small retrieval experiment plan with a measurable hypothesis.  
**Lesson:** [Open Lesson 8](lessons/0008-query-handling-and-reranking.html) · [Reference](reference/query-handling-and-reranking-cheatsheet.html)

**Phase 2 milestone:** You can explain why a source was or was not retrieved and choose a targeted retrieval improvement.
---

## Phase 3 — Grounded answer generation

### Lesson 9 — Context assembly and evidence budgets

**Goal:** Understand how retrieved results become model context and how truncation can remove evidence.  
**Practice:** Inspect `build_context()`, source survival, ordering, and `max_context_chars`.  
**Artifact:** Context assembly diagram and evidence-budget recommendation.  
**Lesson:** [Open Lesson 9](lessons/0009-context-assembly-and-evidence-budgets.html) · [Reference](reference/context-assembly-and-evidence-budgets-cheatsheet.html)

### Lesson 10 — Prompts that answer only from evidence

**Goal:** Design instructions for grounded answers, uncertainty, concise responses, and explicit refusal.  
**Practice:** Compare a baseline prompt with a structured answer prompt against the evaluation set.  
**Artifact:** Versioned QA prompt specification.  
**Lesson:** [Open Lesson 10](lessons/0010-prompts-that-answer-only-from-evidence.html) · [Reference](reference/prompts-that-answer-only-from-evidence-cheatsheet.html)

### Lesson 11 — Citation design and source fidelity

**Goal:** Make citations useful, stable, and tied to evidence actually shown to the model.  
**Practice:** Check document identity, chunk identity, source deduplication, and multi-document answers.  
**Artifact:** Citation contract for the MVP.  
**Lesson:** [Open Lesson 11](lessons/0011-citation-design-and-source-fidelity.html) · [Reference](reference/citation-design-and-source-fidelity-cheatsheet.html)

### Lesson 12 — Refusal, uncertainty, and hallucination control

**Goal:** Build behavior appropriate for QA, regulatory, and audit scenarios when the corpus lacks an answer.  
**Practice:** Analyze the six unanswerable questions and test refusal wording, evidence thresholds, and unsupported claims.  
**Artifact:** Refusal policy and safety test cases.  
**Lesson:** [Open Lesson 12](lessons/0012-refusal-uncertainty-and-hallucination-control.html) · [Reference](reference/refusal-uncertainty-and-hallucination-control-cheatsheet.html)

**Phase 3 milestone:** You can produce an answer that is concise, grounded, cited, and appropriately uncertain.
---

## Phase 4 — Reliability and product readiness

### Lesson 13 — Failure isolation and graceful degradation 

**Goal:** Understand what should happen when Qdrant, Meilisearch, LightRAG, embeddings, or the LLM fails.  
**Practice:** Trace the current exception-handling paths and classify acceptable partial-service behavior.  
**Artifact:** Dependency failure matrix.  
**Lesson:** [Open Lesson 13](lessons/0013-failure-isolation-and-graceful-degradation.html) · [Reference](reference/failure-isolation-and-graceful-degradation-cheatsheet.html)

### Lesson 14 — Latency, cost, and observability 

**Goal:** Balance answer quality with response time, token cost, graph calls, and operational visibility.  
**Practice:** Read p50/p95 latency, backend counts, context size, and model statistics from evaluation reports.  
**Artifact:** MVP performance budget and telemetry checklist.  
**Lesson:** [Open Lesson 14](lessons/0014-latency-cost-and-observability.html) · [Reference](reference/latency-cost-and-observability-cheatsheet.html)

### Lesson 15 — Security, permissions, and deployment boundaries

**Goal:** Prevent the chatbot from exposing documents to the wrong users or leaking secrets and client data.  
**Practice:** Review tenant labels, API boundaries, CORS, environment files, logging, and demo/production isolation.  
**Artifact:** MVP threat and permission checklist.  
**Lesson:** [Open Lesson 15](lessons/0015-security-permissions-and-deployment-boundaries.html) · [Reference](reference/security-permissions-and-deployment-boundaries-cheatsheet.html)

### Lesson 16 — Pilot review and 30-day implementation plan 

**Goal:** Turn evaluation evidence into a prioritized implementation backlog and pilot plan.  
**Practice:** Select the highest-value fixes, rerun the evaluation, document limitations, and define go/no-go criteria.  
**Artifact:** Prototype readiness report and next-30-day roadmap.  
**Lesson:** [Open Lesson 16](lessons/0016-pilot-review-and-30-day-implementation-plan.html) · [Reference](reference/pilot-review-and-30-day-implementation-plan-cheatsheet.html)

**Phase 4 milestone:** You have a defensible prototype plan, measurable acceptance criteria, and a prioritized path toward production reliability.

---

## Recommended order

The four phases build on each other conceptually, so working through 1 → 16 in order is the easiest path the first time through. But nothing enforces that: every lesson links what it assumes back to earlier material, so it's fine to jump straight to whichever one you need — looking something up, picking up mid-course, or skipping ahead to a topic you care about.

| Phase | Lessons | Focus |
|---|---:|---|
| 1 | 1–4 | Foundations and baseline |
| 2 | 5–8 | Retrieval |
| 3 | 9–12 | Grounded answers and citations |
| 4 | 13–16 | Reliability, security, and pilot |

There's no expected rhythm — one lesson in an afternoon or one a month both work.

## Completion criteria 

The course is complete when you can:

- Explain the complete RAG request path.
- Diagnose retrieval versus generation failures.
- Run and trust the evaluation harness.
- Report strict accuracy, source hit rate, refusal accuracy, hallucination rate, and latency separately.
- Explain how chunking, metadata, hybrid search, context assembly, and prompting affect quality.
- Define citation and refusal behavior for the company use case.
- Produce a prioritized MVP backlog based on measured failures.

## Primary reference files

- [Resources](RESOURCES.md)
- [RAG quality cheat sheet](reference/rag-quality-cheatsheet.html)
- [Lesson 1](lessons/0001-from-question-to-cited-answer.html)
- [Demo harness README](../demo/README.md)


