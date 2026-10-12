# Preregistered frozen-run mechanism

This directory studies only the actual-base completion problem for frozen
support 12.  It neither searches for an active-pair witness nor treats a
parameter count as a solvability argument.

The active schedule coordinates are

```
S = {10,11,13,15,18,20,26,28,29,34,42,43,57}.
```

For a set of additional inactive coordinate anchors `P`, start with `S union
P` known.  Repeatedly use an unused SHA-256 recurrence having exactly one
unknown coordinate.  Its identity terms are solved by subtraction; an
unknown small-sigma input is solved with the exact inverse binary linear
map.  This is a coordinate-only search: no word value, message pair, support
assignment, SAT model or probability model is enumerated.

The frozen run has the following finite budget:

1. exhaust all anchor sets of sizes 3 and 4;
2. scan size-5 sets in lexicographic order, stopping at the first complete
   elimination or after 1,600,000 trials;
3. never examine six or more anchors in this stage.

A size-`p` completion necessarily uses `51-p` of the 48 original equations
and leaves `p-3` exact residual equations.  Failure at sizes 3 and 4 rules
out only this single-equation peeling mechanism at those anchor counts.  It
does not disprove base completion or projection surjectivity.  A success at
size 5 must be frozen as the full equation/target order and then checked by
a separate definition-based evaluator before any theorem is claimed.

The preliminary structural pilot identified a size-5 success within this
budget.  The evidence-producing run starts afresh from the frozen source and
records the exhaustive lower-size counts, first success and source hash.

