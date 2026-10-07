# Odd half-order power Hadamard rigidity

## Abstract

Let `m >= 3` be odd. We prove that every complex matrix of order `2m` whose first `m-1` entrywise powers are complex Hadamard is equivalent, by row and column phases, to a generalized Hadamard matrix over the cyclic group of order `m`, with multiplicity two. In particular, all dephased entries are `m`th roots of unity. A self-inversive polynomial reduces every row and column ratio to two regular `m`-gons. An intersection argument makes all nonconstant supports of the `m`th power coincide. The remaining block alternative forces an orthogonal projection to have trace `m/2`, which contradicts oddness. For odd prime `m`, the condition is equivalent to phase equivalence to a Butson matrix of order `2m` and level `m`. The parity hypothesis is necessary: the order-four Fourier matrix supplies a counterexample when `m=2`.

## 1. Definitions and statement

All matrices in this note have complex entries. The conjugate transpose of `H` is denoted `H*`. A complex Hadamard matrix of order `n` is an `n x n` matrix satisfying

\[
 |H_{ij}|=1,\qquad HH^*=nI_n.
\]

Such a square matrix also satisfies `H*H=nI_n`: its first identity makes it invertible, with inverse `H*/n`.

Write `H^{∘k}` for the entrywise `k`th power, so `(H^{∘k})_{ij}=H_{ij}^k`. This differs from an ordinary matrix power. Let

\[
 \mu_m=\{z\in\mathbb C:z^m=1\},\qquad
 \zeta_m=\exp(2\pi i/m).
\]

The dephased matrix of a unimodular matrix `H`, using row and column index zero, is

\[
 K_{ij}=\frac{H_{ij}H_{00}}{H_{i0}H_{0j}}.
 \tag{1}
\]

Every denominator is nonzero, and the initial row and column of `K` are all ones. Formula (1) multiplies rows and columns by unit complex numbers. For each integer `k`, its entrywise `k`th power multiplies the corresponding rows and columns of `H^{∘k}` by unit numbers. Consequently dephasing preserves the Hadamard property of every entrywise power.

A dephased **cyclic generalized Hadamard matrix of multiplicity two** means a `2m x 2m` matrix `K` with entries in `mu_m` such that, for every two distinct rows `a,b`, the multiset

\[
 \{K_{aj}\overline{K_{bj}}:0\le j<2m\}
\]

contains each element of `mu_m` exactly twice. Equivalently, writing `K_{ij}=zeta_m^{E_{ij}}`, each difference of distinct exponent rows in `Z/mZ` contains each residue twice. This definition specifies the cyclic group, rather than a possibly different group of order `m`.

**Theorem 1 (rigidity and exact characterization).** Let `m >= 3` be an odd integer, and let `H` be a `2m x 2m` complex matrix. The following conditions are equivalent:

1. `H^{∘k}` is complex Hadamard for every integer `1 <= k <= m-1`.
2. `H` has unimodular entries, and its dephased matrix (1) is a cyclic generalized Hadamard matrix of multiplicity two.

In particular, condition 1 implies `K_{ij}^m=1` for all `i,j`.

The exponent range in condition 1 is a sufficient hypothesis. We do not assert that it is a minimal range. The theorem does not assert existence of such matrices at every odd `m`.

## 2. Two regular polygons from vanishing moments

**Lemma 2.** Let `m >= 2`, and let `v_1,...,v_{2m}` have modulus one. Suppose

\[
 \sum_{j=1}^{2m}v_j^k=0\qquad(1\le k\le m-1).
 \tag{2}
\]

Then their multiset is the union, with multiplicity, of two rotated regular `m`-gons. In particular the multiset of their `m`th powers is either a single value repeated `2m` times, or two distinct values repeated `m` times each.

**Proof.** Write `p_k=sum_j v_j^k`, and let `e_k` be the elementary symmetric functions of the `2m` entries, with `e_0=1`. Newton's identities read

\[
 k e_k=\sum_{r=1}^k(-1)^{r-1}e_{k-r}p_r.
\]

For `1 <= k <= m-1`, every `p_r` on the right vanishes by (2). Therefore `e_k=0` for every such `k`. Because `1/v_j=conj(v_j)`, complementing a subset in the elementary symmetric sum gives

\[
 e_{2m-k}=e_{2m}\overline{e_k}\qquad(0\le k\le 2m).
 \tag{3}
\]

For completeness, the product associated to the complement of a `k`-element subset `S` equals

\[
 \prod_{j\notin S}v_j
 =\left(\prod_{j=1}^{2m}v_j\right)
   \overline{\prod_{j\in S}v_j},
\]

and summing over `S` proves (3). Thus `e_{m+1},...,e_{2m-1}` vanish as well. The monic polynomial with these entries as roots is

\[
 \prod_{j=1}^{2m}(z-v_j)
 =z^{2m}+(-1)^m e_m z^m+e_{2m}
 =(z^m-a)(z^m-b).
 \tag{4}
\]

Here `a,b` are the roots, with multiplicity, of a quadratic polynomial. The constant `e_{2m}` is nonzero. Each factor in (4) has all its roots among the unimodular `v_j`, so `|a|=|b|=1`. Each factor has `m` distinct roots because `a,b` are nonzero. Its roots are one rotated regular `m`-gon. If `a=b`, that polygon occurs twice. If `a != b`, the two factors have disjoint roots and contribute `m` entries each. Raising the roots to the `m`th power proves the final statement. QED.

Assume condition 1 of Theorem 1 and dephase to `K`. For every two distinct rows `a,b`, put `v_j=K_{aj}conj(K_{bj})`. Orthogonality of the corresponding rows of `K^{∘k}` gives (2). The same reasoning applies to two distinct columns, since every `K^{∘k}` has orthogonal columns too. We may therefore apply Lemma 2 to both row ratios and column ratios.

## 3. Coincidence of supports

Set `L=K^{∘m}`. Since the initial row and column of `K` are ones, so are those of `L`. By applying Lemma 2 to a noninitial row and the initial row, each row of `L` is either all ones or consists of exactly `m` ones and `m` copies of one value `x != 1`. In the latter case call the `m` positions occupied by `x` its **support**. A support never contains column zero. The same alternative holds for columns, with supports excluding row zero.

**Lemma 3.** If `m` is odd, any two nonconstant rows of `L` have the same support. The same holds for nonconstant columns.

**Proof.** Let two nonconstant rows have supports `S,U` and non-one values `x,y`. Suppose `S != U`, and let `t=|S intersect U|`. Both supports have size `m` and lie in the `2m-1` noninitial column positions, so

\[
 1\le t\le m-1.
\]

The ratio of the two rows of `L` takes the following values with the indicated multiplicities:

| Position class | Ratio | Multiplicity |
| --- | --- | ---: |
| Outside `S union U` | `1` | `t` |
| `S` but not `U` | `x` | `m-t` |
| `U` but not `S` | `y^{-1}` | `m-t` |
| `S intersect U` | `xy^{-1}` | `t` |

The first multiplicity is `2m-|S union U|=t`. Every listed multiplicity is positive. This ratio is also the `m`th power of the ratio of two distinct rows of `K`, so Lemma 2 says it has at most two distinct values.

Because `x != 1` and `y^{-1} != 1`, the values `1,x,y^{-1}` can occupy at most two classes only if `y^{-1}=x`. The fourth value is then `x^2`; it must be `1` or `x`. Since `x` is nonzero and is not one, `x^2=x` is impossible, leaving `x^2=1`. Hence `x=y=-1`.

There are now exactly two values, `1` and `-1`, with multiplicities `2t` and `2(m-t)`. Lemma 2 requires each multiplicity to be `m`. This is impossible because `m` is odd. The supposition `S != U` was false. Applying the identical reasoning to column ratios proves the column statement. QED.

## 4. The block alternative

Suppose `L` is not all ones. Let `R` be the set of nonconstant rows, which is nonempty. By Lemma 3 all such rows have a common support `S`, with `|S|=m`.

For a column `j in S`, every row in `R` has a non-one entry there and every row outside `R` has a one. Thus this column is nonconstant. The column alternative following Lemma 2 says that it has exactly `m` non-one entries. It follows that `|R|=m`. It also says that all those non-one entries have one common value. For any fixed `j in S`, these entries are exactly the non-one values of the rows in `R`, so those row values agree with a single `x != 1`.

Every column outside `S` is all ones, because all nonconstant rows have support `S` and the other rows are all ones. After arranging the constant rows first and the constant columns first, both classes have size `m` and

\[
 K=\begin{pmatrix}A&B\\C&D\end{pmatrix},\qquad
 L=\begin{pmatrix}J_m&J_m\\J_m&xJ_m\end{pmatrix},
 \tag{5}
\]

where `A,B,C,D` are `m x m` and `J_m` is the all-ones matrix. All their entries have modulus one. This derivation accounts for both the row and column partition, including the size and common phase of the nonconstant block.

Take a column of `K` from the left group and a column from its right group. The `m`th powers of their entrywise ratio are one on the top `m` rows, and `x` or `x^{-1}` on the bottom `m` rows, depending on the ratio orientation. These two values are distinct. Lemma 2 therefore separates its two regular `m`-gons exactly into the top and bottom halves. The sum of either half is zero, because for `m>=2`

\[
 \sum_{r=0}^{m-1}\zeta_m^r=0.
\]

In particular, the inner product restricted to the top half is zero for every such pair of columns. This is the matrix identity

\[
 A^*B=0.
 \tag{6}
\]

The top-left block of `KK*=2m I_{2m}` gives

\[
 AA^*+BB^*=2mI_m.
 \tag{7}
\]

Multiplying (7) on the left by `AA*` and using (6) gives

\[
 (AA^*)^2+AA^*BB^*
 =(AA^*)^2+A(A^*B)B^*
 =(AA^*)^2=2mAA^*.
\]

Consequently

\[
 P=\frac{AA^*}{2m}
\]

is Hermitian and satisfies `P^2=P`. Its eigenvalues are zero or one, so its trace equals its rank, an integer. But the `m^2` entries of `A` have modulus one, and hence

\[
 \operatorname{tr}P
 =\frac{1}{2m}\operatorname{tr}(AA^*)
 =\frac{1}{2m}\sum_{i,j=1}^m|A_{ij}|^2
 =\frac{m}{2}.
 \tag{8}
\]

This is not an integer when `m` is odd, a contradiction. Therefore `L` is all ones, proving `K_{ij}^m=1` for all entries.

## 5. Exact cyclic-group characterization

Continue under condition 1. By Section 4, every entry of `K` belongs to `mu_m`. For two distinct rows let `c_r` count how often `zeta_m^r` occurs in their ratio, for `0<=r<m`. The assumed power orthogonalities give

\[
 \sum_{r=0}^{m-1}c_r\zeta_m^{kr}=0
 \quad(1\le k\le m-1),\qquad
 \sum_{r=0}^{m-1}c_r=2m.
\]

For each fixed `s`, multiply the `k`th equation by `zeta_m^{-ks}` and sum for `0<=k<m`, including the sum `2m` at `k=0`. The finite geometric series is `m` when `r=s` and zero otherwise. Thus `m c_s=2m` and `c_s=2`. This proves condition 2.

Conversely, condition 2 says that every ratio of distinct rows of `K` contains every element of `mu_m` twice. For `1<=k<m` its `k`th power sum is

\[
 2\sum_{r=0}^{m-1}\zeta_m^{kr}=0.
\]

Its row norms are `2m`, because its entries have modulus one. Hence `K^{∘k}(K^{∘k})*=2m I`, and every such power is Hadamard. Undoing dephasing preserves this property, so condition 1 holds for `H`. Theorem 1 is proved.

The characterization also holds for column differences: either repeat the counting argument with columns or use the column orthogonality of every power.

**Corollary 4 (intrinsic phase invariant).** Under the hypotheses of Theorem 1, every rectangular phase ratio is an `m`th root of unity:

\[
 \left(\frac{H_{ij}H_{ab}}{H_{ib}H_{aj}}\right)^m=1
 \qquad\text{for all }i,j,a,b.
\]

**Proof.** Row and column phases cancel in this expression. In the dephased matrix all four entries are `m`th roots, so their ratio is too. QED.

**Corollary 5 (odd-prime equivalence).** Let `p` be an odd prime, and let `H` be a complex Hadamard matrix of order `2p`. Then its entrywise powers `1,...,p-1` are all Hadamard if and only if it is phase equivalent to a complex Hadamard matrix with entries in `mu_p`.

**Proof.** Necessity follows from Theorem 1. For sufficiency, dephase to a Hadamard matrix `K` with entries in `mu_p`. For distinct rows let `c_r` count the `p`th roots in their ratio, and put `f(X)=sum_{r=0}^{p-1} c_r X^r`. Orthogonality gives `f(zeta_p)=0`. The minimal polynomial of `zeta_p` over the rationals is

\[
 \Phi_p(X)=1+X+\cdots+X^{p-1}.
\]

Since `degree(f)<=p-1`, the polynomial `f` is a rational scalar multiple of `Phi_p`. Its coefficient sum is `2p`, so that scalar is two. Every root therefore occurs twice. The reverse implication of Theorem 1 now applies. This also explains the usual equivalent argument by the Galois automorphisms `zeta_p -> zeta_p^k`, `1<=k<p`. QED.

For composite odd `m`, we do not replace the full power hypothesis by the single Butson condition: that converse has not been proved here.

## 6. Boundary examples and exact checks

Oddness is essential to Theorem 1 as stated. Put `m=2` and take the order-four Fourier matrix

\[
 (F_4)_{ij}=i^{ij},\qquad 0\le i,j<4.
\]

It is dephased. The only required exponent would be `k=1`, and `F_4` is Hadamard by the geometric-series identity. Its `(1,1)` entry is `i`, whose square is `-1`, so the asserted conclusion `K^{∘2}=J_4` fails. Moreover, no choice of row and column phases can turn it into a matrix with entries in `mu_2`, since its rectangular ratio on rows and columns `0,1` is `i`, which is invariant under those phases.

The theorem begins at `m=3`; no assertion is made for `m=1`. The proof of the polygon half-sum uses `m>=2`, and the power range would be empty at `m=1`.

At `m=3`, a positive example is the exponent matrix

\[
 E=\begin{pmatrix}
 0&0&0&0&0&0\\
 0&0&1&2&2&1\\
 0&1&0&1&2&2\\
 0&2&1&0&1&2\\
 0&2&2&1&0&1\\
 0&1&2&2&1&0
 \end{pmatrix},\qquad K_{ij}=\zeta_3^{E_{ij}}.
\]

Each difference of distinct rows contains residues `0,1,2` exactly twice; hence both `K` and `K^{∘2}` are Hadamard. This is the familiar order-six cubic matrix, up to permutations. The order-six Fourier matrix `F_6` is a different useful boundary example: it is Hadamard but its entrywise square has repeated rows, so it fails the required `k=2` hypothesis. Its `(1,1)` entry is not a cube root. Thus, at `m=3`, retaining only `k=1` is insufficient.

The companion script `code/check_examples.py` verifies these assertions exactly. For a matrix whose entries are powers of a specified root of unity, it represents inner products by integer polynomials modulo the relevant cyclotomic polynomial. Polynomial division and remainder calculation use integer arithmetic only. It also directly checks the uniform difference counts for the cubic matrix.

These are finite checks of the examples, not a computer-assisted proof of Theorem 1. The general theorem uses the complete analytical argument in Sections 2–5 and no computation. A complete Lean formalization of the theorem is not claimed in this note.

## 7. Relation to the source argument and prior work

The starting point is the order-six cubic-alternative proof in OpenAI's *Exact Fourier certificates for complex Hadamard matrices of order six*, specifically:

- Repository commit: [`adc7f1241b42e322a6451854ab7e4b4c146bf78a`](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a).
- Actual proof source: [`build/sections/03-cubic.tex`](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/build/sections/03-cubic.tex).

That source treats order six and classifies the resulting cubic matrix. The present note extends its two-polygons and common-support ideas to every odd half-order. It replaces the order-six dimension argument by the projection calculation (6)–(8), which works at every odd `m`, and derives an exact cyclic-group characterization. The proof above is self-contained; it does not assume that source's theorem or its Fourier certificates.

Entrywise-square Hadamard matrices are studied as S-Hadamard matrices. See Jasleen Phangara, *S-Hadamard matrices*, Simon Fraser University master's thesis, 2026 ([primary thesis PDF](https://theses.lib.sfu.ca/file/thesis/etd24287-jasleen-phangara-mscthesisjasleenphan.pdf)). Power and generalized Hadamard matrices have an existing literature; see *Power Hadamard matrices*, Discrete Mathematics ([publisher record](https://www.sciencedirect.com/science/article/pii/S0012365X07004244)). These references identify related terminology and research areas. A complete comparison with prior general rigidity statements remains to be carried out, so no first-proof or novelty-priority assertion is made.
