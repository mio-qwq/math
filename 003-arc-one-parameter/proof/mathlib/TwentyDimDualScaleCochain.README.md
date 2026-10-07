# The fixed cochain's actual dual-scaling eigenvalue

Let R be any commutative characteristic-two ring, q any element, H any
unit and h_H the actual automorphism scaling the dual summand by H.
`TwentyDimDualScaleCochain.lean` proves, on all actual algebra inputs,

`P(h_H x, h_H y, h_H z) = H P(x,y,z)`.

Equivalently, inverse-input pullback has eigenvalue H inverse. The
identities are also stated as equalities of the entire genuine scalar
trilinear maps. Each of the five terms in the full coordinate formula
contains exactly one dual input, so its product acquires one factor H.

The pullback construction accepts every scalar trilinear cochain.
For the fixed one, full character closure is retained, and when q cubed
is nonzero no arbitrary scalar bilinear cochain has it as a boundary.
The latter follows by undoing the unit scaling in the full differential.

Source hashes, actual compilation, independent replay and printed axiom
audits are in the verification JSON. Dependency-ordered replay is:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimDualScaleCochain
```

These are actual cochain identities and full boundary statements. The
action of the inverse-restriction module-category functor on the actual
Ext class still needs an explicit resolution/functor comparison. No
whole-space Ext action, all-degree profile or complete ARC is asserted.
