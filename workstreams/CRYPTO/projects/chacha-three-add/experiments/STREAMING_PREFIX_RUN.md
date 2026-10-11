# Reversible-prefix baseline: reproducible run

## Predetermined bounded workload

This cycle applies the Literature Agent's established-framework baseline to the already specified local correlation. It performs no new original-input enumeration and uses no randomness or third-party library. Before running, the comparison set was fixed to 216 uniform original-word values, 1,274 fixed-word original-word values, and 160 independent standard-32 values.

The core routine keeps only two synchronized prefix/inverse pairs, one final row, a constant number of temporary `4x4` matrices, and a weighted accumulator. It has no per-position prefix list. Its bound is `O(n)` exact rational arithmetic operations and `O(n)` live auxiliary bits per requested output bit, as proved in `../proofs/streaming_prefix_baseline.md`. The test harness separately retains comparison records and parses the input JSON files.

## Command and observed completion

Working directory:

```
/workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add
```

```bash
python experiments/streaming_prefix.py --output experiments/results/streaming_prefix_run.json
```

| Field | Recorded value |
|---|---|
| Actual tool-observed process exit code | `0` |
| UTC timed-harness start | `2026-10-11T07:46:13.768232+00:00` |
| UTC timed-harness finish | `2026-10-11T07:46:15.249035+00:00` |
| Timed-harness seconds | `1.4808091169998079` |
| Uniform original-word comparisons | `216` in `0.1067728440002611` seconds |
| Fixed original-word comparisons | `1274` in `0.3242831309999019` seconds |
| Standard-32 comparisons | `160` in `1.0495624449995375` seconds |
| Random seed | Not applicable: deterministic exact arithmetic |
| Python | `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` |
| Platform | `Linux-6.18.44-x86_64-with-glibc2.39` |
| Machine | `x86_64` |
| Whole-process peak resident set | `14976` KiB |
| Source SHA-256 | `225348096f0e4bddbd13a117840ea45ea5976c32b6a4ec65e2d0ee4476d905b7` |

The program's timer begins after the constant transition/inverse table is constructed. It includes data-file parsing, comparisons, and in-memory result construction; it ends before result JSON serialization. It is not a whole-process wall-clock benchmark. Earlier project runs have different workloads and timing scopes, so no empirical speedup ratio is inferred.

The initial process call returned a running session after the first two comparison groups. A subsequent process poll observed successful completion with actual exit code zero.

## Frozen input hashes

| Data file | SHA-256 |
|---|---|
| `verification/independent_word_counts.jsonl` | `848a174a1f19993baad8cffd32685a0aa6a44205f1da99114483bc4c13fb13ba` |
| `verification/general_fixed_word_counts.jsonl` | `ef161507042abb5352dcf1c09006b536d04ba34a0451f7d9bad5208772ea372c` |
| `verification/general_standard32_exact.json` | `1d593d05f7d6aa466ce6ac9b1f62d8efd4e2268098876031dc1f193e00ebf421` |

Only these frozen data files were read by the harness. No root or verifier source implementation was imported or inspected.

## Premise checks and arithmetic instrumentation

The three unmasked transition matrices were regenerated from the bit truth tables. Their determinants were computed using both exact Gauss–Jordan elimination and the separate 24-term Leibniz expansion. Each determinant is `1/16`. Both `P P^-1=I` and `P^-1 P=I` were checked, together with every constant boundary-phase variant. The result JSON includes the exact three matrices and their inverses.

Every one of the 1,650 correlations matched its frozen exact value. Each call also satisfied the proved `<=8n` bound on dynamic `4x4` matrix products.

Across all calls, instrumentation recorded:

| Metric | Value |
|---|---:|
| Dynamic matrix products | 23,888 |
| Row–matrix products | 12,870 |
| Counted nonzero scalar products in matrix/row routines | 1,013,088 |
| Largest observed reduced numerator bit length | 79 |
| Largest observed reduced denominator bit length | 79 |

The scalar counter covers the matrix/row routines; it is not an exhaustive count of every scalar multiplication in the harness. The observed bit lengths cover the instrumented dynamic matrices, rows, moments, and accumulators. The proof supplies the general growth bound. Process RSS includes Python, constant tables, parsed data, and retained test records, so it is not used to infer asymptotic core space from one execution.

The uniform data include all rotations for widths 3–5. The fixed-word data include all rotations and first-word values for widths 1–4. These cover `q=0`, `i=0`, `i=k`, rotation wraparound, and equal-position `BY` insertion without new brute force. The standard file contributes all 32 bits for one uniform distribution and four fixed ChaCha constants.

## Classification

This is a baseline application of signed finite-state kernels and elementary reversible-prefix products. It improves the arithmetic-operation count relative to this project's direct recomputation of every moment; it does not establish an improvement over the best published method, a smaller schoolbook bit-operation exponent, an optimized wall-clock advantage, or a new cipher attack. Correctness and computational fairness are the completed outputs of this cycle.
