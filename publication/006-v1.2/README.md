# 006：强积打包支配反例论文与补充材料

版本：**1.2.0-draft**，2026-10-10。完整英文论文及验证附件已准备，可供数学研究者审读。作者草稿为 **River Zhang，Chengdu Neusoft University**，ORCID [0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566)。责任审阅、论文存档许可和对外发布批准尚待确认。

- [正式排版 PDF](../../006-strong-product-packing-counterexample/paper/paper.pdf)（15 页）· [独立 LaTeX](../../006-strong-product-packing-counterexample/paper/main.tex) · [参考文献 BibTeX](../../006-strong-product-packing-counterexample/paper/references.bib)。
- [补充材料 ZIP](006-v1.2-reproducibility.zip) · [逐文件 manifest](manifest.json) · [SHA256SUMS](SHA256SUMS)。
- [英文摘要](abstract.txt) · [Zenodo 元数据草稿](metadata-draft.json) · [复现说明](REPRODUCE.md)。
- [独立 AI 数学复核及六方面审查](REVIEW.md) · [最终包验收](package-validation.json) · [实际验证收据](evidence/)。
- [投稿准备报告与三个期刊建议](../../PUBLICATION_READINESS.md) · [历史原创性审查](../ORIGINALITY_REVIEW.md)。

论文以有限连通简单图给出原 Conjecture 3.1 的完整反例：六维 cube 没有半径二支配的 3-packing，而与显式 608 点、9168 边辅助图的强积具有 64 个可行中心。书面证明自包含；存在性断言有原始图与通常路径的 Lean 证明。64 是上界，辅助图阶数不声称最小，历史首创性未确立。

v1.2 保持数学构造和三份数学 Lean 源不变，完善 Main result、Related work、参考文献与真实 AI 披露，修正相关文献对树给出界的表述，并提供准确复现命令。旧 v1 [不可变论文 Release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09)和[数学 Release](https://github.com/mio-qwq/math/releases/tag/006-strong-product-conjecture-counterexample-2026-10-09)原样保留；不能把旧公开时间转述为本版本发布日期。

ZIP 保留仓库相对路径，包含论文、BibTeX、三份数学 Lean 源、固定依赖配置、精确图与同中心证书、历史实际编译记录、两套检查器及当前收据。无缓存、机器 junction、私人指示或第三方论文副本。旧导航文档中的全仓库链接可能指向包外专题，见 [附件边界](ARCHIVE_NOTE.md)。

元数据是**文件草稿，不是 API 请求**。作者与机构来自已提供的草稿；许可、通讯邮箱、实际人类贡献、资金及利益冲突声明未填写，不能推断为没有资金或没有冲突。既有仓库 LICENSE 不替代新的论文存档许可。尚未创建或预留任何 Zenodo DOI、向 arXiv／期刊投稿或联系作者；AI 复核不等于外部人类同行评审。
