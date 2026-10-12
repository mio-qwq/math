# 数学成果与证据目录

本目录对应 **2026-10-12** 的主分支材料与独立验收记录。它区分原公开问题的完整解答、特殊情形、经典定理的推论、方法障碍和未验收候选。同一问题的书面证明、程序、推广和 Lean 实现不重复计为不同突破。精确源版本及集成变化另见各专题的 `provenance.json`；运行证据见 `VERIFICATION.json` 或既有 Lean 收据。

**状态用语：**“完整 Lean”仅指所明确列出的数学范围已有实际编译、声明和公理审计；“独立书面复核”指未参与相应发现的研究 AI Agent 对完整论证进行复核，不能称为外部人类同行评审；“候选”未获得相应全链验收。历史原创性另行判断：没有检索到先例不能证明首创。本文不声称任何成果已经被期刊接受。

## 原公开问题的完整解答：已集成，所列范围有完整 Lean

| 问题、来源与原命题 | 数学结论 | 证明与实际验证 |
| --- | --- | --- |
| **006 强积打包支配继承**，Bujtás 等 [arXiv:2510.02749v1 Conjecture 3.1](https://arxiv.org/html/2510.02749v1#S3)：一因子无可行打包支配，是否任意强积仍无可行方案？ | **严格反例**：$\gamma_2^3(Q_6)=\infty$，而对显式 608 点辅助图 $H$，$\gamma_2^3(Q_6\boxtimes H)\le64$。不声称 64 最优。 | [专题与实际 Lean 范围](006-strong-product-packing-counterexample/README.md)；[v1.3 论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf)；[复现包](publication/006-v1.3/README.md)。**River Zhang、Yongxian Zhang**，2026-10-11 [Zenodo 版本 DOI](https://doi.org/10.5281/zenodo.23293088)，[概念 DOI](https://doi.org/10.5281/zenodo.23293087)。公开预印本，不等于同行评审。 |
| **置换有向图 GP 最优性**，Chandran 等 [2604.15909v1 §3.3 Theorem 3.6 后未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS3)：$\operatorname{gp}(\mathrm{Pe}(d,k))=2(d+k-2)_{k-1}$。 | **严格反例**：$\mathrm{Pe}(6,3)$ 有 90 点一般位置集，超过猜想值 84。未计算其精确 GP 最大值。 | [定理、全参数构造与来源](workstreams/ROOT/permutation-gp-counterexample/THEOREM.md)；[实际图 Lean](workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean)；[18 项审计](workstreams/ROOT/permutation-gp-counterexample/verification.json)。 |
| **无爪次三次图 $(1,1,3,3,4)$ 打包着色**，Mortada 等 [2608.02566v1 §6 Problem 1](https://arxiv.org/html/2608.02566v1#S6)，排除原文指定 12 点例外。 | **严格反例**：36 点连通三正则无爪图无该着色，且不同于指定例外。$12k$ 点奇数 $k\ge3$ 反例族另有完整书面证明。 | [构造及无限族范围](workstreams/ROOT/clawfree-11334-counterexample/README.md)；[固定 36 点 Lean](workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean)；[18 项审计](workstreams/ROOT/clawfree-11334-counterexample/lean-audit.json)。不声称最小反例或无限族全 Lean。 |
| **2-saturated 次三次图 $(1,1,2)$ 猜想**，El Zein–Mortada [2603.25113v1 Conjecture 3](https://arxiv.org/html/2603.25113v1#S5)。 | **严格反例**：细分 $K_4$ 同一顶点的三条关联边得到 7 点 9 边图，满足原始全部假设，无目标着色。 | [专题](workstreams/ROOT/two-saturated-112-counterexample/README.md)；[实际图及任意着色 Lean](workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean)；[14 项审计](workstreams/ROOT/two-saturated-112-counterexample/lean-audit.json)。不否定另有局部围长假设的定理。 |
| **循环图 monophonic position 存在性**，Tuite–Thomas–Chandran [AMC 25 (2025), Conjecture 4.5](https://oro.open.ac.uk/92086/13/92086final.pdf)：每个 $n\ge11$ 是否存在直径 2、mp 数 2 的循环图？ | **严格反例于全称存在性**：$n=15$ 时不存在。排除全部 128 个对称连接集，不只是找到一个失败的图。 | [专题与原定义桥](workstreams/ROOT/monophonic-circulant15-counterexample/README.md)；[诱导路径 Lean](workstreams/ROOT/monophonic-circulant15-counterexample/MonophonicCirculant15.lean)；[7 项审计](workstreams/ROOT/monophonic-circulant15-counterexample/lean-audit.json)。 |
| **笛卡尔积下 GP 数继承**，Kruft Welton–Khudairi–Tuite [2404.19451v1 Conjecture 2.10](https://arxiv.org/html/2404.19451v1)／期刊版 Conjecture 3：$\operatorname{gp}^-(G\square H)\ge\min\{\operatorname{gp}^-(G),\operatorname{gp}^-(H)\}$。 | **严格反例**：11 点与 29 点因子的下 GP 数都至少 6，但 319 点积图有一个仅 5 点的极大 GP 集。无限差距与尖锐修正界另有书面证明，见下表。 | [专题](workstreams/ROOT/lower-gp-product319-counterexample/README.md)；[固定反例的全部极大性 Lean](workstreams/ROOT/lower-gp-product319-counterexample/LowerGPProduct319.lean)；[15 项审计](workstreams/ROOT/lower-gp-product319-counterexample/lean-audit.json)。 |
| **CDC 主特征值**，Collins–Sciriha [1906.05790v1 Question 5.8](https://arxiv.org/pdf/1906.05790)／期刊版 Question 16。 | **完整正面答案**：$M(\operatorname{CDC}(G))=M(G)$；覆盖同构推出主特征值集合相同。结论可直接蕴含于原作者 Theorem 3.3，不作为新数学首创宣传。 | [定理与来源](workstreams/ROOT/cdc-main-eigenvalues/THEOREM.md)；[全有限图 Lean](workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean)；[7 项审计](workstreams/ROOT/cdc-main-eigenvalues/verification.json)。这里的贡献是明确证明与形式化，非全部谱相同。 |

这里打包着色中的重复半径仍代表不同颜色；有向 GP 使用所有最短有向路径，monophonic position 使用所有诱导路径，下 GP 数是极大 GP 集的最小基数。三种定义不能互换。

## 完整书面解答：已集成并独立复核，尚无完整 Lean

以下论证覆盖所列原命题的全范围。计算机辅助项同时需要完整结构归纳及精确证书，有限样本不能替代它们。来源和旧验收与当前字节的对应关系保存在各专题，旧的作者自测不改写为本轮独立执行。

| 原题 | 完整结论及重要限定 | 主分支材料 |
| --- | --- | --- |
| **Gorzkowska–Kwaśny Conjecture 10**，[2609.11832v1](https://arxiv.org/html/2609.11832v1#S5)。 | 任意固定正常边着色下，非 $K_2$、非偶圈的连通简单图存在区分每条边两端完整关联颜色序列的全局边序。全部 $d\ge3$ 正则、恰 $d$ 色情形由构造补足；其余情况明确使用原 Theorem 5。颜色不改动。 | [完整证明、经典辅助定理与严格证书工具](workstreams/ROOT/edge-order-distinguishing/README.md)。修复旧导入问题；完整图构造及严格 K6 证书有小型独立复现，不冒称重跑作者全部大枚举。 |
| **Braun–Bruegge Conjecture 31**，[JIS 26 (2023) Article 23.7.2](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf)；arXiv v4 编号 5.1。 | 原二项式和 $F$ 的同奇偶合法两单位转移不减，给出原固定和极值。至少三行同奇偶推广严格增；偶数行的跨奇偶比较另有证明。 | [原标量、推广及跨奇偶附节](workstreams/ROOT/braun-bruegge-f31/README.md)。不是广义简单图或多面体全部极值猜想的解答。 |
| **连续生成元有向循环图最优性**，[2604.15909v1 §3.1 Theorem 3.3 后未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS1)。 | 所有 $1\le d<n$，$n=qd+r$、$2\le r\le d+1$：$r=d+1$ 时 GP 为 $d+1$；否则为 $\max\{r,\lfloor d/r\rfloor+1\}$。 | [完整精确公式](workstreams/ROOT/distributed-written-proofs/B/circulant/README.md)。旧余数计数 Lean 仅是标量辅助引理，不是实际图的完整形式化。 |
| **El Zein–Mortada Conjecture 1**，[2603.25113v1 §5](https://arxiv.org/html/2603.25113v1#S5)。 | 0-saturated 次三次图中，每个三度点局部围长至多 4，则标准打包色数至多 4。包括任意连接长度与非连通分量。 | [完整证明](workstreams/ROOT/distributed-written-proofs/B/packing_extension/README.md)。 |
| **同文 Conjecture 2**。 | 每个三度点在三角形上的 1-saturated 次三次图具有标准五色打包着色，半径 $(1,2,3,4,5)$。 | [结构论证、完整有限状态证书与无限归纳](workstreams/ROOT/distributed-written-proofs/B/triangle_packing/README.md)。其他 palette 的候选不随之验收。 |
| **同文 Conjecture 6**。 | 每个三度点在三角形上的 $(3,0)$-saturated 次三次图具有 $(1,1,2)$ 打包着色。原文 heavy 点定义及独立性假设保留。 | [全范围证明](workstreams/ROOT/distributed-written-proofs/B/heavy_triangle_112/README.md)。不是仅匹配连接模板。 |
| **无爪次三次图 $(1,2,2,2,2)$ 猜想**，[2608.02566v1 §6 Conjecture 1](https://arxiv.org/html/2608.02566v1#S6)。 | 全范围正面答案，由已有 **Yang–Wu 2022 边着色定理**得到完整推论桥。 | [证明与明确归属](workstreams/ROOT/distributed-written-proofs/B/clawfree_12222/README.md)。已有定理推论，不宣称新一般边着色定理。 |
| **Mizzi v3 §7 两项猜想**，[2603.27559v3](https://arxiv.org/html/2603.27559v3#S7)。 | 第一项：每对非同构 TF-cousins，一图有同长两条不交奇圈 $C_k$，另一图有 $C_{2k}$。第二项：连通非对称不稳定图有互不交 $C_k,C_{2k}$，$k\ge3$ 奇。 | [完整图对证明与非对称定理](workstreams/ROOT/distributed-written-proofs/C/mizzi/README.md)。更一般入口须显式假设非平凡 TF 对；不把任意非连通 CDC 不稳定性作为等价假设。[2608.15281](https://arxiv.org/abs/2608.15281) 的旧版反例不等于否定 v3 非对称修订项。圈非必诱导。 |
| **顶点位置数比率有界性**，Thankachy 等 [DMGT 44 (2024), Problem 4](https://doi.org/10.7151/dmgt.2491)／[2209.00359v2 Problem 2.4](https://arxiv.org/abs/2209.00359)。 | **完整负答案**：连通图的 $\mathrm{vp}/\mathrm{vp}^-$ 无界；即使限于二部、最大度至多 3，仍无界。两族是同题负答案及强化，不重复计数。 | [全参数族与距离证明](workstreams/ROOT/distributed-written-proofs/B/vertex_position_ratio/README.md)。固定根参数是最大根位置集的基数，不是下 GP 数。 |
| **Bychawski Conjecture 6.5**，[2406.06267v1](https://arxiv.org/html/2406.06267v1)。 | 随机标号图在 $n(1-\varepsilon)/2$ 次边翻转内获得非平凡 TF 投射的概率趋零。另得连通、非二分、无开孪生目标的距离 $D_n/n\to1/2$（依概率）。 | [自足完整证明、修正说明与有限回归](workstreams/ROOT/tf-edit-distance/README.md)。下界针对所有非恒等 TF 对；上界产生普通自同构，并非非对角不稳定性构造。经典随机图对称性阈值明确作为相关既有研究。 |
| **非平凡不稳定图渐近计数**，Hujdurović–Mitrović [2210.15249v1 Problem 5.3](https://arxiv.org/html/2210.15249v1#S5)。 | 完整渐近主项：$U_n\sim 2^{\binom{n-4}{2}+2(n-4)-1}/(n-4)!$；典型自同构群为 $C_2$，覆盖群为阶 8 的 $D_8$。 | [计数、典型群与前置正规形](workstreams/ROOT/distributed-written-proofs/C/tf-count/README.md)。作者四点添加构造归原论文；固定模式下界与全局渐近主项区别明确。更强误差及有限常数候选未随之验收。 |
| **下 GP 继承的尖锐修正界**，原被反驳命题的正确替代。 | 任意非空有限简单图满足 $\mathrm{gp}^-(G\square H)\ge\min\{5,\mathrm{gp}^-(G),\mathrm{gp}^-(H)\}$；每个 $r\ge6$ 有连通因子下 GP 数至少 $r$、积图下 GP 数恰为 5 的族。 | [完整修正界、精确证书与无限族](workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/README.md)。固定 319 点反例全 Lean；全称修正界和无限族仅书面／计算机辅助验收。已有 true-twin 方法明确归属。 |

## 重要特殊情形与结构性成果

| 成果 | 已证明范围与证据 | 未解决或既有结论边界 |
| --- | --- | --- |
| **有限树 GP 谱定理** | 全部有限树在所有定向下的 GP 数谱是整数区间；[完整树 Lean 与 44 项审计](workstreams/ROOT/gp-tree-spectrum/README.md)。 | 原 [Conjecture 4.30](https://arxiv.org/html/2604.15909v1#S4.SS2) 针对任意图，尚未由此解决。森林推广另为书面。 |
| **Kautz 词长三精确公式** | 所有 $m\ge3$：$\operatorname{gp}(\mathrm{Ka}(m,3))=m(m-1)(2m-1)/6$；[实际路径与全部基数 Lean、24 项审计](workstreams/ROOT/kautz3-exact-gp/README.md)。允许首尾字母相同。 | 原作者表格已有有限数值观察；贡献是全参数证明与形式化。一般词长 [Problem 5.2](https://arxiv.org/html/2604.15909v1#S5) 未解决。 |
| **Kautz 词长四密度** | 极限 $\lambda_4$ 存在且 $26/125\le\lambda_4\le377/1320<2/7$；[全称书面上下界与 27 状态证书](workstreams/ROOT/distributed-written-proofs/B/kautz_length4/README.md)。有限取整加强上界仅 $m\ge11$。 | 精确有限值及极限值未知；无完整 Lean。 |
| **Braun 多行同奇偶与跨奇偶结构** | [严格转移、唯一极值与跨奇偶变化](workstreams/ROOT/braun-bruegge-f31/README.md)。 | 原标量结论的推广，不另计为原猜想突破；不能从同奇偶比较外推跨奇偶。 |
| **固定 TF 模式与计数下界** | [独立验收的正规形与下界](workstreams/ROOT/distributed-written-proofs/C/tf-count/README.md)。 | 是全局主项证明的结构前置，不能重复当作另一完整计数问题的解答。 |

### 001–006 的既有研究

| 项目 | 主要贡献及材料 | 形式化和来源边界 |
| --- | --- | --- |
| [001 Hadamard 幂刚性](001-odd-half-order-hadamard/README.md) | 根约束、完整相位结构分类、相位圆与有限解图、标准等价商。 | Hadamard switching 等理论已有先例；原创范围按专题区分，不把分类与构造重复计数。 |
| [002 加权矩形剪枝](002-weighted-rectangular-pruning/README.md) | 部分非乘积权重、非 block 关系及多种可精确证明的成本结构。 | 有实际 Lean 和核验；任意关系／任意独立成本不在已证范围。 |
| [003 一参数 ARC 相关代数](003-arc-one-parameter/README.md) | 共振 Yoneda/Tate 结构、实际下层投射分解与正次数 self-Ext 消失等。 | 按实际假设及 [OpenAI／Tang 归属](003-arc-one-parameter/ATTRIBUTION.md)区分已知结论和新增形式化；未声称完整 ARC 或缺失的同调桥已完成。 |
| [004 六维 MUB 三元组](004-mub-triplets/README.md) | 循环特征标、平坦 Gram 消去、条件性桥接。 | 不等于解决一般六维 MUB 猜想；经典 Zauner 构造明确归属。 |
| [005 有向圈打包](005-directed-cycle-packing/README.md) | 已保存的特殊情形、必要条件与计算材料。 | 不等于一般有向圈打包猜想的完整解答。 |
| [006 强积反例](006-strong-product-packing-counterexample/README.md) | 完整反例、Lean、英文论文、复现附件及已公开 Zenodo DOI。 | 唯一在这里明确标为已有 Zenodo 预印本的交付；外部预印本、期刊审稿与 GitHub 验收不同。 |

既有单因子、代数和路径模块的详细目录仍见 [根 README](README.md#完整研究目录) 与 [FORMALIZATION.md](FORMALIZATION.md)。旧索引各有自己的覆盖日期；近期模块以本目录直接链接为准。

## 密码结构研究：限定数学范围

[专题、冻结来源和复现证据](workstreams/ROOT/cryptographic-structures/README.md)统一列明以下不同状态。这些不是完整密码算法安全性被攻破的声明。

| 对象 | 结论或材料 | 实际限制 |
| --- | --- | --- |
| **Circulant related-differential 结构** | 特征 2 域上，每个阶 $n\ge3$ 的可逆 circulant 存在非平凡 RD 对；周期商继承 MDS。完整书面证明、独立复核及固定 10 阶精确证书。 | 完成 [Kumar–Yadav–Samanta 2605.27535v1](https://arxiv.org/abs/2605.27535) 指出的剩余方向；该文未给这部分完整编号猜想。已有 odd／4 整除等基础结论明确归属。无完整 Lean、攻击复杂度或首创认证；$n=2$ 不包含。 |
| **Ascon 两轮局部传播** | 真 320 位全状态均匀模型中，至多两列活跃时 DDT 乘积精确；三列支持完整分类，320 个支持可出现误差，其余 41,344 个精确；每条三列 path 满足 $0\le P\le2M$，且界尖锐。 | 640 是投影秩异常数，320 才是实际可能误差支持数。固定 path 有 $P=2M$ 与 $P=0$ 的精确例。无完整 Lean；不是固定 IV／密钥初态、完整 AEAD、所有轮数或端点差分不可能性的结论。 |
| **ChaCha C001–C008** | 三加法端点、固定字与有限状态矩方法的精确局部相关公式，有限范围复现通过。 | 技术基线；历史原创性未通过。有参数域、均匀／固定输入条件和算术复杂度限制，非最佳攻击或完整 ChaCha20 的结果。 |
| **RSA 条件恢复与范围审计** | 已供应短 primitive ideal-power relation 时的高次结构候选及指定 determinant/projection 路线障碍；最新 [v2 整数链与适用范围](https://github.com/mio-qwq/math/blob/3558a51aabcf1242c2b8c40162643f9b260d937a/workstreams/CRYPTO2-20261011-7f3c/projects/rsa-short-relations/v2/PROOF.md)附八个窄范围 Lean 声明及作者编译／公理日志。普通 RSA 的 $t=0$ 恢复输出落入经典 continued-fraction 范围。 | **高次结构全链仍待精确版本独立验收**；窄 Lean 仅以已供应短线性关系为前提，本轮未独立重编译，不覆盖关系存在性、Legendre 定理或攻击复杂度。不解决原 MNV Q2，不扩大攻击可达范围；$t=0$ 不能推广到正 y-shift。 |
| **SHA-256 消息扩展下界候选** | 对实际 32 位模加的 16→64 word 扩展，提出不同输入至少 13 个异字的必要 support 下界；[冻结证明与证书入口](https://github.com/mio-qwq/math/blob/3558a51aabcf1242c2b8c40162643f9b260d937a/workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/PROOF.md)。本轮固定证书重放核对 5,308,416 条转移不等式，五个损坏控制均被拒绝。 | **尚待完整新数学包的全链独立验收**。13 仅在 support relaxation 内锐利，实际消息对达到等号未知；特定零基 support 排除不能外推任意基，任意基 lift 超时是 unknown。没有完整 Lean、新攻击或原创性确认。 |
| **Keccak 投影** | 已保存原始实例及文献门控。 | **尚无本项目新定理／全局界**；未重建完整实例或运行 $2^{28}$ 枚举。 |

## 未验收候选与方法障碍

候选保留原冻结材料，并不因邻近定理通过而自动获验收。以下是科学状态，不能当作已解决公开问题。

| 材料 | 尚未完成的具体对应或验收 | 冻结入口 |
| --- | --- | --- |
| **CG 奇参数全部 TF-cousin 分类** | 全 odd $n\ge3$ 精确二 cousins、自同构群与参数例外缺精确绑定的全称独立复核。$n=3$ 或有限检查不能替代。 | [C-audit 9ad1f91](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/CG_ODD_COMPLETE_THEOREM.md)。 |
| **Bychawski Conjecture 6.6 精细展开** | 全 TF／投射／条件 reduced 三种期望的一阶项与有效常数尚未整体验收。已发现 [MathDB 的既有公开证明声称](https://mathdb.com/p/363470/conjecture-on-the-expected-size-of-the-two-fold-automorphism)，尚未独立复验该解答；不能宣称该极限未有公开解答或本项目首次。 | [冻结候选](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/BYCHAWSKI_C66_EXPECTED_TF_GROUP.md)。C65 仅复用已审熵引理，不验收整个 C66 包。 |
| **不稳定图更强误差／有效阈值** | 全局主项已复核，但 $O(2^{-n/4})$ 等更强误差及有限常数没有同范围独立验收。 | [定量候选](https://github.com/mio-qwq/math/blob/9ad1f91d953060d01a504481eb857daf57758ab0/workstreams/C-audit-1010/QUANTITATIVE_ERROR_AND_AUT_GROUP_REVIEW.md)。 |
| **下 GP 的 Kneser／line-graph／混合族与其他 palettes** | 更强指定家族结论，以及三种其他 packing palette 的证明未获对应全链验收；通用 min5 或五色结论不自动认证它们。 | [B 冻结](https://github.com/mio-qwq/math/tree/802e030aa8ac47a2018c9441a6b19f59b2db2535/workstreams/B)。 |

已有方法障碍另见：[$Q_6\boxtimes Q_6$ 仿射中心与六点分类](notes/q6-strong-product-affine-obstruction.md)、[$C_7$ 指定格点族界](notes/c7-fraction-family-barrier.md)、[指定 $D_5$ 三根删除界](notes/d5-three-root-cap.md)、[三角形局部交换规则反例](notes/triangle-swap-safety.md)、[七核短圈替换族界](notes/seven-core-short-cycle-substitution.md)。它们分别有精确对象和证据，均不能改称相应一般公开猜想的解答。

## 可复现性与学术归属

新集成的数学源来自明确冻结的公开分支；原历史提交及原作者记录原样保留。必要展示修正、依赖复制和当前运行范围逐文件记录，完整理论证明与程序有限检查分别陈述。程序只在其实际输入域有效；未执行的旧枚举没有重新标记为已运行。已有 Lean 源未修改时，本次核对其当前哈希与真实历史收据，不伪造新编译日期。

AI 系统实际参与数学推导、程序与 Lean 开发、文献分析、独立复核和写作。AI 不列为论文作者；其他专题技术集成不会自动取得 006 的作者署名、作者确认、DOI 或投稿状态。首创性、外部人类评审和形式化范围需分别核查。
