# Fixed-abc scout: independent verification and subsequent ordinary review

Review date: 2026-10-11. Reviewer: `/root/survey_publickey`.

**Verdict: the specified distribution, general proof, implementation, and six disclosed standard-width examples pass the review. No mathematical or code correction is requested. Classification remains L0.** This closes a concrete input-distribution ambiguity; it does not establish a new cryptanalytic method or attack.

## 1. Two separate review stages

The verifier first derived the constant carry phase, the change of variable to a uniform word, the two support intervals, and an integer four-state evaluator without reading the discovery fixed-abc proof, code, result JSON, or run report. An independent original-word implementation and a separate threshold sum agreed with that evaluator on 7 predetermined settings, 90 original `d` inputs, and all 23 corresponding output-bit coefficients. That mathematical derivation, code, and receipt were then frozen in `INDEPENDENT_STAGE_MANIFEST.json`:

`05dda496968ff4d50a182b745cb68126a1e510b3746a5bb619b7ca48f2a7af8e`.

The independence claim is limited and explicit: the parent supplied the word model and requested constant-state verification; the verifier already knew the general carry identity from earlier independent work. The claim is independent derivation and implementation of this conditional model, not independent invention of the research target.

Only after this freeze did the verifier open `../SCOUT.md`, `../fixed_abc.py`, `../results.json`, and `../RUN.md`. This second stage is an **ordinary proof/code/results review**. It imported the discovery evaluator after reading its source, with bytecode-cache creation disabled. It did not invoke its `main()`, rerun the discovering agent's 17-setting harness, modify its files, or perform any additional original-input enumeration. No root `tooling/` implementation was consulted for this review.

## 2. Mathematical audit

The original output and its XOR-linearized expression in `SCOUT.md` and `fixed_abc.py` agree algebraically. The constant phase is

\[
(-1)^{\alpha_i\oplus\alpha_k},\qquad
\alpha=(a+b)\oplus a\oplus b,\quad k=(i-r-q)\bmod n.
\]

It includes the first addition even though the inputs to that addition are now fixed. The substitution `U=c+R_r(d XOR S)` is a permutation for every allowed rotation, so `U` is exactly uniform. No independence assumption between the remaining carry and borrow is introduced.

The variable sign is exactly the XOR of the incoming borrow at `j=(i-q) mod n` in `U-c` and the incoming carry at bit `i` in `S+R_q(b XOR U)`. The borrow comparison is strict (`U_low < c_low`), while the addition threshold is inclusive (`S_low+Y_low >= 2^i`). Both zero-bit boundaries are handled correctly. The change of variable also proves that, with all other parameters fixed, rotation `r` changes only the known phase and leaves the absolute correlation unchanged.

For `i>=q`, the final carry first consumes the independent block `U[n-q,n)` and then shares `U[0,i-q)` with the borrow. The blocks are disjoint because `i<n`. The prefix carry probability is exactly `(S mod 2^q)/2^q`; XOR with fixed `b` bits does not affect its uniform input distribution. For `i<q`, the borrow first consumes the independent block `U[0,n-q)` and then shares `U[n-q,n-q+i)` with the final carry. Its prefix borrow probability is exactly `(c mod 2^(n-q))/2^(n-q)`. In either case the shared bits appear in the same order in both processes, so no unbounded retained rotation state is needed.

The two displayed update rules correctly advance a subtraction borrow and an addition carry on the same uniform bit. The state order `2*borrow+carry`, prefix weights, and terminal signs agree with the independently derived evaluator. The proof includes `n=1`, `r=0`, `q=0`, `i=0`, `i=q`, zero fixed words, and an empty overlap.

The two limiting identities in the discovery note follow immediately: `c=0` makes the borrow zero, and `S=0` makes the final carry zero. The law of total expectation relating the fixed-`a,b,c` coefficient to the earlier fixed-`a` coefficient is correct. Large or zero conditional coefficients do not contradict the averaged coefficient.

## 3. Implementation and resource audit

Reviewed discovery source SHA-256:

`fa914112701aa6c6608c2b21f0a84fbc4e4615d9dac09c86b52ca41b7420a33e`.

The function `fixed_abc_correlation` realizes the proof directly. It maintains four current nonnegative counts and four following counts. Initialization uses one exact prefix threshold count, not an array of all prefixes. Every shared bit branches on the two possible uniform input bits; each branch updates the intended destination borrow/carry state. It multiplies the denominator by two after each step and asserts that total mass equals that denominator. The final denominator is `2^i` or `2^j`, exactly as in the proof, and the fixed phase is multiplied into the signed terminal numerator before reduction.

For one output bit the function has `O(n)` exact arithmetic operations and `O(n)` auxiliary bits. Counts and denominator are at most `2^(n-1)`. The `O(n^2)` elementary bit-cost upper bound for the counting loop is consistent with the operand size; final rational normalization is correctly identified as a separate gcd cost. The source's `max_integer_bits` diagnostic tracks state counts and denominators. It does not measure every temporary Python operand, Fraction internal, allocator object, or total process memory. This distinction does not affect the asymptotic `O(n)` auxiliary-bit proof.

The fixed list of 17 test settings, 54 result records, counterexample lists, six example records, and serialized output belong to the harness, not to the single-output counting core. The process RSS and approximately 0.0015-second computation timer are historical self-check metadata; this review does not independently reproduce that timing or interpret it as a stable performance benchmark. The timer excludes Python startup and result serialization, as stated in `RUN.md`.

Assertions validate the documented research-domain inputs during ordinary Python execution. The code is a local mathematical evaluator, not a production API with a separately specified invalid-input contract. No validation changes are needed for the authorized scope.

## 4. Actual post-disclosure checks

Actual command, tool-observed exit code **0**:

```sh
python workstreams/CRYPTO/projects/chacha-three-add/scouting/fixed_abc/verification/ordinary_review_checks.py
```

Working directory: `/workspace/scratch/5f0455e66649/math-crypto`.

The discovery evaluator was compared against the 23 already frozen independent original-word bit coefficients. All exact fractions, terminal four-state counts, denominators, and constant phases agree. This reuses existing original-word evidence; it does not claim a new enumeration.

The six disclosed standard-width examples were then evaluated by the already frozen independent implementation and by the reviewed implementation. All exact fractions and terminal counts agree with the frozen discovery result JSON. Parameters are `n=32,r=16,q=12,i=28`, with **only `d` uniform**:

| Fixed a | Fixed b | Fixed c | Exact signed correlation |
|---|---|---|---:|
| `61707865` | `00000000` | `00000000` | 110069659/134217728 |
| `61707865` | `01234567` | `89abcdef` | -9620621/33554432 |
| `61707865` | `deadbeef` | `10203040` | -20410923/33554432 |
| `00000000` | `00000000` | `00000000` | 1 |
| `00000000` | `00000000` | `00008000` | 0 |
| `00000000` | `00000000` | `0000ffff` | -32767/32768 |

These are six analytical evaluations selected by the discovering agent before disclosure to the verifier. They are not an independent sample selection, an input search, or a 32-bit original-word enumeration. The zero-operand rows also satisfy their elementary one-carry limiting identities.

Arithmetic consistency of the discovery receipt was checked: its 17 settings imply 188 original inputs, 692 pointwise bit identities, and 54 output coefficients; the stored signed sums, denominators, and exact fractions are mutually consistent. This is a receipt consistency check, not a rerun or independent attestation of its entire original-word execution.

The newly disclosed false-independence control also has a short direct proof. At `(n,r,q,a,b,c,i)=(2,0,0,1,2,1,1)`, `S=3`, the first carry phase is positive, the borrow is `1-U_0`, and the final carry is `U_0`. They are complementary, so the joint signed expectation is `-1`, while both marginal signed expectations are zero. This proof is recorded as post-disclosure review; it was not part of the frozen blind-stage check selection.

All post-disclosure parameters, exact values, source hashes, and execution metadata are in `ordinary_review_run.json`. The independent-stage three file hashes were checked unchanged before this run.

## 5. Scope, originality, and disposition

The strongest result here is an exact, proved conditional distribution formula with a bounded-state evaluator. The model is fixed `a,b,c` and uniformly independent `d` within one local quarter-round relation. Under the RFC operation order, `w` is also exactly the complete quarter-round first output word, because later operations leave that word unchanged. No calculation for the remaining outputs, their joint distribution, a fixed-key full ChaCha state, or a multi-round attack is supplied.

The independent distribution control `(n,r,q,i)=(3,1,1,2)` gives `-3/16` for four uniform words, `1/8` for fixed `a=0` with uniform `b,c,d`, and `1` for fixed `a=b=c=0` with uniform `d`. These are different conditional expectations, not comparable attack improvements.

This verifier did not conduct a fresh priority search for the fixed-abc note's Mealy-machine citation during the mathematical/code audit; the project's separate literature review owns the bibliographic comparison. The evaluator is an ordinary constant-operation finite-state application, and the result is intentionally retained at **L0**. No new lemma, original algorithm, best-attack improvement, or publication recommendation is inferred from successful verification. Internal agent verification is not human peer review or formal proof-assistant certification.

The bounded scout has met its declared stopping criterion. Archive the model clarification and its independently checked evidence. Broader enumeration or favorable-constant searches are not needed to settle this task.

## 6. Freeze and file ownership

This reviewer wrote only within `scouting/fixed_abc/verification/` for the current task and performed no Git mutation. `FIXED_ABC_VERIFICATION_MANIFEST.json` records the final new files and observed Git HEAD. The old 22-file independent verification set and the separate six-file streaming review remain frozen and unchanged. The four discovering-agent fixed-abc files were read only and their hashes are recorded in the ordinary review receipt.
