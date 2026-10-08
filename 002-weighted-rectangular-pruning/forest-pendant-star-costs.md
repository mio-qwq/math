# Sharp local pair-cost bounds for bipartite forests

Research note, 8 October 2026.

A pendant-star preservation lemma extends the local independent
pair-cost construction from a smaller relation to one with a new
right coordinate, one old left neighbor and any number of new left
neighbors. It follows that either coordinate relation may be an
arbitrary finite bipartite forest, while the other is entirely
arbitrary. Complete expansions of forests and partial original
families are included. All costs may be zero.
This is a written theorem, not a Lean proof or a historical
priority claim.

## 1. Framework and theorem

Use the actual conflict/coverage definitions of
[nested-relation-costs.md](nested-relation-costs.md).
For finite \(P,I,S,J\), let
\(E\subseteq P\times I,\ F\subseteq S\times J\),
\(R\subseteq P\times J,\ C\subseteq I\times S\).
Originals \((p,j),(i,s)\) conflict iff \(E(p,i)\) and \(F(s,j)\).
Actual cross-corners H and Z require witnesses from such conflicts.
An R survivor covers \((i,j)\) through E; a C survivor covers it
through F. The augmented graph has tagged sides \(R\sqcup Z_L\)
and \(C\sqcup Z_R\), original conflict edges and the two coverage
edge families, with no \(Z_L\)--\(Z_R\) edge.

Assign independent nonnegative costs \(x,y,h,z\), with the same cost
on both copies of every Z. Assume
\[
x_{pj}y_{is}\le h_{ps}z_{ij}
\quad\text{at every actual conflict}. \tag{1}
\]
A *forest* means the undirected bipartite coordinate graph is acyclic.

**Forest theorem.** If either E or F is a forest, the actual
augmented graph has a vertex cover containing no isolated vertex
and costing at most
\[
\sum_Hh+\sum_Zz. \tag{2}
\]
There are conflict-free survivors retaining every initially
conflict-free original, with actual uncovered corner set U and
\[
D_{\rm del}\le\sum_Hh+\sum_Uz. \tag{3}
\]
The same result holds if either relation is a complete expansion
of a forest. Partial families, isolated coordinates and empty
relations are permitted. The common coefficient one is sharp,
and rational inputs have a deterministic finite construction.

Call a relation's *local pair-cost property* the universal conclusion
(2)--(3) for every other finite relation, all partial families and
nonnegative costs satisfying (1), with retention and finite rational
construction. The empty relation has this property.

For any conflict-free pruning, its cheapest augmented completion costs
\[
\sum_Zz+D_{\rm del}-\sum_Uz. \tag{4}
\]
Opposite-side survivors cannot both cover one corner because they
would conflict. A corner covered from one survivor side forces
its opposite tag into the cover; an uncovered corner forces neither.
Thus the adjusted deletion bound proves the cover bound.

## 2. Pendant-star extension of an arbitrary valid relation

Let \(E_0\subseteq P_0\times I_0\) have the local pair-cost property,
and choose \(p_*\in P_0\).
Introduce a new right coordinate \(i_*\) and a disjoint set Q
of new left coordinates. Form
\[
P=P_0\sqcup Q,\quad I=I_0\sqcup\{i_*\},
\]
\[
E=E_0\cup\{(p_*,i_*)\}\cup(Q\times\{i_*\}). \tag{5}
\]
Each new left coordinate has only this new right neighbor.
No edge to another old left vertex or old right vertex is added.

**Pendant-star lemma.** E has the local pair-cost property.

If Q is empty, this is the already proved
[right-leaf lemma](right-leaf-extension-costs.md#2-a-preservation-lemma-and-its-full-family-reduction).
Hence assume Q is nonempty for the following proof.
No cost of a Q original is assumed positive.

First take full families \(R=P\times J,\ C=I\times S\).
Temporarily remove isolated F coordinates, retaining their originals.
If F becomes empty the result is immediate.
Otherwise every new-star H corner and every new Z corner is actual,
witnessed by the full originals and an incident F edge.
Put
\[
a_j=\sum_{p\in Q}x_{pj},\quad b_j=x_{p_*j},\quad w_j=z_{i_*j},
\]
\[
\alpha_s=\sum_{p\in Q}h_{ps},\quad
\beta_s=h_{p_*s},\quad D_s=y_{i_*s},\quad q_s=\alpha_s+\beta_s.
\]
Summing the new-left local inequalities, and using the pivot one, gives
\[
a_jD_s\le\alpha_sw_j,\qquad b_jD_s\le\beta_sw_j
\quad(F(s,j)). \tag{6}
\]
Old isolated E coordinates can remain as inputs; their originals
will be retained by the residual property.

## 3. High rows and exact new-corner profits

Partition \(S\) into \(S_H=\{s:D_s>q_s\}\)
and \(S_L=S\setminus S_H\).
For high s put \(\rho_s=q_s/D_s\in[0,1)\);
its denominator is positive.
Let \(J_H\) be the columns neighboring a high row, and let
\(J_L=J\setminus J_H\).

Delete the pivot R and every Q original in each column \(j\in J_H\).
Delete every new C\((i_*,s)\) in low rows.
For high new C's, use a common threshold \(T\in(0,1]\),
deleting exactly when \(T\le\rho_s\).
No other old original decision is fixed at this stage.

In a high-neighbor column all possible R covers of its new corner
have been deleted. Its low new-C neighbors are deleted as well.
Therefore that corner is actually uncovered exactly when all
adjacent high new C's are deleted, with probability
\[
m_j=\min_{s\in S_H:F(s,j)}\rho_s.
\]
Adding (6) gives \((a_j+b_j)D_s\le q_sw_j\).
Thus \(a_j+b_j\le m_jw_j\), and the expected fixed R cost
minus its actual new-corner profit is nonpositive.
High new-C deletion costs average to \(\sum_{S_H}q_s\).

Use the distinct positive ratios and endpoint 1, weighted by preceding
interval lengths starting at 0, to make this an exact finite
threshold distribution. Its marginals and neighbor minima are those
just calculated. Zero ratios never delete.
If no high rows exist, use the single threshold 1.
The residual decisions below are independent of T.

## 4. Low-column pooling and the actual partial residual input

Every new-C neighbor of a column in \(J_L\) is low and deleted.
Put
\[
L_j=(w_j-a_j)^+,\qquad
N=\{j\in J_L:b_j<L_j\},\qquad G=J_L\setminus N.
\]
For j in N, delete the pivot and every Q original.
Here \(L_j>0,\ w_j>a_j\), and their adjusted contribution after
the new-corner profit is
\[
a_j+b_j-w_j=b_j-L_j<0. \tag{7}
\]

For good columns retain the pivot as a residual input, with cost
\[
v_j=b_j-L_j\ge0. \tag{8}
\]
Remove the new right coordinate and all Q coordinates from the
residual relation. On \(E_0\) with unchanged F use residual families
\[
R_0=(P_0\times J)\setminus
       \{(p_*,j):j\in J_H\cup N\},\qquad C_0=I_0\times S.
\]
This is a genuinely partial residual R family.
Assign v to the good pivot originals, unchanged x to other
old R's and unchanged y to old C's.

Reconstruct the actual residual H and Z from these inputs.
Their witnesses also witness actual original corners.
On residual H use unchanged h away from the pivot and
\[
h'_{p_*s}=
\begin{cases}
k_s=q_s-D_s,&s\in S_L,\\
0,&s\in S_H.
\end{cases} \tag{9}
\]
Keep original costs on residual Z.
All these costs are nonnegative.
No pivot/high H corner is active in the residual graph:
every column adjacent to a high row had its pivot R removed.

The available residual budget satisfies
\[
\sum_{\text{residual H}}h'
\le
\sum_{\substack{\text{original H}\\p\in P_0\setminus\{p_*\}}}h_{ps}
+\sum_{s\in S_L}k_s. \tag{10}
\]
The first sum is over old left coordinates only.
The auxiliary H budgets are already included in q and are not
counted again there. Inactive nonnegative residual terms only
leave additional slack.

## 5. Preservation of every local inequality at zero costs

A residual conflict away from the pivot keeps (1) unchanged.
At the pivot, its column lies in G and its row must be low.
For every old right neighbor i we need
\[
v_jy_{is}\le k_sz_{ij}. \tag{11}
\]
We have the original \(b_jy_{is}\le\beta_sz_{ij}\)
and the two new-star inequalities (6).

If \(D_s\le\alpha_s\), then
\(k_s=\alpha_s+\beta_s-D_s\ge\beta_s\).
Since \(v_j\le b_j\), the old local inequality proves (11).
This includes \(D_s=0\).

Suppose \(D_s>\alpha_s\). Then \(D_s>0\).
Low membership \(D_s\le\alpha_s+\beta_s\) also proves
\(\beta_s\ge D_s-\alpha_s>0\), so both divisions below
have positive denominators.
The auxiliary inequality in (6) implies
\[
w_j-a_j\ge\frac{w_j(D_s-\alpha_s)}{D_s}\ge0.
\]
Hence \(L_j=w_j-a_j\) and, using the pivot inequality,
\[
L_j\ge\frac{w_j(D_s-\alpha_s)}{D_s}
\ge\frac{b_j(D_s-\alpha_s)}{\beta_s}.
\]
Consequently
\[
0\le v_j=b_j-L_j
\le \frac{b_j(\alpha_s+\beta_s-D_s)}{\beta_s}
=\frac{b_jk_s}{\beta_s}. \tag{12}
\]
Multiply by \(y_{is}\ge0\) and use the old pivot local inequality
to get (11).
Zero a, b, w, v, k and auxiliary budgets are included.
In particular the case \(\beta_s=0\) cannot enter this second
branch; it belongs to the first one with \(v_jy_{is}=0\).

Apply the assumed universal partial-family property of \(E_0\)
to this precise compatible residual instance. It supplies a
conflict-free pruning, retaining initially isolated residual originals,
with adjusted deletion value bounded by (10).
Fix this pruning across all finite high threshold states.

## 6. Lifting to actual survivors and the complete budget

Adopt every residual original decision.
Keep the fixed pivot/Q deletions in \(J_H\cup N\).
In a good column, if the pivot survives, retain every Q original.
If the pivot is deleted, delete every Q original exactly when
\(a_j<w_j\); otherwise retain all of them.

All Q originals conflict only with the new C layer, already deleted
on the low neighbors of a good column.
Retained high new C's have every possible pivot/Q neighbor deleted
in \(J_H\). Old conflicts are exactly the residual survivor conflicts.
Thus the lifted pruning is conflict-free, including residual-isolated
old originals retained by the assumed theorem.

For good j, a retained pivot covers the new corner and incurs no
pivot/Q deletion charge.
If the pivot is deleted and \(a_j<w_j\), every Q original is deleted,
the new corner is uncovered, and the actual adjusted pivot/Q fee is
\(b_j+a_j-w_j=b_j-L_j=v_j\).
If the pivot is deleted and \(a_j\ge w_j\), all Q originals are
retained. Q is nonempty, so they cover the new corner even if all
their costs are zero. Here \(L_j=0\), and the actual fee \(b_j\)
again equals \(v_j\).
The equality \(a_j=w_j\) belongs to this retention branch.
For Q empty the separate right-leaf proof supplies the lemma,
including the zero-profit coverage boundary.

On every old corner present in residual Z, actual and residual
survivor coverage agree exactly: the omitted old pivot originals
were fixed deleted, Q covers only the new coordinate, and all
old C decisions are identical.
An original old corner missing from residual Z may yield additional
nonnegative actual uncovered profit. Omitting it only weakens
an upper bound. Thus actual old-corner profit is at least the
residual profit, without assuming equal entire corner sets.

The low new-C cost is \(\sum_{S_L}D_s\).
The negative-column adjusted fees in (7) are nonpositive.
High fixed-original/new-corner contributions are nonpositive
in expectation, and high new-C fees average to \(\sum_{S_H}q_s\).
Combining these facts with (10) gives
\[
\begin{aligned}
\mathbb E[D_{\rm del}-\sum_{\text{actual U}}z]
&\le
\sum_{\substack{\text{original H}\\p\in P_0\setminus\{p_*\}}}h_{ps}
+\sum_{S_L}k_s+\sum_{S_L}D_s+\sum_{S_H}q_s\\
&=
\sum_{\substack{\text{original H}\\p\in P_0\setminus\{p_*\}}}h_{ps}
+\sum_s(\alpha_s+\beta_s)
=\sum_{\text{original H}}h. \tag{13}
\end{aligned}
\]
Every auxiliary H corner and every pivot H corner is actual in
the active full-family input. They are counted once in q.
Every other actual H corner belongs to the first, old-only sum.
No auxiliary budget is reused.

One finite high state attains (13), and (4) gives the cover.
Initially isolated F originals were retained. Old coordinates
isolated in the extended relation remain isolated in the residual
and are retained there. Pivot/Q originals and new C originals
in incident F coordinates initially have star conflicts, so the
fixed deletions do not discard an initially conflict-free original.

For partial input families, zero-pad missing full originals and
new corners, preserving actual costs. Every padded conflict either
keeps two actual originals and their actual local inequality, or
has a zero original factor. The padded H+Z budget is unchanged.
Construct the full cover, restrict it to actual originals and
actual Z tags, and remove isolated selected vertices.
This is an actual induced-graph restriction and preserves all edges.
An initially conflict-free actual original cannot cover actual Z:
its opposite-original witness would create a conflict.
It is isolated and retained. The cheapest actual completion gives
(3) for the actual U, without dummy survivor witnesses.
This proves the pendant-star lemma for all partial families.

For rational costs the residual construction, positive-denominator
ratios, comparisons and finite thresholds are rational.
Choosing a final state using rebuilt actual U proves deterministic
finite construction whenever the base property has one.

## 7. Building every forest and lifting complete expansions

For each nonisolated tree component, choose a P vertex as root.
Orient the tree away from that root. Every I vertex has one parent
P vertex and zero or more child P vertices.
Process the I vertices in increasing distance from the root.
When one is processed, its parent P already exists, its children
are new, and it has no other old P neighbor:
a second old neighbor would give two paths to the root and a cycle.

Start with the root P and no edges, which has the local property.
Each step with children is exactly (5); a childless I is the
right-leaf case. Thus every tree is obtained by finitely many
valid extensions. Retain isolated coordinates separately.
Different tree components have disjoint P/I coordinates, hence
disjoint original vertices and actual H/Z corners even when S,J
are shared. All augmented edges stay within their component.
Unite their covers/prunings without repeating any budget.
This proves the E-forest theorem.

For a complete expansion, replace each scalar P/I vertex by a
nonempty disjoint group and every scalar forest edge by its complete
rectangle. On full families aggregate x,h over P groups and y,z
over I groups. Summing all local conditions over one complete
rectangle factors into the scalar condition.
Lift each scalar original decision to its whole group.
All corners within a given I group at j have equal R coverage
because their E-neighbor groups agree, and equal C coverage
because I groups at each s are chosen wholly.
Actual uncovered profits, deletion costs and H budgets therefore
equal their aggregate values exactly.
Partial families follow by the same zero-padding and actual cover
restriction used above. An expanded forest can contain coordinate
cycles; no acyclicity of the expanded graph is being asserted.

The family swap \((P,I,S,J)\mapsto(S,J,P,I)\), with transposed
exchanged originals and transposed H/Z tables, preserves conflicts,
tagged coverage edges and costs. It proves the alternative on F.

The preservation lemma also starts from any already valid relation,
such as a [nested component](nested-relation-costs.md), and allows
finitely many extensions (5) before complete expansion.
This additional closure follows from the same universal property;
it is not a theorem for arbitrary cyclic relations.

## 8. Consequences, sharpness and verification boundary

Every orientation of every finite path is a forest and is now included.
In particular the two transposed five-vertex paths left untreated
by [the earlier right-leaf note](right-leaf-extension-costs.md)
are covered, as are paths with arbitrarily many vertices.
This closes that structural gap in written mathematics.
Pairs of unrestricted cyclic relations remain outside this theorem.

The all-ones single-conflict instance is a forest.
Its two disjoint coverage edges force cover cost at least two,
equal to H+Z budget two. Its feasible prunings give
\(D_{\rm del}=1,\ H+U=1\) or \(D_{\rm del}=2,\ H+U=2\).
The common coefficient one in both conclusions is sharp.

The conflict/coverage framework comes from the pinned
[OpenAI pruning source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex).
The [right-leaf lemma](right-leaf-extension-costs.md) supplies the
empty-auxiliary case; the [nested theorem](nested-relation-costs.md)
supplies one possible nonempty base. The new proof pools actual
auxiliary costs and H budgets into a partial pivot problem, and
checks every residual inequality and actual survivor lift directly.

Threshold methods, tree rootings and complete group expansions
are classical. Global literature comparison and mathematical novelty
have not been established. No general optimal-cover algorithm,
new executable certificate, full Lean proof, complexity bound or
upstream second-neighborhood conclusion is asserted.
