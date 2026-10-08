# Complete word lifts and a general nonboundary test

For every degree n, this source lifts arbitrary n letters of the actual
table algebra into its specified finite free term Pn. The recursive
definition uses the actual R-linear coefficient insertion and preserves
all coordinates. At every word w its A-valued coefficient is

```text
wordLift(n,x)(w) = algebraMap(product over i of x(i).coords(w(i))).
```

The proof retains central scalar coefficients without imposing
commutativity on A or A-linearity on coefficient insertion. The source
also proves the complete finite expansion, equality with the actual
A-basis word on coordinate-basis inputs, first-letter additivity and
R-scalar compatibility, and evaluation under every actual A-linear map
to a character module. These are general proofs; no word enumeration is
performed.

If all adjacent letter products vanish and the final letter has zero
character value, the actual recursive boundary satisfies

```text
D(n)(wordLift(n+1,x)) = x(0) * wordLift(n,tail(x)).
```

The complete first A-coefficient remains. If its character value is also
zero, every A-linear map from Pn to the actual character module kills
this boundary. Any next-degree Hom with nonzero evaluation on the word
therefore cannot be a preceding-Hom precomposition boundary. The test
quantifies all actual maps from Pn, without a finite-support restriction
on the proposed boundary.

The source does not assert that the lifted word has zero resolution
boundary. It supplies no cocycle closure, specific cup product, actual
Yoneda product identification, higher-power nonvanishing or complete ARC.
Those are separate obligations.

The companion verification JSON records actual compilation, independent
source replay, eleven printed axiom audits and the exact source hash.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarWordLift
```
