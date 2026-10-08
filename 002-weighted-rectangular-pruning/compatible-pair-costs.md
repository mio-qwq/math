# Local pair-cost compatibility under a block relation

Research note, 8 October 2026.

For arbitrary nonnegative costs on coordinate pairs, a local multiplicative condition suffices for rectangular cover and pruning bounds when either coordinate relation is a disjoint union of complete bipartite blocks. The proof gives a deterministic finite-threshold algorithm. The condition permits examples with no common dominating product-weight system. Historical priority has not been checked. This note supplies a written general proof; it is not a Lean formalization.

## 1. Definitions and theorem

Let P,I,S,J be finite sets, possibly empty, with relations E⊆P×I and F⊆S×J and families R⊆P×J and C⊆I×S. Members r=(p,j) and c=(i,s) conflict if E(p,i) and F(s,j). Define the cross-corners

\[
H=\{(p,s):\exists i,j\ ((p,j)\in R,(i,s)\in C,E(p,i),F(s,j))\},
\]
\[
Z=\{(i,j):\exists p,s\ ((p,j)\in R,(i,s)\in C,E(p,i),F(s,j))\}.
\]

A member (p,j) covers (i,j) if E(p,i); a member (i,s) covers (i,j) if F(s,j). The augmented bipartite graph has left side R⊔Z_L and right side C⊔Z_R, all tagged separately. Its edges are the conflicts r–c, edges r–z_R when r covers z, and edges z_L–c when c covers z. There are no Z_L–Z_R edges.

Assign arbitrary nonnegative real costs x_pj to R, y_is to C, h_ps to H and z_ij to Z. Both copies of a Z corner have the same cost z_ij. Suppose every actual conflict satisfies

\[
x_{pj}y_{is}\le h_{ps}z_{ij}. \tag{1}
\]

A relation is a *disjoint union of complete bipartite blocks* if every nonisolated connected component of its bipartite graph is complete bipartite. Isolated coordinates are permitted.

**Theorem.** If either E or F is a disjoint union of complete bipartite blocks, there is a vertex cover K of the augmented graph, containing no isolated vertex, with

\[
w(K)\le\sum_{(p,s)\in H}h_{ps}+\sum_{(i,j)\in Z}z_{ij}. \tag{2}
\]

There are also conflict-free subfamilies R′⊆R and C′⊆C retaining every initially conflict-free original member such that, for the actual set U⊆Z of corners covered by no survivor,

\[
\sum_{R\setminus R'}x_{pj}+\sum_{C\setminus C'}y_{is}
\le\sum_Hh_{ps}+\sum_Uz_{ij}. \tag{3}
\]

For rational costs, a deterministic exact algorithm constructs K,R′,C′ by checking finitely many thresholds. The common coefficient one is sharp, already on the single-conflict all-ones instance.

The product costs of [paper.md](paper.md) satisfy (1) with equality. The theorem here removes factorization in exchange for a structural assumption on one relation. We assert no conclusion from (1) for arbitrary pairs E,F. The two-product obstruction in [boundary.md](boundary.md) fails (1), so it does not contradict this theorem.

## 2. Aggregation in one complete block

First take a block F=S₀×J₀. Group all (p,j)∈R with j∈J₀ into R_p and all (i,s)∈C with s∈S₀ into C_i. An E edge is *active* if these two groups are nonempty. Ignore groups with no active neighbor; their members have no conflict and will be retained. Write

\[
X_p=\sum_{(p,j)\in R_p}x_{pj},\quad
Y_i=\sum_{(i,s)\in C_i}y_{is},
\]
\[
H_p=\sum_{s\in S_0:(p,s)\in H}h_{ps},\quad
Z_i=\sum_{j\in J_0:(i,j)\in Z}z_{ij}.
\]

On an active E edge, every pair from R_p×C_i conflicts. Summing (1) over those pairs gives

\[
X_pY_i\le
\Big(\sum_{s:(i,s)\in C_i}h_{ps}\Big)
\Big(\sum_{j:(p,j)\in R_p}z_{ij}\Big)
\le H_pZ_i. \tag{4}
\]

Every corner in the first two sums exists, witnessed by any member of the other nonempty group. The last inequality adds only nonnegative terms. Original R–Z_R edges still require the same j; aggregation does not replace them by complete adjacency. The cover constructed below selects entire groups and covers every original edge.

## 3. The threshold cover and zero costs

Define extended nonnegative ratios

\[
\alpha_p=
\begin{cases}
0&X_p=0,\\
\infty&H_p=0<X_p,\\
X_p/H_p&H_p>0,
\end{cases}
\qquad
\beta_i=
\begin{cases}
\infty&Y_i=0,\\
Z_i/Y_i&Y_i>0.
\end{cases}
\]

Equation (4) implies α_p≤β_i on every active E edge. For X_p=0 this is immediate. If H_p=0<X_p, (4) forces Y_i=0. All other nontrivial cases follow by dividing by positive H_p and Y_i.

Fix a finite threshold T≥1. Select all R_p with α_p≤T. Let Q(T) consist of active indices i with an unselected R_p neighbor. For i∈Q(T), select all C_i and all Z_R corners with that i in the block. For i∉Q(T), select the cheaper whole group between C_i and its Z_L corners; resolve ties by selecting C_i.

This is a cover. If an original R endpoint is unselected, every adjacent C group and every adjacent Z_R group is selected because its i belongs to Q. For any Z_L–C edge, the C group or its entire Z_L group is selected. No isolated original member is selected. Its cost is

\[
k(T)=\sum_{\alpha_p\le T}X_p+
\sum_i\min(Y_i,Z_i)+\sum_{i\in Q(T)}\max(Y_i,Z_i). \tag{5}
\]

## 4. A finite weighted-average proof

Let `1=τ₀<τ₁<⋯<τ_m` list 1 and all distinct finite α_p>1. The cover changes only at these thresholds. Put

\[
\lambda_\ell=\frac1{\tau_\ell}-\frac1{\tau_{\ell+1}}
\quad(\ell<m),\qquad
\lambda_m=\frac1{\tau_m}.
\]

These positive weights sum to one. The total weight of thresholds at which a finite α_p>1 is selected is exactly 1/α_p. It is one for α_p≤1 and zero for α_p=∞. Therefore the weighted-average cost of a selected R_p is at most H_p: it equals H_p for finite α_p>1, is X_p≤H_p for α_p≤1, and is zero for α_p=∞. This covers all zero-cost cases.

For an active i, let γ_i be the maximum α_p of its neighbors. Then i∈Q(T) precisely when T<γ_i. If γ_i is finite and greater than one, it is an actual threshold, so the total weight of Q is 1−1/γ_i. It is zero for γ_i≤1 and one for γ_i=∞. Since γ_i≤β_i:

* If Y_i=0, the cost of this group in every cover is at most Z_i.
* If Y_i>0 and Z_i≤Y_i, then β_i≤1 and Q is empty at every threshold. Its cost is Z_i.
* If Z_i>Y_i>0, the total weight of Q is at most 1−Y_i/Z_i. By (5), its average cost is at most `Y_i+Z_i(1−Y_i/Z_i)=Z_i`.

Thus

\[
\sum_{\ell=0}^m\lambda_\ell k(\tau_\ell)
\le\sum_pH_p+\sum_iZ_i.
\]

At least one listed threshold satisfies this bound. Computing every candidate and taking the least-cost one is a deterministic construction. There are at most one plus the number of active R groups candidates. For rational input, ratios and comparisons are exact rational operations of polynomial bit complexity in the explicit input size. No approximation of real zero costs is needed in the proof.

## 5. Multiple blocks, symmetry and pruning

If F is a disjoint union of blocks S_t×J_t, different blocks have disjoint R,C vertices and disjoint H,Z corners, because their S and J coordinates are disjoint. All conflicts and coverage edges stay in their block. Apply the construction separately and take the union. Originals involving isolated S or J coordinates are retained.

For E a block union, interchange the coordinate sets as `(P,I,S,J)↦(S,J,P,I)`, exchange the transposed original families, and exchange x and y. The new F is the old E; H and Z are transposed and keep their costs. This proves the symmetric case.

Delete precisely the original vertices in K. Since conflict edges are covered, the survivors are conflict-free. Initially conflict-free originals are isolated even in the augmented graph: if one covered a Z corner, that corner's witness on the opposite side would conflict with it. They are therefore retained.

Each corner covered by a survivor forces its opposite Z copy into K. Distinct corners charge distinct selected copies, so the deletion cost D satisfies

\[
D\le w(K)-\sum_{Z\setminus U}z
\le\sum_Hh+\sum_Uz.
\]

An entire selected corner group may contain a corner covered by no survivor. Consequently the actual U must be reconstructed from survivors; it need not equal the set with neither Z copy selected. The inequality above accommodates such extra copies.

## 6. A tight nonproduct example

Take S={s}, J={j}, F={(s,j)}, P={p₁,p₂}, I={i₁,i₂} and E={(p₁,i₁),(p₂,i₁),(p₂,i₂)}. Include all two R and two C members. Let

\[
x=(4,1),\quad y=(1,1),\quad h=(1,1),\quad z=(4,1).
\]

The three local tests are `4≤4, 1≤4, 1≤1`. Threshold T=1 selects R₂,C₁,C₂,ZR₁, costing 7=ΣH+ΣZ. Its original deletion costs 3; the surviving R₁ covers z₁ and the actual U={z₂}, giving equality 3=2+1 in (3).

The cover is optimal: put edge-packing amounts 4,1,1,1 on R₁–ZR₁, R₂–ZR₂, ZL₁–C₁, ZL₂–C₂. Each vertex's incident amount is within its cost and the total is 7, so every cover costs at least 7. This optional lower bound is specific to this example; the general checker does not certify optimality.

There is not even a common product system dominating these costs in the directions `x≤ad, y≤bc, h≥ac, z≥bd`. Its positive c,d would require

\[
\max_p x_p/h_p\le d/c\le\min_i z_i/y_i,
\]

that is, 4≤d/c≤1. The new theorem therefore goes beyond exact product weights and their common monotone domination.

For sharpness of the universal coefficient, the one-conflict all-ones graph is a four-vertex path whose minimum cover costs two and whose H+Z budget is two. Every feasible pruning also has deletion-to-(H+U) ratio one.

## 7. Exact implementation and certificate scope

[compatible_pair_costs.py](code/compatible_pair_costs.py) checks the local condition and detects complete blocks by connected components. It applies the finite thresholds in the F orientation, or transposes to the E orientation, retaining full pair costs. It emits an explicit cover, survivors, actual U and exact masses. Its construction trace is explanatory data.

[check_compatible_pair_costs.py](code/check_compatible_pair_costs.py) independently rebuilds the conflicts, corners, coverage edges and costs. It characterizes the structured relation by a different test: intersecting left neighborhoods must coincide. It checks local constraints, every covered edge, absence of isolated selected vertices, survivor preservation, actual U, and both numerical bounds. The normal checker neither imports the constructor nor searches for thresholds; it ignores the construction trace. It proves certificate feasibility and bounds, not optimality.

Coordinates are zero-based integers. Input uses format `compatible-pair-costs-v1`, sizes P,I,S,J, pair lists E,F,R,C and full cost matrices R(P×J), C(I×S), H(P×S), Z(I×J). All entries are nonnegative rational strings, including unused pairs. Duplicate pairs, floats, negative costs and relations outside the structural class are rejected. Empty domains are allowed.

[The example suite](examples/compatible-pair-costs.json) contains eight certificates, including the tight nonproduct case, both zero-denominator branches, selected extra corner copies, isolated originals, the E-oriented branch, multiple F blocks and an empty domain. From this directory:

```text
python -B code/check_compatible_pair_costs.py examples/compatible-pair-costs.json
python -B -O code/check_compatible_pair_costs.py examples/compatible-pair-costs.json
python -B code/compatible_pair_costs.py INPUT.json OUTPUT.certificate.json
python -B code/check_compatible_pair_costs.py OUTPUT.certificate.json
python -B code/check_compatible_pair_costs.py --self-test
python -B code/check_compatible_rectangular.py
```

The constructor can also recompute an example suite from the instances inside it. The optional self-test invokes the constructor to obtain candidates and passes them through the independent checker. It uses a fixed seed for a bounded set of 2×2 instances, including nonzero and zero costs, and verifies rejection of damaged certificates and unsupported structures. Actual commands, counts and hashes are recorded in [compatible-pair-costs.validation.json](compatible-pair-costs.validation.json). These finite checks support implementation reproducibility; Sections 2–5 prove the general real-cost theorem. No Lean or full arbitrary-relation local-cost theorem is claimed.
