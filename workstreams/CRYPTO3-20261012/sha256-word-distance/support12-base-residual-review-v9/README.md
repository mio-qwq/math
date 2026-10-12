# Support-12 base-residual v9 review

This directory contains a blind derivation frozen before author contact and
an exact-byte independent acceptance of `support12-base-residual-v9`.

Run from the repository root:

```
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-residual-review-v9/check_independent.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-base-residual-review-v9/compare_author.py
```

The result is a coordinate reduction only.  It asserts neither residual
solvability nor a message pair.
