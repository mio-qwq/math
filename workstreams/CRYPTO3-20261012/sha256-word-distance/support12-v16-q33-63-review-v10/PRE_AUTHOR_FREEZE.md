# Pre-author independent freeze

Before reading any file in `support12-v16-q33-63-v10/`, this review rebuilt
the bounded selected-twin classifier from the frozen v9 theorem definitions.
The independent checker imports no author-v10 source or certificate.

It reconstructs the SHA-256 `sigma0` and `sigma1` linear rows by basis
evaluation, exhaustively partitions all 65,536 upper words for every odd
`q=33,35,...,63`, verifies every mask class is exactly its coordinate cube,
and covers the Cartesian square of all classes.  It then imposes full 32-bit
modular derivative equations bit-by-bit using explicit integer carries and
checked GF(2) contradiction receipts.  Every surviving affine leaf is turned
into actual 32-bit word pairs and directly evaluated.

The checker additionally freezes the exact q range, reverses every actual
surviving fixture to test the negative orientation, and requires one-bit
damage in each recorded fixture field to be rejected.

Frozen source SHA-256 before author inspection:

```text
check_independent.py  b9ce55525c1c7def35fcd588179a62a8931359665a31e3b67b4b68cf170d0de0
```

This can establish only the exact bounded selected two-pair twin condition.
It cannot by itself establish a third joint-image pair, support-12 assignment,
16-word message pair, distance at least 14, or Lean formalization.
