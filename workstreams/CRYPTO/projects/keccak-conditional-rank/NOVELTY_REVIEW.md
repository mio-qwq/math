# Keccak 方向：选题前原创性审查

更新日期：2026-10-11 UTC。**一级查重仍未关闭，尚无新成果可进入第二级或投稿前审查。** 最新精确比较见 [RECENT_LITERATURE.md](RECENT_LITERATURE.md)，字节/版本及读取边界见 [SOURCE_ACCESS.md](SOURCE_ACCESS.md)。

## 最近的四组研究及规范

| 来源 | 日期与版本 | 已核实覆盖 | 对本候选的约束 |
|---|---|---|---|
| NIST FIPS 202 | 2015 标准 | SHA-3/SHAKE、Keccak 运算及域分隔 | 标准 1600 位状态、内部差分坐标、padding 与输出模型必须分开 |
| Zhang–Hou–Liu，Probabilistic Linearization: Internal Differential Collisions in up to 6 Rounds of SHA-3 | CRYPTO 2024；ePrint 2024/1136 minor revision | MDST、概率线性化、内部差分；正式补充材料含 GreedyPIDS 与路径 | 局部子空间、条件 χ、差分仿射约束与普通消元不是本项目新方法 |
| Zhang–Hou–Liu，Preimage Attacks on up to 5 Rounds of SHA-3 Using Internal Differentials | EUROCRYPT 2025；ePrint 2025/439 major revision | 内部差分原像、逆向线性化、VDDT；正式补充材料已取得 | 原像/碰撞模型不同；一般线性化等价方法仍须跨模型比较 |
| Qin 等，Linear Cancellations in the MitM Attacks on Sponge Functions | ToSC 2025(3):633–692，2025-09-25 | 用高斯消元处理线性抵消、改进内存及 MILP 建模 | 增加消元或缩减抵消表不自动产生新条件/复杂度界 |
| Yan–Bao–Li，Refining Probabilistic-Linearization TIDA for 5-Round SHA3-384 Collision Attacks | SAC 2026 已确认接收及报告；ePrint 2026/2090 收稿 09-18、修订 09-30、minor revision；最终卷页/DOI 未核验 | SA-PIDS 联合优化；投影重数、有效自由度、调和平均校正；精确单纤维枚举；直接优化有效自由度已列开放问题 | 覆盖原来宽泛的秩/自由度目标；必须限定到同一 Table 6 实例的有用全局界 |

来源：[FIPS 202](https://csrc.nist.gov/pubs/fips/202/final)、[2024/1136](https://eprint.iacr.org/2024/1136)、[2025/439](https://eprint.iacr.org/2025/439)、[Qin 等 DOI](https://doi.org/10.46586/tosc.v2025.i3.633-692)、[作者机构记录](https://pure.ecnu.edu.cn/zh/publications/linear-cancellations-in-the-mitm-attacks-on-sponge-functions/)、[2026/2090](https://eprint.iacr.org/2026/2090)、[官方会议稿](https://www.sacworkshop.org/SAC26/preproceedings/SAC2026_2-final50.pdf)、[SAC 接收列表](https://sacworkshop.org/SAC26/accepted-papers.html)。

## 已得到的正文与剩余缺口

2024 与 2025 的正式 Springer 补充材料已取得并固定 SHA-256；两篇主文的部分公开入口失败，不能声称其主文全文已读。Qin 等作者公开全文提取文本已定位相关章节，未取得对应 PDF 字节。曾猜测的 ToSC 数值页面访问失败，未作为数学来源。

SAC 2026 的 35 页官方 preproceedings PDF 已固定字节，Literature Agent 实际审读 §5.1–5.4、§6、Table 5–6。它的文件内制作日期是 2026-07-24，与最新 2026-09-30 ePrint 修订是不同版本对象；后者正文尚未取得。官方 slides、接收列表、日程与 ePrint metadata/版本历史已核。不能把接收状态写成已核验最终出版卷页，也不能将缺失修订稿视为没有更强结论。

作者代码固定到 commit `259d33b3eebfb6c3777c2bbf6299a47335d5ed2a`，tree `4bad4b3fa12ee4f0639b2b4c1e335c3e65358d0e`。只读 README、目录及指定攻击函数片段，没有执行或全链条验证。代码中的构建、随机种子、去重与非正计数处理仅列复现条件，不作漏洞或论文错误主张。

## 明确排除的新贡献表述

- “首次联合考虑约束秩与自由度”“首次注意有效解的投影重数”“首次用调和平均校正”均被近期先行直接覆盖。
- “首次精确枚举单纤维”被会议稿与作者代码覆盖。
- B≥A²/E、size-biased 二阶矩关系及核方向自相关展开是初等直接推论；不授予 L2。
- “作者未优化有效自由度，因此提出这一目标本身新颖”不成立；它已是作者公开开放问题。

## 当前唯一候选与判断

只保留 [OBJECTIVE.md](OBJECTIVE.md) 的同一 Table 6 全局二阶矩／投影有效自由度可检查界。文献使用 R=412、C=388；其 padding 划分、投影核维数 28 和有效集合分解必须独立重建。更弱模型上的界不能转录为原攻击改进。

**当前新贡献：无。原创性未通过，可信程度不足以作任何优先权主张。** 已确认先行覆盖范围的可信度较高；剩余候选是否可行及是否新颖均未知。尚未完成最新修订稿逐节比较、Table 5–6 逐位复算、全局计数和等价计数方法的成果级查重。

若取得同模型的实质性具体界，才生成成果后的逐命题比较，并由未参与发现的 Literature Agent 主动寻找更早或更强覆盖。第三次投稿前审查和任何外部学术发布均未开始。
