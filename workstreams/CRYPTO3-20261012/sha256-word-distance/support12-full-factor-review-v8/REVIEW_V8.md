# Independent review of author support12-full-factor-v8

**REJECT for the claimed support-12 object.**  The author package is
internally self-consistent, but it factors the wrong support.

The hash-frozen source `supports-v2.json` contains

```
supports[12] = {10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

The author proof, certificate, builder and checker instead use

```
{10,11,15,18,20,26,27,28,29,34,42,43,57} = supports[11].
```

The certificate nevertheless labels this object `support_index: 12`, and
the author checker verifies `source_data["supports"][11] == ACTIVE`.  This is
an off-by-one target-binding error, not a notation-only difference: position
13 is missing and position 27 is spurious.

## Exact consequences

Seven of the 48 substituted rows differ, at

```
t = 20,27,28,29,34,42,43.
```

For example, the true row 20 is `d20-G18-d13`, whereas author v8 has
`d20-G18`; the true row 28 contains `-F13`, while author v8 instead obtains
later terms involving the spurious position 27.  The author's thirteen
joint factors therefore omit the required factor 13 and include factor 27.

The following numerical properties happen to survive the support swap and
cannot identify the error:

- both substitutions have 25 nonzero and 23 identically zero rows, at the
  same row times;
- the author's wrong matrix still has unit-pivot rank 25 and free rank 14;
- the author's six negative controls all reject their intended mutations.

Those controls only compare a payload to the same hard-coded wrong `ACTIVE`
list.  None binds the claimed index 12 to `supports[12]`.

For the true support, the independently frozen pre-author derivation in this
review directory has four boundary-private coordinates
`G10,G11,G13,F57`, not the author's three `G10,G11,F57`.  Their existential
elimination leaves ten shared scalars, not eleven.  Consequently the author
factor graph and its composite nonzero conditions are statements about the
index-11 support and do not review or contradict the true-support formulas.

## Reproduction

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/check_independent.py --negative
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/compare_author_v8.py
```

The comparison first verifies every author manifest member and the exact
announced hashes, replays the author checker with all six negative controls,
then reconstructs both 48-row systems directly.  Its expected final status
is `REJECT`.

This rejection is narrow: it does not claim that v8 is internally invalid
as a factorization of `supports[11]`.  It says v8 supplies no proof about the
true support index 12 requested here.  The correct blind derivation remains
frozen and awaits comparison with a newly corrected author object.

