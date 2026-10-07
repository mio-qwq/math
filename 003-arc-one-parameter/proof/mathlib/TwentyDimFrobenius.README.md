# Perfect invariant trace on the actual algebra

`TwentyDimFrobenius.lean` constructs an R-linear trace on `TableAlgebra q` and the actual bilinear form `beta(x,y) = trace(x*y)`. It proves symmetry, invariance and left/right nondegeneracy.

It also proves the stronger perfect-pairing statement: the map `x ↦ beta(x,−)` is an R-linear equivalence from the actual algebra to its entire R-linear dual. The explicit inverse sends a functional f to the vector whose ith coordinate is f evaluated on the basis vector indexed by `dualBasis i`. The two inverse identities follow from the involutive dual permutation and equality on a basis.

Every statement holds for any commutative characteristic-two ring R and any q, including zero parameters and rings with zero divisors. This is a concrete trace-duality construction, with no dependency on a named Frobenius typeclass. All eight audits use only the standard three axioms. The file compiles without warnings and introduces no new enumeration.

The Hochschild/Ext realization and complete ARC theorem remain separate. Replay after `TwentyDimAlgebra.olean` and `TraceInvariance.olean` with `lake env lean TwentyDimFrobenius.lean`.
