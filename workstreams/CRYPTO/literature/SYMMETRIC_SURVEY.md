# 对称密码与 ARX 自动化：研究机会调查笔记

调查日期：2026-10-11（中国时间）。调查者：分工文献 Agent `survey_symmetric`。本文件属于选题前调查，不代表完成攻击复现、数学独立验证或原创性认定。只列可以从原始论文、作者维护页面、官方规范核验的结论；数字缺项保留为未确认。

## 1. 决策摘要

**建议第一项工作：ChaCha 局部结构的精确、有符号相关计算与独立性适用条件审计。** 成功标准应是可验证的公式、可复核的计数证书、已发表局部估计的准确适用条件，或同模型下明确减少计算成本的算法。实现一个普通的 carry 动态规划、发现“连续模加不独立”、重新生成 DDT，都只能先列为 L0。

选择依据有三项：

1. 2022 年已经有专门研究连续模加非独立性及 SAT/#SAT 的论文，说明问题真实存在，但最直接的现象不是新贡献。[ARX2]
2. 2025 年 ToSC 已刊登对 Ascon、ChaCha、Serpent 若干已发表攻击的纠错研究，显示误差控制和模型适用条件具有学术价值；但其已指出的错误不能重复认领。[CORR]
3. 2026-10-09 的 ChaCha 原始论文明确区分截断 path cluster 与未控制的尾项，并把跨加法 carry 依赖、有符号路径求和列为后续方向。其计算依赖大量 GPU 样本，因此一个严格而便宜的局部计算方法有动机；不能据此直接保证存在新的算法。[CH26]

AES 主线适合长期投入；目前快速可验证的实验多处于成熟技术拥挤区域。Ascon 的自动化界限值得作为第二选项，尤其是带可检查不可满足证书的下界，但 2024/2025 已有桌面级 SAT/MILP 改进，单纯替换求解器不算新方法。

## 2. 评分原则与排序

评分是研究资源分配判断，**不是统计成功概率**。重要性来自标准地位及能否影响通用方法；原创机会来自已核文献留下的明确缺口、竞争拥挤程度；近期可行性以本地 CPU、Python/C++、SAT/SMT 为假设。综合参考分 = 0.35×重要性 + 0.30×原创机会 + 0.35×近期可行性，资源和复核难度另列。

| 方向 | 重要性 | 原创机会 | 近期可行性 | 综合 | 资源 / 证明难度 | 潜在发表价值与主要失败风险 |
|---|---:|---:|---:|---:|---|---|
| ChaCha 2/3 次模加局部有符号相关与条件分布 | 9 | 5 | 8 | 7.45 | 小字长穷举、整数 DP、SMT；证明中等，查重较难 | 若给严格新条件或复杂度改进可有方法论文价值；风险是已被 2025/2026 局部公式覆盖 |
| Ascon 差分/线性 trail 下界和证书 | 9 | 4 | 6 | 6.45 | CPU+SAT/MILP；求解时间不可预测，完备性证明较难 | 真正收紧标准宽度界限可发表；风险是只有同界限新实现 |
| ChaCha 全局 DL hull 尾项界 | 9 | 6 | 3 | 6.00 | 张量/谱/概率论 + 局部精确算子；数学难 | 若产生有用而严格界价值高；风险是三角界太松、局部截断无法外推 |
| Ascon 模式安全界、key commitment | 8 | 4 | 4 | 5.40 | 主要理论、有限参数反例搜索；证明难 | 参数边界反例可能有价值；已有 SoK 和 2026 新论文，重复风险大 |
| AES-128 缩减轮 DS-MitM / S-box 结构 | 10 | 3 | 3 | 5.45 | GF(256)、组合结构、成本审计；复核难 | 具体表大小/数据/在线离线改进有价值；2026 cross-ratio 正占据近邻空间 |
| AES-256 缩减轮 DS-MitM / related-key 兼容性 | 10 | 3 | 2 | 5.10 | 同上，附密钥扩展约束；复核很难 | 高价值但不适合短周期主攻；风险是弱模型或漏记指数级内存 |
| 完整标准 ChaCha20 / AES 单密钥实质攻击 | 10 | 1 | 1 | 4.15 | 未有可执行突破方法；当前资源不够 | 长期大目标；作为当前实验目标会导致无信息暴力搜索 |

## 3. AES：规范、模型和近期可核验结果

### 3.1 规范与安全模型

FIPS 197 的 2023 更新明确没有修改算法。AES 块长始终为 128 bit；128/192/256 bit 密钥对应 10/12/14 轮。调查必须分开：单密钥未知密钥恢复、related-key、chosen-key、已知/可选密钥区分器、基于 AES 的哈希压缩模式、量子查询模型。chosen-key 全轮区分器不能表述为常规 AES 密钥恢复。[AESSTD]

### 3.2 2026 年受限数据 DS-MitM 结果

Bao–Guo–List–Wang，*New Records for Practical-data Chosen-plaintext Attacks on Round-reduced AES*，IACR Communications in Cryptology 2(4)，**正式发表 2026-01-08**，全文与表 1 已读取。[AES26]

表内复杂度以 2 的指数记。在线/离线的 encryption equivalents 和巨大表的 memory accesses 必须分开，不能只报较小的 encryption 数字：

| 参数 | 在线加密等价 | 在线内存访问 | 离线加密等价 | 离线内存访问 | 选择明文数 | 内存（128-bit state 等价） |
|---|---:|---:|---:|---:|---:|---:|
| AES-128，7 轮 | 112.7 | 117 | 113.9 | 117 | 44 | 116.8 |
| AES-192，8 轮 | 173.8 | 176 | 160.3 | 161 | 40 | 160.8 |
| AES-256，9 轮 | 230.7 | 232 | 240.1 | 240 | 48 | 241.5 |

该论文的“practical-data”阈值为最多 2^48 选择明文，**不意味着攻击整体可实际执行**。表中没有可直接转录的统一成功率，所以本调查未补写。此处仅为该明确模型的近期可核验参照，不宣称所有 AES 模型的全球最佳。

### 3.3 更近的预印本与查重阻断

*The Cross-ratio Property and Its Use for Cryptanalysis of Round-reduced AES*，ePrint 2026/1549，2026-07-29 收稿；ePrint 当前仍标 Preprint。作者主页列入 ASIACRYPT 2026，调查日期早于会议，写作时应标“预印本；作者列为 ASIACRYPT 2026”，不可写已开会发表。其摘要研究 key-wrapped GF(256) inverse 的 quartet cross-ratio、7 轮 AES-128 DS-MitM、3/4 轮低数据区分。**全文访问失败，未抄具体指数**。[AESCR]

*Chosen-Key Distinguishing Attacks on Full AES-192, AES-256, Kiasu-BC, and More*，ePrint 2023/1095，正式版本 ToSC 2025(3)，研究相关密钥差分存在性和 chosen-key 区分；其 CP + triangulation 已针对虚假 related-key trail 做验证。仅仅验证一个 related-key trail 存在密钥对，或指出局部兼容并不保证全局兼容，已经有很近先行工作。[AESCK]

### 3.4 可执行中间问题

- 从一个已发表 DS-MitM 子结构开始，对假阳性多重集概率或字节约束秩做独立精确计数；要求改进与 2024 *Accurate False-Positive Probability of Multiset-Based Demirci-Selçuk Meet-in-the-Middle Attacks* 比较，避免重复。
- 研究 quartet 多条件同时成立时的 GF(256) 计数，先对 256 元域穷举检验，再证明；在 cross-ratio 全文缺失时任何同类结果的 novelty 均不能通过。
- 长期可做“可检查的 related-key 差分兼容性证书”，但工具层贡献需要性能或新界限支撑。

## 4. ChaCha：近期基线及明确未解决的计算目标

### 4.1 标准参数

IETF RFC 8439 规定 ChaCha20 使用 256-bit key、96-bit nonce、32-bit counter；16 个 32-bit word，20 轮和 feed-forward。RFC 为 Informational，不应误标为 NIST 标准。原始 ChaCha 128-bit key 和 64-bit nonce 配置、裸 permutation 与最终 stream cipher 都必须单列。[CHSTD]

### 4.2 不要引用已被纠正的“最好攻击”

Tezcan–Leander–Hadipour，*Cryptanalysis: Theory Versus Practice: Correcting Cryptanalysis Results on Ascon, ChaCha, and Serpent Using GPUs*，ToSC 2025(3):729–754，正式全文可读。它否定的是特定 WGM24 / OWGM25 7/7.5 轮 ChaCha DL 分析，以及特定 Ascon 4.5/6 轮结果；**不是所有 7 轮攻击**。其分析尤其指出把不同密钥下不足样本的绝对/中位偏差混合并不能证明单密钥微弱 bias。本文原文、明确被否定对象及作者代码已经存在，复现属于 L0。[CORR]

### 4.3 2026-10-09 可读全文：path cluster，不是精确全 hull

Liu–Ren–Sun–Yu–Li，*Differential-linear cryptanalysis against ChaCha based on automated tools*，Cybersecurity 9:228，正式发表 **2026-10-09**，HTML 全文与补充材料目录可读。[CH26]

| 作者报告的实例 | 数据复杂度 | 时间复杂度 | 准确状态 |
|---|---:|---:|---|
| 7 轮 DL 区分 | 2^160.20 | 此处不另推时间 | 截断主路径相关估计，附既有扩展假设 |
| 7.5 轮 DL 区分 | 2^245.00 | 此处不另推时间 | 同上，不能理解为一个密钥可取得这么多唯一标准输入 |
| 7 轮 ReBitP 密钥恢复 | 2^125.91 | 2^140.00 | 将新局部数值代入既有攻击资源公式 |
| 7.5 轮 ReBitP 密钥恢复 | 2^122.96 | 2^241.31 | 同上 |

关键是作者在式 (3) 明确写 `C_full = C_{≤14} + R_{>14}`，本次计算控制的是前者，尾项仍为后续目标。其主路径总和约 2^-31.16 不能作为已证明全相关。这个事实比指数排名更影响我们的选题。

更低数据的候选：Paul–Kundu–Chakrabarti ePrint 2025/1830，2026-05-05 修订，仍为**预印本**。摘要确认 7 轮时间 2^167.90，并声称改善 7.5 轮。CH26 比较表转录 7.5 轮 T=2^237.41、D=2^53.41，但完整攻击成功概率未直接可比；本调查尚未访问此项 PDF，因此这些数值只列“他文转录、待原文核对”，不得取代已核基线。[CHPNB]

### 4.4 两个必须补齐的最近先行工作

1. Okada–Nagai–Miyaji，*Refined Linear Approximations for ARX Ciphers and Their Application to ChaCha*，INDOCRYPT 2025，Springer 首次上线 2025-12-11，书目年份 2026，DOI 10.1007/978-3-032-13301-4_4。其研究内容直接包括三独立变量上的两次连续模加、精确线性近似概率。ePrint 2025/2128 在 2025-11-23 withdrawn，但页面说明正式版本在 INDOCRYPT；**不能把这个标签解释成学术结论被撤销**。目前仅摘要与元数据可得，正式全文有订阅墙，是原创性审查实质缺口。[CHREF]
2. Li 等，*New Derivation Rule for Linear Approximations and Its Application to ChaCha*，ICISC 2025，DOI 10.1007/978-981-95-8034-7_25，出版社页面可访问。全文尚未取得，应列为同类方法的查重阻断项。[CHDER]

## 5. Ascon：标准差异与机会

### 5.1 必须区分版本

SP 800-232 于 2025-08-13 定稿，包括 Ascon-AEAD128、Ascon-Hash256、Ascon-XOF128、Ascon-CXOF128。官方实现明确说明标准版本由大端切换为小端、IV 更新；标准 AEAD128 源自 Ascon-128a，而不是原 Ascon-128。标准模式调用 p[12] 与 p[8]。旧版论文的位位置、IV、padding 和缩减初始化/中间/终结轮数都要显式转换与验证。[ASSTD][ASCODE]

### 5.2 原始论文参照，不能把 free-start 碰撞当标准哈希碰撞

Fu 等，*Preimage and collision attacks on reduced Ascon using algebraic strategies*，Cybersecurity 8:34，正式发表 2025-05-24，全文可读。研究旧版 Ascon：2 轮 XOF-64 原像时间 2^33、2 轮 XOF-128 原像 2^97；3/4/5 轮 Ascon-HASH 的 **free-start** 碰撞时间分别 2^14 / 2^18 / 2^41。这些不是 12 轮标准 Hash256 碰撞。摘要与表 1 的“最好”限定于其模型与当时文献，调查未据此宣称 2026 全球最佳。[ASALG]

Degré–Derbez–Lahaye–Schrottenloher，*New models for the cryptanalysis of ASCON*：ePrint 2024/298 仍显示 Preprint，但出版社有 **Designs, Codes and Cryptography 正式 2025 版本** DOI 10.1007/s10623-025-01572-5。SAT 替代 MITM MILP、降低内存及证明模型内最优，另有 Hamming-weight lossy MILP 与 7 轮下界改善。全文 PDF 本次取回失败；未自行补写具体下界数字。[ASMODEL]

作者维护 Ascon publications 页面还列有完整轮的 non-black-box zero-sum、7 轮 cube、6 轮 trail 概率上界等不同模型。该列表存在诸如“128-bit 变体对应 2^159.97 keys”的可疑摘要字段，因此不得直接抄为已核结论，必须回原论文检查变体。

### 5.3 可执行中间问题

- 对 5-bit S-box / 2 轮结构构造整数精确 differential-linear table，并按等价关系压缩；只有得到新完备分类、可证明复杂度下降或新轮界才升 L2。
- 复现一个现有 Ascon trail 下界，产出能被另一工具检查的 UNSAT 证书；以标准宽度和相同轮边界收紧界限为成功指标。
- 研究标准版和旧版的结构结果能否经显式位重标记转移。仅“改 IV / 大小端后跑通”不是密码分析突破。
- 模式界限、key commitment 是长期方向。已发现 CRYPTO 2026 *Generic Committing Attacks: Zero-Padded Ascon is Less Secure than Expected*；作者机构与主页确认存在，但全文未核，不能把零填充 security proof 缺陷再当新发现。[ASCOM]

## 6. 首轮研究的严格、可执行任务单

### 6.1 模型层次

定义相关始终采用有符号量 `Cor(f,g)=E[(-1)^(f(x) xor g(x))]`；bias 若用 `Pr[f=g]-1/2` 则等于 Cor/2。报告必须注明 convention，不得把 1/bias^2 和 1/Cor^2 的常数混淆。

第一层 L0 基线：独立均匀 n-bit 变量上的链 `u=x+y mod 2^n, v=u+z mod 2^n`。计算任意输入/输出线性掩码的精确有符号相关，并与直接全枚举核对。这一整类很可能被既有自动机或 [CHREF] 覆盖；**先作为 oracle，不认领新定理**。

第二层：ChaCha 半个 quarter-round，显式写成

```
s = a + b mod 2^n
t = rotl(d xor s, r)
u = c + t mod 2^n
v = rotl(b xor u, q)
```

先研究 fresh uniform `a,b,c,d`，再单独研究固定 `a`（标准首次列轮为常数）的分布。不能默认从均匀状态推得固定常量首轮性质。两次加法有 fresh input 时某些独立性可能恰好成立，应尝试证明适用条件，而不是预先假定一定存在偏差。

第三层：接入 ChaCha 第三次加法 `w=s+v mod 2^n`。它重复使用前面生成的 `s` 与由 `b,u` 生成的 `v`，此处是具体的跨加法依赖研究对象。目标是在同一掩码、同一输入分布下比较真实有符号相关与局部乘积；输出严格的相等条件、不等式或反例族。

标准 ChaCha 用 n=32、r=16、q=12。小字长实验必须注明 `r mod n` / `q mod n` 或另选旋转常数；由于 n=4/8 会让一些标准旋转退化为 0，不可把退化 toy 现象当成标准参数证据。先对 n=4/5/6 穷举，再考虑 n=8/16/32 的 DP / SAT，成功才外推。

### 6.2 真正可能有贡献的目标

- **必要条件/充分条件**：明确何种输入分布与 mask 支持使局部加法 correlation 相乘恰好正确；对失效的最小依赖结构给闭式 family。
- **可证实算法改进**：按 carry 边界状态做精确有符号计数，以记忆状态数、位宽 n、旋转距离为参数给复杂度；必须和 Nyberg–Wallén、Lipmaa–Moriai、Qin–Wu、Okada 等比较。通用 variable elimination/weighted automaton 应注明为既有技术。
- **全 hull 截断的可用尾界**：对一个具体小结构输出 `C_partial` 与严格 `|R|≤B`，检验 B 是否小到可以判定符号或改进安全估计。一般性的三角不等式本身不新，若界太松应记录失败，不宣称攻击。
- **证书**：精确计数分母统一为 2^(变量位数)，保留带符号整数分子、mask 和变体；另一实现直接枚举或 SMT 检查。

### 6.3 停止/转向条件

- 若仅复现两次模加公式，归为 L0，并把焦点移到第三加法与标准固定常量。
- 若正式全文缺失，允许继续建立基线，但 novelty 保持 unresolved，不写首创。
- 若旋转使 DP 状态爆炸而没有参数改善，不运行无界暴力；转向可证明的 cutwidth / 状态上界或更局部命题。
- 若得到反例只是 toy rotation=0 退化，不能外推；改用非退化 toy 与标准位宽精确样本。

## 7. 原创性最邻近文献清单

| ID | 来源 / 日期 / 状态 | 直接覆盖内容与本次访问情况 |
|---|---|---|
| ARX1 | Lipmaa–Moriai, *Efficient Algorithms for Computing Differential Properties of Addition*, FSE 2001（出版 2002）；https://eprint.iacr.org/2001/001 | 单次模加差分概率高效计算；ePrint 元数据、PDF 搜索结果可得。不是本项目的新结论。 |
| ARX2 | Qin–Wu, *Towards non-independence of modular additions in searching differential trails of ARX ciphers…*, 2022-03-18；https://arxiv.org/abs/2203.09741 | 54 页全文可读；连续模加差分方程、SAT 验证、#SAT/GANAK 精确概率、SPECK/Chaskey。arXiv 页面未确认后续正式发表状态。 |
| ARX3 | Biryukov–Lambin–Udovenko, *Exact Formula for RX-Differential Probability through Modular Addition for All Rotations*, ToSC 2025(1):542–591；https://eprint.iacr.org/2025/550 | 任意旋转单次模加 RX 精确公式；作者代码 https://github.com/cryptolu/RX-Differentials-Probability 。本次主要核元数据和摘要。 |
| CHREF | Okada–Nagai–Miyaji，INDOCRYPT2025；https://doi.org/10.1007/978-3-032-13301-4_4 | 两次模加/三独立变量精确线性近似；正式全文未取得。ePrint withdrawal 是版本状态，不能解释为结论被否定。 |
| CHDER | *New Derivation Rule for Linear Approximations and Its Application to ChaCha*, ICISC2025；https://doi.org/10.1007/978-981-95-8034-7_25 | 最近线性推导规则；出版社元数据可得，全文缺口。 |
| CORR | Tezcan–Leander–Hadipour，ToSC2025(3)，https://doi.org/10.46586/tosc.v2025.i3.729-754 | 作者机构存档全文 https://research.sabanciuniv.edu/53021/1/Cryptanalysis.pdf 已核；特定已发表攻击纠错。 |
| CH26 | Liu et al., 2026-10-09；https://doi.org/10.1186/s42400-026-00671-7 | 最新可读 path-cluster / MIQCP 对照；尾项未控制。不可将局部数值自动升为完整攻击证明。 |
| CHPNB | Paul et al., ePrint2025/1830，2026-05-05 修订；https://eprint.iacr.org/2025/1830 | 预印本、PNB 集合构造；本次只有元数据及摘要。 |
| AES26 | Bao et al., CiC 2026-01-08；https://cic.iacr.org/p/2/4/38 | https://cic.iacr.org/p/2/4/38/pdf 全文表1已核。 |
| AESCR | Bao et al., ePrint2026/1549；https://eprint.iacr.org/2026/1549 | cross-ratio / quartet / AES inverse；全文缺口，作者主页列 ASIACRYPT2026。 |
| AESCK | Dong et al., ToSC2025(3)；https://eprint.iacr.org/2023/1095 | CP+triangulation / chosen-key；摘要与正式发表元数据已核。 |
| ASMODEL | Degré et al., DCC2025；https://doi.org/10.1007/s10623-025-01572-5 | SAT/MILP Ascon；正式页面已核，ePrint 元数据落后，全文未取得。 |
| ASALG | Fu et al., Cybersecurity 2025-05-24；https://doi.org/10.1186/s42400-024-00340-7 | 2 轮原像、3–5 轮 free-start 碰撞；HTML 全文可读。 |
| ASCOM | Datta–Nandi–Pal–Sasaki–Struck–Weishäupl，CRYPTO2026；https://www.ccs.uni-konstanz.de/research/publications/ | 零填充 commitment 泛型攻击；只核作者机构发表记录，全文及精确参数待核。 |

规范来源：

- [AESSTD] https://csrc.nist.gov/pubs/fips/197/final 与 https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
- [CHSTD] https://www.rfc-editor.org/rfc/rfc8439
- [ASSTD] https://csrc.nist.gov/pubs/sp/800/232/final 与 https://ascon.isec.tugraz.at/specification.html
- [ASCODE] https://github.com/ascon/ascon-c
