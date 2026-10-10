# 数学研究：证明、反例与 Lean 形式化

本仓库研究公开数学问题，收录严格反例、完整证明、结构分类及可复现的计算与形式化材料。研究覆盖图论、组合数学、矩阵结构和同调代数；核心目标是对原始问题给出准确、可独立核验的数学答案。

这里分别记录**数学结论、形式化覆盖范围、独立复核和发布状态**。书面证明与 Lean 证明具有不同的验证范围；分支上的成果也不会因作者自行标记通过而自动成为主分支正式成果。本页按 **2026-10-10** 的实际源码、验证记录和远端分支整理，详细假设、文献关系及后续更新以各专题材料为准。

[已解决或证伪的公开数学问题](#已解决或证伪的公开数学问题) · [完整研究目录](#完整研究目录) · [分布式分支成果](#分布式分支成果) · [证明与复现](#证明与复现) · [在研问题与方法边界](#在研问题与方法边界) · [学术声明](#学术声明)

## 已解决或证伪的公开数学问题

这里优先列出对**原命题全部假设与量词**给出的完整证明或严格反例，正面证明与证伪同等展示。随后单列重要特殊情形与新界，避免把局部进展写成一般猜想已解决。**独立研究 Agent 复核、Lean 检查、主分支集成与历史原创性是分别审查的状态**；下表不表示人类同行评议或首次解决。

### 已正式集成并完成 Lean 的原命题解答

以下五项的所列完整结论均已进入主分支，实际编译、公理审计及独立语义复核通过。证明源码、精确证书与审查记录还集中列于[证明与复现](#证明与复现)。

| 原始论文、命题与原陈述 | 我们的明确结论 | 严格证据与验证范围 |
| --- | --- | --- |
| **006：强积打包支配继承猜想**。Bujtás 等，arXiv:2510.02749v1，[§3 Conjecture 3.1](https://arxiv.org/html/2510.02749v1#S3)：若 $\gamma_d^p(G)=\infty$，则对任意 $H$ 也有 $\gamma_d^p(G\boxtimes H)=\infty$ | **完整反例**：$\gamma_2^3(Q_6)=\infty$，但 $\gamma_2^3(Q_6\boxtimes H)\le64$。所构造 $H$ 为 608 顶点、9,168 边的有限连通简单图 | [证明、证书与独立验证](006-strong-product-packing-counterexample/README.md) · [Lean](006-strong-product-packing-counterexample/proof/Q6PackingComplexCounterexample.lean) · [论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf) · [反例 Release](https://github.com/mio-qwq/math/releases/tag/006-strong-product-conjecture-counterexample-2026-10-09)。实际图／路径的完整存在性反例；辅助图边数、连通性另有书面与精确验证，64 未宣称最优 |
| **置换有向图一般位置数最优性猜想**。Chandran 等，arXiv:2604.15909v1，[§3.3 Theorem 3.6 后未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS3)：$\operatorname{gp}(\mathrm{Pe}(d,k))=2(d+k-2)_{k-1}$，$k\ge3,d\ge2k$ | **完整反例**：原始 $\mathrm{Pe}(6,3)$ 中有 90 点一般位置集，严格超过猜想值 84；全原参数的三终结字母构造另有书面推广 | [定理与证书](workstreams/ROOT/permutation-gp-counterexample/THEOREM.md) · [Lean](workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean) · [独立复核](workstreams/ROOT/permutation-gp-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/permutation-gp-counterexample-2026-10-10)。固定反例的全部最短有向简单路径、18 项审计通过；不是实际最大值等于 90 的证明 |
| **无爪次三次图的 $(1,1,3,3,4)$ 打包着色问题**。Mortada 等，arXiv:2608.02566v1，[§6 Problem 1](https://arxiv.org/html/2608.02566v1#S6)：除指定 12 顶点图外，是否所有无爪次三次图都可作此着色？ | **完整反例**：一个 36 顶点连通简单三正则无爪图无目标着色，且与指定例外不同构；奇数 $k\ge3$ 的 $12k$ 顶点反例族另有完整书面证明 | [构造与证明](workstreams/ROOT/clawfree-11334-counterexample/README.md) · [Lean](workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean) · [独立复核](workstreams/ROOT/clawfree-11334-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/clawfree-11334-counterexample-2026-10-10)。固定 36 点图全部条件与任意着色的不可能性，18 项审计通过；未声称最小反例或无限族全 Lean |
| **2-saturated 次三次图的 $(1,1,2)$ 打包着色猜想**。El Zein–Mortada，arXiv:2603.25113v1，[§5 Conjecture 3](https://arxiv.org/html/2603.25113v1#S5)：每个此类图均可作目标着色，原猜想无额外局部围长条件 | **完整反例**：将 $K_4$ 中同一顶点的三条关联边各细分一次，得到 7 顶点、9 边的连通 2-saturated 次三次图，但不存在目标着色 | [证明与证书](workstreams/ROOT/two-saturated-112-counterexample/README.md) · [Lean](workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean) · [独立复核](workstreams/ROOT/two-saturated-112-counterexample/INDEPENDENT_REVIEW.md) · [Release](https://github.com/mio-qwq/math/releases/tag/two-saturated-112-counterexample-2026-10-10)。所有三色函数的不可能性，14 项审计通过；不否定原文另一个带额外围长假设的定理 |
| **CDC 主特征值问题**。Collins–Sciriha，arXiv:1906.05790v1，[Question 5.8](https://arxiv.org/pdf/1906.05790)（期刊版 Question 16）：典范二重覆盖同构的两图，主特征值是否相同？ | **完整正面解答**：任意有限简单图满足 $M(\operatorname{CDC}(G))=M(G)$，因此二重覆盖同构推出主特征值集合相同 | [定理与来源](workstreams/ROOT/cdc-main-eigenvalues/THEOREM.md) · [Lean](workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean) · [编译与独立验收](workstreams/ROOT/cdc-main-eigenvalues/verification.json) · [Release](https://github.com/mio-qwq/math/releases/tag/cdc-main-eigenvalues-lean-2026-10-10)。7 项审计通过；允许孤立点、零特征值和不保层的覆盖同构，结论仅是主特征值集合 |

记 $(x)_j=x(x-1)\cdots(x-j+1)$。打包着色元组中的每一项代表一个**不同颜色**的距离半径，同色点距离须严格大于该半径。有向一般位置要求任意最短有向路径不含三个选点。

006 的[英文研究稿 PDF](006-strong-product-packing-counterexample/paper/paper.pdf)、[LaTeX 源码](006-strong-product-packing-counterexample/paper/main.tex)、[论文验证与学术状态](006-strong-product-packing-counterexample/paper/README.md)及[固定论文 Release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09)已公开。人工作者信息及责任确认仍待完成，未宣称正式投稿或同行评审。

### 已获独立书面复核、尚待主分支集成的原命题解答

这些完整书面证明仍保留在 A／B／C 分支，**不是主分支已发布数学成果，也没有完整 Lean 认证**。链接锁定实际复核过的冻结提交；后续算法、论文和形式化分别验收。独立书面验收的公开阶段摘要见[冻结协调记录](https://github.com/mio-qwq/math/blob/abd8e85628b1348f250c5d5c46a5450caae2876d/coordination/distributed/BRIEF.md)，部分详细独立报告尚未公开。

| 原始论文与准确命题 | 原命题与已核验结论 | 冻结证明与贡献边界 |
| --- | --- | --- |
| **Gorzkowska–Kwaśny Conjecture 10**，[*Distinguishing adjacent vertices by ordering edges*](https://arxiv.org/html/2609.11832v1#S5) | 每个非 $K_2$、非偶圈的有限连通简单图，任意固定正常边着色均可用一个全局边序区分相邻顶点的关联颜色序列。**完整构造性正面证明**：补足全部 $d\ge3$ 正常 $d$ 边着色的 $d$ 正则情形，再结合原作者已证部分 | [A：全次数完整证明](https://github.com/mio-qwq/math/blob/7168f6df66ba5518cd3420c4668eab5352e4be8c/workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md)。不重着色；原文 Theorem 5 及圈情形明确归属，通用程序包与论文材料仍另待执行验收 |
| **Braun–Bruegge Conjecture 31**，[*Facets of Symmetric Edge Polytopes for Graphs with Few Edges*，JIS 26 (2023), Article 23.7.2](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf)；arXiv v4 为 Conjecture 5.1 | 原文二项式有限和 $F$ 在合法同奇偶、保序参数上的两项转移不等式：$F(a,b,c)\le F(a+2,b,c-2)$ 与 $F(a,b,c)\le F(a+2,b-2,c)$。**原标量陈述完整证明**；并得固定和 $n+1$ 下偶 $n\ge4$ 的极值 $(n-1,1,1)$、奇 $n\ge5$ 的极值 $(n-3,2,2)$ | [A：原标量证明](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/braun-bruegge-f31/PROOF.md) · [多参数推广](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/braun-bruegge-f31/GENERALIZATION.md)。不推出更广的简单图／多面体极值猜想；混奇偶后续稿另待复核 |
| **连续生成元循环有向图最优性猜想**。Chandran 等，[*The general position number of digraphs*，§3.1 Theorem 3.3 后的未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS1) | 对 $\operatorname{Circ}(n,\{1,\ldots,d\})$，原文两种构造中较大的是否总是最优？**全部 $1\le d<n$ 的完整正面证明**，精确值见下式；包括端点与全部余数 | [B：完整证明](https://github.com/mio-qwq/math/blob/628cb3551046886c4fcb383243a090d4b664a231/workstreams/B/circulant/PROOF.md) · [同冻结包的内部审查](https://github.com/mio-qwq/math/blob/628cb3551046886c4fcb383243a090d4b664a231/workstreams/B/audit/REPORT.md)。另经独立原定义全参数复核；条件性余数引理的 Lean 不等于实际图精确公式 Lean |
| **El Zein–Mortada Conjecture 6**，[*Impact of local girth on the S-packing coloring of k-saturated subcubic graphs*，§5](https://arxiv.org/html/2603.25113v1#S5) | 每个三度点都属于三角形的有限简单 $(3,0)$-saturated 次三次图，是否有 $(1,1,2)$ 打包着色？**原全范围正面证明** | [B：完整证明](https://github.com/mio-qwq/math/blob/d6238ac622243f683d1386aa7ca8dc029171e0c4/workstreams/B/heavy_triangle_112/PROOF.md)。与已被反驳的 2-saturated Conjecture 3 是不同命题；无完整 Lean |
| **El Zein–Mortada Conjecture 2**，同论文 [§5](https://arxiv.org/html/2603.25113v1#S5) | 每个三度点都属于三角形的有限简单 1-saturated 次三次图，是否有标准五色打包着色，即半径 $(1,2,3,4,5)$？**原全范围正面证明**，覆盖菱形、一般路径连接及链／环结构 | [B：五色证明](https://github.com/mio-qwq/math/blob/b49a74f9ed65133a8c0e12ee998c44c5401e73d8/workstreams/B/triangle_packing/FIVE_PROOF.md)。完整结构论证及有限状态证书已独立重建；既有特殊图族明确归属，历史新颖性未确定 |
| **Mizzi 修订版第一条猜想**，[*Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*，arXiv:2603.27559v3 §7 未编号两项猜想的第一项](https://arxiv.org/html/2603.27559v3#S7) | 原文非同构 TF-cousins 图对：一图是否含两条顶点不交的奇长 $C_k$，另一图含 $C_{2k}$？**完整图对全称证明**，覆盖原文默认范围 | [C：完整证明](https://github.com/mio-qwq/math/blob/6d479a99483637028f8bf8938746f15d3178cb35/workstreams/C/mizzi_first_clause_full_proof_20261010.md)。这些是普通简单圈，不要求诱导；不依赖有限实例外推 |
| **Mizzi 修订版第二条猜想**，同论文 [v3 §7](https://arxiv.org/html/2603.27559v3#S7) | 原文连通范围内，有限非对称不稳定图是否同时含 $C_k$ 与 $C_{2k}$（奇数 $k\ge3$）？**完整正面证明，并可取两圈顶点不交**；不同轨道长度与固定点均纳入 | [C：完整证明](https://github.com/mio-qwq/math/blob/6d479a99483637028f8bf8938746f15d3178cb35/workstreams/C/mizzi_v3_asymmetric_full_proof.md)。扩展定理须保留非平凡 TF 对的存在假设；不能外推到任意非连通图的 CDC 不稳定性。群论输入含既有 Bychawski 结果 |
| **无爪次三次图的 $(1,2,2,2,2)$ 猜想**。Mortada 等，[*On (1,1,2,3)- and (1,1,3,3,3)-Packing Colorings of Claw-Free Subcubic Graphs*，§6 Conjecture 1](https://arxiv.org/html/2608.02566v1#S6) | 每个有限无爪次三次图均可作此着色。**原全范围正面推论证明**，包括三角形、菱形及任意路径连接 | [B：完整推论证明](https://github.com/mio-qwq/math/blob/15470c9423245b31d2b8949a9d2485eb5577b820/workstreams/B/clawfree_12222/FULL_PROOF.md)。核心使用已有 Yang–Wu 边权着色定理；不宣称新边着色定理或历史首次解决 |
| **循环图的 monophonic position 存在性猜想**。Tuite–Thomas–Chandran，[*On some extremal position problems for graphs*，AMC 25 (2025), #P1.09，Conjecture 4.5](https://oro.open.ac.uk/92086/13/92086final.pdf) | 每个 $n\ge11$ 是否都存在直径 2、monophonic position 数为 2 的简单无向循环图？**完整反例：$n=15$ 不存在这样的图**。全部 128 个对称连接集经结构分类排除，反驳原全称存在性，而非仅展示一个失败图 | [B：完整排除证明](https://github.com/mio-qwq/math/blob/6022d2bcb52324f834028e21c458e0f890e23d14/workstreams/B/monophonic_circulants/COUNTEREXAMPLE_PROOF.md) · [来源与历史门控](https://github.com/mio-qwq/math/blob/6022d2bcb52324f834028e21c458e0f890e23d14/workstreams/B/monophonic_circulants/SOURCE_GATE.md)。独立原定义书面复核通过；无完整 Lean／主分支集成／首次声明。monophonic 限制的是全部诱导路径，与上方有向最短路径问题不同 |

循环有向图的精确式采用原文的余数约定 $n=qd+r$，$q\ge0$、$2\le r\le d+1$：

$$
\operatorname{gp}(\operatorname{Circ}(n,\{1,\ldots,d\}))=
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
| **Kautz 图精确一般位置数**。Chandran 等，[Problem 5.2](https://arxiv.org/html/2604.15909v1#S5)：求树、置换图及词长 $k\ge3$ 的 Kautz 图的一般公式 | **词长三全部参数 $m\ge3$ 的精确公式**：$\operatorname{gp}(\mathrm{Ka}(m,3))=m(m-1)(2m-1)/6$，允许首尾字母相同。一般词长原问题未解决 | **独立书面复核通过、待集成**：[B：完整证明](https://github.com/mio-qwq/math/blob/44c1ec16781f1c363d0874e4dd2f0d93f640a48e/workstreams/B/kautz_length3/PROOF.md)。原始路径语义与全基数的 Lean 集成正在推进，尚无完整已发布 Lean |
| **同一 Problem 5.2 的词长四推进** | **极限存在与新界**：$\lambda_4=\lim_{m\to\infty}\operatorname{gp}(\mathrm{Ka}(m,4))/m^4$ 存在，$26/125\le\lambda_4\le377/1320<2/7$。取整后的有限上界适用 $m\ge11$；未确定精确有限值或极限值 | **独立书面复核通过、待集成、无完整 Lean**：[B：极限与密度证明](https://github.com/mio-qwq/math/blob/0599b104ac0fe3f241a7a3ba4dfeae878c28951f/workstreams/B/kautz_length4/DENSITY_LIMIT.md) · [取整修正](https://github.com/mio-qwq/math/blob/e73202f7223a510ece8a30d7f2d60c6d2cd3dd5e/workstreams/B/kautz_length4/ROUNDING_REFINEMENT.md)。验收含原图距离、全称上界与证书提升；历史原创性仍待核查 |

<details>
<summary>原始论文索引与版本辨认</summary>

- Bujtás、Iršič Chenoweth、Klavžar、Zhang：[On d-distance p-packing domination number in strong products](https://arxiv.org/abs/2510.02749)，本页对应 v1 Conjecture 3.1。
- Chandran 等：[The general position number of digraphs](https://arxiv.org/abs/2604.15909)，本页对应 v1：§3.1／§3.3 两条未编号猜想、Conjecture 4.30 与 Problem 5.2。
- El Zein、Mortada：[Impact of local girth on the S-packing coloring of k-saturated subcubic graphs](https://arxiv.org/abs/2603.25113)，本页区分 v1 Conjectures 2、3、6。
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
| [**001：逐项幂 Hadamard 刚性与解空间分类**](001-odd-half-order-hadamard/README.md) | 对 $m\ge2$，在 $2m$ 阶矩阵的逐项幂 $1,\ldots,m-1$ 均为 Hadamard 的假设下，证明奇数半阶根刚性；给出全部此类半阶的根种子与单相位构造的穷尽分类、带标号去相位解空间及标准矩阵等价商的有限图描述 | 完整结构分类与拓扑描述为书面证明；支持集、实际复数分块、多项式及行比乘积障碍有 Lean。不是全部复 Hadamard 矩阵的无条件分类，也不宣称新偶数阶种子存在；与既有 switching 理论的原创性关系仍需审查 |
| [**002：加权矩形剪枝与独立成对成本**](002-weighted-rectangular-pruning/README.md) | 任意有限关系的乘积权重剪枝界；在局部兼容不等式下，任一关系为弦二部图时独立非负成对成本的尖锐系数一；平移不变六圈的实际覆盖界、精确书面最优值及两正乘积之和的统一常数障碍 | 一般结构推广为完整书面构造，覆盖零成本与部分输入；六圈全输入覆盖、剪枝和尖锐性等有 Lean。任意关系的全部独立成本情形未解决；九式最优值及不变部分输入尚非完整 Lean |
| [**003：20 维代数、投射分解与 Yoneda／Tate 结构**](003-arc-one-parameter/README.md) | 特征二下的实际代数、核心对偶平凡扩张与根基；指定模块全次数投射分解、实际 $\operatorname{Ext}^3$ 类及 $\operatorname{Ext}^6$ 中 Yoneda 平方；有限共振模块的构造与全整数次数 Tate 乘法；下层代数实际 self-Ext 和 regular-target Ext 计算 | 代数与若干实际同调对象已 Lean 化；次数三类与其平方的非零结论分别保留 $q^3\ne0$ 与 $q^4\ne0$ 等原假设。有限共振及完整 Tate 结构主要为书面证明；高次幂、完整 20 维 self-Ext 谱及完整 ARC 实现未完成。下层既有数学结论按 [来源比较](003-arc-one-parameter/ATTRIBUTION.md)归属 |
| [**004：六维 MUB 三元组的伴随兼容性**](004-mub-triplets/README.md) | 完整伴随基的谱矩判据、固定配对支持和酉相位分类；四循环分支消去；实际归一化 MUB 三元组在指定分区的两三阶特征标分别为 $0$ 与 $(243-351i)/125$ | 谱权重、实际矩阵支持／酉条件及该三元组已有 Lean。例子否定更强的“两特征标各自为零”路线，未否定原乘积为零猜想；一般伴随选择及六维最大 MUB 数问题未解决 |
| [**005：有向圈打包的反馈集障碍**](005-directed-cycle-packing/README.md) | 对最小出度为正的弧支配定向图，证明反馈集大小严格超过最小出度；另有七点反馈集对指定打包目标的书面推论 | 指定假设下的全称反馈集障碍有 Lean；从反馈集到一般打包的桥不属于该端点。不是 Bermond–Thomassen $k=4$ 原猜想的完整证明或反例 |
| [**006：强积打包支配猜想反例与论文**](006-strong-product-packing-counterexample/README.md) | 见上方完整原命题反例；同时提供辅助图、64 中心集合、独立精确重放和英文论文 | 存在性层面的完整 Lean 反例已发布；最优中心数、最小辅助图及完整分类不在本结论中 |
| [**ROOT：一般位置、打包着色与图谱独立成果**](workstreams/ROOT/) | 上方置换图反例、两项打包着色反例、主特征值正面解答及全树谱定理 | 各专题各自验收并发布；不将多个特殊情形拼成未证明的更广命题 |
| [**专项笔记与方法边界**](notes/) | $Q_6$ 积图、$C_7$ 码率、指定 $D_5$ 补点、局部三角形交换及七核替换族 | 下方逐项区分图族障碍、有限反例、书面证明和 Lean 实际端点 |

<details>
<summary>展开：001–004 的主要技术与延伸材料</summary>

- **001**：[全半阶根／相位分类](001-odd-half-order-hadamard/general-patterns.md)、[带标号有限解图](001-odd-half-order-hadamard/phase-geometry.md)、[标准矩阵等价商](001-odd-half-order-hadamard/equivalence-quotient.md)。
- **002**：[兼容成对成本](002-weighted-rectangular-pruning/compatible-pair-costs.md)、[两类反身成本](002-weighted-rectangular-pruning/reflexive-cost-families.md)、[双路径独立成本](002-weighted-rectangular-pruning/double-path-independent-costs.md)、[单侧块／路径展开](002-weighted-rectangular-pruning/binary-one-side-costs.md)、[嵌套关系](002-weighted-rectangular-pruning/nested-relation-costs.md)、[右叶扩张](002-weighted-rectangular-pruning/right-leaf-extension-costs.md)、[森林与悬挂星](002-weighted-rectangular-pruning/forest-pendant-star-costs.md)、[弦二部图](002-weighted-rectangular-pruning/chordal-bipartite-costs.md)、[六圈成本](002-weighted-rectangular-pruning/cyclic-six-costs.md)。这些是逐步覆盖更广结构的定理，不是九个独立解决的公开猜想。
- **003 的构造与乘法**：[共振 Yoneda 代数](003-arc-one-parameter/resonant-yoneda-algebra.md)、[有限共振实际实现](003-arc-one-parameter/finite-resonant-realization.md)、[有限阶 Tate 代数](003-arc-one-parameter/finite-resonant-tate-algebra.md)、[阶一接口与乘法](003-arc-one-parameter/order-one-tate-algebra.md)。
- **003 的实际代数与同调**：[标量端同态及分裂](003-arc-one-parameter/proof/mathlib/TwentyDimDualScaleEndomorphism.README.md)、[核心对偶平凡扩张](003-arc-one-parameter/proof/mathlib/TwentyDimTrivialExtension.README.md)、[结构比较与根基](003-arc-one-parameter/structural-bridge-replay.md)、[下层全次数投射分解](003-arc-one-parameter/proof/mathlib/LowerAlgebraCategoricalResolution.README.md)、[regular-target Ext](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularExt.README.md)、[实际右作用](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularRightAction.README.md)。下层 self-Ext 消失要求所有正整数 $m$ 的 $1+q^m\ne0$；regular-target 一维次数二计算另要求 $q\ne0$。
- **004**：[循环特征标](004-mub-triplets/direct-circulant-character.md)、[实际平坦 Gram 消去](004-mub-triplets/flat-gram-cancellation.md)、[归一化三元组的不对称特征标](004-mub-triplets/fourier-character-asymmetry.md)。一般条件性桥接与经典 Zauner 构造分别注明来源。

</details>

## 分布式分支成果

A／B／C 的完整公开命题解答和 Kautz 部分定理已在首页前部按状态列出。这里补充其他结构性成果与尚待验收材料，不重复计数。公开工作分支的发布不等于主分支集成或 ROOT 验收；作者文件中的旧状态文字亦不自动覆盖后续复核。

### 其他已独立书面复核的结构性成果

| 成果 | 已核验范围 | 冻结材料与边界 |
| --- | --- | --- |
| **固定 TF 对的精确计数与不稳定图数下界** | 双换位固定模式的完整正规形、精确标号计数；对 $N\ge16$，非同构意义下的连通、非二分、无孪生不稳定图数满足 $U_N\ge\frac{19}{20}\,2^{\binom N2-2N+3}/N!$ | [C-audit：正规形](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/MINIMAL_TF_SYMMETRY_NORMAL_FORM.md) · [下界](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/UNSTABLE_DENSITY_SHARPENED_LOWER.md)。基于已有构造；固定模式与全局下界不等于原全局计数问题的完整渐近解答，尚无完整 Lean |

### 待独立验收的候选与新材料

| 候选与原题 | 当前实际范围与待办 | 冻结入口 |
| --- | --- | --- |
| **顺序区分的通用构造与论文材料** | 上方 Conjecture 10 的数学证明已获独立书面复核；新全图算法、论文稿及两划分的线性二着色加强引理另行验收。Hall 替代接口明确未编译，不凭作者回执解除审查 | [A：全图算法](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/paper/FULL_GRAPH_ALGORITHM.md) · [工作论文](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/paper/WORKING_MANUSCRIPT.md) · [Hall 接口](https://github.com/mio-qwq/math/blob/c03ae8c40b67b3f5b0b0a92512475ff1dae43cb8/workstreams/A/formal/HallBridge.lean) · [两划分加强稿](https://github.com/mio-qwq/math/blob/79d2d1c4532f040e90da3f1e0fb34b1afdc2125e/workstreams/A/proof/TWO_PARTITION_BICOLOURING.md)。不重复计为新的原问题解答 |
| **笛卡尔积的下 GP 数界候选**。Kruft Welton–Khudairi–Tuite，[*Lower General Position in Cartesian Products*，预印本 Conjecture 2.10／期刊版 Conjecture 3](https://arxiv.org/html/2404.19451v1) | 原猜想为 $\operatorname{gp}^{-}(G\square H)\ge\min\{\operatorname{gp}^{-}(G),\operatorname{gp}^{-}(H)\}$，其中下 GP 数是极大一般位置集的最小基数。B 新提交通用截断至 4 的界，以及所有 $K(n,2)\square K(m,2)$、$n,m\ge5$ 的子类证明，**两稿均待独立验收** | [B：通用部分界](https://github.com/mio-qwq/math/blob/0949c807e9ce28b4066509066ee06433a593b4ff/workstreams/B/lower_gp_product/TRUNCATED_BOUND_PROOF.md) · [Kneser 子类稿](https://github.com/mio-qwq/math/blob/0949c807e9ce28b4066509066ee06433a593b4ff/workstreams/B/lower_gp_product/KNESER_FAMILY_PROOF.md)。无完整 Lean；不是任意因子原猜想的完整证明，已有因子公式明确归属 |
| **非平凡不稳定图的全局渐近计数候选**。Hujdurović–Mitrović，[*Some conditions implying stability of graphs*，Problem 5.3](https://arxiv.org/html/2210.15249v1#S5) | C-audit 新提交有限简单、连通、非二分、开邻域无孪生不稳定图的标号及非同构计数渐近主项，并提出典型自同构群推论。**该公开冻结包待独立验收**，不能用此前固定 TF 模式的复核代替 | [C-audit：完整计数候选](https://github.com/mio-qwq/math/blob/a3796283bf4a005413092a10fb04c1f2ec8ca49a/workstreams/C-audit-1010/GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md) · [条件性群结构推论](https://github.com/mio-qwq/math/blob/a3796283bf4a005413092a10fb04c1f2ec8ca49a/workstreams/C-audit-1010/GENERIC_COVER_GROUP_COROLLARY.md)。尚无完整 Lean／主分支集成；全局计数、随机图期望及零密度是不同结论，历史原创性待核查 |
| **广义无爪 TF 图族的全部参数表与 cousin 计数** | 已受理的固定模式计数不自动验收更广奇偶图族、低参数例外及全部 cousin 分类；须从原图和实际 TF 对重新核查 | [C-audit：参数与例外表](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/N1_EXCEPTIONS_AND_FULL_PARAMETER_TABLE.md) |

最新作者状态可从 [A](https://github.com/mio-qwq/math/tree/partner/dist-A/workstreams/A)、[B](https://github.com/mio-qwq/math/tree/partner/dist-B/workstreams/B)、[C](https://github.com/mio-qwq/math/tree/partner/dist-C/workstreams/C)及 [C-audit](https://github.com/mio-qwq/math/tree/partner/dist-C-audit-1010/workstreams/C-audit-1010)查看；这些是移动分支入口，不替代上面的冻结证据。

## 证明与复现

每项主要成果从专题入口可到达数学证明、原始文献、Lean 源码、运行日志、公理依赖与独立复核。近期 ROOT 成果的关键证据如下；审计数指实际检查的声明数，不是数学贡献数量。

| 成果 | Lean 源码 | 实际运行与独立复核 |
| --- | --- | --- |
| 006 强积反例 | [几何与路径](006-strong-product-packing-counterexample/proof/Q6PackingComplexGeometry.lean)、[原始反例端点](006-strong-product-packing-counterexample/proof/Q6PackingComplexCounterexample.lean) | [源文件验证记录](006-strong-product-packing-counterexample/results/lean-verification.json)：新增两源 12／26 项审计，独立重建含单因子共 12+12+26 项；精确图验证见专题 |
| 排列图 90 点反例 | [PermutationGP90.lean](workstreams/ROOT/permutation-gp-counterexample/PermutationGP90.lean) | [编译与 18 项审计](workstreams/ROOT/permutation-gp-counterexample/verification.json)、[独立复核](workstreams/ROOT/permutation-gp-counterexample/INDEPENDENT_REVIEW.md) |
| 无爪 36 点反例 | [ClawFree11334.lean](workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean) | [编译与 18 项审计](workstreams/ROOT/clawfree-11334-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/clawfree-11334-counterexample/INDEPENDENT_REVIEW.md) |
| 2-saturated 7 点反例 | [TwoSaturated112.lean](workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean) | [编译与 14 项审计](workstreams/ROOT/two-saturated-112-counterexample/lean-audit.json)、[独立复核](workstreams/ROOT/two-saturated-112-counterexample/INDEPENDENT_REVIEW.md) |
| CDC 主特征值 | [CDCMainEigenvalues.lean](workstreams/ROOT/cdc-main-eigenvalues/CDCMainEigenvalues.lean) | [编译、7 项审计及独立验收](workstreams/ROOT/cdc-main-eigenvalues/verification.json) |
| 全有限树 GP 谱 | [TreeGPSpectrum.lean](workstreams/ROOT/gp-tree-spectrum/TreeGPSpectrum.lean) | [编译与 44 项审计](workstreams/ROOT/gp-tree-spectrum/lean-audit.json)、[独立复核](workstreams/ROOT/gp-tree-spectrum/INDEPENDENT_REVIEW.md) |

上述成功编译记录均保留实际源码哈希和运行证据，退出码为零，无错误或警告；审计依赖仅为 `propext`、`Classical.choice`、`Quot.sound` 的子集，无 `sorryAx` 或新增公理。Lean 检查的是所写声明，其与原论文定义、量词和对象的对应关系还须通过语义审查。

Mathlib 项目固定使用 **Lean 4.34.1** 与 **Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`**。从仓库根目录进入现有固定环境，可重放无需额外本地模块构建的 ROOT 单文件，例如：

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/clawfree-11334-counterexample/ClawFree11334.lean
```

多模块项目、006 及使用本地导入的源码，应按各专题说明先构建相应依赖；不要以单文件示例代替这些构建步骤。Python 检查器的调用、依赖、精确证书及损坏输入控制也分别记录在专题中，部分重放会写入新时间戳，复现前应保留原始收据。

更细的既有源码索引见 [FORMALIZATION.md](FORMALIZATION.md)，问题分类见 [RESEARCH_QUESTIONS.md](RESEARCH_QUESTIONS.md)。这些记录各有自己的日期和覆盖范围；近期独立成果的最新端点应直接查上表的源文件记录。

重要里程碑另有 [GitHub Releases](https://github.com/mio-qwq/math/releases)，以精确提交、签名标签、源码 ZIP、manifest 和 SHA256SUMS 固定发布材料。上方列出的 Release 已核对为不可变发布。签名、公开时间和文件摘要证明版本与材料的可核查性，**不自动证明数学首创性**。

## 在研问题与方法边界

当前推进 Kautz 词长三精确计数的全称形式化、词长四密度界的后续研究，以及 TF 不稳定图的全局计数机制；15 阶 monophonic 循环图反例的书面论证已通过独立复核，形式化与集成另行推进。一般图的 GP 谱、公开打包着色问题的剩余范围，也须与已有解答逐项区分。选题前及重要结果后继续核对原始版本、勘误、后续论文和公开证明；未充分确认开放状态的目标明确保留不确定性。

早期方向的具体缺口包括 002 任意关系独立成本、003 尚未完成的同调桥与更高乘法、004 一般伴随耦合及六维 MUB、005 一般有向圈打包。这些缺口不是本仓库已经解决的原猜想。成熟成果的论文整理与研究价值审查可以继续，但不以定理或提交数量决定研究投入。

下列已发布笔记记录了有数学内容的特殊情形、失败机制与构造族界限，避免将局部认识误列为原问题解答：

| 专项成果 | 实际结论 | 边界与材料 |
| --- | --- | --- |
| **$Q_6\boxtimes Q_6$ 的中心构造障碍** | 排除全部二元仿射中心集；六点投影完整分类进一步排除十二中心，尚余非线性 13–21 中心范围 | [仿射障碍](notes/q6-strong-product-affine-obstruction.md)、[六点分类](notes/q6-six-point-midpoint-classification.md)。积图排除主要为书面证明；相关单因子／邻域端点有 Lean。006 用不同辅助因子反驳了原一般继承猜想，不等于解决这个固定积图 |
| **$C_7$ 既有格点参数族的直接映射障碍** | 对该明确构造族的全部可直接映射参数，证书码率至多 $\sqrt{10}$；算术与整数商已有 Lean | [完整笔记](notes/c7-fraction-family-barrier.md)。不是 $C_7$ Shannon 容量上界，也未提高已知下界；图构造／映射桥另有书面范围 |
| **指定 $D_5$ 三根删除后的连续补点界** | 保留其余 37 根，在任意实坐标候选中至多补三点；达到三点时只能补回原删根 | [连续分类与验证](notes/d5-three-root-cap.md)。Lean 已检查实际约束与分类，仅限所指定三根；不是所有删除模式，更不是五维接吻数的完整解答 |
| **局部三角形交换规则的有限反例** | 七顶点图满足所述局部打包／支撑条件，交换仍可破坏与保留边的兼容性；实际有限图反例已 Lean 化 | [规则、例子与范围](notes/triangle-swap-safety.md)。针对特定版本的辅助交换规则，不是 Tuza 原猜想反例，也不自动否定整套算法 |
| **七核短圈替换族的尖锐障碍** | 指定无有向三圈、无 $T_9$ 的正簇吹胀族，最小出度比最大为 $260889/805108<1/3$ | [分类、界与等号构造](notes/seven-core-short-cycle-substitution.md)。整族图论论证为书面；Lean 检查代数界、等号见证及严格间隙，不是一般短圈猜想解答 |

[公开问题候选审查](OPEN_PROBLEM_CANDIDATES.md)还保存七圈容量、五维接吻数及 SIC 等问题的阶段性文献核查。列入候选记录不等于当前仍已确认开放或正在重投入；没有检索到解答也不构成开放性证明。

## 学术声明

- **来源与贡献。** 本项目从原始论文和自己的推导开展研究，也使用公开通用理论。早期部分工作参考 [OpenAI/math](https://github.com/openai/math) 的公开证明，固定上游版本及借用内容见各专题。数学原结论、新证明、新推广及新增形式化分别归属；尤其 003 的 OpenAI／Tang 重合范围见 [ATTRIBUTION.md](003-arc-one-parameter/ATTRIBUTION.md)。
- **正确性与学术状态。** 精确计算、有限证书、全称书面证明和 Lean 端点不互相替代。没有把数值优化当作严格反例，未把工作分支候选当作正式验收结果，也未宣称本仓库材料已获人类同行评审、期刊接受或历史首次。文献审查仍可能遗漏未索引或隐含的既有结果。
- **AI 贡献。** AI 系统实际参与选题与文献分析、数学推导、反例构造、程序验证、Lean 形式化、独立研究 Agent 复核及论文写作。独立 Agent 复核的独立性指未参与相应发现与证明草拟，不等于外部人类审稿。不得将 AI Agent 或模型列为论文作者；人工署名与责任由实际贡献者最终确认，正式提交须按目标平台政策如实披露。
- **使用与引用。** 仓库使用 [Apache-2.0 许可证](LICENSE)；所引外部论文及理论仍按其来源引用。引用本仓库成果时宜同时给出原命题来源、专题材料和精确提交或 Release，并注明书面／形式化范围及历史原创性的不确定性。
