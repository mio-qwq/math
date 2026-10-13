# 无爪次三次图打包着色：36 点反例与奇数无限族

**A structural obstruction to (1,1,3,3,4)-packing colorings**，冻结稿 v0.1；7 页英文论文。

本目录于 2026-10-13 同步已通过技术验收的论文、证明与复现材料。
**作者、署名顺序、贡献／责任声明及单独预印本许可元数据仍待逐篇确认。**
当前为公开 GitHub 论文草稿；尚未取得新 DOI，也不表示期刊投稿、录用或外部人类同行评审。

## 数学结论

对 Mortada–El Zein–Al Hajjar 的 arXiv:2608.02566v1 §6 Problem 1 给出负答案。每个奇数 k≥3 的菱形环三角展开都是 12k 点连通三正则无爪反例；最小列出的实例为 36 点，不声称它是最小反例。

Lean 完整覆盖固定 36 点图与任意目标着色的失败；全部奇数参数族及无菱形结构结论有完整书面证明，未作为全称 Lean 定理宣称。

## 论文与证据

- [英文 PDF](snapshot/paper/main.pdf)、[LaTeX](snapshot/paper/main.tex)、[BibTeX](snapshot/paper/references.bib)。
- [完整复现包](clawfree-packing-v0.1-reproducibility.zip)、[复现方法](snapshot/REPRODUCE.md)。
- [查重及贡献边界](snapshot/ORIGINALITY_REVIEW.md)、[论文准备审查](snapshot/PUBLICATION_READINESS.md)。
- [独立数学审查](snapshot/review/INDEPENDENT_MATHEMATICS.md)、[最终稿审查](snapshot/review/FINAL_MANUSCRIPT_REVIEW.md)。
- [实际编译与复算证据](snapshot/verification/)、[同步完整性验证](package-validation.json)、[外部 SHA256 清单](SHA256SUMS)。

原冻结稿形成于 2026-10-12，其 PDF、源码、内部 manifest 与复现包保持原字节。
`snapshot/` 中的 “private draft” 标签及历史准备报告描述的是该冻结稿形成时的状态；
本目录公开分发的状态以本页为准。准备日期不作为 GitHub 首次公开时间回填。
没有重新运行未变 Lean 或大枚举，也没有把原运行记录伪称为本次新编译。

## 复算

下载复现包并解压，或进入本目录的 `snapshot/`，在普通 Python 下执行：

- `python verify_manifest.py`
- `python supplement/check_structural.py`
- `python replay_independent_checks.py`

精确证书中断言属于检查器，使用方法及限制见复现说明。
准备阶段已执行解压后的数学复算、负面控制、实际 Lean 编译与公理审计，
并完成两遍 LaTeX 导出及全部 PDF 页面检查；本次同步重新核对全部复制字节、ZIP CRC 和内部 manifest。

AI 系统实质参与数学推导、代码、Lean、查重、独立 AI 复核和论文写作，正文已披露；
AI 不列为作者。独立 AI 审查不称为外部人类同行评审。
查重报告注明实际检索范围与限制，不认证历史首创。
006 的作者确认、许可及 DOI 不自动适用于本稿。
本次同步不变更仓库既有 `LICENSE` 或既有数学源码许可，独立预印本与投稿元数据仍待确认。
