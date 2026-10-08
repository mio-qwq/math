# Sharp local pair-cost bounds for nested coordinate relations

Research note, 8 October 2026.

This note extends the [block and four-path expansion theorem](binary-one-side-costs.md)
to arbitrarily many nested neighborhood layers. One coordinate relation
may be a disjoint union of bipartite components whose left neighborhoods
are totally ordered by inclusion; the other relation is arbitrary.
Original and corner costs are independent nonnegative real numbers,
subject only to the inequalities at actual conflicts.
A suffix-budget induction gives a finite construction directly at zero
costs. This is a written theorem, not a Lean proof or a historical
priority claim.

## 1. Definitions and theorem

Use the conflict/coverage framework of [compatible-pair-costs.md](compatible-pair-costs.md).
For finite sets \(P,I,S,J\), let
\(E\subseteq P\times I\), \(F\subseteq S\times J\),
\(R\subseteq P\times J\), and \(C\subseteq I\times S\).
The originals \(r=(p,j)\) and \(c=(i,s)\) conflict exactly when
\(E(p,i)\) and \(F(s,j)\). The actual cross-corners are
\[
H=\{(p,s):\exists i,j\ ((p,j)\in R,(i,s)\in C,E(p,i),F(s,j))\},
\]
\[
Z=\{(i,j):\exists p,s\ ((p,j)\in R,(i,s)\in C,E(p,i),F(s,j))\}.
\]
An \(R\) original covers \((i,j)\) if \(E(p,i)\);
a \(C\) original covers \((i,j)\) if \(F(s,j)\).
The augmented graph has tagged sides \(R\sqcup Z_L\) and \(C\sqcup Z_R\),
with the original conflicts, edges from covering \(R\)'s to \(Z_R\),
and edges from \(Z_L\) to covering \(C\)'s. It has no \(Z_L\)--\(Z_R\) edges.

Assign costs \(x_{pj},y_{is},h_{ps},z_{ij}\ge0\), with cost \(z_{ij}\)
on both copies of each actual \(Z\). Assume
\[
x_{pj}y_{is}\le h_{ps}z_{ij}
\quad\text{at every actual conflict}. \tag{1}
\]
Call a nonisolated component *nested* when its neighborhoods on the
left coordinate side are totally ordered by inclusion.

**Theorem.** If every nonisolated component of either \(E\) or \(F\)
is nested, the augmented graph has a vertex cover containing no isolated
vertex and of cost at most
\[
\sum_H h+\sum_Z z. \tag{2}
\]
There are conflict-free original survivors retaining every initially
conflict-free original, with deletion cost \(D_{\rm del}\) satisfying
\[
D_{\rm del}\le \sum_Hh+\sum_{(i,j)\in U}z_{ij}, \tag{3}
\]
where \(U\) is the actual set of corners covered by no survivor.
The coefficient one is sharp. Rational inputs admit a deterministic
finite construction.

There is no bound on the size or structure of the other relation.
Partial original families and empty relations are included.
A complete block is a one-layer nested component, and a complete
four-path expansion is a two-layer one. The theorem does not assert
(1) suffices for two unrestricted relations.

## 2. Scalar chains, completion and prefix normalization

First suppose \(n\ge1\),
\[
P=I=\{0,\ldots,n-1\},\qquad E(p,i)\iff p\le i, \tag{4}
\]
and \(R=P\times J,\ C=I\times S\) are full families.
Temporarily remove isolated coordinates of \(F\), retaining their
originals. If no \(F\) edge remains, there is no conflict or actual
corner and the conclusion is immediate. Otherwise all remaining
\(H=P\times S\) and \(Z=I\times J\) corners are actual.

For conflict-free survivors, a corner cannot have both an \(R\) survivor
and a \(C\) survivor covering it: those two originals would conflict.
Its cheapest augmented completion therefore costs
\[
\sum_Zz+D_{\rm del}-\sum_Uz. \tag{5}
\]
Indeed, a corner covered from one survivor side forces the opposite
tag into the cover, costing \(z\); a corner covered from neither side
forces no tag. We prove the adjusted deletion bound
\(D_{\rm del}-\sum_Uz\le\sum_Hh\).

We may normalize the \(R\) deletions in every column to a prefix.
If a level \(p\) survives, add all levels \(q>p\) to the survivors.
Their conflict neighborhoods and their corner-coverage neighborhoods
are subsets of those of \(p\). This creates no conflict, leaves \(U\)
unchanged and weakly reduces the deletion cost. Thus the deleted levels
are \(\{0,\ldots,k-1\}\) and the surviving levels its complementary suffix.
This normalization also applies to zero original costs.

For \(n=1\), the [block theorem](compatible-pair-costs.md) proves the
claim, including zeros and isolated originals.
Assume the scalar theorem for \(n-1\) and write \(\ell=n-1\).
Sections 3--6 construct its \(n\)-layer successor.

## 3. The last C layer and high-row coupling

Put
\[
D_s=y_{\ell s},\qquad q_s=\sum_{p=0}^{\ell}h_{ps}.
\]
Partition \(S\) into high rows \(S_H=\{s:D_s>q_s\}\)
and low rows \(S_L=S\setminus S_H\).
For high \(s\), let
\(\rho_s=q_s/D_s\in[0,1)\); its denominator is positive.

Let \(J_H\) be the columns neighboring a high row and
\(J_L=J\setminus J_H\). Make these decisions:

- Delete every \(R\) level in \(J_H\).
- Retain all \(C\)'s of levels \(i<\ell\) in high rows.
- Delete every last-layer \(C\) in low rows.
- For high last-layer \(C\)'s, use one common threshold
  \(T\in(0,1]\), deleting the original iff \(T\le\rho_s\).

All higher corners in a high-neighbor column are covered by retained
high \(C\)'s. Its last corner, of cost \(w_j=z_{\ell j}\),
is uncovered exactly when all adjacent high last-layer \(C\)'s
are deleted, since all low last-layer \(C\)'s and all its \(R\)'s
are deleted. Under a uniform threshold this has probability
\[
m_j=\min_{s\in S_H:F(s,j)}\rho_s.
\]
Summing (1) at \(i=\ell\) over all \(p\) gives
\[
\left(\sum_p x_{pj}\right)D_s\le q_s w_j,
\qquad
\sum_p x_{pj}\le m_jw_j. \tag{6}
\]
Thus the expected adjusted contribution of each high-neighbor column
is nonpositive. The expected high last-\(C\) deletion cost is
\(\sum_{S_H}D_s\rho_s=\sum_{S_H}q_s\).
The retained high higher-\(C\)'s have no surviving \(R\) neighbor.

This probability calculation is a finite convex combination.
Order the distinct positive \(\rho_s\)'s, append 1, and assign
to each endpoint the length of the interval preceding it, starting
at 0. The resulting finite threshold distribution has the same
marginals and simultaneous minima. A zero ratio never causes a deletion.
If there are no high rows, the sole choice is \(T=1\).

## 4. Pooling the last-corner profit into suffix costs

For a low-only column \(j\in J_L\), put
\[
d_j=x_{\ell j},\quad w_j=z_{\ell j},\quad L_j=(w_j-d_j)^+,
\]
\[
A_p(j)=\sum_{r=p}^{\ell-1}x_{rj}
\quad(0\le p<\ell),\qquad A_\ell(j)=0. \tag{7}
\]
All its neighboring last-layer \(C\)'s have already been deleted.
If any higher \(R\) survives, retain the last \(R\) too:
it creates no conflict and changes no corner coverage.
If all higher \(R\)'s are deleted, delete the last \(R\) exactly
when \(d_j<w_j\). The adjusted column cost after its last-corner
profit is then
\[
A_0(j)-L_j. \tag{8}
\]

Let \(N=\{j\in J_L:A_0(j)<L_j\}\). For these columns, \(L_j>0\)
and \(d_j<w_j\); delete all \(n\) originals.
Their adjusted contributions after the last-corner profits are
negative. Any additional higher uncovered-corner profit only improves
this estimate.

On the remaining good columns \(G=J_L\setminus N\), define virtual
higher-level costs
\[
b_{pj}=(A_p(j)-L_j)^+-(A_{p+1}(j)-L_j)^+
\quad(0\le p<\ell). \tag{9}
\]
These satisfy
\[
0\le b_{pj}\le x_{pj},\qquad
\sum_{p=0}^{\ell-1}b_{pj}=A_0(j)-L_j\ge0. \tag{10}
\]
They pool the nonnegative last-corner profit against the higher
original costs, starting from the bottom.

For each low row \(s\), define the H-budget suffix
\[
Q_p(s)=\sum_{r=p}^{\ell}h_{rs}.
\]
The residual budgets are
\[
k_{ps}=(Q_p(s)-D_s)^+-(Q_{p+1}(s)-D_s)^+
\quad(0\le p<\ell-1),
\]
\[
k_{\ell-1,s}=(Q_{\ell-1}(s)-D_s)^+. \tag{11}
\]
They are nonnegative and telescope to
\[
\sum_{p=0}^{\ell-1}k_{ps}=q_s-D_s. \tag{12}
\]
The special last term combines the last two original H levels;
discarding the final H level separately would lose budget when
\(D_s\le h_{\ell s}\).
For \(\ell=1\), only the special last term occurs.

## 5. Preservation of every residual local inequality

For a low edge \(F(s,j)\) with \(j\in G\), we prove
\[
b_{pj}y_{is}\le k_{ps}z_{ij}
\quad\text{whenever }p\le i<\ell. \tag{13}
\]
All divisions below follow a proof that the denominator is positive.

If \(D_s\le Q_{p+1}(s)\), the ordinary terms of (11) give
\(k_{ps}=h_{ps}\); at \(p=\ell-1\) they give
\(k_{ps}=h_{ps}+h_{\ell s}-D_s\ge h_{ps}\).
Now \(b_{pj}\le x_{pj}\) and (1) prove (13).

Suppose \(D_s>Q_{p+1}(s)\), so \(D_s>0\).
Summing the last-\(C\) inequalities for deeper levels gives
\[
\left(\sum_{r=p+1}^{\ell}x_{rj}\right)D_s
\le Q_{p+1}(s)w_j.
\]
Since \(L_j\ge w_j-d_j\),
\[
L_j-A_{p+1}(j)
\ge w_j-\sum_{r=p+1}^{\ell}x_{rj}
\ge \frac{w_j(D_s-Q_{p+1}(s))}{D_s}\ge0. \tag{14}
\]
Therefore (9) reduces to
\[
b_{pj}=(x_{pj}-(L_j-A_{p+1}(j)))^+.
\]
If \(h_{ps}=0\), the original last-\(C\) inequality
\(x_{pj}D_s\le h_{ps}w_j\) forces \(x_{pj}=0\), hence \(b_{pj}=0\).
If \(h_{ps}>0\), that inequality implies
\(w_j/D_s\ge x_{pj}/h_{ps}\). Substitution in (14) gives
\[
b_{pj}\le
x_{pj}\left(1-\frac{D_s-Q_{p+1}(s)}{h_{ps}}\right)^+
=\frac{x_{pj}(Q_p(s)-D_s)^+}{h_{ps}}. \tag{15}
\]
In this case (11), including its special last term, gives
\(k_{ps}=(Q_p(s)-D_s)^+\).
Multiplying (15) by \(y_{is}\ge0\) and applying (1) proves (13).
This argument includes zero \(w_j,k_{ps},x_{pj}\);
\(D_s=0\) belongs to the first case.

Apply the induction hypothesis to the \(\ell\)-layer residual problem
on columns \(G\), rows \(S_L\), and relation \(F|_{S_L\times G}\),
using original costs \(b_{pj},y_{is}\), H costs \(k_{ps}\)
and corner costs \(z_{ij}\) for \(i<\ell\).
Its adjusted deletion value is at most
\[
\sum_{\text{active residual H}}k_{ps}
\le\sum_{s\in S_L}(q_s-D_s). \tag{16}
\]
Retain isolated residual originals; an empty residual relation
requires no deletions. Normalize its \(R\) deletions to prefixes
as in Section 2. This can only improve its adjusted value.

## 6. Lifting the virtual pruning to the actual graph

Fix a good column and let its virtual deleted prefix have length
\(0\le k\le\ell\). Its virtual R deletion cost is exactly
\[
\sum_{p<k}b_{pj}
=(A_0(j)-L_j)^+-(A_k(j)-L_j)^+. \tag{17}
\]
Since \(A_0(j)\ge L_j\), the following branches preserve the budget.

If \(L_j=0\) or \(A_k(j)\ge L_j\), delete the same actual higher
prefix, retain its higher suffix, and retain the last \(R\).
The cost in (17) equals
\(A_0(j)-A_k(j)=\sum_{p<k}x_{pj}\).
When \(L_j>0\), the remaining suffix has positive total cost,
so at least one higher \(R\) survives and covers the last corner.
When \(L_j=0\), the retained last \(R\) covers it even if \(k=\ell\).
The higher uncovered corners agree exactly with the virtual state:
the same higher R's survive, the last R cannot cover a higher
corner, and this column has no high C neighbor.
The actual last R conflicts only with last C's, already deleted
on all its neighbors. Thus this branch has exactly the virtual
adjusted contribution.

If \(L_j>0\) and \(A_k(j)<L_j\), delete all \(n\) actual R's.
Here \(w_j>d_j\) and the adjusted actual column cost after its
last-corner profit is
\[
A_0(j)+d_j-w_j=A_0(j)-L_j,
\]
also exactly (17). Removing the virtual higher survivors creates
no new conflict. With C survivors unchanged, it can only increase
the set of uncovered higher corners. Actual higher-corner profit
is therefore at least the virtual profit.

The equality \(A_k(j)=L_j\) belongs to the first branch.
When \(L_j=0\), the second branch is never used; an expensive
last R with \(d_j>w_j\) is retained.
No positivity of the pooled costs is assumed.

Adopt the residual higher-C decisions in every low row and retain
any such original isolated in the residual relation.
Its neighbors outside \(G\) lie in \(J_H\) or \(N\), where every R
has been deleted, so this is conflict-free.
Combining the high, negative and lifted good regions gives an
actual conflict-free pruning. In good columns, isolated residual
coordinates cause no loss in the comparison: if a column has no
residual neighbor, every R there is retained, and covers all its
higher corners. Every surviving actual original and every corner
profit in this construction refers to the actual full chain graph.

The low last-C deletion cost is \(\sum_{S_L}D_s\).
Use (6), the nonpositive contributions in \(N\), the lift comparison,
and (16) to obtain
\[
\begin{aligned}
\mathbb E\left[D_{\rm del}-\sum_U z\right]
&\le\sum_{S_H}q_s+\sum_{S_L}D_s+
       \sum_{S_L}(q_s-D_s)\\
&=\sum_s q_s=\sum_Hh. \tag{18}
\end{aligned}
\]
The residual pruning is fixed across the finite high threshold states.
At least one of those states attains (18).
Equation (5) gives the cover bound.
This closes the scalar induction for all nonnegative costs.

## 7. Nested expansions, components and partial families

An expanded scalar chain has nonempty disjoint groups
\(P_0,\ldots,P_{n-1}\) and \(I_0,\ldots,I_{n-1}\), with
\[
E=\bigcup_{p\le i}P_p\times I_i. \tag{19}
\]
For full original families, remove isolated F coordinates and aggregate
\[
\bar x_{pj}=\sum_{u\in P_p}x_{uj},\quad
\bar h_{ps}=\sum_{u\in P_p}h_{us},\quad
\bar y_{is}=\sum_{v\in I_i}y_{vs},\quad
\bar z_{ij}=\sum_{v\in I_i}z_{vj}. \tag{20}
\]
For every scalar edge \(p\le i\) and F edge \(F(s,j)\), all pairs
in \(P_p\times I_i\) are actual conflicts. Summing (1) over that
complete rectangle factors exactly as
\[
\bar x_{pj}\bar y_{is}\le \bar h_{ps}\bar z_{ij}. \tag{21}
\]
Apply the scalar theorem, lifting each original decision to its
whole group. All corners within a fixed \(I_i\) group at column \(j\)
have the same R coverage because their E-neighbor groups agree.
Their C coverage also agrees, since each original I group at row
\(s\) is retained or deleted wholly. Thus actual uncovered-corner
profits, original deletion costs and H budgets equal the scalar
aggregates exactly. This proves the expanded full-family theorem.

Every nonisolated connected nested component has form (19).
Group left vertices by their equal neighborhoods and order the
distinct nonempty neighborhoods as
\(N_0\supsetneq\cdots\supsetneq N_{n-1}\).
For \(i<n-1\) put \(I_i=N_i\setminus N_{i+1}\), and put
\(I_{n-1}=N_{n-1}\). These groups are nonempty; \(N_0\) contains
every right vertex of the component, and a vertex in \(P_p\)
is adjacent precisely to the groups \(I_i\) with \(p\le i\).
This standard chain/Ferrers representation is not an originality claim.

For a disjoint union of nested E components, split originals by their
P or I coordinate. Every conflict and coverage edge stays in one
component. Its H and Z corners are also distinct from those of every
other component, even if S or J coordinates are shared. Unite the
component covers and prunings; no budget is counted twice.
Isolated E coordinates yield isolated originals, which are retained.

For partial \(R,C\), first pad missing full-grid originals with cost
zero and newly created corners with cost zero, preserving actual costs.
Every padded conflict either is actual and satisfies (1), or has
a zero-cost missing original and satisfies (1) automatically.
The full budget remains the actual \(\sum_Hh+\sum_Zz\).
Construct the padded cover, then restrict it to the actual originals
and actual Z tags. The actual augmented graph is the induced subgraph
on these vertices, so this restriction preserves its edges and cannot
increase cover cost. Remove all isolated vertices.

Every initially conflict-free actual original is isolated in this
augmented graph: coverage of an actual Z would, together with that
corner's opposite-original witness, supply a conflict.
Hence these originals are retained.
Take the restricted pruning's actual cheapest completion and use
(5) for its actual U to obtain (3).
Padded survivor coverage is not used as a witness in the final problem.

Finally, exchanging the two original families and transposing
coordinates sends \(E\) to \(F\), \(F\) to \(E\), and transposes the
H and Z tables. Conflicts and coverage edges are preserved.
This proves the alternative hypothesis on F and completes the theorem.

## 8. Finite construction, sharpness and provenance

For rational costs, all suffix sums, positive parts, comparisons,
budget differences and threshold weights are rational.
Recursively construct the residual pruning, normalize its R prefixes,
lift by Section 6, then compare the finitely many high threshold states
using their actual uncovered corners. The number of chain layers
decreases at each recursive step. Group aggregation, component splitting
and partial-family restriction preserve finiteness.
This proves a deterministic finite feasible construction.
It does not assert a general optimal-cover algorithm or a complexity bound,
and no new executable checker is supplied by this note.

The single-conflict all-ones example lies in the theorem's domain.
Its two disjoint coverage edges force cover cost at least two, equal
to \(\sum_Hh+\sum_Zz\). Deleting one original costs one with U empty;
deleting both costs two and has U equal to Z.
Thus replacing the common coefficient one in either (2) or (3) by
a smaller constant fails.

The framework comes from the pinned
[OpenAI pruning source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex).
The [block theorem](compatible-pair-costs.md) is the induction base.
The [four-path proof](binary-one-side-costs.md) is its two-layer antecedent;
the present induction uses suffix costs and a pooled final H budget
to preserve every residual inequality and lift to actual survivors.

Weighted thresholds, nested neighborhood representations and
four-functions inequalities are classical.
Ahlswede and Daykin,
[*Inequalities for a pair of maps \(S\times S\to S\) with S a finite set*](https://www.math.uni-bielefeld.de/ahlswede/homepage/public/33.pdf),
Math. Z. 165 (1979), 267--289, impose compatibility for all ordered
pairs in (1.11); Section 3 retains that hypothesis.
Here compatibility is assumed only at actual conflicts.
No reduction supplying the missing hypotheses is claimed.
This comparison does not establish absence of an equivalent earlier
result, mathematical priority or journal readiness.

When neither relation has nested components, the independent local-cost
sufficiency problem remains open. General equality classification,
a full Lean proof and a broader original-literature comparison are
separate tasks. No conclusion about the upstream second-neighborhood
conjecture is asserted.
