# All-integer scope of the conservative shift oracle

This is a supplementary scope result discovered after the original
independent eleven-map check. It changes no accepted support map and
does not reduce the six representatives.

The independently specified oracle assigns each word-pair position one
of zero, nonzero, or unknown. Original frozen-support positions are
zero or nonzero. A new boundary is zero if all four predecessor pairs
are zero, nonzero if exactly one is nonzero and the rest are zero, and
unknown whenever an unknown predecessor or at least two nonzero
predecessors occur. The rank-32 sigma certificates justify the single
transformed nonzero term.

For every one of the fifteen supports, in both directions, a block of
sixteen consecutive unknown positions occurs after at most 63 extension
steps. `ABSORPTION_RUN.json` records the earliest such block and all its
positions; `check_absorption.py` independently recomputes these thirty
finite witnesses with reviewer-owned code.

For forward extension, suppose positions a,...,a+15 are all unknown.
The next index a+16 uses a+14,a+9,a+1,a, which are all unknown; therefore
it is unknown. Repeat by induction. For backward extension, suppose
positions a,...,a+15 are all unknown. At j=a-1 the inverse recurrence
uses a+15,a+13,a+8,a, which are all unknown; hence j is unknown. Repeat
backwards. Thus unknown is absorbing after sixteen consecutive unknowns.

Every subsequent translated 64-word window contains a newly created
unknown boundary position. It cannot be certified equal to one of the
fifteen exact supports by this oracle. Combined with the original
search over offsets -63 through 63, the 24 accepted maps are therefore
all safe source-to-target maps for this oracle at **any integer offset**.

This is completeness of a deliberately conservative proof mechanism.
It is not completeness of mathematical time-translation reductions:
the oracle discards relations between multiple active terms, carries,
and original recurrence constraints. Those could prove further boundary
equalities or inequalities. No impossibility result for such stronger
mechanisms is asserted.

Read-only replay from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/shift-review-v4/check_absorption.py
```

No output file is written unless `--output` is explicitly supplied.
