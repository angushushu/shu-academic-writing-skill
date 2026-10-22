# shu-academic-writing-skill

> **A measured, two-pass method for academic writing: give the paper a spine, then check it without breaking the spine.**

[English](#-english) · [中文](#-中文) · [📊 Benchmark & evolution](BENCHMARK.md) · [🔬 Full evidence](EVIDENCE.md) · [📜 Changelog](CHANGELOG.md)

![version](https://img.shields.io/badge/version-1.2.5-blue)
![license](https://img.shields.io/badge/license-GPL--3.0-blue)
![python](https://img.shields.io/badge/python-3.8%2B-3776AB)
![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

A portable skill bundle for developing, revising and auditing an empirical research manuscript for a
peer-reviewed venue. Plain Markdown plus stdlib-only Python — no plugin system, no API key, no build
step. Point any agent at `SKILL.md` and it has a method.

---

## 🇬🇧 English

### Why it exists

Writing and compliance pull in opposite directions, and **the order is the product**:

| order of operations | result |
|---|---|
| write the paper, then check it | **preferred** |
| check it while writing it | **loses badly** |

The same instructions applied in the other order made every measured paper worse. So the bundle is
organised as two passes: **spine** (one argument a reader finishes) then **check** (correct the finished
file with the smallest edit).

### Quick start

```bash
git clone https://github.com/angushushu/shu-academic-writing-skill.git
cd shu-academic-writing-skill
```

1. **Copy the bundle next to your manuscript** (or use it in place).
2. **Fill in `project/`** — venue rules, authoritative numbers, claim risks. This layer is what makes
   the audit possible; without it the bundle works on argument, structure and prose only.
3. **Ask your agent to read the router:**

   > Read `SKILL.md` and follow the route it gives for revising my manuscript.

4. **Run the deterministic screens before you declare victory:**

```bash
python scripts/argument_screen.py DRAFT.md     # answer placement + Results caveats
python scripts/intake_screen.py DRAFT.md       # mechanical floor: placeholders, missing sections
python scripts/prose_lint.py DRAFT.md          # clarity and calibration tells
```

### What is inside

| module | read when |
|---|---|
| `core/problem-framing/` | Before drafting. Frame the paper as a problem in the reader's existing understanding. |
| `core/reader-layer/` | The paper is correct but hard to read. One argument, one stake, no interruptions. |
| `core/develop-manuscript/` | Planning, drafting, restructuring, substantive revision. The orchestrator. |
| `core/engineer-argument/` | The contribution or the introduction/discussion logic is the problem. |
| `core/polish-prose/` | The argument is settled and the sentences are not. |
| `core/audit-manuscript/` | Adversarial pre-submission gate; reviewer simulation. |
| `core/respond-to-reviewers/` | A decision letter has arrived. |
| `core/corpus-metrics/` | Optional: is this number unusual for the venue? Heavy dependencies. |

Seven stdlib-only Python scripts back the modules: `intake_screen`, `argument_screen`,
`check_manuscript`, `audit_draft`, `prose_lint`, `textmetrics`, `worklog`.

### Why trust it

The method was benchmarked, not just described. On two **constructed argument-damage cases** — real
papers with prose untouched and the argument damaged only (buried contribution, gap opening, broken
handoffs, limitations spliced into claims) — the current version reaches the top of both calibrated
scores, while every characterised competitor package falls short:

| test | this package | strongest characterised competitor |
|---|---|---|
| working case, property-span v2 | **1.00 ×4 artefacts** | 0.00–0.67 |
| hard review case, B1/B2/B3 | **3/3 ×4 artefacts** | 0.25 / 3 |
| same-prompt controlled comparison | **2.500 / 3** | 0.250 / 3 (15/16 cross-pairs) |

The deterministic screens were validated against the metrics: screen A agrees with the abstract property
**25/25**, screen B with the introduction-close property **29/29**. Every package change since 1.0.0 was
one pre-registered edit with a fixed acceptance/revert rule.

**Read the benchmark before quoting it.** It is a distribution on two constructed cases, not an effect
size; there is no ranking, no human anchor, and one blind reader pair went to a competitor. The full
story, including every limit, is in **[BENCHMARK.md](BENCHMARK.md)**; the raw measurement record is in
**[EVIDENCE.md](EVIDENCE.md)**.

### Scope, stated plainly

This bundle is for drafts whose **argument does not land** — contribution buried, claims outrunning
evidence, paragraphs that do not carry the reader. It is **not** a grammar checker, a citation manager,
a plagiarism detector, or a way to write a paper without doing the work. On a draft that merely needs
copy-editing it is not better than anything, and no method is (measured twice).

### License

GPL-3.0 — see `LICENSE`.

---

## 🇨🇳 中文

### 一句话

> **一个经过实测的两遍式学术写作方法：先给论文一根脊椎，再检查它而不折断脊椎。**

**shu-academic-writing-skill** 是一个可迁移的学术写作技能包，面向实证研究论文的撰写、修改与投稿前审查。
纯 Markdown + 标准库 Python：无插件系统、无 API key、无需构建。让任何 agent 读取 `SKILL.md` 即可获得完整方法。

### 为什么存在

写作与合规之间的张力方向相反，而**顺序本身就是产品**：

| 操作顺序 | 结果 |
|---|---|
| 先写论文，再检查 | **更受读者偏好** |
| 边写边检查 | **明显变差** |

同样的指令换一个顺序，会让每一篇被测论文都更差。因此本包分为两遍：**脊椎**（一个读者愿意读完的论证）+
**检查**（在完成的文件上做最小修改）。

### 快速开始

```bash
git clone https://github.com/angushushu/shu-academic-writing-skill.git
cd shu-academic-writing-skill
```

1. **把技能包放在论文旁边**（或直接使用）。
2. **填写 `project/`**——目标期刊规则、权威数字、不能支撑的论断。没有这一层，包只能处理论证、结构与文字。
3. **让 agent 读取路由文件：**

   > 读取 `SKILL.md`，按它给出的路线修改我的论文。

4. **交付前运行确定性屏幕：**

```bash
python scripts/argument_screen.py DRAFT.md     # 答案位置 + Results 中的限制句
python scripts/intake_screen.py DRAFT.md       # 机械底线：占位符、缺节
python scripts/prose_lint.py DRAFT.md          # 清晰度与校准提示
```

### 包含什么

| 模块 | 何时阅读 |
|---|---|
| `core/problem-framing/` | 动笔之前：把论文框定成读者已有理解中的问题。 |
| `core/reader-layer/` | 论文正确但难读：一个论证、一个利害、没有打断。 |
| `core/develop-manuscript/` | 规划、起草、重构、实质修改。总调度。 |
| `core/engineer-argument/` | 贡献、引言/讨论逻辑是问题时。 |
| `core/polish-prose/` | 论证已稳定、句子仍不顺时。 |
| `core/audit-manuscript/` | 投稿前的对抗性检查；审稿人模拟。 |
| `core/respond-to-reviewers/` | 收到审稿意见之后。 |
| `core/corpus-metrics/` | 可选：这个数字对该期刊是否异常？依赖较重。 |

另有 7 个仅用标准库的 Python 脚本支撑各模块：`intake_screen`、`argument_screen`、
`check_manuscript`、`audit_draft`、`prose_lint`、`textmetrics`、`worklog`。

### 为什么可以信任

方法是**实测**出来的，不只是描述。在两个**构造的论证损伤案例**上（真实论文，文字不动，只损伤论证：
贡献被埋、开头讲 gap、段落衔接断裂、限制句被塞进论断），当前版本在两个校准评分器上都达到上限，
而已刻画的竞品包都达不到：

| 测试 | 本包 | 最强的已刻画竞品 |
|---|---|---|
| 工作案例，property-span v2 | **1.00 ×4 个产物** | 0.00–0.67 |
| 硬案例（综述体裁），B1/B2/B3 | **3/3 ×4 个产物** | 0.25 / 3 |
| 同提示受控比较 | **2.500 / 3** | 0.250 / 3（16 交叉对中 15 胜） |

确定性屏幕已与指标对齐校验：screen A 与摘要属性一致 **25/25**，screen B 与引言收尾属性一致 **29/29**。
自 1.0.0 起，每一次包改动都是**预注册的单次编辑**，带固定的接受/回退判据。

**引用前请先读基准。** 这是两个构造案例上的分布，不是效应量；没有排名、没有人类锚，且有一对盲评读者
更偏好竞品。完整故事与全部边界见 **[BENCHMARK.md](BENCHMARK.md)**，原始测量记录见
**[EVIDENCE.md](EVIDENCE.md)**。

### 适用范围

本包适用于**论证没有落地**的稿件——贡献被埋、论断超出证据、段落不能把读者带下去。它**不是**语法检查器、
文献管理器、查重工具，也不能替你完成研究工作。对只需文字润色的稿件，它不比任何方法更好（已实测两次）。

### 许可

GPL-3.0 —— 见 `LICENSE`。
