# Conditional Lean kernel for the uniform-younger 5/4 proof

**Status: the finite scalar induction and its arithmetic are Lean-verified;
the complete randomized ROB theorem is not yet Lean-verified.**

`UniformYoungerPotential.lean` checks the joint-potential argument in
`subagents/theory/RANDOMIZED_FIVE_QUARTERS.md`, theory commit
`9199c455925b65cfd609955ded7d39279b6d6011`. It imports bundled Std only.
Its ten printed declaration audits contain only `propext` and `Quot.sound`.
No final potential inequality is assumed.

## Integer scaling and index convention

The formal module uses **remaining length** `n`, reversing the written
clear-prefix index: written suffix `i` becomes `n=N-i+1`. Let `s>0` be a
common integer scale, `f(n)=s F_i`, and `e(n)=s E_i`. The integer potential is

`k(n)=3 f(n)+s n-4 e(n)`.

The module does not build a probability space or prove the existence of this
common scale for the actual policy; those are part of the remaining bridge.
The finite induction requires local equations only for `1<=n<=limit` and
requires `k(0)=0`. It makes no assumption about values above the fixed program
length.

## What is actually proved

`joint_invariant` proves simultaneously for every `n<=limit`:

1. `k(n)>=0`.
2. If `n>0` and `f(n)=f(n-1)`, then `k(n)+k(n-1)>=s`.

The nonempty condition in statement 2 is present in the formal statement.
The exceptional length-three/equal-tail case uses statement 2 at the
**strictly smaller** length `n-2` to establish statement 1 at `n`. The other
half of the induction then uses the explicit successor identities below;
it does not assume its own conclusion.

`scaled_expected_bound` concludes `4 e(n)<=s n+3 f(n)` from the verified
joint induction. `scaled_five_quarters` additionally assumes the separate
width-two work bound `s n<=2 f(n)` and concludes `4 e(n)<=5 f(n)`.

The arithmetic helpers verify every row of the written potential table
from the actual minimum/mean recurrences: a general forced-macro identity
and all five randomized cases `(ell,x)=(3,0),(3,1),(4,0),(4,1),(4,2)`.
The formal equalities multiply averages by two and never use approximate
arithmetic, external numerical decision procedures, or finite testing as a
replacement for induction.

## Exact abstract interface and remaining gap

`MacroShape` states that each positive suffix has one of nine forms:

| Case | Required potential identity |
| --- | --- |
| Forced singleton | `k(n)=k(n-1)` and `f(n)=s+f(n-1)` |
| Forced pair | `k(n)=s+k(n-2)` |
| Forced length three | `k(n)=s+k(n-3)` |
| Forced length four | `k(n)=2s+k(n-4)` |
| Choice `(3,0)` | `2k(n)=k(n-2)+k(n-3)-s` |
| Choice `(3,1)` | `2k(n)=k(n-2)+k(n-3)+2s` |
| Choice `(4,0)` | `2k(n)=k(n-2)+k(n-4)` |
| Choice `(4,1)` | `2k(n)=k(n-2)+k(n-4)+3s` |
| Choice `(4,2)` | `2k(n)=k(n-2)+k(n-4)` |

Every constructor includes the corresponding minimum remaining-length guard.
Case `(3,0)` also includes `f(n-2)=f(n-3)`.

The three difficult cases additionally require the precise structural
successor equations established in the written graph proof:

- `(3,0)` and `(4,2)` require `k(n-1)=s+k(n-3)`.
- `(4,0)` requires that same equation, or
  `2k(n-1)=k(n-3)+k(n-5)+3s` with **n>=6**.

These are equations for subsequent forced or good randomized macro-actions,
not assumptions of the target inequalities. Their presence is nevertheless
a real interface condition. The Lean file does **not** prove that every
actual ROB program supplies `MacroShape`; the oldest-inclusive normalization,
the exact scalar scheduling recurrence, classification of tail differences,
and the graph/readiness arguments yielding the three successor equations
remain written proofs. The arithmetic helpers validate the equations once
those scalar hypotheses have been supplied.

In particular this file does not certify the full randomized algorithm,
its expectation semantics, the oblivious-adversary lower bound, or the
global minimax-ratio equality. It validates a nontrivial conditional proof
kernel and all local potential arithmetic. Historical novelty remains under
the separate literature review.

## Reproduction

```sh
python workstreams/ILP1-20261014/formal/verify_uniform_potential.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-uniform-potential-independent
```

Omit the optional compatibility flag on ordinary hosts. It only addresses
the same-process executable-path lookup documented in `README.md`.
Fresh author-run hashes, timing, compiler information, and axiom dependencies
are preserved at `subagents/lean/evidence/uniform-younger-potential/`.
