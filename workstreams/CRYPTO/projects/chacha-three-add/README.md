# ChaCha three-addition signed-correlation study

Date: 2026-10-11 UTC. This project studies an exactly specified local component, using analytic proofs, original-input enumeration and independent exact counting. **Correctness and originality are separate:** several claims have written proofs and independent checks; no claim has yet cleared the literature originality gate or improved a published attack.

## Research target and attack model

All words have n bits, additions are modulo 2^n and rotations are to the left:

```
s = a + b
t = rotl(d xor s, r)
u = c + t
v = rotl(b xor u, q)
w = s + v
```

The target is `C_i = E[(-1)^bit_i(w xor L)]`, where L is obtained by replacing **all three** additions by XOR in that same program. This is a signed linear coefficient, not an XOR-differential probability, differential-linear coefficient, absolute correlation, or bias (which is C_i/2).

The operation parameters `(n,r,q)=(32,16,12)` come from the first three additions of a ChaCha quarter round. The full quarter round contains a fourth addition; the complete standard cipher has 20 rounds and feed-forward. See [RFC 8439 §§2.1–2.3](https://www.rfc-editor.org/rfc/rfc8439.html#section-2.1). Only the local endpoint w is analyzed here.

The remaining quarter-round operations never change w, so it is also exactly the **first final output word** of the full quarter round. This semantic equivalence does not supply a joint law for the other outputs or justify multiplying these coefficients across rounds.

Distribution U makes a,b,c,d independent uniform. Distribution A fixes a and makes b,c,d independent uniform. Substituting a standard constant into A is an exact conditional local result; it does not supply the joint distribution of a fixed secret key, nonce and counter or an attack on deployed ChaCha20.

## Results and proof paths

| ID | Statement | Evidence |
|---|---|---|
| C001 | Exact negative coefficient at i=r+q, r,q>=1, r+q<n | [Discovery proof](proofs/special_bit_signed_correlation.md); [independent proof](verification/INDEPENDENT_PROOF.md) |
| C002 | Fixed-first-word coefficient in O(r) integer arithmetic | [Proof and exact constants](proofs/fixed_first_word.md); original-input counts; independent general DP |
| C003 | Positive uniform-input range below r+q when r>=q | [Proof](proofs/positive_bit_range.md); independent original-input and standard-width counts |
| C004 | Any bit/rotation reduces to at most n four-state moments | [General reduction](GENERAL_REDUCTION.md); [general implementation](tooling/exact_dp.py); separately implemented verifier |
| C005 | At the special bit the conditional sign is positive exactly for a mod 2^(r+q)=0 | [Finite-sum proof](proofs/fixed_word_sign.md); independent review tracked in verification |
| C006 | Closed form above r+q through offset k<=q, plus its short recurrence | [Proof](proofs/overlap_bit_closed_form.md); [independent review](verification/UPPER_RANGE_PROOF_REVIEW.md) |

At standard parameters,

\[
C_{28}=-\frac{47180567524833621}{1180591620717411303424}
\approx-3.9963495163690355\cdot10^{-5}.
\]

For fixed a=0 the same bit instead has C=2^-44. Four standard constants have distinct negative coefficients; exact fractions are in the fixed-word proof and the independently compared standard tables. The changed sign is a mathematical consequence of the changed distribution, not evidence of a cryptanalytic break.

## Reproduction and audit

Start with [experiments/README.md](experiments/README.md), [verification/VERIFICATION_REPORT.md](verification/VERIFICATION_REPORT.md) and [tooling/README.md](tooling/README.md). Experiments retain exact commands, true process exit codes, source SHA-256 values, machine information and integer results. All executed mathematical checks are deterministic. The independent verifier first received only the mathematical specification and candidate formula, then wrote its own implementation and proof; later cross-reading is separately recorded. This is agent review, not human peer review or proof-assistant verification.

[NOVELTY_REVIEW.md](NOVELTY_REVIEW.md) compares ten near-predecessor families and equivalent masks. It marks the unmasked multi-addition coefficient and generic finite-state counting as prior art. The unavailable full texts of particularly close INDOCRYPT/ICISC/ISPEC results prevent an originality clearance. A complete fixed-word sign classification may be useful, but its mathematical correctness does not make it historically new.

## Stopping and next-cycle criteria

The initial cycle is successful as an exact, reproducible local analysis. It is **not** successful as a confirmed-original or best-attack improvement. Next work should inspect the missing near-neighbor theorems, compare the same masks and distributions, and determine whether the explicit rotation elimination or conditional classification remains a substantive contribution. The upper-bit overlap region is a bounded follow-up: obtain a proved closed form/recurrence or record a counterexample; do not grow a brute-force search without a complexity reason.

The upper-bit follow-up is now complete: the formula and recurrence were independently checked, and an exact k>q counterexample limits the theorem. [RESULTS.md](RESULTS.md) gives the full standard-width spectrum, fixed-word classification and current originality verdict. The next method comparison checks a more efficient application of existing matrix-prefix techniques before making any complexity claim.

No external submission, author contact, DOI registration, or academic preprint publication has been performed. The code and notes are checkpoints in the user-authorized research branch.
