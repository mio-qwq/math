# Keccak 条件秩：近期文献补充与选题收窄

审查日期：2026-10-11 UTC。执行者：`survey_hashes`。最后核验时间：08:15 UTC 之后的本次有界审查。状态：**本文件冻结；选题前查重补充，未发现可授予 L1–L3 的本项目成果。**

## 1. 结论先行

新发现的 Yan、Bao、Li 的 SAC 2026 工作直接覆盖了“联合优化约束秩、局部密度与剩余自由度”，并明确分析非线性有效解投影到容量部分时的重数。它也已经精确枚举选定容量值对应的整个线性纤维。因此，以下内容都不能作为本项目的新贡献：重新做秩优化、重新提出投影概率公式、指出线性自由变量不是独立有效尝试、精确计算一个纤维、重建调和平均估计器，或仅提出直接优化有效自由度的目标。[R1–R3]

**保留的最小候选**是：固定同一公开 Table 6 实例和完整约束，给出非平凡、可独立检查的**全局**纤维二阶矩／投影大小／有效自由度界，并明确它相对现有分析改变了哪一项同模型结论、用了多少时间和内存。这个候选尚未完成；它也尚未通过原创性审查。Cauchy–Schwarz、二阶矩恒等式、核方向枚举和局部集合乘积分解本身均不作新方法主张。

原 `OBJECTIVE.md` 所要求的“未被已有建模包含的条件”仍是合理验收门槛；但其泛化动机需要以本补充为约束。不能把原先尚未检索到的近期文章当成不存在，也不能因为其最终修订全文仍缺失而提高新颖性信心。

## 2. 身份、日期与版本证据

论文作者为 **Luhan Yan、Zhenzhen Bao、Huina Li**。会议题名为 *Refining Probabilistic-Linearization TIDA for 5-Round SHA3-384 Collision Attacks*；ePrint 题名末尾另有 **(Full Version)**。[R1–R5]

| 对象 | 本轮核实结果 | 不能据此推断的事项 |
|---|---|---|
| SAC 2026 接收与日程 | 官方接收列表含该文；日程安排在 2026-08-27 的 Symmetric cryptanalysis 场次 | 接收列表不是最终 Springer 卷号、页码或 DOI 证据 |
| 官方演讲 | 官方 URL，27 张幻灯片，标题页日期 2026-08-27；已读取文字内容 | 不能认为幻灯片与后续完整稿逐字相同 |
| 官方 preproceedings | 实际取得 35 页 PDF；本 Agent 阅读 §5.1–5.4、§6、附录 A/B 的 Table 5–6，另做全文关键词定位 | 没有声称通读全部证明和所有附录；PDF 内日期不是公开日期的认证 |
| ePrint 2026/2090 当前条目 | 原始 metadata 与摘要已成功打开；received 2026-09-18，revised 2026-09-30；标注 `Published elsewhere. Minor revision. SAC 2026` | 该标签不自动证明最终会议录已经上线 |
| ePrint 版本历史 | 可见两条 PDF update：`20260918:124553` 与 `20260930:142748` | 本轮未取得两个版本的 PDF 字节，未做正文差异比较 |
| 当前 ePrint 的出版说明 | 条目另说明完整稿对应的 camera-ready version 将出现在 SAC 2026 Proceedings | 应同时保留该说明，不把 metadata 的 `Published elsewhere` 扩张成已核验最终出版信息 |

### 已独立再核验的会议稿字节

获取由 `survey_symmetric` 完成；本 Agent 只读取现有缓存，并独立重算以下字段。再核验命令正常退出，`exit_code=0`。

| 字段 | 值 |
|---|---|
| 原始 URL | [SAC2026_2-final50.pdf][R2] |
| 现有缓存 | `workstreams/CRYPTO/.local-cache/keccak-source-access/sac2026_2-final50.pdf` |
| 字节数 | `821976` |
| PDF 页数 | `35` |
| SHA-256 | `da997847e94e3c6fda942af56956d101c17a3dfcaa7ddd25d5b573d4b9292645` |
| CreationDate / ModDate | 均为 `D:20260724135645Z`，仅为文件内元数据 |

**七月制作的会议稿与九月三十日修订的 ePrint 必须分别引用。** “会议稿里未见某命题”不能替代对最新完整稿的查重。

## 3. 最直接的已知覆盖

以下仅提取与选题决策有关的内容；更完整来源与实例可获得性见 `SOURCE_ACCESS.md`。

| 已有工作 | 已覆盖事项／精确定位 | 本项目的限制 |
|---|---|---|
| Yan–Bao–Li，SAC 2026；ePrint 2026/2090 | SA-PIDS 联合选择子空间；投影重数与调和平均校正；会议稿 §5–6；幻灯片 23 将直接优化有效自由度列为开放问题 | 这些方法及“应优化有效自由度”的动机已被提出 |
| Zhang–Hou–Liu，CRYPTO 2024；ePrint 2024/1136 | 概率线性化、MDST、GreedyPIDS、内部差分碰撞；正式补充材料附录 A/B 给算法与路径 | 不能把条件化 χ、局部子空间选择或高斯消元重新认领为方法创新 |
| Zhang–Hou–Liu，EUROCRYPT 2025；ePrint 2025/439 | 内部差分原像、逆向线性化、VDDT；正式补充材料已取得 | 原像与碰撞模型不同，但一般线性化／差分有效性建模不能只与碰撞论文比较 |
| Qin 等，ToSC 2025(3):633–692 | 线性抵消、MitM 方程处理与内存改进 | 增添消元步骤或缩减抵消表，不自动成为新的数学条件或复杂度界 |

后两篇 ePrint/主文的获取与修订差异仍有缺口；本次没有重新下载失败入口。CRYPTO 2024 与 EUROCRYPT 2025 的正式补充材料、Qin 等公开提取全文的实际阅读边界由 `SOURCE_ACCESS.md` 记录。此表是本目标最近的四个工作族，不是全球穷尽目录。[R7–R10]

### 选定会议实例的精确口径

作者在同一 5 轮 SHA3-384 内部差分路径上报告理论攻击代价由约 \(2^{170.73}\) 降至约 \(2^{164.11}\)；本项目没有复现该攻击，也没有独立确认所有复杂度因素。[R1]

用于后续重建的会议稿位置为 Table 5（PDF 第 30 页，路径）和 Table 6（第 31 页，77 个活跃 S-box 的约束选择）。尤其要沿用 §5.2 脚注 6 的 **800 位内部差分模型中 R=412、C=388**，其中 padding 位归入 C。§6 列 \(E_\Delta\) 469 个方程、\(E_R\) 384 个、\(E_C\) 85 个，线性纤维维数为 \(412-384=28\)。这些都是**待本项目独立复算的文献数值**。[R2]

不能将标准 SHA3-384 的 rate/capacity 直接除以二得到 416/384 后，用该不同划分替代作者的 412/388 模型。Table 5 的中间路径范围也不能与攻击的五轮总轮数混为一谈。

## 4. 二阶矩与投影界：直接推论风险

这一节给出本审查者的初等重构，用来否定过宽的新颖性主张；不是新定理。

设 \(S_\Delta\) 是已经固定的仿射约束解集，\(V\subseteq S_\Delta\) 是满足所有非线性有效性条件的解，\(\pi\) 是既定容量投影。写

\[
N_c=|V\cap\pi^{-1}(c)|,\quad
A=|V|=\sum_c N_c,\quad
B=|\pi(V)|,\quad
E=\sum_c N_c^2.
\]

在 \(A>0\) 的情况下，非空纤维的平均大小是 \(\bar\kappa=A/B\)。若所有线性纤维大小为 \(K\)，则基本计数给

\[
|S_\Delta|=K|S_C|,\qquad
p_1=\frac{B}{|S_C|}
=\frac{A}{|S_\Delta|}\frac{K}{\bar\kappa}.
\]

这正是现有投影模型；重新命名 \(A,B,E\) 不改变原创性状态。[R2, §5.2]

### 4.1 从现有采样分布到二阶矩

论文的外层实验从有效解中抽样，因而抽到容量值 \(c\) 的概率是 \(N_c/A\)。论文 §5.3 已写出该分布以及在其下取算术平均的表达式。于是直接有

\[
\mathbb E_{v\leftarrow V}[N_{\pi(v)}]=\frac{E}{A},
\qquad
\mathbb E_{v\leftarrow V}[1/N_{\pi(v)}]=\frac{B}{A}.
\]

Cauchy–Schwarz 随即给出

\[
A^2\le BE,\qquad
B\ge\left\lceil\frac{A^2}{E}\right\rceil,
\qquad
\bar\kappa\le\frac{E}{A}.
\]

因此“利用 size bias 的二阶矩给投影下界”是既有分布与初等不等式的直接应用。即使在本轮所读章节中没有看到作者把它单独命名为 energy bound，也不能据此认定本项目提出了新理论。

### 4.2 核方向枚举同样是普通计数恒等式

令 \(H\) 为 \(S_\Delta\) 的方向空间中被 \(\pi\) 映到零的线性子空间。按有序对 \((v,v')\) 的差 \(h=v\oplus v'\) 分类，立即得到

\[
E=\sum_{h\in H}|V\cap(V+h)|.
\]

若在正确的坐标下**确实**有 \(V=\prod_t V_t\)，则还可写成

\[
E=\sum_{h\in H}\prod_t |V_t\cap(V_t+h_t)|.
\]

这属于集合自相关的普通展开，不因出现在 Keccak 中就变成新算法。要使用第二式，必须先从原始条件证明局部集合乘积分解成立；特别需要处理所选仿射约束、padding 划分、坐标变换以及任何额外耦合条件。不能因为每个 χ 只有五个输入位便自动断言全局有效集可分解。

如果本实例确实有 \(\dim H=28\)，直接遍历所有核方向有 \(2^{28}\) 项。每项再做多个局部查表及整数乘法，位运算代价、内存和验证代价都应另算。这里没有运行该遍历，也没有证明某种结构能将其严格改进。把指数枚举与更差的全局暴力搜索比较，不能单独证明学术意义上的复杂度创新。

### 4.3 新界须说明方向与适用范围

对于非空纤维，若能检查一个全局界 \(L\le N_c\le U\)，则

\[
\frac{A}{U}\le B\le\frac{A}{L}.
\]

这仍是初等计数。其意义来自能否对**全部相关纤维**给出非平凡、同模型的 \(L,U\)，不能用少数样本的最小值／最大值代替。

- \(\bar\kappa\) 的上界给 \(p_1\) 下界，可支持连接阶段代价的上界。
- \(\bar\kappa\) 的下界给 \(p_1\) 上界，可限制可用的有效自由度。
- 一条纤维中的有效解见证，只证明该纤维的下界；不证明其他纤维的大小或整体投影大小。
- 一个投影下界不自动证明完整碰撞攻击的所有复杂度估计；其余阶段和抽样模型的假设必须继续保留。

## 5. 精确内层与有限外层：不得混淆的验证状态

会议稿 §5.3 已说明低维时枚举整个线性纤维，高维时可抽样估计，并通过维数阈值选择可精确枚举的实例；§6 的选定实例使用精确内层与有限外层抽样。因此，“内层某个 \(N_c\) 是精确整数”并不意味着 \(B\)、\(E\) 或 \(\bar\kappa\) 已被全局精确计数。[R2]

在**有效点均匀、有放回、独立抽样，且每个内层 \(N_c\) 精确**的理想模型中，令

\[
Z_m=\frac1m\sum_{j=1}^m\frac1{N_{c_j}},\qquad
\widehat\kappa_{\rm harm}=Z_m^{-1}.
\]

则 \(\mathbb E Z_m=B/A\)。由线性性，\(\widehat p_1=(A/|S_C|)Z_m\) 是 \(p_1\) 的无偏估计；但 \(Z_m^{-1}\) 一般不是有限样本无偏的 \(\bar\kappa\) 估计。它的一致性与有限样本误差界是不同问题。不能把对倒数估计量的提醒错误地转移到线性形式的 \(\widehat p_1\) 上。

本轮没有证明任何具体样本量的置信区间，也没有全局确定性计数证书。独立同分布前提下的常规集中不等式、已知抽样校正或标准置信区间，本身也不能作为新的密码分析方法。

## 6. 作者代码：固定对象与有限阅读边界

公开仓库：[KeccakInternalDiff/keccak-internal-differential][R6]。本 Agent 实际以只读 `git ls-remote --heads --tags` 核验 main 分支目标，命令退出 0，返回：

```text
259d33b3eebfb6c3777c2bbf6299a47335d5ed2a refs/heads/main
```

本次未返回 tags。父 Agent 另以 GitHub ref/commit API 交叉核验。随后本 Agent 通过 GitHub connector 读取精确 commit 的 README、完整递归 tree 与 `attack/attack_experiment.cpp`，只审查与本任务有关的片段。没有克隆、编译或执行第三方代码。

| 对象类型 | 精确标识 |
|---|---|
| Commit | `259d33b3eebfb6c3777c2bbf6299a47335d5ed2a` |
| 该 commit 的真正 tree | `4bad4b3fa12ee4f0639b2b4c1e335c3e65358d0e` |
| README Git blob | `439ab45b4e5f9384e345d1b57d9b55a9584aa9de` |
| `attack/attack_experiment.cpp` Git blob | `d7ba5c4a0aa3d5a7d4eb6a26f8d1cb7471a00fbf` |

这里 Git blob ID 与 PDF SHA-256 是不同类型的标识，不能混称。递归 tree 响应为 `truncated=false`；没有据文件列表宣称读过所有源码。

在 `updated_attack_sha3_384` 中已实际看到 Table 6 对应的硬编码表、`rate/2-4` 的变量划分、\(2^{14}\) 外层抽样数、按核维数请求完整内层计数，以及调和平均计算。这支持“公开实例可作为复现起点”，不构成本项目对其实现正确性或结果数值的独立确认。[R6a]

仅列以下复现条件，不扩大实现审计：

- README 同时写 CUDA 必需与 CPU fallback；该函数的 `#ifndef USE_CUDA` 分支包含编译期 `#error`。复现环境应以实际构建代码为准，本轮没有验证无 CUDA 构建。
- 外层 PRNG 用 `std::random_device` 初始化；固定种子和记录样本序列将是本项目复现时需要另做的工作。
- 代码先将容量值存入 `unique_dc` 去重，再对保留值计数。这在一般有限样本模型下与论文有放回的 size-biased 推导不同；若实际没有重复，二者数值相同。其对当前巨大投影实例是否有可测影响未经本轮实验；不能凭这一观察宣布论文结果错误。
- 代码对非正计数不进入倒数平均。正确生成的有效外层见证应保证相应真实纤维非空；后续验证器应检查该不变量，而不是默默把异常归零结果当作合法缺失样本。

没有把这些事项提升为实现漏洞、安全事件或新的密码分析成果。

## 7. 收窄后的下一步与停止门槛

只保留一个候选：**同一 Table 6 实例的全局二阶矩／投影有效自由度可检查界**。

1. 首先冻结原文 Table 5–6、轮索引、bit 顺序、padding、R412/C388 与全部局部有效集合。由原始 Keccak 定义独立重建 \(E_\Delta\)，再核验秩和投影核维数是否确为 28。
2. 证明或否定 \(V\) 在所用坐标中的局部乘积分解。若有额外全局条件，明确加入；不能为了保留简单乘积而弱化模型。
3. 在运行之前计算普通核方向枚举、乘积查表、所提剪枝及证书检查的真实复杂度。精确数值、验证时间与搜索时间分别记录。
4. 只有在得到相对已知分析有实质增量的具体全局界后，才进入第二级成果查重；届时还须比较最新 ePrint 完整稿及其他投影计数／集合自相关方法。

如果只得到已有公式、一般二阶矩界、一个精确纤维，或普通枚举的实现，就归 L0 并停止扩展该候选。若所得界不足以改变同模型判断，可保留为经核验的复现资料；不能由“有一个新数值”直接授予 L2 或 L3。

## 8. 有界检索记录与剩余缺口

本轮使用两级 web 检索；涉及最新研究和原始 metadata 的判断用 system1 核验。起初精确题名检索与直接 URL 打开存在无关结果或失败，随后限定题名、作者、ePrint ID 与 30/90 天时间窗取得原始条目及官方会议来源。没有把早期失败或未命中当作不存在的证据。

| 动作 | 实际结果 |
|---|---|
| 精确题名／`2026/2090`，90 天近期检索 | 确认 ePrint 原始条目、公开摘要与作者代码链接 |
| 题名加 `erratum correction revision`，30 天近期检索 | 找到 2026-09-30 修订记录及官方接收／日程信息；未另确认独立勘误，不据此断言不存在勘误 |
| 打开 ePrint metadata 与其 `See all versions` | 成功取得接收、修订日期与两条可见 PDF update 记录 |
| SAC 接收列表、日程、官方演讲 | 成功读取；已区分会议状态与最终出版状态 |
| 官方 preproceedings | 同组 Agent 一次公开获取成功；本 Agent 阅读指定章节，并独立核哈希与页数 |
| 全文提取文本关键词定位 | 对 `Cauchy/Schwarz/second moment/energy/confidence/unbiased` 等未取得命中；只是词面检索，不是等价定理不存在的证明 |
| 作者仓库 | ls-remote、精确 tree/README/指定源码只读成功；未执行代码 |

仍未完成：最新 ePrint PDF 的版本固定及逐节比较；会议稿 Table 5–6 的独立逐位复算；作者源码全链条验证；全局二阶矩或投影大小的精确计算／证书；对其他投影计数、有限域自相关和符号模型计数方法的成果级查重。上述缺口一律保持未确认，不能据其为空而认定原创。

## 原始来源

[R1]: https://eprint.iacr.org/2026/2090
[R1v]: https://eprint.iacr.org/archive/versions/2026/2090
[R2]: https://www.sacworkshop.org/SAC26/preproceedings/SAC2026_2-final50.pdf
[R3]: https://sacworkshop.org/SAC26/talks/50-2.pdf
[R4]: https://sacworkshop.org/SAC26/accepted-papers.html
[R5]: https://sacworkshop.org/SAC26/schedule.html
[R6]: https://github.com/KeccakInternalDiff/keccak-internal-differential
[R6a]: https://github.com/KeccakInternalDiff/keccak-internal-differential/blob/259d33b3eebfb6c3777c2bbf6299a47335d5ed2a/attack/attack_experiment.cpp
[R7]: https://eprint.iacr.org/2024/1136
[R8]: https://eprint.iacr.org/2025/439
[R9]: https://doi.org/10.46586/tosc.v2025.i3.633-692
[R10]: https://pure.ecnu.edu.cn/zh/publications/linear-cancellations-in-the-mitm-attacks-on-sponge-functions/

- [R1：ePrint 当前 metadata 与摘要][R1]；[R1v：可见版本历史][R1v]。
- [R2：已固定字节的 SAC preproceedings][R2]；[R3：SAC 官方演讲][R3]。
- [R4：官方接收列表][R4]；[R5：官方日程][R5]。
- [R6：作者仓库][R6]；[R6a：本轮只读源码的精确 commit][R6a]。
- [R7：CRYPTO 2024 / ePrint 2024/1136][R7]；[R8：EUROCRYPT 2025 / ePrint 2025/439][R8]。
- [R9：Qin 等正式 DOI][R9]；[R10：作者机构记录][R10]。

本轮唯一新写文件为本文件；未修改已冻结的 ChaCha 文献、其他成员目录、Git 历史或远端。文献与代码的内部审查不是人类同行评议。
