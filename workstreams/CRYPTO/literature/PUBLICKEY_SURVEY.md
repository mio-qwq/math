# 公钥与后量子密码研究机会调查（独立文献分工）

调查日：2026-10-11（Asia/Shanghai）。角色：Literature / Opportunity Agent；未执行攻击，未修改研究仓库。本文是主 Agent 汇编用的中间笔记。

## 0. 结论与证据边界

本组五个候选算法的建议顺序为：**ML-KEM 的依赖保持概率界与旋转轨道计数；ML-DSA 的拒绝采样/稀疏乘积分布；ECDSA 和 Ed25519 的精确安全模型；一般 RSA 分解**。这是面向有限 CPU、符号计算与独立复核的研究资源分配判断，不是声称前三项已找到新的开放命题。

重要的新近进展：CRYPTO 2026 已正式发表利用环结构改进 MLWE 混合攻击的工作；ML-KEM 的启发式错误事件概率在 CCS 2025 已有形式化计算证明。基础的舍入误差相关性、旋转共享预处理、Ed25519 编码差异、ECDSA nonce 关系，都不能单独登记为原创成果。[S08,S09,S12,S16,S17]

本次只能表述为“检索到并能核验的公开前沿”，不能保证已穷尽截至调查日的所有论文。新颖性检查至少仍有以下全文缺口：ePrint 2025/586 PDF 返回 403；arXiv 2609.09983 仅搜索摘要可见而全文不可取；FIPS203/204 勘误 XLSX 链接可确认但内容未解析。不能把这些标为已全文阅读、已证书复验或已数学复核。

## 1. 标准、目标与模型

| 算法 | 原始/权威规范与本次核验版本 | 正确安全问题 | 必须排除的混淆 |
|---|---|---|---|
| RSA | PKCS #1 v2.2，RFC8017（2016）；签名另见 FIPS186-5（2023）[S01,S02] | 一般均衡半素数分解；RSA inversion；具体 OAEP/PSS 方案各自模型下的安全 | 原始 textbook RSA 的可塑性、短私钥、泄漏素数位、解密 oracle 不是一般 RSA 分解；RSA inversion 与 factoring 不可直接写成已知等价 |
| ECDSA | FIPS186-5，2023-02-03；官方页 2025-05-12 列待修勘误；确定性 nonce 另见 RFC6979 [S02,S03] | 指定曲线、hash、nonce 生成与消息查询模型下的 EUF-CMA；DLP 是基础困难问题 | nonce 重用、偏置、相关性、故障、泄漏均是额外条件；标准 ECDSA 的 (r,s) 到 (r,n-s) 可塑性不等于新消息伪造 |
| Ed25519 | RFC8032（2017，Informational；非 Standards Track）；FIPS186-5；明确 SHA-512、编码与 cofactor 检查 [S02,S04] | EUF-CMA、SUF-CMA、key binding 等必须分别指定变体 | 替换 hash 为缩减轮 Ascon 的结果不攻击标准 SHA-512 Ed25519；非规范编码/弱公钥的行为须区分 honest-key 与 adversarial-key 模型 |
| ML-KEM | FIPS203 final 2024-08-13；官方页 2025-11-17 有待修勘误 [S05] | IND-CCA KEM；K-PKE 是内部 PKE，不作为独立批准算法；安全归约和诚实解封装正确性分别研究 | Kyber 各轮提交和最终 ML-KEM 不得混用；Core-SVP 指数不是实测 CPU 时间；平均正确性、每密钥正确性、适应性 δ-correctness 不等价 |
| ML-DSA | FIPS204 final 2024-08-13；官方页 2026-07-31 列若干 minor errata [S06] | 规定参数与随机预言模型下的强不可伪造、安全归约与拒绝采样条件 | 弱化/跳过拒绝采样、故障、泄漏被拒绝签名的攻击不是标准无泄漏 ML-DSA 的黑盒攻击；旧 Dilithium 参数不自动等于 ML-DSA |

ML-KEM 固定 n=256、q=3329；(k,η1,η2,du,dv) 分别为 (2,3,2,10,4)、(3,2,2,10,4)、(4,2,2,11,5)，对应类别 1/3/5。ML-DSA 固定 q=8380417、n=256；(k,l) 为 (4,4)/(6,5)/(8,7)，η 为 2/4/2，稀疏 challenge 重量 τ 为 39/49/60，对应类别 2/3/5。NIST 类别比较的是参考问题在现实计算模型下所需资源，不能统一简化为一个未经说明的“安全位数”。[S05,S06]

## 2. RSA

### 2.1 可核验前沿与资源

一般均衡 RSA 模数的经典基线仍应从 GNFS 出发，其常见启发式渐近复杂度为 L_N[1/3,(64/9)^(1/3)]。本次找到的最大公开一般形式挑战纪录为 RSA-250，829 bits，2020 年分解。作者机构说明计算约耗 2700 core-years；作者网页给原始公告、源码和复现数据。LORIA 在 2025-03 的机构文章仍称该纪录未破。2026 的作者记录页没有列更大的新一般 RSA 分解，但这不构成穷尽性世界纪录认证。[S19,S20,S21]

不可把 2048-bit N 的素数位泄漏、结构化素数、很小的 d 或已知相关消息等特殊攻击，放入无条件一般模数记录比较表。Boneh–Durfee 的低私钥指数攻击（EUROCRYPT1999 / IEEE TIT2000）是典型有条件基线；有限规模表现、代数独立性和渐近阈值的关系必须阅读原证明，不能只写 d<N^0.292 就当作所有有限密钥的严格充要条件。[S22]

### 2.2 值得但不优先的中间问题

- 对特定 Coppersmith 格族给出机器可核查的行列式/单项式选择证明，区分真正根恢复条件与仅足以得到小向量的条件。
- 推导低维格族的失败证书或确定性边界，并以已知有条件攻击为基线；如果只把已有证明转写 Lean，属于形式化/复现贡献，不能称新密码分析。
- GNFS 多项式选择与关系筛选的可证明小改进有长期价值，但首次论文需要深入数论与完整实用基准，纯 agent 短期突破机会低。

证明方向可用 1–8 CPU cores、1–16GB RAM、Sage/整数格；纪录级分解则超出当前资源。主要失败风险是发现的技巧属于已知 Coppersmith/Wiener/Boneh–Durfee 推论，或只对人工选择的弱密钥有效。

评分（重要性/原创机会/近期可验增量）**8/2/2**；一般 RSA 快速分解目标 **10/1/1**。核验难度高，真正降低一般复杂度的发表价值极高，但不能以高价值代替可行性证据。

## 3. ECDSA

### 3.1 基础安全与最新模型结果

对于约 256-bit 素数阶子群，通用离散对数算法的典型数量级是约 2^128 次群运算；这不是“ECDSA 已有无条件 128-bit 安全证明”。2016 CCS 的 GenericDSA 分析依赖理想化模型；Hartmann–Kiltz ePrint2023/914（本次元数据仍标预印本）进一步给出针对代数归约的限制：若不能编程点到 x-coordinate 模 n 的转换函数，某类安全归约受到障碍。它不是实际 ECDSA 攻击，也不是所有可能证明的不可能性。[S23,S24]

最新正式结果 Keita Emura，DCC，2026-09-06，分析 ECDSA with key recovery 的 BUFF 性质。其结果涉及地址与恢复公钥的 hash 绑定及 weak non-resignability；普通 ECDSA 缺少这些更强绑定性质，不等价于破坏通常的 EUF-CMA。论文也明确部分 adaptor signature 攻击位于被攻击论文原安全模型之外。[S25]

### 3.2 研究窗口

- 针对精确固定的签名变体，给出新安全概念之间的严格蕴含/分离和最小反例。优先可完全穷举的小群模型，随后证明如何推广；小群反例本身不等于标准曲线攻击。
- 如果研究 HNP/nonce 偏置信息，只研究自生成密钥；把数据需求、成功率、泄漏分布、格维数与实际运行记录固定。这方向很拥挤，简单相关 nonce 消元最多算 L0。
- 公钥恢复、哈希截断和 key binding 的组合可做严格理论，但必须先与 PKC2026 的 BUFF 统一框架及上述 DCC2026 工作逐项比对。[S15,S25]

资源：通常 1–8 CPU cores；证明模型反例可在秒到小时内复验，HNP 基准可能需数小时及较大 RAM。近期自主 agent 优势是枚举定义边界和检查归约条件；最大风险是换了安全模型后仍用“破解 ECDSA”叙述。评分 **7/4/4**；验证难度中高；完整、可推广的新模型定理有发表价值，普通 nonce 演示低。

## 4. Ed25519

### 4.1 先行结果与错误标题风险

RFC8032 的 Ed25519 使用 SHA-512；群中主素数阶约为 2^252，因此通用 DLP 工作量数量级为 2^126 群运算，工程上常归为约 128-bit 级别。必须区分 bit exponent 与同一成本模型。[S04]

Brendel–Cremers–Jackson–Zhao（IEEE S&P2021）已系统证明具体 Ed25519 变体的 EUF/SUF 及密钥替换相关性质，并处理编码/验证细节；Chalkias–Garillot–Nikolaenko（SSR2020）已研究多种 EdDSA 验证规则。Bellare–Davis–Di（PKC2023 的 major revision）进一步考虑 MD-style hash/SHA512 与更紧的归约；因此“首次从 Schnorr 证明 Ed25519”或“发现 cofactor 要检查”都不能登记为本项目新贡献。[S12,S13,S14]

另一个特别容易误解的标题是《Preimage-type Attacks for Reduced Ascon-Hash: Application to Ed25519》（SAC2025，版本 2026-01-14）。其 2^64 Gaussian eliminations 的 second-preimage 和 2^29.7 的 random-prefix-preimage 结果均在 **1-round Ascon-Hash256 被放入 Ed25519 的变体场景**，不是标准 Ed25519/SHA-512 被攻击。[S16]

### 4.2 研究窗口

优先研究 hash instantiation、编码等价关系、恶意公钥和多用户模型的精确组合条件；有限空间 exhaustive proof 可以很好地核查 lemma，但普通验证规则差异已经高度覆盖。可尝试提供更紧的普适归约常数或标准变体的完整形式化；如果无新定理，仅构造规范化验证器或重跑测试属于 L0。

资源：1–8 CPU cores，Python/Sage/形式证明；开发和复核主要耗在语义与证明上而非算力。评分 **7/3/5**；验证难度中；首次论文潜力中低，除非找到先行证明没有覆盖的、对真实协议安全必要的性质。

## 5. ML-KEM / Kyber

### 5.1 最强可核验公开攻击比较

Carrier–Meyer-Hilfiger–Shen–Tillich，CRYPTO2025（ePrint2022/1750 最后修订 2025-06-11）用编码理论的 dual attack 代替有争议的独立性假设；其同一 nearest-neighbor 模型的成本为：由摘要给出的基准 143/207/272 减去 3.5/11.9/12.3，可得 **139.5/195.1/259.7 bits**（这里减法为本报告计算）。这不是已执行的标准参数密钥恢复，也不把忽略内存访问代价的模型数字直接等同于现实安全失效。[S07]

最新 CRYPTO2026《Careful with the Ring!》将 MLWE 的系数等距/旋转结构用于共享预处理的 primal/dual hybrid。正式论文摘要报告：稀疏基准速度提高 17–114 倍、部分稀疏 FHE 参数约 14.2 bits 差距，但**标准 ML-KEM 的环结构贡献约 1 bit**。这些数字的模型/对象不同，不能并排当成标准 ML-KEM 的整体实测降幅。完整 Table9 未取得，故不猜其各参数最终指数。[S08]

该论文合并两个独立 ePrint：2026/279（full version a，2026-10-04 修订）与 2026/366（full version b，2026-08-30 修订并注明 Corrected Theorem3.1）。复现时应固定修订版，不应仅按 2026-02 最初摘要建基线。[S09,S10]

### 5.2 正确性与失败概率：真实缺口和已覆盖部分

FIPS203 的诚实 decapsulation failure 表为约 2^-138.8、2^-164.8、2^-174.8。不能用有限 Monte Carlo “从未失败”证明如此小概率；不能把诚实平均失败率直接带入适应性攻击者的 δ-correctness 定义。[S05]

- Fang–Wang–Zhao，ICICS2022 / ePrint2022/212 已分析固定公钥下错误非独立性及其与传统估计差异；ePrint 元数据虽然只写 preprint，但 ICICS2022 官方会议程序与 Springer 正式论文集确认发表。切勿仅根据 ePrint 标签错分发表状态。[S11]
- Almeida et al. CRYPTO2024（ePrint2024/843）的 EasyCrypt 工作覆盖 ML-KEM 的 ROM IND-CCA 归约、正确性相关定理、规格等价及 Jasmin 实现；不是证明固定 SHAKE 是理想随机预言机。[S17]
- Barbosa et al. CCS2025（ePrint2025/1562）形式化验证文献用来近似 ML-KEM 失败的统计事件上界；摘要明确其 ML-KEM 部分保留启发式近似，而 FrodoKEM 示例不需要这种近似。[S18]
- 搜索中找到 arXiv2609.09983（2026-09-09）：摘要称在显式 ROM/CBD abstraction 保留矩阵与两项 ciphertext compression 依赖，certified upper bound 2^-164.81；明确不是 exact DFR、固定 SHAKE 等价、适应性 δ-correctness 或新 IND-CCA 归约。**全文不可获取，仅列为近期必须查清的线索，未认可其证明。**[S26]

### 5.3 最适合有限资源的明确研究提案

**提案 K1：依赖保持的舍入误差联合分布。** 从 q=3329 的 Compress/Decompress 整数映射开始；先穷举 residue 级联合分布作为 L0，再寻找可推广到一般奇 q 的 exact joint law / Fourier 系数或可证总变差界，最后把它接入真实 K-PKE 噪声事件。只有证明保持所有共用变量依赖并比 S11/S18/S26 的可比界更紧、或时间/空间更少，才可能有原创价值。

**提案 K2：旋转轨道的精确成功概率。** 把 S08–S10 的共享格预处理与多个零坐标猜测事件单独抽出，研究 CBD 与固定重量分布下事件并集的精确计数或可证包络。验证可以从 n≤16 完全穷举开始，n=256 用严格 DP/系数提取。目标是替换独立性近似、避免重复计数或减少 estimators 搜索复杂度，而不是重复“旋转有用”的已发表结论。开始前必须读 S09 最新全文、S10 corrected theorem、S07 的 true/false positive 分析。

资源：离散 residue 表几 MB、秒级；联合 DP/整数卷积通常 1–16 CPU cores、1–32GB RAM，需逐步测规模；标准参数实际 lattice attacks 的高维 sieving 不适合当前算力。证明验证难度高，需第二套独立整数实现+负控制+精确 rational certificate。评分 **9/5/6**。发表潜力中高，但原创风险显著：最新论文可能已经完整覆盖；K1 的局部精确量也可能不能改善最终概率界。

## 6. ML-DSA / Dilithium

### 6.1 当前基线与撤稿陷阱

安全分析涉及 MLWE、MSIS、SelfTargetMSIS 与随机预言模型；不同基础问题之间的关系以及具体成本不能一概写成“一个格问题”。FIPS204 给三参数签名拒绝循环期望约 4.25/5.1/3.85，附录对采样循环给概率截断。这些属于已有规范内容，重新用几何/二项分布计算本身通常只有 L0 价值。[S06]

Wang–Xia–Gu《Heuristic Algorithm for Solving Restricted SVP and its Applications》（PQCrypto2025，ePrint2025/586，2025-04-29 修订）给 restricted SVP 启发式方法与 Dilithium forgery 的 gate-count estimator；摘要说与原 Core-SVP 估计匹配并结合 rescaling 得更紧估计。PDF 获取失败，所以本报告**不提供未核验的参数指数，也不称该文已实测攻破标准 ML-DSA**。[S27]

同作者部分较早工作《Revisiting the Concrete Hardness of SelfTargetMSIS in CRYSTALS-Dilithium》（ePrint2022/1601）于 **2025-04-29 withdrawn**。虽然摘要仍可读，它不能作为现行已确认定理/最佳攻击依据；撤回原因未在页面给出，本报告不推断原因。[S28]

### 6.2 中间问题与判断

- 稀疏 challenge c 乘有界秘密 s 时，系数相互依赖；对 rejection 中的联合事件给精确低维计数、解析界或有证明的 envelope，可能对 tightness/算法性能有效。需要保留 c 与 hash commitment 的依赖，不得随意把所有变量当独立均匀。
- 确认有限 attempt bound 是每个 key 的条件界还是全体 key 平均界；如果希望从平均迭代数推出统一几何尾，需额外论证条件 acceptance probability。这里只提出待审阅的问题，未声称 FIPS/论文存在错误。
- 改进求 restricted SVP 的参数优化/精确球交体积可有价值；但必须与 S27 的启发式边界区分，不能用一个低维实验拟合宣称渐近改进。

资源：计数组合/符号证明在 1–16 cores 可行；标准全维格筛超出普通环境。评分 **9/5/5**，独立核验难度高。真正统一收紧概率/归约并影响标准参数可有中高发表价值；仅测签名平均耗时或找到 rejected-loop 模拟现象价值低。

## 7. 横向评分与研究门槛

评分是基于当前明确题目、成熟先行成果覆盖、算力需求及证明复杂度的相对判断，不代表统计概率或承诺。综合排序建议采用“近期可验增量”和“原创风险”优先，不用算法知名度一票决定。

| 方向 | 重要性 | 原创机会 | 近期可验增量 | 资源/周期量级（规划假设） | 验证难度 | 第一篇论文判断 |
|---|---:|---:|---:|---|---|---|
| ML-KEM K1/K2 概率/轨道计数 | 9 | 5 | 6 | CPU 小实验，证明数天至数周；高维攻击不运行 | 高 | 本组首选；先过最新全文查重 |
| ML-DSA 联合拒绝事件/具体界 | 9 | 5 | 5 | CPU，证明与文献阅读为主 | 高 | 次选；需要清晰参数或模型增量 |
| ECDSA 模型分离/绑定性 | 7 | 4 | 4 | CPU；从小群穷举到一般证明 | 中高 | 模型必须有实际密码学意义 |
| Ed25519 具体变体形式分析 | 7 | 3 | 5 | CPU/证明器；实现小而语义繁复 | 中 | 文献成熟，易重做已知内容 |
| RSA 特定小根格族 | 8 | 2 | 2 | CPU 到高 RAM；严格边界困难 | 高 | 需真正超出已知方法 |
| 完整标准 RSA/EC 基础难题 | 10 | 1 | 1 | 现有通用攻击资源不现实 | 极高 | 作为长期目标，不占首轮主体 |

启动 K1/K2 的失败/成功门槛：先完全重建一项已发表小实例的概率/成本，在独立实现一致后冻结基线；任何新公式若被 S09/S10/S11/S18/S26 直接覆盖，归档 L0 并转向。若只改善 estimator 搜索运行时间而不改变 attack cost，结论必须写成计算工具改进而非攻击复杂度降低。

## 8. 来源台账（primary sources；访问 2026-10-11）

每项列 URL、已见状态、主 Agent 可用 ref。用于最终聊天引用时，主 Agent 应自己 open 对应 URL 后引用。

- **S01** RFC8017 / PKCS #1 v2.2：https://www.rfc-editor.org/rfc/rfc8017.html 。规范正文可检索；2016-11。refs turn15search0/4。
- **S02** FIPS186-5：https://csrc.nist.gov/pubs/fips/186-5/final 。final 2023-02-03；planning note 2025-05-12。ref turn53view3。
- **S03** RFC6979：https://www.rfc-editor.org/info/rfc6979/ 。2013-08，Informational，确定性 (EC)DSA。ref turn15search14。
- **S04** RFC8032：https://www.rfc-editor.org/info/rfc8032/ 。2017-01，Informational；全文可读。ref turn19view0。
- **S05** FIPS203：https://csrc.nist.gov/pubs/fips/203/final ；PDF https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf 。标准页和 PDF 可读；errata XLSX 未解析。refs turn13view0, turn37view3, turn40view4。
- **S06** FIPS204：https://csrc.nist.gov/pubs/fips/204/final ；PDF https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf 。标准页和 PDF 可读；errata XLSX 未解析。refs turn13view1, turn37view4, turn40view5/6。
- **S07** Carrier et al.，Assessing the Impact of a Variant of MATZOV's Dual Attack on Kyber：https://eprint.iacr.org/2022/1750 。CRYPTO2025，2025-06-11 修订；摘要明确模型与成本。ref turn45view0。
- **S08** Hou/Jiang/Ogilvie，Careful with the Ring! Concrete Hardness Gaps Between LWE and MLWE：https://link.springer.com/chapter/10.1007/978-3-032-35377-1_15 。CRYPTO2026，2026-08-09；摘要/出版页可读，正文有访问差异，未复验 Table9。refs turn45search0, turn55view0。
- **S09** Ogilvie full version (a)：https://eprint.iacr.org/2026/279 。2026-02-16 received；2026-10-04 revised，指向合并正式论文。ref turn50view0。
- **S10** Hou/Jiang full version (b)：https://eprint.iacr.org/2026/366 。2026-02-23 received；2026-08-30 修订，注明 corrected Theorem3.1。ref turn50view1。
- **S11** Fang/Wang/Zhao，Tight Analysis of Decryption Failure Probability of Kyber in Reality：https://eprint.iacr.org/2022/212 ；正式会议程序 https://icics2022.cyber.kent.ac.uk/program.php ；论文集 https://link.springer.com/book/10.1007/978-3-031-15777-6 。received2022-02-25；ICICS2022，pp148–160。refs turn13view4, turn31search9, turn31search14。
- **S12** Brendel/Cremers/Jackson/Zhao，The Provable Security of Ed25519: Theory and Practice：https://eprint.iacr.org/2020/823 。IEEE S&P2021；2020-10-14 修订。ref turn45view1。
- **S13** Chalkias/Garillot/Nikolaenko，Taming the many EdDSAs：https://eprint.iacr.org/2020/1244 ；作者出版记录 https://www.garillot.net/publication/2020-11-01-Taming-the-Many-EdDSAs 。SSR2020。refs turn45view3, turn44view1。
- **S14** Bellare/Davis/Di，Hardening Signature Schemes via Derive-then-Derandomize: Stronger Security Proofs for EdDSA：https://eprint.iacr.org/2023/298 。PKC2023 major revision，received2023-02-27。ref turn25view1。
- **S15** Struck/Weishäupl，A Framework for Advanced Signature Notions：https://eprint.iacr.org/2025/960 。PKC2026 minor revision；2026-02-27 revised。ref turn25view2。
- **S16** Nageler/Schmid/Eichlseder，Preimage-type Attacks for Reduced Ascon-Hash: Application to Ed25519：https://eprint.iacr.org/2025/1259 。SAC2025；2026-01-14 revised；DOI10.1007/978-3-032-10536-3_1。ref turn53view4。
- **S17** Almeida et al.，Formally verifying Kyber Episode V：https://eprint.iacr.org/2024/843 。CRYPTO2024 major revision；摘要描述机器验证覆盖范围。ref turn44view2。
- **S18** Barbosa/Kannwischer/Lim/Schwabe/Strub，Formally Verified Correctness Bounds for Lattice-Based Cryptography：https://eprint.iacr.org/2025/1562 ；作者全文 https://cryptojedi.org/papers/frodoec-20250831.pdf 。CCS2025；received2025-08-31。ref turn37view0。
- **S19** RSA250 作者计算记录：https://members.loria.fr/EThome/computations/ 。作者指向原始公告/复现数据；原始 Inria 邮件镜像遇 Anubis access denied。refs turn53view2, turn45view2。
- **S20** RSA250 作者机构 UCSD 公告：https://cse.ucsd.edu/about/news/new-record-set-cryptographic-challenge 。2020；829-bit 与约2700 core-years。ref turn50search23。
- **S21** LORIA2025 机构核对：https://www.loria.fr/en/2025/03/the-caramba-team-from-the-loria-has-been-awarded-the-levchin-prize-for-its-cado-nfs-software/ 。截至该文称 RSA240/250 纪录仍在；不能替代 2026-10 的全球穷举核查。ref turn50search3。
- **S22** Boneh/Durfee 作者论文页：https://crypto.stanford.edu/~dabo/pubs/abstracts/lowRSAexp.html 。Cryptanalysis of RSA with private key d less than N^0.292，EUROCRYPT1999/TIT2000。ref turn57search1。
- **S23** Fersch/Kiltz/Poettering，On the Provable Security of (EC)DSA Signatures：https://doi.org/10.1145/2976749.2978413 。CCS2016；模型限制明确。refs turn25search1, turn28search5。
- **S24** Hartmann/Kiltz，Limits in the Provable Security of ECDSA Signatures：https://eprint.iacr.org/2023/914 。received2023-06-12；元数据 Preprint。ref turn37view1。
- **S25** Emura，On the BUFF security of ECDSA with key recovery：https://link.springer.com/article/10.1007/s10623-026-01942-7 。DCC94:197，2026-09-06。ref turn50view2。
- **S26** Duriez/Tommasini，Dependency-Aware ROM/CBD Correctness Bounds for ML-KEM-768 at the Heuristic Failure Scale：https://arxiv.org/abs/2609.09983 。搜索元数据2026-09-09，预印本线索；abs/html 被工具拒取，仅摘要已见，证明与附件未验证。ref turn19academia25。
- **S27** Wang/Xia/Gu，Heuristic Algorithm for Solving Restricted SVP and its Applications：https://eprint.iacr.org/2025/586 。PQCrypto2025；received2025-04-01、revised2025-04-29。摘要已读；PDF403。refs turn13view3, turn53view0。
- **S28** Wang et al.，Revisiting the Concrete Hardness of SelfTargetMSIS in CRYSTALS-Dilithium：https://eprint.iacr.org/2022/1601 。**2025-04-29 withdrawn**；不当作已确认结果。ref turn13view2。
- **S29** PQShield 受托 ML-KEM 评价报告：https://pqshield.com/wp-content/uploads/2026/03/cryptrec-ex-3502-2025.pdf 。2025年度报告，2026公开；用来核对已有 cost-model 基线，不能覆盖之后 CRYPTO2026 新进展。ref turn31view0。其 Table6 的 MATZOV/GSA dual-hybrid 模型数为139.7/196.4/262.3，区别于 S07 的改进。Core-SVP 省去多项式因素和内存费用；不作实际攻击实绩。

## 9. 检索记录与待续

采用 system2 搜索常规规范/标题；system1 加 recency 核验近期结果与官方版本。代表性检索词：RSA factoring record RSA250 RSA260 2026；ECDSA provable security 2025 2026；Ed25519 tight proof；Kyber decryption failure probability rigorous；ML-KEM concrete security；Dilithium rejection sampling；Careful with the Ring MLWE。搜索中第三方博客/镜像仅当线索，不用作密码学结论证据。

优先待续：取 S09 2026-10-04 PDF、S10 corrected theorem 和代码；取 S26 正文与证书并核实其正式 arXiv 元数据；阅读 FIPS203/204 实际勘误；若转选 ML-DSA，优先解决 S27 全文缺口。当前尚无本组自有 L1/L2 原创成果，全部调查属于 L0。
