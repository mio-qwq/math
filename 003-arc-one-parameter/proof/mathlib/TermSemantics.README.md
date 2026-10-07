# Sparse lists and triple products as actual polynomial vectors

`TermSemantics.lean` interprets the frozen `encode`, `scaleEncode`, `leftProduct` and `rightProduct` definitions as actual functions `Nat → Polynomial (ZMod 2)`. It proves the generic list and nested-product semantics for arbitrary inputs, using induction rather than new finite enumeration.

Every actually packed coefficient must fit in its byte. Scaled and triple-product statements impose bounds on the **multiplied** coefficients, not merely on the two inputs. The left and right statements have their respective independent nested bounds. Repeated labels are permitted: XOR accumulation corresponds to polynomial-vector addition, so duplicates add and can cancel correctly.

The proof generalizes over each left fold's initial accumulator. Its scalar scaling uses the universal `decode_pMul` theorem; its single-coordinate interpretation uses `decodeVec_pack`. Thus the claimed semantics does not assume that an encoded equality already denotes a field-algebra equality.

All four printed axiom audits list only `propext`, `Classical.choice`, and `Quot.sound`. The file compiled with exit zero and no warnings in the pinned package. Its source hash is recorded in `TermSemantics.verification.json`.

This generic layer does not yet supply the twenty-dimensional algebra instance, a Hochschild complex or Ext. Table-specific basis associativity can be transferred next using the already verified left/right composed coefficient bounds and the original packed associativity equalities.

After the prerequisites in [BytePacking.README.md](BytePacking.README.md), keep both the local Mathlib proof directory and its parent Std proof directory on `LEAN_PATH`. Then:

```sh
LEAN_PATH=.:.. lake env lean -o BytePacking.olean BytePacking.lean
LEAN_PATH=.:.. lake env lean TermSemantics.lean
```

On Windows, use the semicolon-separated absolute paths shown in the BytePacking README and omit the `LEAN_PATH=.:..` prefix. The public source of every imported local module is supplied; build outputs remain ignored.
