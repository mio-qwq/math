# A streaming reversible-prefix baseline for arbitrary output bits

Date: 2026-10-11. Classification: application and verification of an established finite-state method with elementary prefix-product algebra. No original cryptanalytic technique, best-known attack improvement, or publication-level novelty is claimed.

This note proves the exact matrices, the applicability of reversible prefixes, and the arithmetic/space bounds for the local function. The implementation is `../experiments/streaming_prefix.py`. Earlier frozen proofs and programs are unchanged.

## 1. Model and provenance

Use the local three-add function and all-XOR output word from `../GENERAL_REDUCTION.md`, with `n>=1`, `0<=r,q<n`, and `0<=i<n`. The two allowed input distributions are independent uniform `a,b,c,d`, or a fixed first word `a=A` with independent uniform `b,c,d`.

After the proved middle-carry elimination, set

\[
j=(i-q)\bmod n,\qquad k=(i-r-q)\bmod n.
\]

The correlation is

\[
C_i=2^{-j}\left(M_0-
\sum_{\substack{0\le\ell<i\\h=(\ell-q)\bmod n<j}}2^hM_{h,\ell}\right).
\]

Each moment uses two state bits: the borrow `beta` of `S-B` in the uniform model, or of `S-A` in the fixed-word model; and the carry `gamma` of `S+Y`. Its sign includes `beta_i XOR beta_k XOR gamma_i`, optionally `B_h XOR Y_ell`.

The Literature Agent supplied the reversible-prefix construction as a fair same-target baseline after identifying the relevant existing finite-state theory. Niu, Beyne, Hu and Wang's **Cryptanalytic Properties of Mealy Machines** provides a general framework for signed state-transition products and constant-addend analyses. It was formally published in CRYPTO 2026, LNCS 16805, pages 374–405, first online 11 August 2026; ePrint 2026/1193 identifies its 27 July 2026 version as a minor revision of the CRYPTO publication. The project-specific prefix reconstruction is documented in `../literature/METHOD_COMPARISON.md`; this note does not claim that the authors published this exact ChaCha optimization.

Primary records: [publisher](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13), [ePrint](https://eprint.iacr.org/2026/1193). This implementing agent verified those records and read the project's mathematical reconstruction after its own implementation passed. The paper's full text was not successfully retrieved by this agent in this subcycle; the Literature Agent's full-text review remains separately attributed.

## 2. Constant kernels and exact invertibility

Order states as `00,01,10,11`, indexed by `2*beta+gamma`. Matrix rows are destination states and columns are source states.

In the uniform model, sum the eight bit triples `(s,b,y)`, with

\[
\beta'=[b+\beta>s],\qquad
\gamma'=\lfloor(s+y+\gamma)/2\rfloor.
\]

In a fixed-word position with `a_p=a_bit`, sum the four bit pairs `(s,y)` and use

\[
b=(s-a_{bit}-\beta)\bmod2,\quad
\beta'=[a_{bit}+\beta>s],\quad
\gamma'=\lfloor(s+y+\gamma)/2\rfloor.
\]

Direct enumeration gives

\[
P=\frac18\begin{pmatrix}
4&1&1&0\\2&5&1&2\\2&1&5&2\\0&1&1&4
\end{pmatrix},
\]

\[
P_0=\frac14\begin{pmatrix}
3&1&1&0\\1&3&1&2\\0&0&2&1\\0&0&0&1
\end{pmatrix},\qquad
P_1=\frac14\begin{pmatrix}
1&0&0&0\\1&2&0&0\\2&1&3&1\\0&1&1&3
\end{pmatrix}.
\]

For `P0`, the two diagonal blocks of its integer numerator have determinants 8 and 2. For `P1`, they have determinants 2 and 8. Thus both determinants are `16/4^4=1/16`.

For `P`, the antisymmetric vectors `(1,0,0,-1)` and `(0,1,-1,0)` are right eigenvectors of eigenvalue `1/2`. On the remaining symmetric subspace with basis `(1,0,0,1)` and `(0,1,1,0)`, the representing matrix is

\[
\begin{pmatrix}1/2&1/4\\1/2&3/4\end{pmatrix},
\]

whose determinant is `1/4`. Consequently

\[
\det P=\det P_0=\det P_1=1/16.
\]

All three kernels are invertible over the rationals. The implementation independently confirms these determinants by Gauss–Jordan elimination and the 24-term Leibniz formula, and checks both left and right inverse products.

Define `P^B`, `P^Y`, and `P^BY` by inserting signs `(-1)^b`, `(-1)^y`, and `(-1)^(b XOR y)` in the same truth-table sum. Only the unmasked matrices are inverted. No invertibility assertion is made for masked kernels.

## 3. Boundary phases and conjugated insertions

Before processing position `p`, insert

\[
D_p=\operatorname{diag}_{(\beta,\gamma)}
(-1)^{\beta(\mathbf1_{p=i}+\mathbf1_{p=k})+\gamma\mathbf1_{p=i}}.
\]

The exponent is modulo two; when `i=k`, the two borrow phases cancel. Set

\[
T_p=P_pD_p,\qquad K_p^X=P_p^XD_p,
\]

where `P_p=P` in the uniform case and `P_p=P_(A_p)` in the fixed-word case. Since `D_p^-1=D_p`,

\[
T_p^{-1}=D_pP_p^{-1},\qquad
T_p^{-1}K_p^X=D_pP_p^{-1}P_p^XD_p.
\]

There are only three kernel types and four diagonal phase types. The implementation precomputes this constant-size table once; it does not cache one table per input position.

Let

\[
G_0=I,\qquad G_t=T_{t-1}\cdots T_0,
\]

\[
H_p^X=G_p^{-1}T_p^{-1}K_p^XG_p.
\]

For the initial column `e0=(1,0,0,0)^T` and terminal row `f=(1,1,1,1)`,

\[
M_0=fG_ne0.
\]

If the low mask is at `u` and the high mask at `v>u`, direct cancellation of adjacent inverse products gives

\[
M_{two}=fG_nH_v^{high}H_u^{low}e0.
\]

For example, `G_v G_(u+1)^-1=T_(v-1)...T_(u+1)`, leaving exactly the original transition product with its two marked steps. At a shared position, the correct expression is

\[
M_{same}=fG_nH_u^{BY}e0.
\]

Multiplying separate `B` and `Y` insertions at the same position would not perform the same joint bit average. The `BY` kernel is required.

All terminal states are summed; no final carry or borrow is forced to zero.

## 4. The summation indices form one synchronized interval

The conditions `h<j` and `ell=(h+q) mod n<i` select exactly one of the following cases:

| Case | Pair count `L` | Low position and mask | High position and mask | Weight |
|---|---:|---|---|---|
| `i>=q` | `i-q` | `t`, mask `B` | `t+q`, mask `Y` | `2^t` |
| `i<q` | `i` | `t`, mask `Y` | `t+n-q`, mask `B` | `2^(n-q+t)` |

Here `0<=t<L`. In the first case `q=0` means equal positions and uses `BY`.

To prove the first row, `j=i-q`, so `h<j` implies `h+q<i<n`; there is no wrap. For the second row, write `d=n-q`, so `j=d+i`. If `h<d`, then `ell=h+q>=q>i` and the term is excluded. If `h>=d`, then `ell=h-d`, and the retained positions are exactly `h=d,...,d+i-1`.

Thus both indices advance by one per summand. Empty intervals, including `i=0` and `j=0`, contribute no masked terms.

## 5. Streaming algorithm

First compute the row `fG_n` by scanning positions downwards:

```
row = f
for p = n-1 down to 0:
    row = row * T_p
```

This avoids storing `G_n` or its intermediate products. Let `d` be the position distance in section 4. Initialize the low prefix pair as `(I,I)`. Initialize the high pair at `G_d,G_d^-1` by one forward scan of length `d`.

For each retained pair, build its conjugated insertion(s), evaluate the constant-size scalar product from section 3, and add the weighted moment to one running rational accumulator. Then advance both prefix pairs:

\[
G_{p+1}=T_pG_p,\qquad
G_{p+1}^{-1}=G_p^{-1}T_p^{-1}.
\]

When `d=0`, maintain just the shared prefix pair and use its `BY` insertion. When `L=0`, return `2^-j M0` after the row pass.

At no point does the core evaluator store a list of the `n` prefixes. A constant number of matrices, rows, scalar accumulators, and loop counters is live.

## 6. Arithmetic count and auxiliary bits

For `d>0,L>0`, the implemented routine uses `2d+8L` dynamic `4x4` matrix products, plus `n+L` row–matrix products. This counts even the unnecessary-but-harmless advancement after the final pair. For `d=0`, it uses `4L` matrix products. The index bounds imply at most `8n` dynamic matrix products and at most `2n` row products. The test harness checks the `8n` bound for every evaluated correlation. Since dimensions are fixed, this is **O(n) exact rational arithmetic operations per output bit**. Computing all `n` output bits separately costs `O(n^2)` arithmetic operations.

The auxiliary bit bound requires controlling rational growth, not merely counting matrix objects. All entries are dyadic rationals. The constant `P` matrices have denominator at most `2^3`; their displayed inverses in the result file have denominator at most 2. Their column 1-norms satisfy

\[
\|P_pD_p\|_1\le1,\qquad
\|D_pP_p^{-1}\|_1\le10.
\]

These bounds follow directly from the three explicit matrices and their inverses. Therefore forward prefix entries have magnitude at most one and denominator dividing `2^(3p)`, while inverse-prefix entries have magnitude at most `10^p` and denominator dividing `2^p`. The constant insertion `T_p^-1 K_p^X` has bounded dyadic denominator and magnitude. A conjugation contains only a constant number of such prefixes, so its reduced numerator and denominator have `O(n)` bits. The final scalar products and weighted sum preserve that bound: dyadic denominators share a common power-of-two denominator of exponent `O(n)`, and summing at most `n` bounded-exponential numerators adds only `O(log n)` bits. Ordinary multiplication temporaries have the sum of two `O(n)` bit lengths, also `O(n)`.

A constant number of these matrices and rows thus occupies **O(n) auxiliary bits** in the usual live-storage model. The fixed input word already has `n` bits. Python object and allocator overhead, and the test harness's stored input/output records, are not evidence for or against this mathematical bound; the report records process RSS separately.

This arithmetic count is not linear bit time. The implementation uses normalized `Fraction` arithmetic and growing-integer multiplications. A generic bit bound must include integer multiplication and fraction-normalization cost, for example `O(n*(M(n)+G(n)))` for suitable multiplication and normalization bounds on `O(n)`-bit operands. A dyadic representation can avoid generic gcd normalization and gives the familiar `O(n*M(n))` bound; with schoolbook multiplication, that is `O(n^3)`. The original repeated-moment evaluator also has a cubic elementary bit-operation upper bound because it uses mostly additions and shifts. No smaller elementary bit-time exponent or empirical speedup over an optimized predecessor is claimed here.

## 7. Verification, source boundary, and conclusion

The implementation regenerated all kernels from their bit truth tables. It did not import or inspect the root `tooling/` source or the verifier's source. For this subcycle the agent was explicitly authorized to read only the frozen verification data, which was used to check:

- 216 independent original-word uniform correlations;
- 1,274 independent original-word fixed-first-word correlations;
- 160 independently computed standard-32 correlations.

All 1,650 values matched exactly, including zero rotations, one-bit words, shared mask positions, coincident carry phases, empty moment sums, and the four standard constants. The largest intermediate numerator and denominator observed by the instrumented arithmetic were each 79 bits. That finite observation is consistent with, and does not replace, the general bit-length proof.

The implementation had passed all tests before the agent read `../literature/METHOD_COMPARISON.md`. It was nevertheless developed from the prefix construction supplied by the root and Literature Agent, so it is a verification and implementation of that proposed baseline rather than a blind discovery of it.

The run took approximately 1.481 seconds in its timed harness, including 1.050 seconds for the 160 standard-width values. These workloads differ from earlier root-agent timing batches, so those elapsed times are not compared as a speedup. Exact commands, source/input hashes, timing scope, and environment are recorded in `../experiments/STREAMING_PREFIX_RUN.md`.

The useful outcome is a fairer same-target computational baseline and an independently rebuilt implementation matching existing exact data. It does not establish historical originality for the sparse rotation elimination, closed expressions, or sign classification, and does not improve an attack on the full cipher.
