# Independent reconstruction before reading the proposed projection proof

This reconstruction was started from the SHA-256 recurrence and the
specified sets S, P, T, before reading `base-lift/PROJECTION.md` or its
implementation. It is an independent review of that result; the reviewer
did not participate in its discovery. No claim of external human review
is intended.

All words lie in R=Z/(2^32). Bit zero is the least significant bit.
The recurrence is

```
W[t] - sigma1(W[t-2]) - W[t-7] - sigma0(W[t-15]) - W[t-16] = 0,
16 <= t < 64.
```

The initial interpolation coordinates are

```
S = {2,9,10,16,23,24,30,37,38,44,51,52,58}
P = {0,1,3,4,5,7,8,11,12,15,29,43,57}.
```

## Reconstructing a coordinate chart

Start with K=S union P and reserve the specified residual set
T={28,29,35,36,42,43,49,50,56,57}. Repeatedly select an as-yet-unused recurrence
outside T
whose five positions contain exactly one coordinate outside K. Solve
for that coordinate using addition/subtraction and, when needed, the
inverse of sigma0 or sigma1. Both inverses are rebuilt from the original
output-bit matrices by F2 Gaussian elimination and checked on every
basis vector. Record the exact equation and solved coordinate, and add
that coordinate to K. Choosing the lowest-index eligible equation is a
reviewer implementation choice, not supplied author data. An initial
unrestricted lowest-index closure covered all 64 coordinates but selected
a different equation complement. That is not a mathematical refutation
of the requested chart: different elimination orders can reserve different
residual sets. The failed initial check and precise correction are recorded
in `INDEPENDENT-FIRST-RUN.json` before the author's files were inspected.

If this produces 38 assignments covering every coordinate, any assignment
to S union P has a unique completion satisfying those selected 38
equations. The remaining ten equations are then exact residuals. A
completion is a genuine SHA-256 expansion precisely when every residual
vanishes. This statement does not assert that every assignment to S is
attainable or that the residual equations always have a solution in P.

## Independently reconstructed lifting argument

At every i in S let a_i,b_i be a specified word pair; outside S define
all difference quantities to be zero. Assume each pair is active and
the 48 exact modular difference equations hold, with sigma differences
computed from a_i,b_i. If W is a genuine expansion with W_i=a_i on S,
define W'_i=b_i on S and W'_i=W_i outside S. The difference between
each proposed W' recurrence and the valid W recurrence is exactly the
corresponding assumed difference equation. Thus W' is also a genuine
expansion, and its exact differing support is S. Conversely every such
expanded pair supplies this interpolating W. For any fixed W, the
corresponding W' is uniquely determined.

The nonzero pair assumption is necessary only to assert exact support S;
without it the same argument gives support contained in S. No IV, block
padding, zero base message, probabilistic model or compression function
assumption appears.
