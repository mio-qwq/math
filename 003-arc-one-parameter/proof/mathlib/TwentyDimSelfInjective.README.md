# Actual self-injectivity over every characteristic-two field

For any characteristic-two field k and any parameter q, the actual
table algebra A is injective as a left module over itself. The parameter
may be zero. No finite-dimensional restriction is imposed on the source
or target modules in the injectivity extension criterion.

`TwentyDimSelfInjective.lean` constructs the extension explicitly.
Given an injective A-linear map j from M to N and an A-linear map f
from M to A, choose a k-linear left inverse of j. Composing it with
the scalar trace of f extends that trace to a scalar functional ell
on N. Recover the A-valued extension at n by applying the proved
perfect trace duality inverse to the functional a maps to ell(a n).

Testing against every a proves that the recovered map extends f.
The symmetrizing trace and its invariance prove left A-linearity:
the product tested is a b, and symmetry rotates the trace to test
b times the recovered element. Commutativity of A is not assumed.
Compatible field scalar structures on arbitrary A-modules are
installed by restriction of scalars.

The resulting `Module.Injective A A` is proved, with an actual
instance supplied. The field hypothesis is used for scalar functional
extension; the perfect trace pairing alone over a general commutative
ring does not give that step.

Seven printed audits and actual compilation/independent replay records
are in the verification JSON. Dependency-ordered replay in this folder:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimSelfInjective
```

Actual categorical injectivity and all-positive Ext vanishing into A
are in the separate `TwentyDimExtIntoAlgebra.lean` source. The complete
ARC construction remains separate.
