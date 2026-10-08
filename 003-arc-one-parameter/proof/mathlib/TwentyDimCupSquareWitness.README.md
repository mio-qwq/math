# A nonzero actual sixth Ext class

Write x, y, u, t, V and J for actual coordinate-basis elements with
indices 1, 2, 4, 6, 15 and 17. Over any commutative characteristic-two
ring, use the following six letters in the actual noncommutative algebra:

```text
[t | y + q^2*x | J | V | x + y | u].
```

The installed multiplication table gives zero for all five adjacent
products. Both endpoint values under the f character vanish. The actual
recursive word lift has just four basis-word terms, and the closed
`cupSixHom` evaluates this lift to exactly q^4.

The lifted word is not asserted to be a resolution cycle. Its actual
boundary is its first A coefficient acting on the tail lift. Every
A-linear map P5 -> S, with S the actual f-character module, kills that
boundary because the first character value is zero. Thus, if q^4 is
nonzero, no such map can have boundary precomposition equal to the
complete cup Hom.

The source defines `fCupExtSix` with the genuine Mathlib Ext constructor
of the specified full projective resolution. Closure holds on all P7,
and the complete preceding-Hom criterion proves

```text
fCupExtSix(q) : Ext(S,S,6),
q^4 != 0  ==>  fCupExtSix(q) != 0.
```

In a ring without zero divisors, including a field, q nonzero suffices.
The stronger fourth-power condition is retained for general rings with
zero divisors; a nonzero third power alone does not imply it.

Identification of this class with the actual Yoneda square is separate
from this source. It does not establish all powers to be nonzero,
an all-degree Ext dimension profile, or the complete ARC realization.
There is no six-letter word enumeration.

The companion verification JSON records actual compilation, independent
replay of the frozen source, ten printed axiom audits and its SHA256.
With the pinned package and dependency artifacts installed:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean TwentyDimCupSquareWitness.lean
```
