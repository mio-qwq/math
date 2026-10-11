# Overlapping-carry research cycle: execution receipt

## Target and budget before execution

The target was the uniform-input all-XOR-mask correlation at bit `i=r+q+k`, initially `0<=k<min(r,q)`. The analytical derivation proposed the larger domain `0<=k<=q`. Before testing, the computation was bounded to `2<=i<=8` and all positive `r,q` with nonnegative `k=i-r-q`.

For each absolute bit position `i`, the code directly enumerates `(S,Y)` once and `(S,B)` once per lower-carry position `k`. It accumulates one-bit signed masks in the same loops. This uses `O(i^2*2^(2i))` simple bit operations across all `k` at a given width, with `O(i*2^i)` retained signed counts. It visits exactly 669,920 threshold input pairs across the complete bounded run. There is no new four-word enumeration, no 32-bit brute force, and no sampling.

After conditioning on `S`, multiplying the separately counted sums over `B` and `Y` evaluates the complete three-variable moment exactly; the mathematical justification is in `../proofs/overlap_bit_closed_form.md`.

## Command and real process result

Working directory:

```
/workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add
```

Command:

```bash
python experiments/overlap_moments.py --max-i 8 --output experiments/results/overlap_moments_max8.json
```

| Field | Recorded value |
|---|---|
| Actual tool-observed process exit code | `0` |
| UTC start | `2026-10-11T07:33:41.658848+00:00` |
| UTC finish | `2026-10-11T07:33:42.075917+00:00` |
| Program elapsed seconds | `0.41709214100046665` |
| Threshold pair evaluations | `669920` |
| In-domain parameter triples | `62` |
| In-domain masked-moment comparisons | `214` |
| Reused original-input correlations | `14` |
| Out-of-domain tested triples with a mismatch | `22` |
| Random seed | Not applicable: exact deterministic computation |
| Python | `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` |
| Platform | `Linux-6.18.44-x86_64-with-glibc2.39` |
| Machine | `x86_64` |
| Peak resident set | `12288` KiB |
| Source SHA-256 | `e4127deabed9f4fdb6825be52030e699b7f9d720516aded12cc64dd8fe45ce26` |
| Reused original-input JSON SHA-256 | `f3bf9c13f2d9b3b02a553fc7f9acc9cef51314814622c93fbd0c6be7fd35ba16` |

## Outcomes and negative control

All in-domain moments agreed with their derived closed forms, and their weighted sums agreed with the three-geometric-term correlation formula. Standard-word predictions matched the four independently supplied root-agent values at bits 28–31. The recurrence was also checked arithmetically on bounded legal parameters; its general justification is the characteristic polynomial in the proof.

The domain restriction is substantive. The first mismatch outside the theorem range was `i=4,r=1,q=1,k=2`: the exact threshold calculation gives `-7/256`, while the candidate extrapolation gives `-57/2048`. This is a negative control against removing the condition `k<=q`.

No independent-verification label is attached to this discovering-agent run. The program did not read the root `tooling/` implementation or the verifier's source. It read only the discovering agent's previously frozen original-input JSON for reuse of exact counts. The four root-agent standard-word fractions were included solely as explicit cross-check values and were not fitted to obtain the symbolic coefficients.

The original frozen proof and experiment files were not modified during this appended subcycle. Further work should address independent review, unresolved literature overlap, or a separately justified mathematical extension; increasing enumeration alone would not improve the result.
