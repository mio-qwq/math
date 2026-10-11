# Independent verification report

Date: 2026-10-11. Scope: signed endpoint correlation in the supplied three-addition local structure.

## Verdict

**PASS within the stated model.** The proposed closed form has been independently rederived for all integers r,q>=1 with r+q<n, at bit i=r+q. The reported exact fraction for n=32,r=16,q=12 matches. This is a written proof plus independent finite computations, not formal verification or human peer review. No originality or full-cipher attack claim is made.

Independence: the verifier received only the word-operation specification, candidate equation, and standard-parameter fraction. It did not read any discovery `experiments/` or `proofs/` file before writing and running its own code and proof. The independent method uses a bijection to uniform `(s,b,u,t)`, threshold events, and periodic square-wave prefix sums.

## Files

- `INDEPENDENT_PROOF.md`: complete general proof; includes exact bit endpoints and every independence justification.
- `independent_word_enumerator.cpp`: direct implementation of original and XOR-only word operations; exhaustive input loops; RFC8439 vector; negative rotation control.
- `independent_verify.py`: compiler/runner and independent integer-threshold sum; exact Fraction comparisons.
- `independent_word_counts.jsonl`: all direct counts, including out-of-domain rotations and all output bits.
- `independent_run.json`: exact commands, exit codes, durations, source hashes, environment, parameter rows, and negative controls.

Reproduction from any directory:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/independent_verify.py
```

No random seed is needed: the executed tests use full enumeration or exact integer sums. Compiler command uses `g++ -O3 -std=c++17 -Wall -Wextra -Werror`; compilation and execution returned zero with empty stderr.

## Evidence

All rotations r,q in [0,n) were exhaustively evaluated for n=3,4,5: 9+16+25=50 parameter pairs. Each pair covers every four-word input, namely 2^(4n) inputs, and records a signed sum for every bit. The theorem applies to 1+3+6=10 of those pairs; all ten match both the candidate closed form and the independently implemented threshold sum.

| n | r | q | target i | complete inputs | signed correlation |
|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 1 | 2 | 4096 | -3/16 |
| 4 | 1 | 1 | 2 | 65536 | -3/16 |
| 4 | 1 | 2 | 3 | 65536 | -3/16 |
| 4 | 2 | 1 | 3 | 65536 | -19/128 |
| 5 | 1 | 1 | 2 | 1048576 | -3/16 |
| 5 | 1 | 2 | 3 | 1048576 | -3/16 |
| 5 | 1 | 3 | 4 | 1048576 | -23/128 |
| 5 | 2 | 1 | 3 | 1048576 | -19/128 |
| 5 | 2 | 2 | 4 | 1048576 | -15/128 |
| 5 | 3 | 1 | 4 | 1048576 | -115/1024 |

The separate threshold implementation tested every r,q in {1,2,3,4,5}, totaling 25 cases. These tests support the independently proved identities but do not replace the general proof.

### Negative controls

| deliberate change | exact observed correlation | incorrectly reused formula | detected |
|---|---:|---:|---|
| q=0 at n=3,r=1,i=1 | 0 | -1/8 | yes |
| r+q=n at n=3,r=1,q=2,wrapped i=0 | 1/2 | -3/16 | yes |
| right rotation at n=5,r=1,q=2,i=3 | -1/8 | -3/16 | yes |

These are checks of the hypothesis boundary and rotation convention, not counterexamples to the stated theorem.

### Official ChaCha quarter-round vector

RFC8439 section 2.1.1 input `(11111111,01020304,9b8d6f43,01234567)` produced `(ea2a92f4,cb1cf8ce,4581472e,5881c4bb)` as required. This checks the implementation convention; it does not establish the correlation formula.

Source: https://www.rfc-editor.org/rfc/rfc8439.html#section-2.1.1 (retrieved 2026-10-11, `turn99view0`).

## Standard-parameter conclusion

At n=32,r=16,q=12,i=28:

```
signed correlation = -47180567524833621/1180591620717411303424
signed bias        = -47180567524833621/2361183241434822606848
Pr[error bit = 0]  = 1180544440149886469803/2361183241434822606848
```

The signed correlation is approximately -0.000039963495163690355. Its negativity is not an absolute-value convention, and bias is half the correlation.

## Remaining limits

1. Novelty needs independent literature review. A correct formula can still be an already known special case.
2. The input distribution is four independent uniform n-bit words. A fixed-key or initial-state ChaCha distribution is not substituted silently.
3. At standard parameters, the word after the third addition is exactly the first output word of a complete quarter round; subsequent operations change only the other three words. The formula therefore also describes that single-output-bit linear correlation. It supplies no joint-output analysis or full-round/ChaCha20 attack by itself.
4. General correctness comes from the written proof, not numerical extrapolation from n<=5.
5. No proof assistant has checked the derivation. The next useful step is to compare this independent proof with the discovery proof and resolve any semantic discrepancy.

Subsequent review on 2026-10-11: the discovery endpoint manuscript was read only after the blind work above, and its proof passed cross-review; see `DISCOVERY_ENDPOINT_PROOF_REVIEW.md`. Arbitrary-bit and fixed-first-word extensions are separately documented in `GENERAL_INDEPENDENT_PROOF.md`, `GENERAL_VERIFICATION_REPORT.md`, and `FIXED_WORD_PROOF_REVIEW.md`. The first-output-word scope clarification above was added during that follow-up review.
