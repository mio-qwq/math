# Stability of local pair-cost bounds under right-leaf extensions

Research note, 8 October 2026.

The [nested-component theorem](nested-relation-costs.md) proves local
independent pair-cost bounds when one relation has totally nested
neighborhood components. The present note gives a preservation lemma:
adding a right coordinate with just one left neighbor preserves the
bounds, even when the resulting neighborhoods are incomparable.
Consequently a relation with a nested core and arbitrary right leaves
works against every finite other relation. Complete expansions and
partial original families are included. In particular, at most two
distinct left neighborhoods per component suffice, with no bound on
the number of right coordinates.
This is a written theorem, not a Lean formalization or a novelty claim.

## 1. Definitions and structural theorem

Use the actual H and Z corners, tagged augmented graph and costs of
[nested-relation-costs.md](nested-relation-costs.md).
Thus \(E\subseteq P\times I,\ F\subseteq S\times J\);
\(R\subseteq P\times J,\ C\subseteq I\times S\).
Originals \((p,j),(i,s)\) conflict iff \(E(p,i)\) and \(F(s,j)\).
A surviving R covers \((i,j)\) through E and a surviving C covers it
through F. Actual H and Z corners require an original conflict witness.
Assign independent nonnegative costs \(x,y,h,z\), with equal costs on
the two tagged copies of each Z, and assume
\[
x_{pj}y_{is}\le h_{ps}z_{ij}
\quad\text{at every actual conflict}. \tag{1}
\]

A *right leaf* of E is an I coordinate with exactly one P neighbor.
Its *right-leaf core* is obtained by removing all such I coordinates,
and ignoring isolated coordinates. Call the core nested if each of
its nonisolated components has left neighborhoods totally ordered
by inclusion.

**Theorem.** If either E or F has a nested right-leaf core, the
actual augmented graph has a vertex cover containing no isolated
vertex and of cost at most
\[
\sum_Hh+\sum_Zz. \tag{2}
\]
There are conflict-free original survivors retaining every initially
conflict-free original and satisfying
\[
D_{\rm del}\le \sum_Hh+\sum_Uz, \tag{3}
\]
with U the actual uncovered corner set.
The same conclusions hold for complete expansions of any relation
with a nested right-leaf core, against an arbitrary other relation.
All costs may be zero and original families may be partial.
Rational inputs admit a deterministic finite construction.
The common coefficient one is sharp.

For F, its right coordinate is J, so a leaf has a unique S neighbor.
The complete expansion alternative is defined and proved in Section 6.
The theorem does not cover every forest or every orientation of a path.

## 2. A preservation lemma and its full-family reduction

Say E has the *local pair-cost property* if (2)--(3) hold for every
finite F and all partial original families satisfying (1), including
nonnegative costs, initial retention and finite rational construction.

**Right-leaf lemma.** Suppose \(i_*\in I\) has unique neighbor \(p_*\),
and \(E_0\) is E with \(i_*\) removed.
If \(E_0\) has the local pair-cost property, so does E.

First prove the lemma on full families \(R=P\times J,\ C=I\times S\).
Remove isolated coordinates of E and F temporarily, retaining their
originals. An empty relation is immediate. All remaining H and Z
grid corners are actual.
For any conflict-free pruning, the cheapest augmented completion costs
\[
\sum_Zz+D_{\rm del}-\sum_Uz. \tag{4}
\]
Opposite-side survivors cannot both cover one corner because they
would conflict. A covered corner forces one opposite tag into the
cover; an uncovered corner forces neither.
It suffices to bound the actual adjusted deletion cost.

Write
\[
D_s=y_{i_*s},\quad q_s=h_{p_*s},\quad
a_j=x_{p_*j},\quad w_j=z_{i_*j}.
\]
The leaf conflicts give exactly
\[
a_jD_s\le q_sw_j\quad(F(s,j)). \tag{5}
\]
They involve only the distinguished R row. Other R rows never
cover a leaf corner and never conflict with a leaf C original.

## 3. High rows and actual leaf-corner profit

Set \(S_H=\{s:D_s>q_s\}\), \(S_L=S\setminus S_H\).
For high s let \(\rho_s=q_s/D_s\in[0,1)\), with \(D_s>0\).
Let \(J_H\) be the columns neighboring high rows, and \(J_L\)
its complement.

Delete R\((p_*,j)\) for every \(j\in J_H\).
Delete every leaf C in a low row.
For the high leaf C's use a common threshold \(T\in(0,1]\),
deleting precisely when \(T\le\rho_s\).
Make no fixed deletion of another R row or another C level.

In a high-neighbor column, its leaf corner is uncovered exactly
when all adjacent high leaf C's are deleted: its unique covering R
has been deleted, and all low leaf C's are deleted.
Its probability under a uniform threshold is
\[
m_j=\min_{s\in S_H:F(s,j)}\rho_s.
\]
By (5), \(a_j\le m_jw_j\).
Thus the expected distinguished-R deletion cost minus its actual
leaf-corner profit is nonpositive there.
The expected high leaf-C deletion charge is
\(\sum_{S_H}D_s\rho_s=\sum_{S_H}q_s\).

As before, this is a finite distribution: the distinct positive
ratios, followed by 1, have weights given by consecutive interval
lengths starting at 0. It reproduces every marginal and neighbor
minimum exactly. Zero ratios never delete; when there are no high
rows, the sole threshold is 1.

## 4. The residual partial problem and every local inequality

For low-only columns, all leaf C neighbors are deleted.
Let
\[
N=\{j\in J_L:a_j<w_j\},\qquad G=J_L\setminus N.
\]
Delete R\((p_*,j)\) in N. Its adjusted contribution after the
leaf-corner profit is \(a_j-w_j<0\).
Keep R\((p_*,j)\) as an input original in G with virtual cost
\[
b_j=a_j-w_j\ge0. \tag{6}
\]

Construct the residual input for \(E_0\), keeping F.
Remove all leaf C originals and all already-deleted distinguished
R's in \(J_H\cup N\). Keep every other input R and every nonleaf C.
The residual original families are thus partial even though the
original input was full.
Use cost \(b_j\) for distinguished R's in G and unchanged costs
for all other residual originals.
On residual H corners set
\[
h'_{ps}=
\begin{cases}
h_{ps},&p\ne p_*,\\
q_s-D_s,&p=p_*,\ s\in S_L,\\
0,&p=p_*,\ s\in S_H.
\end{cases} \tag{7}
\]
These are nonnegative. Residual Z corners keep their original costs.

A distinguished residual R cannot conflict in a high row,
since any column with a high F neighbor belongs to \(J_H\).
Hence all its residual conflicts are in low rows.
For \(j\in G\), a low edge \(F(s,j)\), and any nonleaf neighbor i
of \(p_*\), we prove
\[
b_jy_{is}\le(q_s-D_s)z_{ij}. \tag{8}
\]
If \(q_s=0\), low membership gives \(D_s=0\).
Then \(b_j\le a_j\), and the original
\(a_jy_{is}\le q_sz_{ij}=0\) proves (8) without division.
If \(q_s>0\), (5) gives \(w_j\ge a_jD_s/q_s\), so
\[
b_j=a_j-w_j\le a_j(1-D_s/q_s).
\]
The factor is nonnegative because \(D_s\le q_s\).
Multiplying by \(y_{is}\ge0\) and using the original inequality
proves (8). All other residual conflicts keep (1) unchanged.
Zero b, D, w and \(q_s-D_s\) are included.

Every actual residual corner is an actual original corner:
its conflict witness survives the input restriction.
Consequently
\[
\sum_{\text{residual H}}h'
\le \sum_{\substack{\text{original H}\\p\ne p_*}}h
       +\sum_{s\in S_L}(q_s-D_s). \tag{9}
\]
Unused nonnegative H terms may be omitted.
Apply the assumed property of \(E_0\) to this genuine partial
residual input. It gives an adjusted residual deletion value bounded
by (9), with isolated residual originals retained.
Fix one such residual pruning, independent of T.

## 5. The actual lift and missing residual corners

Use exactly the residual survivor decisions for every residual
original. The distinguished R's outside its input remain deleted.
Add the leaf C threshold decisions from Section 3.
A high leaf C has only distinguished-R neighbors, all deleted
in its neighboring columns. A low leaf C is deleted.
Nonleaf conflicts are exactly the surviving residual conflicts.
The resulting original pruning is therefore conflict-free.

For \(j\in G\), the leaf corner is uncovered exactly when the
distinguished residual R is deleted, because all its leaf C
neighbors are low and deleted.
If that R is deleted, its actual cost less leaf-corner profit is
\(a_j-w_j=b_j\); if retained, both contributions are zero.
Thus its actual adjusted contribution equals its virtual deletion
cost, even at \(b_j=0\).
No normalization or positive virtual cost is required.

Every nonleaf corner present in the residual input has exactly the
same coverage from actual and residual survivors. All removed
input R's were actually deleted; leaf C survivors can cover only
corners with coordinate \(i_*\). Every other R and C survivor is
the same in both models.
Hence actual nonleaf U restricted to residual Z is exactly the
residual U. An original nonleaf corner missing from residual Z
contributes an additional nonnegative uncovered profit if it becomes
uncovered. Omitting that possible profit only weakens the bound.
No assertion that all original corners remain active is needed.

Every actual original deletion cost outside the leaf is now counted
once: distinguished R's in high/negative columns are charged
separately, distinguished good R's by b, and other originals by the
residual deletion cost.
Using (9), the nonpositive negative-column contributions, and
the high expectation, we obtain
\[
\begin{aligned}
\mathbb E[D_{\rm del}-\sum_{\text{actual U}}z]
&\le \sum_{S_H}q_s+\sum_{S_L}D_s
   +\sum_{\substack{\text{original H}\\p\ne p_*}}h
   +\sum_{S_L}(q_s-D_s)\\
&=\sum_{\text{original H}}h. \tag{10}
\end{aligned}
\]
The residual pruning is fixed across finitely many high states.
One state attains (10), and (4) proves the cover bound.

For partial original families, pad missing full originals and new
corners with zero costs, preserving actual costs. Every new conflict
has a zero original product; an old conflict keeps its actual
corner costs and (1). Construct the full cover, then restrict it
to actual originals and actual Z tags. This covers the actual
induced augmented graph without increasing cost.
Remove isolated selected vertices.
An initially conflict-free actual original cannot cover an actual Z:
that corner's opposite-original witness would produce a conflict.
Thus it is isolated and retained. Taking the actual cheapest completion
gives (3) for the actual U. Dummy survivors do not witness final coverage.

For rational costs, the residual assumed construction, finite
thresholds, comparisons and rebuilt actual U remain rational and
finite. Therefore the right-leaf lemma preserves the full property,
including zero costs, partial families and finite construction.

## 6. Nested cores and complete expansions

Remove all right leaves of E, ignoring isolated coordinates.
If its core components are nested, the
[nested-component theorem](nested-relation-costs.md) proves its
local pair-cost property. Restore the leaves one at a time,
using the lemma. Each restored right coordinate has its sole original
left neighbor, independent of the other restored leaves.
Left coordinates isolated in the core are permitted;
their restored leaves can create a new component.
This proves the theorem for every E with nested right-leaf core.

A *complete expansion* of a scalar relation
\(\bar E\subseteq\bar P\times\bar I\) replaces each scalar coordinate
by a nonempty disjoint group, and every scalar edge by the complete
rectangle between its groups, adding no other edge.
For full families, aggregate x and h over each P group, and y and z
over each I group. At a scalar edge and F edge, summing all actual
local inequalities over the complete rectangle factors into the
scalar local inequality.
Apply the scalar property and lift each decision to its whole group.
Within one I group at j, all corners have the same R coverage
because their E-neighbor groups agree. Their C coverage also agrees
because every I group at each s is retained or deleted wholly.
Thus actual uncovered gains, original costs and H budgets are exactly
the aggregate values. The scalar cover/pruning bound lifts.
Partial families follow by the same zero-padding, induced restriction
and actual completion argument of Section 5.

This expansion statement is stronger than merely testing right degrees
in the expanded relation: an expanded leaf I group may neighbor
several actual P vertices belonging to a single scalar P group.
The scalar core must satisfy the stated nesting condition;
arbitrary rectangles or arbitrary expansions are not sufficient.

Different nonisolated scalar components have disjoint P/I coordinates.
Their originals and actual H/Z corners are disjoint even when S,J
are shared, and every augmented edge remains inside its component.
Unite their constructions without counting budgets twice.

The family swap and coordinate transpose from
[nested-relation-costs.md, Section 7](nested-relation-costs.md#7-nested-expansions-components-and-partial-families)
exchanges E and F while preserving conflicts, coverage edges and costs.
It proves the theorem when F has the stated core or expansion structure.

## 7. Two neighborhood types, path examples and remaining scope

**Two-neighborhood corollary.** The theorem's conclusions hold if
every nonisolated component of either relation has at most two distinct
left neighborhoods. In particular, \(|P|\le2\), with I arbitrary,
or \(|S|\le2\), with J arbitrary, suffices against an arbitrary
other relation, with all partial families and nonnegative costs.

To prove this, one left-neighborhood type gives a complete block.
For two types, group the left vertices into their twin classes
\(P_0,P_1\). Every incident right coordinate has exactly one of
the three group-neighbor types
\[
I_{10}:\ P_0\text{ only},\quad
I_{11}:\ P_0\text{ and }P_1,\quad
I_{01}:\ P_1\text{ only}. \tag{11}
\]
Within each displayed group all scalar adjacencies are complete.
If \(I_{11}\) is absent, there are disjoint complete blocks.
If either private group \(I_{10}\) or \(I_{01}\) is absent,
the left neighborhoods are nested. If all three groups are present,
the component is a complete expansion of the two-left,
three-right path in (12). That path has a nested right-leaf core,
so Section 6 applies. This exhausts the cases and proves the corollary.
No assumption that either right coordinate set is binary is used.

Consider the oriented five-vertex path
\[
P=\{0,1\},\quad I=\{0,1,2\},\quad
E=\{(0,0),(0,1),(1,1),(1,2)\}. \tag{12}
\]
Its two left neighborhoods \(\{0,1\}\) and \(\{1,2\}\)
are incomparable. Removing the right leaves 0 and 2 leaves the
complete block \(\{0,1\}\times\{1\}\).
Thus (2)--(3) hold for (12) against every arbitrary F, with
independent nonnegative costs and partial original families.
In particular two copies of this orientation are included.
This case is outside the component-nesting hypothesis of the
preceding theorem.

The transpose of (12) has three left coordinates and two right
coordinates, both of right degree two. Its left neighborhoods remain
incomparable, and the right-leaf-core condition does not apply.
Two such transposed relations are not settled by this note.
The six-vertex path can reduce after one right-leaf removal to that
transposed five-vertex path; consequently no theorem for all paths,
all forests or unrestricted pairs of relations is claimed.

The all-ones single-conflict example has cover cost at least two
from two disjoint coverage edges, equal to H+Z budget two.
Its feasible original deletions have respectively
\(D_{\rm del}=1,\ H+U=1\), or \(D_{\rm del}=2,\ H+U=2\).
The coefficient one in both bounds is therefore sharp.

The pinned [OpenAI pruning source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex)
supplies the conflict/coverage framework; the
[block theorem](compatible-pair-costs.md) and
[nested induction](nested-relation-costs.md) are mathematical antecedents.
The leaf preservation proof additionally uses a genuinely partial
residual original family, reduced H charges and exact actual coverage
on surviving residual corners. It does not introduce a new executable
checker, general optimum formula or Lean proof.
Threshold methods and graph leaf reductions are classical;
the broader literature comparison and historical novelty remain open.
No upstream second-neighborhood conclusion is asserted.
