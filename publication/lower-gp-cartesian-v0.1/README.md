# 笛卡尔积下 GP 数：严格反例、无界差距与尖锐修正界

**A sharp lower general-position bound for Cartesian products**，冻结稿 v0.1；13 页英文论文。

本目录于 2026-10-13 同步已通过技术验收的论文、证明与复现材料。
**作者、署名顺序、贡献／责任声明及单独预印本许可元数据仍待逐篇确认。**
当前为公开 GitHub 论文草稿；尚未取得新 DOI，也不表示期刊投稿、录用或外部人类同行评审。

## 数学结论

反驳 Kruft Welton–Khudairi–Tuite 的期刊版 Conjecture 3（预印本 Conjecture 2.10）。对所有非空有限简单图证明尖锐替代界 `gp⁻(G □ H) ≥ min{5,gp⁻(G),gp⁻(H)}`，并构造任意大差距的连通图族。

Lean 完整覆盖固定 319 点反例的实际图、最短路径和极大性；通用界及无限族属于完整书面／计算机辅助证明，未全篇 Lean 化。

## 论文与证据

- [英文 PDF](snapshot/paper/main.pdf)、[LaTeX](snapshot/paper/main.tex)、[BibTeX](snapshot/paper/references.bib)。
- [完整复现包](lower-gp-cartesian-v0.1-reproducibility.zip)、[复现方法](snapshot/REPRODUCE.md)。
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
- `python supplement/fixed319/verify.py`
- `python supplement/universal/verify_universal_five.py`
- `python supplement/universal/verify_unbounded_gap.py`
- `python replay_independent_controls.py`

精确证书中断言属于检查器，使用方法及限制见复现说明。
准备阶段已执行解压后的数学复算、负面控制、实际 Lean 编译与公理审计，
并完成两遍 LaTeX 导出及全部 PDF 页面检查；本次同步重新核对全部复制字节、ZIP CRC 和内部 manifest。

AI 系统实质参与数学推导、代码、Lean、查重、独立 AI 复核和论文写作，正文已披露；
AI 不列为作者。独立 AI 审查不称为外部人类同行评审。
查重报告注明实际检索范围与限制，不认证历史首创。
006 的作者确认、许可及 DOI 不自动适用于本稿。
本次同步不变更仓库既有 `LICENSE` 或既有数学源码许可，独立预印本与投稿元数据仍待确认。
