# Two local-cost families on reflexive rectangular relations

Research note, 8 October 2026.

This note proves two families of the local pair-cost cover and pruning bounds. The first allows arbitrary reflexive relations with proportional original cost tables. The second allows a specified nonproportional family on two four-vertex paths. Neither statement requires a common rank-one product cost table. The proofs include all zero costs. They do not establish the local-cost bound for arbitrary independent original costs or arbitrary rectangular relations. Historical priority has not been checked, and these are written proofs rather than Lean formalizations.

## 1. The actual graph and local condition

Let T,V be finite sets, possibly empty. Set P=I=T and S=J=V, and take the complete original families R=T×V and C=T×V, with separate graph tags. Let E⊆T×T and F⊆V×V contain every diagonal pair. The original r=(p,j) and c=(i,s) conflict exactly when E(p,i) and F(s,j). Define H and Z as the sets of cross-corners (p,s) and (i,j) produced by actual conflicts. Diagonal conflicts give H=Z=T×V.

The augmented bipartite graph has left side R⊔Z_L and right side C⊔Z_R. Its edges are all original conflicts, r–z_R when r=(p,j), z=(i,j) and E(p,i), and z_L–c when z=(i,j), c=(i,s) and F(s,j). There are no edges between the two Z copies. Every vertex has a diagonal edge when the grid is nonempty.

Assign arbitrary nonnegative costs x_pj to R, y_is to C, h_ps to H and z_ij to both Z copies. Assume for every actual conflict that

\[
x_{pj}y_{is}\le h_{ps}z_{ij}. \tag{1}
\]

Write H₀=Σ_Hh, Z₀=Σ_Zz. The desired bounds are a cover K with w(K)≤H₀+Z₀ and conflict-free survivors R′,C′ with

\[
D:=\sum_{R\setminus R'}x+\sum_{C\setminus C'}y
\le H_0+\sum_{U}z, \tag{2}
\]

where U is the actual set of Z corners covered by no survivor. Covering a corner uses the same coordinate and relation as its augmented edge. Initially conflict-free originals must be retained; there are none on a nonempty complete reflexive grid.

## 2. Proportional complete-grid costs

**Theorem 1.** For arbitrary E,F as above, any nonnegative table w:T×V→ℝ and any κ≥0, put x_tv=w_tv and y_tv=κw_tv. If (1) holds, both bounds hold. Only three complete covers need be compared.

**Proof.** Let W=Σw. The diagonal conflicts r=(t,v),c=(t,v) give κw_tv²≤h_tvz_tv. The finite Cauchy–Schwarz inequality gives

\[
\kappa W^2
\le\left(\sum_{t,v}\sqrt{h_{tv}z_{tv}}\right)^2
\le H_0Z_0. \tag{3}
\]

Thus X=W and Y=κW satisfy XY≤H₀Z₀. The following are actual covers and associated deletions:

| Cover | Cover cost | Originals deleted | Actual U |
| --- | --- | --- | --- |
| R⊔Z_L | X+Z₀ | R | Empty: each corner has a surviving diagonal C member |
| C⊔Z_R | Y+Z₀ | C | Empty: each corner has a surviving diagonal R member |
| R⊔C | X+Y | R and C | Z |

For any nonnegative X,Y,H,Z with XY≤HZ, at least one of X≤H, Y≤H or X+Y≤H+Z holds. Indeed, if the first two fail, X>H and Y>H. H cannot be zero, since then XY≤0 would fail. Expanding (X−H)(Y−H)>0 gives X+Y−XY/H<H; since Z≥XY/H, the third inequality follows. Select the corresponding row of the table. Its cover and actual deletion satisfy both bounds. If W=0, κ=0 or the grid is empty, the same cases select a zero-cost deletion directly. No division by a zero pair cost is used. ∎

This is a constructive algorithm with three comparisons after checking the input. It does not restrict E,F to disjoint complete bipartite blocks, as in [compatible-pair-costs.md](compatible-pair-costs.md). It does restrict the two original cost tables to the same table up to a global nonnegative factor. That table need not factor into row and column weights.

## 3. A sharp example with two nonblock relations

Take T=V={0,1} and

\[
E=F=\{(0,0),(0,1),(1,1)\}.
\]

Each relation is a four-vertex path, rather than a union of complete bipartite components. Take

\[
w=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad
\kappa=3,\quad x=w,\ y=3w,\ h=w,\ z=3w.
\]

The nine actual original conflict edges are

\[
r_{00}c_{00},\ r_{00}c_{10},\
r_{01}c_{00},\ r_{01}c_{01},\ r_{01}c_{10},\ r_{01}c_{11},\
r_{10}c_{10},\ r_{11}c_{10},\ r_{11}c_{11}. \tag{4}
\]

Eight local checks are equalities; r₀₁c₁₀ requires only w₀₁w₁₀≤w₀₀w₁₁, here 1≤4. W=6, H₀=6 and Z₀=18. Any of the first and third covers in the table costs 24, equal to H₀+Z₀.

For an exact lower bound, put amount w_tv on each diagonal coverage edge r_tv–ZR_tv, and amount 3w_tv on each ZL_tv–c_tv. These eight edges share no endpoints. Each vertex's incident amount is at most its cost, and their total is 24. Any cover pays at least this total: charge each edge amount to a selected endpoint, and use the vertex capacity bounds. Thus the cover constant one is sharp.

Every conflict-free deletion deletes at least one member of each diagonal original pair, costing at least w_tv. If (t,v) is actually uncovered, both its diagonal originals must be deleted, forcing an additional 3w_tv. Therefore every feasible deletion satisfies

\[
D\ge W+3\sum_{(t,v)\in U}w_{tv}=H_0+\sum_Uz.
\]

Deleting all R attains equality with U empty, so the pruning constant one is sharp as well. The same argument works with any positive 2×2 w satisfying w₀₁w₁₀≤w₀₀w₁₁, with h=min(1,κ)w and z=max(1,κ)w. For the displayed example, det(w)=3, so its original R costs are not a rank-one product table.

## 4. Nonproportional symmetric exchange costs on two paths

**Theorem 2.** On the fixed two-path structure (4), let a,b≥0 and

\[
x=\begin{pmatrix}a&b\\b&a\end{pmatrix},\qquad
y=\begin{pmatrix}b&a\\a&b\end{pmatrix}.
\]

For any nonnegative h,z satisfying the nine local conditions (1), deleting all originals satisfies (2), and R⊔C satisfies the cover bound. For a,b>0 and a≠b, the original tables are not proportional.

**Proof.** For each H corner choose a probability distribution μ_h on actual conflict witnesses of that corner. Let

\[
v_z=\sum_h\sum_{e:\,z(e)=z}\mu_{he}x_{r(e)}y_{c(e)},
\quad
B_z=\sum_h\sum_{e:\,z(e)=z}\mu_{he}h_h.
\]

Multiplying each local condition by its witness probability and summing at a fixed Z corner gives v_z≤B_zz_z. The per-H probability sums give Σ_zB_z=H₀. Hence, directly for nonnegative costs,

\[
H_0+Z_0=\sum_z(B_z+z_z)
\ge2\sum_z\sqrt{B_zz_z}
\ge2\sum_z\sqrt{v_z}. \tag{5}
\]

No division by z or passage to a positive limit is needed.

Suppose b≥a and b>0, and set θ=(b−a)/b. Use the following probabilities; the notation in each entry specifies the actual original conflict witness, its Z corner, and its probability.

| H corner | Witness choices |
| --- | --- |
| H00 | r00–c00 at Z00 with 1−θ; r01–c00 at Z01 with θ |
| H01 | r01–c01 at Z01 with 1−θ; r01–c11 at Z11 with θ |
| H10 | r10–c10 at Z10 with 1 |
| H11 | r11–c11 at Z11 with 1 |

All choices occur in (4), and their probabilities sum to one for each H. They give, in Z order 00,01,10,11,

\[
v=(a^2,\ a^2+b^2-ab,\ ab,\ b^2).
\]

Since a²+b²−ab≥ab, squaring the two nonnegative sides shows

\[
\sqrt{ab}+\sqrt{a^2+b^2-ab}\ge a+b.
\]

Thus 2Σ√v≥4(a+b)=Σx+Σy. By (5), the all-original cover costs at most H₀+Z₀. Its survivors are empty, so its actual U is all Z and the deletion has the same bound.

If a≥b and a>0, set θ=(a−b)/a. Instead mix H00 between r00–c00 at Z00 and r00–c10 at Z10, and H10 between r10–c10 at Z10 and r11–c10 at Z11, with respective weights 1−θ and θ. Keep the other two diagonal witnesses. This gives v=(b²,ab,b²+a²−ab,a²), proving the same inequality. These formulas also cover one of a,b being zero. If both are zero, the all-original cost is zero and the conclusion is immediate. ∎

For the concrete nonproportional case a=1,b=4, the first witness distribution gives v=(1,13,4,16). The rational lower bounds ℓ=(1,7/2,2,4) satisfy ℓ_z²≤v_z and 2Σℓ=21, while all-original cost is 20. Thus every locally feasible h,z has H₀+Z₀≥21, so the chosen cover and deletion meet the bound with a certified margin at least one. This proves a fixed original-cost family for all angle costs, rather than checking one numerical angle-cost instance. It does not assert that the margin one is optimal.

## 5. Exact checks and limitations

[check_reflexive_cost_families.py](code/check_reflexive_cost_families.py) is a standard-library exact rational checker. For proportional inputs it reconstructs the actual graph, checks every local condition, compares the three complete covers, and checks the true survivor-covered set U. When a sharpness certificate is requested, it checks the diagonal edge packing and the diagonal deletion lower bound. For exchange inputs it checks the nine actual conflicts and every witness's support and probability, reconstructs v, and verifies optional rational square-root lower bounds. The supplied h,z are independently checked against every local condition. Witness support checks remain active under Python's optimization flag.

[examples/reflexive-cost-families.json](examples/reflexive-cost-families.json) supplies exact rational examples and zero-cost boundary cases. Run from this directory:

```text
python -B code/check_reflexive_cost_families.py examples/reflexive-cost-families.json
python -B -O code/check_reflexive_cost_families.py examples/reflexive-cost-families.json
python -B code/check_reflexive_cost_families.py --self-test
python -B code/check_reflexive_independent.py
```

The separate independent checker imports neither the family constructor nor its checker. It rebuilds the graph and actual uncovered sets, checks the diagonal packing, and exhausts original deletion subsets only when there are at most eight original vertices. The supplied 12 fixtures require 2,069 such subsets in total. Its optimum calculations are fixture checks, not a claim that the three-cover construction is generally optimal.

The checker proves the listed instance certificates and verifies the explicit family witness calculations. The parameter-wide statements follow from the proofs above. Theorems 1 and 2 cover their stated original-cost families, not arbitrary independently chosen x,y; the general local condition remains unresolved. They are not derived from a claim that no counterexample was found in finite tests.
