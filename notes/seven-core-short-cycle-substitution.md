# A sharp bound for seven-core short-cycle substitutions

We determine the largest minimum-outdegree ratio in one explicit family of
triangle-free oriented graphs that avoid a transitive tournament on nine vertices:

\[
 \max_G\frac{\delta^+(G)}{|V(G)|}
 =\frac{260889}{805108}<\frac{21}{64}<\frac13.
\]

The family allows arbitrary nesting depths and different positive blow-up factors
in its seven clusters. This is a complete bound for the family defined below,
not a solution of a general short-cycle conjecture. Historical originality of
this particular bound has not been established.

The graph classification and its integer realization have complete written
proofs below. [Lean](proof/SevenCoreSubstitutionCertificate.lean) proves the
seven-row inequality, its positive rational equality witness and both strict
threshold comparisons. The graph-to-row reduction is not formalized.

## 1. Definitions and statement

All graphs are finite. An oriented graph has no loops, parallel arcs or digons.
Outdegree counts distinct vertices. Write \(T_s\) for the transitive tournament
on \(s\) vertices and \(t(H)\) for the largest transitive tournament in a nonempty
oriented graph \(H\).

Let \(B\) have vertices \(\mathbb Z/7\mathbb Z\) and arcs
\(i\to i+1,i+2\). Let \(F_0\) be one vertex and recursively let
\(F_k=C_4[F_{k-1}]\), where \(C_4\) is the directed four-cycle and square
brackets denote lexicographic substitution. An arc between two outer vertices
places all arcs in that direction between their clusters.

For each of the **seven nonempty** clusters, choose integers \(k_i\ge0\) and
\(m_i\ge1\). Replace every vertex of \(F_{k_i}\) by an independent set of the
**same size \(m_i\) within that cluster**. Call the resulting graph \(H_i\),
and form \(G=B[H_0,\ldots,H_6]\). Different clusters may have different factors.
Nonuniform blow-ups within a cluster and zero-size outer clusters are outside
this statement.

**Theorem.** Every graph in this family is triangle-free and oriented. Among
those with no \(T_9\), the maximum of \(\delta^+(G)/|V(G)|\) is exactly
\(\gamma=260889/805108\). A finite graph attains it; hence this is a maximum,
not just a continuous relaxation or limiting supremum.

## 2. The complete depth restriction

The outer graph has no directed triangle: three positive steps from \(\{1,2\}\)
sum to a number between three and six, never a multiple of seven. Substitution
preserves the absence of loops, digons and directed triangles. A triangle inside
one cluster would be an internal triangle; one using two clusters cannot return
against their single direction; one using three clusters projects to an outer
triangle. Induction applies this also to every \(F_k\).

Every three-vertex tournament in \(B\) is transitive. Its source must use both
out-neighbors, so these tournaments are exactly
\(\{i,i+1,i+2\}\). There is no larger transitive tournament, since its source
would need three out-neighbors.

For any lexicographic substitution, a transitive tournament projects to an
outer transitive tournament, and its intersection with each cluster is an
internal transitive tournament. Conversely, maximum internal tournaments can
be joined along any outer transitive tournament. Thus

\[
 t(B[H_i])=\max_{A\text{ an outer transitive tournament}}
                 \sum_{i\in A}t(H_i).
\]

Independent-set blow-up does not change \(t\). Since \(t(C_4)=2\), induction
gives \(t(H_i)=2^{k_i}\). Every outer arc and singleton extends to a consecutive
triple, so \(G\) is \(T_9\)-free exactly when

\[
 2^{k_i}+2^{k_{i+1}}+2^{k_{i+2}}\le8\qquad(i\bmod7).
\]

These conditions are equivalent to the following complete classification:
all \(k_i\le2\), and positions with \(k_i=2\) have pairwise circular distance
at least three. Indeed, a depth at least three contributes eight together with
at least one vertex of a neighboring nonempty cluster. Two depth-two positions
within distance two contribute at least \(4+4+1=9\) in a triple. Conversely,
each triple with at most one depth-two position contributes at most \(4+2+2=8\).

There are at most two depth-two positions: three circular gaps of at least
three cannot sum to seven. A pair must be a rotation of \(\{0,3\}\). Every valid
depth profile is therefore coordinatewise dominated, after a rotation, by

\[
 (k_0,\ldots,k_6)=(2,1,1,2,1,1,1).
\]

This covers all depths without enumerating profiles.

## 3. Exact degree optimization

The order and outdegree of \(F_k\) are \(4^k\) and \((4^k-1)/3\). The latter
follows from \(d_k=4^{k-1}+d_{k-1}\), \(d_0=0\). Its internal degree ratio is
\(c_k=(1-4^{-k})/3\), with \(c_0=0,c_1=1/4,c_2=5/16\).

Put \(n_i=4^{k_i}m_i\), \(N=\sum n_i\), and \(w_i=n_i/N\). Every vertex in
cluster \(i\) has total outdegree ratio

\[
 c_{k_i}w_i+w_{i+1}+w_{i+2}.
\]

Increasing an internal coefficient increases one row and does not decrease any
other row. The classified dominating profile consequently gives an upper bound
for the whole family. Let \(M\) have diagonal \(5/16\) at positions zero and
three, diagonal \(1/4\) elsewhere, entries one at \((i,i+1),(i,i+2)\), and zero
elsewhere. It suffices to maximize \(\min_i(Mw)_i\) over positive \(w\) of sum one.

Here are exact primal and dual numerators with common denominator \(D=201277\):

| i | primal numerator a_i | dual numerator b_i | 16 M diagonal |
| ---: | ---: | ---: | ---: |
| 0 | 27892 | 31028 | 5 |
| 1 | 29749 | 26757 | 4 |
| 2 | 26757 | 29749 | 4 |
| 3 | 31028 | 27892 | 5 |
| 4 | 27505 | 30325 | 4 |
| 5 | 28021 | 28021 | 4 |
| 6 | 30325 | 27505 | 4 |

Both vectors are positive and both numerator sums equal \(D\). If
\(s_i=16M_{ii}\), the fourteen integer identities are

\[
 s_i a_i+16a_{i+1}+16a_{i+2}=1043556,
 \qquad
 s_j b_j+16b_{j-1}+16b_{j-2}=1043556.
\]

Thus \(p=a/D\), \(q=b/D\) satisfy
\(Mp=\gamma\mathbf1\), \(M^Tq=\gamma\mathbf1\), where
\(\gamma=1043556/(16D)=260889/805108\). For every nonnegative \(w\) of sum one,

\[
 \min_i(Mw)_i\le\sum_iq_i(Mw)_i
 =\sum_j(M^Tq)_jw_j=\gamma.
\]

The positive vector \(p\) attains equality in every row. No assumption about an
optimizer or a numerical solver is needed. The exact threshold gaps are

\[
 \frac{21}{64}-\gamma=\frac{52593}{12881728}>0,
 \qquad
 \frac13-\gamma=\frac{22441}{2415324}>0.
\]

## 4. Attainment by an actual finite graph

Take \(N=16D=3220432\), \(n_i=16a_i\), and the dominating depth profile.
Use the following positive integer factors:

| i | depth k_i | cluster order n_i | uniform internal blow-up m_i |
| ---: | ---: | ---: | ---: |
| 0 | 2 | 446272 | 27892 |
| 1 | 1 | 475984 | 118996 |
| 2 | 1 | 428112 | 107028 |
| 3 | 2 | 496448 | 31028 |
| 4 | 1 | 440080 | 110020 |
| 5 | 1 | 448336 | 112084 |
| 6 | 1 | 485200 | 121300 |

The internal outdegree is \(5m_i\) in a depth-two cluster and \(m_i\) otherwise;
the external outdegree is \(n_{i+1}+n_{i+2}\). Their sum is exactly 1043556 in
every cluster. This proves attainment in the specified finite graph family.
The graph is **out-regular**; its indegrees are not all equal. For example,
cluster-zero vertices have indegree \(139460+485200+448336=1072996\).

The construction is an exact adjacency rule; no adjacency matrix with millions
of rows needs to be materialized. All graph hypotheses follow from Sections
1–2, rather than from sampling vertices.

## 5. Relation to the original questions and verification

The original Caccetta–Häggkvist three-cycle question asks whether a nonempty
loopless simple digraph with \(3\delta^+\ge N\) must contain a cycle of length
at most three. Steiner's [2026 v2 introduction, Conjecture 1 and the following
paragraph](https://arxiv.org/html/2604.13700v2) explicitly records the girth-four
case as still open. The version was submitted on 26 April 2026, according to
the [version history](https://arxiv.org/abs/2604.13700).

Grzesik's [2017 original paper, Conjecture 3, k=3](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i2p19/pdf/)
proposes \(21N/64\) as an upper bound for triangle-free \(T_9\)-free oriented
graphs. This is the second reference threshold above. The current general
status of that particular strengthening has not been sufficiently confirmed
here. Its k=1 and k=2 cases are proved in the source; none is reproposed as an
open target. Our finite-family theorem is independent of the conjecture's status.

Lexicographic short-cycle constructions and nested four-cycles are established
tools discussed in that source. The calculation here only determines the
precisely specified heterogeneous seven-core family. It supplies no general
CH proof, no counterexample to either source conjecture and no historical
priority claim. Its sharp gap rules out obtaining such a counterexample merely
by increasing nesting depths or retuning the seven cluster sizes in this family.

The [exact certificate](results/seven-core-substitution-exact.json) and
[standard-library checker](code/check_seven_core_substitution.py) independently
verify the primal/dual equations, strict gaps and integer realization:

```sh
python notes/code/check_seven_core_substitution.py
```

With the fixed Lean 4.34.1 / Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` environment already described in
[FORMALIZATION.md](../FORMALIZATION.md), run from its Mathlib proof package:

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../notes/proof/SevenCoreSubstitutionCertificate.lean
```

Three declarations are audited. Their only axioms are `propext`,
`Classical.choice` and `Quot.sound`; no `sorryAx`, added axiom or `native_decide`
is used. [Verification records](results/seven-core-substitution-verification.json)
separate actual author and independent Lean runs from independent written graph
review and exact arithmetic checks. The Lean boundary remains algebraic: the
actual graph construction, transitive-tournament classification and profile
domination are written results, not kernel-checked graph declarations.
