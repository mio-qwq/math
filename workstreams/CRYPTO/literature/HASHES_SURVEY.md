# 密码学哈希研究机会调查：SHA-2、SHA-3、BLAKE、SHA-1

调查日期：2026-10-11（Asia/Shanghai）。执行角色：独立 Hash Literature / Opportunity Agent。仅为主 Agent 提供调查草稿，不是论文、攻击公告或同行评议。

## 0. 结论与可信边界

本次覆盖六个候选：SHA-256、SHA-512、SHA-3/Keccak、BLAKE2、BLAKE3、SHA-1。现有资料足以排除“复现低轮差分或用 SAT 找一个碰撞即可宣布原创”的做法。尤其 SHA-2 在 2026 年已有新纪录：不能继续将 31 步碰撞或 39 步半自由起点碰撞当作现行最优标准碰撞纪录。

在本组算法中，首项探索建议是 **BLAKE3 合法初始状态/消息约束下，短轮 ARX 差分路径的精确联合概率、可实现性与可核验界**；并将 **Keccak/SHA-3 条件线性结构及 SAT 连接阶段的可证明剪枝**列为同等级备选。这个选择是关于可处理的中间问题，不是判断完整 BLAKE3 比 SHA-256 容易攻破。若只得到普通模加差分公式、路径概率不能相乘的例子、或已有方法的换语言实现，必须降级 L0。

调查没有穷尽所有新预印本、学位论文、论文修订及开放挑战提交。多个 IACR PDF 请求返回 403；相应条目只核验了原始摘要、元数据或出版商摘要，没有把未获取全文的细节补成事实。所有“作者报告的复杂度/实例”均未在本轮重新执行，不能标作本项目验证。对各模型的当前最好结果，以下采用“本次找到并核验的强基线”，不是数学上的穷尽声明。

## 1. 标准对象与安全目标

| 候选 | 固定研究对象 | 规范来源 | 需要保持的边界 |
|---|---|---|---|
| SHA-256 | 32-bit word，64 步，256-bit digest，512-bit block | NIST FIPS 180-4 [H01] | 固定标准 IV 与填充；压缩函数/完整哈希分别建模；普通碰撞与 SFS/FS 分开 |
| SHA-512 | 64-bit word，80 步，512-bit digest，1024-bit block | NIST FIPS 180-4 [H01] | 不把 SHA-512/224、SHA-512/256、截断输出或自由 IV 结果混入 |
| SHA-3/Keccak | FIPS 202 的 SHA3-224/256/384/512、SHAKE128/256；标准置换宽度 1600，24 轮 | NIST FIPS 202 [H02] | 原始 Keccak 与 FIPS 202 的域分隔不同；c、r、输出长度、轮编号必须固定；小宽度 Crunchy 实例单列 |
| BLAKE2 | BLAKE2s：32-bit/10 轮；BLAKE2b：64-bit/12 轮；各有参数化输出长度 | RFC 7693（Informational）[H03] | RFC 不是 NIST 标准；keyed permutation、compression function、完整 hash/MAC 分开 |
| BLAKE3 | 32-bit/7 轮；默认 256-bit 输出；树结构、hash/keyed_hash/derive_key/XOF | 设计者规范 [H04]、C2SP 规范 [H05] | 规范目标为至少 128-bit 安全；256-bit 默认输出不能直接写成所有属性均承诺 256-bit；保留 IV、flags、counter、block length、树节点约束 |
| SHA-1 | 80 步，160-bit digest，512-bit block | NIST FIPS 180-4 [H01] | 完整碰撞已破； chosen-prefix、identical-prefix、任意原像和第二原像是不同问题 |

对 n-bit 普通哈希的经典通用基线，碰撞约为 2^(n/2)、原像约为 2^n；这是比较模型的背景量级，而非对具体标准的已证明下界。SHAKE 还须记录 capacity 与输出长度带来的约束；BLAKE3 则按其明确的 128-bit 目标评价。NIST 页面仍列出 FIPS 180-4（2015）与 FIPS 202（2015），分别记录 2023、2025 的修订/更新计划；不能把计划当成新规范已经颁布。[H01,H02]

## 2. 本次核验的公开攻击基线

### 2.1 SHA-256

| 来源 | 日期/状态 | 模型和结果 | 本次核验程度 |
|---|---|---|---|
| [H06] | ePrint received 2026-06-01；最后修订 2026-09-09；Preprint | 普通碰撞：38/64 步，时间 2^104.3、内存 negligible；36 步时间 2^57，并报告给出碰撞消息对；同法未得到有效 39 步 SHA-256 攻击 | 原始摘要、日期、状态；PDF 未取得；未重新检查消息对 |
| [H07] | received 2026-05-28；CRYPTO 2026 minor revision | 普通碰撞：SHA-256 与 SHA-512 均达到实际 35 步；36/37 步理论攻击；其 38 步尝试受未控制部分概率限制 | 原始摘要与发表元数据 |
| [H08] | received 2026-02-12；EUROCRYPT 2026 minor revision | 普通 SHA-256 碰撞到 37 步；自动 local-collision 搜索及 Boolean 条件模型改进 | 原始摘要；该版本时间/空间数值未确认 |
| [H09] | received 2024-02-27；EUROCRYPT 2024 minor revision | 39 步 **SFS** SHA-256 的实际消息对。它与上方标准 IV 碰撞的 38 步并不矛盾 | 原始摘要；是较弱 IV 模型 |
| [H10] | FSE 2012，论文预印本最初 2011-06-03 | 45 步普通原像时间 2^255.5、内存约 2^6；52 步 **pseudo-preimage** 时间 2^255 | 已取得作者学校版论文及 IACR 演讲表格，明确区分两类 |
| [H11] | arXiv 2024-06-28 | 程序化 SAT+CAS 达到 38 步 **修改 IV** 的碰撞复现；纯 SAT 对照不超过 28 步 | 原始论文摘要；不是新标准 SHA-256 碰撞纪录 |

关键查重结论：SAT/SMT 路径搜索、布尔位条件捕捉、局部碰撞自动化和内存高效 MitM 已有很新的竞争性工作。潜在新结果必须相对于 2026 年模型比对，而非只对 2013/2024 模型。完整 64 步标准 SHA-256 普通碰撞/原像的重大突破，不是上述结果的含义。

### 2.2 SHA-512

| 来源 | 日期/状态 | 模型和结果 | 本次核验程度 |
|---|---|---|---|
| [H06] | 2026-09-09 修订的预印本 | 普通碰撞：38/80 步 2^125.4；39/80 步 2^178；内存均报告 negligible | 原始摘要，未取得全文/独立复现 |
| [H07] | CRYPTO 2026 | 35 步实际碰撞；36/37 步理论碰撞 | 原始摘要 |
| [H12] | CRYPTO 2025，2025-08-17 online | 29 步实际碰撞；31 步时间从 2^97.3 降到 2^85.5；引入 2-bit 条件模型 | 出版商原始摘要及发表记录 |
| [H09] | EUROCRYPT 2024 | 28 步实际、31 步理论碰撞；后续已经改进 | 原始摘要 |
| [H10] | FSE 2012 | 50 步普通原像时间 2^511.5、内存约 2^4；57 步 **pseudo-preimage** 时间 2^511、内存约 2^6 | IACR 作者演讲表格明确区分 |

不能把“52 步 SHA-256/57 步 SHA-512 preimage”不加修饰地从百科/帖子照搬：原作者表格在这些行的普通 preimage 一栏是空白。时间极接近通用上界的理论原像攻击也不具有实际可运行含义。

### 2.3 SHA-3 / Keccak

| 来源 | 日期/状态 | 明确的模型和结果 | 注意事项 |
|---|---|---|---|
| [H13] | CRYPTO 2024；received 2024-07-12 | 内部差分碰撞：SHA3-384 从 4 轮扩到 5；SHAKE256 从 5 扩到 6 | 不代表所有 SHA-3 实例均有 6 轮经典碰撞 |
| [H14] | EUROCRYPT 2025；received 2025-03-07 | squeeze-Mitm/internal-differential 原像：五个实例改进 4 轮，四个实例达到 5 轮；提出 VDDT | 只对小宽度 4 轮实例作实际验证；不能称标准宽度实际 5 轮原像 |
| [H15] | CT-RSAC 2026，2026-07-02 online | 4 轮 SHA3-384 碰撞估计从 2^59.64 降到 2^56.11；改进无效差分对条件和 SAT 连接 | 原始摘要已核验；作者的 0.63 年性能估计不是本项目执行；完整全文未取得 |
| [H16] | Designs, Codes and Cryptography，2026-02-18 | Keccak-384/512：2 轮原像分别 2^39/2^204；3 轮分别 2^270/2^424；提供 2 轮 Keccak-384 全零摘要原像及代码 | **原始 Keccak 命名/填充必须对照全文**，不可未经检查直接转为 FIPS SHA3；数值与设计者汇总页面冲突，见 §5 |
| [H17] | ToSC 2026(1), 189–211 | 5 轮 Keccak[r=640,c=160] 实际原像挑战；设计者页面报 2^59.7 | 这是 800-bit 状态且 c=160 的 Crunchy 参数，非标准 1600-bit SHA3；原期刊 DOI landing 被工具阻挡，确切模型/时间留全文复核 |
| [H18] | ToSC 2025(3), 633–692 | sponge MitM 的 linear cancellation；Keccak 高容量及 Ascon/Xoodyak 相关方法 | 研究方向已有自动化/线性代数方法，正式选此方向前须取得全文 |

设计者汇总 [H19] 还列有 6 轮 SHAKE128 经典碰撞时间 2^123.5（ASIACRYPT 2022）、6 轮 SHAKE256 碰撞时间 2^232.29（CRYPTO 2024）、2025 年对 3 轮 Keccak-256 的实际原像等。这里仅将该清单用作找到原论文的索引，不将其中数字全部作为最终已审计最优值。尤其 6 轮 SHAKE 的碰撞比较必须带输出长度；汇总页面省略的参数不能用直觉补全。

可处理的中间问题包括：χ 条件线性化后的精确仿射空间维数、条件表的冗余/蕴含证书、满足实际 absorb/padding 限制的两阶段连接、跨 lane 条件导致的概率依赖，以及对某一精确定义的路径族给出可检查的不可行性或最优性证明。单纯穷举 5-bit χ 的 DDT/VDDT 是 L0；已有 VDDT/内部差分方法的重述也不是新成果。

### 2.4 BLAKE2

| 来源 | 日期/状态 | 已有内容 | 不可误写 |
|---|---|---|---|
| [H20] | ePrint 2013/467，CT-RSA 2014 对应研究 | 系统研究 BLAKE→BLAKE2 的调整，差分、impossible differential、rotational 等 | 原始 BLAKE 的攻击不能无条件搬到 BLAKE2 |
| [H21] | CRYPTO 2015；received 2015-05-29 | 高阶差分 MitM；BLAKE/BLAKE2 2.75 轮带 padding 原像、7.5 轮压缩函数 pseudo-preimage 的框架 | 抽象覆盖两个系列，必须查看表格后才能把某数值绑定 BLAKE2s/b |
| [H22] | ePrint 2023/299，2023-02-28，当前标 Preprint | 近似 signed-difference MILP + digraph 位条件推导；BLAKE2s boomerang 较先前多 0.5 轮；检索到 PDF 摘要片段明示 8 轮 | 攻击对象是 keyed permutation；本轮未确认 BLAKE2s 的确切时间表格，勿从二手摘要填 2^182 |
| [H23] | FSE 2017 对应 ToSC 研究；received 2016-08-30 | 在 weakly ideal cipher 模型中证明 BLAKE2 压缩函数的 indifferentiability，并讨论模式安全 | 不是对真实 BLAKE2 轮函数安全性的无条件证明 |

有吸引力的研究切口是合法 hash 初始化约束下，对 signed-difference 工具结果做 exact satisfiability/probability 检查；比较 BLAKE2s 与 BLAKE3 的消息安排和 flags 是否改变相同路径族的最优界。只发现“自由状态攻击被常量阻挡”并不自动新颖，早期分析及设计文档已指出这种区别。BLAKE2b 的 64-bit 词通常使直接精确计数更难，首轮先以 BLAKE2s 为对照。

### 2.5 BLAKE3

规范 [H04,H05] 是主参照，不能把 BLAKE/BLAKE2 的表格标作 BLAKE3 当前最优表。

1. [H22] 报告针对 **keyed permutation** 的 7/7 轮 boomerang，时间 2^180，并用缩减轮 quartet 验证方法。该对象并非标准 BLAKE3 树哈希碰撞；2^180 也没有突破规范所述的 128-bit 目标。
2. [H24]（CRYPTO 2022，ePrint major revision）已经讨论 BLAKE3 类模式的证明，指出 XOF 随机访问 counter 的可见性条件。因此“首次注意 BLAKE3 XOF counter 需要公开”“BLAKE3 完全没有任何模式安全研究”均不成立。
3. [H25] 早在 2013 年就系统说明 ARX 单个操作的概率乘积未必等于路径概率，最优 characteristic 也未必代表整个 differential。BLAKE3 设计文档还主动引用这一限制。不能把验证这种偏差的任意小例子当作新密码分析。

本次未找到并核验标准合法输入下的完整 7 轮 BLAKE3 hash 碰撞、原像或相关安全目标低于其 128-bit 目标的公开攻击。这是调查结论而不是不存在这类攻击的证明。

首项小目标可规定为：**对 32-bit BLAKE3 前 r 轮（先 r≤2）的某个明确低权输入差分族，保留标准 IV、flags 与 counter，构建精确联合约束，寻找相对于 2023 signed-difference 模型的遗漏可实现性条件/更紧概率界；在可行时生成可检查 UNSAT/计数证书。** r≤2 只是建模与证书基线。只有进一步得到新的可推广条件，或严格改善较强轮数/路径族的界，才是论文候选。

### 2.6 SHA-1

| 来源 | 日期/状态 | 模型与复杂度 | 研究含义 |
|---|---|---|---|
| [H26] | CRYPTO 2017，ePrint 2017/190 | 标准完整 SHA-1 首个实际普通碰撞 | 是历史复现基线，不能作为本项目原创 |
| [H27] | USENIX Security 2020；ePrint 最后修订 2020-07-26 | 标准完整 80 步：identical-prefix 碰撞 2^61.2、chosen-prefix 碰撞 2^63.4（论文指定设备成本度量）；作者实际使用大型 GPU 集群 | GPU 费用为历史值，不当作 2026 报价；本轮不运行集群攻击 |
| [H21] | CRYPTO 2015 | 62 轮两块带 padding 原像；56 轮单块带 padding；62 轮单块不带 padding | 碰撞已破不意味着完整原像已破；差分阶数扩展已属既有方法 |
| [H28] | 2017 的作者研究 | SHA-1 碰撞检测以 unavoidable conditions 大幅提速 | 适合验证/防御研究，但不应改称破解算法数学本体 |

该方向适合建立独立 verifier、路径条件复核和性能基线，首篇纯密码分析新论文的优先级较低：成熟工具、昂贵大实例和标准退役共同降低新增收益。若能对已有条件族给出可证明最优检测集合或迁移到仍使用的算法，则可提高价值，但不能把实现层检查主张当作安全界突破。NIST 的 2022 公告计划于 2030 年末完成对 SHA-1 全应用加密保护的迁移；这里仅作优先级背景。[H29]

## 3. 机会评分与资源预算

以下是 **研究决策分数**，不是统计概率；面向有边界的中间问题，绝不是对完整算法被破解的概率。资源为首阶段建议上限而非实际运行记录。重要性考虑标准使用与方法可转移性，原创机会扣除最接近工作的拥挤度，可行性强调普通 CPU 可产出严格结论；综合分=0.30×重要性+0.30×原创机会+0.40×近期可验证增量。

| 候选 | 重要性 | 原创机会 | 近期增量 | 综合 | 首阶段资源/时间建议 | 证明/复核难度 | 主要失败风险与潜在价值 |
|---|---:|---:|---:|---:|---|---|---|
| BLAKE3 合法状态下 ARX 联合条件 | 9 | 6 | 6 | 6.9 | 单机 8–16 GB；数小时建立小参数基线，数日到数周精确路径比较；任何 >2^35 预期枚举先停作复杂度审核 | 中高：路径概率依赖、轮/模式边界 | 结果早被 BLAKE2 或通用 ARX 文献覆盖；若有新可推广条件和现实路径提升，方法型论文可期 |
| SHA-3/Keccak 约束及精确线性结构 | 10 | 5 | 6 | 6.9 | 单机 8–32 GB；先小宽度 exhaustive，再标准宽度低轮 SAT；数日到数周 | 中高：仿射维数可以严格证明；整攻击概率和消息阶段较难 | 2024–2026 文献活跃，极易落后；真实剪枝/空间改进、证书支持的界有发表潜力 |
| BLAKE2s 对照与符号模型 | 8 | 5 | 6 | 6.3 | 单机 8–16 GB；与 BLAKE3 共用底层，独立规范 verifier | 中高 | 10+ 年已有分析；较好的价值在跨算法通用定理，不在单个玩具实例 |
| SHA-256 局部碰撞/符号位条件 | 10 | 3 | 4 | 5.5 | 建模 8–32 GB；新路径可能需更多内存，端到端碰撞通常超出会话 | 高：复杂消息扩展、可控制性、未控制概率 | 2026 最新两代工作已迅速改善纪录；首篇直接追 39 步标准碰撞成功概率低；若真提升则价值很高 |
| SHA-512 条件模型/内存复杂度 | 9 | 4 | 4 | 5.5 | 比 SHA-256 更大位宽；从已知路径条件验证开始 | 高 | 64-bit 状态使 naive search 失控；可以改进证明/框架，但目前纪录已达 39 步理论 |
| SHA-1 条件复核/迁移 | 6 | 3 | 7 | 5.5 | 单机可核验公开向量和低轮例子；生成全碰撞远超预算 | 中：核验简单、证明新最优性难 | 极高重复风险；纯复现 L0，除非提出跨算法方法或严格优化边界 |

AI Agent 优势主要在：整理相互矛盾参数、生成多实现与负控制、枚举低维真值表、搭建求解器证书检查、寻找失败反例。弱项主要在：为模型独立性作错误假设、把易跑弱模型当标准攻击、低估 literature 的等价推广，以及用搜索空白断言世界首次。大型碰撞所需数十到上百 bit 指数工作不能以“多开 agent”替代。

## 4. 可执行第一小目标及验收门槛

### 4.1 建议的 hash 子组目标

名称暂定：**BLAKE3 前轮约束下的进位依赖与差分可实现性审计**。这只是研究命题，不表示已有贡献。

1. 按 [H04/H05] 实现纯 Python 或 C 的 BLAKE3 压缩函数参考；独立实现不共享轮函数代码；以设计者公开向量交叉检查标准完整哈希。保存源码 hash、compiler/runtime、命令、退出码与种子。
2. 固定 unkeyed hash 的首块模型，明确消息长度 64 字节还是更短、flags、counter、最终 XOR 与输出截断。另开内部 keyed-permutation 模型作弱模型对照，不把二者混算。
3. 首先在小 word width 的**研究模型**验证状态相关进位计数；对同一差分路径比较 (a) 每个模加概率相乘，(b) brute force，(c) 独立精确 DP/#SAT。穷举应对全部输入，不用抽样声称定理。
4. 查 [H20,H21,H22,H25] 与通用 ARX 精确计数/Markov 依赖论文，确认发现是否已经覆盖。仅“乘积估计有偏”立即归档 L0。
5. 真正可接受的增量：新的充分必要条件/结构压缩，使标准 32-bit 某个路径族精确计数复杂度下降；新的可核验不可行性证书消除已有路径候选；或在相同输入/轮/时间单位下，严格改进已知路径或整个攻击代价。
6. 终止/转向标准：若新条件只是通用 carry automaton、BDD、现有 signed-difference bit deduction 的直接应用，无更强结论或复杂度改进，则停止扩大规模，切向 Keccak 条件系统的精确维数/蕴含证书；记录负结果和直接先行文献。

不要把 solver runtime 的单次降低当作攻击复杂度指数降低。要区分建模、求解、路径验证和实际消息搜索四类成本；随机 solver seed 至少重复对照，并给长尾/超时样本而不是只选赢的实例。

### 4.2 更难但值得长期跟踪

SHA-256 39 步标准 IV 碰撞目前本次核验的新预印本还未有效实现；未控制部分概率过低是作者明确指出的障碍 [H06]。这比“研究 SHA-256”具体，但仍是高难目标。先研究能否严格证明某类局部路径的瓶颈，或突破该类路径而保持合法消息扩展；不能把换成 SFS 逃开障碍写作成功。

SHA-3 标准参数更高轮碰撞、原像仍值得长期追踪；中间问题的数学结构比 ARX 更适合线性代数/有限域工具，但 2023–2026 的 internal differential、VDDT、线性 cancellation、SAT 优化必须逐项比较。

完整 SHA-256 原像/碰撞、完整 SHA3 哈希碰撞、完整 BLAKE3 对规范目标的显著攻击，都应留作长期方向；不作为第一个运行周期的可交付承诺。

## 5. 查重警报与已发现来源问题

1. **2026 年 SHA-2 攻击纪录快速更新。** 31 步实际碰撞、37 步理论碰撞、38 步理论碰撞和 36 步消息对依次对应不同文献/模型/日期。报告必须按版本记录。
2. **SFS 与普通碰撞不可只比轮数。** 2024 的 39-step SFS 不能“击败”2026 的 38-step 标准碰撞。
3. **SHA-2 的 52/57 步是 pseudo-preimage。** 已对照原作者 IACR 演讲表格，不采纳二手误写。
4. **Keccak 设计者汇总页面存在具体数值冲突。** [H19] 将 [H16] 的 2-round K384/3-round K512 写为 2^28/2^426；[H16] 原出版商摘要及 [H16a] ePrint 一致为 2^39/2^424。本草稿采用原研究数值。不能因为是设计者网站就跳过核验。
5. **BLAKE3 全轮 boomerang 不是全轮哈希碰撞。** [H22] 已注明 keyed permutations；亦非打破 128-bit 安全目标。
6. **BLAKE3 counter 与模式证明并非未研究。** [H24] 2022 已给相关条件，必须审查其模型和结论是否覆盖提案。
7. **ARX 概率依赖非新发现。** [H25] 及 BLAKE3 设计文档已主动说明。小参数反例本身默认 L0。
8. **摘要声称“best”只属于论文当时。** 如 2022/2023 ePrint 标 best 或 2024 abstract 标 first，不能直接提升为截至本次日期最优。
9. **HashSmash 新公开挑战值得监测。** 组织官方账号与组织供稿新闻于 2026-10-05 宣布在 Yukon 对 SHA-256、SHA-3、BLAKE3、Poseidon 的 AI 研究挑战 [H30]。挑战网页本次工具无法访问。可作后续公开成果查重入口；不注册、不提交、不把公告等同成果。

## 6. 进入实质研究前的最小文献核验清单

- BLAKE3 路线：取得 [H22] 全文和实际 quartet 参数/生成代码；[H24] 的 counter 证明模型；[H20/H21/H25] 的等价条件；检索通用模加 exact counting、ARX differential hull、non-Markov probability、#SAT/BDD/transfer matrix 与 model-counting 方法。
- SHA-3 路线：取得 [H13,H14,H15,H17,H18] 表格与附录，尤其 capacity、输出长度、padding、round index、memory、概率、实际验证范围；不得将几篇摘要拼成不存在的统一最优表。
- SHA-2 路线：取得 [H06,H07,H08,H12] 最新版本代码和路径，检查标准 IV、双块拼接、填充、有效 step subset、counterexample pair；先验证消息对再声称实际纪录。
- 所有路线：最终 novelty review 至少列最接近 3–10 项；具体说明哪些技术来自先行研究，什么精确命题/复杂度是新贡献，哪些文章全文仍缺失。后两级成果后与投稿前审查尚未发生，不能预填“通过”。

## 7. 来源登记（原始来源优先）

以下标题、日期、状态为本次实际检索结果；普通链接便于仓库复查。括号 `ref` 是此次 web 工具返回的可追溯引用 ID，供主 Agent 在重新打开来源后用于聊天引用。检索未声明穷尽。

| ID | 来源与状态 | URL | 本轮 ref |
|---|---|---|---|
| H01 | NIST, FIPS 180-4, 2015-08；页面有 2023 修订计划 | https://csrc.nist.gov/pubs/fips/180-4/upd1/final ; https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf | turn33view1, turn56view2 |
| H02 | NIST, FIPS 202, 2015-08；页面有 2025 更新计划 | https://csrc.nist.gov/pubs/fips/202/final | turn33view2 |
| H03 | Saarinen/Aumasson, RFC 7693, 2015-11, Informational | https://www.rfc-editor.org/info/rfc7693/ | turn9view3, turn56view4 |
| H04 | BLAKE3 design paper/specification，设计者源文件 | https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.tex | turn9view0, turn11view2, turn11view3 |
| H05 | The BLAKE3 Hashing Framework, C2SP v1.0.0 | https://c2sp.org/BLAKE3@v1.0.0 | turn54view3, turn56view5 |
| H06 | Li et al., Pushing Collision Attacks on SHA-2 to 39 Steps；2026/1120；Preprint；last revised 2026-09-09 | https://eprint.iacr.org/2026/1120 | turn6view0 |
| H07 | Li et al., Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2；CRYPTO 2026；2026/1080 | https://eprint.iacr.org/2026/1080 | turn54view0 |
| H08 | Zhang et al., Collision Attacks on SHA-256 up to 37 Steps with Improved Trail Search；EUROCRYPT 2026；2026/232 | https://eprint.iacr.org/2026/232 | turn3view0 |
| H09 | Li/Liu/Wang, New Records in Collision Attacks on SHA-2；EUROCRYPT 2024；2024/349 | https://eprint.iacr.org/2024/349 | turn3view1 |
| H10 | Khovratovich/Rechberger/Savelieva, Bicliques for Preimages: Attacks on Skein-512 and the SHA-2 family；FSE 2012；2011/286 | https://eprint.iacr.org/2011/286 ; https://www.iacr.org/workshops/fse2012/SLIDES/59.pdf ; https://www.hse.ru/data/2012/02/06/1262670848/shaMITM.pdf | turn36view0, turn39view1, turn39view2 |
| H11 | Alamgir/Nejati/Bright, SHA-256 Collision Attack with Programmatic SAT；arXiv 2406.20072；2024-06-28 | https://arxiv.org/abs/2406.20072 | turn0academia35 |
| H12 | Li et al., New Collision Attacks on Round-Reduced SHA-512；CRYPTO 2025，2025-08-17 | https://link.springer.com/chapter/10.1007/978-3-032-01901-1_7 | turn54view2 |
| H13 | Zhang/Hou/Liu, Probabilistic Linearization: Internal Differential Collisions in up to 6 Rounds of SHA-3；CRYPTO 2024；2024/1136 | https://eprint.iacr.org/2024/1136 | turn22view1 |
| H14 | Zhang/Hou/Liu, Preimage Attacks on up to 5 Rounds of SHA-3 Using Internal Differentials；EUROCRYPT 2025；2025/439 | https://eprint.iacr.org/2025/439 ; https://link.springer.com/chapter/10.1007/978-3-031-91107-1_12 | turn21view0, turn18search6 |
| H15 | Cui/Hu/Cui/Wang, Improved Collision Attacks on 4-Round SHA3-384；CT-RSAC 2026；online 2026-07-02 | https://link.springer.com/chapter/10.1007/978-3-032-22931-1_11 | turn46view0 |
| H16 | He/Lin/Yu, Improved preimage attacks on round-reduced Keccak-384/512；DCC 94,55；2026-02-18 | https://link.springer.com/article/10.1007/s10623-025-01780-z ; https://github.com/lxe21/2round-Keccak384 | turn49view3 |
| H16a | He/Lin/Yu/Guo, 同题较早 ePrint；2022/788；last revised 2023-03-08；元数据仍 Preprint | https://eprint.iacr.org/2022/788 | turn42view1 |
| H17 | Lin et al., Practical Preimage Attack on 5-Round Keccak[r=640,c=160]；ToSC 2026(1),189–211；原 landing 未取得 | https://doi.org/10.46586/tosc.v2026.i1.189-211 | turn39search19, turn42search1；原文访问 turn42view0 失败 |
| H18 | Qin et al., Linear Cancellations in the MitM Attacks on Sponge Functions；ToSC 2025(3),633–692；全文待取得 | https://faculty.ecnu.edu.cn/_s43/wgl2/main.psp ; https://keccak.team/third_party.html | turn6view3, turn22view2 |
| H19 | Keccak 团队 third-party cryptanalysis 索引；本轮发现数值冲突，不能替代原文 | https://keccak.team/third_party.html | turn22view2 |
| H20 | Guo/Karpman/Nikolic/Wang/Wu, Analysis of BLAKE2；2013/467；CT-RSA 2014 对应研究 | https://eprint.iacr.org/2013/467 | turn9view2, turn11view0 |
| H21 | Espitau/Fouque/Karpman, Higher-Order Differential Meet-in-The-Middle Preimage Attacks on SHA-1 and BLAKE；CRYPTO 2015；2015/515 | https://eprint.iacr.org/2015/515 | turn36view2 |
| H22 | Hao/Wang/Jiao/Gong, Approximate Modeling of Signed Difference and Digraph based Bit Condition Deduction: New Boomerang Attacks on BLAKE；2023/299；Preprint | https://eprint.iacr.org/2023/299 | turn22view0 |
| H23 | Luykx/Mennink/Neves, Security Analysis of BLAKE2's Modes of Operation；2016/827；FSE 2017 对应工作 | https://eprint.iacr.org/2016/827 | turn52view1 |
| H24 | Gunsing, Block-Cipher-Based Tree Hashing；CRYPTO 2022；2022/283 major revision | https://eprint.iacr.org/2022/283 | turn14view0 |
| H25 | Mouha/Preneel, Towards Finding Optimal Differential Characteristics for ARX: Application to Salsa20；2013/328；发表状态未另核验 | https://eprint.iacr.org/2013/328 | turn54view1 |
| H26 | Stevens et al., The first collision for full SHA-1；CRYPTO 2017；2017/190 | https://eprint.iacr.org/2017/190 | turn56view1 |
| H27 | Leurent/Peyrin, SHA-1 is a Shambles；USENIX Security 2020；2020/014 | https://eprint.iacr.org/2020/014 ; https://www.usenix.org/conference/usenixsecurity20/presentation/leurent ; https://github.com/SHA-mbles/sha1-cp | turn33view0, turn56view0, turn30search3 |
| H28 | Stevens, Speeding up detection of SHA-1 collision attacks using unavoidable conditions；2017/173 | https://eprint.iacr.org/2017/173 | turn0search28 |
| H29 | NIST, Transitioning Away from SHA-1 for All Applications；2022-12-15 | https://www.nist.gov/news-events/news/2022/12/nist-transitioning-away-sha-1-all-applications | turn30search18 |
| H30 | Eigen Labs 官方账号与组织供稿，HashSmash 公告；2026-10-05；非学术成果 | https://www.linkedin.com/posts/eigenlabsorg_ai-is-getting-better-at-finding-vulnerabilities-activity-7512862811203563520-uAXt ; https://www.prnewswire.com/news-releases/preparing-the-worlds-cryptography-for-the-ai-era-eigen-labs-and-zcash-organization-shielded-labs-launch-hashsmash-an-open-multiplayer-competition-to-test-how-far-ai-can-advance-attacks-on-widely-used-hash-functions-302897508.html | turn18search8, turn18search12 |

## 8. 本阶段验证状态

- 已完成：六候选研究机会调查，标准/原始摘要/发表记录核验，过时纪录与模型混淆检查，识别一项明确二手数值冲突。
- 未完成：任何新定理、原创攻击、原攻击端到端复现、formal proof、独立人类同行评议、二级成果后 novelty review、三级发表前 novelty review。
- 成果等级：**L0 文献调查与研究设计**。
- 研究代码尚未启动；没有远端提交、投稿、预印本发布或第三方通信。
