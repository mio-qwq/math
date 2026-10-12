# Independent review of support12-base-residual-v9

**ACCEPT, exact frozen author version.**  The author package with manifest
SHA-256 `cbdfa2fd8d76c4e7bc511f10c30d15b43763144dfd1eac6fff758e1d5ee6546f`
correctly eliminates base residual row 57 and correctly replaces the local
projected factor at active position 57 by a derivative evaluated at the
base value forced by the completion chart.

## Independent freeze and dependency result

Before reading the author directory, this reviewer froze a separate
incidence derivation and checker.  In the accepted 46-row chart, prescribed
`u57` affects exactly coordinates

```
57, 59, 61, 63.
```

It does not affect `C0,...,C56` or `R33`.  All right-side coordinates of
row 57 are independent of it, so

```
R57 = u57 - H,
H = g(C55) + C50 + f(C42) + C41              (mod 2^32).
```

The coefficient of `u57` is the unit 1.  Hence row 57 has the unique
solution `u57=H`.  Equivalently, omit 57 from the prescribed coordinates
and insert `(row 57,target 57)` after row 56 and before row 59.  The resulting
chart has seventeen inputs, 47 distinct solve rows and targets, and only
residual row 33.  Twelve genuine schedule roundtrips and twelve independent
replacement tests verify this rewrite and the exact identity for `R57`.

## Composition with the factor at 57

The corrected factor normal form has `d57=z`, `G57=b`, and the standalone
condition `PG(z,b)`, meaning that *some* first endpoint `x` realizes
`g(x+z)-g(x)=b`.  In the base-completed problem that endpoint is no longer
free: it is `H`.  The exact composed position-57 condition is therefore

```
g(H+z)-g(H)=b.
```

Standalone `PG(z,b)` remains necessary but is not sufficient for the exact
composition.  Both checkers include a definition-level separation control:
for `z=1`, `b=0x0000a000` has projected witness `x=0`, while evaluation at a
different forced base can give `0xffffa000`.  The private `F57` value is then
the actual `f(H+z)-f(H)` and is unused by schedule rows through 63.

This is consistent with the difference rows: row 57 uses `d57=F42`, and row
59 is the row that consumes the pointwise `G57=b` condition.

## Exact-byte and control checks

The six non-manifest author members have exactly the byte counts and hashes
recorded in `SHA256.json`; there are no extra non-cache files.  All three
accepted-input provenance hashes match the live accepted packages.  The
author checker reruns byte-for-byte to `CHECK.json`, covering 36 contexts,
five replacements per context, 64 row-57 pair identities, dependency
reconstruction, and the PG separation control.  The separate pre-author
checker also reruns byte-for-byte to its frozen receipt.  The accepted base
and corrected factor review replays pass unchanged.

## Acceptance boundary

Accepted only: the sink-coordinate identity, the unique row-57 solve, the
one-residual chart rewrite, and the exact pointwise endpoint merge.

Not accepted or inferred: solvability of residual row 33, solvability of the
pointwise position-57 condition together with the other twelve factors, any
thirteen-pair witness, a pair of message blocks, distance-13 attainability,
a distance-14 lower bound, Lean certification, or human review.
