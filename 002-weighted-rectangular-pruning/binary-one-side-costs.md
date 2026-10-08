# Local pair-cost bounds for block and four-path expansions

Research note, 8 October 2026.

This note extends the [binary-coordinate theorem](double-path-independent-costs.md):
one of the coordinate relations can be a union of complete bipartite
blocks and complete four-path expansions. The other relation can be any
finite relation. In particular, one binary coordinate relation suffices,
while the other can have arbitrary size. All
original and corner costs may be independently chosen nonnegative
real numbers, subject to the actual local conflict inequalities.
The proof treats zero costs directly, without positive approximation.
It is written mathematics, not a Lean formalization or a historical
priority claim.

## 1. Statement and the remaining structural case

Use the definitions of [compatible-pair-costs.md](compatible-pair-costs.md).
Thus \(E\subseteq P\times I\), \(F\subseteq S\times J\),
\(R\subseteq P\times J\), \(C\subseteq I\times S\); an original
\((p,j)\) conflicts with \((i,s)\) exactly when \(E(p,i)\) and \(F(s,j)\).
The actual cross-corners are \(H=(p,s)\), \(Z=(i,j)\) witnessed by
these conflicts. An \(R\) original covers \((i,j)\) when \(E(p,i)\);
a \(C\) original covers it when \(F(s,j)\).
The augmented graph has tagged sides \(R\sqcup Z_L\), \(C\sqcup Z_R\),
with original conflicts and these two coverage edge families only.

Assign nonnegative original costs \(x_{pj},y_{is}\), corner costs
\(h_{ps},z_{ij}\), and the same cost to both copies of each \(Z\).
Assume
\[
x_{pj}y_{is}\le h_{ps}z_{ij}
\quad\text{for every actual conflict}. \tag{1}
\]

**Theorem.** If \(|P|,|I|\le2\), or if \(|S|,|J|\le2\), the actual
augmented graph has a vertex cover of cost at most
\(\sum_Hh+\sum_Zz\), containing no isolated vertex.
There are conflict-free survivors retaining every initially
conflict-free original and satisfying
\[
D_{\rm del}\le\sum_Hh+\sum_{z\in U}z, \tag{2}
\]
where \(U\) is the actual uncovered corner set.
The coefficient one is sharp. Rational inputs admit a deterministic
finite construction.

If either relation is a disjoint union of complete bipartite blocks,
the [block theorem](compatible-pair-costs.md) already proves the result.
A binary relation that is not such a union is precisely a three-edge
four-vertex path, up to independent relabeling of its two sides.
We first treat
\[
P=I=\{0,1\},\quad E=\{(0,0),(0,1),(1,1)\}, \tag{3}
\]
with arbitrary \(F\) and complete original families.
Section 5 then handles partial families and the symmetric alternative.

## 2. Full grids and the actual adjusted deletion cost

Remove isolated coordinates of \(F\) temporarily. Their corresponding
originals have no conflict or augmented coverage edge and are retained.
On the remaining nonempty coordinates put
\[
a_j=x_{0j},\quad c_j=x_{1j},\quad
A_s=y_{0s},\quad C_s=y_{1s},
\]
\[
\alpha_s=h_{0s},\quad \gamma_s=h_{1s},\quad
u_j=z_{0j},\quad w_j=z_{1j}.
\]
Here \(C_s\) denotes a cost, not the original family.
All \(H\) and \(Z\) corners on the remaining full grids are actual.
For every \(F(s,j)\), (1) becomes exactly
\[
a_jA_s\le\alpha_su_j,\qquad
a_jC_s\le\alpha_sw_j,\qquad
c_jC_s\le\gamma_sw_j. \tag{4}
\]
No other cost inequalities are assumed.

For any conflict-free survivors, a corner cannot be covered from both
sides: those covering originals would conflict. Their cheapest
augmented completion therefore has cost
\[
\sum_Zz+D_{\rm del}-\sum_{z\in U}z. \tag{5}
\]
When a corner is survivor-covered, select the opposite tagged copy;
when it is uncovered, select neither copy. Together with the deleted
originals these selections cover every augmented edge. Conversely,
every augmented cover restricts to an original conflict cover, and
its corner part costs at least this cheapest completion.
It is enough to construct a deletion with adjusted cost at most
\(\sum_s(\alpha_s+\gamma_s)\).

Partition rows by
\[
S_H=\{s:C_s>\alpha_s+\gamma_s\},\qquad S_L=S\setminus S_H.
\]
Let \(J_H\) be the columns adjacent under \(F\) to any row of \(S_H\),
and \(J_L=J\setminus J_H\).

## 3. High rows: a finite coupled construction

For \(s\in S_H\), set
\[
\lambda_s=(\alpha_s+\gamma_s)/C_s\in[0,1).
\]
This division is valid since every high \(C_s\) is positive.
Always delete both \(R\) originals in \(J_H\), and always retain
all high originals \(A_s\).
Using a common parameter \(T\in(0,1]\), delete high \(C_s\) exactly
when \(T\le\lambda_s\). Delete every low \(C_s\); the remaining
low originals are dealt with in Section 4.

For \(j\in J_H\), its \(u_j\) corner stays covered by a retained high
\(A_s\). Its \(w_j\) corner is uncovered exactly when every adjacent
high \(C_s\) is deleted, since both \(R\) originals and all low \(C_s\)
are deleted. This event has probability
\[
\min_{\substack{s\in S_H\\F(s,j)}}\lambda_s
\]
under a common uniform \(T\). The high-neighbor set is nonempty.
By (4), for each such neighbor,
\[
a_j+c_j\le\lambda_s w_j. \tag{6}
\]
Consequently the expected adjusted contribution of high rows and
their neighboring columns is at most
\[
\begin{aligned}
&\sum_{s\in S_H}C_s\lambda_s
+\sum_{j\in J_H}
\left(a_j+c_j-w_j
 \min_{\substack{s\in S_H\\F(s,j)}}\lambda_s\right)\\
&\hspace{2em}\le\sum_{s\in S_H}(\alpha_s+\gamma_s). \tag{7}
\end{aligned}
\]
No \(u_j\) gain is charged in these columns.

This is a finite weighted-average argument. Sort the distinct positive
values of \(\lambda_s\), append \(1\), and use those values as candidate
\(T\)'s. Give each candidate the length of the interval from the
preceding value, starting at zero. The marginal probability of
\(T\le\lambda_s\) is exactly \(\lambda_s\), and the simultaneous
probability above is its indicated minimum. Zero \(\lambda_s\) is
never selected for deletion in these positive-\(T\) candidates.
There are at most \(|S_H|+1\) candidates. If \(S_H\) is empty,
use \(T=1\). Thus (7) requires neither randomized output nor a
limiting algorithm.

## 4. Low rows: eliminate the bottom cost and use one block

For \(s\in S_L\), put
\[
k_s=\alpha_s+\gamma_s-C_s\ge0.
\]
For \(j\in J_L\), set
\[
a_j^*=a_j-(w_j-c_j)_+.
\]
These columns have only low neighbors.
If \(a_j^*<0\), delete both originals \(a_j,c_j\).
Then \(w_j>c_j\), the actual \(w_j\) corner is uncovered, and the
adjusted contribution is exactly
\(a_j+c_j-w_j=a_j^*<0\). Any additional uncovered \(u_j\) gain
can safely be omitted from the upper bound.

For the other columns \(J_+=\{j\in J_L:a_j^*\ge0\}\), we claim
\[
a_j^*A_s\le k_su_j
\quad\text{whenever }s\in S_L,\ j\in J_+,\ F(s,j). \tag{8}
\]
If \(C_s\le\gamma_s\), then \(k_s\ge\alpha_s\), and
\(a_j^*\le a_j\) together with (4) proves (8).
If \(C_s>\gamma_s\), low membership gives
\(\alpha_s\ge C_s-\gamma_s>0\); both denominators below are positive.
The last two inequalities in (4) yield
\[
(w_j-c_j)_+
\ge w_j(C_s-\gamma_s)/C_s
\ge a_j(C_s-\gamma_s)/\alpha_s.
\]
Hence \(a_j^*\le a_jk_s/\alpha_s\).
Multiply by \(A_s\ge0\) and use the first inequality in (4) to
prove (8). This includes \(k_s=0\) and all zero original or corner
costs. No division by a possibly zero \(\alpha_s\) is made.

Consider the residual top-only problem: one \(E\) edge, the relation
\(F\) restricted to \(S_L\times J_+\), original costs \(a_j^*,A_s\),
and corner costs \(k_s,u_j\). Its one-edge \(E\) is a complete
bipartite block, so (8) permits the already proved block theorem.
Let \(D_B,U_B\) be its deletion cost and actual uncovered corner set.
It gives conflict-free residual survivors with
\[
D_B-\sum_{j\in U_B}u_j
\le \sum_{\substack{s\in S_L\\
                    s\text{ has a residual neighbor}}}k_s
\le \sum_{s\in S_L}k_s. \tag{9}
\]
Its initially isolated \(A_s\)'s can be retained, and the conclusion
also covers an empty residual problem.

Translate its choices back to actual originals. If \(a_j\) is
retained, retain \(c_j\) too. If \(a_j\) is deleted, delete \(c_j\)
exactly when \(c_j<w_j\); otherwise retain it. Since all neighboring
\(C_s\)'s are low and deleted, the resulting original deletion cost
minus its \(w_j\) gain is exactly \(a_j^*\) for a deleted top original,
and zero for a retained top original.
The actual \(u_j\) uncovered set in \(J_+\) is precisely \(U_B\):
there is no adjacent high \(A_s\), the bottom original cannot cover
\(u_j\), and the remaining top originals are exactly those of
the residual problem.

These choices are conflict-free. In \(J_H\) both originals are deleted;
in \(J_L\), all bottom \(C_s\)'s are deleted and the remaining top
conflicts are covered by the residual solution or the forced negative
column deletions. The additional deletion of all low \(C_s\)'s costs
\(\sum_{s\in S_L}C_s\).
Combining (7), the nonpositive negative-column contributions, and (9),
the expected total adjusted cost is at most
\[
\sum_{s\in S_H}(\alpha_s+\gamma_s)
+\sum_{s\in S_L}(C_s+k_s)
=\sum_s(\alpha_s+\gamma_s). \tag{10}
\]
The low solution is fixed across the finite high-row choices, so
one of those actual finite deletions attains (10).
Equation (5) then proves both desired bounds.
Every step above is valid directly for nonnegative costs.

## 5. Partial families, symmetry and construction

For partial originals on (3), fill the missing full-grid originals
with cost zero. Fill corners outside the actual \(H,Z\) with zero
cost, preserving all actual costs. A new full-grid conflict either
has both originals present and keeps its assumed inequality, or
has a zero-cost missing original and satisfies (1) automatically.
The completed budget is the unchanged actual \(\sum_Hh+\sum_Zz\).

Apply Sections 2–4 to this nonnegative full-grid problem, then
restrict its cover to the actual originals and the two actual \(Z\)
copies. The actual augmented graph is the induced subgraph on those
vertices, so restriction preserves every edge and does not increase
cost. Remove all isolated vertices from the restricted cover.

An initially conflict-free original is isolated in this actual
augmented graph: if it covered an actual \(Z\), that corner's
opposite-original witness would give a conflict with it.
Thus the unselected originals retain every initially conflict-free
original. Taking their cheapest completion, as in (5), gives
(2) for the actual uncovered set. No artificial padded corner
appears in its budget.

This proves the \(|P|,|I|\le2\) alternative, since all remaining
binary relations are block unions. For \(|S|,|J|\le2\), swap the
families and transpose coordinates: new \(R\) consists of old
\((s,i)\), new \(C\) of old \((j,p)\), new \(E=F\), new \(F=E\).
The \(H,Z\) costs transpose as well, and the conflict and coverage
conditions are preserved. The already proved alternative applies.

For rational input all relabeling, high/low decisions, modified costs
and finite probabilities use exact rational operations. Use the
existing finite threshold construction for the residual block,
compare the at most \(|S_H|+1\) actual high choices, then restrict
and remove isolated vertices. This gives a deterministic finite
construction, including zero costs. We do not claim that this
construction computes the general optimum; the fifteen-candidate
optimum belongs to the smaller full double-path theorem.

## 6. Complete four-path expansions and disjoint components

A *complete four-path expansion* is the bipartite relation with
disjoint nonempty coordinate groups \(P_0,P_1\) and \(I_0,I_1\), and
edge set
\[
(P_0\times I_0)\ \cup\ (P_0\times I_1)\
\cup\ (P_1\times I_1). \tag{11}
\]
Thus each vertex of the four-vertex path is replaced by a nonempty
group, each old edge by the complete rectangle between its groups,
and no other edge is added.

**Structural theorem.** The conclusions of Section 1 hold whenever
every nonisolated component of either \(E\) or \(F\) is a complete
bipartite block or a complete four-path expansion. The other relation
is arbitrary. This permits arbitrarily large coordinates and arbitrary
partial original families, with all independent nonnegative costs.

**Proof for one expanded component and full original families.**
First remove isolated \(F\) coordinates as in Section 2. On every
remaining \(j,s\), aggregate
\[
\begin{aligned}
a_j&=\sum_{p\in P_0}x_{pj},&
c_j&=\sum_{p\in P_1}x_{pj},\\
A_s&=\sum_{i\in I_0}y_{is},&
C_s&=\sum_{i\in I_1}y_{is},\\
\alpha_s&=\sum_{p\in P_0}h_{ps},&
\gamma_s&=\sum_{p\in P_1}h_{ps},\\
u_j&=\sum_{i\in I_0}z_{ij},&
w_j&=\sum_{i\in I_1}z_{ij}.
\end{aligned} \tag{12}
\]
All these corners are actual on the full grid. For each \(F(s,j)\),
sum (1) over the three complete edge rectangles in (11).
For example the rectangle \(P_0\times I_0\) gives
\[
\left(\sum_{p\in P_0}x_{pj}\right)
\left(\sum_{i\in I_0}y_{is}\right)
\le
\left(\sum_{p\in P_0}h_{ps}\right)
\left(\sum_{i\in I_0}z_{ij}\right).
\]
The three sums are exactly the three scalar inequalities (4).
Apply the nonnegative full-grid theorem of Sections 2–4.

Lift each scalar original decision to retaining or deleting the
corresponding whole original group. The conflict rule agrees exactly
with the scalar path. Within either \(I\) group at a fixed \(j\),
the \(R\)-coverage decision is shared because its vertices have the
same \(E\)-neighbor groups. The \(C\)-coverage decision is also shared,
because every original \(I\) group at each \(s\) is retained or deleted
as a whole. Consequently all corners \((i,j)\) in one such group
are simultaneously covered or uncovered. Their total actual gain is
precisely \(u_j\) or \(w_j\). Lifted deletion costs and the \(H\)
budget also equal (12) exactly. Thus the scalar pruning bound lifts
to the expanded component, and its cheapest completion proves the
cover bound. This is whole-group aggregation of complete rectangles;
it does not replace the actual coverage edges by arbitrary new edges.

For partial families, pad all missing originals with cost zero and
all new corners with cost zero, and apply this full-grid construction.
Only after constructing a full augmented cover, restrict it to the
actual induced graph, remove isolated vertices and take its cheapest
completion. Section 5 proves that this preserves the actual budget
and retention. A dummy survivor in the padded model is not used as
a survivor-coverage witness in the final partial problem.

For a disjoint union of components of \(E\), every nonisolated
original and every corner belongs to one component through its
\(P\) or \(I\) coordinate. Every conflict and coverage edge stays
in that component. The component subgraphs, actual \(H\)'s and
actual \(Z\)'s are disjoint even if their \(S,J\) coordinates overlap.
Apply the block theorem or expanded-path theorem to each component
and unite the covers and pruning choices. No original cost or
corner budget is counted twice. Isolated \(E\) coordinates give
isolated originals, which are retained. The empty relation is
included. Symmetry from Section 5 handles the stated hypothesis
on \(F\) instead. This proves the structural theorem. \(\square\)

An empty group in (11) is unnecessary for the definition; the
resulting degenerate edge patterns are complete-block unions and
already fall under the other component case. The exact rational
construction applies per component with the aggregation (12).
It supplies a feasible bound, without claiming an optimal cover
for general expanded components.

## 7. Sharpness, provenance and open scope

The single-conflict all-ones instance is in the theorem's domain.
Its two disjoint coverage edges force cover cost at least two,
equal to \(\sum_Hh+\sum_Zz=2\); deleting either original gives
\(D_{\rm del}=1=\sum_Hh\) with \(U\) empty. Deleting both costs two
and has \(U=Z\). Both constants are therefore sharp.

The conflict/coverage framework comes from the pinned
[OpenAI pruning source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/02-pruning.tex).
The [block theorem](compatible-pair-costs.md) is an essential
mathematical antecedent, including its treatment of zero costs and
initially isolated originals. This proof extends the independent-cost
domain through a high-row coupling, actual bottom-corner profits and
a residual one-edge block. The [double-path theorem](double-path-independent-costs.md)
remains a separate exact optimum calculation.

Weighted threshold arguments and four-functions inequalities are
classical methods. Ahlswede and Daykin's original
[*Inequalities for a pair of maps \(S\times S\to S\) with \(S\) a
finite set*](https://www.math.uni-bielefeld.de/ahlswede/homepage/public/33.pdf),
Math. Z. 165 (1979), 267–289, defines weight compatibility for all
ordered pairs in (1.11), and its product theorem proof in Section 3
retains that hypothesis. Our assumptions apply to actual conflicts;
no direct invocation replacing those missing hypotheses is supplied.
This bounded comparison does not establish global novelty.

When neither coordinate relation has the component structure of
Section 6, local sufficiency remains open.
The complete independent-cost theorem for arbitrary relations,
general equality classification and a full Lean formalization
remain separate tasks. No conclusion about the upstream
second-neighborhood conjecture or historical priority is asserted.
