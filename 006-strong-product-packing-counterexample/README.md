# A counterexample to packing-domination inheritance in strong products

The self-contained English [research paper](paper/paper.pdf),
[standalone LaTeX source](paper/main.tex) and
[paper verification and academic-status record](paper/README.md)
give a conventional theorem-and-proof presentation of this construction.
Human author information and accountable approval are pending; substantial
AI involvement is disclosed, and no human peer-review or submission status
is claimed.

We construct a finite connected simple graph \(H\) with **608 vertices and
9,168 edges** such that

\[
  \gamma_2^3(Q_6)=\infty,
  \qquad
  \gamma_2^3(Q_6\boxtimes H)\le64.
\]

This is a counterexample, with a complete written proof, to **Conjecture 3.1**
of Bujtás, Iršič Chenoweth, Klavžar and Zhang, *On d-distance p-packing
domination number in strong products*. The conjecture assumes that **one**
factor has no packing-dominating set and asserts the same for its strong
product with **every** other graph; it does not assume both factors are bad.
[Original preprint, §3](https://arxiv.org/html/2510.02749v1),
[published article, DOI 10.1007/s00026-026-00814-0](https://link.springer.com/article/10.1007/s00026-026-00814-0).

The 64-center set below covers all **38,912** product vertices. We do not
claim that 64 is the minimum number of centers. The proof has independent
mathematical checks and two exact graph-distance replays. **The complete
existence-level counterexample is now Lean checked on actual finite
`SimpleGraph` objects and standard Mathlib `Walk`s**, including the all-subset
single-factor obstruction, all 608 auxiliary vertices, ordinary strong-product
edges and same-center coverage. The two new sources have 12 and 26 axiom
audits; an independent fresh-artifact rebuild compiled the factor and both
new sources, with 12+12+26 audits. Every run has zero errors, warnings and
nonstandard axioms. [Source-specific records](results/lean-verification.json)
retain the exact theorem scope. Historical priority has not been established.

## 1. Definitions and the original statement

For a finite nonempty simple undirected graph \(F\), a set \(D\subseteq V(F)\)
is a \(d\)-distance dominating set if every vertex is within graph distance
\(d\) of some member of \(D\). This closed-ball formulation is equivalent to
the original definition, which imposes the condition only on vertices outside
\(D\). It is a \(p\)-packing if distinct members have distance at least \(p+1\).
Write \(\gamma_d^p(F)=\infty\) if no set satisfies both conditions.

The original Conjecture 3.1 asserts

\[
 \gamma_d^p(G)=\infty
 \quad\Longrightarrow\quad
 \gamma_d^p(G\boxtimes H)=\infty
 \quad\text{for every graph }H.
\]

Our parameters \(d=2,p=3\) lie in its remaining interval \(d<p<2d\).
Both factors constructed here are finite, nonempty and connected.

Let \(V=\mathbb F_2^6\). Addition is coordinatewise XOR; write
\(\delta(x,y)=\operatorname{wt}(x+y)\), where weight counts the nonzero
coordinates. The cube \(Q_6\) joins words differing in exactly one coordinate.
Its actual graph distance is \(\delta\): any path must change each differing
coordinate, and changing precisely those coordinates realizes this length.

For connected graphs, the strong-product distance is

\[
 d_{G\boxtimes H}((x,h),(a,k))
   =\max\{d_G(x,a),d_H(h,k)\}.
\]

Each product step changes a factor coordinate by at most one edge, proving the
lower bound. Following shortest factor paths simultaneously, with the shorter
path waiting when it finishes, proves the upper bound. Thus a product vertex
is covered only when **the same center** is close in both factors.

## 2. The complete single-factor obstruction

**Lemma 1.** Every subset of \(V\) with pairwise distance at least four has
at most four members, and its radius-two balls do not cover \(V\).

**Proof.** For \(m\) binary words, let \(t_j\) be the number of ones in
coordinate \(j\). The sum of their unordered pair distances is

\[
 \sum_{u<v}\delta(u,v)=\sum_{j=1}^6t_j(m-t_j).
\]

Five words in a distance-four packing would have total pair distance at least
\(4\binom52=40\). Every coordinate contributes at most \(2\cdot3=6\),
giving a total at most 36. Any larger packing contains five words, so the
packing has at most four members. This is the classical Plotkin counting
argument.

Each radius-two cube ball has
\(1+6+\binom62=22\) vertices. Zero, one or two centers therefore cover
fewer than 64 vertices.

For three centers the distance sum is at least 12 and at most
\(6\cdot2=12\), so all three pair distances equal four. For four centers
the corresponding bounds are both 24, so all six pair distances equal four.
After translating one center to zero, every other center has weight four.
Two such words have distance four exactly when their two-element zero sets
are disjoint. Consequently three centers use two disjoint zero pairs, while
four centers use a partition of the six coordinates into three zero pairs.

For any two distance-four centers, their radius-two balls intersect in six
vertices: after translating one to zero, a common vertex must have weight two
supported on the four nonzero coordinates of the other center. For any three
pairwise distance-four centers, the three balls have exactly one common
vertex. In the normalized description this is the weight-two word on the two
coordinates outside the two zero pairs.

In a four-center packing that unique triple-intersection vertex is distance
six from the remaining center, so the fourfold intersection is empty.
Inclusion–exclusion gives the exact covered sizes

\[
 3\cdot22-3\cdot6+1=49,
 \qquad
 4\cdot22-6\cdot6+4\cdot1=56.
\]

Both are less than 64. This proves the lemma for **all subsets**, including
nonlinear ones, and therefore \(\gamma_2^3(Q_6)=\infty\). ∎

The earlier [complete factor proof](../notes/q6-strong-product-affine-obstruction.md)
and its [Lean source](../notes/proof/Q6PackingDomination.lean) establish the
same factor obstruction. The source-specific
[verification receipt](../notes/results/q6-packing-domination-verification.json)
records actual compilation and 12 axiom audits; its theorem covers every
subset of the actual six-bit Hamming space.

## 3. The auxiliary graph

Let

\[
 \mathcal P_4=\{\{a,b\}\subseteq V:\delta(a,b)=4\}.
\]

Construct \(H\) using three **disjoint tagged** sets of vertices:

\[
 \{A_a:a\in V\},\qquad
 \{S_a:a\in V\},\qquad
 \{E_P:P\in\mathcal P_4\}.
\]

The first set consists of code nodes. Call the other two sets Steiner nodes
and assign their supports by

\[
 \sigma(S_a)=\{a\},\qquad \sigma(E_P)=P.
\]

An edge of \(H\) is exactly one of the following:

1. \(A_aT\), where \(T\) is a Steiner node and \(a\in\sigma(T)\).
2. \(TU\), where \(T,U\) are **distinct** Steiner nodes and every two
   **distinct words** in \(\sigma(T)\cup\sigma(U)\) have distance at least
   four.

There are no edges between code nodes, no loops, and no other edges. The
support union is a set: shared endpoint words are counted once and are not
compared with themselves. Adjacency is symmetric, so this defines an actual
finite simple undirected graph, rather than a proposed table of distances.

Each word has \(\binom64=15\) distance-four neighbors. Hence
\( |\mathcal P_4|=64\cdot15/2=480\) and \( |V(H)|=608\).

The graph is connected. Let \(\mathbf1=(1,1,1,1,1,1)\), write
\(\bar a=a+\mathbf1\), and let \(e_i\) be a coordinate word. Both edges

\[
 S_a\;-\;S_{\bar a}\;-\;S_{a+e_i}
\]

exist, because the corresponding label distances are six and five. Thus every
coordinate flip between singleton labels is realized by a two-step path, and
all singleton nodes belong to one component. Each code node is attached to
its singleton node, and each pair node is attached to its endpoint code
nodes. All vertices of \(H\) therefore belong to this component.

## 4. Short paths cannot spoil the product packing

**Lemma 2.** If \(a\ne b\) and \(d_H(A_a,A_b)\le3\), then
\(\delta(a,b)\ge4\).

**Proof.** No path of length one exists, because there are no code–code
edges. A path of length two has form \(A_a-T-A_b\), so both \(a,b\) belong
to \(\sigma(T)\). A singleton support cannot contain both words; the pair
support must be \(\{a,b\}\in\mathcal P_4\), giving distance four.

A path of length three has form \(A_a-T-U-A_b\), with both internal nodes
Steiner: an internal code node would create a code–code edge at one end.
The edge \(TU\) forces all distinct words in their support union to be
pairwise distance at least four. Since this union contains \(a,b\), the
conclusion follows. These cases include shared-endpoint pair nodes and
exhaust all short paths. ∎

Define

\[
 C=\{(a,A_a):a\in V\}\subseteq V(Q_6\boxtimes H).
\]

This is a set of exactly 64 distinct centers. For two different labels \(a,b\),
if \(\delta(a,b)\ge4\), the first factor supplies separation four. Otherwise
Lemma 2 gives \(d_H(A_a,A_b)\ge4\). The strong-product maximum-distance
formula proves that \(C\) is a **3-packing**.

## 5. Every graph node sees enough code labels to cover the cube

For \(h\in V(H)\), let

\[
 L(h)=\{a\in V:d_H(h,A_a)\le2\}.
\]

We prove that each \(L(h)\) radius-two covers \(V\), treating every node type.

### Code nodes and singleton nodes

For \(a\in V\), put
\(L_a=\{a\}\cup\{b:\delta(a,b)=4\}\).
This set radius-two covers \(V\). After translating \(a\) to zero, words of
weight at most two are covered by zero. A weight-three word extends to a
weight-four word at distance one; a weight-four word is itself in the set;
a weight-five word contains a weight-four subset at distance one; and a
weight-six word is distance two from any weight-four word. These are all 64
possible query words, grouped by weight.

We have \(L_a\subseteq L(A_a)\): when \(\delta(a,b)=4\), the path
\(A_a-E_{\{a,b\}}-A_b\) has length two. Also
\(L_a\subseteq L(S_a)\): \(S_a\) is adjacent to \(A_a\), and for each such
\(b\), the path \(S_a-S_b-A_b\) has length two. Thus both node types have the
required covering property.

### Pair nodes: an exact eight-label covering set

Let \(P=\{a,b\}\in\mathcal P_4\). The code nodes \(A_a,A_b\) are adjacent
to \(E_P\). If a word \(c\notin P\) satisfies
\(\delta(c,a)\ge4\) and \(\delta(c,b)\ge4\), then
\(E_P-S_c-A_c\) is a two-step path. Consequently

\[
 K(a,b)=\{a,b\}\cup
   \{c:\delta(c,a)\ge4,\ \delta(c,b)\ge4\}
 \subseteq L(E_P).
\]

Translate \(a\) to zero and permute coordinates so \(b=(1111,00)\). Then

\[
 K(a,b)=\{(0000,00),(1111,00)\}
       \cup\{(u,11):u\in\mathbb F_2^4,\ \operatorname{wt}(u)=2\}.
\]

Indeed, for \(c=(r,s')\), putting \(t=\operatorname{wt}(r)\) and
\(s=\operatorname{wt}(s')\), the two compatibility inequalities give
\(t+s\ge4\) and \(4-t+s\ge4\). Since \(s\le2\), they force \(t=s=2\).
Thus there are exactly six compatible nonendpoint words and eight labels
altogether.

For an arbitrary query \(x=(r,s')\), the distances to the two endpoints are
\(t+s\) and \(4-t+s\). The least distance to the six other words is

\[
 \min_{\operatorname{wt}(u)=2}\delta(x,(u,11))
       =|t-2|+2-s.
\]

The overlap of \(u\) with the support of \(r\) can be made
\(\min(t,2)\), which proves the formula and realizes its minimum. Therefore
the least distance from \(x\) to \(K(a,b)\) is

\[
 \min\{t+s,\ 4-t+s,\ |t-2|+2-s\}.
\]

It is at most two for all \(0\le t\le4\), \(0\le s\le2\). For \(t=0,4\)
use the relevant endpoint. For \(t=1,3\), use an endpoint when \(s\le1\),
and a word \((u,11)\) when \(s=2\). For \(t=2\), the third expression is
\(2-s\le2\). This exact argument covers every query word, including all
parities and boundary weights. It proves the pair-node case.

## 6. The same centers dominate the full product

Fix an arbitrary vertex \((x,h)\in V(Q_6\boxtimes H)\). Section 5 proves
that \(L(h)\) radius-two covers \(V\). Choose **one label** \(a\in L(h)\)
with \(\delta(x,a)\le2\). By the definition of \(L(h)\), its own code node
satisfies \(d_H(h,A_a)\le2\). Hence

\[
 d_{Q_6\boxtimes H}((x,h),(a,A_a))
       =\max\{\delta(x,a),d_H(h,A_a)\}\le2.
\]

Thus \(C\) is a 2-distance dominating set as well as a 3-packing. Lemma 1
and this explicit construction prove

\[
 \boxed{\gamma_2^3(Q_6)=\infty,
        \qquad \gamma_2^3(Q_6\boxtimes H)\le64.}
\]

This contradicts the original universal claim of Conjecture 3.1. It does
not determine the exact product domination number or solve the separate
nonlinear packing problem in \(Q_6\boxtimes Q_6\).

## 7. Edge count and the close-vertex consistency check

The edge count can be obtained directly from the definition:

| Edge type | Count |
| --- | ---: |
| Code–Steiner incidences | \(64+2\cdot480=1,024\) |
| Singleton–singleton | \(64(15+6+1)/2=704\) |
| Singleton–pair | \(480\cdot8=3,840\) |
| Pair–pair, one shared endpoint | \(64(15\cdot6/2)=2,880\) |
| Pair–pair, disjoint supports | \(240\cdot3=720\) |
| **Total** | **9,168** |

For singleton–pair edges, the eight compatible singleton labels are precisely
the endpoints and the six words computed in Section 5. For pair nodes with a
shared endpoint, translate that endpoint to zero: their other labels have
weight four and disjoint zero pairs. There are \(15\cdot6/2=45\) choices
per endpoint. For disjoint supports, their union is a four-word
distance-four packing. Such a packing is determined by a translated zero
and a partition of the six coordinates into three zero pairs. There are
\(64\cdot15/4=240\) distinct four-word packings, each giving three partitions
into two pair supports.

The original Theorem 3.3 supports the conjecture when the **other factor**
\(H\) has a \((2,3)\)-close vertex, meaning that its radius-two ball has
diameter at most three. Our \(H\) has none. For a code or singleton node,
choose two weight-four translated labels sharing three nonzero coordinates
in its covering set. For a pair node, choose two words \((u,11)\) whose
weight-two first blocks share one coordinate. In either case their labels
are distance two apart in the cube, and both code nodes are within two of
the fixed graph node. Lemma 2 makes their \(H\)-distance at least four;
the triangle inequality makes it at most four. It is therefore exactly
four. Every radius-two ball in \(H\) has diameter at least four, so the
construction does not violate that supporting theorem's hypothesis.

## 8. Verification scope and attribution

The written proof above uses actual graph edges and shortest paths. Exact
graph replay checks the 608 vertices, 9,168 edges, all pairs of the 64
specified centers, and all 38,912 product targets. Its role is to check the
explicit construction independently of the symbolic covering argument.

The new [geometry source](proof/Q6PackingComplexGeometry.lean) proves the
actual six-bit metric, one-edge distance reduction and both label-covering
lemmas with ordinary kernel-checked `decide` certificates. The
[graph source](proof/Q6PackingComplexCounterexample.lean) defines the canonical
480 unordered pairs and the entire 608-node finite simple graph. It proves
the ordinary strong-product adjacency formula, an at-most-length reachability
predicate equivalent to **standard Mathlib Walks**, the cube's Hamming/path
bridge, all short-path exclusions, the same-center covering theorem and
`original_existence_counterexample`.

The last theorem has no remaining geometric, linearity, cardinality or
external-certificate premise: it combines nonexistence of **any** valid set
in the actual cube graph with existence of the displayed valid set in its
actual strong product. It formalizes the existence content of the original
gamma-infinity/finite claim. The file does not define the numerical minimum
gamma function or use a numerical `SimpleGraph.dist` function. The 608-node
cardinality is a Lean theorem; connectedness, the 9,168-edge count and the
exact maximum distances are verified by the written argument and exact
BFS, rather than separate Lean declarations. The actual final endpoint uses
only `propext`, `Classical.choice` and `Quot.sound`; no `sorry`,
`native_decide`, added axiom or Python certificate is used as a proof.

[Primary and independent Lean receipts](results/lean-verification.json)
include source hashes, actual UTC intervals, exit codes and every printed
axiom list. The independent replay builds all three project modules in a
new object directory from their actual sources. The
[explicit graph](results/graph.json), [distance/cover certificate](results/certificate.json),
[primary exact record](results/graph-verification.json),
[independent full-BFS record](results/independent-graph-verification.json)
and [certificate comparison](results/independent-certificate-comparison.json)
make the finite evidence inspectable. The independent exact checker examines
all 608 BFS rows (369,664 distances), certifies shortest paths by edge
Lipschitz and descending-neighbor conditions, and checks all 2,016 center
pairs and 38,912 same-center targets before comparing with the first checker.

From the repository root, with Python 3.10+ and the pinned package prepared:

```sh
python 006-strong-product-packing-counterexample/verify_graph.py /tmp/q6-primary-new
python 006-strong-product-packing-counterexample/verify_independent.py own --out /tmp/q6-independent-new
python 006-strong-product-packing-counterexample/verify_independent.py compare --out /tmp/q6-independent-new --root /tmp/q6-primary-new
python 006-strong-product-packing-counterexample/verify_lean.py --out /tmp/q6-lean-new
```

Supply fresh output directories; they are never silently reused. On Windows
use fresh local paths in place of `/tmp/...`, and `--lake PATH_TO_LAKE` when
Lake is not on PATH. The isolated package is
`002-weighted-rectangular-pruning/proof/mathlib`, pinned to Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` and Lean 4.34.1. If its fixed
dependency artifacts have not been obtained, prepare that package with
`lake update` and `lake exe cache get Mathlib.Combinatorics.SimpleGraph.Walk.Basic
Mathlib.Data.Fintype.Prod Mathlib.Data.Fintype.Sum Mathlib.Data.Fin.VecNotation`
before the serial Lean replay. All three project sources are rebuilt rather
than accepted through old project objects.

The factor counting method is classical; the graph-product distance formula
is standard and is also recalled in the original paper. The construction and
its complete written argument are recorded here without a first-discovery
or historical-priority claim. The preprint and published conjecture are
identified above so that the exact statement and its relation to this
counterexample can be checked directly.

Current original-source and subsequent-work checks are recorded in [LITERATURE.md](LITERATURE.md). Their limits remain separate from mathematical correctness.
