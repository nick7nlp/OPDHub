# 大语言模型同策略蒸馏综述（中文翻译版）

> **原文**: A Survey of On-Policy Distillation for Large Language Models  
> **作者**: Mingyang Song & Mao Zheng, Tencent  
> **说明**: 逐段翻译，公式保留 LaTeX，⚠️ 标注审查发现的问题

---

**摘要**

Knowledge distillation（知识蒸馏）已成为将推理能力和领域专业知识从前沿的 Large Language Models (LLMs)（大型语言模型）转移到更小、可部署的 student（学生模型）的主要机制。然而，当前的主导范式仍然是 off-policy（离线策略/异策略）：学生模型在教师生成的静态数据上进行训练，且在学习过程中从不接触自己产生的错误。这种训练与测试的不匹配是 exposure bias（暴露偏差）的一种表现，会导致预测错误在推理阶段 autoregressively（自回归地）累积。

On-Policy Distillation (OPD)（在线策略蒸馏/同策略蒸馏）通过让学生模型生成自己的 trajectories（轨迹），并接收教师模型对这些自生成输出的反馈来解决这个问题，从而将蒸馏奠基于 interactive imitation learning（交互式模仿学习）理论之上。尽管涵盖 divergence minimization（散度最小化）、reward-guided learning（奖励引导学习）和 self-play（自我博弈）的相关研究正在快速增长，但 OPD 领域的文献仍然呈现碎片化状态，缺乏统一的论述。

本综述首次对 LLMs 的 OPD 进行了全面的概述。我们在 on-policy（在线策略）样本上引入了一个统一的 $f$-divergence（$f$-散度）框架，并沿着三个正交维度梳理了该领域的全貌：**feedback signal**（反馈信号：基于 logit、基于结果或自我博弈）、**teacher accessibility**（教师可访问性：白盒、黑盒或无教师）以及 **loss granularity**（损失粒度：token 级别、序列级别或混合）。我们系统地分析了代表性的方法，考察了工业界的部署情况，并指出了包括 distillation scaling laws（蒸馏缩放定律）、uncertainty-aware feedback（感知不确定性的反馈）以及 agent-level distillation（智能体级别的蒸馏）在内的开放性问题。

---
> ⚠️ **审查问题：术语翻译建议**
> 原文中的 `off-policy` 和 `on-policy` 在经典的强化学习理论中标准译法为“异策略”和“同策略”。但在目前大模型（LLM）对齐与蒸馏的语境下，国内学术界和工业界也常将其翻译为“离线策略”和“在线策略”（强调数据是预先静态收集的还是模型交互实时生成的）。为了兼顾严谨性与行业习惯，译文中同时保留了这两种中文注释。

---

# 引言

大型语言模型（Large Language Models, LLMs）从根本上重塑了自然语言处理领域，并日益深刻地影响着整个人工智能领域。从数亿参数扩展到数千亿参数，诸如 GPT-4、PaLM 和 LLaMA 等模型在推理、代码生成、多语言理解和指令遵循方面展现出了卓越的能力。然而，对于大多数部署场景而言，训练和部署这些前沿模型所需的庞大计算成本仍然令人望而却步。对一个 5400 亿参数模型进行单次推理调用，其消耗的能量和产生的延迟可能比一个训练有素的 70 亿参数替代模型高出几个数量级，这使得将能力从大型教师模型转移到紧凑的学生模型不仅是令人向往的，更是经济上所必需的。知识蒸馏（Knowledge Distillation, KD）最初由 [KD, hinton2015distilling] 正式提出，即训练一个学生网络以匹配教师模型软化的输出分布，相应地，它已经从一种小众的压缩技术发展成为现代 LLM 开发流程的核心支柱。DeepSeek-R1 [DeepSeek-R1, 2501.12948] 的发布，成功地将复杂的思维链（chain-of-thought）推理能力从一个 6710 亿参数的混合专家（mixture-of-experts）教师模型转移到了参数量从 15 亿到 700 亿不等的稠密学生模型中，这说明蒸馏现在已经成为一个通用的*能力转移引擎（capability transfer engine）*，而不仅仅是一个单纯的尺寸缩减工具。

随着蒸馏的作用不断扩大，人们也越来越意识到其主导范式中存在一个根本性的瓶颈。传统的 LLM 蒸馏在本质上是异策略（off-policy）的。学生模型在一个固定的语料库上进行训练，该语料库通常是从数据分布 $\pdata$ 中采样的，或者是教师模型提前生成的，并且学生模型学习在这些预先收集的序列上复制教师模型在词元（token）级别的概率。然而，在推理阶段，学生模型必须自回归地（autoregressively）生成文本，将每个新词元条件化于其自身先前的（且可能是错误的）输出之上。训练分布与学生模型自身的生成分布之间的这种差异，造成了一种*训练-测试不匹配（train-test mismatch）*，这种不匹配会随着序列长度的增加而复合加剧。[文献, 2305.15717] 对这种失效模式进行了系统的实证演示，表明经过异策略蒸馏的学生模型在需要持续多步生成的任务上性能会急剧下降。从形式上看，这种现象是模仿学习（imitation learning）文献中被广泛研究的曝光偏差（exposure bias）的一个实例 [DAgger, ross2011reduction]，即仅在专家状态演示上训练的策略在测试时会漂移到陌生的状态，并且缺乏恢复的监督信号。对于自回归 LLM 而言，这个问题尤为严重，因为早期位置的错误会传播到整个剩余序列，而学生模型接收不到任何关于如何在这些自我诱发的分布外状态下表现的梯度信息。

同策略蒸馏（On-Policy Distillation, OPD）提供了一个原则性的解决方案。OPD 不是在静态数据集上进行训练，而是让学生模型从其自身不断演进的策略 $\ptheta$ 中采样序列，然后针对这些自我生成的轨迹征求教师模型的反馈。这种反馈可以采用多种形式，从白盒设置（white-box settings）下的完整词元级概率分布 [GKD, 2306.13649]、[MiniLLM, 2306.08543]，到仅可进行黑盒（black-box）教师访问时的标量奖励、对抗性反馈或成对偏好 [GAD, 2511.10643]、[Lion, 2305.12870]，甚至在无教师框架中自我生成的对比信号 [SPIN, 2401.01335]。其理论动机直接来源于交互式模仿学习。DAgger 算法 [DAgger, ross2011reduction] 确立了在学习者自身访问过的状态上查询专家，可以将纯行为克隆（behavior cloning）下 $O(T^2)$ 的复合误差降低到 $O(T)$，其中 $T$ 是视野长度。OPD 将这一原则实例化用于自回归语言生成，将蒸馏从单次分布匹配转化为迭代的、自我校正的优化循环。近年来，这种范式催生了一波方法论创新的浪潮。GKD [GKD, 2306.13649] 引入了同策略采样，并具有学生和教师序列之间可配置的混合比例。MiniLLM [MiniLLM, 2306.08543] 通过最小化逆 KL 散度（reverse KL divergence）重构了目标函数，以避免前向 KL（forward KL）的模式覆盖病理（mode-covering pathology）。DistiLLM [DistiLLM, 2402.03898] 提出了一种倾斜逆 KL（skewed reverse KL）目标，通过混合学生和教师分布来稳定模式寻求（mode-seeking）优化。RLKD [RLKD, 2505.16142] 引入了带有结构感知奖励模型的强化学习（reinforcement learning），以捕获单纯的分布匹配无法转移的推理模式。SPIN [SPIN, 2401.01335] 证明了即使完全没有教师模型，学生模型也可以通过区分自身生成的内容与人类参考内容来获得提升。

尽管发展迅速，但 OPD 文献仍然处于碎片化状态。源自知识蒸馏社区、基于人类反馈的强化学习（reinforcement learning from human feedback, RLHF）社区以及模仿学习社区的方法，通常使用不同的形式化表达、不同的评估协议和不同的术语来解决相同的潜在问题。现有的 LLM 蒸馏综述 [综述, 2402.13116] 主要围绕经典的压缩框架来组织该领域，将异策略和同策略方法视为可互换的变体，而不是具有不同理论保证和失效模式的本质上截然不同的范式。迄今为止，还没有综述对连接这些看似不相关的工作流的同策略动态进行统一的数学处理，也没有任何综述系统地比较过白盒、黑盒和无教师的 LLM 同策略学习实例化之间的权衡。

本综述填补了这一空白。我们首次对大型语言模型的同策略蒸馏进行了专门且全面的探讨，并围绕具有理论动机的分类法进行了组织。我们的贡献如下：
*   **统一的理论框架。** 我们通过序列决策（sequential decision-making）和在学生采样的轨迹上最小化 $f$-散度（$f$-divergence）的视角，公式化了从异策略到同策略蒸馏的过渡。该框架揭示了 GKD [GKD, 2306.13649]、MiniLLM [MiniLLM, 2306.08543] 和 DistiLLM [DistiLLM, 2402.03898] 如何在不同的散度选择和采样混合系数下实例化相同的底层目标，为比较以前被孤立研究的方法提供了一种通用的分析语言。
*   **三维分类法。** 我们沿三个正交轴组织 OPD 方法，即*反馈信号*（基于逻辑值（logit-based）的分布匹配、基于结果的标量或偏好信号，或自我博弈（self-play））、*教师可访问性*（白盒逻辑值访问、黑盒仅生成访问，或完全无教师的自蒸馏（self-distillation）），以及*损失粒度*（词元级、序列级或混合/自适应）。该分类法厘清了设计空间，并揭示了代表有前景的研究方向的尚未被充分探索的组合。
*   **连接白盒和黑盒机制。** 我们系统比较了需要完整教师内部信息的同策略方法与仅使用采样输出运行的方法，通过 GAD [GAD, 2511.10643] 和 Lion [Lion, 2305.12870] 等代表性方法，分析了从完整概率分布学习与从 top-$k$ 生成学习之间的理论信息差距。
*   **识别被忽视的挑战。** 我们强调了几个尚未得到充分关注的问题，包括在线生成（online generation）中的计算-质量权衡（compute-quality trade-off）、在学生低置信度状态下查询教师时的“回声室”效应（echo chamber effect）、在不同训练阶段动态调整散度的需求，以及将蒸馏重新概念化为结构化能力转移而非参数级压缩的必要性。
*   **未来研究路线图。** 我们规划了开放性问题，包括蒸馏的缩放定律（scaling laws）、感知不确定性的 OPD、课程驱动（curriculum-driven）的采样策略，以及模型必须从与外部环境的多轮、依赖状态的交互中学习的智能体级蒸馏（agent-level distillation）。

本综述的其余部分组织如下。第 \ref{sec:background} 节建立了数学预备知识，将自回归生成形式化为序列决策问题，并推导了促使同策略方法产生的曝光偏差。第 \ref{sec:taxonomy} 节详细介绍了我们的三维分类法。第 \ref{sec:white_box} 节深入分析了白盒 OPD 方法，第 \ref{sec:black_box} 节涵盖了黑盒和自蒸馏方法。第 \ref{sec:reasoning} 节探讨了特定于推理的蒸馏流程。第 \ref{sec:systems} 节讨论了工业部署的注意事项和实践指南，第 \ref{sec:future} 节指出了开放性问题和未来方向。

> ⚠️ 审查问题：
> 1. 原文引用的 arXiv 编号 `2511.10643` 似乎有误（年份月份对应 2025 年 11 月，大概率为 `2411.10643` 的笔误），建议核实。
> 2. 原文引用的 arXiv 编号 `2505.16142` 似乎有误（年份月份对应 2025 年 5 月，大概率为 `2405.16142` 的笔误），建议核实。

---

# 背景与预备知识

为了弥合从标准的、绑定数据集的 Knowledge Distillation（知识蒸馏）到动态的 On-Policy Distillation（同策略蒸馏）之间的鸿沟，我们首先对 LLM（大语言模型）生成的序列特性进行了形式化。本节定义了 distribution matching（分布匹配），对 exposure bias（曝光偏差）进行了形式化，并使用 f-divergence family（f-散度族）构建了一个框架。

**符号说明。** 我们使用小写字母 $p$ 表示 token-level（词元级）条件分布（例如 $\pteacher(\cdot|x, y_{<t})$，$\ptheta(\cdot|x, y_{<t})$），使用大写字母 $P$ 表示 sequence-level（序列级）或 trajectory-level（轨迹级）分布（例如 $P_{\mathcal{T}}(y|x)$，$P_\theta(y|x)$）。在 exposure bias（曝光偏差）的 MDP（马尔可夫决策过程）形式化（第 \ref{subsec:exposure_bias} 节）中，我们使用 $\pi$ 表示策略。在详细讨论各个单独的方法时，为了便于理解，我们会沿用各篇论文的符号（例如，在第 \ref{subsec:token_level} 节的 divergence analysis（散度分析）中，用 $p_S/p_T$ 表示学生/教师；在第 \ref{sec:reasoning} 节的 reasoning distillation（推理蒸馏）中，使用 $P_\theta/P_{\text{Teacher}}$）。

> ⚠️ 审查问题：公式中包含了自定义 LaTeX 宏 `\pteacher` 和 `\ptheta`，在标准 Markdown 渲染器中可能无法正常解析渲染，建议确保目标编译环境中已定义这些宏。

---

### Knowledge Distillation 基础

由 [Knowledge Distillation, hinton2015distilling] 开创的经典 Knowledge Distillation（知识蒸馏）框架，将隐含在庞大的 teacher network（教师网络）$\mathcal{T}$ 的连续概率分布中的“dark knowledge”（暗知识）转移到紧凑的 student network（学生网络）$\mathcal{S}$ 中。在标准的分类任务中，进而扩展到语言建模中的 token-level（词元级别）词表选择中，神经网络会生成一个 pre-softmax logits（未经过 softmax 归一化的逻辑值）向量 $z \in \mathbb{R}^{|V|}$，其中 $|V|$ 是词表大小。

为了提取类别之间的关系结构（例如，词元“automobile”在语义上比“apple”更接近“car”），需要使用 temperature scalar（温度标量）$\tau > 0$ 对 logits 进行平滑处理。对于给定的输入上下文 $x$，其 softened probability（软化概率）为：

$$
    p(y|x; \tau) = \frac{\exp(z_y / \tau)}{\sum_{y' \in V} \exp(z_{y'} / \tau)}
$$

标准的 Knowledge Distillation 目标旨在最小化教师的软化预测分布 $\pteacher$ 与学生相应的软化分布 $\ptheta$ 之间的 Kullback-Leibler (KL) divergence（KL 散度）：

$$
    \loss_{\mathrm{KD}} = \tau^2 \KL(\pteacher(\cdot|x; \tau) \parallel \ptheta(\cdot|x; \tau)) = \tau^2 \sum_{y \in V} \pteacher(y|x; \tau) \log \left( \frac{\pteacher(y|x; \tau)}{\ptheta(y|x; \tau)} \right)
$$

$\tau^2$ 缩放因子非常重要，因为随着 $\tau$ 的增加，交叉熵梯度的大小会按 $1/\tau^2$ 缩放，因此乘以 $\tau^2$ 可以使蒸馏损失在联合目标中与 hard-label cross-entropy（硬标签交叉熵）保持相称。

为了理解这种转移过程，我们分析蒸馏损失相对于学生 logits $z_i^{\mathcal{S}}$ 的梯度。令 $p_i^{\mathcal{T}}$ 和 $p_i^{\mathcal{S}}$ 分别表示经过温度缩放的教师和学生概率。该梯度为：

$$
    \frac{\partial \loss_{\mathrm{KD}}}{\partial z_i^{\mathcal{S}}} = \frac{\tau^2}{\tau} (p_i^{\mathcal{S}} - p_i^{\mathcal{T}}) = \tau (p_i^{\mathcal{S}} - p_i^{\mathcal{T}})
$$

当 $\tau \to \infty$ 时，通过 Taylor expansion（泰勒展开）$\exp(z_i/\tau) \approx 1 + z_i/\tau$ 可以看出，在假设 zero-meaned logits（零均值逻辑值，即 $\sum_j z_j = 0$）的情况下，概率趋近于：

$$
    p_i \approx \frac{1 + z_i/\tau}{|V| + \sum_j z_j/\tau} = \frac{1}{|V|} + \frac{z_i}{|V|\tau}
$$

将其代回梯度公式中，可以揭示出一种等价关系：

$$
    \frac{\partial \loss_{\mathrm{KD}}}{\partial z_i^{\mathcal{S}}} \approx \tau \left( \frac{z_i^{\mathcal{S}}}{|V|\tau} - \frac{z_i^{\mathcal{T}}}{|V|\tau} \right) = \frac{1}{|V|} (z_i^{\mathcal{S}} - z_i^{\mathcal{T}})
$$

这一推导表明，在高温极限下，经典的 Knowledge Distillation 退化为最小化 raw logits（原始逻辑值）之间的 Mean Squared Error (MSE)（均方误差）。这迫使学生网络复制教师网络的整个 logit 结构，同时转移 primary predictive modes（主要预测模式）和构成泛化基础的微妙的 sub-optimal probability masses（次优概率质量，即暗知识）。然而，当把这种形式化方法简单粗暴地应用于 autoregressive LLMs（自回归大语言模型）时，它假设输入 $x$（前缀）是从目标数据分布中提取的，完全忽略了语言生成所具有的 sequential, compounding nature（序列化累积特性）。

> ⚠️ **审查问题**：
> 1. 公式中包含了原作者自定义的 LaTeX 宏命令（如 `\pteacher`、`\ptheta`、`\loss`、`\KL`）。按照“公式保留 LaTeX”的规则，这些宏命令已被原样保留。但在标准的 Markdown 渲染器（如 MathJax 或 KaTeX）中，如果不预先在前端定义这些宏，会导致这部分公式无法正常渲染。
> 2. 原文中的 `\label{subsec:kd_fundamentals}` 属于 LaTeX 内部交叉引用标签，在 Markdown 中通常通过标题自动生成锚点，因此在翻译中已将其省略。

---

### Token-Level vs. Sequence-Level Distillation（词元级与序列级蒸馏）

将 [Knowledge Distillation, hinton2015distilling] 的公式应用于语言建模通常会产生 Token-Level Distillation（词元级蒸馏）。在 autoregressive（自回归）设置中，序列 $y = (y_1, y_2, \dots, y_T)$ 是按条件生成的。令 $y_{<t}$ 表示直至第 $t$ 步的 prefix（前缀）。词元级蒸馏的 loss（损失）是经验数据集 $\mathcal{D}$ 的前缀上的 expected divergence（期望散度）。
$$
    \loss_{\mathrm{Token-KD}} = \mathbb{E}_{x, y \sim \mathcal{D}} \left[ \sum_{t=1}^{|y|} \KL(\pteacher(\cdot | x, y_{<t}) \parallel \ptheta(\cdot | x, y_{<t})) \right]
$$

尽管 Token-Level KD 在计算上是 tractable（易处理的/可行的），因为它依赖于静态的、预先计算的前缀，但它与 global generative objective（全局生成目标）并不对齐，因为它在优化 next-token accuracy（下一词元准确率）的同时，假设了一个无误差的历史记录 $y_{<t}$。

认识到这一局限性后，[Sequence-Level Knowledge Distillation, kim2016sequence] 提出了 Sequence-Level Knowledge Distillation（序列级知识蒸馏）。Sequence-Level KD 并没有在固定的数据集前缀上逐个词元（token-by-token）地分解损失，而是旨在匹配整个序列空间 $\mathcal{Y}$ 上的 joint probability distributions（联合概率分布）。理论上的序列级目标最小化了全局 KL divergence（KL 散度）：
$$
    \loss_{\mathrm{Seq-KD}} = \KL(P_{\mathcal{T}}(y | x) \parallel P_{\theta}(y | x)) = \sum_{y \in \mathcal{Y}} P_{\mathcal{T}}(y | x) \log \left( \frac{P_{\mathcal{T}}(y | x)}{P_{\theta}(y | x)} \right)
$$

由于序列空间 $\mathcal{Y}$ 随长度 $T$ 呈指数增长（$|\mathcal{Y}| = |V|^T$），精确计算这一求和是 intractable（难以处理的）。[Sequence-Level Knowledge Distillation, kim2016sequence] 务实地解决了这个问题。他们观察到 $P_{\mathcal{T}}(y|x)$ 在其 mode（众数/峰值）附近呈现尖峰，因此他们在 beam-search（束搜索）输出处使用 Dirac delta（狄拉克 $\delta$ 函数）来近似该分布：
$$
    P_{\mathcal{T}}(y | x) \approx \begin{cases} 
      1 & \text{if } y = \arg\max_{y' \in \mathcal{Y}} P_{\mathcal{T}}(y' | x) \\
      0 & \text{otherwise} 
   \end{cases}
$$

将此近似代入序列级 KL 散度中，可将损失简化为 student（学生模型）的标准 negative log-likelihood (NLL)（负对数似然），并在 teacher（教师模型）的最高概率序列 $\hat{y}$ 上进行评估：
$$
    \loss_{\mathrm{Seq-Approx}} = - \sum_{t=1}^{|\hat{y}|} \log \ptheta(\hat{y}_t | x, \hat{y}_{<t})
$$

这种公式迫使学生模型去建模教师模型所偏好的完整 trajectories（轨迹），隐含地传递了序列级的 structural dependencies（结构依赖）。然而，Sequence-Level KD 仍然是一种 *off-policy*（离轨/异策略）算法。学生模型仍然通过在静态轨迹（由教师模型离线生成的 pseudo-labels（伪标签））上进行 teacher-forcing（教师强制）来训练。虽然目标 $\hat{y}$ 源于模型而非人类，但学生模型在训练期间从未将其预测条件建立在自己的前缀上。因此，Sequence-Level KD 仍然容易受到它试图缓解的 train-test mismatch（训练-测试不匹配）的影响，这激发了真正的 on-policy（同轨/同策略）算法的研究。

> ⚠️ **审查问题**：
> 1. 原文中使用 `\citet` 进行作者级别的引用（如 `\citet{kim2016sequence} resolved...` 意为“Kim 等人解决了...”），为严格遵守“`[方法名, cite_key]`”的引用格式规则，译文中直接替换为了方法名。这在中文语境下作主语时可能略显生硬（例如“[Sequence-Level Knowledge Distillation, kim2016sequence] 务实地解决了这个问题”）。建议根据最终排版需求确认是否需要补全作者名（如“Kim 等人 [Sequence-Level Knowledge Distillation, kim2016sequence]”）。
> 2. 公式中的 `\loss`, `\pteacher`, `\ptheta` 等属于自定义 LaTeX 宏，已严格按照要求保留原样，在未加载对应宏包的 Markdown 渲染器中可能会显示为源码。

---

### 1.1 分布不匹配问题与曝光偏差 (Exposure Bias)

促使 On-Policy Distillation（同策略蒸馏）成为必然的核心问题是*曝光偏差*（exposure bias，指模型在训练和推理时所面临的输入分布不一致的问题），这是序列决策（sequential decision-making）中协变量偏移（covariate shift，指训练集与测试集的输入分布发生改变）的直接体现。我们将自回归生成（autoregressive generation）建模为马尔可夫决策过程（Markov Decision Process, 简称 MDP）。状态空间（state space）$\mathcal{S}$ 包含所有的词元前缀（token prefixes）$s_t = (x, y_{<t})$，动作空间（action space）$\mathcal{A}$ 是词表（vocabulary）$V$，且状态转移是确定性的（deterministic）；在状态 $s_t$ 下执行动作 $y_t$ 会产生 $s_{t+1} = (x, y_{<t}, y_t)$。

在异策略蒸馏（off-policy distillation，通常指 teacher-forcing，即“教师强制”：训练时强行使用真实数据的上一词元作为当前输入）期间，学生模型遇到的状态受数据分布 $\pdata$ 控制。将数据集策略下的状态访问分布（state visitation distribution）定义为 $d_{\mathcal{D}}(s)$，则训练目标为：
$$
    \loss_{\mathrm{train}} = \mathbb{E}_{s \sim d_{\mathcal{D}}} \left[ \KL(\pi^*(\cdot|s) \parallel \pi_\theta(\cdot|s)) \right]
$$

然而，在推理（inference）阶段，学生模型根据其自身学习到的策略 $\pi_\theta$ 采取动作。由于学生模型并不完美，其动作会偏离数据集分布。令 $d_{\pi_\theta}(s)$ 表示由学生模型自身的 rollouts（展开/生成轨迹，指模型基于自身策略连续生成序列的过程）引发的状态访问分布。真实的生成质量是在这个截然不同的分布下进行评估的：
$$
    \loss_{\mathrm{test}} = \mathbb{E}_{s \sim d_{\pi_\theta}} \left[ \loss_{\mathrm{task}}(s, \pi_\theta) \right]
$$

曝光偏差源于不等式 $d_{\mathcal{D}}(s) \neq d_{\pi_\theta}(s)$。由于学生模型在训练期间从未遇到过位于 $d_{\pi_\theta}(s) \setminus d_{\mathcal{D}}(s)$ 中的状态，因此它在这些区域接收到的监督信号为零。

我们使用模仿学习（imitation learning）中的性能界限（performance bounds）来量化这种不匹配。正如 [DAgger, ross2011reduction] 通过 DAgger 分析所展示的，如果学生策略 $\pi_\theta$ 模仿教师策略 $\pi^*$，且在训练分布下的单步误差（per-step error）以 $\epsilon$ 为界，即 $\mathbb{E}_{s \sim d_{\pi^*}}[\mathbb{I}(\pi_\theta(s) \neq \pi^*(s))] \le \epsilon$，那么在学生自身分布下，长度为 $T$ 的轨迹上的预期总差异将呈二次方（quadratically）增长：
$$
    \mathbb{E}_{s \sim d_{\pi_\theta}} \left[ \sum_{t=1}^T \mathcal{L}(s_t) \right] \le O(\epsilon T^2)
$$

这种 $O(T^2)$ 的累积界限（compounding bound）对于现代 LLM（大语言模型）来说意义重大，因为它们通常会生成跨越数千个词元的序列。一个单一的次优（suboptimal）词元就会使前缀略微偏离分布（out-of-distribution）；模型由于从未见过这种受扰动的前缀（perturbed prefix），更有可能再次出错，从而导致文本质量下降或产生幻觉文本（hallucinatory text）。On-Policy Distillation 通过将训练期望从 $\mathbb{E}_{s \sim d_{\mathcal{D}}}$ 更改为 $\mathbb{E}_{s \sim d_{\pi_\theta}}$ 来解决这个问题。通过在线（online，指在训练过程中实时进行）生成回复，学生模型会直面自己的错误，在那些特定的分布外状态上接收教师的反馈，并学习鲁棒的恢复行为（recovery behaviors），从而将误差积累从 $O(\epsilon T^2)$ 降低到 $O(\epsilon T)$。

**备注：LLM 中 DAgger 界限的微妙之处。** 虽然从 $O(\epsilon T^2)$ 到 $O(\epsilon T)$ 的理论转变极具吸引力，但将 DAgger 界限应用于 LLM 需要细致入微的考量。最初的 DAgger 定理假设存在一个能在任何状态下提供最优动作（optimal actions）的*交互式专家（interactive expert）*。在白盒 OPD（white-box OPD，指白盒同策略蒸馏）中，“专家”提供的是以学生前缀 $\hat{y}_{<t}$ 为条件的下一词元分布（conditional distribution）$\pteacher(y_t | \hat{y}_{<t})$。如果学生模型幻象出一个严重的分布外前缀，教师模型的条件分布本身可能会变得校准不良（poorly calibrated）。强制学生模型匹配这种噪声分布（noisy distribution）违反了交互式模仿学习的核心假设，这不仅无法恢复 $O(\epsilon T)$ 的界限，反而可能破坏训练的稳定性。这突显了为什么自适应散度方法（adaptive divergence methods，见第 \ref{subsec:token_level} 节）对于选择性地信任教师模型至关重要。

这种模仿学习的视角（在学生模型的 rollouts 上训练，用教师模型的反馈进行监督）直接启发了现代 LLM 蒸馏方法。[GKD, 2306.13649] 和 [DistiLLM, 2402.03898] 将这种 DAgger 风格的模式推广到了大型语言模型环境中，用十亿参数级的模型取代了 NMT（神经机器翻译）规模的架构，并引入了散度感知（divergence-aware）的训练目标。

> ⚠️ **审查问题：**
> 1. 原文 LaTeX 代码中使用了自定义宏命令（如 `\pdata`, `\loss`, `\pteacher`, `\KL`）。在标准的 Markdown 渲染器中，如果没有预先定义这些宏，公式可能会渲染失败。建议在实际使用时将它们替换为标准 LaTeX 语法（例如将 `\loss` 替换为 `\mathcal{L}`，`\pdata` 替换为 `p_{\mathrm{data}}`），或在 Markdown 渲染环境中补充宏定义。
> 2. 原文引用的 `[方法名, cite_key]` 映射中，`\citet{ross2011reduction}` 根据上下文被译作了 `[DAgger, ross2011reduction]`，`\citep{2306.13649}` 与 `\citep{2402.03898}` 被分别对应到了 `[GKD, 2306.13649]` 和 `[DistiLLM, 2402.03898]` 以严格符合您的格式要求。

---

### f-散度族与几何直觉

为了在 OPD（On-Policy Distillation，同策略蒸馏）中对分布匹配进行参数化，我们依赖于 f-divergence（f-散度）框架。给定空间 $\mathcal{X}$ 上的两个概率分布 $P$ 和 $Q$，f-divergence 通过一个满足 $f(1) = 0$ 的凸生成函数（convex generator）$f: (0, \infty) \to \mathbb{R}$ 来衡量它们的差异：

$$
    D_f(P \parallel Q) = \int_{\mathcal{X}} Q(x) f\left(\frac{P(x)}{Q(x)}\right) dx = \mathbb{E}_{x \sim Q} \left[ f\left(\frac{P(x)}{Q(x)}\right) \right]
$$

$f(u)$ 的选择会赋予蒸馏目标不同的性质。在 LLM（大型语言模型）蒸馏中，我们设定 $P \equiv \pteacher$（教师）且 $Q \equiv \ptheta$（学生），其中 token（词元）级别的符号与我们在第 \ref{subsec:kd_fundamentals} 节中的约定保持一致。

**1. Forward Kullback-Leibler Divergence（前向 KL 散度）。** 选择 $f(u) = u \log u$ 即可得到 Forward KL，即 $\KL(P \parallel Q) = \mathbb{E}_{x \sim P} [ \log(P(x)/Q(x)) ]$。其梯度会迫使学生 $Q$ 在教师 $P$ 具有概率质量（probability mass）的所有位置分配质量。如果 $P(x) > 0$ 但 $Q(x) \approx 0$，惩罚项将趋于发散。因此，Forward KL 具有强烈的 *mode-covering*（模式覆盖 / 避零）特性。在 LLM 蒸馏中，由于参数量较小的学生模型无法记忆教师庞大的分布，覆盖所有模式（modes）会导致概率分散到有效模式之间的空白区域，从而生成毫无意义的、平均化的文本表达。

**2. Reverse Kullback-Leibler Divergence（反向 KL 散度）。** 选择 $f(u) = -\log u$ 即可得到 Reverse KL，即 $\KL(Q \parallel P) = \mathbb{E}_{x \sim Q} [ \log(Q(x)/P(x)) ]$。这里的期望是基于学生 $Q$ 计算的。如果在 $P(x) \approx 0$ 的区域出现 $Q(x) > 0$，惩罚项将趋于发散。因此，学生模型只会向教师模型支持的区域分配概率，从而表现出 *mode-seeking*（模式寻求 / 促零）行为，即坍缩（collapsing）到某一个主要模式上，同时忽略次要模式。对于生成式语言任务而言，这种特性是理想的，因为生成一个连贯的回答远比生成多个正确回答的语无伦次混合体要好。

**3. Jensen-Shannon Divergence (JSD，Jensen-Shannon 散度)。** JSD 通过衡量与混合分布 $M = \frac{1}{2}(P + Q)$ 的散度引入了对称性。通过使用 $f(u) = \frac{1}{2}\left[u \log\left(\frac{2u}{u+1}\right) + \log\left(\frac{2}{u+1}\right)\right]$，JSD 的取值被限制在 $[0, \log 2]$ 范围内。这提供了一个稳定的梯度场，能够平衡 mode-seeking 和 mode-covering 行为，从而防止在分布外（out-of-distribution）区域出现极端的梯度爆炸。

> **图 1 注**：Forward KL 与 Reverse KL 散度在将学生分布 $P_S$ 拟合到双峰教师 $P_T$ 时的对比。（a）具有双峰（bimodal）的教师分布。（b）Forward KL 表现为 mean-seeking（均值寻求）：学生模型覆盖了两个模式，但在模式间的“幻觉区（hallucination zone）”也分配了概率质量。（c）Reverse KL 表现为 mode-seeking（模式寻求）：学生模型集中在单一峰上，完全舍弃了另一个模式。自适应方法（如 ToDi、Entropy-Aware OPD）会根据教师模型的置信度在两者之间进行动态切换。*(注：原文 TikZ 图代码已省略)*

**4. Total Variation Distance (TVD，总变差距离)。** 使用 $f(u) = \frac{1}{2}|u-1|$，TVD 衡量的是任意事件上的最大绝对概率差异，即 $\sup_{A} |P(A) - Q(A)|$。无论对数概率比（log-probability ratios）多么极端，TVD 都能提供一个鲁棒的距离度量，不过其在 $u=1$ 处的不可导性给神经网络空间中的直接优化带来了挑战。从这个 f-divergence 族中作出的选择，决定了学生模型在 on-policy（同策略）生成过程中如何对教师模型的知识进行插值（interpolate）。

---
> ⚠️ **审查问题：** 
> 原文公式中存在自定义的 LaTeX 宏（`\pteacher`、`\ptheta` 和 `\KL`）。在标准 Markdown 渲染器中，除非预先配置了 MathJax/KaTeX 的宏定义，否则这些符号可能会渲染失败。建议在实际发布时将其替换为标准 LaTeX 写法（例如将 `\KL` 替换为 `\text{KL}`，`\pteacher` 替换为 `P_{\text{teacher}}` 等）。

---

## 现代 OPD 的统一数学视角

最近的 OPD（在策略蒸馏，On-Policy Distillation）方法可以通过将采样分布（sampling distribution，决定轨迹）与散度度量（divergence metric，决定局部的 token 级别匹配）解耦，统一到一个单一的目标函数下。广义的 OPD 目标为
$$
    \loss_{\mathrm{OPD}}(\theta) = \mathbb{E}_{y \sim \pi_{\mathrm{mix}}} \left[ \sum_{t=1}^{|y|} \mathcal{D}_f \left( \pteacher(\cdot | x, y_{<t}) \parallel \ptheta(\cdot | x, y_{<t}) \right) \right]
$$
其中 $\pi_{\mathrm{mix}}$ 是驱动状态探索（state exploration）的行为策略（behavioral policy），而 $\mathcal{D}_f$ 是选定的 f-散度（f-divergence）。关键的现代方法（[GKD, 2306.13649]、[MiniLLM, 2306.08543] 和 [DistiLLM, 2402.03898]）都可以映射到这个等式上，作为连续理论空间中的不同参数化形式。

**Generalized Knowledge Distillation (GKD) [GKD, 2306.13649]。** GKD 通过将 $\pi_{\mathrm{mix}}$ 定义为数据集和学生模型的在策略分布（on-policy distribution）之间的显式插值（explicit interpolation），来解决轨迹不匹配（trajectory mismatch）问题。输出序列以 $\lambda$ 的概率从 $\ptheta$ 中抽取，以 $1-\lambda$ 的概率从 $\mathcal{D}$ 中抽取。GKD 在 $\mathcal{D}_f$ 的选择上具有灵活性，在实验中测试了前向 KL 散度（Forward KL）、反向 KL 散度（Reverse KL）和 JS 散度（JSD）。将 $\lambda \to 1$ 会使得 GKD 变成纯粹的在策略方法。

**MiniLLM [MiniLLM, 2306.08543]。** MiniLLM 发现前向 KL 散度会强制对教师模型的长尾（long tail）分布进行过度分配。为了强制实现寻模行为（mode-seeking behavior），它选择了反向 KL 散度（$\mathcal{D}_f = \KL(\ptheta \parallel \pteacher)$）。在采样方面，MiniLLM 采用了一种混合教师策略（teacher-mixed strategy），即以 $\alpha = 0.2$ 的概率从教师模型中抽取 token，以缓解奖励作弊（reward hacking）问题，从而使得 $\pi_{\mathrm{mix}} = (1 - \alpha)\ptheta + \alpha \pteacher$。由于反向 KL 散度将学生参数同时置于期望（expectation）和对数比率（log-ratio）中，MiniLLM 通过策略梯度定理（Policy Gradient theorem，即 REINFORCE）重新构建了优化过程，将教师模型的对数概率视为奖励（reward）。定义累积未来奖励（cumulative reward-to-go）为 $R_t = \sum_{t'=t}^{|y|} \log \frac{\pteacher(y_{t'}|y_{<t'})}{\ptheta(y_{t'}|y_{<t'})}$，梯度变为：
$$
    \nabla_\theta \mathcal{L}_{\mathrm{MiniLLM}} = -\mathbb{E}_{y \sim \ptheta} \left[ \sum_{t=1}^{|y|} \left( R_t - 1 \right) \nabla_\theta \log \ptheta(y_t|y_{<t}) \right]
$$
为了缓解策略梯度的高方差（high variance）问题，MiniLLM 将 $R_t$ 分解为单步奖励（single-step reward）$r_t = \log \frac{\pteacher(y_t|y_{<t})}{\ptheta(y_t|y_{<t})}$ 加上未来回报（future return），从而启用了逐 token 基线（per-token baselines），将强化学习（RL）优化与知识蒸馏（knowledge distillation）连接起来。

**DistiLLM [DistiLLM, 2402.03898]。** 尽管 MiniLLM 在理论上实现了寻模行为，但对高方差强化学习的依赖导致了经验上的不稳定性（empirical instability）。DistiLLM 通过倾斜反向 KL 散度（Skewed Reverse KL divergence）解决了这个问题。它定义了一个倾斜混合分布（skewed mixture）$\tilde{p} = \alpha \pteacher + (1-\alpha) \ptheta$ 并最小化 $\KL(\ptheta \parallel \tilde{p})$，这继承了反向 KL 散度的寻模几何特性（mode-seeking geometry），同时避免了当 $\ptheta(y) > 0$ 但 $\pteacher(y) \approx 0$ 时的除零不稳定性（zero-division instability），因为只要 $\ptheta$ 非零，混合分布 $\tilde{p}$ 就总是非零的。这允许在不使用策略梯度的情况下进行标准的交叉熵（cross-entropy）优化。在我们的统一视角下，DistiLLM 保持了 $\pi_{\mathrm{mix}} = \ptheta$，但为了易处理性（tractability）和稳定性重新参数化了 $\mathcal{D}_f$。

这一统一的视角表明，现代 OPD 并不是一系列互不相关的启发式方法（disparate heuristics），而是对控制轨迹采样（trajectory sampling）和几何分布匹配（geometric distribution matching）的边界进行系统性、渐进式收紧的过程。

> ⚠️ 审查问题：公式 (1) 中使用了 `\loss_{\mathrm{OPD}}(\theta)`，而在后续 MiniLLM 的公式 (2) 中使用了 `\mathcal{L}_{\mathrm{MiniLLM}}`。`\loss` 并非 LaTeX 的标准内置命令（通常为作者自定义的宏），若未在导言区定义可能会导致独立编译时报错，且上下文对于损失函数的符号表示（`\loss` 与 `\mathcal{L}`）不够统一。

---

# 在线策略蒸馏的分类体系

为了梳理不断扩展的 OPD（On-Policy Distillation，在线策略蒸馏）文献，我们提出了一种多维度的分类体系。我们并未根据发布的时间顺序或微小的架构差异对方法进行分类，而是沿着三个基本维度对其进行划分：（1）**反馈信号（Feedback Signal）**，决定了哪些信息从教师模型流向学生模型；（2）**教师访问权限（Teacher Access）**，反映了教师模型在部署上的限制条件；以及（3）**粒度（Granularity）**，描述了蒸馏损失（Distillation Loss）的时间分辨率。

该分类体系的结构层级关系在图 \ref{fig:taxonomy_tree} 中进行了可视化展示。

> ⚠️ 审查问题：原 LaTeX 代码中包含了复杂的 TikZ 绘图代码（用于绘制分类树状图），标准 Markdown 无法直接渲染此类图形代码，因此译文中省略了该代码块，仅保留了图注的翻译。

**图 \ref{fig:taxonomy_tree}**：大型语言模型在线策略蒸馏的分类体系。方法论空间沿着三个正交维度（Orthogonal dimensions，即相互独立的分类标准）与代表性方法进行了组织。由于这些坐标轴是相互独立的，单一方法可能会跨越并出现在多个类别中。

---

### 3.1 反馈信号 (Feedback Signal)

OPD 算法之间的主要区别在于用于纠正同策略（on-policy）偏差的监督信号（supervisory signal）。我们将这一空间划分为三种范式（paradigms）。

**基于 Logit 的反馈 (Logit-Based Feedback)。** 学生模型生成的序列会逐词元（token-by-token）地与教师模型的连续概率分布（continuous probability distribution）进行评估。像 [GKD, 2306.13649] 和 [MiniLLM, 2306.08543] 等方法在每个生成步骤计算 f-散度（f-divergences）。最近的工作，例如 [ToDi, 2505.16297]，使用源自师生对数概率比（log-probability ratio）的 sigmoid 权重，自适应地结合每个 token 的前向与反向 KL 散度（Forward and Reverse KL）。基于 Logit 的反馈提供了最密集的梯度信号，因为在每个时间步 $t$，损失向量的大小为 $|V|$，从而确保学生模型能够捕捉到教师模型精确的决策边界（decision boundaries）。

**基于结果的反馈 (Outcome-Based Feedback)。** 随着模型规模的扩大，计算完整的 logit 变得极其困难。基于结果的方法用评估生成轨迹（trajectory）正确性的标量奖励信号（scalar reward signals）取代了精确的 token 匹配。像 [RLKD, 2505.16142] 这样的框架让学生模型展开（roll out）完整的答案，并从奖励模型或验证器（verifier）接收奖励 $R(x, y)$。优化过程通过策略梯度方法（policy gradient methods）或直接偏好优化（Direct Preference Optimization, DPO）进行，将目标从散度最小化转变为奖励最大化：$\max_\theta \mathbb{E}_{y \sim \ptheta} [R(x, y)] - \beta \KL(\ptheta \parallel p_{\mathrm{ref}})$。这赋予了学生模型寻找达到正确结果的新路径的自由，而无需模仿教师模型特定的措辞。

**自我对弈反馈 (Self-Play Feedback)。** 在无教师对齐（teacher-free alignment）中，自我对弈从学生模型自身不断演进的策略（evolving policy）中构建反馈。[SPIN, 2401.01335] 模拟了一个双人博弈，在迭代 $t$ 时，模型将其自身的输出与人类编写的参考文本区分开来，其对数似然差距（log-likelihood gap）提供了一个不断锐化的训练信号。同策略自我蒸馏（On-Policy Self-Distillation）[OPSD, 2601.18734] 采用了一种不同的方法：通过利用特权信息（privileged information），单个模型同时充当教师和学生；教师变体以真实答案（ground-truth answer）为条件，为学生生成的展开轨迹提供密集的 token 级别监督。随着学生模型的改进，这两种范式在没有持续的外部教师干预的情况下，提供了自然扩展的课程（naturally scaling curricula）。

---

> ⚠️ **审查问题：**
> 1. **自定义 LaTeX 宏：** 第三段公式中的 `\ptheta` 和 `\KL` 属于作者在原 LaTeX 导言区自定义的宏命令（通常代表 $p_\theta$ 和 $\text{KL}$）。在标准的 Markdown 渲染器中直接使用可能会导致公式解析失败，建议在最终发布时替换为标准 LaTeX 语法（如 `p_\theta` 和 `\text{KL}`）。
> 2. **疑似年份错误：** 最后一段引用的 OPSD 论文编号为 `2601.18734`。如果这是基于 arXiv 的编号规则（YYMM.NNNNN），“2601” 意味着 2026 年 1 月，这在当前时间节点可能是一个笔误，请核对原文或文献来源是否应为 `2401` 或 `2501`。

---

### 教师模型的访问权限

前沿模型（frontier models）的部署约束严重限制了蒸馏的执行方式。教师模型内部状态的可用性决定了允许使用的数学公式（mathematical formulations）。

**白盒蒸馏（White-Box Distillation）。** 当可以访问完整的教师模型权重时，算法会执行精确的解析散度匹配（analytical divergence matching）。[DistiLLM, 2402.03898] 利用完整的 logit 张量（logit tensor）进行偏斜 KL 优化（skewed KL optimization）。白盒访问权限使得利用暗知识（dark knowledge）成为可能，因为错误 token 上微小的概率也带有结构化正则化（structural regularization）的益处。然而，在内存中同时维护一个庞大的教师模型（例如 70B 参数）和学生模型，需要大量的工程工作和大型计算集群。

**黑盒蒸馏（Black-Box Distillation）。** 前沿模型（例如 GPT-4、Claude）的闭源性质通常将其访问权限限制在 API 级别，仅返回硬 argmax 文本（hard-argmax text，即直接输出概率最高的文本）。黑盒同策略蒸馏（On-Policy Distillation, OPD）必须创造性地近似教师模型的分布。[Lion, 2305.12870] 将教师模型同时用作偏好标注器（preference annotator）和课程设计器（curriculum designer）。学生模型生成同策略候选（on-policy candidates），教师模型识别其弱点并创建更难的指令。Generative Adversarial Distillation (GAD) [GAD, 2511.10643] 通过训练一个判别器（discriminator）来区分学生模型生成的文本和 API 输出，从而隐式地对教师模型的分布进行建模，完全避开了对 logit 的需求。

**自蒸馏（Self-Distillation）。** 当不存在更优的教师模型时，模型会自举（bootstraps）其自身的能力。自蒸馏将稳定的历史检查点（stabilized historical checkpoint）或通过 dropout 集成的版本作为教师模型。通过生成同策略响应并通过自我评估（self-evaluation）对其进行过滤（如 [SPIN, 2401.01335] 所示），模型在没有外部参数依赖的情况下优化其分布。

最近的一项扩展工作 [OPSDC, 2603.05433] 将同策略自蒸馏专门应用于推理压缩（reasoning compression）；同一个模型既充当教师（以“保持简洁（be concise）”的指令为条件），又充当学生，在学生模型自身的生成轨迹（rollouts）上最小化逐 token 的反向 KL 散度（reverse KL）。这在各个基准测试中将推理轨迹长度（reasoning trace length）减少了 41--59%（在 MATH-500 上为 57--59%，在 AIME 2024 上为 41%），同时保持或提高了准确率，解决了蒸馏后的推理模型通常会产生不必要冗长推理链的实际问题。

[GATES, 2602.20574] 解决了在没有真实标签（ground-truth labels）或外部验证器（external verifiers）环境下的自蒸馏问题。单个模型既充当导师模型（tutor，在训练期间可以访问相关的源文档），又充当学生模型（在测试时仅根据问题进行回答）。GATES 并没有假设导师模型是正确的，而是从多个样本中导师模型的共识（consensus）里在线获取监督信号，通过门控机制（gating）调节蒸馏信号以抑制不可靠的监督。

[SDPO, 2601.20802] 引入了自蒸馏策略优化（Self-Distillation Policy Optimization），它通过利用丰富的文本反馈（rich textual feedback，例如编译器错误、测试输出、裁判评估）而不是标量奖励（scalar rewards），在强化学习（RL）和自蒸馏之间架起了桥梁。模型生成同策略的轨迹，接收结构化文本反馈（structured textual feedback），并利用这些反馈通过自蒸馏创建密集的逐 token 学习信号（dense token-level learning signals），其中以反馈为条件的当前模型充当无条件学生策略的教师。这解决了困扰标准 RLVR 的信用分配瓶颈（credit-assignment bottleneck），在标准 RLVR 中，二元奖励无法提供关于哪一步导致失败的信号。在科学推理、工具使用和竞争性编程方面，SDPO 在样本效率（sample efficiency）和最终准确率上都超越了强大的 RLVR 基线模型。

[Privileged Information Distillation, 2602.04942] 通过形式化训练时特权信息（privileged information, PI）在蒸馏中的作用，推广了 GATES 范式。虽然学生模型在测试时必须在没有 PI 的情况下运行（例如，在不访问源文档的情况下回答问题），但以 PI 为条件的同一模型的教师变体可以生成高质量的监督信号。其核心贡献在于证明了这种特权自蒸馏框架在基础模型没有 PI 就无法解决问题的困难、长视野强化学习环境（long-horizon RL settings）中特别有效，从而扩大了适用同策略自蒸馏的任务范围。

> ⚠️ 审查问题：原文中 `RLVR` 的全称未给出。在相关文献语境中，通常指代 "Reinforcement Learning with Verifiable Rewards"（带有可验证奖励的强化学习），此处已作为专有名词缩写直接保留，读者需结合上下文理解。

---

### 粒度 (Granularity)

蒸馏损失（distillation loss，指用于指导学生模型学习教师模型输出分布的损失函数）的时间分辨率（temporal resolution）决定了学生模型是学习到了复杂的推理，还是仅仅在进行风格模仿。

**Token-Level Granularity（词元级粒度）。** 损失在每个时间步 $t$ 进行计算，为每个动作 $y_t$ 提供即时的局部反馈。这确保了稳定的梯度和快速的收敛，但存在短视（myopia）的问题；在教师模型的局部分布下概率较低的词元（token），可能是一条有效的替代推理路径的最佳起点。

**Sequence-Level Granularity（序列级粒度）。** 信号仅在生成终止时施加，通常通过 Outcome Reward Models（结果奖励模型）来实现。虽然这赋予了模型极大的自由度去探索替代结构，但梯度极其稀疏。信用分配（Credit assignment，强化学习术语，指将最终结果的奖励合理分配给中间各个步骤的过程）问题十分严峻；一个包含 1000 个词元的证明如果在第 999 步失败，将获得统一的负奖励，从而无法强化前面 998 个正确的步骤。

**Hybrid / Adaptive Granularity（混合/自适应粒度）。** 为了弥合词元级短视和序列级稀疏性之间的鸿沟，最近的方法将密集的词元级监督与步骤级（step-level）或轨迹级（trajectory-level）奖励信号结合起来。Process Reward Models (PRMs) [Process Reward Models, 2305.20050] 提供对中间推理的逐步验证，实现了纯词元级或纯序列级方法都无法达到的细粒度信用分配。SuperCorrect [SuperCorrect, 2410.09008] 利用从教师模型中提取的层次化思维模板来引导步骤级推理蒸馏，并结合跨模型 DPO（Direct Preference Optimization，直接偏好优化）进行自我纠错。这些混合粒度方法平衡了密集词元反馈的稳定性与步骤级评估的结构感知能力，从而能够更有效地蒸馏复杂的推理链。

---

# 白盒 On-Policy 方法
\label{sec:white_box}

On-Policy Distillation (OPD，同策略蒸馏) 的决定性特征不在于散度度量（divergence metric）的选择，而在于控制训练的分布：传统的 off-policy KD（异策略知识蒸馏）强制学生模型在教师模型的边缘分布（marginal distribution） $\pteacher(x,y)$ 下模仿教师，而 OPD 则将采样权交还给学生模型自身不断演进的策略 $\ptheta(x,y)$。这种转变消除了曝光偏差（exposure bias，指模型在训练和推理阶段面临的数据分布不一致导致误差累积的问题），但也引入了新的挑战：如何在学生（而非教师）生成的轨迹（trajectories）上，高效且稳定地对齐教师模型密集的 logit（逻辑值，即模型输出的未经过归一化的预测分数）信号。

白盒方法具有强大的优势：能够完全访问教师模型的概率分布，从而在每个解码步（decoding step）提供密集的、token 级别（词元级别）的反馈。本节将通过四个小节来追溯白盒 OPD 的技术演进。第 \ref{subsec:token_level} 节涵盖了 token 级别散度最小化（token-level divergence minimization）这一最活跃的研究方向，并围绕三条概念主线展开：从固定散度到自适应散度的演进、token 权重分配与选择的正交维度，以及跨架构蒸馏。第 \ref{subsec:sequence_level} 节探讨了将蒸馏重新构建为强化学习（reinforcement learning）的序列级别（sequence-level）方法。第 \ref{subsec:hybrid} 节综述了弥合粒度鸿沟（granularity gap）并解决实际瓶颈的混合方法。第 \ref{subsec:theory_whitebox} 节对理论分析进行了汇总。

> ⚠️ 审查问题：公式中的 `\pteacher` 和 `\ptheta` 似乎是原作者自定义的 LaTeX 宏（macros）。在脱离原论文 LaTeX 环境的 Markdown 渲染器中可能无法正常显示（通常应为 `p_{\text{teacher}}` 和 `p_{\theta}`），但遵循“公式保留 LaTeX”的规则，此处原样保留了这些宏。

---

## 2.1 Token级别散度最小化 (Token-Level Divergence Minimization)

Token级方法允许学生模型生成轨迹（trajectories） $y_{<t} \sim \ptheta$，然后在每个位置最小化教师和学生分布之间的散度（divergence）。散度的选择严重影响稳定性、收敛性以及下游任务的质量。正如在第 \ref{subsec:unified_view} 节的统一框架中所确立的，所有这些方法都实例化了一个由采样策略（sampling policy） $\pi_{\mathrm{mix}}$ 和一个 $f$-散度 $\mathcal{D}_f$ 参数化的共同目标。与其孤立地回顾每种方法，我们围绕捕捉该领域技术演进的三个概念主线来组织本小节。

### 从固定散度到自适应散度

在Token级 OPD（On-Policy Distillation，同策略蒸馏）中，最基本的设计轴是用于衡量教师-学生不匹配程度的散度函数。该领域已经从固定的、全局应用的散度发展到越来越自适应的、上下文敏感的公式。

**基线：带有同策略采样的均匀散度。**
[GKD, 2306.13649] 通过引入混合采样策略 $\pi_{\mathrm{mix}}$ 确立了规范的同策略蒸馏框架，该策略在数据集和学生模型自身的生成结果之间进行插值，由学生数据比例 $\lambda \in [0,1]$ 控制：
$$
    \mathcal{L}_{GKD} = \mathbb{E}_{x \sim \mathcal{D},\; y \sim \pi_{\mathrm{mix}}(\cdot|x)} \left[ \sum_{t=1}^{|y|} D\big( \pteacher(\cdot|x, y_{<t}) \parallel \ptheta(\cdot|x, y_{<t}) \big) \right]
$$
其中 $D$ 可以是正向 KL（Forward KL）、反向 KL（Reverse KL）或 JSD（Jensen-Shannon Divergence，杰森-香农散度）。GKD 默认使用 JSD，因为其具有有界且对称的梯度，提供了一个安全的通用选择。设置 $\lambda=1$ 会产生纯粹的同策略训练；$\lambda=0$ 则恢复为标准的异策略 KD（Off-policy KD）。虽然与异策略基线相比，GKD 极大地缓解了复合误差（compounding errors），但单一的全局固定散度无法适应序列中各个 Token 之间不同的难度级别。

**通过插值稳定反向 KL。**
[DistiLLM, 2402.03898] 解决了反向 KL 的一个特定失效模式：当教师模型对学生生成的 Token 分配接近零的概率时，梯度会爆炸。解决方案是一个倾斜的混合目标（skewed mixture target） $\tilde{p} = \alpha \pteacher + (1{-}\alpha)\ptheta$，它保证了在学生模型具有概率质量的任何地方都具有非零密度：
$$
    \mathcal{L}_{DistiLLM} = \mathbb{E}_{y \sim \ptheta} \left[ \sum_t \KL\big(\ptheta(\cdot|y_{<t}) \parallel \alpha \pteacher(\cdot|y_{<t}) + (1{-}\alpha) \ptheta(\cdot|y_{<t})\big) \right]
$$
这继承了反向 KL 的求众数（mode-seeking）几何特性，同时无需策略梯度（policy gradients）即可实现标准的交叉熵优化（cross-entropy optimization），从而获得更快、更稳定的收敛。在此基础之上，[DistiLLM-2, 2503.07067] 观察到教师生成的输出和学生生成的输出受益于*不同的*损失函数：对教师的输出应用倾斜 KL（Skew KL）以增加学生模型生成高质量回复的可能性，而对学生的输出应用倾斜反向 KL（Skew Reverse KL）以降低生成低质量内容的可能性。这种对比的不对称性，结合基于课程（curriculum-based）的自适应系数和基于投机解码（speculative-decoding-based）的数据集筛选，在指令遵循、代码生成和数学推理等任务中，在 Token 级蒸馏方法中达到了最先进（state-of-the-art）的结果。

**逐 Token 自适应散度。**
GKD 和 DistiLLM 的主要局限性在于它们对所有 Token 均匀地应用相同的散度。[ToDi, 2505.16297] 认为序列中的不同位置需要不同的匹配严格度：关键的推理转折点需要严格的反向 KL，而句法填充词则可以容忍宽松的正向 KL。ToDi 使用基于 Sigmoid 的权重（由教师-学生对数概率比得出），在每个位置自适应地结合正向和反向 KL：
$$
    \mathcal{L}_{ToDi} = \mathbb{E}_{y \sim \ptheta} \left[ \sum_t \omega_t D_{f^{(t)}} \big( \pteacher(\cdot|y_{<t}) \parallel \ptheta(\cdot|y_{<t}) \big) \right]
$$
当该比率表明学生模型低估了教师模型的高置信度预测时，反向 KL 占主导地位以抑制错误；当教师模型的分布更加不确定时，正向 KL 贡献更多以保持多样性。由此产生的逐 Token 自适应性代表了相对于全局固定散度的质的飞跃，尽管它通过 $\omega_t$ 的启发式计算引入了架构上的复杂性。

**平衡分布的头部和尾部。**
[AKL, 2404.02657] 挑战了反向 KL 在 LLM（大语言模型）蒸馏中绝对优越的传统观念。通过理论分析和实验，[AKL, 2404.02657] 证明了反向 KL 和正向 KL 的求众数和求均值（mean-seeking）特征在 LLM 的离散分布中并不成立，并且在给定足够的训练轮数（epochs）下，两种散度会收敛到相同的目标。然而，在实际的轮数预算下，正向 KL 将学习集中在教师分布的头部，而反向 KL 则集中在尾部。AKL 根据当前教师和学生的分布，自适应地分配权重以结合这两种散度，在有限的训练预算下实现了更优的对齐（alignment）。这种头尾分析通过提供散度选择的分布视角而非位置视角，补充了 ToDi 的逐 Token 自适应方法。

**熵门控的散度切换。**
[Entropy-Aware OPD, 2603.07079] 发现了一个互补的失效模式：当教师分布具有高熵（对正确的后续内容存在真正的物理不确定性）时，反向 KL 的求众数特性迫使学生模型任意选择许多同样合理的模式之一，从而丢弃了有价值的分布信息并产生不稳定的学习信号。解决方案是熵门控（entropy-gated）混合：
$$
\begin{split}
    \mathcal{L}_{Ent\text{-}OPD} = \mathbb{E}_{y \sim \ptheta} \bigg[ \sum_t (1 - \alpha_t) \KL\big(\ptheta(\cdot|y_{<t}) \parallel \pteacher(\cdot|y_{<t})\big) \\
    + \alpha_t \KL\big(\pteacher(\cdot|y_{<t}) \parallel \ptheta(\cdot|y_{<t})\big) \bigg]
\end{split}
$$
其中 $\alpha_t$ 随着教师的熵 $\mathcal{H}(\pteacher(\cdot|y_{<t}))$ 的增加而增加。在低熵区域（自信的预测），反向 KL 在精确模仿中占据主导地位；在高熵区域，正向 KL 捕捉各种合理的输出。在 Qwen3-4B-Base 上，与标准反向 KL 相比，它在数学推理上实现了 +5.05 Pass@8 的提升，使其成为抵御分布偏移（distribution shifts）最稳健的 Token 级策略之一，尽管它需要在每一步计算教师的熵。
> ⚠️ 审查问题：年份和模型名称存在异常。引用键 `2603.07079` 和 `2602.12125` 暗示了2026年的论文，且提及了 `Qwen3-4B-Base`。这可能是原文中的笔误（如将 25xx 错写为 26xx），或者是来自尚未发表的草稿/合成文本，建议核对 LaTeX 原文的准确性。

**作为 KL 约束强化学习的 OPD。**
[G-OPD, 2602.12125] 提供了一个统一的理论视角，证明了标准 OPD 是密集的 KL 约束强化学习（KL-constrained RL）的特例：最小化教师和学生之间的同策略 KL 散度等价于最大化 Token 级奖励（由教师的对数概率得出），同时受制于针对参考策略的 KL 惩罚。通过将参考模型与教师模型解耦，并引入奖励缩放因子 $\alpha$，G-OPD 泛化了该框架。当 $\alpha = 1$ 时，它恢复为标准 OPD；当 $\alpha > 1$（ExOPD）时，学生模型被激励去*超越*教师的分布，打破了限制标准蒸馏的模仿天花板（imitation ceiling）。在实证方面，ExOPD 使得学生模型在数学推理基准测试中能够超越教师的性能。

### Token 权重分配与选择

与散度选择正交的问题是*哪些 Token 最重要*。标准的 OPD 目标对所有位置一视同仁，忽略了某些 Token（如推理步骤、罕见词汇）比其他 Token（如冠词、标点符号）承载着多得多的信息。

---

[AdaKD, 2510.11615] 根据学生当前的学情（learning state）动态调整每个 token（词元）的蒸馏权重，在学生-教师差距较大且学生置信度较低的 token 上增加权重。[SelecTKD, 2510.24021] 则采取了互补的方法，基于 token 的学习价值对其进行选择和重新加权，并过滤掉对知识迁移贡献甚微的 token。这两种方法都实现了一种类似课程学习（curriculum-like）的策略，在不修改底层散度（divergence）的情况下提高了蒸馏效率。

一个更激进的突破是具体分数蒸馏（Concrete Score Distillation, [CSD, 2509.25837]），它完全挑战了基于 softmax 的概率匹配范式。通过直接对 logits（逻辑值/未归一化的预测分数）而不是概率进行操作，CSD 避免了由 softmax 归一化引入的信息损失，并捕捉了教师输出分布中更丰富的结构关系，为所有基于 KL（Kullback-Leibler 散度）的目标提供了一个有理论基础的替代方案。

### 跨架构蒸馏

传统的白盒 KD（Knowledge Distillation，知识蒸馏）假设教师和学生共享相同的词表（vocabulary）和表示空间（representation space），而这一假设在实践中越来越容易被打破（例如，将 Llama 蒸馏到 Qwen 中）。

双空间知识蒸馏（Dual Space Knowledge Distillation, [DSKD, 2504.11426]）通过引入两个投影器（projectors）来解决这个问题，这两个投影器将教师的隐藏状态（hidden states）映射到学生的表示空间中，反之亦然，从而使两个模型能够共享预测头（prediction heads）以进行分布比较：
$$
    \mathcal{L}_{DSKD} = \KL(P_{T \to S} \parallel P_S) + \KL(P_{S \to T} \parallel P_T)
$$
其中 $P_{T \to S}$ 表示投影到学生空间并通过学生预测头解码的教师隐藏状态。一种精确的 token 对齐算法通过在不同分词器（tokenizers）之间对齐相同的 token 来处理词表不匹配的问题。在指令遵循（instruction following）、数学推理和代码生成方面，DSKD 始终优于标准的白盒 KD，尽管双空间公式使内存开销（memory overhead）大约增加了一倍。

[Delta KD, 2509.14526] 采用了一种不同的方法来解决容量差距（capacity gap）问题。它不是对齐绝对分布，而是保留了教师在监督微调（supervised fine-tuning, SFT）期间发生的*分布偏移*（distributional shift）。通过构建一个捕捉从预训练教师到微调教师转换过程的目标分布 $\pi_s^*$，学生学会了重现相对变化而不是绝对输出，从而在压缩到更小的模型时改善了知识迁移，其代价是需要同时提供预训练和微调模型的检查点（checkpoints）。

### 跨方法分析

**为什么不同的方法使用不同的散度？**
在 token 级别的方法中，散度的选择并不是随意的；每种选择都反映了对特定失效模式（failure modes）的深思熟虑。[GKD, 2306.13649] 默认使用 JSD（Jensen-Shannon Divergence，JS 散度）以获得有界且对称的梯度。[DistiLLM, 2402.03898] 采用偏向逆 KL（Skew Reverse KL），因为当教师对学生生成的 token 赋予接近零的概率时，标准逆 KL（Reverse KL）会产生梯度尖峰（gradient spikes）。[ToDi, 2505.16297] 和 [Entropy-Aware OPD, 2603.07079]（OPD 即 On-Policy Distillation，同策略蒸馏）认为最优散度在单个序列*内*是变化的，并据此进行自适应调整。在经验上，这些设计选择体现在特定任务的优势中：在数学推理基准测试（GSM8K, MATH）中，逆 KL 变体始终优于正向 KL（Forward KL），因为寻峰行为（mode-seeking behavior）防止了学生在不同的求解策略之间进行平均；在开放式生成任务（MT-Bench, AlpacaEval）中，正向 KL 和 JSD 保留了创造性和对话性回复所需的多样性。从业者应该根据下游任务对模式丢弃（mode-dropping）与幻觉（hallucination）的容忍度来匹配他们的散度选择（见图~\ref{fig:forward_vs_reverse_kl}）。

**更深层的几何视角。**
正向/逆向 KL 的二分法虽然具有指导意义，但掩盖了一个更微妙的几何现实。在正向 KL 下，学生的分布被拉向教师概率质量的*质心*（centroid），对于多峰分布（multimodal distributions）而言，该质心位于模式（modes，即峰值）之间的低密度区域，这就解释了幻觉这种病理现象。在逆向 KL 下，学生坍缩到一个单一的高密度模式上，产生自信但狭隘的输出。JSD 描绘出一条部分覆盖多个模式而没有完全局限于任何一个模式的路径，这解释了在经验中观察到的其“万金油”（jack-of-all-trades）行为。

这一视角也阐明了为什么自适应散度（如 ToDi、AKL、Entropy-Aware）在实践中始终优于固定散度。在推理关键（reasoning-critical）的 token 处，教师的分布通常是单峰的（unimodal），逆 KL 能很好地对齐。在生成灵活（generation-flexible）的 token 处（例如，在“therefore”和“thus”之间进行选择），分布在同义词上接近均匀分布，而正向 KL 保留了这种多样性。自适应方法隐式地检测这种模态结构（modality structure）并相应地进行切换，从而实现了两全其美。

表~\ref{tab:white_box_comparison} 提供了白盒方法的详细多维比较。表~\ref{tab:experimental_configs} 提供了所有调查方法的实验配置。

| **方法** | **年份** | **粒度** | **散度** | **访问权限** | **同策略形式 (On-Policy Formulation)** | **核心创新** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [GKD, 2306.13649] | 2024 | Token | F-KL / R-KL / JSD | 白盒 | 学生推演 (Student Rollouts) | 统一的同策略蒸馏 (OPD) 框架 |
| [G-OPD, 2602.12125] | 2026 | Token | KL 约束的 RL | 白盒 | 奖励外推 (Reward Extrapolation) | 将 OPD 视为 RL；学生超越教师 |
| [MiniLLM, 2306.08543] | 2024 | Seq. (序列) | Reverse KL | 白盒 | REINFORCE | 序列级奖励 |
| [DistiLLM, 2402.03898] | 2024 | Token | Skew R-KL | 白盒 | 插值 (Interpolated) | 针对 Reverse KL 的 $\alpha$-平滑 |
| [DistiLLM-2, 2503.07067] | 2025 | Token | 对比 SKL/SRKL | 白盒 | 批处理同策略 (Batched On-Policy) | 针对每种数据类型的非对称损失 |
| [PromptKD, 2402.12842] | 2024 | Token | Forward KL | 白盒 | 提示生成 (Prompted Generation) | 上下文桥接容量差距 |
| [AKL, 2404.02657] | 2025 | Token | Adaptive KL | 白盒 | FKL+RKL 加权 | 头尾自适应组合 |
| [DSKD, 2504.11426] | 2025 | Token | Dual-Space KL | 白盒 | 跨空间投影 (Cross-Space Projection) | 词表无关的 KD |
| [Delta KD, 2509.14526] | 2025 | Token | Delta Logit | 白盒 | SFT 偏移保留 | 分布偏移迁移 |
| [ToDi, 2505.16297] | 2025 | Token | 动态 $f$-散度 | 白盒 | Token 重要性 (Token-Significance) | 逐 Token 的散度选择 |
| [Constrained, 2509.22921] | 2025 | Seq. (序列) | Constrained KL | 白盒 | 状态增强 CMDP | 带有硬 KL 约束的奖励感知蒸馏 |
| [Entropy-Aware, 2603.07079] | 2026 | Token | 自适应 FKL+RKL | 白盒 | 熵自适应 (Entropy-Adaptive) | 高熵鲁棒性 |
| [Fast OPD, 2602.15260] | 2026 | Hybrid (混合) | 前缀上的 R-KL | 白盒 | 前缀截断 (Prefix-Truncated) | 推理前缀重用 |
| [PACED, 2603.11178] | 2026 | Hybrid (混合) | 自适应 | 白盒 | 前沿课程 (Frontier Curriculum) | 学生能力边界 |
| [$\mathcal{X}$-KD, 2602.12674] | 2026 | Hybrid (混合) | AVRIL + KL | 白盒 | 奖励引导 (Reward-Guided) | 教师环境重建 |
| [AdaSwitch, 2510.07842] | 2025 | Hybrid (混合) | KL (自适应) | 白盒 | 一次性切换 (One-time Switch) | 自适应同策略/离策略切换 |
| [TAID, 2501.16937] | 2025 | Hybrid (混合) | Forward KL | 白盒 | 分布插值 (Distribution Interpolation) | 时间自适应的容量桥接 |
| [CSD, 2509.25837] | 2026 | Token | 分数匹配 (Score Matching) | 白盒 | Logit 级别 | 无 Softmax 的 Logit 蒸馏 |
| [AdaKD, 2510.11615] | 2025 | Token | 加权 KL | 白盒 | Token 加权 (Token Weighting) | 自适应 Token 重要性 |
| [SelecTKD, 2510.24021] | 2025 | Token | 选择性 KL | 白盒 | Token 选择 (Token Selection) | 质量感知的 Token 过滤 |
| [REOPOLD, 2603.11137] | 2026 | Token | 奖励截断 R-KL | 白盒 | 放松模仿 (Relaxed Imitation) | 将 OPD 作为策略优化 |
| [TSD-KD, 2603.13260] | 2026 | Token | 双重 KD (间接 + 直接) | 白盒 | 学生重排序 (Student Re-ranking) | Token 选择性的以学生为中心 |
| [DASD, 2601.09088] | 2026 | Seq. (序列) | 分布对齐 | 白盒 | 同策略校正 (On-policy Correction) | 用于序列 KD 的分布对齐 |
| [DDT, 2602.12222] | 2026 | Seq. (序列) | IDFT + 提示解码 | 白盒 | 分布对齐 SFT | 同策略 SFT 理论 |

*表注：白盒同策略蒸馏（white-box on-policy distillation）方法的全面比较。*

---

代表性 on-policy distillation（同策略蒸馏）方法的实验配置。“Self” 表示 self-distillation（自蒸馏），即同一个模型同时作为 teacher（教师）和 student（学生）。破折号表示原论文中未提供的信息。

| **方法 (Method)** | **教师 (Teacher)** | **学生 (Student)** | **损失 / 目标 (Loss / Objective)** | **主要任务 (Primary Tasks)** |
| :--- | :--- | :--- | :--- | :--- |
| **White-Box Token-Level（白盒词元级）** | | | | |
| [GKD, 2306.13649] | T5-XL (3B) | T5-Small (60M) / Base (220M) / Large (770M) | F-KL（前向 KL 散度） / R-KL（反向 KL 散度） / JSD（Jensen-Shannon 散度） | XSum, WMT, GSM8K |
| [G-OPD, 2602.12125] | Qwen3-4B / 30B-A3B | Qwen3-1.7B / 4B | KL-constrained RL（KL 约束的强化学习） ($\lambda{=}1.25$) | AIME, MATH, HumanEval |
| [DistiLLM, 2402.03898] | GPT-2 XL (1.5B), OpenLLaMA-7B | GPT-2 (124M), OpenLLaMA-3B | Skew R-KL（偏斜反向 KL 散度） ($\alpha{=}0.1$) | Dolly, S-NI, XSum |
| [DistiLLM-2, 2503.07067] | Gemma-2-9B-Inst, Mistral-7B-Inst | Gemma-2-2B, Danube2-1.8B | Contrastive（对比）SKL/SRKL | AlpacaEval, GSM8K, HumanEval |
| [ToDi, 2505.16297] | GPT2-1.5B, Llama-2-7B | GPT2-120M, TinyLlama-1.1B | Token-adaptive（词元自适应） F-KL/R-KL | Dolly, S-NI, VicunaEval |
| [AKL, 2404.02657] | GPT-2 1.5B, LLaMA 6.7B | GPT-2 120M, TinyLlama 1.1B | Adaptive（自适应） F-KL/R-KL blend（混合） | Dolly, S-NI, UnNI |
| [Delta KD, 2509.14526] | Qwen2.5-7B / 7B-Inst | Qwen2.5-1.5B | Delta logit KL（增量逻辑 KL 散度） | GSM8K, MATH, Dolly |
| [Entropy-Aware, 2603.07079] | Qwen3-8B | Qwen3-0.6B/1.7B/4B-Base | Entropy-gated（熵门控） R-KL/F-KL | AIME, MATH, MMLU |
| [AdaKD, 2510.11615] | Qwen2-7B, OpenLLaMA-7B | Qwen2-1.5B, OpenLLaMA-3B | Adaptive token weighting（自适应词元权重） | Dolly, S-NI, UnNI |
| [SelecTKD, 2510.24021] | Qwen2-7B-Inst, Gemma-2-9B-IT | Qwen2-1.5B-Inst, Gemma-2-2B-IT | Selective token KL（选择性词元 KL 散度） | AlpacaEval, GSM8K, HumanEval |
| [CSD, 2509.25837] | GPT-2 XL (1.5B), OpenLLaMA-7B | GPT-2 (120M), OpenLLaMA-3B | Concrete score distillation（具体分数蒸馏） | Instruction following（指令遵循） |
| [DSKD, 2504.11426] | Qwen2.5-7B-Inst, Qwen2.5-Math-7B | Qwen2.5-1.5B, Llama-3.2-1B | Dual-Space KL（双空间 KL 散度） | Instruction following, Reasoning（推理）, Code |
| [REOPOLD, 2603.11137] | Qwen3-32B | Qwen3-7B | Reward-clipped（奖励截断） R-KL | AIME, Math, Visual reasoning（视觉推理） |
| [TSD-KD, 2603.13260] | Qwen2.5-14B-Inst | Qwen2.5-1.5B-Inst | Token-selective dual KD（词元选择性双重 KD） | Math, Code, Science |
| **White-Box Sequence-Level（白盒序列级） & Hybrid（混合）** | | | | |
| [MiniLLM, 2306.08543] | GPT-2 1.5B, OPT-13B, LLaMA-13B | GPT-2 120M--760M, OPT 1.3B--6.7B, LLaMA 7B | Seq-level R-KL (REINFORCE) | Instruction following |
| [Constrained, 2509.22921] | Qwen2.5-7B-Math | Qwen2.5-1.5B-Math | CMDP（约束马尔可夫决策过程） (reward + KL constraint) | MATH, GSM8K |
| [Fast OPD, 2602.15260] | Qwen3-8B | Qwen3-1.7B / 8B-Base | R-KL on prefix only（仅在原词缀上的 R-KL） | AIME, MATH, LiveCode |
| [PromptKD, 2402.12842] | GPT-2 XL (1.5B), OPT-13B | GPT-2 120M--340M, OPT-1.3B | F-KL + prompt tuning（提示微调） | Instruction following |
| [PACED, 2603.11178] | Qwen3-14B | Qwen3-8B | Beta-kernel weighted KL（Beta 核加权 KL） | AIME, MATH |
| [AdaSwitch, 2510.07842] | Qwen2.5-3B, Llama-3.1-3B, Gemma-7B | Qwen2.5-0.5B, Llama-3.1-1B, Gemma-2B | Adaptive on/off-policy KL（自适应同策略/离策略 KL） | Summarization（摘要生成）, GSM8K, GSM-Plus |
| [$\mathcal{X}$-KD, 2602.12674] | T5-Large (780M) | T5-Small (60M) / Base (220M) | AVRIL-based KL | Summarization, Translation（机器翻译）, Arithmetic |
| [TAID, 2501.16937] | Phi-3-mini (3.8B), Llama-2-7B-Chat, StableLM-Zephyr-3B | TinyLlama (1.1B), Pythia-410M | F-KL + distribution interpolation（分布插值） | MT-Bench, Open LLM Leaderboard |
| [DASD, 2601.09088] | DeepSeek-R1 | DASD-4B-Thinking (4B) | Distribution-aligned seq. KD（分布对齐序列 KD） | AIME, MATH, LiveCode |
| [DDT, 2602.12222] | N/A (on-policy SFT（监督微调）) | Qwen2.5-7B-Inst | IDFT + Hinted Decoding（提示解码） | Alignment（对齐）, Reasoning |
| **Black-Box（黑盒）** | | | | |
| [GAD, 2511.10643] | GPT-5-Chat (black-box) | Qwen2.5-14B-Inst | Adversarial (minimax)（对抗性极小极大） | LMSYS-Chat, Dolly, Vicuna |
| [Lion, 2305.12870] | ChatGPT (black-box) | LLaMA-7B / 13B | Adversarial curriculum（对抗性课程） | BIG-Bench Hard, AGIEval |
| [ORPO-Distill, 2509.25100] | InternLM2.5-7B-Chat | InternLM2.5-1.8B, TinyLlama-1.1B | ORPO (reference-free)（无参考） | GSM8K, ARC, MedQA, StrategyQA |
| [DAIL, 2602.02405] | Expert solutions（专家解答） (black-box) | Qwen2.5-7B-Inst, Qwen3-8B | Contrastive imitation（对比模仿） | AIME, GPQA |
| **Self-Play（自我对弈） & Self-Distillation（自蒸馏）** | | | | |
| [SPIN, 2401.01335] | Self (iter $t{-}1$) | Zephyr-7B-SFT | Self-play DPO（直接偏好优化） | MT-Bench, AlpacaEval |
| [OPSD, 2601.18734] | Self (privileged info-conditioned)（条件于特权信息） | Qwen3-1.7B/4B/8B-Inst | F-KL / JSD on rollouts（在轨迹上的展开） | AIME, MATH, HMMT |
| [OPSDC, 2603.05433] | Self (concise prompt)（简洁提示） | Qwen3-8B / 14B | Per-token R-KL（逐词元 R-KL） | AIME, MATH-500 |
| [GATES, 2602.20574] | Self (document-conditioned)（文档条件） | Qwen3-4B-Base | Consensus-gated KL（共识门控 KL） | Open-domain QA（开放域问答） |
| [SDPO, 2601.20802] | Self (textual feedback)（文本反馈） | Qwen3-8B, OLMo3-7B | Self-distill + credit assign（信用分配） | Code, math, science |
| [MTP Self-Distill, 2602.06019] | Self (same checkpoint)（同一检查点） | Llama-3.1-8B, Qwen2.5-7B | Multi-token prediction（多词元预测） | GSM8K, MATH, MMLU |
| [OPCD, 2602.12275] | Self (context-augmented)（上下文增强） | Qwen3-1.7B / 4B / 8B | R-KL context distillation（上下文蒸馏） | Knowledge, sys prompts（系统提示） |
| [OEL, 2603.16856] | Self (experiential)（经验性） | Qwen3-1.7B / 4B / 8B | KL + context distillation | Text-based games（基于文本的游戏） |
| [SDFT, 2601.19897] | Self (demo-conditioned)（演示条件） | Qwen2.5-7B-Inst | Self-distill + KL reg（正则化） | Skill learning（技能学习）, Tool Use（工具使用） |
| [Priv. Info. Distill, 2602.04942] | Self (PI-conditioned)（特权信息条件） | Qwen3-4B / 8B, R1-Distill-Llama-8B | Privileged self-distill KL（特权自蒸馏 KL） | Long-horizon RL（长视距强化学习） |
| [HDPO, 2603.23871] | Self (privileged, ground-truth)（特权，真实标签） | Qwen2.5-Math-1.5B-Inst | GRPO（群体相对策略优化） + JSD self-distill | MATH, AMC, AIME |
| [TMS, 2602.03073] | Self (historical checkpoints)（历史检查点） | Qwen2.5-7B-Inst | On-policy curriculum SFT（同策略课程 SFT） | MATH, GSM8K |
| **Reasoning & RL Integration（推理与强化学习集成）** | | | | |
| [RLKD, 2505.16142] | DeepSeek-R1 paths + GSRM (7B) | DeepSeek-R1-Distill-Qwen-7B | KL-regularized RL + GSRM | Math reasoning |
| [RLAD, 2602.22495] | Qwen3-8B | Qwen3-0.6B / 1.7B | Trust-region ratio distill（信任区域比率蒸馏） | MATH, GSM8K, ARC |
| [AlignDistil, 2503.02832] | Synthetic DPO + reverse DPO（合成 DPO + 反向 DPO） | Qwen2-1.5B-Inst, Qwen2.5-1.5B-Inst | DPO + token-level KD | AlpacaEval, MT-Bench, Arena-Hard |
| [LUFFY, 2504.14945] | DeepSeek-R1 traces (black-box)（轨迹） | Qwen2.5-Math-7B / 1.5B | Mixed-policy GRPO（混合策略 GRPO） | GSM8K, MATH, AIME |
| [SuperCorrect, 2410.09008] | o1-mini, gpt-4o-mini (black-box) | Qwen2.5-Math-7B, Llama-3.1-8B | KD + self-correction reward（自纠正奖励） | MATH, GSM8K |
| [KDRL, 2506.02208] | Skywork-OR1-Math-7B | DeepScaleR-1.5B | Joint KD + RL objective（联合 KD + RL 目标） | AIME, MATH |
| [KEPO, 2602.00400] | Qwen3-VL-32B | Qwen3-VL-2B | KD + preference optim.（偏好优化） | OmniMedVQA |
| [SCoRe, 2509.14257] | Qwen2.5-72B-Inst | Qwen2.5-7B/3B-Inst, Llama-3.1-8B | Earliest-error correction（最早错误纠正） | AIME, MATH, Multi-hop QA（多跳问答） |
| **Multimodal（多模态） & Domain-Specific（特定领域）** | | | | |
| [VOLD, 2510.23497] | Qwen3-8B (text-only)（仅文本） | Qwen2.5-VL-3B-Inst | GRPO + token-level KL | MMMU-Pro, MathVision |
| [Video-OPD, 2602.02994] | Qwen3-VL-32B-GRPO | Qwen3-VL-8B-Inst | On-policy temporal distill（同策略时间蒸馏） | TVG (Charades, ActivityNet) |
| **Systems（系统） & Scaling（扩展）** | | | | |
| [Speculative KD, 2410.11325] | Gemma-7B-IT, Qwen2-7B-IT | Gemma-2B, Qwen2-0.5B | Block-verified on-policy KL（块验证同策略 KL） | Translation, Dialogue（对话） |
| [DistillSpec, 2310.08461] | T5-XL (3B), GPT-like (234M) | T5-Small (77M), GPT-like (33M) | On-policy draft $\to$ target（同策略草稿到目标） | XSum, CNN/DM |
| [Cross-Tok. KD, 2402.12030] | Llama-2-7B-Chat, Mistral-7B-Inst | OPT-350M, Pythia-160M--1B, Bloomz-560M | Latent OT alignment（潜在 OT（最优传输）对齐） | QA, Summarization |
| [Gemma 2, 2408.00118] | Gemma 2 27B $\to$ 9B $\to$ 2B | Gemma 2 2B / 9B / 27B | Online KD in pre-training（预训练中的在线 KD） | MMLU, HellaSwag, GSM8K |
| [Qwen3, 2505.09388] | Qwen3-32B / 235B-A22B | Qwen3-0.6B--14B, 30B-A3B | On-policy distillation | AIME, MATH, LiveCode |
| [MiMo-V2, 2601.02780] | Domain-specialized teachers（领域专用教师） (RL/SFT) | MiMo-V2-Flash (309B/15B MoE（混合专家）) | Multi-teacher logit + reward（多教师逻辑值 + 奖励） | AIME, MATH, GPQA |

> ⚠️ 审查问题：`DDT` 方法中的 `IDFT` 可能是特定算法的缩写（如 Iterative Direct Feedback Tuning 等），此处未加中文注释，如需展开请根据原论文具体指代进行确认。

---

> ⚠️ **审查问题**：提供的 LaTeX 代码片段仅包含表格的最后一行以及表格的结束标签（`\bottomrule \end{tabular} ...`），缺失了表头（Header）和其他数据行。为了符合 Markdown 表格的语法规范，此处根据内容推测并补充了占位表头。

| 模型/方法 | 教师模型/数据源 | 基础模型/架构 | 训练方法 | 评估领域/基准 |
| :--- | :--- | :--- | :--- | :--- |
| [Nemotron-Cascade 2, 2603.19220] | 领域 RL（Reinforcement Learning，强化学习）/ SFT（Supervised Fine-Tuning，监督微调）教师模型 | Nemotron 30B MoE（Mixture of Experts，混合专家模型）（3B 激活参数） | Cascade RL + 领域 OPD（Online Preference Distillation，在线偏好蒸馏） | IMO（国际数学奥林匹克竞赛）, IOI（国际信息学奥林匹克竞赛）, ICPC（国际大学生程序设计竞赛） |

---

### 3.1 序列级同策略（On-Policy）方法

尽管词元级（token-level）方法提供了密集的监督信号，但它们本质上受到贪婪优化偏差（greedy optimization bias，即只关注当前步骤最优而忽略全局最优的倾向）的影响：每个词元都是独立匹配的，忽略了完整序列的联合概率（joint probability）。序列级 OPD（On-Policy Distillation，同策略蒸馏）将蒸馏重新构建为轨迹级（trajectory-level）强化学习，将完整的输出视为一个单一的决策，并优化一个全局奖励。

**MiniLLM 与 REINFORCE 推导。**
[MiniLLM, 2306.08543] 作为基础的序列级方法。正如第 \ref{subsec:unified_view} 节所介绍的，MiniLLM 选择反向 KL 散度（Reverse KL，一种衡量概率分布差异的指标，倾向于生成样本集中在目标分布的高概率区域）在序列级别强制实现寻态行为（mode-seeking behavior，即倾向于拟合目标分布中的主要峰值）。核心挑战在于，当 $\ptheta$ 本身由 $\theta$ 参数化时，如何计算关于 $\ptheta$ 期望的梯度。使用对数导数技巧（log-derivative trick，也称 REINFORCE 技巧，一种将期望的梯度转化为梯度期望的数学方法），推导过程如下。从 $\KL(\ptheta \parallel \pteacher) = \mathbb{E}_{y \sim \ptheta} [ \log \ptheta(y|x) - \log \pteacher(y|x) ]$ 开始，并应用乘积法则（product rule）：

$$
\begin{aligned}
    \nabla_\theta \KL(\ptheta \| \pteacher) &= \nabla_\theta \sum_y \ptheta(y|x) \left( \log \ptheta(y|x) - \log \pteacher(y|x) \right) \\
    &= \sum_y \ptheta(y|x) \nabla_\theta \log \ptheta(y|x) \log \frac{\ptheta(y|x)}{\pteacher(y|x)} + \sum_y \ptheta(y|x) \nabla_\theta \log \ptheta(y|x)
\end{aligned}
$$

由于 $\sum_y \ptheta(y|x) = 1$ 且其梯度消失为零，最终的梯度简化为：

$$
\nabla_\theta \mathcal{L}_{MiniLLM} = \mathbb{E}_{y \sim \ptheta} \left[ \Big( \log \ptheta(y|x) - \log \pteacher(y|x) \Big) \nabla_\theta \log \ptheta(y|x) \right]
$$

这表明，最小化序列级反向 KL 散度在数学上等价于奖励为 $r(x,y) = \log \pteacher(y|x) - \log \ptheta(y|x)$ 的策略梯度（policy gradient）强化学习。MiniLLM 将其分解为单词元奖励（per-token rewards）和未来回报（future returns），从而能够使用减小方差的基线（baselines）。然而，在庞大的组合输出空间中，REINFORCE 估计需要大量的训练迭代和复杂的基线减法（baseline subtraction）才能收敛。

**用于提高稳定性的约束优化。**
为了克服 REINFORCE 的高方差问题，[文献, 2509.22921] 将蒸馏重新构建为约束马尔可夫决策过程（Constrained Markov Decision Process, CMDP，一种在优化累积奖励的同时必须满足特定约束条件的强化学习框架）。他们没有将 KL 惩罚视为带有手动调节参数 $\lambda$ 的软拉格朗日项（soft Lagrangian term），而是在满足硬约束（hard constraint）$\KL(\ptheta \parallel \pteacher) \le \epsilon$ 的前提下最大化任务奖励。通过采用约束状态增强强化学习（constrained state-augmented RL），该方法在不需要部署时有教师模型参与的情况下，保持了满足约束的理论保证。

> ⚠️ **审查问题：** 
> 1. 引用 `\citet{2509.22921}` 中的 arXiv 编号前缀 "2509" 可能是笔误（指代2025年9月，通常论文不会有未来的编号，可能为 2309 或 2409）。
> 2. 原文该处未明确提及具体的方法名称，因此引用格式暂处理为 `[文献, 2509.22921]`。

**词元级与序列级：根本的权衡。**
比较这些不同粒度的方法揭示了一个核心冲突。词元级方法优化的是序列级散度（sequence-level divergence）的上界；它们强制的局部对齐带来了低方差和高稳定性，但贪婪优化可能会在完善局部语法的同时丧失全局连贯性（global coherence）。序列级方法直接对轨迹奖励进行建模，从而能够捕捉整体的推理结构，但蒙特卡洛采样（Monte Carlo sampling，一种基于随机采样来估计数值的统计方法）的高方差需要消耗大量的计算资源。第 \ref{subsec:hybrid} 节中的混合方法（hybrid approaches）正是为了在这种权衡中寻找平衡而设计的。

---

## 混合与自适应方法

认识到纯粹的词元级蒸馏（token-level distillation）缺乏长期规划，而纯粹的序列级蒸馏（sequence-level distillation）则面临难以控制的方差问题，当代研究已趋向于结合这两种粒度的混合架构，或致力于解决 OPD（On-Policy Distillation, 在线策略蒸馏）的主要实际瓶颈：生成在线策略轨迹（on-policy trajectories）时的计算-质量权衡。我们将这些方法划分为四个优化维度：计算效率、弥合容量差距、课程设计以及新颖范式。

### 计算效率

OPD 最直接的瓶颈在于每个训练步生成完整学生推演（rollouts）的成本。有两种方法从互补的角度降低了这一成本。

[Fast OPD, 2602.15260] 观察到在标准 OPD 过程中，训练信号集中在每个输出的前缀（prefix）部分；即使是简短的、由教师监督的前缀也足以帮助学生模型产生正确的答案。通过将采样视界（sampling horizon）和损失计算均截断至前缀区域，Fast OPD 在匹配完整 OPD 性能的同时，将训练 FLOPs（浮点运算次数）减少了 $2\times$ 到 $47\times$。在第 \ref{sec:systems} 节中进一步讨论的 [Speculative KD, 2410.11325] 则将学生模型的生成结果作为投机草稿（speculative drafts），由教师模型并行验证，从而在无需教师独立生成的全部成本下产生同策略（on-policy）训练数据。

### 弥合容量差距

当师生模型的容量比（capacity ratio）超过 $10\times$ 时，直接匹配教师的分布会导致模式平均（mode averaging）：学生模型有限的参数会将教师模型独特多样的输出模式模糊地混合在一起。

[TAID, 2501.16937] 通过构建随时间变化的中间分布 $P_t = (1{-}\lambda_t)P_\theta + \lambda_t P_T$ 来解决这一问题，其中插值系数 $\lambda_t$ 随着训练的进行从接近于零（接近学生模型）逐渐增加到一（接近教师模型）。学生模型通过最小化与该中间目标的前向 KL 散度（Forward KL），将巨大的师生差距转化为一系列更小、更易处理的蒸馏步骤。[PromptKD, 2402.12842] 采用了一种对偶方法：它并非调整学生的目标，而是通过前置可学习的提示词元（learnable prompt tokens）来调整教师的输出，促使教师产生更容易被容量有限的学生模型所接受的“学生友好型”分布，而这仅增加了教师模型 0.0007\% 的参数。

### 课程与难度自适应

并非所有的训练实例都包含同等丰富的信息。几种方法设计了课程（curricula），将计算资源集中在最具成效的样本上。

[PACED, 2603.11178] 通过梯度信噪比（gradient signal-to-noise ratio, SNR）分析证明，蒸馏梯度 SNR 在学生能力的两个极端处会消失：即当学生对某个问题的通过率接近 0（太难）或 1（太容易）时。为了利用处于中间求解率并集中了最佳学习信号的“最近发展区”（zone of proximal development），PACED 实现了一种 Beta 核权重方案 $w(p) = p^\alpha(1{-}p)^\beta$，为接近学生能力边界的序列分配最大权重。该框架被证明具有极小化极大鲁棒性（minimax-robust），在有界的乘性模型误设（multiplicative misspecification）情况下，最坏情况下的效率损失仅为 $O(\delta^2)$。两阶段的散度调度方案（首先使用前向 KL 散度实现广泛的模式覆盖，然后使用反向 KL 散度（Reverse KL）进行巩固）取得了最强的结果。

[AdaSwitch, 2510.07842] 引入了词元级的自适应切换（adaptive switching）：学生模型开始自主生成每个序列（即在线策略）；一旦发散程度超过了感知上下文的阈值，就会选择性地整合教师的指导。与以往在在线策略（on-policy）和离线策略（off-policy）词元之间频繁切换的混合方法不同，AdaSwitch 使用了一种有原则的切换标准，在确保高质量监督的同时保持了语义的连贯性。

### 新颖范式

有几种方法完全脱离了标准的散度最小化（divergence-minimization）框架，引入了性质上不同的优化原则，重新构建了蒸馏的含义。

[$\mathcal{X}$-KD, 2602.12674] 借鉴了经验学习理论和逆向强化学习（inverse reinforcement learning），采用近似变分奖励模仿学习（Approximated Variational Reward Imitation Learning, AVRIL）框架来联合建模教师的原始奖励函数并执行策略蒸馏（policy distillation）。这鼓励学生模型在教师学习环境的*重建*（reconstructed）版本中进行学习，而不是仅仅模仿输出，从而实现了比 GKD 和 MiniLLM 基线更好的性能-多样性权衡（performance--diversity tradeoffs）。

虽然 $\mathcal{X}$-KD 重建了教师的环境，但 [REOPOLD, 2603.11137] 通过证明师生对数似然比可以作为一种词元级奖励，更直接地桥接了 OPD 与策略优化（policy optimization）。基于这一见解，它通过基于混合的奖励裁剪（mixture-based reward clipping，防止对极端教师信号的过度信任）、基于熵的动态采样（entropy-based dynamic sampling，在高不确定性词元处选择性地利用教师反馈）以及统一的探索到细化策略（exploration-to-refinement strategy），放宽了严格的模仿约束。REOPOLD 实现了比近期 RL（强化学习）方法高 $6.7$--$12\times$ 的样本效率，使得 7B 的学生模型能够匹敌 32B 的教师模型，并获得约 3.3$\times$ 的推理加速。

作为这些双重方法的补充，[TSD-KD, 2603.13260] 结合了间接和直接蒸馏：学生模型生成在线策略候选，教师模型通过偏好反馈（preference feedback）对其进行重新排序（间接），然后基于师生相对置信度选择性地应用分布匹配（distribution matching）（直接），重点关注高熵推理词元。这种双重方法在 10 个推理基准测试中超越基线高达 54.4\%。

该类别中剩下的两种方法挑战了基于 SFT（Supervised Fine-Tuning, 监督微调）的蒸馏范式本身。[DASD, 2601.09088] 批判性地重新审视了在教师生成的推理轨迹（reasoning traces）上进行 SFT 的主导范式，指出了三个局限性：单一的 best-of-$n$（$n$ 选一）样本无法充分表示教师的序列级分布；教师输出分布与学生容量之间存在错位；以及来自教师强制（teacher-forced）训练的暴露偏差（exposure bias）。其增强的分布对齐流水线（distribution-aligned pipeline）仅使用 448K 个训练样本，便在同等规模下实现了最先进的性能。

[DDT, 2602.12222] 提供了一个理论框架，解释了为什么 RL 的泛化能力优于 SFT：关键因素在于 RL 的在线策略（on-policy）数据生成，这使得训练能够与模型不断演变的分布保持一致。DDT 提出了分布内微调（In-Distribution Finetuning，通过重新加权损失以降低分布外样本的权重）和提示解码（Hinted Decoding，将训练语料库与模型当前分布重新对齐），在保持 SFT 效率的同时实现了超越 DPO 和 SimPO 的泛化能力。

---

### 理论分析与方法比较

白盒 OPD（White-box OPD，注：OPD 通常指输出概率蒸馏或在线策略蒸馏）的理论基础主要围绕高维概率空间中散度函数（Divergence functions）的几何性质展开。我们综合了关键的分析结果及其在实践中的意义。

**Forward KL 与 Reverse KL：超越标准二分法。**
传统观点认为，Forward KL 是避零（Zero-avoiding）或模式覆盖（Mode-covering）的，这意味着学生模型会分散概率质量（Probability mass）以覆盖教师模型的所有模式（Modes），从而在模式间的区域产生概率风险；而 Reverse KL 是趋零（Zero-forcing）或模式寻求（Mode-seeking）的，它以牺牲多样性为代价，集中于单一模式。然而，[文献, 2404.02657] 对大语言模型（LLMs）中离散分布的这种二分法提出了挑战，证明了模式寻求和均值寻求（Mean-seeking）的特征并不严格成立，并且在给定足够的训练轮数（Epochs）的情况下，这两种散度都会收敛到相同的目标。在实际的训练轮数预算下，通过*头尾焦点（Head-tail focus）*的视角可以更好地理解它们之间的差异：Forward KL 将学习集中在教师分布的头部（Head），而 Reverse KL 则强调尾部（Tail）。[文献, 2402.11890] 提供了补充证据，表明在 Forward KL 和 Reverse KL 之间的选择是依赖于具体任务的，而不是可以普遍规定的，自适应组合（Adaptive combinations）始终优于任何单一的固定选择。

**统一的 $f$-divergence 视角。**
[文献, 2307.15190] 表明，任何 $f$-散度（$f$-divergence）都可以表示为 $D_f(\pteacher \parallel \ptheta) = \mathbb{E}_{y \sim \ptheta}[f(\pteacher(y)/\ptheta(y))]$，其中 $f$ 是凸函数（Convex function），且满足 $f(1)=0$。通过连续调节凸性参数（Convexity parameter），研究人员可以在模式寻求和模式覆盖行为之间平滑过渡，从而根据下游任务的需求定制蒸馏（Distillation）过程。

**为什么自适应散度（Adaptive divergences）会胜出。**
ToDi、AKL 和 Entropy-Aware OPD 等方法的成功具有几何学上的解释。在推理关键的词元（Reasoning-critical tokens）处，教师模型的分布通常是单峰的（Unimodal，即只有一个正确的逻辑步骤），此时 Reverse KL 能够很好地对齐。在生成灵活的词元（Generation-flexible tokens，例如在“therefore”和“thus”之间做选择）处，分布在同义词（Synonyms）上接近均匀分布（Near-uniform），此时 Forward KL 能够保留这种多样性。自适应方法隐式地检测这种分布模式结构（Modality structure）并相应地进行切换。其实际意义在于，没有任何一种单一的散度在所有词元位置上都是最优的。该领域已经果断地从探讨“使用哪种散度？”转向了“在*哪里*使用哪种散度？”。

---

> ⚠️ **审查问题：**
> 1. **自定义 LaTeX 宏**：公式中的 `\pteacher` 和 `\ptheta` 是原作者自定义的 LaTeX 宏命令。已按照规则原样保留在公式块中，但在实际渲染 Markdown 时，如果未在前端定义这些宏，公式可能会报错或显示异常（通常代表 $p_{\text{teacher}}$ 和 $p_{\theta}$）。
> 2. **引用格式**：原文中的 `\citet{...}` 并没有在上下文中显式提及具体的“方法名”，因此严格按照 `[方法名, cite_key]` 规则强行填入方法名可能会产生误导，此处采用 `[文献, cite_key]` 进行替代以保证严谨性。

---

# Black-Box 与 Self-Distillation 方法
<a id="sec:black_box"></a>

尽管第 \ref{sec:white_box} 节中的 white-box 方法通过完整的 logit（未归一化概率）访问权限实现了 dense distributional matching（密集分布匹配），但当教师模型是不公开权重或 vocabulary-wide logits（词表级逻辑值）的 proprietary model（专有模型，例如 GPT-4、Claude 3）时，这些方法便无法适用。此外，随着模型逼近 human-curated data（人工筛选数据）的边界，它们必须在没有任何外部教师模型的情况下，通过 self-distillation 方法来优化自身的 policy（策略）。本节将涵盖这两种机制。

---

### 3.1 黑盒同策略蒸馏 (Black-Box On-Policy Distillation)

在黑盒 OPD（On-Policy Distillation，同策略蒸馏）中，学生模型无法计算 $\KL(\pteacher \parallel \ptheta)$，因为 $\pteacher$ 在结构上是不可访问的。相反，教师模型仅作为学生模型同策略轨迹 (on-policy trajectories) 的打分函数 (scoring function) 或偏好排序器 (preference ranker)。目前主要涌现出两种信号构建策略：对抗性反馈 (adversarial feedback) 和基于偏好的反馈 (preference-based feedback)。

**对抗性信号构建 (Adversarial signal construction)。**
[GAD, 2511.10643] 将黑盒蒸馏转化为一个两人极小极大博弈 (minimax game)。学生生成器 (generator) $G$ 产生同策略回复，而判别器 (discriminator) $D$（由带有标量预测头 (scalar prediction head) 的学生模型初始化）使用 Bradley-Terry 偏好模型 (Bradley-Terry preference model) 来区分学生输出和教师输出：
$$
    \max_{G} \min_{D}\; V(G, D) = \mathbb{E}_{(x, y^{\mathcal{T}}) \sim \mathcal{T}} \left[ -\log \sigma\!\left( D(y^{\mathcal{T}}) - D(G(x)) \right) \right]
$$
生成器通过 REINFORCE 算法最大化 $V$，将判别器得分用作不断演变的同策略奖励信号 (evolving on-policy reward signal)。与匹配完整分布 (full distributions) 的白盒方法 (white-box methods) 不同，GAD 通过标量质量信号提取知识，以分布保真度 (distributional fidelity) 换取 API 兼容性 (API compatibility)。尽管它继承了对抗性目标函数的训练不稳定性 (training instability)——因为判别器可能会过度拟合风格线索 (stylistic cues) 而非语义质量 (semantic quality)——但它仍比 SFT（Supervised Fine-Tuning，监督微调）基线取得了稳定的一致提升。

[Lion, 2305.12870] 实现了一个互补的三阶段对抗循环 (three-stage adversarial loop)：*模仿 (imitation)*（学生模型在教师回复上进行微调）、*判别 (discrimination)*（教师模型识别出学生模型表现不佳的指令）和*生成 (generation)*（教师模型针对识别出的弱点创建更难的指令）。这种闭环 (closed loop) 通过将计算资源集中在学生模型最薄弱的能力上，逐步缩小了学生与教师之间的差距，形成了一个自然的难度递增课程 (difficulty-increasing curriculum)。与使用学习得到的判别器的 GAD 不同，Lion 利用教师模型本身同时作为裁判 (referee) 和课程设计者 (curriculum designer)，以增加教师 API 调用次数为代价免去了判别器的训练。Lion-13B 仅使用 7 万个训练样本，就在 BIG-Bench Hard 和 AGIEval 上取得了极具竞争力的性能。

**基于偏好的信号构建 (Preference-based signal construction)。**
超越对抗性目标，第二类黑盒方法通过偏好对 (preference pairs) 而不是判别器得分来构建监督信号。[ORPO-Distill, 2509.25100] 将跨架构蒸馏 (cross-architecture distillation) 转化为一个偏好优化 (preference optimization) 任务。它不再依赖单一的最佳教师输出，而是通过多样化的推理轨迹 (reasoning traces) 传递知识，并通过赔率比偏好优化 (Odds-Ratio Preference Optimization) 目标函数来对比教师生成的（偏好的）轨迹和学生生成的（不偏好的）轨迹。这种结合了同策略学生轨迹与离策略 (off-policy) 教师轨迹的混合策略 (mixed-policy strategy)，优于纯离策略和纯同策略的替代方案。与需要外部打分的基于 DPO 的方法不同，ORPO-Distill 直接利用教师与学生轨迹的质量差异来构建偏好对。

当存在高质量的专家解决方案，但这些方案对学生模型而言属于分布外 (out-of-distribution) 时（例如，带有隐式推理空白 (implicit reasoning gaps) 的教学式教科书证明），[DAIL, 2602.02405] 通过一个两步过程弥合了这一差距：首先将专家解决方案转化为详细的、分布内 (in-distribution) 的推理轨迹，然后应用对比目标 (contrastive objective) 使学习过程聚焦于专家的方法论。仅使用不到 1,000 个专家解决方案，DAIL 就实现了 $10$--$25\%$ 的 pass@k 增益和 $2$--$4\times$ 的推理效率 (reasoning efficiency) 提升，这表明在模仿专家级解决方案时，分布对齐 (distribution alignment) 至关重要。

---

## 2.1 自我博弈与自蒸馏（Self-Play and Self-Distillation）

当外部教师模型不可用或计算成本过高时，模型必须生成自己的蒸馏目标。自蒸馏（self-distillation）代表了同策略学习（on-policy learning）的自然终点，在这种情况下，模型不断地自我引导（bootstraps）以提升自身能力。我们将不断增长的相关文献围绕四个概念主题进行组织。

### 自我博弈及其饱和天花板（Self-Play and Its Saturation Ceiling）

[SPIN, 2401.01335] 将自蒸馏形式化为一个双人博弈游戏（two-player game）：在第 $t$ 次迭代中，更新后的模型 $p_{\theta_{t+1}}$ 被训练用于区分上一次迭代生成的回复与人类编写的回复：
$$
    \mathcal{L}_{\text{SPIN}} = \mathbb{E}_{x, y \sim p_{\text{data}}, y' \sim p_{\theta_t}} \left[ \ell\!\left( \lambda\left(\log \frac{p_{\theta_{t+1}}(y|x)}{p_{\theta_t}(y|x)} - \log \frac{p_{\theta_{t+1}}(y'|x)}{p_{\theta_t}(y'|x)}\right) \right) \right]
$$
SPIN 提供了一个理论上的收敛保证：当 $\ptheta = p_{\text{data}}$ 时达到全局最优。从 Zephyr-7B-SFT 开始，它在 3 次迭代中将 MT-Bench 的得分从 5.94 提升至 6.78，但每轮的收益呈现递减趋势（diminishing returns）。关键在于，由于 SPIN 不使用任何外部教师或验证器（verifier），它无法突破监督微调（SFT）数据的质量天花板。自我博弈的快速饱和现象将在第 \ref{subsec:saturation_analysis} 节中进行分析。

### 特权信息：打破自我博弈天花板（Privileged Information: Breaking the Self-Play Ceiling）

使自蒸馏能够突破数据天花板的核心洞见是特权信息（PI, Privileged Information，即在训练期间可用但在测试时不可用的任何信号）。基于 PI 的方法不再让模型在零和博弈（zero-sum game）中与自己对抗，而是让单一模型扮演双重角色：作为教师（以 PI 为条件）和作为学生（在没有 PI 的情况下运行）。这种不对称性为循环注入了新鲜信息，打破了限制纯自我博弈的饱和天花板。

[OPSD, 2601.18734] 将这一原则应用于数学推理。教师策略（teacher policy）同时以问题 $x$ 和真实答案（ground-truth answer）$y^\star$ 为条件，而学生策略仅以 $x$ 为条件。学生生成同策略的展开轨迹（on-policy rollouts），教师则对这些学生生成的序列提供密集的 token 级别监督：
$$
    \mathcal{L}_{\text{OPSD}}(\theta) = \mathbb{E}_{(x, y^\star) \sim \mathcal{S}} \mathbb{E}_{\hat{y} \sim \ptheta(\cdot|x)} \left[ \sum_{n=1}^{|\hat{y}|} D\!\left( \pteacher(\cdot|x, y^\star, \hat{y}_{<n}) \;\|\; \ptheta(\cdot|x, \hat{y}_{<n}) \right) \right]
$$
在竞赛级数学基准测试（AIME 2024/2025, HMMT）上，OPSD 在 4B 和 8B 规模上匹配或超过了 GRPO 的表现，同时使用的生成 token 数量少了一个数量级；不过在 1.7B 规模上，OPSD 的表现不如 GRPO，这表明充足的模型容量（model capacity）是必要的。

[GATES, 2602.20574] 将特权自蒸馏扩展到了没有真实标签或外部验证器的场景。单一模型同时充当导师（tutor，以源文档为条件）和学生（仅根据问题作答）。其核心创新是一种基于共识的门控机制（consensus-based gating mechanism）：对于每个问题，采样 $k$ 个导师回复，只有当导师表现出高度一致性时才进行蒸馏，而在导师不确定性高时抑制梯度。这直接解决了“信息茧房/回音室”（echo chamber）问题，即蒸馏不确定的教师信号会放大噪声。

[统一框架, 2602.04942] 将 OPSD 和 GATES 范式推广为一个基于特权信息的统一框架，并形式化了特权自蒸馏在何种条件下能够被证明优于标准训练。PI 必须充分降低教师的熵（entropy）以提供有意义的监督，但又不能降低太多以至于教师的分布发生退化（degenerate）。经验表明，该框架在困难的、长视野强化学习（long-horizon RL）场景中特别有效，在这些场景中，基础模型如果没有 PI，其求解率几乎为零。

[OPCD, 2602.12275] 将特权信息范式应用于实际部署问题：学生从自己的策略中生成展开轨迹，而以常下文为条件的教师（通过系统提示词、示例或检索上下文进行增强）通过反向 KL 散度（Reverse KL）提供监督，使模型能够内化那些在推理时本需要冗长提示词的知识。其后续方法 [OEL, 2603.16856] 将此扩展到部署后的持续学习（continuous post-deployment learning），模型从交互式环境（例如基于文本的游戏）中积累经验，并通过同策略上下文蒸馏定期将这些经验蒸馏回其权重中，从而形成一个在线学习循环。

### 推理压缩（Reasoning Compression）

经过蒸馏的推理模型通常会产生不必要的冗长思维链（chains of thought），这增加了推理成本而没有提高准确率。[OPSDC, 2603.05433] 应用了同策略自蒸馏，其中同一个模型既充当教师（被提示要求“保持简洁”），又充当学生（生成不受约束的展开轨迹），并在学生自身的轨迹上最小化逐 token 的反向 KL 散度。在 MATH-500 数据集上，OPSDC 将思维链的 token 数量减少了 57--59%，同时将准确率提高了 9--16 个百分点，这证明了蒸馏推理模型中的冗长性是一种可通过训练消除的低效现象。

基于自蒸馏的 [MTP, 2602.06019] 使用在线自蒸馏目标将预训练的自回归模型（autoregressive model）转换为快速的多 token 预测模型，在不改变架构的情况下，在 GSM8K 上实现了超过 3 倍的解码加速，且准确率下降不到 5%。

### 通过自蒸馏实现无奖励对齐（Reward-Free Alignment via Self-Distillation）

近期研究中一个反复出现的主题是，自蒸馏能够复制强化学习（RL）的优势（如探索 exploration、信用分配 credit assignment、抗遗忘 forgetting resistance），而无需显式的奖励模型或验证器。核心洞见在于，来自环境或模型自身历史行为的结构化反馈可以替代标量奖励（scalar rewards）。

[SDPO, 2601.20802] 就是一个典型的例子，它用丰富的文本反馈（编译器错误、测试输出、证明检查器消息）取代了标量奖励。模型生成同策略的展开轨迹，接收结构化反馈，并构建细粒度的信用分配，将成功或失败归因于特定的推理步骤，而不是整个轨迹。这解决了标准 RLVR（带有验证器奖励的强化学习）中基本的信用分配瓶颈，在科学推理、工具使用和竞争性编程等任务中同时提高了样本效率和最终准确率。

SDPO 致力于解决信用分配问题，而 [TMS, 2602.03073] 则解决了强化学习的另一个优势：记忆保持（retention）。标准的 SFT 面临监督不匹配（supervision mismatch）问题：模型不断演进的策略会偏离静态的训练标签，从而导致灾难性遗忘（catastrophic forgetting）。TMS 从模型自身的历史检查点（checkpoints）创建一个动态课程（dynamic curriculum），构建近策略（near-policy）的监督目标以最小化策略-标签散度（Policy--Label Divergence），从而在无需奖励模型的情况下弥补了与强化学习之间的差距。

当标准强化学习本身失效时，会出现一个互补的挑战。[HDPO, 2603.23871] 针对的是“悬崖（cliff）”提示词，即所有的展开轨迹均失败且策略梯度完全消失的情况。HDPO 通过针对这些零梯度（zero-gradient）提示词的特权自蒸馏来增强标准 GRPO：作为教师的模型接收真实信息并生成特权展开轨迹，这些轨迹通过 JSD（Jensen-Shannon Divergence，被证明实现了从 KL 正则化的 RL 最优策略中进行拒绝采样）蒸馏给学生。在 Qwen2.5-Math-1.5B-Inst 上的实验表明，该方法在覆盖率指标上取得了持续的提升。

最后，[SDFT, 2601.19897] 将这些线索统一起来，将同策略自蒸馏定位为持续学习（continual learning）的通用机制：模型从专家演示中学习，同时通过隐式 KL 正则化（implicit KL regularization）对其自身的先前分布进行正则化约束，从而在无需奖励函数的情况下，实现了可与基于 RL 的持续学习相媲美的抗遗忘能力。

---
> ⚠️ **审查问题**：
> 1. 公式中包含 `\ptheta` 和 `\pteacher` 等非标准 LaTeX 宏，在标准的 Markdown 渲染器中可能会无法解析（通常应写为 `p_{\theta}` 和 `p_{\text{teacher}}`）。为遵循“公式保留 LaTeX”的规则，译文中已保持原样，建议在渲染前确保您的环境已定义这些宏，或进行全局替换。
> 2. 原文第8段 `\citet{2602.04942}` 未提及具体方法名，为遵循 `[方法名, cite_key]` 的引用格式规则，译文中根据其内容提炼为 `[统一框架, 2602.04942]`。

---

### 为什么自我对弈会饱和及其突破策略

自蒸馏（self-distillation）的一个关键理论瓶颈是策略饱和（policy saturation）的迅速出现。在经历了几次 SPIN 或 OPSD 迭代后，经验观察普遍发现模型性能会出现平台期或严重退化。这种现象与“衔尾蛇”问题（Ouroboros problem，即模型反噬自身）密切相关，并且代表了一种与暴露偏差（exposure bias）截然不同的失败模式：暴露偏差源于离轨（off-policy）设置下的训练-测试分布不匹配，而饱和则源于完全同轨（on-policy）的自我对弈（self-play）中*缺乏*分布多样性。

在数学上，这与 GANs 中的模式崩溃（mode collapse）有关。因为学生模型（student）是针对一个与其共享自身归纳偏置（inductive biases）和架构限制的目标进行优化的，所以假设空间（hypothesis space）会逐渐坍缩。如果模型发现了一个句法上的“捷径”（syntactic "hack"）或一种高度自信但有缺陷的推理启发式（flawed reasoning heuristic），没有外部信号会对其进行惩罚。模型会自我强化这条有缺陷的轨迹，驱使 $\ptheta(y_{flawed}|x) \to 1$；一旦对其自身的幻觉（hallucinations）完全确定，就会发生梯度消失（gradients vanish），探索停止，策略就会陷入困境。

> ⚠️ 审查问题：原文公式中的 `\ptheta` 属于自定义 LaTeX 宏（通常代表 $p_\theta$），在标准 Markdown 渲染器中可能无法正常显示，建议后续替换为 `p_\theta`。

**突破饱和的策略。** 目前已经出现了两种主要的方法。首先，*外部验证器和符号落地（symbolic grounding）*：正如在 OPSD 中所展示的，自我对弈必须锚定在不可导的真实度量（non-differentiable truth metrics）（如代码执行引擎、符号数学验证器）上。即使模型对有缺陷的推导变得高度自信，验证器也会分配 $R=0$，从而粉碎自我强化的回音室（echo chamber）。其次，*蒸馏-RL 循环（distillation--RL loop）*：为了保持轨迹的多样性，最先进的框架将自蒸馏与基于 PPO 的 RL 交替进行：

$$
    \max_\theta \mathbb{E}_{y \sim \ptheta} \left[ R(y) - \beta \KL(\ptheta \parallel p_{\mathrm{ref}}) \right]
$$

> ⚠️ 审查问题：与上一段类似，公式中的 `\ptheta` 和 `\KL` 是自定义宏，标准 Markdown 可能无法渲染，建议检查并替换为 `p_\theta` 和 `\text{KL}`。

其中 $R(y)$ 由独立训练的奖励模型（reward model）提供。使用针对学生模型最新生成内容的人工标注的偏好数据（human-annotated preference data）定期刷新奖励模型，可以防止过早收敛（premature convergence），确保自我对弈的动态过程始终是一个不断移动的目标。

---

# 推理蒸馏

复杂推理仍然是大型语言模型（LLM）研究中最活跃的前沿领域。在此，OPD（同策略蒸馏，On-Policy Distillation）不仅作为一种压缩技术，更是结构化知识转移（structured knowledge transfer）的基础机制。通过将训练分布从教师模型的静态数据集转移到学生模型的活跃探索空间（active exploration space），OPD 已成为将 CoT（思维链，Chain-of-Thought）和多步推理注入较小模型的事实标准。第 \ref{sec:white_box} 节中分析的词元级（token-level）和序列级（sequence-level）目标提供了数学基础；本节将探讨这些目标如何与推理转移（reasoning transfer）的独特挑战相互作用——在推理转移过程中，错误会在长推导链（derivation chains）中不断累积。遵循标准的推理蒸馏符号约定，我们在本节中统一使用 $P_\theta$ 和 $P_T$ 来表示轨迹级采样（trajectory-level sampling）和词元级条件概率（token-level conditionals），因为推理方法通常在完整的展开序列（full rollout）上运行。

> ⚠️ **审查问题**：
> 1. 原文中方法缩写“OPD”在本段未给出全称，基于大模型推理蒸馏领域的上下文，此处将其推断并注释为 On-Policy Distillation（同策略蒸馏）。请核对是否与论文前文的定义一致。
> 2. LaTeX 交叉引用 `\ref{sec:white_box}` 在纯 Markdown 环境下无法自动渲染编号，建议在最终排版时手动替换为实际的章节号（如“第 X 节”）。

---

## \subsection{Chain-of-Thought Distillation (思维链蒸馏)}

传统的 off-policy distillation (异策略蒸馏) 迫使 student (学生模型) 在固定的数据集上模仿 teacher (教师模型) 的 reasoning traces (推理轨迹)，然而推理过程是高度 path-dependent (路径依赖) 的。正如 [Distilling Step-by-Step, 2305.02301] 所证实的那样，从大型语言模型 (LLM) 提取的 rationales (推理依据) 中学习，能够使小模型的表现超越未经过微调的大型对应模型。

最近的 CoT distillation (思维链蒸馏) 工作强调了将推理路径与学生模型自身的 linguistic manifold (语言流形) 对齐的必要性。当学生模型生成自己的 intermediate steps (中间步骤) 时，教师模型就从输出的 static dictator (静态指令者) 转变为学生 intrinsic logic (内在逻辑) 的 active evaluator (主动评估者)。形式上，设 $x$ 为 input prompt (输入提示)，$y$ 为最终答案，$r = (r_1, r_2, \dots, r_T)$ 为中间推理 token 的序列。学生模型 $P_\theta$ 生成 rollouts (生成轨迹) $r^S \sim P_\theta(\cdot | x)$。在 on-policy CoT distillation (同策略思维链蒸馏) 中的目标函数会在每个生成步骤最小化 Reverse KL divergence (逆 KL 散度)：

$$
\begin{aligned}
\mathcal{L}_{\text{CoT-OPD}}(\theta) &= \mathbb{E}_{x \sim \mathcal{D}, r^S \sim P_\theta(\cdot|x)} \left[ \sum_{t=1}^{|r^S|} \KL \Big( P_\theta(\cdot | x, r^S_{<t}) \parallel P_T(\cdot | x, r^S_{<t}) \Big) \right] \label{eq:cot_opd}
\end{aligned}
$$

与 off-policy Forward-KL (异策略前向 KL 散度) 不同——后者是 mean-seeking (均值搜寻) 的，并且迫使学生模型覆盖教师模型推理的所有 modes (模式)（这通常会导致 probability mass (概率质量) 落在 implausible regions (不合理区域)）——公式 \ref{eq:cot_opd} 中的 Reverse-KL 是 mode-seeking (模式搜寻) 的。它确保了学生模型能够强化在其自身 parameterization (参数化) 下具有高概率的推理路径，前提是这些路径得到了教师模型的验证。

这种公式化表达被诸如 SuperCorrect [SuperCorrect, 2410.09008] 等框架进一步增强，该框架引入了一种用于 reasoning distillation (推理蒸馏) 的 two-stage framework (两阶段框架)。在第一阶段，从教师模型中提取 hierarchical thought templates (分层思维模板)（包括 high-level strategies (高层策略) 和详细的 step-level reasoning patterns (步骤级推理模式)），以指导学生模型生成更 fine-grained reasoning (细粒度推理)。在第二阶段，cross-model collaborative DPO (跨模型协同直接偏好优化) 增强了学生模型的 self-correction abilities (自我纠错能力)。具体而言，教师模型在训练期间为学生模型的 erroneous reasoning steps (错误推理步骤) 提供 correction traces (纠错轨迹)，而 cross-model DPO objective (跨模型 DPO 目标) 则教导学生模型利用 teacher-guided insights (教师指导的见解) 来定位并解决错误。

$$
\begin{aligned}
\mathcal{L}_{\text{SuperCorrect}}(\theta) &= \mathcal{L}_{\text{template}}(\theta) + \lambda \cdot \mathcal{L}_{\text{cross-DPO}}(\theta)
\end{aligned}
$$

其中 $\mathcal{L}_{\text{template}}$ 将教师模型的 thought templates (思维模板) 蒸馏到学生模型的推理过程中，而 $\mathcal{L}_{\text{cross-DPO}}$ 则使用教师模型的 correction traces (纠错轨迹) 来优化学生模型在正确与错误推理路径之间的 preference (偏好)。SuperCorrect-7B 模型在 MATH/GSM8K 数据集上分别以 7.8%/5.3% 和 15.1%/6.3% 的优势超越了 DeepSeekMath-7B 和 Qwen2.5-Math-7B。

---
> ⚠️ **审查问题：**
> 1. 公式 `\ref{eq:cot_opd}` 中的 `\KL` 是一个自定义的 LaTeX 宏。在标准的 Markdown 数学渲染引擎（如 MathJax 或 KaTeX）中，如果没有在前端提前定义该宏，可能会报 `Undefined control sequence \KL` 错误。如果在网页端展示，建议将其替换为 `\text{KL}` 或补充宏定义。
> 2. 原文 LaTeX 块使用的是 `\begin{align} ... \end{align}`，为了保证在 Markdown 中的兼容性和正确渲染，译文中已将其转换为包含在 `$$ ... $$` 内的 `\begin{aligned} ... \end{aligned}` 格式。

---

### 奖励引导的同策略蒸馏

将强化学习（Reinforcement Learning, RL）整合到蒸馏流程中，弥合了模仿学习（Imitation Learning）与结果驱动优化（Outcome-driven Optimization）之间的差距。这里汇聚了两条技术路线：基于结果的奖励（稀疏但灵活）和基于逻辑值（Logit-based，指模型输出的原始预测分数）的信号（密集但需要白盒访问权限）。优化目标从纯粹的分布匹配（Distribution Matching）转变为在蒸馏约束条件下的期望奖励最大化。

诸如 RLKD [RLKD, 2505.16142] 和 AlignDistil [AlignDistil, 2503.02832] 等框架通过奖励引导的学习统一了对齐（Alignment）和蒸馏。RLKD 提出了一种生成式结构奖励模型（Generative Structure Reward Model, GSRM），将推理路径转化为元推理求解步骤，并计算衡量学生和教师推理之间结构对齐程度的奖励。基于 RL 的框架不再仅仅通过监督微调（Supervised Fine-Tuning, SFT）模仿教师扁平的词元序列（Token Sequence），而是让学生内化教师隐含的多分支推理结构，即使在纯 RL 机制下仅使用 0.1% 的数据，也能超越标准的 SFT-RL 流程。

$$
\begin{aligned}
\max_{\theta} \mathcal{J}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim P_\theta(\cdot|x)} \left[ R_T(x, y) - \beta \text{KL}\big(P_\theta(\cdot|x) \parallel P_T(\cdot|x)\big) \right]
\end{aligned}
$$

在奖励加权蒸馏（Reward-weighted Distillation）框架中，稀疏的结果奖励被用于对密集的词元级（Token-level）蒸馏损失进行加权。在实践中，上述公式中的 KL 项被计算为每个词元 KL 散度（KL Divergences）的总和 $\sum_t \text{KL}(P_\theta(\cdot|y_{<t}) \parallel P_T(\cdot|y_{<t}))$，从而实现解析梯度计算（Analytic Gradient Computation）。目标函数关于学生参数 $\theta$ 的梯度依赖于由密集蒸馏基线修改的 REINFORCE 估计器（REINFORCE Estimator）：

$$
\begin{aligned}
\nabla_\theta \mathcal{J}(\theta) \approx \mathbb{E}_{y \sim P_\theta} \left[ \sum_{t=1}^{|y|} \nabla_\theta \log P_\theta(y_t | x, y_{<t}) \cdot \hat{A}_t(x, y) \right] - \beta \nabla_\theta \text{KL}(P_\theta \parallel P_T)
\end{aligned}
$$

其中 $\hat{A}_t$ 是通过教师价值函数（Value Function）估计的优势函数（Advantage）。这种数学上的协同作用使学生能够推断并超越教师的能力，这种效应被记录为奖励外推（Reward Extrapolation）[Reward Extrapolation, 2602.12125]。外推的发生是因为学生在状态空间（State Space）的未知区域 $\mathcal{S}_{\text{novel}}$ 中探索了新颖且结构合理的推理路径，在这些区域中，教师的生成概率 $P_T(y|x)$ 可能很低，但教师的结果验证奖励 $R_T(x, y)$ 仍然保持高度正向。通过针对这种联合信号进行优化，学生摆脱了严格行为克隆（Behavioral Cloning）的性能天花板，发现了教师默认解码策略永远无法达到的算法捷径，并缓解了纯自对弈（Self-play）RL 中典型的饱和问题。

一个互补的方法是 LUFFY [LUFFY, 2504.14945]，它直接解决了推理任务中同策略（On-policy）RL 的一个根本局限性，即学生仅从自身的展开（Rollouts，指模型在环境中的采样轨迹）中学习，从而受到其初始能力的限制。LUFFY 将 GRPO 扩展为一个混合策略（Mixed-Policy）目标，将离策略（Off-policy）的推理轨迹（例如来自 DeepSeek-R1）与学生同策略的展开结合起来，进行联合优势计算。为了防止对离策略轨迹中高概率词元的表面模仿而忽略低概率但关键的推理步骤，LUFFY 通过正则化重要性采样（Regularized Importance Sampling）引入了策略塑形（Policy Shaping），对梯度进行重新加权，以强调从不熟悉但有效的动作中学习。在六个数学基准测试中，LUFFY 相比标准的基于规则验证的强化学习（RLVR，Reinforcement Learning with Verifiable Rewards）方法实现了平均 +6.4 分的提升，并且在纯同策略 RL 完全失败的弱基础模型（例如 Llama-3.1-8B）训练中取得了关键性成功。

---
> ⚠️ **审查问题：**
> 1. 原文 LaTeX 公式中使用了 `\KL` 宏，这通常是作者自定义的 LaTeX 命令。在标准 Markdown (MathJax/KaTeX) 环境中直接使用会导致渲染失败。译文中已将其替换为 `\text{KL}` 以确保在 Markdown 中正常显示。
> 2. 原文中的 `Equation~\ref{eq:rlkd}` 依赖 LaTeX 的自动编号系统。在 Markdown 中无此机制，故译文中将其调整为“上述公式”以保持上下文连贯。
> 3. LaTeX 公式块原为 `\begin{align}...\end{align}`，为了符合 Markdown 公式块规范，已转换为 `$$ \begin{aligned}...\end{aligned} $$`。

---

### DeepSeek-R1：离策略推理蒸馏 (Off-Policy Reasoning Distillation)
DeepSeek-R1 [DeepSeek-R1, 2501.12948] 的发布彻底改变了推理蒸馏领域，尽管其蒸馏方法本身是严格的*离策略* (off-policy) 的。DeepSeek-R1 证明了将大规模 RL (GRPO) 直接应用于大型基础模型（671B MoE）能产生高度结构化、可验证的推理轨迹，从而带来一种涌现的“顿悟时刻” (Aha moment)，即模型会自我分配计算资源来验证其逻辑。

蒸馏步骤非常直接。*离线*从 DeepSeek-R1 生成了 800,000 个长思维链 (long-CoT) 推理样本，较小的学生模型（从 Qwen-1.5B 到 Llama-70B）通过标准的监督微调 (SFT) 在这个静态数据集上进行微调。没有同策略 (on-policy) 的学生 rollout，没有 logit 匹配，没有迭代的师生交互；学生在训练期间从不生成自己的响应。这是经典的大规模应用 [Sequence-Level Knowledge Distillation, kim2016sequence]。

#### 为什么离策略蒸馏在这里效果如此之好
这种离策略方法的显著有效性需要解释，因为它似乎与本综述的核心论点（即同策略训练可缓解暴露偏差）相矛盾。我们总结了三个因素。

首先，*数据质量优于数据分布*。来自 DeepSeek-R1 的 800K 样本包含了极高品质的推理链，具有逐步验证、自我纠错和结构化的深思熟虑。当教师数据如此丰富多样时，暴露偏差问题得到了部分缓解，因为静态数据集已经覆盖了广泛的推理模式和错误恢复策略。

其次，*推理轨迹本质上具有自我纠错能力*。与典型的离策略数据（例如，教师生成的摘要）不同，R1 的长 CoT 输出包含回溯、“等等，让我重新考虑一下”的时刻，以及在单个序列中的多路径探索。学生不仅学习到了正确答案，还学到了验证和纠正中间步骤的元认知过程，这部分补偿了同策略探索的缺乏。

第三，*学生的任务是记忆结构，而不是探索替代方案*。对于数学推理而言，与开放式生成相比，有效的解决路径相对较少。离策略数据覆盖了主要的有效路径，学生的主要挑战是忠实地重现这些结构化链条，而不是发现新的链条。

#### 在 R1 蒸馏之上使用同策略方法的理由
然而，离策略的上限是真实存在的。DeepSeek-R1 论文明确指出，引入 RL 可以进一步提升模型性能，但他们选择不包含它。后续工作表明，在离线 R1 风格蒸馏*之后*应用同策略方法，能产生有意义的进一步提升。

如第 \ref{sec:reward_guided_opd} 节所述，[RLKD, 2505.16142] 证明了结构化奖励信号可以显著提高推理蒸馏的样本效率，即使在 0.1% 的数据上也能超越标准的 SFT-RL 流水线。
在此方向的基础上，[KDRL, 2506.02208] 提供了一个统一框架，在后训练期间联合优化 KD 和 RL 目标。KDRL 在 RL 训练期间在学生和教师之间添加了一个同策略 KL 正则项，防止学生偏离教师策略太远，同时仍能受益于奖励驱动的探索。这解决了序列流水线（先蒸馏后 RL，或先 RL 后蒸馏）的一个关键失效模式。RL 阶段可能会“遗忘”蒸馏的知识，而 KD 阶段可能会抑制通过 RL 发现的新颖推理模式。
[RLAD, 2602.22495] 通过选择性模仿策略进一步推进了这种统一：学生仅在遵循教师指导能改善策略更新时才这么做，并在教师信号会降低学生自身轨迹质量时忽略教师。其核心机制是 Trust Region Ratio Distillation (TRRD)，它用 PPO 风格的似然比目标取代了标准的 KL 正则项。TRRD 并不惩罚学生和教师之间的绝对 KL 距离，而是将每个 token 的概率比 $\ptheta(y_t)/\pteacher(y_t)$ 裁剪在信任区域内，确保稳定的更新，从而继承教师的优势而不被其劣势拖累。这种选择性方法在推理基准测试中优于离线蒸馏和纯 RL (GRPO)，并显著超越了那些盲目在每个 token 上最小化散度（无论教师信号是否有益）的标准基于 KL 的 OPD 方法。
[KEPO, 2602.00400] 将蒸馏集成到视觉-语言模型的偏好优化中，利用密集的 token 级教师监督来解决面向推理的 RL 中的稀疏奖励问题。通过将偏好优化条件化于教师知识，KEPO 在学生初始解决率接近零的问题上稳定了训练，而在这种情况下，标准的 RLVR 会因为探索崩溃而失败。
从理论角度来看，[Unified Framework, 2512.23097] 提供了一个统一的数学框架，将同策略 KD 和 RL 均作为结合了轨迹级 KL 散度与任务奖励的复合目标的特例。他们的梯度分解表明，KD 组件为 token 级模仿提供了密集的、解析可计算的梯度，而 RL 组件为奖励最大化贡献了蒙特卡洛策略梯度。这种形式化解释了为什么混合 KD+RL 方法始终优于单独的任何一种方法。密集的 KD 梯度稳定了早期训练，而 RL 梯度使模型能够探索超出教师分布的范围。
> ⚠️ 审查问题：原文献为 `\citet{2512.23097}`，按照要求转换为 `[方法名, cite_key]` 格式，由于缺乏具体方法名，此处提取为 `[Unified Framework, 2512.23097]`。

[OPSD, 2601.18734] 和 [PACED, 2603.11178] 代表了下一步的演进，应用了真正的同策略蒸馏，即学生生成自己的推理 rollout，而教师对这些学生生成的序列提供 token 级监督。这解决了离线 R1 蒸馏无法解决的残余暴露偏差问题；学生在推理过程中的错误与训练数据中的错误不同，只有同策略方法才能纠正这种分布不匹配。

一个正交但在实践中非常重要的方向是*推理压缩*。如第 \ref{subsec:self_distill} 节所述，[OPSDC, 2603.05433] 应用同策略自蒸馏来压缩冗长的思维链，在 MATH-500 上将 token 数量减少了 57--59%，同时提高了准确率。在推理背景下，OPSDC 的结果尤为引人注目：在 AIME 2024 上，14B 变体在压缩 41% 的情况下比未压缩基线提高了 +10 分。这表明蒸馏推理模型中的冗长性是一种可训练的低效，而不是必须付出的代价。

#### 实验结果：离策略 R1 蒸馏
尽管如此，DeepSeek-R1 离策略蒸馏的结果提供了一个极具说服力的性能基线。使用 DeepSeek-R1（671B MoE）作为教师，蒸馏出的学生模型在各个模型规模上都取得了显著的性能。在 AIME 2024 基准测试 (pass@1) 上，R1-Distill-Qwen-1.5B 获得了 28.9% 的分数，已经超越了 GPT-4o (9.3%) 和 Claude-3.5-Sonnet (16.0%)。R1-Distill-Qwen-7B 达到 55.5%，R1-Distill-Qwen-14B 达到 69.7%，R1-Distill-Qwen-32B 达到 72.6%，而 R1-Distill-Llama-70B 达到了 70.0%（或者使用 consensus@64 多数投票达到 86.7%）。在 MATH-500 上，7B 蒸馏模型达到 92.8%，32B 模型达到 94.3%。

#### 蒸馏对比直接 RL
进一步的重要发现是，*对于中小型模型，离策略蒸馏决定性地优于直接 RL*。在 32B 规模下，将 GRPO 直接应用于 Qwen-2.5-32B-Base（产生“Qwen2.5-32B-Zero”）在经过 1 万步 RL 后，在 AIME 2024 上仅达到 47.0%，与 QwQ-32B-Preview (50.0%) 相当。相比之下，R1-Distill-Qwen-32B 达到了 72.6%，差距高达 **25.6 个百分点**。这种巨大的差异突显出，即便是从能力足够强的教师那里进行离策略蒸馏，对于较小的模型来说也远比直接 RL 有效。那么自然的问题变成了：*同策略蒸馏能否进一步缩小这一差距，或者突破离策略的上限？* 这仍然是该领域最重要的开放问题之一。

#### R1 之后的演进：Qwen3 及超越
DeepSeek-R1 范式已被迅速采用和扩展。[Qwen3, 2505.09388] 通过引入多阶段训练改进了流水线，将离策略蒸馏与随后的同策略 RL 相结合，其中专门的奖励模型在学生 rollout 期间提供特定领域的反馈。Qwen3 还引入了“思考预算” (thinking budget) 机制，允许学生根据问题难度动态分配思维链长度，防止学生在简单问题上生成不必要的冗长推理，这是在直接 R1 蒸馏中观察到的失效模式，学生有时会复制教师的冗长思考，即使简短的推导就足够了。这些发展表明，最优的推理蒸馏流水线既不是纯粹的离策略，也不是纯粹的同策略，而是一个精心分阶段的混合体。首先在高质量教师数据上进行离线 SFT 以建立强大的基础，然后进行同策略 RL 或 OPD 以消除剩余的分布差距。

## 工业系统与扩展 (Industrial Systems and Scaling)
\label{sec:systems}

随着 OPD 从学术原型走向工业级部署，围绕计算效率、缩放定律 (scaling laws) 和架构不匹配的工程挑战成为舞台中心。第 \ref{sec:white_box}--\ref{sec:reasoning} 节提供了算法基础；本节探讨这些算法如何适应万亿 token 规模的训练，在这样的规模下，梯度计算、教师查询和延迟隐藏方面的创新变得至关重要。

### 大规模部署
最近的基础模型在后训练中严重依赖 OPD，证明了其可扩展性。Qwen3 技术报告 [Qwen3, 2505.09388] 强调了工业级 OPD，其中动态教师集成实时评估学生的生成。在这种设置下，目标分布聚合了 $K$ 个专家。设 $w_k$ 为第 $k$ 个教师 $T_k$ 的权重，产生凸组合：
$$
\tilde{P}_{\text{ensemble}}(y_t | x, y_{<t}) = \sum_{k=1}^K w_k(x) P_{T_k}(y_t | x, y_{<t}), \quad \text{where } \sum w_k(x) = 1
$$
这平滑了目标分布，并防止学生过拟合单一教师的特性。Gemma 2 [Gemma 2, 2408.00118] 同样使用在线 KD 来弥合其参数层级之间的性能差距，将蒸馏直接嵌入到持续预训练中。MiniPLM [MiniPLM, 2410.17215] 通过离线的*差异采样 (Difference Sampling)* 将 KD 扩展到预训练阶段本身，选择教师和小型参考模型之间对数概率差异最大的实例，对困难和多样化的示例进行上采样，同时过滤掉琐碎或嘈

---

# 工业系统与扩展
\label{sec:systems}

随着 OPD（在线偏好优化）从学术原型走向工业级规模的部署，围绕计算效率、缩放定律（scaling laws）以及架构不匹配（architectural mismatches）的工程挑战成为了核心焦点。第 \ref{sec:white_box} 至 \ref{sec:reasoning} 节提供了算法基础；本节将探讨这些算法如何适应万亿级 token 规模（trillion-token-scale）的训练，在这种规模下，梯度计算、教师模型查询（teacher querying）以及延迟隐藏（latency hiding）等方面的创新变得至关重要。

> ⚠️ 审查问题：原文中的缩写“OPD”在此处暂译为“在线偏好优化”，其具体全称（如 Online Preference Descent 或 Online Preference Direction 等）需根据论文上下文确认，以确保术语翻译的准确性。

---

## 大规模部署

近期的基础模型（foundation models）在后训练（post-training）阶段严重依赖 OPD（在线策略蒸馏，Online Policy Distillation），这证明了其可扩展性。[Qwen3, 2505.09388] 技术报告强调了工业级的 OPD，其中动态集成的教师模型（dynamic ensemble of teachers）会实时评估学生模型的生成内容。在这种设置下，目标分布（target distribution）聚合了 $K$ 个专家模型。设 $w_k$ 为第 $k$ 个教师模型 $T_k$ 的权重，从而得到如下凸组合（convex combination）：
$$
\begin{aligned}
\tilde{P}_{\text{ensemble}}(y_t | x, y_{<t}) = \sum_{k=1}^K w_k(x) P_{T_k}(y_t | x, y_{<t}), \quad \text{where } \sum w_k(x) = 1
\end{aligned}
$$
这平滑了目标分布，并防止学生模型过拟合（overfitting）于单一教师模型的特质（idiosyncrasies）。[Gemma 2, 2408.00118] 同样使用在线 KD（知识蒸馏，Knowledge Distillation）来弥合其不同参数层级（parameter tiers）之间的性能差距，将蒸馏直接嵌入到持续预训练（continuous pre-training）中。[MiniPLM, 2410.17215] 通过离线的 Difference Sampling（差异采样）将 KD 扩展到了预训练阶段本身，挑选出教师模型与小型参考模型（reference model）的对数概率（log-probabilities）差异最大的样本，对困难且多样的样本进行上采样（up-sampling），同时过滤掉微不足道或嘈杂的数据。这种离线筛选（offline curation）完全避免了同策略（on-policy）的教师模型推理，且精炼后的语料库可以在多个学生模型中重复使用。MiniPLM 在 9 个下游任务（downstream tasks）上提升了学生 LMs（语言模型，Language Models，参数量 200M--1.2B）的性能，同时减少了预训练的计算量。

此外，三种反馈路径（feedback routes）——logits（逻辑值）、outcomes（结果反馈）和 self-play（自我对弈）——之间的界限在规模扩大时变得模糊。[MiMo-V2, 2601.02780] 将来自领域特化教师模型（domain-specialized teachers）的蒸馏与基于 RL（强化学习，Reinforcement Learning）的训练相结合，证明了在不同训练阶段受益于不同监督信号（supervisory signals）的大规模系统中，这些范式可以是互补的。

> ⚠️ **审查问题：**
> 1. **疑似虚构/未来文献**：原文中出现的 `\citep{2505.09388}` (对应2025年5月) 和 `\citep{2601.02780}` (对应2026年1月) 的 arXiv 编号在当前时间点属于未来时间，且 `Qwen3` 与 `MiMo-V2` 等模型版本可能属于未发布或 AI 幻觉生成的占位符，建议核实原稿中的引用真实性。
> 2. **术语缩写推断**：原文仅使用了 "OPD" 缩写，此处根据上下文翻译为“在线策略蒸馏（Online Policy Distillation）”（也有可能指 Online Preference Distillation），请根据论文前文的定义进行最终确认。

---

## 效率创新

OPD（On-Policy Distillation，同策略蒸馏）的主要系统性瓶颈在于教师模型对动态生成的学生 token（词元）进行的前向传播（forward pass）。如果学生生成一个长度为 $N$ 的序列，朴素的实现需要进行 $O(N)$ 次自回归（autoregressive）的教师模型前向传播，或者一次 $O(N^2)$ 的注意力前向传播，这会严重削弱训练吞吐量（training throughput）。

[Speculative KD, 2410.11325] 通过将学生模型的生成内容作为投机草稿（speculative drafts）来解决这一瓶颈。在采样阶段（rollout），学生生成一个包含 $K$ 个 token 的块 $(y_{t+1}, \dots, y_{t+K})$；随后教师模型并行地验证并对这些草稿进行打分。预期加速比 $E[S]$ 取决于接受率（acceptance rate）$\alpha$：

$$
\begin{align}
E[S] = \frac{\mathbb{E}[K_{\text{accepted}}] + 1}{1 + c} \quad \text{where } \mathbb{E}[K_{\text{accepted}}] = \mathbb{E}_{y \sim P_S}\!\left[\sum_{k=1}^K \prod_{i=1}^k \min \left(1, \frac{P_T(y_{t+i} | y_{<t+i})}{P_S(y_{t+i} | y_{<t+i})} \right)\right]
\end{align}
$$

> ⚠️ 审查问题：原文提到预期加速比依赖于接受率 $\alpha$（`depends on the acceptance rate $\alpha$`），但紧随其后的公式中并未出现 $\alpha$ 变量。

其中 $c$ 是学生与教师前向传播成本的比率。通过利用学生和教师之间的合作来动态（on the fly）生成训练数据，Speculative KD 加速了同策略循环（on-policy loop），同时保持了与学生模型推理时分布（inference-time distribution）的对齐。一项互补的研究 [DistillSpec, 2310.08461] 则反转了这一方向。DistillSpec 并没有加速*训练*，而是利用同策略 KD 来改进用于*推理*阶段投机解码（speculative decoding）的草稿模型。在草稿模型自身生成的序列上，以目标模型的逻辑值（logits）作为监督（supervision）信号进行训练，可以提高接受率，并比标准的投机解码获得 10--45% 的推理加速。Speculative KD 和 DistillSpec 共同构成了同一枚硬币的两面；前者加速了蒸馏训练，后者则通过更好对齐的草稿加速了推理。

此外，跨分词器蒸馏（cross-tokenizer distillation）[cross-tokenizer distillation, 2402.12030] 技术已经成熟，通过在不同词表（vocabularies）之间对齐 token 概率分布，实现了在不同模型家族（disparate model families，例如从 Llama 到 Mistral）之间的 OPD。利用最优传输（optimal transport）来匹配学生词表 $V_S$ 和教师词表 $V_T$ 之间的 logit 分布，Universal Logit Distillation（ULD，通用逻辑值蒸馏）框架最小化了词表空间中的分布距离（distributional distance）：

$$
\begin{align}
\mathcal{L}_{\text{CrossTok}} = \inf_{\pi \in \Pi(P_S, P_T)} \mathbb{E}_{(z_S, z_T) \sim \pi} \left[ \parallel W_{S \to T} z_S - z_T \parallel_2^2 \right]
\end{align}
$$

从结构的角度来看，[Minitron, 2407.14679] 结合了基于重要性的结构化剪枝（importance-based structured pruning）与知识蒸馏，以生成继承教师架构的紧凑学生模型（compact students）。该方法首先通过在校准数据（calibration data）上使用轻量级的基于激活的指标（activation-based metrics）来评估神经元（neuron）和注意力头（attention head）的重要性，对最不重要的组件执行一次性结构化移除（one-shot structured removal），然后应用基于 KD 的重训练（KD-based retraining）来恢复准确率。与从头训练（training from scratch）相比，这种先剪枝后蒸馏流水线（pruning-then-distillation pipeline）所需的训练 token 数量减少了高达 40 倍，证明了从教师模型处进行架构继承（architectural inheritance）显著降低了收敛成本（convergence cost）。

在工业级 OPD 的前沿领域，[Nemotron-Cascade 2, 2603.19220] 展示了在一个拥有 30B 参数、仅有 3B 激活参数（activated parameters）的混合专家（Mixture-of-Experts）模型中进行的多领域同策略蒸馏。其后训练流水线（post-training pipeline）将级联强化学习（cascade RL）与跨越数学推理（mathematical reasoning）、代码生成（code generation）和智能体任务（agentic tasks）的特定领域 OPD 相结合，在 IMO（国际数学奥林匹克）、IOI（国际信息学奥林匹克）和 ICPC World Finals（国际大学生程序设计竞赛全球总决赛）中达到了金牌水平的表现；这是继 DeepSeek-V3.2-Speciale (671B-A37B) 之后第二个做到这一点的开源权重模型（open-weight model），且参数量减少了 20 倍。

---

### 计算与质量的权衡分析

一个被忽视的领域是 OPD（在线策略蒸馏，On-Policy Distillation）的成本效益分析。系统设计者经常面临在更多 token（词元）（off-policy，离线策略）与更好监督（on-policy，在线策略）之间分配计算资源的两难境地。我们将 $N$ 个 token 的预期计算成本（以 FLOPs（浮点运算次数）为单位）公式化如下：

$$
\begin{align}
C_{\text{off}} &\approx N \times (F_{\text{teacher}} + F_{\text{student}} + B_{\text{student}}) \\
C_{\text{on}} &\approx N \times \left( G_{\text{student}} + \lambda F_{\text{teacher}} + F_{\text{student}} + B_{\text{student}} \right)
\end{align}
$$

其中 $F, B$ 分别表示前向和反向的 FLOPs，$G$ 是 autoregressive generation（自回归生成）成本（由于 KV cache（键值缓存）的更新，它随序列长度呈二次方缩放），而 $\lambda \in (0, 1]$ 是教师监督刷新率（例如，对每个 token 评分与仅在序列末尾评分）。由于 $G_{\text{student}} \gg F_{\text{student}}$，$C_{\text{on}}$ 通常是 $C_{\text{off}}$ 的数倍，确切的比例取决于学生与教师的模型大小比例以及 $\lambda$。

令 $\mathcal{U}(\theta, C)$ 表示在给定计算预算 $C$ 的情况下，学生的 downstream utility（下游效用）。constrained optimization（约束优化）问题为：

$$
\begin{align}
\max \mathcal{U}(\theta, C) \quad \text{subject to } C = \gamma C_{\text{on}} + (1 - \gamma) C_{\text{off}} \le C_{\text{max}}
\end{align}
$$

其中 $\gamma$ 是使用在线策略处理的比例。对于通用知识迁移和语法对齐，由于 data manifold（数据流形）是密集的，$\gamma \to 0$（离线策略）就足够了。然而，对于推理、代码生成和复杂的数学问题，输出空间是高度多峰（multimodal）且脆弱的，$\frac{\partial \mathcal{U}}{\partial C_{\text{on}}}$ 远远超过 $\frac{\partial \mathcal{U}}{\partial C_{\text{off}}}$，这就证明了增加计算倍数是合理的。我们推荐一种 hybrid curriculum（混合课程训练策略）。从 $C_{\text{off}}$ 开始以预热 latent representations（潜在表示），然后在训练的最后 20% 阶段过渡到 $\gamma \to 1$，以微调 reasoning trajectories（推理轨迹）。

> ⚠️ 审查问题：原文中的 "highly multimodal" 在数学与概率空间的语境下意为“高度多峰的”（即存在极多不同的有效输出模式或局部解），而非深度学习中常见的“多模态”（图文/音视频结合）。翻译中已处理为“高度多峰（multimodal）”以防歧义。

**具体的成本示例**
为了将这些公式落到实处，考虑在 8$\times$H100 GPU 上将一个 70B 的教师模型蒸馏到一个 7B 的学生模型。在 10 亿 token 的离线策略中，教师模型离线生成数据集（约 200 GPU 小时），学生模型训练约 100 GPU 小时，总计约 300 GPU 小时。在 10 亿 token 的在线策略中，每一步需要（1）学生生成（由于 autoregressive decoding（自回归解码），成本约为前向传递的 3 倍），（2）教师评分（一次 70B 的前向传递），以及（3）学生反向传递；这将产生约 1,200--1,500 GPU 小时，即 4--5 倍的 overhead（开销）。

**GPU 显存开销与实用解决方案。** 除了 FLOPs 之外，white-box OPD（白盒在线策略蒸馏）最严峻的限制是 GPU 显存。同时保留 70B 的教师模型和 7B 的学生模型需要教师模型的权重（在 BF16 下约 140 GB），学生模型的权重和 optimizer states（优化器状态）（约 84 GB），以及最关键的，用于生成的 KV cache 和用于蒸馏的 full-vocabulary logits tensor（全词表逻辑值张量，$[B, T, |V|]$）。Peak memory（峰值显存）很容易超过一个 8$\times$80 GB 的 H100 节点。从业者可以通过以下方式缓解这一问题：（1）Teacher Quantization（教师量化）：以 FP8 或 INT4 格式部署教师模型，在精度损失可忽略的情况下实现 2--4 倍的显存缩减；（2）Logit Offloading/Recomputation（Logit 卸载/重计算）：立即将 logits 卸载到 CPU 内存，或仅保留 top-$k$；以及（3）Aggressive Gradient Checkpointing（激进的梯度检查点）：在反向传递期间最小化学生模型的激活显存。结合这些技术对于在标准集群上实现可行的白盒 OPD 至关重要。

然而，质量上的提升可能是巨大的。在 instruction-following benchmarks（指令遵循基准测试）中，在线策略方法始终以显著的优势优于离线策略 SFT（监督微调）；例如，[DistiLLM, 2402.03898] 实现了最先进的 ROUGE-L 分数，并且与之前的在线策略基线相比具有显著的训练加速。对于推理任务，off-policy ceiling（离线策略天花板），即无论数据量大小所能达到的最大性能，从根本上来说是较低的，因为静态数据集无法覆盖有效推理路径的 combinatorial space（组合空间）。这种 ceiling gap（天花板差距）随着任务复杂度的增加而扩大，这为在线策略方法提供了最强烈的动机，尽管其成本更高。

[Speculative KD, 2410.11325] 通过将学生的生成结果作为 speculative drafts（投机草稿），由教师模型并行验证，部分缩小了这一成本差距，从而产生更高质量的在线策略训练数据，而无需承担教师独立生成的全部成本，因为教师只需对学生的提案进行评分和纠正，而不是从头开始生成序列。

---

# 开放问题与未来方向

尽管前几节综述了该领域取得的快速进展——涵盖从 token-level divergence matching（词元级散度匹配）（第 \ref{sec:white_box} 节）、black-box（黑盒）与 self-play（自我对弈）设定（第 \ref{sec:black_box} 节），再到 reasoning-specific pipelines（特定推理流水线）（第 \ref{sec:reasoning} 节）——但其理论基础依然薄弱，且仍存在大量 scaling bottlenecks（扩展瓶颈）。下文我们将概述最关键的开放问题，并详细阐述问题定义、formalisms（形式化体系）、初步尝试以及具体的未来发展路径。

> ⚠️ 审查问题：原文中的 `\ref{...}` 交叉引用标签已在 Markdown 中直接保留为纯文本形式（如 `\ref{sec:white_box}`）。在实际的 Markdown 渲染或静态网站生成中，如果缺少相应的插件支持，这些标签可能无法正确解析为章节号。建议根据最终的发布平台将其替换为实际章节号或超链接。

---

## 蒸馏缩放定律

**问题定义。** Chinchilla 缩放定律（Chinchilla scaling laws，指预训练中模型参数与训练数据量之间的最优比例关系）定义了预训练的最优参数与数据比例，但在策略蒸馏（On-Policy Distillation，指学生模型在蒸馏过程中基于自身生成的样本进行学习的方法）领域尚无与之等效的定律。从业者目前只能猜测相对于学生模型规模的最优生成预算。理解蒸馏损失如何随学生模型参数 $N_S$、教师模型参数 $N_T$ 以及在策略词元（on-policy tokens，指模型在当前策略下生成并用于训练的文本单元）$D_{\text{on}}$ 进行缩放，对于有原则的计算资源分配至关重要。

**现有尝试。** 初步的研究仅拟合了经验性的幂律曲线，缺乏理论基础。一个具体的未来研究方向是推导出一个联合缩放定律：
$$
L(N_S, N_T, D_{\text{on}}) = E + \frac{A}{N_S^\alpha} + \frac{B}{N_T^\beta} + \frac{C}{D_{\text{on}}^\gamma} + f(N_S, N_T)
$$
其中 $E$ 是不可约简的任务熵（irreducible task entropy，指任务本身固有的、无法通过模型优化消除的最小不确定性），而 $f(N_S, N_T)$ 用于对学生和教师模型之间的容量差距干扰（capacity-gap interference，指由于学生和教师模型表达能力差异导致的学习阻碍）进行建模。

不断涌现的经验证据部分支持了这一结构。尽管 DeepSeek-R1 使用的是离策略蒸馏（off-policy distillation，指学生模型使用外部或固定的数据集而非自身生成数据进行学习的蒸馏方式）（因此没有探究 $D_{\text{on}}$ 这一维度），但其结果 [DeepSeek-R1, 2501.12948] 阐明了学生模型容量项 $A/N_S^\alpha$ 的作用。在 AIME 2024 数据集上，当固定教师模型参数为 671B 时，随着学生模型规模从 1.5B $\to$ 7B $\to$ 14B $\to$ 32B 变化，性能的缩放表现为 $28.9\% \to 55.5\% \to 69.7\% \to 72.6\%$，在超过约 14B 后出现边际收益递减。最陡峭的性能增长发生在 1.5B 到 7B 之间（绝对提升 26.6%），而 14B 到 32B 的跨度仅带来了 2.9% 的提升。这表明上述公式中的 $\alpha$ 可能很大（学生模型规模带来的收益快速饱和），而教师模型容量项 $B/N_T^\beta$ 占据主导地位；这也与 7B 学生模型在足够强大的教师模型指导下能在 MATH-500 上达到 92.8% 的准确率相一致。对在策略数据项 $C/D_{\text{on}}^\gamma$ 的验证仍然是一个未解决的经验性问题。

Qwen3 的经验 [Qwen3, 2505.09388] 进一步表明 $f(N_S, N_T)$ 是不可忽视的，因为从多个专用教师模型中进行蒸馏，比从一个总参数量相当的单一庞大教师模型中蒸馏能带来更好的缩放效果。未来的工作必须进行受控的网格搜索，独立改变 $N_S$、$N_T$ 和 $D_{\text{on}}$ 以解耦这些效应，从而使从业者能够回答诸如“在给定 $10^4$ GPU 小时的情况下，我应该使用 70B 的教师模型蒸馏 1B 个词元，还是使用 405B 的教师模型蒸馏 200M 个词元？”这样的问题。

作为对这些缩放观察结果的补充，文献 [2505.13111] 提供了一个关于*为什么*知识蒸馏能改善生成模型的最简解释。通过受控模拟，他们表明蒸馏会引发精确率-召回率权衡（precision-recall trade-off，在生成模型的语境下，精确率对应生成样本的质量，召回率对应生成样本的多样性与覆盖率）。随着教师模型的分布变得更具选择性，学生模型会以牺牲覆盖率（召回率）为代价，将概率质量集中在高似然区域（精确率），这一过程由单一的熵控制参数进行调节。在 SmolLM2 上的验证表明，这一动态过程揭示了当样本质量（精确率）优先于多样性（召回率）时，KD（Knowledge Distillation，知识蒸馏）尤为有益，这也为 KD 能够持续提升生成质量提供了理论依据。

---

> ⚠️ **审查问题**：
> 1. **交叉引用兼容性**：原 LaTeX 公式中的 `\label{eq:scaling}` 以及后文对应的 `Equation~\ref{eq:scaling}` 在标准 Markdown 中无法直接实现锚点跳转。译文中已去除 `\label` 标签，并将后文的引用意译为“上述公式”以保证文本流畅性。
> 2. **文献年份异常**：原文中的引用键值（如 `2501.12948`、`2505.09388`、`2505.13111`）符合 arXiv 预印本的命名规则，但其前缀指示的年份为 **2025 年**（如 2505 代表 2025 年 5 月）。这可能意味着原文为虚构文本、预测性文本或作者笔误。

---

### 教师模型校准与不确定性感知 OPD

**问题定义。** 白盒 OPD（White-box OPD）假设 $P_T$ 提供高质量、密集的信号。在现实中，教师模型受到过度自信（overconfidence）、幻觉（hallucination）和校准不良（poor calibration）的困扰；特别是在处于探索阶段的学生模型生成分布外（out-of-distribution，指偏离训练数据分布的数据）前缀时。当教师模型校准不良时，其 logits（逻辑值/未归一化的预测概率）会错误地反映成功的真实概率；如果学生模型生成了有缺陷的推理步骤，教师模型可能会为产生幻觉的后续内容分配高概率，从而将学生模型拖入错误级联（error cascade，指一个错误导致后续一连串错误）。此外，当容量差距（capacity gap，指教师与学生模型在能力或参数量上的差异）太小（教师模型几乎没有提供优势）或太大（教师模型的推理依赖于学生模型无法模仿的表征）时，标准的 OPD 目标就会退化。这造成了严重的*回音室效应*（echo chamber）：针对不确定的教师模型最小化 KL（Kullback-Leibler divergence，KL散度/相对熵）散度，会迫使学生模型自信地模仿噪声。

**现有尝试。** 当前的方法为所有 token（词元，文本处理的最小单元）的 KL 损失分配统一的权重，忽略了教师模型的可靠性。一个原则性的解决方案需要将教师模型的不确定性分解为偶然不确定性（aleatoric uncertainty，数据固有的）和认知不确定性（epistemic uncertainty，模型固有的）两部分，然后在教师模型的置信度不可靠时动态地对损失进行折扣。设教师模型在贝叶斯后验（Bayesian posterior）$q(\phi)$ 上的预测方差为 $U_{\text{epi}}(x) = \text{Var}_{\phi \sim q}[P_\phi(y|x)]$。一个不确定性感知（uncertainty-aware）的目标将按如下方式对蒸馏损失进行加权：

$$
\begin{aligned}
\mathcal{L}_{\text{Uncertainty-OPD}} = \mathbb{E}_{r \sim \ptheta} \left[ \sum_t \exp\big(-U_{\text{epi}}(r_{<t})\big) \KL\Big(\pteacher(\cdot | r_{<t}) \parallel \ptheta(\cdot | r_{<t})\Big) \right]
\end{aligned}
$$

通过在 $U_{\text{epi}}$ 较高时衰减梯度，学生模型可以依赖自身的先验（priors）而不是模仿幻觉，从而提高鲁棒性（robustness）。

> ⚠️ **审查问题：**
> 公式中使用了 `\ptheta`、`\pteacher` 和 `\KL`，这些通常是原 LaTeX 文档导言区中自定义的宏（如 `\newcommand{\ptheta}{p_\theta}`）。在纯 Markdown/MathJax 环境中直接渲染可能会报错（显示为未定义控制序列）。如果在网页或 Markdown 编辑器中使用，建议将其替换为标准 LaTeX（如 `p_\theta`、`p_{\text{teacher}}` 和 `\text{KL}`），或在渲染环境中补充宏定义。此处按照规则已保留原 LaTeX 源码。

---

### 动态课程蒸馏 (Dynamic Curriculum Distillation)

**问题定义。** 在 OPD（On-Policy Distillation，在线策略蒸馏）期间对提示词（prompts）进行均匀采样，忽略了学生模型不断演变的能力。让初学阶段的学生模型接触复杂的推理提示词会产生梯度噪声（gradient noise）；而让高阶阶段的学生模型接触过于简单的提示词则会浪费计算资源（compute）。

**现有尝试。** 受 [PACED, 2603.11178] 的启发，我们提出了一种基于自适应散度（adaptive divergence）的动态课程（dynamic curriculum）。设 $\mathcal{H}(x)$ 为提示词难度，由教师模型推理路径的熵（entropy）来量化。采样概率应随着训练步数 $t$ 演变：

$$
P_t(x) \propto \exp\left( -\frac{| \KL(P_T || P_{\theta_t}) - \delta_t |}{\tau} \right)
$$

其中 $\delta_t$ 是一个单调递增的步调函数（pacing function），$\tau$ 是温度系数（temperature）。这确保了学生模型始终在其当前能力的边界，即最近发展区（zone of proximal development）内针对提示词进行训练，从而最大化每步的训练效率。

---

> ⚠️ **审查问题：**
> 1. **逻辑矛盾**：原文第二段的小标题为 `\textbf{Existing Attempts.}`（现有尝试），但紧接着的正文却是 `we propose...`（我们提出……）。此处存在上下文逻辑矛盾，建议将小标题修改为 `Our Approach.`（我们的方法）或类似表述。
> 2. **LaTeX 宏定义**：公式中的 `\KL` 通常是作者自定义的宏（代表 Kullback-Leibler 散度），在标准的 Markdown 数学公式渲染器中可能会报错，建议在实际使用时替换为 `\text{KL}` 或确保您的渲染环境已定义该宏。
> 3. **缩写未定义**：原文 `OPD` 未给出全称，翻译中暂且推断并标注为 On-Policy Distillation（在线策略蒸馏），若该文语境为 Online Preference Distillation（在线偏好蒸馏），请根据全文语境进行调整。

---

### 针对词表不匹配的潜在空间蒸馏

**问题定义。** 公式 \ref{eq:cot_opd} 假设学生模型和教师模型共享相同的词表（vocabulary）。在实践中，将 Llama 模型蒸馏到 Phi 模型中会涉及严重的分词器不匹配（tokenizer mismatch）。对未对齐的分词器进行边缘化处理（marginalizing）在计算上是极其高昂的，并且会破坏高频语义信号。

**现有尝试。** 早期的跨分词器方法依赖于启发式字符串匹配（heuristic string matching）或静态嵌入（static embeddings）。最优解决方案在于深度潜在空间对齐（deep latent space alignment）。令 $h_t^S \in \mathbb{R}^{d_S}$ 和 $h_t^T \in \mathbb{R}^{d_T}$ 为逆嵌入层（unembedding layer）之前的最终隐藏状态（hidden states）。连续最优传输损失（continuous optimal transport loss）为

$$
\begin{align}
\mathcal{L}_{\text{Latent}} = \min_{W \in \mathbb{R}^{d_T \times d_S}} \mathbb{E}_{x} \left[ \parallel W h^S(x) - h^T(x) \parallel_2^2 + \lambda \mathcal{R}(W) \right]
\end{align}
$$

> ⚠️ 审查问题：前文定义的隐藏状态符号带有下标 $t$（即 $h_t^S$ 和 $h_t^T$），但在上述公式中使用的符号为 $h^S(x)$ 和 $h^T(x)$，缺少了下标 $t$，上下文符号表达存在不一致。

其中 $\mathcal{R}(W)$ 用于强制实现正交性（orthogonality）或稀疏性（sparsity）。潜在蒸馏完全绕过了词表瓶颈，使学生模型能够模仿教师模型推理流形（reasoning manifold）的几何结构，从而实现无缝的跨架构 OPD。

---

### 针对自主智能体的同策略蒸馏 (On-Policy Distillation)

**问题定义。** 当前的 OPD 主要针对单轮生成或线性的 CoT（Chain of Thought，思维链），然而大型语言模型（LLMs）正越来越多地作为与环境（API、终端、数据库）交互的自主智能体（Autonomous Agents）被部署。在智能体设定中，动作空间非常庞大且反馈具有高度延迟性；词元级别（token-level）的蒸馏无法捕捉到多步规划所需的长期信用分配（long-horizon credit assignment，指在多步决策中确定当前行动对最终结果的贡献或影响）。

**现有尝试。** 智能体 OPD（Agentic OPD）可以被重新构建为一个部分可观测马尔可夫决策过程（Partially Observable Markov Decision Process, POMDP）。假设 $\tau = (o_1, a_1, \dots, o_T, a_T)$ 是学生模型与环境交互的一条轨迹（trajectory）。教师模型扮演全知全能的价值函数（value function）$Q_T(o_t, a_t)$ 的角色，对中间动作进行打分。轨迹级别的目标函数变为：

$$
\begin{align}
\mathcal{L}_{\text{Agent-OPD}} = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t=1}^T \KL\Big( \pi_T(\cdot | h_t) \parallel \pi_\theta(\cdot | h_t) \Big) \cdot Q_T(h_t, a_t) \right]
\end{align}
$$

这在语言建模和强化学习（reinforcement learning）之间架起了桥梁，使得学生模型能够蒸馏出教师模型的战略远见和工具使用能力，而不仅仅是语言句法。

实际挑战不仅限于公式表述。首先是*环境非平稳性（environment non-stationarity，指环境的状态转移概率或观测空间受动作影响而发生动态变化）*，与“环境”（提示词）固定不变的文本生成不同，智能体环境会根据动作发生改变。一个在第 3 步进行了次优 API 调用的学生模型，在第 4 步面临的观测空间与教师模型原本会遇到的观测空间有本质上的不同，这使得直接的轨迹对比变得毫无意义。因此，教师模型必须提供*反事实（counterfactual）*评估；即基于学生模型的实际状态（而非教师模型的假设状态）来对学生模型的动作进行打分。

其次是*工具使用组合复杂性（tool-use combinatorics）*，现代智能体框架提供了数十种具有结构化参数模式的工具。蒸馏过程不仅必须传递调用哪个工具的知识，还要传递精确的参数构建、错误处理以及后备策略（fallback strategies）。词元级别的 KL（Kullback-Leibler散度）匹配非常不适合这种结构化的输出空间，这表明 Agent-OPD 可能需要作用于工具调用级别（tool-call level）而非单个词元的损失函数。

[SCoRe, 2509.14257] 提供了智能体级别蒸馏的早期实现。学生模型生成多步轨迹（包括工具调用和环境交互），而教师模型仅纠正最早出现的错误，而不是提供完整的演示。这种以学生为中心的方法避免了来自完整轨迹模仿的复合误差（compounding error，指误差在多步自回归生成中累积放大的现象）；学生模型学会了从自己的错误中恢复，而不是死记硬背特定的动作序列，从而产生能够迁移到新环境的更具鲁棒性的智能体策略。

第三是*安全攸关的信用分配（safety-critical credit assignment）*：在代码智能体中，一次错误的文件写入就可能损坏代码库；在网页浏览智能体中，一次误导性的点击可能会触发不可逆的动作。蒸馏框架必须结合安全约束，防止学生模型在同策略（on-policy）生成期间探索灾难性的危险序列，即使这些序列可能对学习具有信息参考价值。

***

> ⚠️ **审查问题：LaTeX 宏定义缺失风险**
> 在上述公式中，原文使用了 `\KL` 这一自定义 LaTeX 宏（通常在导言区被定义为 `\text{KL}` 或 `\operatorname{KL}`）。在标准的 Markdown 渲染器（如 KaTeX 或 MathJax）中，直接渲染 `\KL` 可能会报错提示 "Undefined control sequence"。建议在实际发布至 Markdown 平台时，将其替换为通用的 `\text{KL}` 或 `\operatorname{KL}`，或在渲染器配置中补充该宏定义。

---

### 3.1 多模态同策略蒸馏

**问题定义。** 当前的 OPD（On-Policy Distillation，同策略蒸馏）方法绝大多数针对纯文本的 LLMs（Large Language Models，大语言模型），但将同策略蒸馏扩展到 VLMs（Vision-Language Models，视觉-语言模型）是一个新兴且在很大程度上仍处于开放状态的研究方向。VLMs 面临着一个独特的挑战：高质量的视觉推理数据非常稀缺，而基于文本的推理数据却很丰富且易于验证。

**现有尝试。** VOLD [VOLD, 2510.23497] 证明了同策略蒸馏可以跨模态迁移推理能力。通过使用纯文本教师模型 (Qwen3-8B) 来指导 VLM 学生模型 (Qwen2.5-VL-3B)，VOLD 采用了一个两阶段的流水线：首先在教师生成的文本推理轨迹上进行 SFT（Supervised Fine-Tuning，监督微调）以完成初始对齐，然后在学生模型自身生成的轨迹（rollouts）上，使用一个结合了 GRPO（Group Relative Policy Optimization，群体相对策略优化）和密集词元级 KL 蒸馏（token-level KL distillation）的统一同策略目标进行训练。仅使用基于文本的训练数据，该方法在视觉推理基准测试（MMMU-Pro、MathVision、LogicVista）上的表现就超过了单独使用 GRPO 的效果。VOLD 的关键发现是，SFT 冷启动（cold-start）阶段对于跨模态蒸馏至关重要，这凸显了当教师和学生在不同的输入空间上运行时，分布对齐的重要性。

> ⚠️ 审查问题：原文提到纯文本教师模型为 "Qwen3-8B"，但目前公开的 Qwen 系列模型中主流为 Qwen2/Qwen2.5（如 Qwen2.5-7B 等），"Qwen3-8B" 极可能是原论文作者的笔误，建议核实。

Video-OPD [Video-OPD, 2602.02994] 将同策略蒸馏扩展到了时序视频定位（temporal video grounding）任务中，在该任务中，多模态 LLM 必须在未裁剪的视频中定位事件。通过将稀疏的 GRPO 奖励替换为来自更强教师模型的密集同策略蒸馏，并使用学生模型自身采样的时序预测作为训练分布，Video-OPD 在三个 TVG（Temporal Video Grounding，时序视频定位）基准测试上取得了 SOTA（State-of-the-Art，目前最先进）的结果，同时与基于 GRPO 的替代方案相比降低了训练成本。

---

### Distillation-RL 的良性循环

**问题定义。** 历史上，蒸馏（Distillation）和强化学习（RL，Reinforcement Learning）被视为线性的阶段（要么是 Distill $\to$ RL，要么是 RL $\to$ Distill）。然而，静态蒸馏会达到饱和，而纯 RL 会发散。真正的性能上限在于形成闭环（closing the loop），但在不发生灾难性遗忘（catastrophic forgetting，指模型在学习新知识时丧失对旧知识的记忆）或模式崩溃（mode collapse，指模型生成的样本失去多样性）的情况下实现这一点，仍然是一个悬而未决的挑战。来自 [2510.18874] 的经验证据表明，同策略（on-policy，指生成训练数据所用的策略与当前正在优化的策略相同）数据在缓解遗忘方面发挥着关键作用：在 Llama 和 Qwen 系列模型中，基于 RL 的后训练（post-training）比 SFT（Supervised Fine-Tuning，监督微调）保留了更多的预训练能力，这正是因为 RL 生成了同策略的轨迹（rollouts），这些轨迹保持了与学生模型先验（prior）分布的接近性。这表明，同策略的训练分布（而非奖励信号本身）是 RL 避免遗忘的主要机制，这也促使我们将同策略蒸馏作为一种抗遗忘的 SFT 替代方案。
在此基础上，[SDFT, 2601.19897]（在第 \ref{subsec:self_distill} 节中介绍）证明了自蒸馏（self-distillation）可以作为持续学习（continual learning）中一种有原则的 RL 替代方案。通过将 SFT 替换为一种同策略自蒸馏目标（该目标对模型自身的历史分布进行正则化），SDFT 实现了与基于 RL 的方法相当的抗遗忘能力，且无需显式的奖励函数，从而将同策略自蒸馏定位为一种既能获取新能力又不会牺牲现有能力的通用机制。

**现有尝试。** 我们将 Distillation-RL 循环形式化为交替投影（alternating projection）。假设目标能力流形（manifold）为 $\mathcal{M}^*$。学生模型 $\theta_k$ 经过 RL 来扩展其边界：$\theta_{k+1/2} = \theta_k + \eta \nabla J_{\text{RL}}$。由于 RL 会使参数空间扭曲并偏离语言先验（linguistic priors），因此蒸馏投影 $\mathcal{P}_{\text{KD}}$ 会将模型拉回到稳定的教师流形上：
$$
\begin{align}
\theta_{k+1} &= \arg\min_{\theta} \left( \parallel \theta - \theta_{k+1/2} \parallel_2^2 + \lambda \KL(P_T \parallel P_\theta) \right)
\end{align}
$$
证明这种交替算子（alternating operator）的收敛界（convergence bounds）并映射其压缩特性（contraction properties），是大语言模型（LLMs）递归自我提升（recursive self-improvement）的一个重要理论方向。

> ⚠️ 审查问题：
> 公式中的 `\KL` 通常是原作者在 LaTeX 导言区自定义的宏（如 `\newcommand{\KL}{\mathrm{KL}}`）。在标准的 Markdown/MathJax 渲染器中，直接使用 `\KL` 可能会因为未定义而报错（显示为红色源码）。如果您的 Markdown 渲染环境不支持自定义宏，建议将其手动修改为 `\text{KL}` 或 `\mathrm{KL}`。为遵守“公式保留 LaTeX”的指令，译文中暂未做修改。

---

### 超越基准测试的评估方法

**问题定义。** 标准基准测试（如 MMLU、GSM8K）受到数据污染（Data Contamination，指测试数据泄露到训练集中的现象）的影响，且仅能衡量静态模式匹配，无法捕捉蒸馏后的学生模型（Student Model）相对于其教师模型（Teacher Model）的内在鲁棒性（Robustness，指模型面对扰动时的稳定性）、OOD 泛化能力（Out-of-Distribution Generalization，分布外泛化能力，指模型在未见过的、与训练数据分布不同的数据上的表现）以及幻觉率（Hallucination Rates，指模型生成看似合理但实际不正确或无根据内容的比率）。

**现有尝试。** 评估必须转向动态对抗性测试（Adversarial Testing，通过引入恶意扰动来评估模型缺陷的测试方法）。我们将泛化差距 $\Delta_{\text{OOD}}$ 定义为在对抗性扰动 $\epsilon$ 下，学生模型与教师模型之间的詹森-香农散度（Jensen-Shannon Divergence，一种衡量两个概率分布相似度的方法）：

$$
\Delta_{\text{OOD}} = \max_{\parallel \epsilon \parallel \le \delta} \text{JS}\Big( P_T(\cdot | x + \epsilon) \parallel P_S(\cdot | x + \epsilon) \Big)
$$

> ⚠️ 审查问题：原文第二段开头使用了“Existing Attempts”（现有尝试），但其后续内容（“Evaluation must move toward...” 以及“We define...”）表述的更像是本文提出的新方法或未来的研究方向，而非对已有工作的总结。建议确认原文此处的粗体小标题是否应为“Proposed Approach”（提出方法）或“Future Directions”（未来方向）以保持逻辑连贯。

未来的基准测试套件必须在语义等价但句法多样的提示词（Prompts）上系统地计算这一散度，从而验证学生模型是否学到了推理的潜在因果机制（Causal Mechanism），而不是仅仅学到了表层相关性（Superficial Correlations）。

---

### 实践指南与决策框架

**问题定义。** 工程团队缺乏用于选择正确蒸馏方法的算法框架。大量的技术（离线策略（off-policy）、基于逻辑值（Logit）的在线策略蒸馏（On-Policy Distillation, OPD）、基于奖励的在线策略蒸馏（Reward-OPD）、投机知识蒸馏（Speculative KD））导致了决策瘫痪。

**现有尝试。** 我们将该决策形式化为基于三个变量的分段选择，这三个变量分别是可用计算力（Available Compute, $C$）、学生模型容量（Student Capacity, $S$）和任务复杂度（Task Complexity, $\mathcal{T}$）。最优策略 $\Pi^*(C, S, \mathcal{T})$ 为：

$$
\begin{aligned}
\Pi^*(C, S, \mathcal{T}) =
\begin{cases}
\text{Off-Policy KD}, & \text{if } C \le \tau_{\text{low}} \lor \mathcal{T} \in \text{Syntax/Chat} \\
\text{Logit-based OPD}, & \text{if } C > \tau_{\text{low}} \land S < 3B \land \mathcal{T} \in \text{Reasoning} \\
\text{Reward-aware OPD}, & \text{if } C \gg \tau_{\text{high}} \land S \ge 3B \land \text{Access to Verifier} \\
\text{Speculative OPD}, & \text{if Latency Bound is strict } \land \text{Teacher is white-box}
\end{cases}
\end{aligned}
$$

> ⚠️ 审查问题：原文小标题为 "Existing Attempts"（现有尝试），但后文紧接着写 "We formalize..."（我们将该决策形式化为...），逻辑上似乎存在矛盾。通常 "现有尝试" 描述的是前人的工作，建议检查原文此处是否应为 "Our Approach" 或类似表述。

除了这个决策矩阵之外，我们还从所调研的文献中提炼出了实践经验，并将其转化为具体的建议。

**何时使用离线策略蒸馏（off-policy distillation）。** 对于通用的指令遵循（instruction-following）和对话任务，在教师模型生成的数据上进行离线策略监督微调（Supervised Fine-Tuning, SFT）仍然是最具成本效益的起点。高质量的教师数据结合偏好优化（preference optimization），能够以在线策略（on-policy）计算成本的一小部分实现具有竞争力的性能。建议从这里开始，并在投资在线策略基础设施之前衡量性能差距。

**何时必须使用在线策略（on-policy）。** 当出现以下情况时，向在线策略蒸馏的过渡是合理的：（1）学生模型表现出明显的曝光偏差（exposure bias），即在教师风格的提示词（prompts）上表现良好，但在措辞不同的用户生成提示词上却表现不佳；（2）任务涉及多步推理（multi-step reasoning），其中复合错误（compounding errors）会降低生成质量（如数学、代码、逻辑推导）；或者（3）学生模型需要通过奖励引导的探索（reward-guided exploration）在特定领域超越教师模型。

**在基于逻辑值（logit-level）和基于奖励（reward-level）的 OPD 之间做选择。** 如果教师模型是白盒（white-box）且学生模型较小（$<$7B），基于逻辑值的方法（GKD、DistiLLM）能够提供小模型所需的密集监督（dense supervision）。对于配备了结果验证器（outcome verifiers）的较大规模学生模型（$\ge$7B），基于奖励的 OPD（RLKD、AlignDistil）能够使其发现新颖的求解路径。混合方法（先进行离线策略 SFT 预热（如 DeepSeek-R1 中所示），然后进行基于逻辑值或基于奖励的在线策略微调）始终能产生最佳结果。

**“蒸馏税（distillation tax）”预算规则。** 基于第~\ref{sec:systems} 节中的计算力分析，一个实用的经验法则是将 60--70\% 的训练预算分配给离线策略预热（off-policy warm-up），20--30\% 分配给在线策略逻辑值蒸馏（on-policy logit distillation），10\% 分配给基于奖励的优化（reward-guided refinement）。这种分阶段的方法将廉价、高带宽的学习前置，并为最终的质量提升保留昂贵的在线策略计算力。

---

[翻译失败: \section{Conclusion}]
stderr: 2026-03-30 12:32:19,892 [ERROR] Gemini call failed: HTTP 200 but empty response: {'code': 1021, 'msg': '大模型结果解析失败:{"error":{"message":"当前分组上游负载已饱和，请稍后再试","type":"upstream_saturated","param":"","code":null}}, 详见https://iwiki.woa.com/p/4016609149', 'answer': None, 'search_results': 
2026-03-30 12:32:1

---

