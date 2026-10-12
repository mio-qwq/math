# Mechanism

This stage uses only exact integer row operations and direct definitions.
It runs no solver and has no timeout.

The generator reconstructs all 48 schedule-difference rows from the four
lags `(2,7,15,16)` and the independently bound support-index-12 active set.
It obtains 25 unit pivots using 53 swaps, sign changes and integral row
additions.  The definition checker reconstructs the rows without importing
the generator, checks the normal form, reverses all operations, verifies the
four private versus ten shared parameters, and checks that both small sigma
maps have binary rank 32.

The six controls damage the exact failure-prone surfaces: zero-based target
index, the `13/27` distinction, true row 20, one row operation, one normal
form coefficient, and an independently supplied target binding.

Run from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-v9/build_certificate.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-full-factor-v9/check.py --negative
```

The checker uses only Python's standard library and imports no generator
code.

