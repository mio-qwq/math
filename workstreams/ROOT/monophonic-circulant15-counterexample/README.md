# 15 阶循环图排除定理：证伪 monophonic 存在性猜想

**不存在同时满足直径 2 与 monophonic position number 2 的 15 阶有限简单无向循环图。**
因此 Tuite–Thomas–Chandran《On some extremal position problems for graphs》
[Conjecture 4.5](https://arxiv.org/pdf/2106.06827v3) 的全称存在性命题在 `n=15` 失败。
原猜想要求每个 `n≥11` 都存在这样的循环图。本反例是整数 15 及该阶全部循环图的
排除证明；单个失败图不能代替这一排除。

Monophonic 集要求每条诱导路径至多含两个选点，`mp(G)` 为其最大基数。
诱导路径包括任意长度，不能因为直径为二而仅检查短路径。

证明覆盖全部 128 个逆对连接集：有三角形时 `mp≥3`；部分图不满足直径二；
剩余情形具有三个开放邻域相同的点，仍有 `mp≥3`。
完整[书面证明](PROOF.md)、[原题语义及源码独立复核](INDEPENDENT_REVIEW.md)、
[文献来源与历史边界](HISTORY.md)、[Lean 源码](MonophonicCirculant15.lean) 均在本目录。

Lean 使用真实 mathlib `Walk.IsPath` 和 `Walk.IsChordless`，证明与原三点支持定义
等价；定义并证明 `mpNumber` 确为可达到的最大基数，再由任意原连接集和任意
顶点标签的表示桥导出最终 `not_originalConjecture45`。有限核查仅分类连接集，
任意长度诱导路径上的障碍由一般定理证明。

固定 Lean 4.34.1、Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`。
实际编译与全部七项声明审计见[收据](lean-audit.json)、[日志](lean-audit.log)。
在仓库根目录复现：

```powershell
Set-Location 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/monophonic-circulant15-counterexample/MonophonicCirculant15.lean
```

本结果不声称最小反例阶数，也不否定去掉循环图限制后的原 Theorem 4.4。
历史首创性尚未确认。研究、Lean 和文字整理使用 AI 辅助；独立复核由另一
AI 代理完成，不能等同人工同行评审或第二次独立编译。论文作者和投稿另行确认。
