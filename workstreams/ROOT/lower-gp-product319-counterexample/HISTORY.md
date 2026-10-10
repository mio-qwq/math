# 原始问题、文献关系与历史范围

原问题来自 Eartha Kruft Welton、Sharif Khudairi、James Tuite，
*Lower General Position in Cartesian Products*：

- [arXiv:2404.19451v1](https://arxiv.org/html/2404.19451v1)，Conjecture 2.10。
- *Communications in Combinatorics and Optimization* 10(1) (2025), 110–125，
  [DOI:10.22049/cco.2024.29171.1879](https://doi.org/10.22049/cco.2024.29171.1879)。
  [作者机构托管的最终 PDF](https://oro.open.ac.uk/98050/9/98050final.pdf)，
  Conjecture 3，印刷页 117。

原定义使用有限简单无向图中的全部最短路径。lower general-position
number 是包含极大 GP 集基数的最小值。原猜想为

$$
\operatorname{gp}^{-}(G\square H)\ge
\min\{\operatorname{gp}^{-}(G),\operatorname{gp}^{-}(H)\}.
$$

本目录固定的 11 与 29 顶点因子均满足原假设，实际笛卡尔积给出严格反例。
这是原不等式的反例，而非某个额外加强版本的反例。原文关于 lower
**terminal** number 的 Proposition 1 是不同参数的结果，不应据此认定原
lower-GP 猜想已经被解决。

## 已有工具与本构造

H 中同块克隆点是**相邻且闭邻域相同**的真孪生点；本目录明确证明其距离性质。
这与原论文以相同开邻域定义的裸词 twins 有区别。
真孪生饱和及通过大 clique 抬高较小极大集基数的机制是已有工具，应归功于
Boštjan Brešar、Ismael G. Yero 的
*Lower (total) mutual-visibility number in graphs*，§2.2、Proposition 5：
[arXiv:2307.02951v2](https://arxiv.org/pdf/2307.02951v2)，
*Applied Mathematics and Computation* 465 (2024), 128411，
[DOI:10.1016/j.amc.2023.128411](https://doi.org/10.1016/j.amc.2023.128411)。
本目录不将这项通用方法声称为新发明。

固定构造与无界族的冻结研究入口分别是
[固定反例](https://github.com/mio-qwq/math/blob/9c4b1855f5ae028f59f4f999cc8d36935f519c49/workstreams/B/lower_gp_product/COUNTEREXAMPLE_PROOF.md)、
[全参数族](https://github.com/mio-qwq/math/blob/6556271dcb99553af752c245438e517f4c01c1f0/workstreams/B/lower_gp_product/UNBOUNDED_GAP_PROOF.md)。
本目录保留其数学论证，并加入实际原图语义的完整固定 Lean 证明及独立验证材料。
无界族与固定反例属于同一个原问题的解答，不重复计数为两个公开猜想解答。

## 文献检查及尚不能宣称的事项

2026-10-10 的多轮检查重新读取原预印本、最终论文、版本页、
[James Tuite 的机构主页](https://profiles.open.ac.uk/j-tuite)及
[The General Position Problem: A Survey，v5](https://arxiv.org/html/2501.19385v5)
的 lower-GP 与乘积问题部分；再次检索准确标题、DOI、arXiv 编号及
Cartesian / lower general position / counterexample / proof / correction 的组合。
在已检索材料中，未确认更早的同范围完整解答。
这不是全球文献穷尽，也不是开放状态或优先权的自动认证；**历史首创性仍未确认**。
若出现更早的可核验结果，应更新文献关系与贡献定位。

数学正确性、公开时间锚及历史原创性是不同事项。本目录不声明世界首次、
最小反例阶、H 的精确 lower-GP、产品的精确 lower-GP 或人工同行评审。
无限族是独立复核的书面证明，尚未 Lean 化；固定反例的形式化范围见
[独立复核](INDEPENDENT_REVIEW.md)和[实际收据](lean-audit.json)。

AI 辅助用于数学研究、程序重建、Lean 推导、文字整理及独立审查。
独立代理复核指不同于发现者或源码写作者的 AI 代理审查，不等同于独立人工研究
或期刊同行评审。AI 不列为论文作者；人工作者及正式投稿另行确认。
