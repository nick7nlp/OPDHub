# 精读 Schema v3 — 结构化检索数据库

**核心理念**: 不是写论文摘要，是把每篇论文的真实方法+全部 teacher/student 配置+实验数字扒成可检索的结构化记录。

**目标**:
1. 综述写作时直接 `WHERE primary_section='§5.3.3' AND teacher.size>=70B` 查询
2. 整体统计（"所有用 7B student 的 OPD 论文平均提升几个点？"）
3. 边界争议时凭 evidence_quote 反查
4. 后续 figure/table 配图直接从 JSON 字段渲染

---

## 完整 Schema

```json
{
  "paper_id": "2605.15113",
  "title": "Learning from Language Feedback via Variational Policy Distillation",
  "venue": "arXiv 2026 / ICLR 2026 / NeurIPS 2025 / ...",
  "authors": ["Yang Li", "..."],
  "affiliation_primary": "Salesforce / DeepSeek-AI / Tencent / ...",

  "summary": "50-80 字核心贡献",

  "method": {
    "training_loop": "训练循环结构（150字以内，pseudocode 风格）",
    "loss_formulation": "loss 函数表达式（latex 字符串）",
    "data_source": "训练数据来源",
    "key_components": ["component1", "component2", "..."]
  },

  "novelty": "创新点（独立于 method 字段，强调 vs prior work 的差异）",

  "on_policy_mechanism": {
    "student_rollout_in_training": "yes / no / unclear",
    "rollout_frequency": "per-step / per-outer-iter / once-before-training / n/a",
    "teacher_signal": "logits / reward / preference / none / self",
    "signal_source": "external-teacher / self / PI(GT) / PI(reference) / PI(demos) / verifier-RLVR / no-supervision",
    "evidence_quote": "原文摘录或伪代码 ← 没这个判定不算数"
  },

  "opd_classification": {
    "is_opd": "yes / no / analysis",
    "primary_section": "§5.3.2",
    "secondary_sections": ["§4.3", "§6.1"],
    "reasoning": "一句话说清为什么放这里"
  },

  "teacher_student_config": [
    {
      "teacher": {
        "name": "Qwen3-32B",
        "family": "Qwen3",
        "size_B": 32,
        "type": "dense / MoE",
        "moe_active_B": null,
        "vocab": "shared / cross-tokenizer",
        "is_self": false
      },
      "student": {
        "name": "Qwen3-1.7B",
        "family": "Qwen3",
        "size_B": 1.7,
        "type": "dense",
        "init_from": "base / SFT / RL-trained",
        "is_self": false
      },
      "scenario_label": "main / ablation / scaling / cross-family"
    }
  ],

  "training_setup": {
    "compute_budget": "8×H100 × 24h / 1024 GPU-hours / unspecified",
    "tokens_seen_B": 5.0,
    "context_length": 8192,
    "rollout_batch_size": 64,
    "rollout_per_iter": 8,
    "kl_coeff": 0.05,
    "rl_algorithm": "PPO / GRPO / DPO / pure-KD / n/a",
    "stabilization_tricks": ["importance-sampling", "EMA-teacher", "clip", "..."]
  },

  "benchmarks": [
    {
      "name": "MATH-500",
      "metric": "accuracy",
      "student_baseline": 36.4,
      "student_after_OPD": 41.5,
      "delta": 5.1,
      "teacher_score": 56.2,
      "gap_closed_pct": 26.0,
      "is_main_result": true
    },
    {
      "name": "GSM8K",
      "metric": "accuracy",
      "student_baseline": 78.0,
      "student_after_OPD": 82.5,
      "delta": 4.5,
      "is_main_result": false
    }
  ],

  "key_findings": [
    "main number: +5.1 on MATH-500 over baseline",
    "ablation: removing E-step drops 2.3 pts",
    "scales: 1.7B student gains > 8B student"
  ],

  "limitations": ["only tested on math reasoning", "requires verifier"],

  "ablations_summary": "哪些 component 被消融了，最大的 contributing factor 是什么",

  "compute_efficiency": {
    "teacher_inference_cost": "1× / amortized / cached / unknown",
    "speedup_vs_baseline": "1.0× / 4.0× / not-reported",
    "memory_footprint": "shared / 2× / unspecified"
  },

  "openness": {
    "code_released": "yes / no / promised",
    "code_url": "github.com/...",
    "model_released": "yes / no",
    "data_released": "yes / no"
  },

  "relevance_to_opd": "跟 OPD 的具体关系（不八股）",

  "comparable_papers": ["2306.13649", "2604.13016"],
  "citations_in_v3": 3,
  "score": 9,

  "_success": true,
  "_read_date": "2026-05-16T...",
  "_attempts": 1,
  "_schema_version": "v3"
}
```

---

## 关键改进 vs v2

| 维度 | v2 现状 | v3 新增 |
|---|---|---|
| **元数据** | 只 title | + venue / authors / affiliation |
| **方法** | 一段 method 字符串 | 拆成 training_loop / loss / data / components 4 子段 |
| **Teacher/Student** | 隐含在 method 文本里 | **list** 结构，支持多组 t/s 配置 |
| **训练参数** | 无 | compute / tokens / batch / KL / RL algo |
| **实验数字** | 无（埋在 summary 里）| benchmarks list，每条带 baseline/after/delta/teacher/gap_closed |
| **消融** | 无 | ablations_summary + key_findings |
| **效率** | 无 | speedup / memory / amortization |
| **开源** | 无 | code/model/data url 字段 |
| **关联** | 无 | comparable_papers / citations_in_v3 |

---

## 检索/统计场景

```python
# 1. 所有 §5.3.3 verifier-RLVR 的论文
{p for p, n in notes.items() if n['opd_classification']['primary_section'] == '§5.3.3'}

# 2. 用 7B 以下 student 的论文
[p for p, n in notes.items() 
 for tc in n.get('teacher_student_config', [])
 if tc['student']['size_B'] <= 7]

# 3. MATH-500 的所有结果
[(p, b['delta']) for p, n in notes.items() 
 for b in n.get('benchmarks', []) if b['name'] == 'MATH-500']

# 4. 平均 gap_closed 率
deltas = [b['gap_closed_pct'] for n in notes.values() 
          for b in n.get('benchmarks', []) if b.get('gap_closed_pct')]
mean(deltas)

# 5. 所有 cross-family 配置
[p for p, n in notes.items() 
 for tc in n.get('teacher_student_config', [])
 if tc['teacher']['family'] != tc['student']['family']]

# 6. 哪些论文报了 4× 以上 speedup
[(p, n['compute_efficiency']['speedup_vs_baseline']) for p, n in notes.items()
 if 'compute_efficiency' in n and n['compute_efficiency'].get('speedup_vs_baseline', '0').endswith('×')]
```

---

## 落地步骤

1. **定 schema 终稿**（这次讨论）
2. **改 dispatcher prompt**：让精读 LLM 按 v3 schema 输出
3. **写 migration 脚本**：把现有 53 条 v2 → v3（缺字段标 null）
4. **新精读自动用 v3**
5. **写检索工具**：`~/clawd/scripts/query_paper_notes.py` 命令行检索
6. **回填 106 篇**：先高引（cite ≥ 5）的 30 篇，再剩下的
