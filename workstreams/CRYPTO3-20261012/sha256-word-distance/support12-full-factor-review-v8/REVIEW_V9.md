# Independent acceptance of corrected support12-full-factor-v9

**ACCEPT, exact frozen v9 version.**  The author v9 package correctly
factors the true zero-based support identifier 12 at the
independent-active-pair layer.  This acceptance supersedes no part of the
preserved v8 rejection: v8 remains a useful immutable failure record for
the wrong `supports[11]` object.

## Target and row system

The accepted target is exactly

```
supports[12]={10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

V9 binds that set to the frozen support source, the accepted actual-boundary
proof, and the base-lift structural artifact.  Its checker explicitly
requires zero-based index 12 and rejects both an index-11 binding and the
replacement `13 -> 27` that caused v8 to fail.

The independent comparison reconstructs every one of the 48 SHA-256
difference rows from the support and lags `(2,7,15,16)`.  All 48 equal the
v9 certificate byte-for-structure.  There are 25 nonzero rows and 23
identically zero rows.  V9's 53 integer unit row operations replay and
reverse exactly, proving rank 25 and free rank 14 over the integers and
hence over `Z/(2^32)` without field division or hidden 2-power torsion.

## Equality with the blind normal form

The pre-author blind proof used parameters

```
a,b,c,e,p,q,r,s,u,v,z10,z11,z13,z57.
```

V9 chooses different free coordinates.  Their exact change of basis into
the blind coordinates is

```
d10=-a, d11=b, d13=-e, d15=-u,
F11=a-c, F13=-p-q-r,
G10=z10, G11=z11, G13=z13,
F15=-s, G26=p, F29=q, F42=v, F57=z57.
```

After this substitution, the independent checker compares all 39
`d_i,F_i,G_i` coordinate forms.  Every coefficient is identical.  Thus the
author table is not merely rank-compatible with the blind result; it is the
same integral solution module in a different basis.

## Exact factor theorem

Both derivations give thirteen actual-pair factors:

- nine retain the full joint `(d,F,G)` relation from one actual word pair;
- positions 10, 11 and 13 use the exact `(d,F)` projection;
- position 57 uses the exact `(d,G)` projection.

The four private coordinates are exactly `G10,G11,G13,F57`.  Existentially
absorbing them leaves ten shared scalars and a connected thirteen-factor
graph.  The seven distinct active-difference conditions in v9,

```
a,b,c,k,p+a,q+s,z != 0,
```

map exactly, up to signs, to the blind conditions

```
a,b,c,e,u,q+r,v != 0.
```

No `F` and `G` values from different word pairs are combined.  Independent
direct GF(2) calculations give rank 32 for each SHA-256 small sigma, so an
unequal input pair also has nonzero `F` and `G`; those consequences do not
need extra support assumptions.

## Controls and preserved failure

All nine v9 manifest members match their recorded hashes.  The author
checker passes and rejects all six damaged controls, including recurrence
of the v8 off-by-one binding and deletion of the true row-20 `d13` term.
The rejected v8 manifest remains byte-identical at
`02a3729a66b7e474eb2abfeb33920160e2d60386f324ab5d4ef1b5c1e2bc0814`.

Reproduce the independent gates from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/check_independent.py --negative
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/compare_author_v8.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-review-v8/compare_author_v9.py
```

The expected statuses are respectively `PASS`, `REJECT`, and `ACCEPT`.

## Acceptance boundary

Accepted: a complete written proof, independently reconstructed and
machine-replayed, of the exact thirteen-factor criterion for independent
actual word pairs on support 12.

Not accepted or claimed: feasibility of those thirteen factors, a set of
actual pair witnesses, completion to two common 16-word base messages, a
distance-13 SHA-256 message-expansion pair, a distance-at-least-14 proof,
Lean formalization, or external human review.

