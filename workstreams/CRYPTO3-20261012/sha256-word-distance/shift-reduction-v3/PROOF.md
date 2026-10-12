# Temporal-window reduction for true SHA-256 13-word difference supports

**CRYPTO3-20261012, phase 3 — new written lemma, verified by a separate definition-based checker; still a research candidate pending independent mathematical review.** This is a conditional reduction of possible support patterns, **not** a proof of minimum distance 14 or a SHA-256 attack. It uses *arbitrary* 16-word input blocks, without padding constraints.

## 1. Frozen object and the precise theorem

The input to this note is the **fixed 15-pattern classification** in SHA-256 CRYPTO2 v2, commit `80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, file `projects/sha256-schedule-distance/v2/supports.json`. The extracted, byte-identical local `supports-v2.json` is SHA256 `02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`. We do **not** independently reprove completeness of that list or the inherited lower bound 13.

Let `E(M)` be the true 64-word SHA-256 schedule of an arbitrary 16-word input `M` in `Z/(2^32)`, using

    W[t] = g(W[t-2]) + W[t-7] + f(W[t-15]) + W[t-16],   16 <= t < 64,

where `f=ROTR7 xor ROTR18 xor SHR3` and `g=ROTR17 xor ROTR19 xor SHR10` on 32-bit words. For two messages `M != M'`, write `S = {t in [0,63]: E(M)[t] != E(M')[t]}`. A support *is attainable* only if **both** real schedules and both complete initial 16-word inputs exist.

**Theorem A (exact left-window implications).** If support number `source` is attainable, so is `target` in each row:

| source | shift `r` | target | future extension terms checked |
|---:|---:|---:|---|
| 0 | 1 | 9 | `t=64` |
| 1 | 1 | 0 | `t=64` |
| 2 | 2 | 0 | `t=64,65` |
| 4 | 3 | 0 | `t=64,65,66` |
| 6 | 1 | 12 | `t=64` |
| 13 | 2 | 12 | `t=64,65` |
| 7 | 3 | 12 | `t=64,65,66` |

The new input pair is the two adjacent 16-word windows of the *actual* sequences, not a free collection of independently selected word pairs.

**Theorem B (reverse implications for the first family).** If support 0 is attainable, then supports 1, 2, and 4 are attainable, by **right** shifts of 1, 2, and 3, respectively, after uniquely constructing a common three-word backward prefix. Therefore 0, 1, 2, and 4 are equivalent for attainability; there is no analogous unconditional reverse assertion for 12, 6, 13, and 7.

**Corollary.** Subject to the inherited complete list of 15 necessary supports and previously proved unconditional exclusions 3 and 14, it is sufficient for proving `|S| >= 14` to exclude the **six** representative supports

    {5, 8, 9, 10, 11, 12}.

Proof of the corollary: support 0 directly implies support 9. Each of supports 1, 2, 4 implies support 0, hence by transitivity also support 9. Each of supports 6, 7, 13 implies support 12. No support in the inherited 15-pattern list is omitted. Conversely, the current corollary does **not** establish that these six representatives are attainable or impossible.

## 2. Proof of Theorem A: extend, shift, re-expand

The standard recurrence has time-invariant lags. **Extend** any true 64-word schedule forward by the *same* formula for indices `t=64,65,66`. This defines extra words uniquely, for each base message separately. Let `W` and `W'` denote these extended schedules.

At the three extra indices the relevant predecessor sets, including the direct `W[t-16]` term, are

    t=64: {62, 57, 49, 48};
    t=65: {63, 58, 50, 49};
    t=66: {64, 59, 51, 50}.

For each of the seven rows in Theorem A, direct substitution of the frozen *source* support shows **none** of the four predecessors at each required extra index is active. At `t=66`, the potentially new index 64 has already been shown inactive. Equal operands produce equal `f` and `g` outputs; hence both schedules have the same new word at each needed extra index. This is a universal argument for **any** base words: it does not use cancellation of two nonzero terms or a zero-base assumption.

Now fix a row with shift `r` and define

    V[i]  = W[i+r],   V'[i] = W'[i+r],   0 <= i <= 63.

Set the two *new* 16-word inputs to `V[0..15]` and `V'[0..15]`. For `16 <= i <= 63`, the extended recurrence at `i+r >= 17` gives exactly the standard recurrence for `V[i]` and `V'[i]`. Therefore `V,V'` are genuine SHA-256 expanded blocks. None of the frozen source supports has an index `< r`, so no old active location is discarded. All added tail indices `64..63+r` are inactive, so no new active location is introduced. Consequently their support is exactly `{s-r : s in S_source}`, equal to the listed target support in all seven rows. Each target retains active input coordinates, so its two 16-word inputs are distinct. This completes the proof.

## 3. Proof of Theorem B: unique common backward prefix

Take an arbitrary real pair with support 0:

    S0={2,9,10,16,23,24,30,37,38,44,51,52,58}.

The recurrence can be solved **backwards** because the coefficient of `W[t-16]` is 1. Define the three extra words, first at `t=15` then `t=14` and `t=13`, by

    W[t-16] = W[t] - g(W[t-2]) - W[t-7] - f(W[t-15])

separately for each input; everything on the right is already defined at its step. The same construction applies to `W'`. For `t=15,14,13` the nonnegative predecessor indices required, apart from the newly reconstructed positions, are respectively

    t=15: {15,13,8,0};
    t=14: {14,12,7} and the newly constructed -1;
    t=13: {13,11,6} and the newly constructed -2.

None of `{0,6,7,8,11,12,13,14,15}` lies in `S0`. Induction therefore shows `W[-1]=W'[-1]`, then `W[-2]=W'[-2]`, then `W[-3]=W'[-3]`.

For `r=1,2,3` define the new 64-word sequences

    V[i] = W[i-r],   V'[i] = W'[i-r],   0 <= i <= 63.

Every new recurrence at `i >= 16` is one of the old recurrences, with old index `i-r >= 13`, which holds either by the standard rule or by the displayed backward definitions. So the shifted sequences are real SHA-256 schedules of their first 16 words. Their support is exactly `S0+r`, since the three new negative prefix words agree and `max(S0)=58 <= 63-r`. Direct comparison with the fixed pattern file yields supports 1, 2, and 4 for `r=1,2,3`. Both inputs are unequal because the new support still meets the initial 16 words. This proves Theorem B.

**Important boundary caveat.** For support 12, positions 13 and 15 are active. The backward equation at `t=15` need *not* construct the same -1 word for both inputs. Thus Theorem B cannot automatically be copied to the second family, even though its masks are translates.

## 4. Consistency with the two previously excluded supports

There is also a valid *different* time-shift implication: **support 3 implies support 14**. Extend a hypothetical true support-3 pair to t=64,65. For t=64, the only active predecessor among {62,57,49,48} is position 57, so `d64=d57 != 0`. For t=65, none of {63,58,50,49} is active, so `d65=0`. Shift the 64-word window two positions to the left. This discards active position 1 and adds forced active position 64, which becomes new index 62. Every other active old index shifts by -2; the resulting support is **exactly support 14**. Thus the existing unconditional exclusion of support 14 would already imply the exclusion of support 3 for true schedules, independently of repeating its sigma-chain contradiction. This is a check on the time-window reasoning, not a newly excluded pattern. Neither direction is assumed reversible.

## 5. Independently replayable checks and limitations

Run `python -B check.py --save`. This checker reads exactly the pinned 15-pattern file, and checks:

1. All seven source-target translations and the empty predecessor intersections at `t=64..66`, without treating a nonempty intersection as automatic contradiction.
2. All three backward shared-prefix recurrences, from the actual backward formula.
3. The exact six-element representative cover of the thirteen nonexcluded v2 patterns.
4. The time-shift identity against 15 pairs of unrelated 32-bit standard schedules (45 shift checks), plus five negative controls: added active position 57 in a left-shift source, added position 15 in a backward source, altered active position 59 at a three-step forward boundary, added position 11 affecting backward t13, and active position 57 spoiling the new `0 -> 9` tail. A deliberately damaged actual post-64 schedule also fails the window-identity check.

The checker is a **finite audit aid** to the symbolic proof, not an independent-agent mathematical review, a new proof of all v2 supports, a Lean compilation, or a full 13-word witness. Its bit-for-bit output is frozen as `RESULTS.json`; `manifest.json` pins the checker, statement and data.

## 6. Research implications and attribution

This reduction is grounded in the original nonlinear SHA-256 schedule, **not** a linearized schedule or random-message heuristic. It is a structural *equivalence/implication between possible true supports* and therefore reduces a proof-by-cases task from 13 remaining supports to six representatives. It does not reduce the numeric lower bound or guarantee a witness. Time-translation of an autonomous recurrence is elementary mathematical prior knowledge; **no independent historical originality claim** is made for that principle. The contribution of this candidate is its verified application to the frozen complete 13-support list, including the forward tail and backward input boundaries. No external publication or human peer review is asserted.
