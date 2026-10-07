# Necessary patterns for power Hadamard matrices at all half-orders

This companion to [paper.md](paper.md) treats every integer `m>=2`, including even half-orders. It classifies the possible shapes of the dephased `m`th entrywise power. The statements are necessary conditions; we do not assert that every listed pattern or every even value of `m` is realized by a matrix satisfying all the required power orthogonalities.

## 1. Statement

Let `H` be a complex matrix of order `n=2m`, `m>=2`, such that `H^{∘k}` is complex Hadamard for every integer `1<=k<=m-1`. Dephase it as in (1) of the main paper to obtain `K`, and set `L=K^{∘m}`. Let `J_t` denote the all-ones matrix of order `t`.

**Theorem A (necessary-pattern trichotomy).** After permutations of rows and columns, exactly one of the following descriptions applies:

1. **Root pattern:** `L=J_{2m}`. Consequently every entry of `K` is an `m`th root of unity.
2. **Single-support pattern:** for a unit complex number `x!=1`,
   \[
   L=\begin{pmatrix}J_m&J_m\\J_m&xJ_m\end{pmatrix}.
   \tag{A1}
   \]
   This case forces `m` to be even. If `K=[A B; C D]` is partitioned into the corresponding four `m x m` blocks, each block has rank `m/2`, and all its nonzero singular values are `sqrt(2m)`.
3. **Binary quotient pattern:** there are integers `q>=4` and `t>=1` with `q t=2m`, and a real sign Hadamard matrix `Q` of order `q`, such that
   \[
   L=Q\otimes J_t.
   \tag{A2}
   \]
   In this case `4` divides `q`, so `m` is even. Every entry of `K` is a `2m`th root of unity.

The three descriptions are mutually exclusive when case 2 is understood as having only one support among nonconstant rows, and case 3 as having at least two such supports. In (A2), the quotient `Q` is dephased if the initial constant row and column are placed first.

This strengthens the odd-half-order result: for odd `m`, cases 2 and 3 are impossible, leaving case 1.

## 2. The ratio alternative

Lemma 2 of the main paper applies for every `m>=2`, with no parity assumption. For any two distinct rows of `K`, the first `m-1` power sums of their entrywise ratio vanish. Newton's identities and the unimodularity identity

\[
 e_{2m-r}=e_{2m}\overline{e_r}
\]

make its root polynomial a quadratic in `z^m`. Thus the ratio is a union of two rotated regular `m`-gons. Its `m`th power has either one value repeated `2m` times or two distinct values repeated `m` times each. The same holds for column ratios, since every power has orthogonal columns as well.

Because `K` is dephased, every row of `L` is either all ones or has `m` ones and `m` copies of a single value `x!=1`. The support of a nonconstant row is the set of positions carrying that value. It has size `m` and excludes column zero. Columns obey the corresponding alternative and exclude row zero from their support.

If all rows of `L` are constant, they are all ones, giving case 1. We henceforth assume there is a nonconstant row.

## 3. Two different supports force signs

Let two nonconstant rows have supports `S,U` and non-one values `x,y`, with `S!=U`. Put `r=|S intersect U|`. Since both supports lie in `2m-1` positions and have size `m`,

\[
 1\le r\le m-1.
\]

Their ratio in `L` has values and multiplicities

\[
\begin{array}{c|rrrr}
\text{value}&1&x&y^{-1}&xy^{-1}\\
\text{multiplicity}&r&m-r&m-r&r.
\end{array}
\tag{A3}
\]

All four multiplicities are positive. The ratio alternative allows at most two distinct values. Because `x,y^{-1}` are different from one, it forces `y^{-1}=x`, followed by `x^2=1`. Hence `x=y=-1`. The two final multiplicities are `2r` and `2(m-r)`, so the ratio alternative also gives `r=m/2` and makes `m` even.

If there exist two different supports, compare any third nonconstant row with one of these two whose support differs from its own. The same argument forces its non-one value to be `-1`. Thus **every entry of `L` is a sign** in this situation.

Any two distinct row vectors of this sign matrix have ratio values `1,-1`. The ratio alternative forces each value to occur `m` times, so the two rows are orthogonal. Rows that are not distinct are identical. The same reasoning for columns shows that two distinct column vectors are orthogonal, while nondistinct columns are identical.

## 4. Compression of the sign pattern is uniform

Suppose there are at least two different nonconstant supports. Partition the rows of `L` into classes of identical row vectors, and its columns into classes of identical column vectors. Let there be `r` row classes and `c` column classes.

Distinct row representatives are orthogonal and nonzero. They therefore form a basis for the row space of `L`, making `rank(L)=r`. Likewise distinct column representatives form a basis for the column space, so `rank(L)=c`. Consequently `r=c=q`.

Let `Q` be the `q x q` matrix of entries at the class representatives. Write `rho_a` for the positive integer size of row class `a`, and `kappa_b` for the positive integer size of column class `b`. Put

\[
 D_\rho=\operatorname{diag}(\rho_1,\ldots,\rho_q),\qquad
 D_\kappa=\operatorname{diag}(\kappa_1,\ldots,\kappa_q).
\]

The row and column orthogonalities of the representatives are exactly

\[
 QD_\kappa Q^{\mathsf T}=nI_q,\qquad
 Q^{\mathsf T}D_\rho Q=nI_q.
 \tag{A4}
\]

In particular `Q` is invertible. The first identity gives

\[
 Q^{-1}=\frac{D_\kappa Q^{\mathsf T}}{n},
\]

and the second gives

\[
 Q^{-1}=\frac{Q^{\mathsf T}D_\rho}{n}.
\]

Comparing entry `(b,a)` in these formulas yields

\[
 \kappa_b Q_{ab}=\rho_a Q_{ab}.
\]

Every `Q_{ab}` is `1` or `-1` and is nonzero. Hence all the row-class and column-class sizes are equal to one positive integer `t`. Summing their sizes gives `q t=n`. Substituting in (A4) proves `QQ^{T}=q I_q`: the quotient is a real sign Hadamard matrix. Arranging the classes now gives `L=Q tensor J_t`.

There are at least three row classes: the all-ones class and the two different nonconstant-support classes. Thus `q>=3`. We recall the short sign argument that then forces `4|q`. Normalize a sign Hadamard matrix so its first row is all ones. Each other row contains `q/2` plus signs and `q/2` minus signs. Take two such rows. If the four possible sign pairs occur `a,b,c,d` times, orthogonality to the first row gives

\[
 a+b=a+c=q/2,
\]

so `b=c` and `a=d`. Orthogonality between the two rows gives `a+d=b+c`, hence `a=b=c=d` and `q=4a`. In particular `q>=4`. Since `q|2m`, it also follows that `m` is even.

Finally `L` has only sign entries, so `K_{ij}^{2m}=L_{ij}^2=1`. This proves all assertions of case 3.

## 5. The single-support pattern and block ranks

It remains to assume that every nonconstant row has the same support `S`. By the ratio alternative `|S|=m`. Let `R` be the set of nonconstant rows.

For any `j in S`, the non-one entries of column `j` are exactly those in `R`. The column alternative says that this column has `m` non-one entries with one common value. Therefore `|R|=m`, and all nonconstant rows have the same non-one value `x!=1`. Every column outside `S` is all ones. This gives (A1) after arranging constant rows and columns first.

Partition `K=[A B; C D]` correspondingly. For a left-group column and a right-group column, the `m`th powers of their ratio have one value on the top `m` rows and a distinct value on the bottom `m` rows. Its two regular `m`-gons are therefore separated by these row groups; the sum of either group is zero. Similarly, opposite row groups separate the two regular `m`-gons by column group. These statements give

\[
 A^*B=0,\quad C^*D=0,\quad AC^*=0,\quad BD^*=0.
 \tag{A5}
\]

The diagonal blocks of the Hadamard identity give

\[
 AA^*+BB^*=2mI_m,\qquad
 CC^*+DD^*=2mI_m.
 \tag{A6}
\]

Using `A*B=0` in the first identity, and `C*D=0` in the second, shows that for every block `V in {A,B,C,D}`,

\[
 (VV^*)^2=2mVV^*.
\]

Thus `P_V=VV*/(2m)` is an orthogonal projection. Every block has `m^2` unit-modulus entries, giving

\[
 \operatorname{rank}(V)=\operatorname{tr}(P_V)
 =\frac{m^2}{2m}=\frac m2.
\]

Its nonzero squared singular values are `2m`, as the projection identity shows. The rank is an integer, so `m` is even. This proves case 2 and completes Theorem A.

The case distinction used in the proof is exhaustive: no nonconstant rows, one support among nonconstant rows, or at least two supports. It also proves the asserted mutual exclusivity. In the binary quotient case there are at least four distinct row vectors; in the single-support case there are exactly two, so row and column permutations cannot identify the two cases.

## 6. One phase or finitely many roots

There is a useful immediate consequence. In the single-support case choose any `alpha` with `alpha^m=x`. Then all entries of the three blocks `A,B,C` belong to `mu_m`, while every entry of `D` belongs to `alpha mu_m`. Thus the only continuous phase allowed by this necessary pattern occurs in one `m x m` block. In the other two cases the entire dephased matrix has entries in the finite root set `mu_{2m}` (and case 1 uses the smaller set `mu_m`).

This describes the phase restriction only. It neither solves all orthogonality equations for the exponent data nor establishes existence of the single-support pattern for each even `m`. The order-four Fourier matrix in Section 6 of the main paper realizes case 2 at `m=2`, with `x=-1`; no further even-half-order existence claim is made here.

The argument is analytical and exact. It adds no reliance on numerical searches or on a claim of complete Lean formalization. The provenance and priority qualifications in Section 7 of the main paper continue to apply.
