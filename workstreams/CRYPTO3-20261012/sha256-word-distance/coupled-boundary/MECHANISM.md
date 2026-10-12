# Proof-producing test of the sigma0-coupled low-12 boundary

Before computation: test the exact fixed-mask word system below with a
transparent gate-level CNF and a solver-produced DRUP proof. A solver's
UNSAT answer alone is not a result. The CNF must be reconstructed from
the standard operations and every proof addition independently checked
by reverse unit propagation before any exclusion is claimed.

Let K=0xfbca7000, q'=q XOR K, f=sigma0 and g=sigma1. The arbitrary
32-bit words q,p,p' must satisfy these modular equalities:

```
q+g(q) = q'+g(q')
p'+q = p+q'
f(p')+f(q') = f(p)+f(q)
```

The second equality says p'-p=q'-q; the third says their sigma0
derivatives are opposite. K is not an assumed arbitrary nonzero
difference: the separate complete low-12 h-collision mask lemma proves
this exact XOR mask when the common additive difference is divisible
by 4096. All three q,p,p' words retain all 32 unconstrained bits.

This is a small exact boundary obligation, not a complete schedule
solver or a repeated free-difference tail query. Its usefulness would
be to couple two neighbouring active pairs back to the same original
sigma definitions. Support bridges and every legal boundary still
require separate derivation. No complete support exclusion is implied.

The solver receives a finite conflict budget. Unknown or timeout is
recorded as a failed proof attempt, never as an impossibility proof.
