# Independent review: odd q=33..63 valuation-16 twin classification

## Decision

**ACCEPT**, with the narrow scope stated below.

For every odd `q` in the exact interval `33..63`, let `D=q*2^16`.  The author
package completely classifies the bounded selected twin condition

```text
F_D(x)=F_D(y),  G_D(y)-G_D(x)=2D  (mod 2^32).
```

The independently accepted positive-q classification is:

| q | input classes | F leaves | twin leaves |
|---:|---:|---:|---:|
| 33 | 65 | 11,317 | 0 |
| 35 | 97 | 54,829 | 0 |
| 37 | 118 | 59,524 | 4 |
| 39 | 107 | 49,761 | 2 |
| 41 | 117 | 50,677 | 2 |
| 43 | 138 | 68,938 | 4 |
| 45 | 127 | 64,609 | 0 |
| 47 | 95 | 16,817 | 0 |
| 49 | 94 | 16,934 | 0 |
| 51 | 125 | 55,589 | 0 |
| 53 | 135 | 60,083 | 0 |
| 55 | 114 | 45,998 | 0 |
| 57 | 103 | 45,295 | 0 |
| 59 | 113 | 44,273 | 0 |
| 61 | 92 | 39,578 | 0 |
| 63 | 61 | 12,035 | 0 |

Thus the local twin condition is excluded for positive
`q={33,35,45,47,49,51,53,55,57,59,61,63}`.  It survives for
`q={37,39,41,43}` with respectively `4,2,2,4` affine leaves.  Reversal of
both directed pairs gives the same result for the corresponding negative
residues.

## Independence and exact cover

Before opening any author-v10 file, the reviewer wrote and hashed
`check_independent.py` (`b9ce55525c1c7def35fcd588179a62a8931359665a31e3b67b4b68cf170d0de0`).
It imports no author-v10 code or certificate.  Starting only from the frozen
v9 definitions, it independently:

1. reconstructed both SHA-256 small-sigma linear maps by basis evaluation;
2. exhaustively partitioned all 65,536 upper words for each of the sixteen q;
3. regenerated every addition-XOR class from its fixed-coordinate equations;
4. covered every ordered class pair, leaving both lower halves free;
5. propagated all 32 bits of both modular derivative equations with explicit
   integer carries and checked GF(2) contradiction receipts; and
6. recovered and directly evaluated an actual word fixture for every surviving
   affine leaf.

The full independent run took 515.52 seconds and produced 12 actual fixtures.
All 12 negative-orientation reversals passed, and all 96 one-field fixture
damages were rejected.

## Author comparison and replay

All sixteen author cases agree with the independent run on the exact q range,
input-class count, class-size histogram, sigma0 leaf count and full twin-leaf
count.  Both implementations find the same twelve `(xor_x,xor_y)` leaf
signatures.  Their chosen word representatives differ because their GF(2)
pivot/free-variable conventions differ; all 24 representatives (12 author and
12 independent) were directly checked as genuine full-word local fixtures.
This expected distinction is recorded in `FAILED-RUN-01.md` rather than hidden.

The four-file author SHA-256 manifest passed.  The author checker was then
replayed with four workers and negative controls in 124.00 seconds; it matched
the frozen certificate and rejected all 48 author fixture-field mutations.
The frozen v9 dependency hash also matched
`a58fc79b82edce8c82d8838a0d197bdd77b9dc42a4d91c4250b0d3ae4d6d1d60`.

## Exact scope

This acceptance is an exact finite proof for the selected **two-pair local
twin condition** and its pair-reversed negative orientation only.  A surviving
fixture is made of real 32-bit words, but it is not a third joint-image pair,
complete support-12 assignment, or 16-word SHA-256 message pair.  The separate
three-pair package mentioned by the author was not reviewed here.  Nothing in
this review proves distance 13 reachable, proves distance at least 14, or
constitutes Lean formalization.

## Replay

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-q33-63-review-v10/check_independent.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-q33-63-review-v10/compare_author.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-q33-63-v10/check.py --jobs 4 --negative
```
