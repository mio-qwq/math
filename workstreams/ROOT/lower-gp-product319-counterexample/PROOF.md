# 原 lower-GP 笛卡尔积猜想的严格反例

数学构造与下面第 1–5 节来自[冻结证明](https://github.com/mio-qwq/math/blob/9c4b1855f5ae028f59f4f999cc8d36935f519c49/workstreams/B/lower_gp_product/COUNTEREXAMPLE_PROOF.md)。原论证正文保留，验证状态更新如下。

## 1. Original statement and definitions

Eartha Kruft Welton, Sharif Khudairi and James Tuite, *Lower General Position in Cartesian Products*, arXiv2404.19451v1, Conjecture2.10; final Communications in Combinatorics and Optimization10(1)(2025),110–125, **Conjecture3 on printedp117**, DOI10.22049/cco.2024.29171.1879. Primary final https://oro.open.ac.uk/98050/9/98050final.pdf ; preprint https://arxiv.org/html/2404.19451v1 . The assertion is

    gp^-(G square H) >= min{gp^-(G),gp^-(H)}.

A general-position (GP) set has no three distinct vertices on a graph shortest path. Maximal means inclusion-maximal, not maximum; gp^- is the minimum size among maximal GP sets. In the Cartesian product, adjacency changes EXACTLY one coordinate along a factor edge. Graphs below are finite simple undirected, nontrivial, connected, and of diameter2, so they satisfy the source hypotheses even if connectivity is imposed.

We construct factors of orders11and29 with

    gp^-(G)=6,       gp^-(H)>=6,       gp^-(G square H)<=5.     (C)

Thus the ORIGINAL conjecture is false. The elementary proof below does not depend on B's universal-five partial theorem, a numerical solver, a full optimum computation in H or the product, or a smallest-size claim.

## 2. Explicit factors and selected set

Let A={a_0,...,a_4}, B={b_0,...,b_4}. Graph G has vertex set {c} union A union B. Both {c} union A and {c} union B induce complete graphs K6, and there are no A–B edges. It has11vertices and30edges. Vertex c is universal, so G is connected of diameter2.

Graph H starts with five vertices z,u_0,u_1,v_0,v_1. Vertex z is adjacent to the other four, all four u_i–v_j edges exist, and u_0–u_1 and v_0–v_1 are absent. For each i,j in{0,1}, add a SIX-vertex clique Q_ij. Every member of Q_ij is adjacent to z,u_i,v_j and to no other vertices outside Q_ij. No edges join different Q-cliques. Equivalently, H is the union of the four complete graphs on {z,u_i,v_j} union Q_ij, each a K9. It has29vertices and140edges. Again z is universal and H is connected of diameter2.

The product has319vertices and2410edges. Select

    s_0=(a_0,u_0), s_1=(a_0,u_1), s_2=(c,z),
    s_3=(b_0,v_0), s_4=(b_0,v_1), and S={s_0,...,s_4}.       (S)

Reproducible labels: G uses c=0,a_i=1+i,b_i=6+i. H uses u_0=0,u_1=1,z=2,v_0=3,v_1=4, and Q_ij={5+6(2i+j),...,10+6(2i+j)}. Hence the selected coordinate pairs are exactly

    (1,0),(1,1),(0,2),(6,3),(6,4).

## 3. Factor lower bounds

### G has lower GP exactly6

A GP set containing c cannot meet both A and B, because a–c–b is a geodesic for any a in A,b in B. Such a set is contained in one of the two K6blocks; maximality requires the entire block, giving size6. A GP set omitting c and contained in just one side can add c, so it is not maximal. A set meeting both sides but omitting c can add every vertex of A union B: this whole set is GP, since within-side distances are1and between-side distances are2. Its maximal completion is A union B, of size10. These exhaust all maximal GP sets. Thus gp^-(G)=6.

### True-twin saturation lemma

If x,y are adjacent true twins, meaning N[x]=N[y], then d(x,w)=d(y,w) for every w outside{x,y}. If a GP set contains x but not y, adding y preserves GP. Triples involving y but not x have the same distances as the corresponding triple with x. For a triple{x,y,w}, the distances are1,d,d with d>=1, so there is no triangle equality. Therefore any maximal GP set meeting a true-twin clique contains that entire clique.

### H has lower GP at least6

Each Q_ij is a six-vertex true-twin clique. Any maximal GP set meeting one has size at least6 by the lemma.

It remains to exclude a maximal GP set contained in the five original landmarks L={z,u_0,u_1,v_0,v_1}. In a diameter2 graph a GP set is exactly a vertex set inducing a disjoint union of cliques: a forbidden triple is exactly an induced three-vertex path. The inclusion-maximal GP subsets WITHIN L are precisely

    {u_0,u_1}, {v_0,v_1}, and {z,u_i,v_j} for i,j in{0,1}.

Indeed a set containing z must be a clique, and a nonclique subset of L contains one of the two nonadjacent pairs; including any other landmark then gives an induced three-vertex path. A smaller clique can still add z and then an unused endpoint from the other pair.

Each listed subset extends outside L. A member of Q_ij extends the triangle {z,u_i,v_j} by making a K4. A member of Q_00 extends {u_0,u_1} (it is adjacent only to u_0 of that pair) and also extends {v_0,v_1} (adjacent only to v_0). Every GP subset of L lies inside one of these maximal subsets, so it too has an outside extension. Hence no GP set contained entirely in L is maximal in H. This proves gp^-(H)>=6.

## 4. The five-point product set is GP

Cartesian distances add. Every path must move the requisite distance in each coordinate, and concatenated shortest factor paths attain the sum. In the order s_0,...,s_4 the distance matrix is

    0 2 2 3 3
    2 0 2 3 3
    2 2 0 2 2
    3 3 2 0 2
    3 3 2 2 0.

All off-diagonal distances are2or3. The sum of any two is at least4, greater than every possible third distance. Thus no three selected vertices are collinear on a geodesic, and S is GP.

## 5. S is inclusion-maximal: every outside vertex is blocked

Let x=(g,h) be a product vertex outside S. Every h!=z has distance2from at least one of u_0,u_1,v_0,v_1: an endpoint is nonadjacent to its paired endpoint; a Q_ijvertex is nonadjacent to u_(1-i) and v_(1-j). Also every h!=z is adjacent to z.

**Case g=c.** Here h!=z. Choose an endpoint w in{u_0,u_1,v_0,v_1} at distance2from h, and let s_t be the selected point having second coordinate w. Then

    d(x,s_2)=1, d(s_2,s_t)=2, d(x,s_t)=3.

So s_2 lies on an x–s_t geodesic.

**Case g in A.**
- If h=z, then d(x,s_2)=1, d(s_2,s_3)=2, d(x,s_3)=3.
- If h is not in{z,u_0,u_1}, there is j in{0,1} with d_H(h,v_j)=2. This holds for h=v_0,v_1 and for every Q-clique vertex. With t=3+j,

      d(x,s_2)=2, d(s_2,s_t)=2, d(x,s_t)=4.

- If h=u_i, then g!=a_0 because x is not selected. In this case

      d(x,s_i)=1, d(s_i,s_(1-i))=2, d(x,s_(1-i))=3.

Each subcase puts a selected point on a geodesic between x and another selected point.

**Case g in B.** Exchange A with B, a_0 with b_0, and the u-pair with the v-pair in the preceding argument. H's construction is invariant under that exchange (Q_ij is mapped to Q_ji), so the same three subcases cover every such x.

These cases exhaust all product vertices outside S. Every addition creates a forbidden GP triple, proving S maximal. Therefore gp^-(G square H)<=5. Together with the factor bounds this proves(C) and refutes the original conjecture. QED.


## 6. 验证范围

完整固定反例由 [Lean 源码](LowerGPProduct319.lean) 证明，实际运行及 15 项标准公理审计见 [JSON](lean-audit.json) 与 [日志](lean-audit.log)。其中任意最短实际简单路径与距离 GP 双向对应，单点不可扩张与全部包含极大等价，lowerGP 是真正的最小极大基数，产品为 Mathlib 的实际 boxProd。G 的下界使用三个明确大 GP 集的结构归约；H 的下界使用六点真孪生饱和及 32 个核心子集归约。

[独立复核](INDEPENDENT_REVIEW.md) 核对原定义、全部假设、源码和实际日志；[标准库验证程序](verify.py) 独立于发现者的构造程序重建邻接与全部 BFS 距离，给出 314 个外点的实际最短阻塞路径。该程序的原独立运行记录保留于复核材料，不把代码存在视为一次新的执行。

附加[无界差距族](FAMILY_PROOF.md) 已通过独立书面审查，尚未 Lean 化。固定反例无需依赖通用 min5 下界、全局最优值或此无限族。未证明最小反例阶、H 的精确 lowerGP 或完整产品最优值；不声明历史首次。AI 辅助研究及复核不等同人工同行评审。
