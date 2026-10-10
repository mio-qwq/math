# 数学研究：证明、反例与 Lean 形式化

本仓库研究公开数学问题，收录严格反例、完整证明、结构分类及可复现的计算与形式化材料。研究覆盖图论、组合数学、矩阵结构和同调代数；核心目标是对原始问题给出准确、可独立核验的数学答案。

这里分别记录**数学结论、形式化覆盖范围、独立复核和发布状态**。书面证明与 Lean 证明具有不同的验证范围；分支上的成果也不会因作者自行标记通过而自动成为主分支正式成果。本页按 **2026-10-10** 的实际源码、验证记录和远端分支整理，详细假设、文献关系及后续更新以各专题材料为准。

[重点成果](#重点成果) · [完整研究目录](#完整研究目录) · [分布式分支成果](#分布式分支成果) · [证明与复现](#证明与复现) · [在研问题与方法边界](#在研问题与方法边界) · [学术声明](#学术声明)

## 重点成果

以下成果均已进入主分支，包含完整书面论证、实际 Lean 编译与公理审计，以及未参与发现的研究 Agent 所作独立复核。**树谱定理解决原猜想的全部有限树情形；其余条目在所列原命题范围内给出完整反例或正面解答。** 独立 Agent 复核不是外部人类同行评议，历史原创性也须单独审查。

| 原始问题 | 数学结论与意义 | Lean 范围与限制 | 完整材料与固定版本 |
| --- | --- | --- | --- |
| **强积中的打包支配继承猜想（006）**：Bujtás 等，[Conjecture 3.1](https://arxiv.org/html/2510.02749v1#S3) | **完整反例**。构造有限连通简单图 $H$，使 $\gamma_2^3(Q_6)=\infty$，但 $\gamma_2^3(Q_6\boxtimes H)\le64$；$H$ 有 608 顶点、9,168 边。否定“一因子不存在该集合则任意强积也不存在”的原始全称命题 | 实际 `SimpleGraph`、`Walk` 上的完整存在性反例：单因子所有子集的障碍、辅助图和同一中心的覆盖。$H$ 的边数与连通性另有书面及精确图验证；64 不宣称最优 | [证明与验证](006-strong-product-packing-counterexample/README.md) · [反例 Release](https://github.com/mio-qwq/math/releases/tag/006-strong-product-conjecture-counterexample-2026-10-09) · [论文 PDF](006-strong-product-packing-counterexample/paper/paper.pdf) · [论文 Release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09) |
| **排列有向图一般位置数的最优性猜想**：[Theorem 3.6 后的猜想](https://arxiv.org/html/2604.15909v1#S3.SS3) | **完整反例**。在原始 $\mathrm{Pe}(6,3)$ 中构造 90 点一般位置集，严格超过猜想值 84；另有覆盖全部原参数 $k\ge3,d\ge2k$ 的三终结字母书面构造 | 固定 90 点反例对原图全部最短有向简单路径成立，18 项声明审计通过。全参数推广为独立复核的书面证明；未证明实际最大值等于 90 | [定理、来源与证书](workstreams/ROOT/permutation-gp-counterexample/THEOREM.md) · [Release](https://github.com/mio-qwq/math/releases/tag/permutation-gp-counterexample-2026-10-10) |
| **无爪次三次图的 $(1,1,3,3,4)$ 打包着色问题**：Mortada 等，[§6 Problem 1](https://arxiv.org/html/2608.02566v1#S6) | **完整反例**。36 顶点的连通、简单、三正则无爪图不可作目标着色，且不与原文指定的 12 顶点例外图同构；奇数 $k\ge3$ 的 $12k$ 顶点反例族有完整书面证明 | 固定 36 顶点图的度、无爪性、连通性、例外排除和任意着色的不可能性，18 项审计通过。无限族未完整 Lean 化；不声称最小反例 | [构造、证明与复核](workstreams/ROOT/clawfree-11334-counterexample/README.md) · [Release](https://github.com/mio-qwq/math/releases/tag/clawfree-11334-counterexample-2026-10-10) |
| **2-saturated 次三次图的 $(1,1,2)$ 打包着色猜想**：El Zein–Mortada，[§5 Conjecture 3](https://arxiv.org/html/2603.25113v1#S5) | **完整反例**。将 $K_4$ 中同一顶点的三条关联边各细分一次，得到 7 顶点、9 边的连通 2-saturated 次三次图，仍无目标着色。原猜想未附加局部围长条件 | 实际原图上的饱和条件、连通性和所有三色函数的不可能性，14 项审计通过。原文另一个带额外局部围长条件的定理不受此反例否定 | [证明与复核](workstreams/ROOT/two-saturated-112-counterexample/README.md) · [Release](https://github.com/mio-qwq/math/releases/tag/two-saturated-112-counterexample-2026-10-10) |
| **典范二重覆盖的主特征值问题**：Collins–Sciriha，[Question 5.8](https://arxiv.org/pdf/1906.05790)（期刊版 Question 16） | **完整正面解答**。任意有限简单图满足 $M(\operatorname{CDC}(G))=M(G)$，因而二重覆盖同构的两图具有相同的主特征值集合 | 任意有限顶点类型、真实邻接作用和非零坐标和的特征向量，7 项审计通过。允许孤立点和零特征值，不要求同构保层；结论仅指主特征值集合，并非整个邻接谱 | [定理、形式化与来源](workstreams/ROOT/cdc-main-eigenvalues/THEOREM.md) · [Release](https://github.com/mio-qwq/math/releases/tag/cdc-main-eigenvalues-lean-2026-10-10) |
| **有向一般位置谱的区间猜想**：[Conjecture 4.30](https://arxiv.org/html/2604.15909v1#S4.SS2) | **完整有限树情形**。每个有限树在全部边定向下的一般位置数谱都是整数区间，覆盖原文已处理树族以外的所有有限树 | 真实 `SimpleGraph.IsTree`、全部定向、原始最短路径和最大集基数，44 项审计通过。森林推论为书面分量和论证；任意图的原猜想未由此解决 | [定理、证明与复核](workstreams/ROOT/gp-tree-spectrum/README.md) · [Release](https://github.com/mio-qwq/math/releases/tag/tree-gp-spectrum-lean-2026-10-10) |

打包着色的元组表示各个**不同颜色**的距离半径，同色点的原图距离必须严格大于该半径；重复的 1 或 3 不是同一种颜色。上述反例均按原命题的全部假设核验，不以辅助路线失效、浮点搜索或局部模型代替原命题反例。

006 已有自包含英文研究稿：[PDF](006-strong-product-packing-counterexample/paper/paper.pdf)、[LaTeX 源码](006-strong-product-packing-counterexample/paper/main.tex)及[论文验证与学术状态](006-strong-product-packing-counterexample/paper/README.md)。目前是公开研究稿，人工作者信息及责任确认仍待完成，未宣称正式投稿或同行评审。

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
| [**ROOT：一般位置、打包着色与图谱独立成果**](workstreams/ROOT/) | 上方排列图反例、两项打包着色反例、主特征值正面解答及全树谱定理 | 各专题各自验收并发布；不将多个特殊情形拼成未证明的更广命题 |
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

以下内容保留在工作分支，**尚未作为主分支正式成果合入，也没有相应完整 Lean 认证**。链接锁定已审或待审的精确提交，不以移动分支名代替冻结输入。“书面复核通过”表示独立研究 Agent 已重建全称论证；其程序包、论文和形式化可仍有单独待办。作者文件中的旧状态文字不自动代表后续验收状态。

### 已独立复核的书面成果

| 方向与原命题 | 已核验的数学范围 | 材料与归属边界 |
| --- | --- | --- |
| **固定正常边着色的顺序区分猜想**：Gorzkowska–Kwaśny，Conjecture 10 | 全部 $d\ge3$ 正常 $d$ 边着色的 $d$ 正则图有构造性全局边序；结合原作者已证的调色板与圈情形，给出原猜想完整正面证明 | [A：全次数证明](https://github.com/mio-qwq/math/blob/7168f6df66ba5518cd3420c4668eab5352e4be8c/workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md)。借用原文 Theorem 5 明确归属；最新通用构造程序包仍待独立执行验收 |
| **Braun–Bruegge Conjecture 31 的标量陈述** | 二项式有限和的同奇偶参数转移与固定总和极值；另有多参数严格转移推广 | [A：原标量证明](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/braun-bruegge-f31/PROOF.md)、[推广](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/braun-bruegge-f31/GENERALIZATION.md)。不推出原论文更广的简单图／多面体极值猜想；混奇偶的后续稿另行待审 |
| **El Zein–Mortada Conjecture 6** | 全部有限简单、$(3,0)$-saturated 次三次图，在每个三度点属于三角形的条件下存在 $(1,1,2)$ 打包着色 | [B：完整证明](https://github.com/mio-qwq/math/blob/d6238ac622243f683d1386aa7ca8dc029171e0c4/workstreams/B/heavy_triangle_112/PROOF.md)。这是正面结论，与主分支反驳的 2-saturated Conjecture 3 不同 |
| **El Zein–Mortada Conjecture 2** | 全部有限简单、1-saturated、每个三度点属于三角形的次三次图有标准五色打包着色；包括一般连接路径、菱形与链／环结构 | [B：五色证明](https://github.com/mio-qwq/math/blob/b49a74f9ed65133a8c0e12ee998c44c5401e73d8/workstreams/B/triangle_packing/FIVE_PROOF.md)。全称结构论证结合完整有限状态证书，证书已独立重建；已有特殊图族须归属既有文献，历史新颖性未确定 |
| **Kautz 图一般位置数，Problem 5.2 的词长三情形** | 原始 $\mathrm{Ka}(m,3)$ 对所有 $m\ge3$ 满足 $\operatorname{gp}=\sum_{j=1}^{m-1}j^2=m(m-1)(2m-1)/6$，允许首尾字母相同 | [B：精确全参数证明](https://github.com/mio-qwq/math/blob/44c1ec16781f1c363d0874e4dd2f0d93f640a48e/workstreams/B/kautz_length3/PROOF.md)。ROOT 正在完成原始最短路径语义与全基数定理的 Lean 集成；词长四及一般词长不由此解决 |
| **Mizzi 修订版第一条 TF-cousin 循环猜想** | 非同构有限图的典范二重覆盖同构时，一图含两条顶点不交的奇长 $C_k$，另一图含 $C_{2k}$；完整覆盖原文默认范围 | [C：图对全称证明](https://github.com/mio-qwq/math/blob/6d479a99483637028f8bf8938746f15d3178cb35/workstreams/C/mizzi_first_clause_full_proof_20261010.md)。循环为普通简单圈，不要求诱导；不依赖有限样例外推 |
| **Mizzi 修订版第二条非对称不稳定图猜想** | 原文连通范围内，有限非对称不稳定图含互不交的 $C_k$ 与 $C_{2k}$，其中 $k\ge3$ 为奇数；不同轨道长度和固定点均包含 | [C：完整证明](https://github.com/mio-qwq/math/blob/6d479a99483637028f8bf8938746f15d3178cb35/workstreams/C/mizzi_v3_asymmetric_full_proof.md)。一般定理须保留“存在非平凡 TF 对”的假设，不能扩张为任意非连通图的原始 CDC 不稳定性；群论输入含既有 Bychawski 结果 |
| **固定 TF 对的精确计数与不稳定图数下界** | 双换位固定模式的完整正规形与标号计数；对 $N\ge16$，非同构意义下的连通、非二分、无孪生不稳定图数 $U_N\ge\frac{19}{20}\,2^{\binom N2-2N+3}/N!$ | [C-audit：正规形](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/MINIMAL_TF_SYMMETRY_NORMAL_FORM.md)、[下界](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/UNSTABLE_DENSITY_SHARPENED_LOWER.md)。基于已有构造；固定模式和全局下界不等于原全局计数问题的渐近解答 |
| **无爪次三次图的 $(1,2,2,2,2)$ 猜想** | 原文全范围的书面正面证明，包括三角形、菱形及任意路径连接 | [B：完整推论证明](https://github.com/mio-qwq/math/blob/15470c9423245b31d2b8949a9d2485eb5577b820/workstreams/B/clawfree_12222/FULL_PROOF.md)。核心使用已有 Yang–Wu 边权着色定理，应视为既有理论的明确推论，不宣称新边着色定理或首次解决 |

原始命题与历史比较在各证明及同目录 `SOURCE_GATE`／相关文献文件中给出。上述书面验收不代替主分支发布所需的最终材料检查；计算样例数量也不等于全称证明。

### 待独立验收的候选与新材料

| 候选 | 当前实际范围与待办 | 冻结入口 |
| --- | --- | --- |
| **词长四 Kautz 图的渐近密度** | 候选全称论证声称极限 $\lambda_4=\lim_{m\to\infty}\operatorname{gp}(\mathrm{Ka}(m,4))/m^4$ 存在，且 $26/125\le\lambda_4\le2/7$；后续取整稿进一步给出候选上界 $377/1320$。两稿均待独立数学验收，无完整 Lean，未给精确有限值或精确极限 | [B：密度与极限稿](https://github.com/mio-qwq/math/blob/0599b104ac0fe3f241a7a3ba4dfeae878c28951f/workstreams/B/kautz_length4/DENSITY_LIMIT.md)、[取整修正稿](https://github.com/mio-qwq/math/blob/e73202f7223a510ece8a30d7f2d60c6d2cd3dd5e/workstreams/B/kautz_length4/ROUNDING_REFINEMENT.md) |
| **顺序区分的通用构造与论文材料** | 全正则数学证明已有独立书面复核；新全图／非连通算法、输入回归、源文件绑定及论文稿的执行与完整性另行待验收，不凭作者运行回执解除审查 | [A：全图算法](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/paper/FULL_GRAPH_ALGORITHM.md)、[工作论文](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/paper/WORKING_MANUSCRIPT.md) |
| **广义 claw 图的 TF-cousin 参数分类** | 分支有奇偶参数、低阶例外及群作用计数稿；完整原定义对应关系、独立验收和形式化仍待完成 | [C-audit：全参数表](https://github.com/mio-qwq/math/blob/519a05b0ed6cfeb3b1ca56238fe2190ea1124fcb/workstreams/C-audit-1010/N1_EXCEPTIONS_AND_FULL_PARAMETER_TABLE.md) |

不同问题的“已证”“反例”“候选”分别列出，不因同一 Agent 的其他结果已获验收而继承其状态。其他被冻结但尚未核准的探索材料仍可从 [A 分支](https://github.com/mio-qwq/math/tree/partner/dist-A/workstreams/A)、[B 分支](https://github.com/mio-qwq/math/tree/partner/dist-B/workstreams/B)、[C 分支](https://github.com/mio-qwq/math/tree/partner/dist-C/workstreams/C)与 [C-audit 分支](https://github.com/mio-qwq/math/tree/partner/dist-C-audit-1010/workstreams/C-audit-1010)查阅；这些移动入口是工作记录，不是固定成果引用。

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

当前推进 Kautz 精确计数的全称形式化、词长四的新界验收，以及 TF 不稳定图的全局计数机制。一般图的 GP 谱、公开打包着色问题的剩余范围，也须与已有解答逐项区分。选题前及重要结果后继续核对原始版本、勘误、后续论文和公开证明；未充分确认开放状态的目标明确保留不确定性。

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
