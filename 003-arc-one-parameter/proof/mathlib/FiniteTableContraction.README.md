# The concrete table satisfies finite contraction identities

`FiniteTableContraction.lean` converts sparse polynomial-vector sums into finite sums of structure constants. The generic statement requires only that output labels are below n; duplicate labels remain permitted. It also provides a finite-index family version by zero extension.

For the actual twenty-label table it defines `tConstants a b k = sumTerms (tTerms a.val b.val) k.val`. The frozen output-label bounds and genuine polynomial-vector basis associativity prove all contraction identities required by `FiniteBilinear.StructureAssociative`.

This source performs no new finite enumeration. Every semantic input is supplied by the preceding compiled layers; the generic contraction does not need a byte bound because it operates directly on decoded polynomial vectors. All five axiom audits report only the standard three axioms, and compilation succeeded without warnings.

Build `TableBasisSemantics.olean` from source after its prerequisites, then:

```sh
LEAN_PATH=.:.. lake env lean FiniteTableContraction.lean
```

Use the Windows path syntax documented in the BytePacking README where applicable.
