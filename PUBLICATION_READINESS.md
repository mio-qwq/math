# 006 论文投稿与预印本准备报告

2026-10-10；论文版本 **1.2.0-draft**。完整英文稿、15 页 PDF、参考文献、补充材料和元数据草稿已准备，供最终责任审阅。**文件准备完成不等于已投稿、人类同行评审或历史首创已确认。**

[PDF](006-strong-product-packing-counterexample/paper/paper.pdf) · [LaTeX](006-strong-product-packing-counterexample/paper/main.tex) · [BibTeX](006-strong-product-packing-counterexample/paper/references.bib) · [版本包](publication/006-v1.2/README.md) · [六方面审查](publication/006-v1.2/REVIEW.md) · [逐项原创性报告](publication/ORIGINALITY_REVIEW.md)

## 内容与贡献

**A counterexample to packing-domination inheritance in strong products** 给出 [Bujtás、Iršič Chenoweth、Klavžar、Zhang 的正式论文](https://doi.org/10.1007/s00026-026-00814-0) Conjecture 3.1 的反例；[arXiv:2510.02749v1](https://arxiv.org/abs/2510.02749v1) 有同一量词范围。原命题只要求一个因子不可行，第二因子没有 cycle、regular 或自乘限制。

\[
\gamma_2^3(Q_6)=\infty,\qquad \gamma_2^3(Q_6\boxtimes H)\le64,
\]

其中 \(H\) 为608点、9168边有限非空连通简单图。贡献是兼容支持辅助图、八标签覆盖机制及原命题反例的完整证明；不是新发明 Plotkin 计数、强积距离公式或 perfect-code 理论。64 是可行上界，不声称最优或最小辅助阶数；未解决 \(Q_6\boxtimes Q_6\)。

全文包含 Abstract、Introduction、Main result、Related work、Definitions、完整证明、Formal verification、Exact computational verification、Discussion、AI involvement、复现附录及 References。本次修订不改变数学正文。

## 验收与实际范围

| 检查 | 实际证据 | 界限 |
| --- | --- | --- |
| 原定义与证明 | 任意cube子集障碍、真实邻接、所有短路、三类型同中心覆盖、连通性/边数；独立AI重新推导并复核当前源 | 非外部人类同行评审 |
| Lean | 三数学源绑定实际fresh-object日志，12+12+26声明审计，退出码零；完整存在性端点无额外几何/证书前提 | 本阶段不重编译未变源；数值gamma、H连通/边数/直径不是另有Lean端点 |
| 精确程序 | 10月10日实际双实现及比较：608点、9168边、2016中心对、38912同中心目标，零违反 | 非独立人类实验室；未对整个乘积做全源BFS |
| 环境 | 实际Lean4.34.1/Mathlib HEAD与pin、tracked clean、配置哈希；完整rc/dev token合成负控制被拒绝 | 环境-only的proof_compiled=false；无空缓存新机器Lean重建 |
| 排版 | Tectonic实际编译；15页逐页检查，20字体嵌入，10引用key和Bib一致，交叉引用有定义 | 原生编辑器平台目录错误和非致命Fontconfig启动消息单列 |
| 附件 | [manifest](publication/006-v1.2/manifest.json)、[SHA256SUMS](publication/006-v1.2/SHA256SUMS)、ZIP字节/CRC及[解压运行收据](publication/006-v1.2/archive-replay.json) | 文件摘要不能替代数学证明或首创审查 |

六方面内部准备评分每项0–5，采用主观判断，**不是录用概率、重复率或原创性认证**：正确性 **4.5**（完整证明与原定义形式化）；原创性 **3**（有限检索、历史缺口）；意义 **4**（否定已发表通用命题，未给广参数分类）；文献 **3.5**（核心核查、引用链未穷尽）；可读性 **4**（自包含英文及排版）；投稿规范 **3**（责任审阅、声明、许可和期刊模板待定）。

## 查重与风险

多轮检查原v1、正式版、作者/题名/标识、旧\((p,d)\)-domination术语、perfect-code和支持构造来源；最终修订再次核对正式版Conjecture3.1及相关正结果。没有定位已复验的更早完整解答，**不代表历史首次**。

[2009 perfect-code 定理](https://richardhammack.github.io/reprints/rperfect_codes_strong_prod.pdf)处理p=2d的不交球；本例d<p<2d。[Fisher1994](https://doi.org/10.1137/S0895480191217806)、其[2013后继](https://doi.org/10.1016/j.disc.2012.10.008)及[Plotkin原文](https://doi.org/10.1109/TIT.1960.1057584)未完成全文覆盖。正文自给计数和距离证明，不以不可达全文补逻辑。未运行商业文字相似度数据库，无重复率；独立阅读不是穷尽查重认证。

## 三个匹配期刊

官方范围核查于2026-10-10；以下为编辑适配判断，没有联系编辑或保证录用，正式投稿前须再次核对政策。

| 期刊 | 匹配理由 | 风险与可提高之处 |
| --- | --- | --- |
| **Annals of Combinatorics** | [范围](https://link.springer.com/journal/26/aims-and-scope)含结构/度量图论；原猜想就在该刊，问题与读者直接匹配 | 新颖性标准高；补历史引链全文，突出继承失败机制，按[规范](https://link.springer.com/journal/26/submission-guidelines)完成声明/模板 |
| **Graphs and Combinatorics** | [范围](https://link.springer.com/journal/373/aims-and-scope)含极值/结构图论；显式支持图与可行性反例匹配 | 编辑可能希望更普遍解释；可压缩验证正文到补充材料，保留完整数学链，按[规范](https://link.springer.com/journal/373/submission-guidelines)整理 |
| **The Electronic Journal of Combinatorics** | [要求](https://www.combinatorics.org/ojs/index.php/eljc/about/submissions)覆盖图论/离散数学，重视原创自包含论文及完整细节 | AI得到的证明须作者用自己的语言改写并逐步负责核验，未经充分人类检查的主要AI稿不被接受；当前AI复核不能代替该条件，满足后再评估，不能假称已合规 |

不以影响因子排序；完整反例不必先做到最小图。目标期刊确定后可调整验证篇幅/模板，不能削弱证明或披露。

## 作者、AI 披露与外部发布

草稿署名 **River Zhang**，ORCID [0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566)，**Chengdu Neusoft University**。不列AI作者；正文披露OpenAI Codex/GPT-6-based agent system对构造、推导、Lean、程序、检索、独立AI审查和写作的实质作用，不缩减成语言润色。

人类最终确认项：正式署名/机构与其他实际作者；通讯邮箱/学院；实际人类贡献；资金/利益冲突；责任审阅和同意；论文存档许可；对外发布与日期。未知字段保持待定，不虚构“无资金”或“无利益冲突”。真实披露不自动满足[arXiv](https://info.arxiv.org/help/moderation/index.html)或[Springer Nature](https://group.springernature.com/gp/group/ai/ai-guidance-for-researchers-editors-reviewers)全部条件。

[元数据草稿](publication/006-v1.2/metadata-draft.json)有英文标题/摘要/关键词、作者/ORCID/机构、preprint类型、版本、建议math.CO和MSC2020，以及实际已有[v1论文Release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09)和[数学Release](https://github.com/mio-qwq/math/releases/tag/006-strong-product-conjecture-counterexample-2026-10-09)。许可/发布日期/DOI未选，没有Zenodo请求、DOI创建或预留、arXiv/期刊投稿或作者联系。

其他已有成果的归属、风险和入口保存在[逐项原创性报告](publication/ORIGINALITY_REVIEW.md)；没有将它们包装成本次已完成的独立英文论文。
