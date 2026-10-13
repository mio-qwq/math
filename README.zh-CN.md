# 数学研究：证明、反例与 Lean 形式化

**简体中文** | [English](README.md)

本仓库研究公开数学问题，收录严格反例、完整证明、结构分类及可复现的计算与形式化材料。研究覆盖图论、组合数学、矩阵结构和同调代数；核心目标是对原始问题给出准确、可独立核验的数学答案。

这里分别记录**数学结论、形式化覆盖范围、独立复核和发布状态**。书面证明与 Lean 证明具有不同的验证范围；分支上的成果也不会因作者自行标记通过而自动成为主分支正式成果。本页的已验收数学成果目录依据 **2026-10-12** 汇整的源码与验证记录，并包含 **2026-10-13** 的论文更新及当日远端分支核对；详细假设、文献关系及后续更新以各专题材料为准。部分链接材料为中文。

[全部成果与证据目录](RESEARCH_RESULTS.md) · [已解决或证伪的公开数学问题](#已解决或证伪的公开数学问题) · [完整研究目录](#完整研究目录) · [分布式成果及待验收范围](#分布式成果及待验收范围) · [证明与复现](#证明与复现) · [未完成问题与方法边界](#未完成问题与方法边界) · [学术声明](#学术声明)

**已公开数学预印本（006）**：[A counterexample to packing-domination inheritance in strong products](https://doi.org/10.5281/zenodo.23293088)，作者 **River Zhang、Yongxian Zhang**，Zenodo，2026-10-11，论文 **v1.3**（首次 Zenodo V1）。 [Version DOI：10.5281/zenodo.23293088](https://doi.org/10.5281/zenodo.23293088) · [Concept DOI：10.5281/zenodo.23293087](https://doi.org/10.5281/zenodo.23293087) · [论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf) · [复现附件](publication/006-v1.3/006-v1.3-reproducibility.zip)。本成果为**公开预印本，尚未经过期刊同行评审**。

**新增论文冻结稿（2026-10-13）**：[笛卡尔积下 GP 的反例、无界差距与尖锐修正界](publication/lower-gp-cartesian-v0.1/README.md)（13 页）与[无爪次三次图打包着色反例及无限族](publication/clawfree-packing-v0.1/README.md)（7 页）已完成技术验收，公开同步 PDF、TeX、复现包和准确验证范围；作者及单独预印本许可元数据仍待逐篇确认。查看[完整论文与复现索引](publication/README.md)，其中单列尚未集成的分支初稿。

## 已解决或证伪的公开数学问题

这里优先列出对**原命题全部假设与量词**给出的完整证明或严格反例，正面证明与证伪同等展示。随后单列重要特殊情形与新界，避免把局部进展写成一般猜想已解决。**独立研究 Agent 复核、Lean 检查、主分支集成与历史原创性是分别审查的状态**；下表不表示人类同行评议或首次解决。

### 已正式集成并完成 Lean 的原命题解答

以下七项的所列完整结论均已进入主分支，实际编译、公理审计及独立语义复核通过。证明源码、精确证书与审查记录还集中列于[证明与复现](#证明与复现)。

| 原始论文、命题与原陈述 | 我们的明确结论 | 严格证据与验证范围 |
| --- | --- | --- |
| **006：强积打包支配继承猜想**。Bujtás 等，arXiv:2510.02749v1，[§3 Conjecture 3.1](https://arxiv.org/html/2510.02749v1#S3)：若 $\gamma_d^p(G)=\infty$ ，则对任意 $H$ 也有 $\gamma_d^p(G\boxtimes H)=\infty$ | **完整反例**： $\gamma_2^3(Q_6)=\infty$ ，但 $\gamma_2^3(Q_6\boxtimes H)\le64$ 。所构造 $H$ 为 608 顶点、9,168 边的有限连通简单图 | [证明、证书与独立验证](006-strong-product-packing-counterexample/README.md) · [Lean](006-strong-product-packing-counterexample/proof/Q6PackingComplexCounterexample.lean) · [论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf) · [Zenodo DOI](https://doi.org/10.5281/zenodo.23293088) · [反例 Release](https://github.com/mio-qwq/math/releases/tag/006-strong-product-conjecture-counterexample-2026-10-09)。实际图／路径的完整存在性反例；辅助图边数、连通性另有书面与精确验证，64 未宣称最优 |
| **置换有向图一般位置数最优性猜想**。Chandran 等，arXiv:2604.15909v1，[§3.3 Theorem 3.6 后未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS3)： $\mathrm{gp}(\mathrm{Pe}(d,k))=2(d+k-2)_{k-1}$ ， $k\ge3,d\ge2k$ | **完整反例**：原始 $\mathrm{Pe}(6,3)$ 中有 90 点一般位置集，严格超过猜想值 84；全原参数的三终结字母构造另有书面推广 | [定理与证书](workstreams/ROOT/permutation-gp-counterexample/THEOREM.md) · [Lean](workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean) · [独立复核](workstreams/ROOT/permutation-gp-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/permutation-gp-counterexample-2026-10-10)。固定反例的全部最短有向简单路径、18 项审计通过；不是实际最大值等于 90 的证明 |
| **无爪次三次图的 $(1,1,3,3,4)$ 打包着色问题**。Mortada 等，arXiv:2608.02566v1，[§6 Problem 1](https://arxiv.org/html/2608.02566v1#S6)：除指定 12 顶点图外，是否所有**连通**无爪次三次图都可作此着色？ | **完整反例**：一个 36 顶点连通简单三正则无爪图无目标着色，且与指定例外不同构；奇数 $k\ge3$ 的 $12k$ 顶点反例族另有完整书面证明 | [构造与证明](workstreams/ROOT/clawfree-11334-counterexample/README.md) · [Lean](workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean) · [独立复核](workstreams/ROOT/clawfree-11334-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/clawfree-11334-counterexample-2026-10-10)。固定 36 点图全部条件与任意着色的不可能性，18 项审计通过；未声称最小反例或无限族全 Lean |
| **2-saturated 次三次图的 $(1,1,2)$ 打包着色猜想**。El Zein–Mortada，arXiv:2603.25113v1，[§5 Conjecture 3](https://arxiv.org/html/2603.25113v1#S5)：每个此类图均可作目标着色，原猜想无额外局部围长条件 | **完整反例**：将 $K_4$ 中同一顶点的三条关联边各细分一次，得到 7 顶点、9 边的连通 2-saturated 次三次图，但不存在目标着色 | [证明与证书](workstreams/ROOT/two-saturated-112-counterexample/README.md) · [Lean](workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean) · [独立复核](workstreams/ROOT/two-saturated-112-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/two-saturated-112-counterexample-2026-10-10)。所有三色函数的不可能性，14 项审计通过；不否定原文另一个带额外围长假设的定理 |
| **CDC 主特征值问题**。Collins–Sciriha，arXiv:1906.05790v1，[Question 5.8](https://arxiv.org/pdf/1906.05790)（期刊版 Question 16）：典范二重覆盖同构的两图，主特征值是否相同？ | **完整正面解答**：任意有限简单图满足 $M(\mathrm{CDC}(G))=M(G)$ ，因此二重覆盖同构推出主特征值集合相同 | [定理与来源](workstreams/ROOT/cdc-main-eigenvalues/THEOREM.md) · [Lean](workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean) · [编译与独立验收](workstreams/ROOT/cdc-main-eigenvalues/verification.json) · [Release](https://github.com/mio-qwq/math/releases/tag/cdc-main-eigenvalues-lean-2026-10-10)。7 项审计通过；允许孤立点、零特征值和不保层的覆盖同构，结论仅是主特征值集合。原作者 Theorem 3.3 已蕴含这一答案，新增自足证明与形式化不作为新数学首创宣传 |
| **循环图（circulant）的 monophonic position 存在性猜想**。Tuite–Thomas–Chandran，[*On some extremal position problems for graphs*，AMC 25 (2025), #P1.09，Conjecture 4.5](https://oro.open.ac.uk/92086/13/92086final.pdf) | 每个 $n\ge11$ 是否都存在直径 2、monophonic position 数为 2 的简单无向循环图（circulant）？**完整反例： $n=15$ 不存在这样的图**。全部 128 个对称连接集经结构分类排除，反驳原全称存在性，而非仅展示一个失败图 | [完整排除与来源](workstreams/ROOT/monophonic-circulant15-counterexample/README.md) · [实际诱导路径 Lean](workstreams/ROOT/monophonic-circulant15-counterexample/MonophonicCirculant15.lean) · [7 项审计](workstreams/ROOT/monophonic-circulant15-counterexample/lean-audit.json)。已集成并独立语义复核；全部连接集，不仅有限失败样本 |
| **笛卡尔积下 GP 数继承猜想**。Kruft Welton–Khudairi–Tuite，[2404.19451v1 Conjecture 2.10](https://arxiv.org/html/2404.19451v1)／期刊版 Conjecture 3： $\mathrm{gp}^-(G\square H)\ge\min\{\mathrm{gp}^-(G),\mathrm{gp}^-(H)\}$ | **完整反例**：11 点与 29 点因子下 GP 数都至少 6，319 点积图却有仅 5 点的极大 GP 集；尖锐正确替代界与无限差距族另有书面证明 | [定理及原定义](workstreams/ROOT/lower-gp-product319-counterexample/README.md) · [实际图 Lean](workstreams/ROOT/lower-gp-product319-counterexample/LowerGPProduct319.lean) · [15 项审计](workstreams/ROOT/lower-gp-product319-counterexample/lean-audit.json)。固定反例完整 Lean；全称修正界并非该 Lean 的结论 |

记 $(x)_j=x(x-1)\cdots(x-j+1)$ 。打包着色元组中的每一项代表一个**不同颜色**的距离半径，同色点距离须严格大于该半径。有向一般位置要求任意最短有向路径不含三个选点。下 GP 数是按包含关系极大的一般位置集的最小基数，其中“极大”不等于“最大”。

006 已以 **River Zhang、Yongxian Zhang** 双作者正式公开为 [Zenodo 数学预印本（v1.3，Version DOI：10.5281/zenodo.23293088）](https://doi.org/10.5281/zenodo.23293088)； [Concept DOI](https://doi.org/10.5281/zenodo.23293087) 关联后续版本。对应 [论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf)、[LaTeX 源码](006-strong-product-packing-counterexample/paper/main.tex)、[复现材料](publication/006-v1.3/README.md)及[论文验证记录](006-strong-product-packing-counterexample/paper/README.md)均可核验。该成果是**公开预印本，尚未经过期刊同行评审**；[旧版论文 Release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09)保留为历史材料，不与本次 Zenodo 发表混同。

### 已正式集成并获独立书面复核的原命题解答

这些完整书面证明已按独立验收的精确范围集成到主分支，**尚无完整 Lean 认证**。原冻结稿和源哈希保留，经典工具及原作者已证部分明确归属。验证记录区分旧作者自测、本轮有限复现和全称书面论证；未验收的邻近候选不随之升级。完整清单与限定见[成果目录](RESEARCH_RESULTS.md)。

| 原始论文与准确命题 | 原命题与已核验结论 | 冻结证明与贡献边界 |
| --- | --- | --- |
| **Gorzkowska–Kwaśny Conjecture 10**，[*Distinguishing adjacent vertices by ordering edges*](https://arxiv.org/html/2609.11832v1#S5) | 每个非 $K_2$ 、非偶圈的有限连通简单图，任意固定正常边着色均可用一个全局边序区分相邻顶点的关联颜色序列。**完整构造性正面证明**：补足全部 $d\ge3$ 正常 $d$ 边着色的 $d$ 正则情形，再结合原作者已证部分 | [主分支完整证明与严格证书](workstreams/ROOT/edge-order-distinguishing/README.md)。原文 Theorem 5 和经典 de Werra 辅助结果明确归属；程序导入问题已修复，有限独立复现通过。大枚举保留为作者历史执行，未称本轮重跑 |
| **Braun–Bruegge Conjecture 31**，[*Facets of Symmetric Edge Polytopes for Graphs with Few Edges*，JIS 26 (2023), Article 23.7.2](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf)；arXiv v4 为 Conjecture 5.1 | 原文二项式有限和 $F$ 在合法同奇偶、保序参数上的两项转移不等式： $F(a,b,c)\le F(a+2,b,c-2)$ 与 $F(a,b,c)\le F(a+2,b-2,c)$ 。**原标量陈述完整证明**；并得固定和 $n+1$ 下偶 $n\ge4$ 的极值 $(n-1,1,1)$ 、奇 $n\ge5$ 的极值 $(n-3,2,2)$ | [主分支原标量、同奇偶推广及跨奇偶附节](workstreams/ROOT/braun-bruegge-f31/README.md)。不推出更广简单图／多面体极值猜想；跨奇偶部分已有独立代数复核，无完整 Lean |
| **连续生成元循环有向图最优性猜想**。Chandran 等，[*The general position number of digraphs*，§3.1 Theorem 3.3 后的未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS1) | 对 $\mathrm{Circ}(n,\{1,\ldots,d\})$ ，原文两种构造中较大的是否总是最优？**全部 $1\le d<n$ 的完整正面证明**，精确值见下式；包括端点与全部余数 | [完整证明与来源](workstreams/ROOT/distributed-written-proofs/B/circulant/README.md)。全参数书面复核；旧余数标量 Lean 不能代替实际图精确值形式化 |
| **El Zein–Mortada Conjecture 6**，[*Impact of local girth on the S-packing coloring of k-saturated subcubic graphs*，§5](https://arxiv.org/html/2603.25113v1#S5) | 每个三度点都属于三角形的有限简单 $(3,0)$ -saturated 次三次图，是否有 $(1,1,2)$ 打包着色？**原全范围正面证明** | [完整证明与条件对应](workstreams/ROOT/distributed-written-proofs/B/heavy_triangle_112/README.md)。与已反驳的 Conjecture 3 不同；无完整 Lean |
| **El Zein–Mortada Conjecture 2**，同论文 [§5](https://arxiv.org/html/2603.25113v1#S5) | 每个三度点都属于三角形的有限简单 1-saturated 次三次图，是否有标准五色打包着色，即半径 $(1,2,3,4,5)$ ？**原全范围正面证明**，覆盖菱形、一般路径连接及链／环结构 | [五色完整结构证明与证书](workstreams/ROOT/distributed-written-proofs/B/triangle_packing/README.md)。有限状态不变量和无限归纳已独立重建；其他 palette 未随之验收 |
| **Mizzi 修订版第一条猜想**，[*Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*，arXiv:2603.27559v3 §7 未编号两项猜想的第一项](https://arxiv.org/html/2603.27559v3#S7) | 原文默认有限连通、非二分、无开孪生的非同构 TF-cousins 图对：一图是否含两条顶点不交的奇长 $C_k$ ，另一图含 $C_{2k}$ ？**完整图对全称证明**，覆盖原文默认范围 | [完整图对证明](workstreams/ROOT/distributed-written-proofs/C/mizzi/README.md)。普通简单圈，不要求诱导；已有 TF/cousin 理论明确归属，无完整 Lean |
| **Mizzi 修订版第二条猜想**，同论文 [v3 §7](https://arxiv.org/html/2603.27559v3#S7) | 原文连通范围内，有限非对称不稳定图是否同时含 $C_k$ 与 $C_{2k}$ （奇数 $k\ge3$ ）？**完整正面证明，并可取两圈顶点不交**；不同轨道长度与固定点均纳入 | [完整非对称定理与范围修正](workstreams/ROOT/distributed-written-proofs/C/mizzi/README.md)。原连通范围保留；更一般入口显式要求非平凡 TF 对，不外推任意非连通 CDC 不稳定性。已比较 [2608.15281](https://arxiv.org/abs/2608.15281) 的旧版反例 |
| **无爪次三次图的 $(1,2,2,2,2)$ 猜想**。Mortada 等，[*On (1,1,2,3)- and (1,1,3,3,3)-Packing Colorings of Claw-Free Subcubic Graphs*，§6 Conjecture 1](https://arxiv.org/html/2608.02566v1#S6) | 每个有限无爪次三次图均可作此着色。**原全范围正面推论证明**，包括三角形、菱形及任意路径连接 | [完整推论及经典归属](workstreams/ROOT/distributed-written-proofs/B/clawfree_12222/README.md)。使用已有 Yang–Wu 边权着色定理；不宣称新一般边着色定理或首次解决 |
| **El Zein–Mortada Conjecture 1**，同论文 [§5](https://arxiv.org/html/2603.25113v1#S5) | 0-saturated 次三次图中，每个三度点局部围长至多 4，则标准打包色数至多 4。**原全范围正面证明**，含任意连接长度与非连通分量 | [完整证明](workstreams/ROOT/distributed-written-proofs/B/packing_extension/README.md)。不与五色及 $(1,1,2)$ 的另两条原猜想混同，无完整 Lean |
| **顶点位置数比率有界性**。Thankachy 等，[DMGT 44 (2024), Problem 4](https://doi.org/10.7151/dmgt.2491)／[2209.00359v2 Problem 2.4](https://arxiv.org/abs/2209.00359) | **完整负答案**：连通图的 $\mathrm{vp}/\mathrm{vp}^-$ 无界；二部、最大度至多 3 子类仍无界 | [两个全参数族及独立验收范围](workstreams/ROOT/distributed-written-proofs/B/vertex_position_ratio/README.md)。同题负答案与强化；顶点位置参数不是下 GP 参数，无完整 Lean |
| **Bychawski Conjecture 6.5**，[2406.06267v1 §6](https://arxiv.org/html/2406.06267v1) | **完整正面证明**：每个固定 $\varepsilon>0$ ，均匀随机标号图 $G\sim G(n,1/2)$ 在 $n(1-\varepsilon)/2$ 次边编辑内获得非平凡 TF 投射的概率趋零；另得更严格的连通、非二分、无开孪生目标类的距离 $D_n/n\to1/2$ （依概率） | [自足证明与实际有限回归](workstreams/ROOT/tf-edit-distance/README.md)。下界对所有非恒等 TF 对；上界用普通自同构。已修正原稿引言的目标类蕴含方向；经典对称性阈值归属保留，无完整 Lean |
| **非平凡不稳定图计数 Problem 5.3**。Hujdurović–Mitrović，[2210.15249v1](https://arxiv.org/html/2210.15249v1#S5) | **完整渐近主项**：令 $U_n$ 为连通、非二分、无孪生的不稳定图的非同构计数，则 $U_n\sim2^{\binom{n-4}{2}+2(n-4)-1}/(n-4)!$ ；典型原图自同构群 $C_2$ ，覆盖群为阶 8 的 $D_8$ | [完整计数、正规形及群结构](workstreams/ROOT/distributed-written-proofs/C/tf-count/README.md)。原作者四点添加构造明确归属；更强误差／有效阈值未随之验收，无完整 Lean |

循环有向图的精确式采用原文的余数约定 $n=qd+r$ ， $q\ge0$ 、 $2\le r\le d+1$ ：

$$
\mathrm{gp}(\mathrm{Circ}(n,\{1,\ldots,d\}))=
\begin{cases}
d+1,&r=d+1,\\
\max\{r,\lfloor d/r\rfloor+1\},&2\le r\le d.
\end{cases}
$$

这是连续生成元图的完整结果，不是其他生成集的结论。上述未编号猜想、§3.3 的置换图猜想和下方 Kautz 特殊情形是不同问题；同一问题的证明、程序、推广和形式化不重复计为多个原问题解答。

### 重要特殊情形与部分定理

| 原公开问题 | 已严格核验的推进 | 状态与材料 |
| --- | --- | --- |
| **任意图的有向一般位置谱区间猜想**。Chandran 等，[Conjecture 4.30](https://arxiv.org/html/2604.15909v1#S4.SS2)：任意图在全部边定向下的 GP 数谱是否为整数区间？ | **全部有限树情形完整证明**，覆盖原文树族之外的全部有限树；森林推论另有书面分量和证明。任意图原猜想仍未由此解决 | **已集成、完整树情形 Lean、独立复核通过**：[定理](workstreams/ROOT/gp-tree-spectrum/README.md) · [Lean](workstreams/ROOT/gp-tree-spectrum/TreeGPSpectrum.lean) · [复核](workstreams/ROOT/gp-tree-spectrum/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/tree-gp-spectrum-lean-2026-10-10)。真实树、全部定向与最大集基数，44 项审计 |
| **Kautz 图精确一般位置数**。Chandran 等，[Problem 5.2](https://arxiv.org/html/2604.15909v1#S5)：求树、置换图及词长 $k\ge3$ 的 Kautz 图的一般公式 | **词长三全部参数 $m\ge3$ 的精确公式**： $\mathrm{gp}(\mathrm{Ka}(m,3))=m(m-1)(2m-1)/6$ ，其中 $m$ 为字母表大小，允许首尾字母相同。一般词长原问题未解决 | **已集成、全参数词长三 Lean、独立复核通过**：[完整专题](workstreams/ROOT/kautz3-exact-gp/README.md) · [真实路径 Lean](workstreams/ROOT/kautz3-exact-gp/Kautz3ExactGP.lean) · [24 项审计](workstreams/ROOT/kautz3-exact-gp/lean-audit.json)。原作者表格已有有限数值观察，不宣传数值猜想首次发现 |
| **同一 Problem 5.2 的词长四推进** | **极限存在与新界**： $\lambda_4=\lim_{m\to\infty}\mathrm{gp}(\mathrm{Ka}(m,4))/m^4$ 存在， $26/125\le\lambda_4\le377/1320<2/7$ 。取整后的有限上界适用 $m\ge11$ ；未确定精确有限值或极限值 | **已集成、独立书面复核、无完整 Lean**：[完整上下界、极限与取整修正](workstreams/ROOT/distributed-written-proofs/B/kautz_length4/README.md)。实际图距离和有限状态桥已验收，历史原创性未确认 |

<details>
<summary>原始论文索引与版本辨认</summary>

- Bujtás、Iršič Chenoweth、Klavžar、Zhang：[On d-distance p-packing domination number in strong products](https://arxiv.org/abs/2510.02749)，本页对应 v1 Conjecture 3.1。
- Chandran 等：[The general position number of digraphs](https://arxiv.org/abs/2604.15909)，本页对应 v1：§3.1／§3.3 两条未编号猜想、Conjecture 4.30 与 Problem 5.2。
- El Zein、Mortada：[Impact of local girth on the S-packing coloring of k-saturated subcubic graphs](https://arxiv.org/abs/2603.25113)，本页区分 v1 Conjectures 1、2、3、6。
- Mortada、El Zein、Al Hajjar：[On (1,1,2,3)- and (1,1,3,3,3)-Packing Colorings of Claw-Free Subcubic Graphs](https://arxiv.org/abs/2608.02566)，本页区分 v1 §6 Problem 1 与 Conjecture 1。
- Collins、Sciriha：[On the Walks and Bipartite Double Coverings of Graphs with the same Main Eigenspace](https://arxiv.org/abs/1906.05790)：预印本 Question 5.8 对应[期刊版 Question 16](https://doi.org/10.7151/dmgt.2386)。
- Braun、Bruegge：[Facets of Symmetric Edge Polytopes for Graphs with Few Edges](https://arxiv.org/abs/2201.13303)：JIS 26 (2023), Article 23.7.2 的 Conjecture 31，在 arXiv v4 编号为 Conjecture 5.1；仅所列标量陈述已书面证明。
- Gorzkowska、Kwaśny：[Distinguishing adjacent vertices by ordering edges](https://arxiv.org/abs/2609.11832)，本页对应 v1 Conjecture 10。
- Mizzi：[Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins](https://arxiv.org/abs/2603.27559)，本页使用 2026-09-10 的 v3 §7 两条未编号猜想，保留连通性／非平凡 TF 对等适用条件。

</details>

## 完整研究目录

编号 001–006 保留原有项目归属；近期独立选题的成果另放在 `workstreams/ROOT/`，不重新编号或混入早期项目。各入口同时提供证明、文献及形式化记录。

| 项目 | 主要数学成果 | 证明层级与尚未覆盖的范围 |
| --- | --- | --- |
| [**001：逐项幂 Hadamard 刚性与解空间分类**](001-odd-half-order-hadamard/README.md) | 在 $2m$ 阶矩阵的逐项幂 $1,\ldots,m-1$ 均为 Hadamard 的假设下，对奇数 $m\ge3$ 证明根刚性；对全部 $m\ge2$ 给出根种子与单相位构造的穷尽分类、带标号去相位解空间及标准矩阵等价商的有限图描述 | 完整结构分类与拓扑描述为书面证明；支持集、实际复数分块、多项式及行比乘积障碍有 Lean。不是全部复 Hadamard 矩阵的无条件分类，也不宣称新偶数阶种子存在；与既有 switching 理论的原创性关系仍需审查 |
| [**002：加权矩形剪枝与独立成对成本**](002-weighted-rectangular-pruning/README.md) | 任意有限关系的乘积权重剪枝界；在局部兼容不等式下，任一关系为弦二部图时独立非负成对成本的尖锐系数一；平移不变六圈的实际覆盖界、精确书面最优值及两正乘积之和的统一常数障碍 | 一般结构推广为完整书面构造，覆盖零成本与部分输入；六圈全输入覆盖、剪枝和尖锐性等有 Lean。任意关系的全部独立成本情形未解决；九式最优值及不变部分输入尚非完整 Lean |
| [**003：20 维代数、投射分解与 Yoneda／Tate 结构**](003-arc-one-parameter/README.md) | 特征二下的实际代数、核心对偶平凡扩张与根基；指定模块全次数投射分解、实际 $\mathrm{Ext}^3$ 类及 $\mathrm{Ext}^6$ 中 Yoneda 平方；有限共振模块的构造与全整数次数 Tate 乘法；下层代数实际 self-Ext 和 regular-target Ext 计算 | 代数与若干实际同调对象已 Lean 化；次数三类与其平方的非零结论分别保留 $q^3\ne0$ 与 $q^4\ne0$ 等原假设。有限共振及完整 Tate 结构主要为书面证明；高次幂、完整 20 维 self-Ext 谱及完整 ARC 实现未完成。下层既有数学结论按 [来源比较](003-arc-one-parameter/ATTRIBUTION.md)归属 |
| [**004：六维 MUB 三元组的伴随兼容性**](004-mub-triplets/README.md) | 完整伴随基的谱矩判据、固定配对支持和酉相位分类；四循环分支消去；实际归一化 MUB 三元组在指定分区的两三阶特征标分别为 $0$ 与 $(243-351i)/125$ | 谱权重、实际矩阵支持／酉条件及该三元组已有 Lean。例子否定更强的“两特征标各自为零”路线，未否定原乘积为零猜想；一般伴随选择及六维最大 MUB 数问题未解决 |
| [**005：有向圈打包的反馈集障碍**](005-directed-cycle-packing/README.md) | 对最小出度为正的非空有限弧支配定向图，证明反馈集大小严格超过最小出度；另有七点反馈集对指定打包目标的书面推论 | 指定假设下的全称反馈集障碍有 Lean；从反馈集到一般打包的桥不属于该端点。不是 Bermond–Thomassen $k=4$ 原猜想的完整证明或反例 |
| [**006：强积打包支配猜想反例与论文**](006-strong-product-packing-counterexample/README.md) | 见上方完整原命题反例；同时提供辅助图、64 中心集合、独立精确重放和英文论文 | 存在性层面的完整 Lean 反例已发布；最优中心数、最小辅助图及完整分类不在本结论中 |
| [**ROOT：一般位置、打包着色与图谱独立成果**](workstreams/ROOT/) | 上方置换图反例、两项打包着色反例、主特征值正面解答及全树谱定理 | 各专题各自验收并发布；不将多个特殊情形拼成未证明的更广命题 |
| [**专项笔记与方法边界**](notes/) | $Q_6$ 积图、 $C_7$ 码率、指定 $D_5$ 补点、局部三角形交换及七核替换族 | 下方逐项区分图族障碍、有限反例、书面证明和 Lean 实际端点 |

<details>
<summary>展开：001–004 的主要技术与延伸材料</summary>

- **001**：[全半阶根／相位分类](001-odd-half-order-hadamard/general-patterns.md)、[带标号有限解图](001-odd-half-order-hadamard/phase-geometry.md)、[标准矩阵等价商](001-odd-half-order-hadamard/equivalence-quotient.md)。
- **002**：[兼容成对成本](002-weighted-rectangular-pruning/compatible-pair-costs.md)、[两类反身成本](002-weighted-rectangular-pruning/reflexive-cost-families.md)、[双路径独立成本](002-weighted-rectangular-pruning/double-path-independent-costs.md)、[单侧块／路径展开](002-weighted-rectangular-pruning/binary-one-side-costs.md)、[嵌套关系](002-weighted-rectangular-pruning/nested-relation-costs.md)、[右叶扩张](002-weighted-rectangular-pruning/right-leaf-extension-costs.md)、[森林与悬挂星](002-weighted-rectangular-pruning/forest-pendant-star-costs.md)、[弦二部图](002-weighted-rectangular-pruning/chordal-bipartite-costs.md)、[六圈成本](002-weighted-rectangular-pruning/cyclic-six-costs.md)。这些是逐步覆盖更广结构的定理，不是九个独立解决的公开猜想。
- **003 的构造与乘法**：[共振 Yoneda 代数](003-arc-one-parameter/resonant-yoneda-algebra.md)、[有限共振实际实现](003-arc-one-parameter/finite-resonant-realization.md)、[有限阶 Tate 代数](003-arc-one-parameter/finite-resonant-tate-algebra.md)、[阶一接口与乘法](003-arc-one-parameter/order-one-tate-algebra.md)。
- **003 的实际代数与同调**：[标量端同态及分裂](003-arc-one-parameter/proof/mathlib/TwentyDimDualScaleEndomorphism.README.md)、[核心对偶平凡扩张](003-arc-one-parameter/proof/mathlib/TwentyDimTrivialExtension.README.md)、[结构比较与根基](003-arc-one-parameter/structural-bridge-replay.md)、[下层全次数投射分解](003-arc-one-parameter/proof/mathlib/LowerAlgebraCategoricalResolution.README.md)、[regular-target Ext](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularExt.README.md)、[实际右作用](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularRightAction.README.md)。下层 self-Ext 消失要求所有正整数 $m$ 的 $1+q^m\ne0$ ；regular-target 一维次数二计算另要求 $q\ne0$ 。
- **004**：[循环特征标](004-mub-triplets/direct-circulant-character.md)、[实际平坦 Gram 消去](004-mub-triplets/flat-gram-cancellation.md)、[归一化三元组的不对称特征标](004-mub-triplets/fourier-character-asymmetry.md)。一般条件性桥接与经典 Zauner 构造分别注明来源。

</details>

## 分布式成果及待验收范围

A／B／C 已验收成果现有主分支数学入口，详见首页前表及[完整成果目录](RESEARCH_RESULTS.md)。不覆盖协作者分支，不改写原冻结历史；程序、数学正文和当前验收范围分别保存来源哈希。

- **下 GP 的尖锐正确替代界**：[完整书面证明与精确证书](workstreams/ROOT/distributed-written-proofs/B/lower_gp_product/README.md)给出任意非空有限简单无向图的界 $\mathrm{gp}^-(G\square H)\ge\min\{5,\mathrm{gp}^-(G),\mathrm{gp}^-(H)\}$ ，且每个 $r\ge6$ 有因子参数至少 $r$ 、积图参数恰 5 的连通族。与上方已 Lean 的固定反例是同题反驳及正确修正，不重复计数；全称修正界／无限族尚无完整 Lean。
- **密码结构书面成果**：[circulant RD 与周期商 MDS 继承、Ascon 两轮／三列固定路径精确概率](workstreams/ROOT/cryptographic-structures/README.md)已经独立复核并集成。其中 circulant 定理对特征二域上全阶 $n\ge3$ 的可逆矩阵建立非平凡 RD 对。ChaCha 仅为局部模型技术基线；RSA 高次结构仍待验收，新增窄整数 Lean 与经典 continued-fraction 范围审计；SHA-256 新增实际消息扩展异字数 ≥13 的候选，固定证书复算通过但尚待全链验收；Keccak 尚无本项目新结果。详细范围见[成果目录](RESEARCH_RESULTS.md#密码结构研究限定数学范围)。没有完整密码攻击或完整算法 Lean，历史原创性未确认。
- **未验收候选**：CG 奇参数的完整 cousin 分类、Bychawski Conjecture 6.6 精细期望／有效常数、不稳定图更强误差、指定下 GP 家族及其他 packing palettes 均保持各自范围；不会因相邻成果通过而自动验收。C66 已发现既有公开证明声称，须比较和独立复验；[候选与冻结入口](RESEARCH_RESULTS.md#未验收候选与方法障碍)列明具体边界。

这些差别用于准确描述科学证据；书面成果的集成不表示完成全文 Lean、确认首创或获得期刊同行评审。

## 证明与复现

每项主要成果从专题入口可到达数学证明、原始文献及复核范围；具备 Lean 的成果另提供源码、编译日志和公理审计。近期 ROOT 形式化成果的关键证据如下；审计数指实际检查的声明数，不是数学贡献数量。

| 成果 | Lean 源码 | 实际运行与独立复核 |
| --- | --- | --- |
| 006 强积反例 | [几何与路径](006-strong-product-packing-counterexample/proof/Q6PackingComplexGeometry.lean)、[原始反例端点](006-strong-product-packing-counterexample/proof/Q6PackingComplexCounterexample.lean) | [源文件验证记录](006-strong-product-packing-counterexample/results/lean-verification.json)：新增两源 12／26 项审计，独立重建含单因子共 12+12+26 项；精确图验证见专题 |
| 排列图 90 点反例 | [PermutationGP90.lean](workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean) | [编译与 18 项审计](workstreams/ROOT/permutation-gp-counterexample/verification.json)、[独立复核](workstreams/ROOT/permutation-gp-counterexample/INDEPENDENT_REVIEW.md) |
| 无爪 36 点反例 | [ClawFree11334.lean](workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean) | [编译与 18 项审计](workstreams/ROOT/clawfree-11334-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/clawfree-11334-counterexample/INDEPENDENT_REVIEW.md) |
| 2-saturated 7 点反例 | [TwoSaturated112.lean](workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean) | [编译与 14 项审计](workstreams/ROOT/two-saturated-112-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/two-saturated-112-counterexample/INDEPENDENT_REVIEW.md) |
| CDC 主特征值 | [CDCMainEigenvalues.lean](workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean) | [编译、7 项审计及独立验收](workstreams/ROOT/cdc-main-eigenvalues/verification.json) |
| 全有限树 GP 谱 | [TreeGPSpectrum.lean](workstreams/ROOT/gp-tree-spectrum/TreeGPSpectrum.lean) | [编译与 44 项审计](workstreams/ROOT/gp-tree-spectrum/lean-audit.json)、[独立复核](workstreams/ROOT/gp-tree-spectrum/INDEPENDENT_REVIEW.md) |
| Kautz 词长三全参数 | [Kautz3ExactGP.lean](workstreams/ROOT/kautz3-exact-gp/Kautz3ExactGP.lean) | [24 项审计](workstreams/ROOT/kautz3-exact-gp/lean-audit.json)、[独立语义复核](workstreams/ROOT/kautz3-exact-gp/INDEPENDENT_REVIEW.md) |
| 15 阶 monophonic 排除 | [MonophonicCirculant15.lean](workstreams/ROOT/monophonic-circulant15-counterexample/MonophonicCirculant15.lean) | [7 项审计](workstreams/ROOT/monophonic-circulant15-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/monophonic-circulant15-counterexample/INDEPENDENT_REVIEW.md) |
| 319 点下 GP 积反例 | [LowerGPProduct319.lean](workstreams/ROOT/lower-gp-product319-counterexample/LowerGPProduct319.lean) | [15 项审计](workstreams/ROOT/lower-gp-product319-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/lower-gp-product319-counterexample/INDEPENDENT_REVIEW.md) |

上述成功编译记录均保留实际源码哈希和运行证据，退出码为零，无错误或警告；审计依赖仅为 `propext`、`Classical.choice`、`Quot.sound` 的子集，无 `sorryAx` 或新增公理。Lean 检查的是所写声明，其与原论文定义、量词和对象的对应关系还须通过语义审查。

Mathlib 项目固定使用 **Lean 4.34.1** 与 **Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`**。从仓库根目录进入现有固定环境，可重放无需额外本地模块构建的 ROOT 单文件，例如：

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean
```

多模块项目、006 及使用本地导入的源码，应按各专题说明先构建相应依赖；不要以单文件示例代替这些构建步骤。Python 检查器的调用、依赖、精确证书及损坏输入控制也分别记录在专题中，部分重放会写入新时间戳，复现前应保留原始收据。

更细的既有源码索引见 [FORMALIZATION.md](FORMALIZATION.md)，问题分类见 [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md)。这些记录各有自己的日期和覆盖范围；近期独立成果的最新端点应直接查上表的源文件记录。

重要里程碑另有 [GitHub Releases](https://github.com/mio-qwq/math/releases)，以精确提交、签名标签、源码 ZIP、manifest 和 SHA256SUMS 固定发布材料。上方列出的 Release 已核对为不可变发布。签名、公开时间和文件摘要证明版本与材料的可核查性，**不自动证明数学首创性**。

## 未完成问题与方法边界

词长三 Kautz 精确公式、15 阶 monophonic 排除和固定 319 点下 GP 积反例均已完成实际 Lean 并集成；词长四精确值、一般图 GP 谱及公开 packing 问题剩余范围仍未由此解决。新集成完整书面成果的实际图、路径、概率极限等全文 Lean 桥也未完成。源论文、既有解答、历史新颖性和验收状态继续分别记录；不能将未充分确认的开放状态直接当作仍未解的事实。

早期方向的具体缺口包括 002 任意关系独立成本、003 尚未完成的同调桥与更高乘法、004 一般伴随耦合及六维 MUB、005 一般有向圈打包。这些缺口不是本仓库已经解决的原猜想。成熟成果的论文整理与研究价值审查可以继续，但不以定理或提交数量决定研究投入。

下列已发布笔记记录了有数学内容的特殊情形、失败机制与构造族界限，避免将局部认识误列为原问题解答：

| 专项成果 | 实际结论 | 边界与材料 |
| --- | --- | --- |
| **$Q_6\boxtimes Q_6$ 的中心构造障碍** | 排除全部二元仿射中心集；六点投影完整分类进一步排除十二中心，尚余非线性 13–21 中心范围 | [仿射障碍](notes/q6-strong-product-affine-obstruction.md)、[六点分类](notes/q6-six-point-midpoint-classification.md)。积图排除主要为书面证明；相关单因子／邻域端点有 Lean。006 用不同辅助因子反驳了原一般继承猜想，不等于解决这个固定积图 |
| **$C_7$ 既有格点参数族的直接映射障碍** | 对该明确构造族的全部可直接映射参数，证书码率至多 $\sqrt{10}$ ；算术与整数商已有 Lean | [完整笔记](notes/c7-fraction-family-barrier.md)。不是 $C_7$ Shannon 容量上界，也未提高已知下界；图构造／映射桥另有书面范围 |
| **指定 $D_5$ 三根删除后的连续补点界** | 保留其余 37 根，在任意实坐标候选中至多补三点；达到三点时只能补回原删根 | [连续分类与验证](notes/d5-three-root-cap.md)。Lean 已检查实际约束与分类，仅限所指定三根；不是所有删除模式，更不是五维接吻数的完整解答 |
| **局部三角形交换规则的有限反例** | 七顶点图满足所述局部打包／支撑条件，交换仍可破坏与保留边的兼容性；实际有限图反例已 Lean 化 | [规则、例子与范围](notes/triangle-swap-safety.md)。针对特定版本的辅助交换规则，不是 Tuza 原猜想反例，也不自动否定整套算法 |
| **七核短圈替换族的尖锐障碍** | 指定无有向三圈、无 $T_9$ 的正簇吹胀族，最小出度比最大为 $260889/805108<1/3$ | [分类、界与等号构造](notes/seven-core-short-cycle-substitution.md)。整族图论论证为书面；Lean 检查代数界、等号见证及严格间隙，不是一般短圈猜想解答 |

[公开问题候选审查](OPEN_PROBLEM_CANDIDATES.md)还保存七圈容量、五维接吻数及 SIC 等问题的阶段性文献核查。列入候选记录不等于当前仍已确认开放或正在重投入；没有检索到解答也不构成开放性证明。

## 学术声明

- **来源与贡献。** 本项目从原始论文和自己的推导开展研究，也使用公开通用理论。早期部分工作参考 [OpenAI/math](https://github.com/openai/math) 的公开证明，固定上游版本及借用内容见各专题。数学原结论、新证明、新推广及新增形式化分别归属；尤其 003 的 OpenAI／Tang 重合范围见 [ATTRIBUTION.md](003-arc-one-parameter/ATTRIBUTION.md)。
- **正确性与学术状态。** 精确计算、有限证书、全称书面证明和 Lean 端点不互相替代。没有把数值优化当作严格反例，未把工作分支候选当作正式验收结果，也未宣称本仓库材料已获人类同行评审、期刊接受或历史首次。文献审查仍可能遗漏未索引或隐含的既有结果。
- **AI 贡献。** AI 系统实际参与选题与文献分析、数学推导、反例构造、程序验证、Lean 形式化、独立研究 Agent 复核及论文写作。独立 Agent 复核的独立性指未参与相应发现与证明草拟，不等于外部人类审稿。不得将 AI Agent 或模型列为论文作者；人工署名与责任由实际贡献者最终确认，正式提交须按目标平台政策如实披露。
- **使用与引用。** 仓库使用 [Apache-2.0 许可证](LICENSE)；所引外部论文及理论仍按其来源引用。新稿件单独预印本归档的许可元数据须按论文另行确认，详见论文索引。引用本仓库成果时宜同时给出原命题来源、专题材料和精确提交或 Release，并注明书面／形式化范围及历史原创性的不确定性。
