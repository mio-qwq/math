# Actual scaling automorphisms of the dual summand

For any commutative characteristic-two ring R, any parameter q and any
unit H of R, `TwentyDimDualScale.lean` constructs an actual R-algebra
automorphism of the twenty-coordinate table algebra. It fixes the first
ten coordinates and multiplies the last ten coordinates by H. Its inverse
is the same construction with the inverse unit. The actual e and f
characters are fixed.

The proof derives multiplication support from the already checked dual
transpose recurrence: two base inputs have base output, a mixed product
has dual output, and two dual inputs have zero product. Thus each output
weight equals the product of the two input weights on every supported
term. Finite bilinear contraction gives multiplicativity on all inputs.
The unit has only the base coordinates 0 and 8, so it is preserved.

Coordinatewise scaling and inverse scaling give a genuine R-linear
equivalence; the actual multiplication and unit proofs upgrade it to
`AlgEquiv`. No new enumeration of table pairs or cochain quadruples is
needed, and no domain or nonzero-parameter hypothesis is used.

The verification JSON records source hash, actual compilation,
independent replay and printed axiom audits. Dependency-ordered replay:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimDualScale
```

This source constructs the actual algebra automorphism. The fixed
cochain's pullback formula is a separate source; the induced action of a
module-category functor on actual Ext is a further comparison obligation.
