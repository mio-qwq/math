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
