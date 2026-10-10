# lower-GP 笛卡尔积猜想的严格反例

**两个连通因子的 lower-GP 数均至少为 6，而其笛卡尔积的 lower-GP 数至多为 5。**
这严格反驳 Welton–Khudairi–Tuite《Lower General Position in Cartesian Products》
的原 [Conjecture 2.10](https://arxiv.org/html/2404.19451v1)；最终期刊编号为
**Conjecture 3，印刷页 117**，见 [DOI](https://doi.org/10.22049/cco.2024.29171.1879)。

原命题断言
$$
\operatorname{gp}^{-}(G\square H)\ge
\min\{\operatorname{gp}^{-}(G),\operatorname{gp}^{-}(H)\}.
$$
这里 lower-GP 是所有**包含极大** general-position 集中的最小基数。
反例因子分别有 11 与 29 个顶点，都是有限简单无向连通图，直径为 2；
实际 319 顶点笛卡尔积含有五点 GP 集，且每个外点都被真实最短路径阻塞，
所以该五点集包含极大。

完整[数学证明](PROOF.md)、[Lean 源码](LowerGPProduct319.lean)、
[原题与源码独立复核](INDEPENDENT_REVIEW.md)、[文献及历史范围](HISTORY.md)、
[实际编译收据](lean-audit.json)、[公理日志](lean-audit.log) 均在本目录。
另有任意参数的[无界差距族](FAMILY_PROOF.md)，已经独立书面复核，尚未 Lean 化。

固定 Lean 4.34.1、Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`。
在仓库根目录复现：

```powershell
Set-Location 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/lower-gp-product319-counterexample/LowerGPProduct319.lean
```

可另用标准 Python 运行 `python workstreams/ROOT/lower-gp-product319-counterexample/verify.py`。
它重新计算因子及产品的全部 BFS 距离，并以实际路径检查全部 314 个外点；
程序核查、书面无限族与 Lean 固定反例分别列明范围。

不声称最小反例阶、H 或产品的精确 lower-GP、历史首次或人工同行评审。
研究、证明、形式化与文字整理使用 AI 辅助，完整源码由另一位未参与写作的
AI 代理复核；论文作者和正式投稿另行确认。
