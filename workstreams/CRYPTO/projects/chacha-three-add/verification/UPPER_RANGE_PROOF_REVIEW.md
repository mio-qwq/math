# Independent review of the overlapping-carry closed form

Date: 2026-10-11. Reviewed manuscript: `../proofs/overlap_bit_closed_form.md`.

Reviewed SHA-256: `679893a5d746d0180215031b0b7c0ceed3d926d74f0d5969f5d7928cd8ba0fca`.

Verdict: **the stated closed form, its domain, strict sign, and recurrence passed mathematical review. No correction to the mathematical statement is requested.**

## 1. Independence and provenance

The verifier first received only the candidate equation and its proposed domain. Before reading this manuscript, it compared the equation against its own previously implemented general four-state evaluator and its earlier original-word enumeration. Those results are preserved in `upper_range_independent_run.json`; they were not replaced by post-review data.

The manuscript was subsequently read for mathematical cross-review. The new `upper_moment_review_checks.py` checks the disclosed intermediate moment formulas with that earlier independent state evaluator. These checks are post-disclosure proof review, distinct from the preceding checks of the initial candidate. No discovery `experiments/`, `tooling/`, or corresponding implementation output was read or imported. The verifier has not inspected the root agent's independently generated numerical output. This is internal agent verification, not human peer review or formal proof-assistant verification.

## 2. Statement and exact domain

All four input words are independent uniform `n`-bit words. The operations, left rotations, and all-XOR linearization are those in `GENERAL_INDEPENDENT_PROOF.md`. Let

`r,q>=1`, `0<=k<=q`, `i=r+q+k<n`.

Here `k` is an **offset**, and `C_k=E[(-1)^bit_i(w XOR L)]`. Put

\[
\alpha=-\frac1{3\,2^r}+\frac4{3\,2^{3r+2q}},\qquad
\beta=-\frac1{7\,2^q}-\frac1{7\,2^{3r+q}},\qquad
\delta=\frac2{7\,2^{3r+q}}.
\]

The reviewed result is

\[
C_k=\alpha4^{-k}+\beta2^{-k}+\delta16^{-k}<0.
\]

The recurrence

\[
C_{k+3}=\frac{13}{16}C_{k+2}-\frac{11}{64}C_{k+1}+\frac1{128}C_k
\]

requires all four offsets to lie in the same valid range, equivalently

`k+3 <= min(q,n-r-q-1)`.

At standard rotations the word `w` is also exactly the first output word of a complete quarter round. All remaining quarter-round operations modify only the other three words; its completely XOR-linearized first output is also `L`. The result concerns this single-output-bit relation under the stated distribution. It supplies no optimality statement about masks, analysis of the joint output distribution, full-round attack, or ChaCha20 key recovery.

## 3. Middle-carry elimination and width independence

The general carry identity specializes to

`error_i = K1_i XOR K1_k XOR K2_(r+k) XOR K3_i`.

This matches the independent general proof. After the bijection to independent `S,B,Y,T`, eliminating `T` gives the affine bit expansion with masks `ell=0,...,r+k-1` and `p=ell+q`. The largest such `p` is `i-1`, so none wraps around the word. All remaining events and masks depend only on the low `i` bits. Truncating the three independent words to `N=2^i` therefore preserves their uniform independence and the exact expectation. This proves independence from the ambient word width once `n>i`.

The two threshold signs share `S`, and the proof conditions on `S` before multiplying their separate `B` and `Y` averages. This is legitimate conditional factorization; it does not assume independent carries.

## 4. Splitting at the lower carry

Let `K=2^k`, `H=2^(r+q)`, `N=KH`, and decompose

`S=KX+s`, `B=KZ+b`.

Set `a_s=(2s+2-K)/K` and `U_X=2X-H+1`. If `Z<X`, the product of the two borrow signs is the lower borrow sign; if `Z>X`, it is its negative. In the equal block `Z=X`, the two borrows coincide and their product is exactly `+1`.

Counting the `X` smaller and `H-X-1` larger blocks thus gives

\[
E_B[A\mid S]=\frac{1+U_Xa_s}{H}.
\]

This equal-block term cannot be replaced by a product of separately averaged borrows.

### Masks below the split

For `ell<k`, the equal block has zero masked average. The unequal blocks use

`E_b[(-1)^[b>s] chi_ell(b)] = 2H_ell(s+1)/K`.

The correct shifted argument is `s+1`, not `s`, because equality `b=s` belongs to the non-borrow side. Hence

\[
E_B[A\chi_\ell(B)\mid S]=\frac2N U_XH_\ell(s+1).
\]

### Masks at or above the split

For `ell>=k`, put `e=ell-k`; the mask is a bit of `Z`. The smaller-block square-wave sum is `H_e(X)`, and the larger-block sum is `-H_e(X)-chi_e(X)`. Including the equal block gives

\[
E_B[A\chi_\ell(B)\mid S]
=\frac{2a_sH_e(X)+(a_s+1)\chi_e(X)}H.
\]

Both ranges have been derived without assuming any ordering between `k` and `r`.

## 5. The affine block identity and the `k=q` boundary

The final-carry masked average is `2H_p(S)/N`. For `p>=k`, set `f=p-k`. The small input block of length `K` lies within one linear piece of the triangle at resolution `p`, and

\[
H_p(KX+s)=K H_f(X)+s\chi_f(X),\qquad 0\le s<K.
\]

The range `k<=q` guarantees `p=ell+q>=k` for **every** retained mask, including `ell=0`. This is the essential upper-domain restriction. The indices also satisfy `f<log2(H)`, as required by the subsequent period averages.

At the limiting case `k=q`, the lowest mask has `p=k` and `f=0`. Then `H_0(X)` is zero or one according to the parity of `X`, and the identity becomes `s` on rising blocks and `K-s` on falling blocks. It is valid at both the block start and every retained point `s<K`; no strict inequality `k<q` is needed.

For the upper-mask range, `e=ell-k` satisfies `0<=e<r` and `f=e+q>e` regardless of whether `k>=r`. For the lower-mask range, `ell<k` guarantees that the small wave's period divides `K`. Thus the formerly suggested restriction `k<r` is genuinely unnecessary, as claimed.

## 6. Moment calculations and the factor two

The period sums used in the manuscript are consistent. In particular, with `P=2^f`,

`E[U_X H_f(X)]=P/2` and `E[U_X chi_f(X)]=-P`.

For `ell<k`, set `J=2^ell`. The shifted small-triangle sums are

`E[H_ell(s+1)]=J/2`,

`E[s H_ell(s+1)]=J(K-2)/4`.

The latter follows by changing `t=s+1`: the full-period weighted triangle sum is `JK^2/4`, and subtracting the unweighted sum `KJ/2` gives the stated average. This shift is responsible for the surviving correction in the low-mask calculation.

Multiplying the conditional low-mask expressions yields

\[
M_{\ell,p}=\frac4{N^2}
\left(\frac{KPJ}{4}-\frac{PJ(K-2)}4\right)
=\frac{2^{\ell+p-k+1}}{N^2}\qquad(\ell<k).
\]

For the high-mask range, the mixed triangle/square and square/square expectations vanish by period pairing, since `f=e+q>e`. The surviving term uses `E[a_s]=1/K` and `E[H_e(X)H_f(X)]=2^(e+f)/4`, giving

\[
M_{\ell,p}=\frac{2^{\ell+p-k}}{N^2}\qquad(\ell\ge k).
\]

Thus the factor two below the split is exact and has a valid derivation; it is not inferred from the resulting correlation values.

The unmasked moment follows by expanding the product of the two conditional unmasked factors. The terms with a single `U_X` vanish. Since `E[a_s]=1/K` and `E[U_X^2]=(H^2-1)/3`,

\[
M_0=\frac1K\left(-\frac13+\frac4{3H^2}\right).
\]

No independence between `a_s` and `s` is needed in these calculations. They are both functions of the same low word; the vanishing mixed terms instead come from the independent `X` average.

## 7. Summation, endpoint reduction, and recurrence

Weighting the mixed moments by `2^ell` produces the sum

\[
2\sum_{\ell=0}^{k-1}8^\ell+
\sum_{\ell=k}^{r+k-1}8^\ell
=\frac{2^{3(r+k)}+2^{3k}-2}{7}.
\]

Substitution gives the displayed finite-sum expression. Collecting powers of `2^-k` gives exactly the claimed coefficients of `4^-k`, `2^-k`, and `16^-k`.

At `k=0`, the low-mask range is empty, `K=1`, and every masked moment is `2^(ell+p)/N^2`, matching the independently proved endpoint calculation. The coefficient combination `alpha+beta+delta` has the endpoint's positive correction `+1/(7*2^(3r+q))`, so the constant term's sign also reduces correctly. No expression involving a nonexistent below-split mask is used.

Since `H>=4`, `M0<0` and every mixed moment is positive. The final positive weights are subtracted, proving strict negativity throughout the valid range.

The characteristic polynomial is exactly

\[
(z-1/4)(z-1/2)(z-1/16)
=z^3-\frac{13}{16}z^2+\frac{11}{64}z-\frac1{128}.
\]

This proves the recurrence from the closed form. It is not justified merely by the coincidence of four standard-word observations; the manuscript supplies the required derivation and the correct range of four consecutive offsets.

## 8. Independent numerical evidence

### Before manuscript disclosure

`upper_range_independent_checks.py` passed:

- All 14 in-domain output-bit values available in the earlier original-word enumeration for `n=3,4,5`.
- All 275 independently computed DP values for `r,q=1..5`, `k=0..q`, at the distinct widths in `{r+q+k+1, r+2q+1, r+2q+3}`.
- All 60 recurrence checks using four directly computed DP values at a common word width.
- The four standard-word values at absolute bits 28 through 31, compared with the previously saved independent spectrum.

The required domain failure was also reproduced from both old original-word counts and the general DP:

`n=5,r=q=1,k=2,i=4`: true correlation `-7/256`, invalid extension `-57/2048`, difference `1/2048`.

### After manuscript disclosure

`upper_moment_review_checks.py` compared each intermediate closed moment against the previously independent four-state evaluator, for `r,q=1..5`, `0<=k<=q`, and `n=r+q+k+1`:

| Moment or boundary | Comparisons | Result |
|---|---:|---|
| Unmasked moment | 100 | All equal |
| Low-mask moments `ell<k` | 175 | All equal |
| High-mask moments `ell>=k` | 300 | All equal |
| Included parameter cases at `k=q` | 25 | All equal |
| Included parameter cases at `k=0` | 25 | All equal |
| Included parameter cases with `k>=r` | 35 | All equal |

The out-of-domain example isolates the failure more precisely. At `n=5,r=q=1,k=2,ell=0,p=1`, the independently evaluated masked moment is **zero**. The invalidly extended low-mask formula would give `1/256`. The middle-carry weight is `2^-3`, accounting for exactly the correlation discrepancy `1/2048`. Here `p<k`, so the within-block affine identity is unavailable. This supports the stated domain restriction without making an unsupported general claim about every possible extension.

## 9. Commands, artifacts, and remaining gates

Reproduce the two verification phases separately:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/upper_range_independent_checks.py
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/upper_moment_review_checks.py
```

Both recorded executions exited zero. Their exact source/input hashes, command lines, timestamps, declared domains, and individual rational comparisons are in `upper_range_independent_run.json` and `upper_moment_review_run.json`. No random sampling or new original-word exhaustive search was used.

The coefficient formula evaluates one correlation with a constant number of arithmetic operations on integers having `O(r+q+k)` bits. The recurrence can generate a valid offset sequence with a constant number of such arithmetic operations per further value, after three initial values. These are evaluation costs for this fixed input/output-mask family. They are not claims of improved generic ARX analysis complexity, optimal correlation, or attack complexity.

The mathematical review found no error, including in the low/high mask split, the `k=q` edge, and the `k=0` reduction. Formal proof-assistant validation, novelty against prior exact ARX work, and any improved cryptanalytic record remain separate gates.
