# The actual third Ext class has a nonzero Yoneda square

The constructed whole shifted suffix lift identifies the Yoneda square
of the fixed actual third self-Ext class with the closed cup Hom class
`fCupExtSix`. The explicit six-letter evaluation then proves

```text
q^4 != 0 ==> fExtThree(q) composed with fExtThree(q) != 0 in Ext(S,S,6).
```

The coefficient ring is any commutative ring of characteristic two.
For a ring without zero divisors, including a field, q nonzero suffices.
The source also identifies the already defined actual second power
`fYonedaPower(q,2)` with this sixth Ext class and proves it nonzero under
the same fourth-power hypothesis.

This combines a genuine whole shifted product comparison with the full
preceding-Hom nonboundary obstruction; nonzero Ext^6 alone was not used
to infer a nonzero square. All higher powers, dimensions of the Ext
groups, the full self-Ext profile and the complete ARC construction
require further proofs.

The verification JSON records actual compilation, independent replay of
the frozen source, five axiom audits and its SHA256. With the pinned
package and dependency artifacts installed:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean TwentyDimYonedaSquare.lean
```
