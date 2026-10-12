# Independent AI review of support12-base-lift-v8

**ACCEPT, exact frozen author version.**  The author package with manifest
SHA256
`374732f8fee671cd7290d7596ab7f0cb85bb83502b3c94a124d7a78280802dc6`
proves an exact base interpolation bijection for the thirteen prescribed
first-word coordinates of frozen support 12.  It does not prove that its two
residual equations have a common zero.

## Independence and comparison

Before any author file was read, this reviewer independently derived and
hash-froze a different coordinate chart:

| object | blind independent chart | author chart |
|---|---|---|
| five anchors | `{21,22,23,24,32}` | `{9,12,14,19,22}` |
| solved original rows | 46, all distinct | 46, all distinct |
| solved coordinates | 46, all distinct | 46, all distinct |
| residual rows | `{33,57}` | `{33,57}` |

The blind freeze is `PRE-AUTHOR-FREEZE.json`.  Its own checker exhausts all
272,052 inactive anchor sets of sizes zero through four and finds no complete
single-row reversible propagation.  It then verifies its separate
five-anchor chart, four genuine single-schedule roundtrips, all inverse-map
compositions, and four damage controls.

After the freeze, `compare_author.py` checked every author file against the
manifest and independently rescanned the five-anchor sets in lexicographic
order.  The author's anchor set is exactly the first success, at trial
1,498,469.  The lower-size author counts agree with the blind exhaustive
calculation: 20,825 triples and 249,900 quadruples.

The author order was checked step by step against the five coordinates of
each original recurrence.  Every target is the only coordinate not yet
known.  Its 46 row indices and 46 targets are pairwise distinct.  The author
step types are 21 output identities, 9 lag-16 identities, 2 lag-7 identities,
2 sigma0 inversions and 12 sigma1 inversions.  The complementary rows are
exactly 33 and 57.

## Permutations and evaluator

The reviewer reconstructed the two small-sigma binary matrices directly
from their FIPS bit definitions.  Both have rank 32.  The author and reviewer
inverse columns agree exactly; 128 left/right standard-basis compositions
pass.  Therefore every displayed reverse step has a unique 32-bit solution,
including the steps through sigma0 and sigma1.

Four cross-implementation schedules reconstruct identically with the author
and independent evaluators.  The author's own verifier was rerun and matched
its frozen JSON exactly: all sixteen schedule roundtrips pass.  Its damage of
active coordinate 10 preserves the 46 construction rows and makes both
residuals nonzero; damage to constructed coordinate 31 violates used rows.
The independent controls additionally reject a wrong solve target, an
omitted residual, an altered inverse column and an altered fixed roundtrip
coordinate.

## Accepted theorem and proof boundary

Let

```
S = {10,11,13,15,18,20,26,28,29,34,42,43,57},
P = {9,12,14,19,22}.
```

For arbitrary prescribed values `u` on `S` and parameters `p` on `P`, the
author elimination uniquely constructs a 64-word vector satisfying 46
original SHA-256 message-schedule rows.  This vector is a genuine expanded
schedule iff its exact original residuals at rows 33 and 57 both vanish.
Conversely, any genuine schedule with `S`-projection `u` is recovered by
taking `p` to be its `P`-projection and reversing the same unique steps.
Projection and construction are therefore inverse maps.

The anchor minimality statement is accepted only inside the explicitly
enumerated class: start with the thirteen `S` coordinates plus inactive free
anchors, then repeatedly solve one original recurrence having exactly one
unknown through an identity, sigma0, or sigma1 occurrence.  It is not a
minimality theorem for arbitrary nonlinear elimination or auxiliary
coordinate systems.

This acceptance does **not** establish residual solvability, compatible
second active endpoints, all thirteen actual active pairs, a full pair of
messages, distance-13 attainability, a lower bound of 14, Lean certification,
or human review.  Five word parameters against two word equations is a
coordinate description, not a counting or surjectivity proof.

## Replay

From the repository root, using only Python's standard library:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-review-v8/replay_readonly.py
```

The replay checks the blind freeze and both manifests, reruns the independent
minimality/roundtrip/controls, and repeats the exact author comparison without
modifying either frozen directory.
