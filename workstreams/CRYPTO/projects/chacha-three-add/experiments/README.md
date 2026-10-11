# Reproducible discovery and self-check experiments

## Scope and evidence status

`exact_signed.py` accompanies three written derivations in `../proofs/`:

- the exact signed correlation at bit `r+q` for uniform inputs;
- the conditional formula for a fixed first input word;
- the positive-correlation range `0<=i<r+q` when `r>=q`.

This directory contains the discovering agent's own implementation and self-checks. It is not independent verification, formal proof-assistant certification, a claim of originality, or a cipher attack. A separate agent may implement and audit the statements independently without this source code.

## Complexity decision made before execution

The direct implementation enumerates `2^(4n)` original inputs for each `(n,r,q)` and accumulates all `n` output-bit signs. Its time is `O(n*2^(4n))` per parameter triple and its retained result storage is `O(n+2^n)`. Enumerating all `r,q>=1`, `r+q<n`, for `n=3,4,5` visits exactly 6,492,160 input tuples across 10 parameter triples. This bounded run was chosen before execution; 32-bit brute force would require `2^128` tuples and is not attempted.

The fixed-word expression instead uses `O(r)` exact arithmetic operations on `O(n)`-bit integers. Standard-word values in the result file are theorem predictions evaluated with this formula, not empirical estimates. The uniform special-bit formula uses a constant number of exact arithmetic operations.

## Exact command and observed execution

Working directory:

```
/workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add
```

Command:

```bash
python experiments/exact_signed.py --max-n 5 --output experiments/results/exact_signed_max5.json
```

Observed execution on 2026-10-11:

| Field | Recorded value |
|---|---|
| Actual process exit code | `0` |
| UTC start | `2026-10-11T07:19:38.468055+00:00` |
| UTC finish | `2026-10-11T07:19:45.171399+00:00` |
| Program elapsed seconds | `6.703367934999733` |
| Input tuples executed | `6492160` |
| Prefix arithmetic self-check cases | `3786` |
| Random seed | Not applicable: no randomness or sampling |
| Python | `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` |
| Platform | `Linux-6.18.44-x86_64-with-glibc2.39` |
| Machine | `x86_64` |
| Peak resident set, Linux `ru_maxrss` | `12160` KiB |
| Source SHA-256 | `0cb36f039d5c40b59478fa21a720252d4ac45daa3dda962968e296bc25c12543` |

The initial execution tool returned a live process identifier; the subsequent poll observed actual completion with exit code zero. The JSON success field alone is not being substituted for an observed process exit code.

The source has no third-party Python dependencies. `results/exact_signed_max5.json` records the resolved interpreter path, source hash, full integer signed counts, exact rational results, standard-parameter predictions, and environment. Proof documents are not hashed inside this run file; the repository's final manifest and Git commit should bind those documents separately.

## What was checked

For every eligible `(n,r,q)` and every original input, the program computes the modular-add function and the XOR-linearized function directly. It does not use the transformed carry variables to generate the empirical count. Each correlation is the exact signed integer count divided by the number of inputs.

It checks the special-bit uniform formula; the fixed-first-word formula for **every** `a`; the average of those conditional formulas against the uniform formula; `a=0`; and every bit covered by the positive-range theorem. The prefix primitives are checked against their one-step differences for both positive and negative arguments, and the triangle product is compared with direct finite sums.

Boundary coverage includes `r=1`, `q=1`, `r<q`, `r=q`, the minimum allowed width `n=r+q+1`, `a=0`, and `a=2^n-1`. The theorems do not cover `r=0`, `q=0`, or `r+q>=n`; the run excludes those parameter regimes rather than silently extrapolating to them.

The deliberately false independent-carry product gives positive `2^(-3r-2q)`, while all exact special-bit results are negative. This is a negative control for our own modeling, and is not attributed to any published cryptanalysis without inspecting that paper's exact masks and assumptions.

## Exact uniform special-bit results

| `n` | `r` | `q` | Exact signed correlation |
|---:|---:|---:|---:|
| 3 | 1 | 1 | `-3/16` |
| 4 | 1 | 1 | `-3/16` |
| 4 | 1 | 2 | `-3/16` |
| 4 | 2 | 1 | `-19/128` |
| 5 | 1 | 1 | `-3/16` |
| 5 | 1 | 2 | `-3/16` |
| 5 | 1 | 3 | `-23/128` |
| 5 | 2 | 1 | `-19/128` |
| 5 | 2 | 2 | `-15/128` |
| 5 | 3 | 1 | `-115/1024` |

Further testing should address a concrete missing risk or an independently proposed extension. Repeating larger direct enumerations alone would not establish novelty or improve the analytical complexity.

## Follow-up: conditional-sign classification

The proof in `../proofs/fixed_word_sign.md` rewrites each conditional sum as a nonpositive triangular area. This yields the complete sign classification: if `A=a mod 2^(r+q)`, then `C_A` is positive only for `A=0`, equals `-C_0` for `A=1`, and is strictly below `-C_0` for all larger `A`. The new bounded check targets this identity and the alternate arithmetic implementation, not a larger brute-force search.

Before running, the experiment fixed the domain to `2<=r+q<=12`, all positive `r,q` with that sum, and all `A` in `[0,2^(r+q))`. That domain has exactly 81,924 formula cases. Each case costs `O(r)` arithmetic operations, with at most 12-bit parameter-domain inputs and small exact integer intermediates. No original-input enumeration or random sampling is performed in this follow-up.

Command in the same working directory:

```bash
python experiments/fixed_word_sign_check.py --max-i 12 --output experiments/results/fixed_word_sign_max12.json
```

| Field | Recorded value |
|---|---|
| Actual process exit code | `0` |
| UTC start | `2026-10-11T07:26:28.910178+00:00` |
| UTC finish | `2026-10-11T07:26:31.336316+00:00` |
| Program elapsed seconds | `2.426149630000509` |
| Exact formula cases | `81924` |
| Triangle-area direct-sum checks | `980` |
| Triangle-product arithmetic comparisons | `458748` |
| Random seed | Not applicable: deterministic calculation |
| Peak resident set | `12672` KiB |
| Follow-up source SHA-256 | `ed87b0f85878f3136380a8d2d72aecfa9aea6d1ce2b430107cd9b0e6e6995041` |
| Imported source SHA-256 | `0cb36f039d5c40b59478fa21a720252d4ac45daa3dda962968e296bc25c12543` |

The follow-up used the same Python and Linux environment as the original enumeration. It imports the discovering implementation to compare two exact finite-sum evaluations, so it is explicitly a self-check. The general sign statement is justified by the written proof, not by absence of a counterexample in these 81,924 cases. The JSON also retains finite-domain minima as diagnostic observations; no general extremum theorem is inferred from them.
