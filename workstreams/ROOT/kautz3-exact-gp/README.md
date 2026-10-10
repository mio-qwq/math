# 长度三 Kautz 有向图的一般位置数：完整 Lean 证明

对每个字母数 \(m\ge3\)，本目录证明

\[
\operatorname{gp}(Ka(m,3))=\frac{m(m-1)(2m-1)}6.
\]

这里的顶点是全部三字词 `abc`，只要求 `a≠b`、`b≠c`，允许 `a=c`；
弧为 `abc→bcd`，要求 `c≠d`。一般位置禁止三个不同选点位于原有向图的
同一条最短路径上，不能改成“存在一条避开第三选点的最短路径”。

这是 Chandran 等《The general position number of digraphs》
[arXiv:2604.15909v1，Problem 5.2](https://arxiv.org/html/2604.15909v1) 的
**词长固定为三、字母数任意的完整特殊情形**。原文 Table 1 给出有限参数的
数值观察；本结果的上界由符号证明及 Lean 内核验证，不由有限搜索推断。
其他词长及 Problem 5.2 的其余对象仍未由本结果解决。若文献用出度 `d`
表示 Kautz 参数，则 `d=m−1`，对应公式为 `d(d+1)(2d+1)/6`。

[完整书面证明](PROOF.md)、[独立语义复核](INDEPENDENT_REVIEW.md)、
[来源及历史边界](HISTORY.md) 与 [Lean 源码](Kautz3ExactGP.lean) 均在本目录。
最终声明 `Kautz3.exact_cardinality` 同时给出达到该数值的原语义 GP 集及
全部 GP 集的上界。实际有向距离、所有最短简单路径、下界构造、三字母基例
和删字母归纳均已形式化，没有把待证核心作为假设。

固定环境为 Lean 4.34.1、Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`。实际编译及全部 24 项声明审计见
[收据](lean-audit.json) 和 [日志](lean-audit.log)。在仓库根目录复现：

```powershell
Set-Location 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/kautz3-exact-gp/Kautz3ExactGP.lean
```

数学推导、Lean 编码、检查及文字整理使用 AI 辅助。独立语义复核由未参与
该完整源码撰写的另一 AI 代理完成，不能等同外部同行评审或第二次独立编译。
不宣称世界首次；作者身份及正式投稿另行确认。根目录 README 的既有状态
汇总不替代本目录绑定源码和实际验证的记录。
