# 2026-05-08 叙事质量检查 + 重写

## Motivation
老大说："paper 吧，看一下新加的文章，确保不是陈列出来的那种写法。"
(Reviewing 5 月 scout 新加的 PBSD、TT-OPD、PRISM、CoPD、MAD-OPD、PAINT、MSD、OPSDL、GUI-SD、IRIS 等)

## 检查结果
- ✅ PRISM, CoPD, MAD-OPD, PAINT, IRIS, MSD, OPSDL, GUI-SD — 已融入叙事/递进/对比
- ⚠️ TT-OPD §5.3.1 (L697) — 陈列式消融数字,与其他 agentic OPD (TCOD/Skill-SD/MAD-OPD) 无连接 → **重写**
- ⚠️ TT-OPD §7.2 (L864) — 3 个 pathology 局部描述,未抽象 → **重写**
- ✅ PBSD §5.3.1 (L695) — 已有递进叙事,但可加强 → 补一句链接 CaOPD + epistemic suppression

## 改动 3 处

### 改动 1: §5.3.1 TT-OPD 段重写 (L697)
- 加入 granularity 光谱叙事: trajectory (TCOD) / turn (TT-OPD) / step (MAD-OPD) / skill (Skill-SD)
- TT-OPD 定位为 "填补 turn-level PI 空缺"
- Ablation 数字精简,重在说明"为何 EMA+hints 缺一不可"
- 与 §7.2 cross-reference

### 改动 2: §7.2 Agentic collapse 段重写 (L864)
- 3 个 pathology 重组为三个 emph'd 子标题:
  * teacher-dynamics collapse (连接 TCOD's Trajectory-Level KL Instability)
  * trajectory-structure erosion (连接 Skill-SD / MAD-OPD 的 granularity mismatch)
  * reward-hint runaway (连接 epistemic suppression / 2603.24472)
- 结尾抽象成一般性原理: "stable teacher dynamics + trajectory regularizers + granularity-matched credit"
  三者 jointly necessary,各方法占据不同组合

### 改动 3: §5.3.1 PBSD 段补充一句 (L695 末尾)
- 原文末尾:"preference-based targets are a more principled substitute..."
- 新增:"This post-peak decline is the same pathology that CaOPD attributes to 
  training-deployment context mismatch and that 2603.24472 diagnose as epistemic 
  suppression (§7.2), so PBSD converts these diagnostic insights into a corrective
  optimization target rather than post-hoc recalibration."

## 验证
- 编译: 56 pages, 118 citations, 0 errors (XeLaTeX)
- 所有 cross-ref (subsec:curriculum, subsec:failure, sec:applications) 有效
- 字数/页数不变 (56 页保持)
