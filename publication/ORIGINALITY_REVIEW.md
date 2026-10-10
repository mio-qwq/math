# 已验收成果的原创性与引用风险报告

审查日期：2026-10-10。数学材料基准为主分支提交 `6c9860628edc76ab4eac9ce82d4e552a2feff95d`；本次另审查 006 v1.2 稿件。A/B/C 的链接锁定已验收的提交，后续分支材料不自动继承验收。

本报告区分数学正确性、已有理论归属、历史新颖性和论文价值。**没有检出先前解答不等于首次发现。** 本轮独立复核由 AI 代理完成，不是外部人类同行评审；未进行作者联系、正式投稿或 DOI 注册。论文准备总表见 [PUBLICATION_READINESS.md](../PUBLICATION_READINESS.md)。

## 审查方法与证据限制

对重点成果先核对原文定义、量词、命题编号和最新可访问版本，再检索精确标识、题名、解答/勘误与等价术语，最后沿经典构造、直接引用、作者主页和公开综述检查潜在重复。重要结果再次按数学对象和结论核对，避免把另一参数、另一 palette 或旧版本的解答误作重复。

原作者论文、出版社、作者/机构自存稿是数学依据；搜索镜像仅用于定位。查询覆盖原始论文及后续公开材料，但未完成付费索引的全量引证图、所有未索引稿件或所有经典论文全文的穷尽核查。无法取得全文的条目单独保留。以下“中风险”均含历史不确定性；不是数学证明的质量等级。

本轮重新核对未变 Lean 源码与既有实际编译收据的哈希，不将读日志写成重新编译。006 的两个精确程序另于 2026-10-10 实际运行；新环境检查也实际执行，但不是 Lean 证明编译。

## 已集成原命题反例与重要证明

| 成果与原始锚点 | 相对已核对文献的贡献定位 | 在先内容与必须保留的限制 | 重复风险 |
| --- | --- | --- | --- |
| **006 强积打包支配**：[2510.02749v1 Conjecture 3.1](https://arxiv.org/html/2510.02749v1#S3)，[正式版](https://doi.org/10.1007/s00026-026-00814-0) | 显式有限连通简单图使一个因子无可行集合、强积却有可行集合；完整书面证明及原图/路径 Lean 存在性反例 | Plotkin 计数、Hamming 距离、强积距离公式和 perfect-code 理论已有。64 是上界，608 不是已证最小阶；历史首次未确认 | 中；Fisher 等历史全文仍有缺口 |
| **置换有向图**：[2604.15909v1 §3.3，Thm 3.6 后未编号猜想](https://arxiv.org/html/2604.15909v1#S3.SS3) | 在原 `k≥3,d≥2k` 范围构造 `3(d+k−3)_(k−1)` 点 GP 集；固定 `Pe(6,3)` 为 90>84 | 网络、原两终端构造与距离方法已有。新内容是三终端计数和合法缓冲路径；未求精确最大值。Lean 仅固定例，全参数为已复核书面证明 | 中 |
| **7 点 packing**：[2603.25113v1 Conjecture 3](https://arxiv.org/html/2603.25113v1#S5) | 经典 pyramid 严格否定无附加局部围长条件的 2-saturated `(1,1,2)` 猜想 | 图形及 odd-cut 方法已有；原定义 `g3` 取最大局部围长，本图为 5、普通 girth 为 3，不否定原 `g3=3` 正定理。未证最小性 | **高／不确定**；旧图例全文未排除 |
| **36 点 packing**：[2608.02566v1 §6 Problem 1](https://arxiv.org/html/2608.02566v1#S6) | 奇数 diamond 环的三角展开形成无目标 `(1,1,3,3,4)` 着色的书面无限族；固定 36 点 Lean 反例 | 展开和 core 技术已有；增量是色 4 的 private-neighbor 必要条件和奇环障碍。不是充要分类；未证最小性或全族 Lean | 中 |
| **15 阶 monophonic circulant**：[2106.06827v3 Conjecture 4.5](https://arxiv.org/html/2106.06827v3)，[期刊版](https://doi.org/10.26493/1855-3974.3094.bc6) | 排除全部 15 阶循环图同时具有直径 2、mp=2；书面归约及全部呈现的原定义 Lean | `C5` 的三点独立 blow-up 图形已知；贡献是整个阶数不存在见证。未证明最小失败阶，未否定一般图的存在性定理 | 中；期刊全文覆盖尚需补足 |
| **lower-GP 笛卡尔积**：[2404.19451v1 Conjecture 2.10](https://arxiv.org/html/2404.19451v1)，[期刊 Conjecture 3](https://doi.org/10.22049/cco.2024.29171.1879) | 固定 11×29 图的五点极大 GP 集否定因子最小值下界；已复核 `r≥6` 家族使差距无界、比例趋零 | true-twin clique 膨胀和 lower-terminal 乘积降落已有。新作用是同时保持两因子 lower-GP≥r 和乘积五点极大集。固定例 Lean；全族仅书面 | 中 |
| **Kautz 长度三**：[2604.15909v1 §3.2 Table 1／Problem 5.2](https://arxiv.org/html/2604.15909v1) | 证明原作者已数值观察的平方和公式，全部 `m≥3`；上界含非独立 GP 集，全参数 Lean | 公式观察归原作者；字母表大小 `m` 与度 `d=m−1` 要统一。`m=2` 是例外；不是所有长度的解答 | 中；**公式本身已有明确先例** |
| **有限树 GP 谱**：[2604.15909v1 Conjecture 4.30](https://arxiv.org/html/2604.15909v1#S4.SS2) | 全部有限树在所有定向间的 GP 数无缺值；完整树情形 Lean | 固定树定向的 GP 可用经典偏序 2-family 优化。增量是跨全部定向的插值；一般图猜想未解决，森林推论仅书面 | 中；特殊情形 |
| **CDC 主特征值**：[1906.05790v1 Question 5.8](https://arxiv.org/html/1906.05790v1)，[期刊 Question 16](https://www.dmgt.uz.zgora.pl/publish/pdf.php?doi=2386) | 自足短证明及原定义 Lean；解释原问题与既有定理的关系 | **原作者 Thm 3.3／期刊 Thm 2 已直接蕴含肯定结论**。不是新的重要开放问题突破；同主特征值不等于同全部谱 | **高：已有定理的直接推论** |

证明与复核入口： [006](../006-strong-product-packing-counterexample/paper/VERIFICATION.md)、[置换图](../workstreams/ROOT/permutation-gp-counterexample/INDEPENDENT_REVIEW.md)、[7 点](../workstreams/ROOT/two-saturated-112-counterexample/INDEPENDENT_REVIEW.md)、[36 点](../workstreams/ROOT/clawfree-11334-counterexample/INDEPENDENT_REVIEW.md)、[15 阶](../workstreams/ROOT/monophonic-circulant15-counterexample/INDEPENDENT_REVIEW.md)、[lower-GP](../workstreams/ROOT/lower-gp-product319-counterexample/INDEPENDENT_REVIEW.md)、[Kautz](../workstreams/ROOT/kautz3-exact-gp/INDEPENDENT_REVIEW.md)、[树谱](../workstreams/ROOT/gp-tree-spectrum/INDEPENDENT_REVIEW.md)、[CDC](../workstreams/ROOT/cdc-main-eigenvalues/INDEPENDENT_REVIEW.md)。

## 关键归属判断

### 006：反例有效，经典输入不属于新发现

当前 arXiv v1 与正式版的 Conjecture 3.1 都只要求一个因子不可行；反例取 `(d,p)=(2,3)`，位于原文剩余区间 `d<p<2d`。64 中心同时覆盖两坐标，不能用分别存在的两个中心代替。本次独立审查从定义重新推导了 cube 任意集合障碍、短路排除和所有支持类型覆盖，未发现数学必须修复项。

[Abay-Asmerom–Hammack–Taylor 的原稿](https://richardhammack.github.io/reprints/rperfect_codes_strong_prod.pdf)涉及不重叠的 perfect-code 球分割，与本例重叠的半径二球不同；应充分归属，不能直接认作本猜想的既有解决。Fisher 的 [1994 原论文](https://doi.org/10.1137/S0895480191217806)及其 [2013 引用后继](https://doi.org/10.1016/j.disc.2012.10.008)尚未完成全文覆盖；[Plotkin 原文](https://doi.org/10.1109/TIT.1960.1057584)本轮全文也不可达。论文提供自己的计数证明，不依赖不可达全文补足逻辑，但不能据此认证历史首次。

006 v1.2 的数学未改变。稿件明确披露 AI 在数学、Lean、检查器、检索、审查及写作中的实质作用，不把此类工作缩减成语言润色。完整最终材料的检查见 [006 投稿前复核](006-v1.2/REVIEW.md)。

### CDC：原定理的直接推论

原 Theorem 3.3、期刊 Theorem 2 保持全部长度参数的行走矩阵。对 n 阶邻接矩阵 A 取列 `j,Aj,…,A^n j`，相同行置换保持列依赖，因此保持使 `m(A)j=0` 的最小首一多项式。实对称谱分解说明其根正是主特征值。只取一次足够大的长度即可，不需要所有长度共用同一标号。

所以原作者仍把问题列为 Question 16，与其已有定理蕴含答案是两个不同事实。可写“给出该推论的自足证明与形式化”，不能写“发现此前未知的 CDC 谱不变量”。CDC 同构不保持全部邻接谱，后者不能由本结果推出。

### 7／36 点：两个不同 palette 的反例

7 点构型属于经典 [pyramid](https://arxiv.org/abs/1912.11246)；删去 packing 色类后二分的机制已有于 [S-Packing Colorings of Cubic Graphs](https://arxiv.org/html/1403.7495v2)。重点旧文 [AJC 90(2) (2024), 155–167](https://ajc.maths.uq.edu.au/pdf/90/ajc_v90_p155.pdf)的全文在本轮受限，必须保留旧反例图覆盖不足的风险。已核对 [2024/25 后续稿](https://arxiv.org/html/2407.07424v1)和 [AJC 92(2) (2025), 237–243](https://ajc.maths.uq.edu.au/pdf/92/ajc_v92_p237.pdf)的相关正结果；不同饱和度或不同 palette 不能当成同一命题。

36 点族从任何原着色选择每个三角形的一个高色代表，得到必要条件，不假设恰好一个代表。色 4 要求外部私有邻点；奇数 diamond 环违反此条件。它既不同于半径 5 的旧负例，也不否定半径 3 的正定理。推荐合成一篇 packing 反例短文，分别列明两个原问题，避免将短例包装成新的通用理论。

### Monophonic：版本变化与已知 survivor

2106.06827 的 v1/v2 曾在 Thm 4.4 的证明中写 11≤n≤32 的 circulant 计算范围；v3 删除这句，Conjecture 4.5 保留。不能引用旧计算句支持当前猜想，也不能猜测删除原因。n=15 的反例必须排除所有连接集；一张图的 mp>2 不足够。

书面归约中唯一直径二的 triangle-free 类型是 `C5 ∘ overline(K3)`。同一图和连接集 `{1,4,6}` 已见于 [Severini–Weisstein 2608.19467v1](https://arxiv.org/abs/2608.19467)，用于另一问题；不据此判定 monophonic 排除重复，也不把图形当成新构造。当前 arXiv v3 的全文已核对；[期刊机构终稿](https://oro.open.ac.uk/92086/13/92086final.pdf)本轮仅取得官方索引中的准确锚点，不能声称本轮遍读全文。既有验收中的终稿定位与本次访问范围分别记录。

### Lower-GP：突出无界乘积机制，归属旧膨胀引理

lower-GP 是包含极大 GP 集的最小基数。`r≥6` 家族有因子阶 `2r−1`、`4r+5`，两因子 lower-GP 至少 r，乘积有五点极大 GP 集，从而差距至少 `r−5`、比例至多 `5/r`。这是同一个 min 猜想的反例与加强，不重复计为两个解答。

True-twin saturation 已见于 [Brešar–Yero 2307.02951v2 Prop 5](https://arxiv.org/html/2307.02951v2)，也见于 [Lower General Position Sets in Graphs](https://arxiv.org/html/2306.09965v2)。原 [期刊终稿](https://oro.open.ac.uk/98050/9/98050final.pdf)的 Prop 1 已有 lower-terminal 与乘积的任意大差距；那个参数不能替代两个因子的 lower-GP。论文应比较这个最近先例，突出新五点极大集的作用。全参数家族已书面独立复核，固定 r=6 实例有 Lean；不得交换验证层级。

### Kautz 与树谱：准确描述特殊情形

Kautz 原 Table 1 已观察 `5,14,30,55,91` 的平方和模式。新稿应写“证明所观察公式”，而不是“发现公式”；完整上界必须覆盖含弧的 GP 集。标准 Kautz 长度三允许首尾字母相同，m=2 不满足所显示公式。

树谱贡献是全部定向间无缺值。固定定向的 2-family 优化有 [Greene–Kleitman](https://doi.org/10.1016/0097-3165(76)90077-7)等经典背景；不能声称首个树上算法。一般图 Conjecture 4.30 未解决。当前 [GP survey v5](https://arxiv.org/html/2501.19385v5)用于核对引文链，不能作为独立的全球开放性证明。

## 已独立书面验收、未主分支形式化集成的成果

此表只评估已接受的书面命题，不批准后续算法、论文或新加强稿。源证明未在本轮修改；状态与冻结链接须同时保留。

| 成果 | 当前贡献范围与引用风险 | 冻结入口／本轮查重深度 |
| --- | --- | --- |
| Gorzkowska–Kwaśny Conjecture 10 | 补足 regular class-one 的全部 d≥3 情形，再结合原作者正结果；固定正常边着色不改变。原 Theorem 5/9 与圈情形须明确归属 | [完整证明](https://github.com/mio-qwq/math/blob/7168f6df66ba5518cd3420c4668eab5352e4be8c/workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md)；本轮核对 [2609.11832v1](https://arxiv.org/html/2609.11832v1)，未完成所有旧 edge-ordering 论文的全文查重 |
| Braun–Bruegge Conjecture 31／arXiv v4 Conjecture 5.1 | 原有限二项式和的标量转移不等式与同奇偶极值；不推出更广图／多面体极值猜想。Vandermonde 等经典工具应归属 | [标量证明](https://github.com/mio-qwq/math/blob/2a289d276c23e17569ea9143f9daa67bf1d044b2/workstreams/A/braun-bruegge-f31/PROOF.md)；核对 [JIS 原文](https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf)、[arXiv v4](https://arxiv.org/abs/2201.13303v4)及 [join-graph 后续](https://arxiv.org/html/2312.11287v3)。后者不是同一标量命题；穷尽等价查重未完成 |
| 连续生成元循环有向图最优性 | `Circ(n,{1,…,d})` 全部参数的 GP 精确值；仅这一生成集。原文已有两种下界构造，新增是普遍上界 | [完整证明](https://github.com/mio-qwq/math/blob/628cb3551046886c4fcb383243a090d4b664a231/workstreams/B/circulant/PROOF.md)；源 [2604.15909v1 §3.1](https://arxiv.org/html/2604.15909v1#S3.SS1)。本阶段沿用已验收原定义审查，专项历史全文查重尚不足 |
| El Zein–Mortada Conjecture 6 | 三度点都在三角形的 `(3,0)`-saturated 图 `(1,1,2)` 全范围证明；与失败的 Conjecture 3 不同 | [冻结证明](https://github.com/mio-qwq/math/blob/d6238ac622243f683d1386aa7ca8dc029171e0c4/workstreams/B/heavy_triangle_112/PROOF.md)；[原文 §5](https://arxiv.org/html/2603.25113v1#S5)。旧 packing 全文覆盖不足，中／不确定风险 |
| El Zein–Mortada Conjecture 2 | 三度点都在三角形的 1-saturated 图具有半径 `(1,2,3,4,5)` 着色；保留全部结构范围 | [冻结证明](https://github.com/mio-qwq/math/blob/b49a74f9ed65133a8c0e12ee998c44c5401e73d8/workstreams/B/triangle_packing/FIVE_PROOF.md)。专项投稿级旧文查重未完成，不把内部有限状态 PASS 写成完整 Lean |
| 无爪 `(1,2,2,2,2)` | 从已有 Yang–Wu 边权着色定理得到完整推论；不是新边着色定理 | [冻结推论](https://github.com/mio-qwq/math/blob/15470c9423245b31d2b8949a9d2485eb5577b820/workstreams/B/clawfree_12222/FULL_PROOF.md)。历史等价性风险较高，宜与 packing 论文一起归属审查 |
| Kautz 长度四 | 极限存在及 `26/125≤λ4≤377/1320<2/7`，有限取整界 m≥11；不是精确公式 | [密度定理](https://github.com/mio-qwq/math/blob/0599b104ac0fe3f241a7a3ba4dfeae878c28951f/workstreams/B/kautz_length4/DENSITY_LIMIT.md)。已书面验收，但本阶段未完成专项新颖性审查／完整 Lean |
| Vertex-position 比值 | 已验收无界比值及次三次二分加强；对象不同于 shortest-path GP | [冻结证明](https://github.com/mio-qwq/math/blob/d1d82779f60c522dd2fa689d27c7c839d1115012/workstreams/B/vertex_position_ratio/PROOF.md)；原 [DMGT 问题](https://doi.org/10.7151/dmgt.2491)。无完整 Lean；最新后续全文查重仍需专项完成，暂不独立包装论文 |
| Mizzi v3 两条 | 完整书面证明：非同构 TF-cousins 的配对奇／偶简单环，以及原连通背景下 asymmetric unstable 图的奇／偶环 | [当前冻结 C 文件](https://github.com/mio-qwq/math/tree/979598c300580b18b603b51ded9ccdf59f470faa/workstreams/C)。本轮完成版本与经典 TF 输入重点审查，结论见下节；旧结构全文仍有缺口 |

Vertex-position 行的证明链接必须以实际冻结分支中可见文件为准；其书面验收不扩大到任何不同位置参数。以上均未取得人类同行评审认证。

### Mizzi：旧反例不能否定 v3 修订命题

[Mizzi 当前 v3 §7](https://arxiv.org/html/2603.27559v3#S7)与 v2 量词不同。[Srivastava 2608.15281v1](https://arxiv.org/html/2608.15281v1)的十顶点反例针对旧单图表述；该图有普通自同构 `(1 6)(2 3)`，不是 asymmetric。因此它没有否定 v3 第二条，也不是第一条图对普遍证明。

C 的增量候选应定位在从非同构／不对称障碍到普通简单环的显式嵌入。TF twist、轨道独立与群论输入已见于 [Lauri–Mizzi–Scapellato 2011](https://ajc.maths.uq.edu.au/pdf/49/ajc_v49_p165.pdf)、[Bychawski 2406.06267v1](https://arxiv.org/html/2406.06267v1)等。直接相关 [1989 对称矩阵论文](https://doi.org/10.1016/0024-3795(89)90075-X)、[1997 结构论文](https://doi.org/10.1016/S0012-365X(97)00018-6)的全文未取得，故不认证历史首次。

第二条须保留原文连通、非二分、vertex-determining 背景，或明确存在非平凡 TF 对。不能只写任意非连通 asymmetric CDC-unstable 图：一棵三臂长 1、2、3 的树与孤立点的并可给无环的扩大表述反例。这个范围修正不否定已验收的原 v3 命题。

## 001–005 与其他结构性材料

| 项目 | 已有／新贡献界限 | 论文与查重决策 |
| --- | --- | --- |
| [001 Hadamard](../001-odd-half-order-hadamard/paper.md) | GH 字符判据、Butson 与 switching 已有；任意单位相位多重幂正交强迫根结构的必要性仍有候选价值 | [Power Hadamard matrices](https://doi.org/10.1016/j.disc.2006.06.050)全文未取得；[Acar–Yayla](https://arxiv.org/abs/2004.00771)、[Orrick](https://arxiv.org/abs/math/0507515)、[Szöllősi](https://arxiv.org/abs/math/0610297)须归属。暂缓新的独立预印本；完整分类不能写成全部已 Lean 化 |
| [002 pruning](../002-weighted-rectangular-pruning/paper.md) | 精确产品权重／实际未覆盖预算是技术增量；复制、min-cut、Four Functions 方法已知 | 比较 [Seacrest](https://arxiv.org/abs/1212.1883)、[Ahlswede–Daykin 1978](https://noah.nrw/ubbihs/download/pdf/5106477)及 [1979](https://noah.nrw/ubbihs/download/pdf/5106483)。不能包装成新 max-flow 或任意四成本。其他更强已验收命题不自动属于当前 paper |
| [003 ARC](../003-arc-one-parameter/ATTRIBUTION.md) | 原 ARC 构造来自 OpenAI；基础扩域、自 Ext／ARC 结论与 Tang 当前 v2 重合。有限证书和局部 Yoneda 形式化仍有验证价值 | [OpenAI 固定原稿](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-counterexample-to-the-Auslander-Reiten-conjecture-September-23-2026)、[Qiyue Tang，Hexagon 2610.00143v2](https://hexagonmath.org/2610.00143v2)。不是 arXiv 标识。lower q 有限阶与 twist ratio 有限阶不同；共振增量须另行精确比较，不自动判重复或新颖 |
| [004 MUB](../004-mub-triplets/README.md) | 已验收指定结构、字符不对称与方法边界；没有解决六维最大 MUB 问题 | 本轮未完成全方向投稿级新颖性审查，不作为已解决公开原猜想论文包 |
| [005 有向圈](../005-directed-cycle-packing/README.md) | 指定弧支配假设的反馈集障碍，而非完整 Bermond–Thomassen 猜想 | 本轮未完成全方向投稿级查重，不扩张论文承诺 |
| TF 计数与其他分支候选 | 固定 TF 模式、Bychawski 构造及尚待验收的全局渐近稿须分别判断 | 本阶段没有对未验收全局稿开论文包，也未用固定模式的复核替代普遍证明验收 |

Tang v1 已被 v2 取代。本轮读取当前 22 页稿的相关命题：基础无限乘法阶扩域在先；§9 的有限阶指 lower-algebra 参数 q。不能仅因标题都含“finite order”就将已有共振研究视为同一结果。

## 文字重复、参考文献与披露

本轮为定理、证明和文字引用的人工式 AI 阅读审查，**没有运行商业相似度数据库，不提供重复率百分比**。006 的十条参考文献已有逐项原始元数据核对；新审查再核对猜想当前版本与经典输入。主证明的支持构造、路径论证和逐例覆盖不是原论文证明的直接复制；定义、背景和标准公式仍须引用原来源。历史不可达全文不能声称已逐句排除重复。

尚未形成英文成稿的候选只有贡献定位和证据评估，不能记作通过英文／LaTeX 审查。正式稿必须区分一般书面族与固定 Lean，特别是 permutation、36 点和 lower-GP。所有“首次”“最小”“最优”“完整形式化”“外部同行评审”承诺都需对应独立证据；目前不采用未经支持的承诺。

AI 披露包括核心研究、证明推导、Lean、程序、查重、审查和论文撰写的实际辅助。作者只能是实际承担责任的人类。006 的草稿信息为 River Zhang、ORCID 0009-0004-2437-8566、Chengdu Neusoft University；这不等于人类责任审阅已完成，其他署名、实际贡献与声明及存档许可仍待确认。政策说明见 [准备报告](../PUBLICATION_READINESS.md#作者ai-披露与外部发布)。

## 有限检索的复查入口

代表查询组包括：精确论文 ID 加 `proof/counterexample/correction`；原题名加准确命题号；packing 的完整 palette、pyramid、diamond 与旧图形；`permutation digraph` 加三终端；`monophonic circulant 15` 及 v1/v2/v3；`lower general position Cartesian` 加 min、unbounded、旧 twin；Kautz 的字母表／度两种参数；Mizzi v2/v3、TF-cousin、asymmetric、odd/even；CDC 行走矩阵与 main eigenspace；Tang 当前版本。

检索前后均区分本仓库发布后的自引用命中与历史来源。引用综述、作者主页和行政 text-overlap 提示不构成完整解答或独立开放性证明。新证据可能改变归属判断，保留原公开历史和正确数学证据，并修订贡献定位。

当前最重要的文献缺口是 Fisher 的完整相关历史论文、7 点项 AJC90 的旧图例、monophonic 期刊终稿全文、Mizzi 的 1989/1997 结构文献及 001 的 Power Hadamard 全文。访问失败以缺口记录，不降低 TLS 校验或用摘要冒充全文。
