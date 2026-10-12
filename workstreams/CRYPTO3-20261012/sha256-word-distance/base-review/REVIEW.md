# Independent review: exact SHA-256 base completion reduction

**Decision: accepted within the precise scope below.** No mathematical or
implementation correction is required for the two reviewed reductions.
This is independent review by an assistant agent that did not participate
in this candidate's discovery; it is not external human peer review and
is not Lean formalization.

## Exact versions reviewed

| Source | SHA256 |
| --- | --- |
| `base-lift/PROJECTION.md` | `436a80b20ae6d98a6d8a6b68248449ed047e212aaff8c9f6eb41a8ba73a76b9f` |
| `base-lift/base_completion.py` | `1215aa82a6abe196fe2396803a5a7565042e7862c35a434ed2be0b4bfc156955` |
| `base-lift/verify_completion.py` | `476d03768e5f79040186273a6384c87a453f167ac98875260c107db49d0aedc8` |
| Frozen CRYPTO2 `v2/supports.json` | `02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf` |

The frozen support file is from commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`, under
`workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance/`.
The reviewed support is index zero:

```
S = {2,9,10,16,23,24,30,37,38,44,51,52,58}.
```

All seven entries of the author's local manifest were hash-verified.
Hash verification of an exploratory file is not verification of the
mathematical result asserted by that file.

## 1. Independent reconstruction and review separation

Before reading the author's proof or code, the reviewer rebuilt the two
sigma output-bit matrices directly from ROTR7/ROTR18/SHR3 and
ROTR17/ROTR19/SHR10. Both inverse matrices were reconstructed by F2
row elimination and checked in both composition orders on all 32 basis
vectors: 128 basis-composition checks. These checks, together with
linearity of the displayed bit functions, establish the exact inverse
maps on all 32-bit words.

Starting solely from S, the specified parameter set P and residual set T,
the reviewer derived a different legal single-unknown elimination order.
It assigns 38 distinct new coordinates by 38 distinct original equations,
fills all 64 coordinates, and reserves exactly T. The reconstruction,
script and its hash checkpoint were saved before the author files were
read; see `PRE-AUTHOR-CHECKPOINT.json`.

The first unrestricted greedy order produced another valid 38-equation
chart with a different residual complement. Requiring the supplied T for
that unrestricted order was an error in the initial reviewer check, not
in the candidate. Reserving T before choosing eligible equations gives
the requested chart. This distinction and the initial exit-1 record are
preserved in `INDEPENDENT-FIRST-RUN.json`.

## 2. Prescribed-pair lifting equivalence: accepted

For every i in S, prescribe unequal words a_i,b_i. Define d_i=b_i-a_i,
F_i=f(b_i)-f(a_i), G_i=g(b_i)-g(a_i), and define these three quantities to
be zero outside S. Suppose all 48 exact modular difference equations hold.

The reviewer independently obtains the same equivalence:

> These pairs are restrictions of a genuine pair of SHA-256 expanded
> messages with exact support S if and only if a genuine base expansion
> W exists with W_i=a_i for all i in S.

For the forward implication take the first expansion. For the reverse
implication, define W'_i=b_i on S and W'_i=W_i elsewhere. At every t,
subtracting the two full recurrence residuals gives exactly

```
d_t - G_(t-2) - d_(t-7) - F_(t-15) - d_(t-16).
```

That expression vanishes by hypothesis, while W's residual is zero.
Thus W' satisfies every original recurrence. Both sequences are exactly
the expansions of their first 16 words. All prescribed pairs are unequal,
so the differing support is precisely S, and the two input blocks differ
at positions 2, 9 and 10. For a given base W the second schedule W' is
uniquely determined.

The requirement that prescribed pairs are unequal is correctly present.
Without it, the same construction would only guarantee support contained
in S. No assumption about a zero base, padding, an IV, independent carries
or a random-message distribution is needed.

## 3. The 38-equation coordinate chart and ten residuals: accepted

The prescribed additional coordinates are disjoint from S:

```
P = {0,1,3,4,5,7,8,11,12,15,29,43,57}.
```

At each displayed author step, exactly four of the recurrence's five
coordinates have already been specified. The remaining coordinate appears
once, either through the identity, f or g, with coefficient +1 or -1.
These transformations are bijections, so that coordinate has exactly one
value satisfying the equation, for every assignment to the known words.
No division by a nonunit of Z/(2^32) is used.

Induction through all 38 steps proves, without relying on test cases,
that every assignment on S union P has a unique completion satisfying
the selected 38 equations. The remaining equations are exactly

```
T = {28,29,35,36,42,43,49,50,56,57}.
```

The same induction proves uniqueness even when a different legal order
uses those same 38 equations. Thus the reviewer's independently derived
completion and the author's completion are identical functions of all
26 anchors, not merely equal on the tested samples.

Fix the active-coordinate tuple u. Let C(u,p) be that unique completion.
Then C(u,p) is a genuine schedule exactly when the ten remaining original
residuals are zero. Conversely a genuine schedule projecting to u gives
p by restriction to P, and the elimination induction recovers the whole
schedule. Restriction and completion are inverse maps; distinct p remain
distinct because their P-coordinates are retained. This establishes the
claimed bijection between actual base schedules over u and zeroes of the
ten residual equations.

The ten displayed U/V/D/Q formulas were independently expanded back to
the original lag sets at t=28,29,…,56,57. Every coordinate in those formulas
is outside S. They are correct rewritings of the residuals. The proof also
correctly says these common-word values are functions of u,p, not separate
independent variables.

## 4. Definition-based code verification

`verify_independent.py` uses the independently written bit-matrix maps,
inverse matrices, elimination order and raw recurrence evaluator. It
loads the author's evaluator only after the pre-author checkpoint; it
does not import the author's verifier or discovery search.

Actual completed checks, recorded in `VERIFICATION.json` and `RUNS.json`:

| Check | Observed result |
| --- | --- |
| Author order against original coordinate dependencies | 38 valid assignments, exact T complement |
| Reviewer order against original dependencies | 38 valid assignments, same equation set, different order |
| Sigma maps and inverses against independently rebuilt basis maps | All checked basis images agree |
| Four independently chosen nonzero 16-word inputs | All 64 reconstructed words match; all 48 original equations vanish |
| Two arbitrary assignments to all 26 anchors | Both orders give identical completions; all 38 selected equations vanish; ten residuals equal the original remaining equations |
| Common-word formula substitutions | All ten agree exactly with the original recurrence |
| Direct paired-residual subtraction | All 48 identities agree for deliberate sparse replacements; the infeasible replacement is correctly not treated as a witness |
| Original author verifier replay | Exit 0; output equals the frozen author's `verification.json` |

The following seven malformed controls were rejected: a missing active
anchor, an out-of-range word, a Boolean value in place of an integer word,
an incorrect elimination target, an omitted residual equation, an incorrect
sigma0 rotation constant, and a tampered completed word. Separately,
altering active anchor 16 in a valid base keeps all 38 constructed equations
zero but makes the ten original residuals nonzero. This directly checks
that the completion evaluator does not silently claim every anchor choice
is a genuine schedule.

These examples test implementations and rejection behavior. The universal
theorems are justified by recurrence subtraction, sigma invertibility and
the elimination induction, not by the number of samples.

## 5. Scope of acceptance

The reviewed result is an exact reformulation retaining every actual base
equation. It identifies precisely where a pure independent-active-pair
model needs a real-base interpolation solution.

This review does **not** establish that the projection onto S is onto,
that every independent-pair solution lifts, that the ten residuals are
independent, or that every active tuple has any completion. It proves no
fiber size or success probability. It supplies no actual distance-13 pair,
distance-14 lower bound, cryptanalytic attack, novelty claim, solver speedup
or Lean formalization.

The separate 20,825 three-anchor enumeration was neither rerun nor accepted
as part of this review. Its code and recorded output were hash-verified
only. The full v1/v2 certificate chains and equality-support classification
are also outside this narrow review; the exact frozen S0 is used as data.

No required revision was found for the two stated reductions or their
displayed common-word residual rewritings. Acceptance applies only to the
hash-pinned versions above.
