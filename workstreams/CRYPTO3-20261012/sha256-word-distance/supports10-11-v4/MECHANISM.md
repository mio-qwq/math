# Supports 10 and 11: a new two-pair core

This directory is owned by the independent supports-10/11 research agent.
No frozen source is edited. The actual 32-bit SHA-256 schedule is the object,
with arbitrary base messages and all 64 word positions counted.

Before the first new calculation, direct recurrence substitution yields the
following necessary core. Let `X` be the actual pair at index 18 and `Y`
the pair at index 26, and put `A=d(X)`, `C=G(X)`. Then

```
G18=d20=C, d26=-F18,
d34=A+C              (support 10),
d34=2A+C             (support 11),
F26=-d34.
```

Both pairs and d34 are nonzero. All three interfaces on a word pair retain
their actual common operands. Write `m=1` or `m=2`; the resulting two-pair
conditions are `d(Y)=-F(X)` and `F(Y)=-m*d(X)-G(X)`. This differs from the
old independently feasible five-equation tail and from the repeated-D
four-word twin core studied for supports 6/7/12/13.

First calculation: examine the simultaneous high-divisibility stratum
`2^k | A` and `2^k | d34`. These imply `2^k | G(X)`. At k=17 the binary
input/output low-bit kernel of sigma1 is trivial, so X would be equal.
At k=16 it is one-dimensional with possible nonzero input XOR mask
`44ab0000`. The new question is whether the second actual pair Y can
coexist with this boundary. Since F(Y) shares low 16 bits, its input XOR
mask belongs to the 16-dimensional kernel of the low 16 output bits of
sigma0. A bounded enumeration will first filter those masks by the exact
independent signed-carry feasibility of `d(Y)+F(X)=0`. Any survivor must
still retain the common X and Y bits in all original sigma equations.

No solver UNSAT, timeout, or empty sufficient construction will be used
as a theorem. An empty complete necessary mask cover would be certified
with a definition-based checker. A nonempty cover would diagnose this
mechanism boundary and guide a new exact bit/carry step. This experiment
does not solve the complete actual-pair system or the base-message lift.

The complete first mask calculation visits 65,536 candidates in the
sigma0-low-16 kernel and leaves exactly five masks for Y:
`4804ddd6`, `c814ddf6`, `d814ffd6`, `5804fff6`, `d805eee6`.
Thus the relaxation is nonempty and alone proves no boundary exclusion.

Before the next calculation, fix X's mask to `44ab0000` and each of these
five Y masks. A finite-budget exact two-word query will retain X'=X xor K
and Y'=Y xor L, and both equations with m=1 or m=2. Each case gets five
seconds. This query diagnoses whether this new two-pair boundary is
feasible; certified fixed-mask contradiction proofs would be needed
before promoting any solver UNSAT to a lemma. A SAT result will be
recomputed by ordinary Python word operations as a local boundary
fixture only. No complete active-pair assignment or message lift is
represented in these queries.

The ten fixed-mask SMT cases are UNSAT in discovery, but this output is
not needed: the second equation's three independent signed masks already
have an empty reachable carry set in every case. For m=1 every case fails
at bit 16; for m=2 the first failing bits are 27, 27, 29, 24, and 22.
The k=16 boundary therefore admits a solver-free complete mask proof.

Before the next calculation, test k=15 with the same complete necessary
mask mechanism. The first-pair kernel has two free bits and the second
kernel has 17, for 393,216 mask combinations. If any pair survives both
necessary signed-carry checks, it remains only a relaxation fixture and
needs actual-word validation. If all fail, the next strictly weaker k=14
stratum can be inspected with an explicit finite budget. This is a new
boundary stratum, not a rerun with a longer SMT timeout.

At k=15, 393,216 complete mask combinations leave 153 after the first
carry condition. The second relaxed condition leaves 39 masks for m=1
and 29 for m=2. Thus this mask-only proof does not extend to k=15.
Before the next calculation, test a bounded prefix of at most 12 of
these exact fixed-mask cases per m, with a one-second limit per case,
stopping at the first actual local pair witness for each m. A found
fixture will show the k=16 threshold is sharp for this two-pair core.
An empty prefix or an unknown case cannot exclude this stratum.
