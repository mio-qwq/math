# Sharp local pair-cost bounds for chordal bipartite relations

Research note, 8 October 2026.

A nested-pivot preservation lemma extends the local independent-cost
construction to a new right coordinate attached to any number of
old left coordinates with nested old neighborhoods. The other old
coordinates need no nesting. Applying the classical weakly-simplicial
elimination theorem gives the sharp bounds whenever either coordinate
relation is chordal bipartite and the other is arbitrary. Arbitrary
partial original families and zero costs are included.
The mathematical proof is written; it is not a Lean theorem or a
claim of historical priority.

## 1. Actual graph, costs and theorem

For finite coordinate sets P,I,S,J, let
\[
E\subseteq P\times I,\quad F\subseteq S\times J,\quad
R\subseteq P\times J,\quad C\subseteq I\times S.
\]
Two original vertices R(p,j) and C(i,s) conflict iff E(p,i) and F(s,j).
The actual cross-corners are
\[
H=\{(p,s):\exists j,i,\ (p,j)\in R,\ (i,s)\in C,\
                         E(p,i),F(s,j)\},
\]
\[
Z=\{(i,j):\exists p,s,\ (p,j)\in R,\ (i,s)\in C,\
                         E(p,i),F(s,j)\}.
\]
An R(p,j) survivor covers Z(i,j) when E(p,i); a C(i,s) survivor
covers Z(i,j) when F(s,j). Coverage always has matching j or i
as displayed. Write U for the actual Z covered by neither side
of the final survivor set.

The augmented bipartite graph has left side R disjoint-union Z_L
and right side C disjoint-union Z_R. Its edges are original conflicts,
R--Z_R coverage edges and Z_L--C coverage edges. There is no
Z_L--Z_R edge. Independent costs x,y,h,z are nonnegative, and
both copies of each Z have cost z. Assume
\[
x_{pj}y_{is}\le h_{ps}z_{ij}
\quad\hbox{at every actual original conflict}. \tag{1}
\]

A finite bipartite graph is *chordal bipartite* if it has no induced
cycle of length at least six. Four-cycles are allowed.

**Theorem.** If either E or F is chordal bipartite, the actual
augmented graph has a vertex cover selecting no isolated vertex
and costing at most
\[
\sum_Hh+\sum_Zz. \tag{2}
\]
There is a conflict-free pruning retaining every initially
conflict-free original and satisfying
\[
D_{\rm del}\le\sum_Hh+\sum_Uz. \tag{3}
\]
Complete expansions of such a relation also satisfy these bounds.
Partial input families, empty relations and arbitrary zero costs
are included. The common coefficient one is sharp. Rational inputs
have a deterministic finite feasible construction.

Call the universal conclusions just stated for a fixed E, against
every F and every partial input, its *local pair-cost property*.
An empty E has this property: there are no actual conflicts or
corners, and retaining every original gives the empty cover.

For any conflict-free survivors, their cheapest augmented completion
has cost exactly
\[
\sum_Zz+D_{\rm del}-\sum_Uz. \tag{4}
\]
Survivors from both sides cannot cover the same corner, since
they would conflict. A survivor-covered corner forces the opposite
Z tag into the cover. An uncovered corner forces neither tag.
Thus an adjusted deletion bound yields the cover bound.

## 2. A general nested-pivot extension

Let \(E_0\subseteq P_0\times I_0\) have the local pair-cost property.
Choose distinct old pivots \(p_0,\ldots,p_{m-1}\), with \(m\ge1\), such that
\[
N_0(p_0)\supseteq N_0(p_1)\supseteq\cdots\supseteq N_0(p_{m-1}).
                                                               \tag{5}
\]
Equal or empty neighborhoods are permitted. Introduce a new right
coordinate \(i_*\) and a finite disjoint set Q of fresh left coordinates.
Form
\[
E=E_0\ \cup\ \{(p_r,i_*):0\le r<m\}\ \cup\ (Q\times\{i_*\}).       \tag{6}
\]
Each fresh left coordinate has only the neighbor \(i_*\).
No other edge is added; Q may be empty.

**Preservation lemma.** E has the local pair-cost property.

Only the chosen old neighborhoods must be nested. The remaining
old E relation and the other F relation are unrestricted.
The single-pivot case recovers the
[pendant-star lemma](forest-pendant-star-costs.md);
the proof below treats the empty-Q boundary directly.

First take full families \(R=(P_0\sqcup Q)\times J\),
\(C=(I_0\sqcup\{i_*\})\times S\).
Remove isolated F coordinates temporarily and retain their originals.
If F becomes empty the conclusion is immediate. Otherwise every
attached-pivot/auxiliary H corner and every new Z corner is actual,
witnessed by a new E edge and an incident F edge.

For each column j and row s put
\[
B_{rj}=x_{p_rj},\quad \beta_{rs}=h_{p_rs},\quad
A_j=\sum_{q\in Q}x_{qj},\quad \alpha_s=\sum_{q\in Q}h_{qs},
\]
\[
D_s=y_{i_*s},\quad w_j=z_{i_*j},\quad
q_s=\alpha_s+\sum_{r<m}\beta_{rs}.
\]
The actual new conflicts give
\[
B_{rj}D_s\le\beta_{rs}w_j,\qquad
A_jD_s\le\alpha_sw_j \quad(F(s,j)).                              \tag{7}
\]
The second inequality sums the auxiliary inequalities; empty sums
are zero. No cost factorization is used.

## 3. High rows and low-column profits

Put \(S_H=\{s:D_s>q_s\}\), \(S_L=S\setminus S_H\).
For high s let \(\rho_s=q_s/D_s\in[0,1)\); its denominator is positive.
Let J_H consist of columns with a high F neighbor and
\(J_L=J\setminus J_H\).

In J_H delete all pivot and auxiliary R originals.
Delete every new C original in low rows.
In high rows delete the new C exactly when a common threshold
\(T\in(0,1]\) satisfies \(T\le\rho_s\).
No other old decisions are fixed yet.

A new corner in J_H is actually uncovered exactly when all its
high new-C neighbors are deleted. Its uncovered probability is
\[
\mu_j=\min_{s\in S_H:F(s,j)}\rho_s.
\]
Summing (7) gives
\[
\bigl(A_j+\sum_{r<m}B_{rj}\bigr)D_s\le q_sw_j,
\]
so its fixed attached-R fee is at most \(\mu_jw_j\).
The expected fixed R fee minus actual new-corner profit is nonpositive.
The high new-C fee averages to \(\sum_{S_H}q_s\).

This requires only a finite threshold distribution. Sort the
distinct positive ratios, append 1, and weight each value by its
preceding interval length from 0. It has the stated marginals
and neighbor minima. Zero ratios never delete; with no high rows
use the single value 1. The later residual choices are fixed across
these states.

For a low column set
\[
L_j=(w_j-A_j)^+,\quad
S_r(j)=\sum_{t=r}^{m-1}B_{tj}\ (r<m),\quad S_m(j)=0,
\]
\[
N=\{j\in J_L:S_0(j)<L_j\},\qquad G=J_L\setminus N.
\]
For j in N delete every pivot and auxiliary R.
Here \(L_j>0,\ w_j>A_j+S_0(j)\); the new corner is actually
uncovered, and the attached adjusted fee is
\[
A_j+S_0(j)-w_j=S_0(j)-L_j<0.                                  \tag{8}
\]

## 4. Suffix costs and the actual partial residual

For j in G assign pivot virtual costs
\[
b_{rj}=(S_r(j)-L_j)^+-(S_{r+1}(j)-L_j)^+,\quad r<m.             \tag{9}
\]
Monotonicity and the 1-Lipschitz property of positive part give
\[
0\le b_{rj}\le B_{rj},\qquad
\sum_{r<m}b_{rj}=S_0(j)-L_j.                                  \tag{10}
\]

For low s put
\[
H_r(s)=\alpha_s+\sum_{t=r}^{m-1}\beta_{ts},\quad
H_m(s)=\alpha_s.
\]
Allocate residual pivot H budgets by
\[
k_{rs}=(H_r-D_s)^+-(H_{r+1}-D_s)^+,\quad r<m-1,
\]
\[
k_{m-1,s}=(H_{m-1}-D_s)^+.                                    \tag{11}
\]
All k are nonnegative, and low membership \(D_s\le H_0=q_s\)
gives
\[
\sum_{r<m}k_{rs}=q_s-D_s.                                     \tag{12}
\]
The final term deliberately includes the auxiliary budget; it
does not subtract \((\alpha_s-D_s)^+\). For m=1 it is
\((\beta_{0s}+\alpha_s-D_s)^+=q_s-D_s\).

On E_0, with unchanged F, use the residual input
\[
R_0=(P_0\times J)\setminus
       \{(p_r,j):r<m,\ j\in J_H\cup N\},\qquad C_0=I_0\times S.
\]
This is a genuinely partial R family. Use b on good-column
pivots, unchanged x on nonpivot old R, and unchanged y on old C.
Rebuild the actual residual corner sets \(H_0',Z_0'\) from these
input originals. Their witnesses also witness extended corners.

Residual Z costs are unchanged. At residual H use k for a low-row
pivot, zero for a high-row pivot and unchanged h at any other
old left coordinate. No pivot/high H is active, since every
column adjacent to a high row had every pivot R removed.

Writing \(H_{\rm other}\) for actual extended H corners with
old nonpivot left coordinate, the available residual budget obeys
\[
\sum_{H_0'}h'\le
\sum_{H_{\rm other}}h+\sum_{s\in S_L}(q_s-D_s).                 \tag{13}
\]
The first sum excludes Q and all pivots. Auxiliary H budgets
already occur in \(\alpha_s\) and are counted only there.

## 5. Every residual local inequality, including zeros

An old nonpivot conflict keeps (1) unchanged.
For a residual pivot conflict with any old neighbor i, its column
j is good and its row s is low. We need
\[
b_{rj}y_{is}\le k_{rs}z_{ij},                                 \tag{14}
\]
given the original \(B_{rj}y_{is}\le\beta_{rs}z_{ij}\).

Write \(B=B_{rj},\ \beta=\beta_{rs},\ D=D_s,\ w=w_j,\ L=L_j\),
\(V=S_{r+1}(j)\) and \(t=H_{r+1}(s)\).

If \(D\le t\), both ordinary positive parts in (11) are
unclipped, so \(k=\beta\). For the final index,
\(k=\beta+\alpha_s-D\ge\beta\). Since \(b\le B\), (14)
follows from the original inequality. This includes D=0
and the boundary D=t without division.

If \(D>t\), then D>0. Sum (7) over deeper pivots and Q:
\[
(A_j+V)D\le tw.
\]
Since \(L\ge w-A_j\),
\[
L-V\ge w-(A_j+V)\ge w(D-t)/D\ge0.                             \tag{15}
\]
The second positive part in (9) vanishes, so
\(b=(B-(L-V))^+\). If \(\beta=0\), (7) and D>0 force B=0;
hence b=0 and (14) is immediate.
If \(\beta>0\), (7) gives \(w/D\ge B/\beta\). Thus
\[
b\le\bigl(B-B(D-t)/\beta\bigr)^+
   =B(\beta+t-D)^+/\beta
   =Bk/\beta.                                                \tag{16}
\]
In this branch the ordinary second part in (11) is zero;
the same last equality holds for the special final term.
Multiplying by \(y_{is}\ge0\) and using the original local
inequality proves (14).

Every denominator was proved strictly positive before division.
Zero w, A, b, k, beta and auxiliary sums are included.
This step used no neighborhood ordering; it applies at every
old pivot neighbor. Apply the assumed partial-family property
of E_0 to this exact residual instance, obtaining a pruning
with virtual adjusted fee at most (13).

## 6. Old-neighborhood normalization and actual lift

In a good column, if pivot \(p_r\) survives, add every deeper
pivot \(p_t\), t>r, to the residual survivors.
By (5) its old conflict neighbors and old Z coverage are subsets
of those of the surviving \(p_r\), with the same j.
No conflict appears, residual old U is unchanged, and the
nonnegative virtual deletion fee weakly decreases.

Consequently the deleted pivots may be normalized to a prefix
of length \(\ell_j\), \(0\le\ell_j\le m\).
All nonpivot old R and all old C decisions remain unchanged.
For such a prefix its virtual fee is
\[
V_j=\sum_{r<\ell_j}b_{rj}
   =(S_0(j)-L_j)^+-(S_{\ell_j}(j)-L_j)^+.                     \tag{17}
\]

Adopt the normalized old decisions and the new-C choices.
Keep every pivot/Q deletion fixed in J_H and N.
For a good column use these two actual branches:

* If \(L_j=0\) or \(S_{\ell_j}(j)\ge L_j\), delete the same
  pivot prefix, retain its suffix and retain every auxiliary R.
  The actual attached fee equals \(S_0-S_{\ell_j}=V_j\).
  When L>0 the retained suffix has positive total cost and
  contains an actual pivot covering the new corner.
  When L=0 and Q is nonempty an actual retained auxiliary
  covers it even if every auxiliary cost is zero.
  When L=0 and Q is empty, A=0 forces w=0. If all pivots were
  deleted, the new corner can be uncovered, but its profit
  is zero and the same numerical adjusted fee is valid.
* If \(L_j>0\) and \(S_{\ell_j}(j)<L_j\), delete every actual
  pivot and auxiliary R. All new-C neighbors are low and
  deleted, so the new corner is actually uncovered. Its
  adjusted attached fee is
  \(S_0+A-w=S_0-L_j=V_j\).

The boundary \(S_{\ell_j}=L_j\) belongs to the first branch.
In its L=0, empty-Q case no nonexistent auxiliary is used
as a coverage witness.

On shared old residual corners the first branch has identical
survivor coverage. The second branch removes additional pivots
and can only increase actual old U. Old R omitted from the
residual input were already fixed deleted. Q covers no old
right coordinate and new C covers only \(i_*\).
Thus every uncovered residual corner stays actually uncovered.
Extended old corners absent from \(Z_0'\) may add further
nonnegative profit. Actual old-U profit is therefore at least
the residual profit; equal entire corner sets are not assumed.

The lifted survivors are conflict-free. Old conflicts were
settled in the residual pruning. New-C low rows are deleted;
retained high new C has every possible pivot/Q neighbor
deleted in J_H. Retained Q in good columns has only deleted
new-C neighbors. Removing extra pivots creates no conflict.

## 7. Whole budget, partial families and initial retention

Let \(D_0^{\rm virt}\) be the normalized residual pruning's
deletion cost, using b at the good-column pivots, and let
\(U_0'\) be its actual uncovered residual corners. Set
\[
\Phi_0=D_0^{\rm virt}-\sum_{U_0'}z
       \le\sum_{H_0'}h',\qquad
\Phi(T)=D_{\rm del}(T)-\sum_{U(T)}z,
\]
where U(T) is the extended instance's actual uncovered set.
The good-column adjusted fees equal their virtual prefix
fees, and every residual uncovered corner remains actually
uncovered. Hence, for each threshold state,
\[
\begin{aligned}
\Phi(T)\le\Phi_0
 &+\sum_{j\in N}(S_0(j)-L_j)\\
 &+\sum_{j\in J_H}
       \bigl(A_j+S_0(j)-w_j\mathbf1_{\{T\le\mu_j\}}\bigr)\\
 &+\sum_{s\in S_L}D_s
   +\sum_{s\in S_H}D_s\mathbf1_{\{T\le\rho_s\}}.
\end{aligned}
\]
The N terms are negative by (8). Each J_H term has
nonpositive expectation, and each high new-C term has
expectation q_s. The residual choices and good-column
lifts are fixed across threshold states. Taking expectations
and applying (13) therefore gives
\[
\begin{aligned}
\mathbb E[D_{\rm del}-\sum_{\text{actual U}}z]
&\le \sum_{H_{\rm other}}h+
   \sum_{S_L}(q_s-D_s)+\sum_{S_L}D_s+\sum_{S_H}q_s\\
&=\sum_{H_{\rm other}}h+\sum_s
          \bigl(\alpha_s+\sum_{r<m}\beta_{rs}\bigr)
 =\sum_{\text{actual H}}h.                                   \tag{18}
\end{aligned}
\]
Every pivot and auxiliary H corner in the active full input
is actual and counted exactly once in q; all other H corners
belong to \(H_{\rm other}\). Since the threshold distribution
has finite support, one state has adjusted deletion fee at
most its expectation, hence at most \(\sum_H h\) by (18).
Choose that state and use (4) to obtain its actual cover.

F-isolated originals were retained initially. An ordinary old
original initially isolated in the extended graph remains
isolated in the residual graph and is retained there.
Every attached R and new C in an active F coordinate has
a new-star conflict, so none of their fixed deletions discards
an initially conflict-free full-input original.
Residual-isolated old C is also safe: omitted pivots were
fixed deleted, and normalization only adds pivots whose old
conflicts are dominated by an already surviving pivot.

For partial inputs, enlarge R and C to the full families and
give every added original cost zero. Rebuild the padded
instance's actual corner sets \(\widehat H,\widehat Z\).
Keep h and z at the original actual corners H and Z, and
give every corner in \(\widehat H\setminus H\) or
\(\widehat Z\setminus Z\) cost zero. Thus zero padding applies
to all corners made actual by padding, not just those involving
the newly attached coordinate \(i_*\). A padded conflict with
two original input members has its H and Z witnesses in the
original instance, so its local inequality is unchanged.
Every other padded conflict has original-cost product zero
and nonnegative corner-cost product. The padded H+Z budget
therefore equals the original actual H+Z budget.

Construct a padded cover and restrict it to the original
input members and the two tags of each original actual Z
corner. The original augmented graph is the induced subgraph
on these vertices, so this restriction covers every actual
edge and cannot increase its nonnegative cost. Remove any
selected vertices that are isolated in this actual graph.
An initially conflict-free original cannot cover an actual Z
corner: that corner's opposite original witness would conflict
with it. It is therefore isolated and remains a survivor.

Let U be the actual Z corners uncovered by the survivors
of this restricted cover. Their cheapest actual completion
costs no more than the restricted cover. Formula (4) now
gives (3) with this actual U. Padded survivors are not used
as witnesses for actual coverage.
This proves the full preservation lemma.

All suffix operations and comparisons are rational on rational
inputs. Construct one residual pruning, normalize its pivot
prefixes, lift it, and compare the finitely many high states
using rebuilt actual U. This preserves a deterministic finite
feasible construction. Optimality and complexity bounds are
not part of the conclusion.

## 8. Weakly-simplicial elimination and chordal bipartite graphs

In a bipartite graph, a vertex is *weakly simplicial* when
the neighborhoods of its neighbors are linearly ordered by
inclusion. Its neighbors are already independent.
If a right vertex i is weakly simplicial, its left neighbors'
right neighborhoods are nested. Removing their common
coordinate i preserves that nesting.

An ordering \(i_1,\ldots,i_n\) of all right coordinates is
a right weakly-simplicial elimination ordering if \(i_t\)
is weakly simplicial in the relation remaining after
\(i_1,\ldots,i_{t-1}\) are deleted.
Reverse this ordering, starting with all P and no right
coordinates. Each nonisolated restored i has precisely
the nested old-pivot form (6), with Q empty.
Isolated i may be restored trivially. Induction with the
preservation lemma gives the local pair-cost property.

To obtain the ordering from a chordal bipartite E, consider
the hypergraph on active I whose edges are the distinct
nonempty neighborhoods \(N_E(p)\). By
[Brault-Baron, *Hypergraph Acyclicity Revisited*,
arXiv:1403.7076v1](https://arxiv.org/pdf/1403.7076v1),
Characterization 2 (p. 8), beta acyclicity is equivalent
to the impossibility of obtaining an ordinary cycle by
removing hyperedges and vertices.

If such a cycle on k>=3 right coordinates existed, its
k selected neighborhood traces would be distinct adjacent
pairs. Choose their corresponding distinct left coordinates.
In E these selected left and right coordinates induce a
cycle of length 2k, contradicting chordal bipartiteness.
The hypergraph is therefore beta acyclic.
Characterization 9 (pp. 16–17), using Definition 4 and
Theorem 7, gives an elimination ordering whose incident
hyperedges are nested at each removed vertex.
This is exactly the required right weakly-simplicial ordering.
Repeated left neighborhoods preserve nesting even though
the hypergraph combines equal edges; empty left neighborhoods
have no incident right edge. Right coordinates that become
isolated are removed trivially. The argument can be repeated
on every induced residual relation.

For clarity the converse is elementary here. If an induced
cycle of length at least six existed, take its earliest
removed right coordinate i. All other cycle right coordinates
and both its left neighbors remain. Those two left neighborhoods
are incomparable: each contains its other cycle right neighbor,
and the induced-cycle condition excludes the corresponding
chord. Thus i would fail to be weakly simplicial, a contradiction.

Only the classical existence direction is used as a literature
dependency; the cost-preservation argument above is proved
directly. Reversing the ordering proves the E case of the theorem.
The family exchange \((P,I,S,J)\mapsto(S,J,P,I)\), with exchanged
transposed R/C families and H/Z tables, preserves all original
conflicts, coverage edges and costs. It proves the F alternative.

A finite construction may find the elimination ordering by
repeatedly testing right vertices' neighbor inclusions in the
remaining relation. The classical theorem ensures success on
the stated class. The resulting feasible pruning is obtained
by the finite rational construction proved above.

## 9. Complete expansions, sharpness and scope

Replace scalar P/I vertices by nonempty disjoint groups and
each scalar edge by its complete group rectangle.
For full families aggregate x,h over each P group and y,z
over each I group. Summing all local constraints in one
complete rectangle factors into its scalar condition (1).
Lift each scalar original decision to its whole group.

Within an I group and fixed j, R survivor coverage agrees
on every corner because E neighborhoods agree. C coverage
also agrees because its group decisions at each s are whole.
Actual uncovered profits, deleted original costs and H
budgets therefore equal their aggregate values exactly.
Partial families follow by the padded-cover restriction
proved in Section 7. This proves the expansion statement
without asserting any separate graph-class closure result.

The all-ones single-conflict instance is chordal bipartite.
Its two disjoint coverage edges force augmented cover cost
two, equaling its H+Z budget. Feasible prunings either delete
one original, giving \(D_{\rm del}=H+U=1\), or both, giving
\(D_{\rm del}=H+U=2\). The common coefficient one is sharp.

This theorem includes all forests, nested/Ferrers components,
complete blocks and four-cycles. It goes beyond forests
because complete blocks can contain cycles and their
weakly-simplicial extensions need not be globally nested.
It does not settle a pair of unrestricted relations containing
induced cycles of length at least six. Equality classifications,
a general optimum formula and a full Lean proof remain open.

## 10. Provenance and verification boundary

The actual conflict/coverage framework comes from the pinned
[OpenAI pruning source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex).
The earlier [forest theorem](forest-pendant-star-costs.md)
is the single-pivot precursor. The multiple-pivot proof
uses suffix virtual costs and H budgets, normalizes only
the chosen nested old pivots, and compares actual old
coverage rather than assuming identical corner sets.

Weakly-simplicial elimination and the underlying chordal
bipartite characterization are classical. The cited primary
hypergraph proof supplies the needed existence direction;
the incidence translation is explicit in Section 8.
These are prior graph theory, not claimed as new mathematics.
A bounded primary-literature comparison does not establish
worldwide novelty of the independent-cost theorem.
The new general construction has not been Lean-formalized
or implemented as an executable certificate checker.
No new Lean compilation, axiom audit, exhaustive cost
search, unrestricted pruning theorem or upstream
second-neighborhood conclusion is claimed.

**Remark (local conditions do not force the natural total-product bound).**
The local condition (1) does not imply
\((\sum_R x)(\sum_C y)\le(\sum_H h)(\sum_Z z)\), even when
both coordinate relations are chordal bipartite. Take four
disjoint two-element coordinate sets, indexed by 0 and 1,
let E and F be the diagonal matchings, and let R and C
contain only the diagonal originals. Their actual H and Z
also consist of the two diagonal corners. Assign
\[
(x_{00},x_{11})=(4,1),\quad
(y_{00},y_{11})=(1,4),\quad
(h_{00},h_{11})=(z_{00},z_{11})=(2,2).
\]
Each actual conflict satisfies xy=hz=4, whereas the proposed
total-product inequality reads \(25\le16\). The natural
cross-corner maps send the nonconflicting original pairs to
inactive off-diagonal corners; zero padding those corners
does not supply compatibility for these positive products.

This is not a counterexample to the cover or pruning bound.
The actual augmented graph is two disjoint four-vertex paths.
On the first choose C and its opposite Z_R tag; on the second
choose R and its opposite Z_L tag. Their total cover cost is
6, below the H+Z budget 8. Deleting the two cost-one originals
leaves both actual Z corners covered, so U is empty and
the deletion cost 2 is below the H budget 4.

Ahlswede and Daykin's general-map framework requires
compatibility on every pair in a finite domain together with
an appropriate weighted-expansiveness hypothesis; see
their definitions (1.11)--(1.13), Theorem 1 and Theorem 6 in
[the original 1979 paper](https://noah.nrw/ubbihs/download/pdf/5106483).
The example rules out applying its sum-expansion conclusion
with the unchanged original R/C/H/Z totals. It does not
rule out a different encoding or a more elaborate deduction
of the present cover bound, and it establishes no historical
novelty claim.

R. Ahlswede and D. E. Daykin, *Inequalities for a pair of maps
S × S → S with S a finite set*, Mathematische Zeitschrift
165 (1979), 267–289. DOI: 10.1007/BF01437563.
[Original article](https://noah.nrw/ubbihs/download/pdf/5106483).
