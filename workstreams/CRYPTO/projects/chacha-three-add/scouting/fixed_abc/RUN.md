# Fixed-abc scout: completed bounded run and decision

## Outcome and stopping decision

The exact model and four-state procedure in `SCOUT.md` passed the entire predetermined bounded test. The calculation is an ordinary application of two constant-operation chains with an exactly averaged nonoverlapping prefix. It is archived as **L0 input-distribution clarification**. The scout's purpose is complete; no larger input enumeration, search for favorable constants, or publication claim is warranted by these results.

The constant phase is necessary, and the two remaining carries are not generally independent. Both planned negative controls detected their intended errors.

## Command, environment, and true completion

Working directory:

```
/workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add
```

Command:

```bash
python scouting/fixed_abc/fixed_abc.py
```

| Field | Recorded value |
|---|---|
| Actual tool-observed process exit code | `0` |
| UTC program start | `2026-10-11T08:00:01.957368+00:00` |
| UTC program finish before report writing | `2026-10-11T08:00:01.958872+00:00` |
| Program computation timer | `0.0015120580001166672` seconds |
| Fixed parameter tuples | `17` |
| Exact original-word inputs, varying only `d` | `188` |
| Pointwise error-bit identities | `692` |
| Exact output-bit correlation comparisons | `54` |
| Cases refuting the false product of carry marginals | `7` |
| Cases detecting an omitted constant phase | `7` |
| Random seed | Not applicable: literal fixed cases and complete small-word enumeration |
| Python | `3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]` |
| Platform | `Linux-6.18.44-x86_64-with-glibc2.39` |
| Machine | `x86_64` |
| Peak process resident set | `11392` KiB |
| Source SHA-256 | `fa914112701aa6c6608c2b21f0a84fbc4e4615d9dac09c86b52ca41b7420a33e` |

The tiny program timer measures this bounded computation, not Python startup, tool latency, or report serialization. It is not presented as a stable performance benchmark. All parameters, signed sums, terminal state counts, and failure-control records are retained in `results.json`.

No earlier project implementation or verification source was imported. Both the direct original-word computation and the small-state evaluator were written in this scout, so their agreement is labeled a research self-check rather than independent agent verification. The general result is justified by the case-wise proof in `SCOUT.md`.

## Six standard-width analytical examples

Each example fixes `n=32,r=16,q=12,i=28` and fixes all three displayed input words. Only `d` is uniform. All values below come from 16 shared-bit state transitions after an exact 12-bit prefix average; there is no 32-bit input enumeration or statistical estimate.

| `a` | `b` | `c` | Exact signed correlation |
|---|---|---|---|
| `61707865` | `00000000` | `00000000` | `110069659/134217728` |
| `61707865` | `01234567` | `89abcdef` | `-9620621/33554432` |
| `61707865` | `deadbeef` | `10203040` | `-20410923/33554432` |
| `00000000` | `00000000` | `00000000` | `1` |
| `00000000` | `00000000` | `00008000` | `0` |
| `00000000` | `00000000` | `0000ffff` | `-32767/32768` |

These examples are synthetic fixed words. The first row is approximately `0.8200828656554222`; the next two are approximately `-0.28671684861183167` and `-0.6082929074764252`. Their magnitudes are not comparable as improvements over a coefficient computed under random `b,c`.

In particular, the previously derived fixed-`a` result averages over `b,c,d`, whereas this scout conditions on `b,c`. The precise relationship is the elementary law of total expectation:

\[
C_i^{\text{fixed }a,\ \text{uniform }b,c,d}
=2^{-2n}\sum_{b,c}C_i^{\text{fixed }a,b,c,\ \text{uniform }d}.
\]

Large positive and negative conditional values can cancel in this average. Computing such a value does not contradict the previous exact formula, establish a new attack, or justify substituting one input distribution for another.

## Explicit failure controls

For `(n,r,q,a,b,c,i)=(4,0,3,7,9,0,0)`, direct enumeration gives `-1`; omitting the constant first-add carry phase gives `+1`. The pointwise carry identity catches the error for every relevant input.

For `(n,r,q,a,b,c,i)=(2,0,0,1,2,1,1)`, the two random carries are complementary. Their individual signed expectations are zero, so the false independence product is zero; the correct joint signed expectation is `-1`. This is a local mathematical negative control, not an allegation that a specific paper uses that incorrect product.

The completed scout closes a model-use risk. Any further cryptanalytic work must specify the distribution of every input word, the role of constants and secrets, and any actual round composition separately. No external deployment, third-party key, or cipher oracle was accessed.
