# Pre-author independent freeze

This review was completed through the independent run below before reading
the author's `CERTIFICATE.json`, `check.py`, `search_survivors.py`, or
`ALL-SURVIVORS-PRECOMMIT.md`.  The only author-side v9 input read in advance
was `PRECOMMIT.md`.  The accepted v8 fixed-`D=2^16` author proof and independent
review were also read as the established input theorem and a regression target.

## Independent method

`check_independent.py` imports no author code or certificate.  It constructs
both SHA-256 small-sigma maps from direct rotations and shifts and reconstructs
their 32 output-bit linear rows by basis evaluation.  For each odd
`q=1,3,...,31`, it exhaustively assigns all 65,536 upper-half inputs to the
mask `u xor (u+q mod 2^16)`, regenerates every resulting class from its fixed
coordinate equations, and checks disjoint coverage.  The two lower halves are
left as 32 free Boolean coordinates, so every ordered `(x,y)` lies in exactly
one traversed class pair.

For each class pair the checker expands the modular difference equations one
bit at a time with an explicit signed incoming integer carry.  Every at-most-
two-variable truth table is enumerated and then checked to be exactly recovered
by its affine parity equations.  A separately written highest-pivot GF(2)
eliminator verifies every contradiction receipt algebraically.  Every surviving
leaf is converted to actual 32-bit words and checked by direct small-sigma
evaluation.

## Frozen result

The tuple in the last column is `(input classes, sigma0 leaves, full twin
leaves)`.

| odd q | result |
|---:|---:|
| 1 | `(16, 414, 0)` |
| 3 | `(29, 3123, 0)` |
| 5 | `(41, 3495, 3)` |
| 7 | `(40, 2310, 0)` |
| 9 | `(51, 3277, 0)` |
| 11 | `(63, 10057, 0)` |
| 13 | `(62, 10054, 2)` |
| 15 | `(49, 2345, 4)` |
| 17 | `(59, 3983, 0)` |
| 19 | `(82, 31014, 0)` |
| 21 | `(93, 33495, 4)` |
| 23 | `(81, 28467, 2)` |
| 25 | `(80, 28634, 2)` |
| 27 | `(91, 47541, 4)` |
| 29 | `(79, 45225, 0)` |
| 31 | `(56, 9874, 0)` |

Thus the independently predicted excluded positive residues are
`q={1,3,7,9,11,17,19,29,31}`.  Full survivors occur for
`q={5,13,15,21,23,25,27}`.  There are 21 surviving affine leaves in all;
one directly verified word representative is stored for every leaf in
`PRE_AUTHOR_RUN.json`.

For every q the separate 31-bit run returned exactly the same twin-leaf count
as the full 32-bit run.  Hence this bounded classification has no case whose
only obstruction is bit 31; the accepted q=1 bit-30 obstruction remains a
regression match (`414 -> 0`).  All 21 full representatives were also checked
after reversing both directed pairs, which realizes the corresponding negative
orientation.  Mutating each of six fields in each representative gave 126/126
rejections.

## Frozen execution

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-review-v9/check_independent.py
```

The run took 461.37 seconds under CPython 3.12.14.  An earlier wrapper attempt
failed before execution because `/usr/bin/time` is not installed; its exact
diagnostic is retained in `PRE_AUTHOR_CONSOLE.txt`.  It did not produce or
alter the classified result.

Frozen SHA-256 values:

```text
check_independent.py  938cc2a2bebfce6537fb19663c959f274e44a8c21f74d6de3980e80f0d247d42
PRE_AUTHOR_RUN.json   0e1f4637e56fa86312cc003bf2d288f57dcd87dc66357d399c7cfa06ca6252b6
```

## Scope

This is an exact bounded classification of the selected **two-pair twin local
condition** only.  A survivor is an actual pair of actual word pairs, but is not
the third joint-image pair, reciprocal edge, full support-12 assignment, or a
16-word message pair.  An excluded q excludes only that fixed residue and its
pair-reversed negative orientation.  Nothing here proves distance at least 14.

