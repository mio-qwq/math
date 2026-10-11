# 原创性审查：第一阶段与主线选择

日期2026-10-11。等级：L0。判定对象是研究选题，不是已产生的新攻击。

## 已确认的近邻覆盖

| 研究 | 日期/状态 | 已覆盖内容 | 对本工作的约束 |
| --- | --- | --- | --- |
| Lipmaa–Moriai，Efficient Algorithms for Computing Differential Properties of Addition | FSE2001，出版2002；https://eprint.iacr.org/2001/001 | 单模加差分精确公式 | 普通公式/代码只能复现 |
| Mouha等，The Differential Analysis of S-functions | SAC2010作者稿；https://lirias.kuleuven.be/retrieve/0b5465ef-3483-4d2e-9f8f-a697d2107822 | 有限状态/矩阵精确差分计算 | 普通状态DP不是新范式 |
| Bellini等，Finding differential trails on ChaCha by means of state functions | 正式元数据进一步核对；https://iris.polito.it/retrieve/handle/11583/2987931/707706 | half-quarter XDP/ADP、quarter独立性启发式及小字长比较 | 半轮精确DP和toy非独立现象已有覆盖；作者表需含正式版Grados |
| Qin–Wu，Towards non-independence of modular additions… | arXiv2203.09741，2022-03-18；https://arxiv.org/abs/2203.09741 | 连续模加SAT/#SAT与精确概率 | “加法不独立”不是新结论 |
| Tezcan–Leander–Hadipour，Cryptanalysis: Theory Versus Practice | ToSC2025(3):729–754；https://research.sabanciuniv.edu/53021/1/Cryptanalysis.pdf | 特定Ascon/ChaCha/Serpent结果纠错 | 已点名错误不能再次认领 |
| Okada–Nagai–Miyaji，Refined Linear Approximations… | INDOCRYPT2025；https://doi.org/10.1007/978-3-032-13301-4_4 | 两次模加精确线性近似 | 正式全文未得；ePrint撤回不等于结论撤销 |
| Li等，New Derivation Rule for Linear Approximations… | ICISC2025，2026出版；https://doi.org/10.1007/978-981-95-8034-7_25 | 新线性推导规则 | 全文缺口阻止直接认新 |
| Liu等，Differential-linear cryptanalysis against ChaCha based on automated tools | Cybersecurity，2026-10-09；https://doi.org/10.1186/s42400-026-00671-7 | 有符号路径簇与跨加法模型误差 | 局部精确算子须具体比较；未受控全尾项不是已闭合问题 |

## 当前判断

一般精确计数、普通相关性反例与常量模加建模高度可能已有直接覆盖。选择三加法输出与XOR线性化的特定相关，目的是用最小可核验问题检验能否得到超出基线的结构。

目前新贡献：**无已审定项**。尚未证明的候选不计研究等级。即使写出正确闭式，仍须对近期两模加/ChaCha线性近似论文排除直接特例或等价变形。未搜索到不等于首次。

## 第二级与第三级

具体项目必须另有NOVELTY_REVIEW.md，逐条列命题、模型和与最邻近3–10项研究的差异。成果后由未参与发现的Literature Agent主动寻找先行覆盖。论文前最终审查尚未开始，不预填通过。

## 2026-10-11 第二级已执行的裁决

[ChaCha项目审查](projects/chacha-three-add/NOVELTY_REVIEW.md)已由未参与发现/程序验证的Literature Agent完成，列十组最接近文献，结论为**原创性未通过**。均匀特殊位的M0是旧三字加法相关；额外masked moments等价旧多输入模加问题的具体mask；一般四状态方法是既有范式。旋转消去、固定字完整符号分类及后续闭式是否有独立可发表贡献仍须逐条比较，不能因得到标准字宽精确分数而授予L2。

已取得关键2021、2022和2026作者/公开出版文本；Okada2025、最近Li规则等仍有全文缺口。当前不存在已审定原创贡献，也未证实任何公开最佳攻击复杂度改进。第三次投稿前审查未启动；没有投稿对象需要批准。

## 同日补充：从方法相似到具体重构

[METHOD_COMPARISON.md](projects/chacha-three-add/literature/METHOD_COMPARISON.md)已逐项写出普通两进位矩阵、特征行向量和带掩码乘积，直接重构特殊位与重叠上位的关键矩。它还给出同一任意位目标的可逆前缀O(n)算术构造，后续实现已匹配1650个精确值。由此排除了“新的四状态方法”“新的谱技术”及“以O(n²)逐矩重算作为最好基线”的表述。

尚未历史排除的最小候选是具体quarterround第一输出的旋转消去、稀疏支持与权重以及固定首字的统一符号分类。这些结论目前只有应用级价值候选，没有新攻击。固定a,b,c、仅d均匀的有界评估现已完成独立验证与八组近邻比较，确为直接常量核应用，已归L0并停止扩张。

## 同日转向：近期Keccak先行收窄新目标

[Keccak近期审查](projects/keccak-conditional-rank/RECENT_LITERATURE.md)确认SAC2026工作已联合优化秩、局部密度和自由度，给出投影重数公式、调和平均校正并精确枚举单纤维；直接优化有效自由度本身也是作者公开开放问题。一般二阶矩和核方向自相关只是初等直接推论。当前仅保留同一Table6实例的非平凡全局投影计数界候选，尚无新算法、实验或原创性通过结论。
