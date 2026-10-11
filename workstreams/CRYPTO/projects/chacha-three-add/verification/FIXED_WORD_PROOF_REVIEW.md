# Mathematical cross-review: fixed first word and complete sign classification

Date: 2026-10-11. Verdict: **both reviewed mathematical statements and proofs passed review; no correction requested**.

## Reviewed versions and independence

| Manuscript | SHA-256 of reviewed version |
|---|---|
| `../proofs/fixed_first_word.md` | `e96dbb4e8ef1ece9ec26bc8ff5bda58a1f63d441b6934084a07890bf43b812cb` |
| `../proofs/fixed_word_sign.md` | `7fb3e5763f56369730408395242c646b6fe6f5f0cefcac34ed112ec649154c1f` |

Before reading these manuscripts, this verifier had independently implemented the original-word fixed-`a` enumerator and the general signed four-state evaluator. Their exact finite comparisons and standard-parameter output were already saved in `general_fixed_word_counts.jsonl`, `general_independent_run.json`, and `general_standard32_exact.json`. Those computations used the supplied general mathematical specification, without reading any discovery implementation.

The present document is a **post-disclosure written-proof cross-review**. The auxiliary check script was written after reading the two manuscripts. Its original-word evidence comes from the preceding blind code and data; its formulas were transcribed and checked from the now-disclosed mathematics. These kinds of independence are recorded separately. The discovery `experiments/`, `tooling/`, and `tooling/` outputs were not read by this verifier. This is internal agent review, not human peer review or formal verification.

## 1. Precise result checked

All additions are modulo `2^n`, rotations are left rotations, `r,q>=1`, `i=r+q<n`, and `N=2^i`. The first input word `a` is fixed and `b,c,d` are independent uniform words. Write `A=a mod N`.

For the signed first-output-bit correlation `C_A=E[(-1)^bit_i(w XOR L)]`, the fixed-word manuscript asserts

\[
C_A=\frac{N(1-2A)+2A(A-1)
+4\sum_{\ell=0}^{r-1}2^\ell T_{\ell,\ell+q}(A)}{2^rN^2},
\]

where

\[
T_{\ell,p}(A)=\sum_{x=0}^{A-1}\chi_\ell(x-A)H_p(x),\qquad p>\ell.
\]

Here `chi` is a periodic square wave and `H` its nonnegative triangular prefix sum, including periodic interpretation at negative arguments. The companion sign result is

\[
C_A=\begin{cases}
C_0,&A=0,\\
-C_0,&A=1,\\
<-C_0,&2\le A<N,
\end{cases}
\qquad C_0=2^{-(2r+q)}.
\]

Thus positive correlation occurs exactly for `A=0`; zero never occurs. Exactly `2^(n-i)` of the `2^n` possible fixed words have positive correlation, a fraction `2^-i`. This is a counting statement about possible conditioned input words under the stated local model, not an attack success probability or a claim about real key distributions.

At standard parameters, the third-addition output `w` is unchanged by the remaining quarter-round operations. It is exactly the complete quarter round's first output word; the fully XOR-linearized first output is likewise `L`. The result therefore is also a one-bit linear correlation of that output word under the specified input distribution. It supplies no assertion about the three remaining words or the joint output law.

## 2. Fixed-word derivation

With `a` fixed, the inverse map `(b,u,t) -> (b,c,d)` is correct. Equivalently the verifier's earlier map gives independent uniform `S,Y,T` with `B=S-a`. Consequently the low-word first carry equals `[S<A]`, and the upper bits of fixed `a` cannot affect this endpoint statistic after the independent middle word is eliminated.

The unmasked moment has the exact value

`[N(1-2A)+2A(A-1)]/N^2`.

This follows by subtracting twice the prefix `S=0,...,A-1` from the unrestricted average of `1-2S/N`. It gives `1/N` at `A=0` and `-1/N` at `A=1`, as required.

For the masked moment, averaging the final carry over its independent input yields `2H_p(S)/N`. The complete sum of `chi_ell(S-A) H_p(S)` is zero: the shift by `P=2^p` preserves the square wave when `p>ell`, and the two triangle heights sum to `P`; the remaining square wave sums to zero over `P` positions. Since `2P` divides `N`, this applies over the entire low-word domain. Inserting the threshold sign `1-2[S<A]` then gives exactly `-4T_(ell,p)(A)/N^2`, with the sign and factor four as displayed.

## 3. Signed antiderivatives, including negative arguments

The first manuscript explicitly uses Euclidean division `t=k(2h)+z` with `0<=z<2h`, so the formulas have a well-defined meaning for negative `t`.

For one full period, `sum chi=0` and `sum z*chi(z)=-h^2`. Consequently the weighted primitive consists of the full-period contribution `-k h^2`, the translated partial-period contribution `k(2h)F_0(t)`, and the partial weighted sum `G_1(z)`. This verifies the displayed `F_1` formula and its difference identity at ordinary positions and across period boundaries, including negative-to-nonnegative boundaries. The use of truncation toward zero instead of the specified Euclidean quotient would be invalid; no such ambiguity is present in the written statement.

Both `Q_0` and `Q_1` follow by telescoping. The `+A Q_0` term in `Q_1` is necessary because the summand's weight is `x`, whereas `F_1` uses the shifted argument `x-A`. The complete-period cancellation and the two triangular-segment formulas then give the stated constant-size evaluation of each `T`.

## 4. Abel summation and period reduction in the sign proof

This is the main point requiring careful indices. For `A>=1`, put `m=A-1`. Because `chi_ell(-d-1)=-chi_ell(d)`, reversal gives

\[
T=-\sum_{d=0}^{m}\chi_\ell(d)H_p(m-d).
\]

Use `chi_ell(d)=H_ell(d+1)-H_ell(d)` and telescope. The two boundary terms vanish because both triangular prefixes are zero at zero. The resulting expression is

\[
T=-\sum_{z=1}^{m}H_\ell(z)\chi_p(m-z)
 =-\sum_{y=0}^{m-1}H_\ell(m-y)\chi_p(y).
\]

This establishes the displayed Abel step, including the empty sum at `A=1`.

Let `h=2^ell`, `P=2^p`. Since `p>ell`, `2h` divides `P`. In the last expression, translating `y` by `P` preserves `H_ell(m-y)` and reverses the square-wave sign. Hence every complete block of length `2P` cancels. Write `m=K(2P)+t`, `0<=t<2P`. The residual block has summands `H_ell(t-y) chi_p(y)` for `0<=y<t`: reducing the first factor's phase is valid because `2h` divides `2P`. This explicitly resolves the potential phase ambiguity in the period reordering.

If `t<=P`, every residual square-wave sign is positive and reversal gives `F_ell(t)`. If `t>P`, the first `P` consecutive triangle values sum to `hP/2`, independently of their phase, and the remaining negative part gives `-F_ell(t-P)`. Thus

\[
T=\begin{cases}
-F_\ell(t),&t\le P,\\
F_\ell(t-P)-hP/2,&t>P,
\end{cases}
\qquad t=(A-1)\bmod 2P.
\]

### The exceptional-looking `A=0` boundary

The Abel derivation assumed `A>=1`, so `A=0` must be checked separately. Its defining sum is empty, giving zero. The modular formula uses `t=2P-1`, and

`F_ell(P-1)=F_ell(P)=hP/2`

because `H_ell(P)=0` and `P` is an integer number of small-triangle periods. The second branch therefore also gives zero. This boundary treatment is correct. At `t=P`, the two expressions would both give `-hP/2`, so the branch convention introduces no discontinuity.

## 5. From triangle bounds to the strict sign classification

`H_ell(z)>=0`, so `F_ell` is nondecreasing. Its value at `P` is `hP/2`. Both branches yield

`-hP/2 <= T_(ell,p)(A) <= 0`.

The correlation numerator can be written as

`N - 2A(N+1-A) + 4 sum 2^ell T_(ell,ell+q)(A)`.

At `A=0`, every `T` is empty and the numerator is `N`. At `A=1`, `H_p(0)=0` makes every `T` zero and the numerator is `-N`. For `2<=A<N`,

`A(N+1-A)-N = (A-1)(N-A) > 0`.

Thus the unmasked part alone is strictly less than `-N`, and the nonpositive triangular terms cannot increase it. The denominator is positive. This proves the strict inequality and excludes zero without relying on a numeric search.

## 6. Exact supporting checks and provenance

Run:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/fixed_proof_review_checks.py
```

The recorded run exited zero. Results:

| Check | Declared finite domain | Result |
|---|---|---|
| Both signed-primitive difference identities | `ell=0..5`; `t=-3*2^(ell+1)-1` through `3*2^(ell+1)+1` | 774 parameter pairs, 1,548 identities passed |
| Direct `T` versus Abel convolution, triangular-area formula, and signed-primitive formula | `p=1..6`, `ell=0..p-1`, `A=0..4*2^p+1` | All 2,610 cases passed |
| Bounds on `T` and area formula versus direct triangle summation | Same auxiliary domain | All cases passed |
| The `A=0` branch | All 21 auxiliary `(ell,p)` pairs | All passed |
| Fixed-word formula versus earlier blind original-word enumeration | All legal endpoint cases present in the `n<=4` conditional count file | All 56 fixed-word cases passed |
| Sign classification against those original-word counts | Same 56 cases | 10 at `+C0`, 10 at `-C0`, 36 strictly below `-C0` |
| Both arithmetic prefix formulas versus previously generated independent 32-bit DP values | Four standard constants, bit 28 | All four exact fractions agree |
| `A=0` at 32-bit standard rotations | Independent general DP versus fixed-word formula | `1/17592186044416` agrees |

No new original-word enumeration was performed for this review. The small auxiliary checks target index, sign, phase, and period-boundary errors; they do not replace the general proof. The exact command, run status, source/data/manuscript SHA-256 hashes, environment, individual original-word comparisons, and standard fractions are saved in `fixed_proof_review_run.json`. No random sampling was used.

## 7. Conclusion and limitations

The fixed-word formula, the negative-argument primitives, the Abel identity, the nonpositive bound on every triangular term, and the complete sign classification are mathematically consistent and agree with the independent pre-review computation. Both `O(r)` arithmetic evaluations are supported by their displayed finite formulas; their integer operands have `O(n)` bits. This is an arithmetic cost for correlation evaluation and says nothing by itself about improved attack cost.

The review does not establish that these are novel consequences relative to generic exact ARX analysis or older results. It supplies ordinary proof review and independent code evidence, with the dependence between the two disclosed prefix algorithms explicitly recorded. Any originality level or publication claim requires the separate literature review.
