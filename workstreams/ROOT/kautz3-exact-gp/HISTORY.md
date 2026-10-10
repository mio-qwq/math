# 命题来源、已有结果与历史边界

本目录证明词长为三的 Kautz 有向图的精确一般位置数

\[
\operatorname{gp}(Ka(m,3))=\sum_{j=1}^{m-1}j^2
=\frac{m(m-1)(2m-1)}6\qquad(m\ge3).
\]

## 原始问题与准确范围

Chandran S.V.、Di Stefano、Erskine、Haritha、Thomas、Tuite 的
[*The general position number of digraphs*，arXiv:2604.15909v1](https://arxiv.org/html/2604.15909v1)
在 Definition 2.1 定义有向一般位置，§3.2 定义 Kautz 有向图，Problem 5.2
提出确定相关有向图族一般位置数的问题。本文的 `m` 是字母数，词长固定为三；
相邻字母必须不同，首尾字母可以相等。原命题禁止任意三个不同选点落在
同一条最短有向路径上，要求对所有这样的最短路径成立。

本成果解决 **Problem 5.2 中词长三、全部字母数 m≥3 的完整子族**。
它不是所有词长的一般公式，也不是整个 Problem 5.2 的解决。

## 原文已经公开的证据

原文 Theorem 3.4 给出词长二的全称结果。Table 1 对词长三、字母数
3、4、5、6、7 给出 5、14、30、55、91，原文已指出平方和规律。
这些数值及公式的观察归属于原论文；本目录新增的可核查内容是覆盖全部
字母数的构造、一般上界、完整书面证明及 Lean 形式化。

相应说明文字存在参数索引不一致。本目录以原图定义、Table 1 和上述明确
公式陈述证明，不把对索引的解释称作作者已经发布的勘误。

Chandran S.V.、Klavžar、Tuite 的
[*The General Position Problem: A Survey*，arXiv:2501.19385v5](https://arxiv.org/html/2501.19385v5)
于 2026-08-16 公开。Theorem 5.61 仍给出词长二的结果，文中问题清单
保留较大词长的计算问题。这是较晚的原作者综述证据，不能据此认证其后
全球没有独立证明。

## 参数对应

部分文献及软件以出度 `d` 为参数，字母数为 `d+1`。此时本结果为

\[
\operatorname{gp}(K(d,3))=\frac{d(d+1)(2d+1)}6\qquad(d\ge2).
\]

[SageMath 的 Kautz 定义](https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/digraph_generators.html#sage.graphs.digraph_generators.DiGraphGenerators.Kautz)
以出度及词长表示参数；[igraph 的定义](https://r.igraph.org/reference/make_kautz_graph.html)
在 Details 中将标签长写为第二参数加一。不能直接将这些参数代入字母数公式。
额外要求首尾字母不同的 cyclic Kautz 图、无向底图和 directed mutual visibility
均不属于本目录已证对象。

## 历史审查状态

2026-10-10 的发布前审查核对原论文当前版本、上述较晚综述、作者公开页面、
相关预印本及公开索引，并对名称、公式、出度参数改写进行多轮检索。
在实际核读范围内，未定位同一定义、全部字母数的等价完整证明或完整证明声明。
检索受索引、页面访问和未公开文献限制；这一结果不能证明不存在更早的工作。

**历史首次与绝对开放性尚未确认，不作世界首次或优先权声明。** 若获得更早
或新的同范围证明，应按对象、量词和证明内容重新比对并修正文献说明。
数学证明的正确性、公开提交时间、历史原创性和外部同行评审是不同事项。
