# Precommit: strengthen one q=5 twin survivor

Use the lexicographically first frozen q=5 twin fixture:

```text
D=00050000, A=40406e02, c=1ff8913e, T=c+D=1ffd913e.
```

Run at most two independent QF_BV SAT queries, each with a 30-second
timeout and no retry:

1. Find a forward-D actual pair whose joint derivative is `(-A,-T)`.
   Its reversal would be the third `-D` pair in the accepted v7 selected
   three-pair criterion.
2. Find a forward-A actual pair whose sigma0 derivative is D.  Its
   reversal would supply the reciprocal edge.

Only a SAT model directly rechecked by a standard-library verifier counts
as positive evidence.  `unknown` stops, and `unsat` without a checkable
certificate is recorded only as an observation.  Even two positive models
would establish only the selected four-pair local system, not all 48 rows,
base completion, or a message pair.

