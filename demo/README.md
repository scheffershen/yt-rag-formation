# Demo corpus + evaluation harness - 演示语料库 + 评估工具套件

Two things the YouTube walkthrough needs and the project did not have: - YouTube 演示视频需要但该项目未具备的两点：

1. **A sanitised demo workspace** — an isolated stack, a synthetic document set,
   and demo-only collections, so nothing on screen is client data.
2. **A scored evaluation harness** — a defensible accuracy number, produced live
   on camera, with the method visible.

1. **一个经过脱敏处理的演示工作区** —— 包含隔离的技术栈、模拟文档集以及仅用于演示的集合，确保屏幕上不显示任何客户数据。
2. **一套带评分功能的评估机制** —— 能够得出经得起推敲的准确率数据，且该数据在镜头前实时生成，评估方法清晰可见。

Nothing here modifies `api/`. The demo API reads `.env.demo`, not `api/.env`.

```
docker-compose.demo.yml   isolated stack: qdrant, meilisearch, postgres, redis, api
.env.demo                 container env - demo collections, no production secrets
.env.demo.local           the ONE real secret (OPENAI_API_KEY) - git-ignored, demo-only
setup_demo.py             up / ingest / status / down
build_corpus.py           25 synthetic documents -> Markdown + PDF
eval_set.yaml             65 questions of ground truth over that corpus (version 1.1.0)
eval.py                   verify (offline) + run (scores the live system)
test_scoring.py           self-test for the metric code
```

```
docker-compose.demo.yml   独立部署栈：包含 qdrant、meilisearch、postgres、redis 和 api
.env.demo                 容器环境变量 —— 针对演示数据集，不含生产环境敏感信息
.env.demo.local           唯一的真实敏感信息 (OPENAI_API_KEY) —— 已在 git 中忽略，仅用于演示
setup_demo.py             启动 / 导入数据 / 检查状态 / 停止服务
build_corpus.py           生成 25 份模拟文档 -> Markdown + PDF 格式
eval_set.yaml             基于上述语料库的 65 个带标准答案的问题（版本 1.1.0）
eval.py                   验证（离线）+ 运行（对实时系统进行评分）
test_scoring.py           评分指标代码的自测脚本
```

## About secrets

The demo stack consumes exactly one real secret, `OPENAI_API_KEY`, from
**`demo/.env.demo.local`** — a file you create yourself from the checked-in
`.env.demo.local.example`, containing nothing but that one key:

```bash
cp .env.demo.local.example .env.demo.local
# then edit .env.demo.local and set OPENAI_API_KEY=sk-... without
# screen-sharing the editor
```

## Setup

```bash
pip install -r requirements.txt
cp .env.demo.local.example .env.demo.local
# set OPENAI_API_KEY in .env.demo.local
```

Python 3.10+ and Docker. These four packages are independent of `api/`'s
dependencies — you do **not** need a working local api environment, because
ingestion runs inside the API container.

## Quickstart

```bash
python build_corpus.py                    # corpus/md + corpus/pdf
python eval.py verify                     # offline, no API cost
python setup_demo.py up                   # build + start the isolated stack
python setup_demo.py ingest               # index into demo-only collections
python eval.py --env-file .env.demo.local run --workspace meridian_demo --tag demo-1
python setup_demo.py down                 # when you are done
```

---

## 1. The demo stack

`docker-compose.demo.yml` is deliberately not the project stack: 

- its own container names, network and datastore ports, so it does not collide
  with the project stack
- demo-only datastore credentials; the only real secret it consumes is
  `OPENAI_API_KEY`

- 拥有独立的容器名称、网络配置及数据存储端口，避免与项目主技术栈发生冲突
- 仅限演示使用的数据存储凭证；其使用的唯一真实敏感信息是 `OPENAI_API_KEY`

| Service | Host port | Why it matters |
|---|---|---|
| `api` | 8000 | what `eval.py` talks to |
| `qdrant` | 6433 | dashboard shows an empty instance, no production collections |
| `meilisearch` | 7800 | same |
| `postgres` | 5533 | LightRAG graph + vector storage |
| `redis` | 6479 | present so nothing fails if a code path reaches for it |

A one-shot `init-db` service creates the LightRAG tables before the API starts.
It is idempotent, so it runs safely on every `up`.

一次性的 `init-db` 服务会在 API 启动前创建 LightRAG 数据库表。
它是幂等的，因此每次启动时都能安全运行。

```bash
python setup_demo.py up        # first run builds the image - a few minutes
python setup_demo.py status    # container state + /health
python setup_demo.py down      # --volumes also removes them
```

Two settings differ from production, both on purpose and both reversible in
`.env.demo`: the questionnaire workers are disabled (they poll Redis
continuously and the Q&A demo does not use them), and the models are pinned to
`gpt-4o-mini` — the same cost-driven limit production runs under, so the numbers
on screen are the numbers you actually get.

`.env.demo` 文件中有两项设置与生产环境不同（均为有意为之且可随时改回）：一是禁用了问卷处理进程（这些进程会持续轮询 Redis，而问答演示功能并不需要它们）；二是将模型固定为 `gpt-4o-mini`——这与生产环境出于成本考量所采用的限制一致，因此屏幕上显示的数值即为您实际获得的数值。

## 2. The demo corpus - 演示语料库

`build_corpus.py` generates 25 documents for **Meridian Labs**, a fictional
organisation. The structure mirrors a real regulated document set — reference
codes (`PR-QA-MRD-009`), versions, effective dates, approvers, revision history,
cross-references between documents, and a French/English mix — so the demo
exercises the same retrieval problems as production without showing any real
content.

`build_corpus.py` 脚本为虚构组织 **Meridian Labs** 生成了 25 份文档。这些文档的结构仿照了真实的受监管文档集——包含引用代码（如 `PR-QA-MRD-009`）、版本号、生效日期、审批人、修订记录、文档间的交叉引用以及英法双语混用的内容——因此，该演示既能模拟生产环境中的检索难题，又无需展示任何真实数据内容。

| | |
|---|---|
| `corpus/md/` | source of truth, human-readable, used by `eval.py verify` |
| `corpus/pdf/` | mounted read-only into the API container at `/corpus` |

| `corpus/md/` | 权威数据源，人类可读，供 `eval.py verify` 使用 |
| `corpus/pdf/` | 以只读方式挂载至 API 容器内的 `/corpus` 目录 |

Regenerate any time; output is deterministic. Everything — organisations,
people, products, figures — is invented.

可随时重新生成；输出结果是确定性的。一切——包括组织、人物、产品和数据——均为虚构。

To change a document, edit the `DOCUMENTS` list in `build_corpus.py`, rebuild,
then run `python eval.py verify` to confirm the eval set still matches.

若要修改文档，请编辑 `build_corpus.py` 中的 `DOCUMENTS` 列表并重新构建，然后运行 `python eval.py verify` 以确认评估集依然匹配。

## 3. Indexing

```bash
python setup_demo.py ingest --dry-run   # inspect the commands first
python setup_demo.py ingest
```

Runs `ingest.py` inside the API container once per PDF, which is why no local
api environment is needed. `--runner local` runs it on the host instead, against
the published ports — that path does need api's dependencies installed.

该操作针对每个 PDF 文件在 API 容器内运行一次 `ingest.py`，因此无需配置本地 API 环境。若使用 `--runner local` 参数，则会在宿主机上运行该脚本并连接到已发布的端口——这种方式确实需要安装 API 的相关依赖。

`--recreate` is passed on the **first document only**. It drops the entire
collection, index and workspace, so passing it per document would wipe
everything indexed a moment earlier.

`--recreate` 仅在处理**第一个文档**时传入。该参数会删除整个集合、索引及工作区，因此如果针对每个文档都传入该参数，就会清除掉刚才建立的索引内容。

## 4. The eval set - 评估集

`eval_set.yaml` — version `1.1.0`, 65 questions, 59 answerable and 6 deliberately not:
`eval_set.yaml` — 版本 `1.1.0`，包含 65 个问题，其中 59 个可回答，6 个特意设为不可回答：

| Category | n | What it tests |
|---|---|---|
| `factual` | 35 | single-hop lookup of a specific figure or name |
| `reference_lookup` | 7 | exact document identifiers — where pure vector search degrades |
| `multi_hop` | 9 | answers requiring two documents |
| `cross_lingual` | 5 | English question over French source, and the reverse |
| `acronym` | 3 | glossary resolution |
| `unanswerable` | 6 | **should be refused** — measures hallucination, not recall |

| 类别 | 数量 | 考察内容 |
|---|---|---|
| `factual`（事实性） | 35 | 针对特定数值或名称的单跳（single-hop）检索 |
| `reference_lookup`（引用检索） | 7 | 精确的文档标识符检索——纯向量搜索在此类场景下效果较差 |
| `multi_hop`（多跳推理） | 9 | 需要结合两份文档才能回答的问题 |
| `cross_lingual`（跨语言） | 5 | 基于法语源文档回答英语问题，或反之 |
| `acronym`（缩写） | 3 | 术语/缩写解析 |
| `unanswerable`（无法回答） | 6 | **应拒绝回答**——用于评估“幻觉”现象，而非召回能力 |

The unanswerable set matters most on camera. Recall alone is easy to inflate; a
system that answers everything confidently scores well on recall and is useless
in a regulated context.

在实际应用场景中，那些无法给出确切答案的问题（即“不可回答”类问题）至关重要。仅凭“召回率”这一指标很容易虚高：一个对任何问题都自信作答的系统，虽然召回率表现亮眼，但在受监管的实际应用环境中却毫无用处。

### Keeping ground truth honest - 确保真实可靠

```bash
python eval.py verify
```

Offline, no API calls. Checks that every `expect_sources` document exists and
that every `must_include` token literally appears in it. Run it after any corpus
edit — it is what stops the eval set from drifting away from the documents and
quietly grading against facts that no longer exist.

离线运行，不涉及 API 调用。该工具会检查每个 `expect_sources` 文档是否存在，并确认每个 `must_include` 标记是否确实出现在该文档中。请在每次修改语料库后运行此工具——它能防止评估集与文档内容脱节，避免在事实已不复存在的情况下进行无效评分。

## 5. The harness

### Retrieval mode — the ablation - 回收模式——剔除

```bash
python eval.py run --mode retrieval --workspace meridian_demo --tag ablation
```

Calls `/api/v1/search`, which returns each backend's results separately, so one
call per question scores all four indexes independently:

调用 `/api/v1/search`，该接口会分别返回各后端的结果；因此，针对每个问题的单次调用会对全部四个索引进行独立评分：

```
Indexes enabled     Hit rate   Index alone
vector only            ...%          ...%
+ fulltext             ...%          ...%
+ summary              ...%          ...%
+ graph (approx)       ...%          ...%
```

No LLM cost, so it is cheap to re-run while tuning `--topk` and
`--similarity-threshold`. This table is the evidence that four indexes beat one.

无需支付大语言模型（LLM）费用，因此在调整 `--topk` 和 `--similarity-threshold` 参数时，重新运行的成本很低。该表格有力地证明了“四个索引优于单个索引”这一结论。

### Answer mode — the accuracy number - 回答模式——准确率数值

```bash
python eval.py --env-file .env.demo.local run --mode answer --workspace meridian_demo
```

Calls `/api/v1/qa` and scores each answer three ways: whether the expected
source documents were cited, whether the required tokens appear, and an LLM
judge verdict of `correct` / `partial` / `incorrect` against the reference
answer.

调用 `/api/v1/qa` 并从三个维度对每个答案进行评分：是否引用了预期的源文档，是否包含必要的词元（tokens），以及 LLM 评判员根据参考答案给出的“正确”（correct）、“部分正确”（partial）或“错误”（incorrect）的判定结果。

Useful flags: `--limit N`, `--category multi_hop`, `--model gpt-4.1-mini`,
`--judge-model`, `--concurrency`, `--fail-under 85`.

常用标志：`--limit N`、`--category multi_hop`、`--model gpt-4.1-mini`、
`--judge-model`、`--concurrency`、`--fail-under 85`。

Reports land in `reports/<tag>.json` (full per-question detail) and
`reports/<tag>.md` (shareable summary, including every failure with the judge's
reasoning).

报告将生成在 `reports/<tag>.json`（包含每个问题的详细信息）和 `reports/<tag>.md`（可分享的摘要，列出所有失败案例及评判依据）中。

### What the numbers mean - 这些数字的含义

Be precise about these on camera — they are what a technical viewer will probe.

在镜头前务必做到精准——因为这些正是懂行的观众会仔细审视的地方。

- **Strict accuracy** — judge verdict `correct` only. This is the headline.
  Quote this one.
- **Lenient accuracy** — `correct` + `partial`. Always higher. Say which you are
  quoting.
- **Source hit rate** — share of answerable questions where **every** expected
  document was cited. Multi-source questions need all of them; partial credit is
  tracked separately but not counted.
- **Refusal accuracy** — share of the 6 unanswerable questions correctly
  declined.
- **Hallucination rate** — unanswerable questions answered anyway.

- **严格准确率** — 仅判定结果为“正确”的情况。这是主要指标。 引用此项数据。
- **宽松准确率** — “正确”与“部分正确”之和。该数值总是更高。请说明您引用的是哪一个。
- **来源命中率** — 在可回答的问题中，引用了**所有**预期文档的比例。对于多来源问题，必须引用全部来源；部分引用情况会单独记录，但不计入此指标。
- **拒答准确率** — 针对6个不可回答的问题，正确拒绝回答的比例。
- **幻觉率** — 不可回答的问题却给出了回答的情况。

Two deliberate limitations, worth stating out loud rather than being asked:

有两处刻意设定的局限性，与其等着被问起，不如主动说明：

- **Retrieval matching uses result metadata only, never chunk body text.** The
  corpus cross-references documents, so matching on body text would credit an
  index for retrieving `PR-QA-MRD-009` when it actually returned a chunk of
  `PR-QA-MRD-001` that merely mentions it. `test_scoring.py` pins this
  behaviour.
- **The graph column is approximate.** LightRAG returns a flat context string
  rather than structured hits, so a reference found there may come from a
  cross-reference inside another document. It is reported separately and never
  merged silently into the other numbers.

- **检索匹配仅使用结果元数据，绝不使用数据块的正文内容。** 由于语料库中存在文档间的交叉引用，若基于正文内容进行匹配，可能会导致索引在实际返回 `PR-QA-MRD-001` 的数据块（其中仅提及了 `PR-QA-MRD-009`）时，却将功劳归于检索到了 `PR-QA-MRD-009`。`test_scoring.py` 明确界定了这一行为。
- **“图（graph）”列的数据为近似值。** LightRAG 返回的是扁平化的上下文字符串，而非结构化的匹配结果，因此其中发现的引用可能源自另一文档内部的交叉引用。该数据会单独列出，绝不会在后台静默合并到其他统计数值中。

### Trusting the metrics - 信任指标

```bash
python test_scoring.py
```

A wrong scorer still prints a confident percentage — just the wrong one. This
covers the retrieval scorer, the cross-reference false-positive case,
multi-source questions, source citation matching, and accent-insensitive
keyword matching. Run it before quoting any number publicly.

即使评分逻辑有误，系统仍会输出一个看似确信无疑的百分比 —— 只不过数值是错的。这涵盖了检索评分、交叉引用中的误报情形、多源问题、源引用匹配以及不区分重音符号的关键词匹配等场景。在公开引用任何数据之前，请务必先运行此检查。

---

## Before you hit record - 在开始录制之前

- [ ] `python eval.py verify` passes
- [ ] `python test_scoring.py` passes
- [ ] `setup_demo.py up` reports healthy, `setup_demo.py ingest` had no failures
- [ ] A full `eval.py run` finished and `reports/*.md` reviewed — know your
      failure cases before someone in the comments finds them
- [ ] The project stack is **stopped**, so nothing on 8000 or in a browser tab
      is serving production data
- [ ] Terminal title, shell prompt, editor tabs and browser tabs show no client
      names
- [ ] `demo/.env`, `demo/.env.demo.local` and `api/.env` are not open anywhere —
      `demo/.env` and `api/.env` hold live production secrets

- [ ] `python eval.py verify` 执行通过
- [ ] `python test_scoring.py` 执行通过
- [ ] `setup_demo.py up` 报告状态正常，`setup_demo.py ingest` 未出现错误
- [ ] 完成了完整的 `eval.py run` 并检查了 `reports/*.md` —— 务必在评论区有人指出之前，自己先了解失败案例的情况
- [ ] 项目服务栈已**停止**，确保端口 8000 或浏览器标签页中没有正在提供生产数据的内容
- [ ] 终端标题、Shell 提示符、编辑器标签页和浏览器标签页均未显示客户名称
- [ ] `demo/.env`、`demo/.env.demo.local` 和 `api/.env` 文件未在任何地方处于打开状态 —— `demo/.env` 和 `api/.env` 包含真实的生产环境机密信息
      
After recording: `python setup_demo.py down`.
