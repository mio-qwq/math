# Exact patterns and phase-circle construction at all half-orders

This companion to [paper.md](paper.md) treats every integer m>=2. It sharpens the earlier necessary-pattern trichotomy: its binary quotient branch cannot occur. Retaining the product of the original row ratios gives an exact root/single-support dichotomy. Compatible rectangles then construct full phase circles, and every nonroot solution arises this way.

These are analytical proofs. The existing Lean files prove supporting scalar and block results; a complete Lean formalization of this matrix theorem is not claimed.

## 1. Statement and notation

Let H have order 2m, m>=2, and suppose every entrywise power H^{∘k}, 1<=k<=m-1, is complex Hadamard. Dephase to

\[
 K_{ij}=\frac{H_{ij}H_{00}}{H_{i0}H_{0j}},\qquad L=K^{\circ m}.
 \tag{A1}
\]

The initial row and column are all ones. Dephasing preserves every required power orthogonality. Write J_s for the all-ones matrix of order s, and mu_m for the mth roots of unity.

**Theorem A (exact pattern dichotomy).** After row and column permutations placing the initial indices in the first groups, exactly one of these alternatives holds:

1. **Root pattern:** L=J_{2m}. Then K is cyclic generalized Hadamard over mu_m with multiplicity two: every ratio of distinct rows contains each root exactly twice.
2. **Single-support pattern:** for a unit number x!=1,
   \[
   L=\begin{pmatrix}J_m&J_m\\J_m&xJ_m\end{pmatrix}.
   \tag{A2}
   \]
   This forces m even. In the corresponding partition K=[A B; C D], each block has rank m/2 and all its nonzero singular values are sqrt(2m).

For odd m only the root pattern is possible. The binary quotient branch of the previous necessary classification is empty under the full hypotheses. We do not assert existence at every m, or that every root matrix admits a nonconstant phase deformation.

## 2. Two polygons and their product

Lemma 2 of [paper.md](paper.md) applies without a parity assumption. If unit entries v_1,...,v_{2m} have vanishing power sums for 1<=k<=m-1, their root polynomial is

\[
 \prod_j(z-v_j)=(z^m-a)(z^m-b),\qquad |a|=|b|=1.
 \tag{A3}
\]

Their multiset is two rotated regular m-gons. Their mth powers either coincide or take two distinct values a,b, each repeated m times.

**Lemma B (product refinement).** Under (A3),

\[
 \prod_jv_j=ab.
 \tag{A4}
\]

If their mth powers take the values 1,-1, their actual multiset is exactly mu_{2m}, each root once, and its product is -1.

**Proof.** Degree 2m is even, so the root product equals the constant term ab. In the last case (A3) is exactly (z^m-1)(z^m+1)=z^{2m}-1, with simple roots. There is no extra rotated factor: the two sets are the roots of the two specified polynomials. QED.

Apply these statements to ratios of distinct K rows and columns. Column orthogonality holds because each required power is square Hadamard. Comparing with the initial row shows that each row of L is either all ones or has m ones and m copies of one x!=1. Its support has size m and excludes column zero. The analogous column alternative excludes row zero.

## 3. Common supports without parity

**Lemma C.** All nonconstant rows of L have one common support for every m>=2; the same holds for columns.

**Proof.** Suppose rows a,b have different supports S,U and non-one values x,y. Put r=|S intersect U|. Their supports avoid column zero and have size m, so 1<=r<=m-1. The ratio in L has the following values, all with positive multiplicities:

| Position class | Ratio | Multiplicity |
| --- | --- | ---: |
| Outside S union U | 1 | r |
| S but not U | x | m-r |
| U but not S | y^{-1} | m-r |
| S intersect U | xy^{-1} | r |

At most two distinct values are allowed by (A3). Since x,y^{-1} differ from one, this forces y^{-1}=x. Then x^2 is either one or x; x!=0,1 rules out the latter. Thus x=y=-1.

Compare each actual K row with the initial all-ones row. Its mth powers take 1,-1, so Lemma B gives

\[
 \prod_jK_{aj}=\prod_jK_{bj}=-1.
 \tag{A5}
\]

The mutual row ratio also has the distinct mth-power values 1,-1. Formula (A3) gives multiplicity m for each, and Lemma B gives

\[
 \prod_j(K_{aj}\overline{K_{bj}})=-1.
 \tag{A6}
\]

But its product is (prod_j K_{aj}) conjugate(prod_j K_{bj})=1 by (A5), a contradiction. Transposition proves the column assertion. QED.

The earlier intersection equation 2r=m alone did not exclude even m. The additional invariant is the product of the original entries. Rows with the same support, and the case with no nonconstant rows, are not excluded.

## 4. Pattern and block ranks

If L has no nonconstant row it is all ones, so K has entries in mu_m. For a distinct row pair let c_s count its ratio entries equal to zeta_m^s. The full power hypothesis makes every nontrivial finite Fourier coefficient of (c_0,...,c_{m-1}) zero, and the coefficient at zero is 2m. Fourier inversion gives c_s=2. Conversely, these difference counts imply all the required power orthogonalities, also for composite m.

Otherwise let R be the nonconstant rows and S their common support. Its size is m. A column in S has non-one entries exactly on R. The column alternative gives |R|=m and a common non-one value on those rows. Hence all nonconstant rows use one x!=1; all remaining entries are one. This proves (A2), with initial indices outside R,S.

Partition K=[A B; C D]. For a cross-group row ratio, its two distinct mth-power values separate the two regular m-gons by column group. Each half therefore has zero sum. The column argument gives

\[
 A^*B=0,\quad C^*D=0,\quad AC^*=0,\quad BD^*=0.
 \tag{A7}
\]

The diagonal Gram identities give

\[
 AA^*+BB^*=2mI_m,\qquad CC^*+DD^*=2mI_m.
 \tag{A8}
\]

Thus (VV*)^2=2mVV* for each of the four blocks V. The matrix P_V=VV*/(2m) is an orthogonal projection. Every block has m^2 unit entries, so

\[
 \operatorname{rank}(V)=\operatorname{tr}(P_V)
 =\frac{m^2}{2m}=\frac m2.
 \tag{A9}
\]

Its nonzero squared singular values are 2m, and its integer rank forces m even. This proves Theorem A. Its alternatives are disjoint because the first has no nonconstant rows in L and the second has m.

## 5. Exact phase-circle construction

Let G be a dephased cyclic generalized Hadamard matrix over mu_m with multiplicity two. Choose row and column subsets R,S of size m, avoiding the initial indices. Call the rectangle **compatible** when, for each a in R and b outside R,

\[
 \{G_{aj}\overline{G_{bj}}:j\in S\}
\]

contains each element of mu_m exactly once. The complementary columns then have the same property, since the full difference contains each root twice. For a unit phase alpha, define

\[
 G(\alpha)_{ij}=
 \begin{cases}
 \alpha G_{ij},&i\in R,\ j\in S,\\
 G_{ij},&\text{otherwise}.
 \end{cases}
 \tag{A10}
\]

**Theorem D (construction and exhaustiveness).** Every G(alpha) is dephased and has all powers 1,...,m-1 complex Hadamard. Conversely, every nonroot K in Theorem A has this form for a root seed G and a compatible rectangle. Its non-one mth-power phase is x=alpha^m.

**Construction proof.** Entries remain unit and the initial row and column are unaffected. For two rows both inside R the common alpha^k cancels in their ratios on S; two outside R are unchanged. For a cross-group pair the kth-power sum vanishes separately on S and its complement, since each contains every root once and

\[
 \sum_{z\in\mu_m}z^k=0\qquad(1\le k<m).
\]

Multiplying either restricted zero sum by alpha^{+/-k} preserves orthogonality. Row norms remain 2m.

**Exhaustiveness proof.** In the nonroot pattern K=[A B; C D], choose a unit alpha with alpha^m=x and set

\[
 G=\begin{pmatrix}A&B\\C&\alpha^{-1}D\end{pmatrix}.
 \tag{A11}
\]

All its entries lie in mu_m. For each 1<=k<m, the original cross-group ratio separates its two regular m-gons by the column groups. Each restricted kth-power sum is zero. Writing V_k=V^{∘k}, this gives

\[
 A_kC_k^*=0,\qquad B_kD_k^*=0.
 \tag{A12}
\]

Replacing D_k by alpha^{-k}D_k leaves the diagonal Gram blocks unchanged and the off-diagonal blocks zero. Thus G has all required power orthogonalities and is cyclic generalized Hadamard by Fourier inversion.

Each cross-group ratio in G restricts to m distinct entries in mu_m on either column group: removing the phase leaves one full regular polygon. Hence each restriction contains every root once, proving compatibility. Formula (A10) recovers K, and its mth power equals x on the rectangle and one elsewhere. QED.

Every nonroot solution therefore belongs to an entire exact phase circle through root solutions. This constructs all admissible phases once a compatible root seed is supplied; it does not assert that such seeds exist at new parameter orders.

## 6. Finiteness and a boundary family

For fixed m there are finitely many root exponent matrices and candidate rectangles. The dephased solution set is therefore a finite union of root points and compatible phase circles. Some or all may be absent. For odd m any compatible rectangle would produce alpha^m!=1, contradicting (A9); the dephased solution set is finite at every odd half-order.

At m=2 the real Hadamard seed

\[
 G=\begin{pmatrix}
 1&1&1&1\\
 1&-1&1&-1\\
 1&1&-1&-1\\
 1&-1&-1&1
 \end{pmatrix}
\]

has compatible subsets given by the last two rows and columns. It gives the classical order-four family

\[
 G(\alpha)=\begin{pmatrix}
 1&1&1&1\\
 1&-1&1&-1\\
 1&1&-\alpha&-\alpha\\
 1&-1&-\alpha&\alpha
 \end{pmatrix},\qquad |\alpha|=1.
\]

Its square has the lower-right 2x2 block equal to alpha^2, with all other entries one. This realizes the nonroot branch. The family itself is classical.

For even m>2, the remaining realization question is which root seeds admit compatible balanced rectangles. No existence claim at every such m is made. This does not establish order-eight S-Hadamard nonexistence: that problem requires only powers 1,2, while the present m=4 hypotheses also require power 3.

## 7. Attribution and comparison boundary

Lemma C applies the classical cyclic-even complete-mapping obstruction. Two rows enumerating mu_{2m} whose quotient also enumerates it would yield permutations with a permutation difference map on an even cyclic group. The product of all group elements is the nontrivial involution, contradicting the product identity. See Hall and Paige, *Complete mappings of finite groups*, Pacific J. Math. 5 (1955), 541-549 ([original publisher PDF](https://msp.org/pjm/1955/5-4/pjm-v5-n4-p07-s.pdf)). The elementary abelian product argument is also stated in Eberhard, Manners and Mrazovic, *An asymptotic for the Hall-Paige conjecture* ([original preprint](https://arxiv.org/abs/2003.01798)). No deep converse is used here.

The source attribution in Section 7 of [paper.md](paper.md) continues to apply. A full comparison with Craigen and Woodford's *Power Hadamard matrices* and existing complex Hadamard block deformation results remains pending. We assert the proved dichotomy and exhaustive construction under this precise power range, without a historical first-proof or priority claim.
