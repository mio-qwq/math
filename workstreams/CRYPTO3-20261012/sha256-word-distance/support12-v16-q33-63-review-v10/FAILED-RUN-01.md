# Failed comparison run 01

The first post-author comparison required exact equality of the recovered word
fixtures and stopped at `q=37` with:

```text
RuntimeError: q=37: exact recovered fixtures disagree
```

This was an invalid comparison requirement, not a theorem failure.  The author
and independent checkers use different GF(2) pivot/free-variable conventions,
so they may choose different actual points from the same surviving affine
leaf.  Direct recomputation showed that both sets are genuine fixtures.  The
repaired comparison checks all actual arithmetic independently and compares
the stable `(xor_x,xor_y)` leaf-signature sets.  It also reports, but does not
require, exact word-fixture coincidence.
