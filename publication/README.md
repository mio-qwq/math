# 论文与复现材料

本页区分已公开预印本、通过技术验收的 GitHub 冻结稿，以及尚未集成的分支初稿。
数学证明、Lean 覆盖、独立 AI 复核、作者责任审阅和期刊同行评审分别说明，互不替代。
下表按 2026-10-13 实际文件与精确分支版本核对；不认证历史首创。

## 主分支论文

| 论文 | 核心数学结果 | 稿件与复现材料 | 状态及范围 |
| --- | --- | --- | --- |
| **006：A counterexample to packing-domination inheritance in strong products** | 反驳强积打包支配继承猜想；显式辅助图与完整反例证明 | [15 页 PDF](../006-strong-product-packing-counterexample/paper/paper.pdf) · [LaTeX](../006-strong-product-packing-counterexample/paper/main.tex) · [v1.3 复现包](006-v1.3/README.md) · [版本 DOI](https://doi.org/10.5281/zenodo.23293088) | **已公开 Zenodo 预印本**。River Zhang、Yongxian Zhang；原作者记录及 DOI 保持原样。尚未经过期刊同行评审。 |
| **A sharp lower general-position bound for Cartesian products** | 319 点反例、任意大差距族与尖锐修正界 `gp⁻(G □ H) ≥ min{5,gp⁻(G),gp⁻(H)}` | [13 页 PDF](lower-gp-cartesian-v0.1/snapshot/paper/main.pdf) · [LaTeX](lower-gp-cartesian-v0.1/snapshot/paper/main.tex) · [完整包、查重与验收](lower-gp-cartesian-v0.1/README.md) | **技术验收完成，GitHub 冻结稿 v0.1**。固定反例有完整 Lean、15 项公理审计；全称界及无限族为书面／计算机辅助证明。作者与单独预印本许可元数据待确认；没有新 DOI 或投稿。 |
| **A structural obstruction to (1,1,3,3,4)-packing colorings** | 36 点无爪三正则反例与全部奇数 `k≥3` 的 `12k` 点反例族；结构证明无需穷举 | [7 页 PDF](clawfree-packing-v0.1/snapshot/paper/main.pdf) · [LaTeX](clawfree-packing-v0.1/snapshot/paper/main.tex) · [完整包、查重与验收](clawfree-packing-v0.1/README.md) | **技术验收完成，GitHub 冻结稿 v0.1**。固定 36 点实例有完整 Lean、18 项公理审计；无限族及无菱形引理为书面证明。作者与单独预印本许可元数据待确认；没有新 DOI 或投稿。 |

两份新冻结稿的 TeX、PDF、历史审查与复现包保留准备阶段原字节。
PDF 中的 private-draft 标签及 2026-10-12 日期描述原稿形成时的状态，
当前 GitHub 公开分发的状态由包外入口与同步验证记录说明。
准备日期没有回填为首次公开日期，原 SHA256 及真实编译时间没有改写。
本次同步重验全部复制字节、ZIP CRC 和内部 manifest；没有把未变源码的旧编译冒充新编译。

## 尚未集成的分支初稿

STRUCT2 分支已提供七页英文[theta 与 bicyclic 图论文初稿](https://github.com/mio-qwq/math/tree/c3fe80a57bbbfa2adaabb14e90871ee1e90559a7/workstreams/STRUCT2-20261012/theta/paper)。
该材料报告 theta 图精确极值及 bicyclic 图上界，附实际 LaTeX/PDF 构建证据；
其冻结证明有分别记录的 AI 复核，但这份整合稿尚未得到 ROOT 最终验收及本轮新的独立全文复核。
它不是主分支已验收论文，也不与以上三篇重复计数。

## 其他成果与在研边界

已验收但尚未形成完整论文的置换有向图反例、15 阶 monophonic 反例、
7 点打包着色反例及其他证明，见[数学成果与证据目录](../RESEARCH_RESULTS.md)。
Kautz 长度四、TF 结构／随机计数及密码结构的后续分支研究仍有未解决问题和未验收增量；
已完成的核心证明不意味着相应整个研究方向已经结束。

AI 系统实质参与研究、证明、代码与 Lean、文献检查和写作，论文正文如实披露。
AI 不列为作者，独立 AI 复核不称为外部人类同行评审。
新稿署名、贡献／责任声明及独立预印本许可元数据须逐篇确认，不能自动沿用 006。
GitHub 同步不表示 Zenodo、arXiv 或期刊投稿授权，也不表示已取得新 DOI、期刊录用或历史首次证明。
