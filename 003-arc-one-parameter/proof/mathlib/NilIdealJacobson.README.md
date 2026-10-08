# Whole nil ideals and the actual noncommutative radical

An actual left ideal every one of whose elements is nilpotent is contained in the actual ring Jacobson radical. The proof applies nilpotence to every left multiple, using its left-ideal membership, and uses a genuine left inverse of one plus that element. It does not infer radical membership from an arbitrary individual nilpotent element. For every surjective ring homomorphism with full kernel contained in the source radical, the whole source radical is exactly the inverse image of the target radical. A full nil kernel suffices; if the target radical is zero, the source radical is exactly the full kernel. Neither ring needs to be commutative.

This source does not establish a concrete radical calculation, simple-module
classification, category equivalence, Ext comparison or the complete ARC
realization. No new finite enumeration is used.

Actual checks: Lean 4.34.1, pinned Mathlib, exit 0, zero warnings and 4
printed audits using only standard axioms. The manifest is unchanged.

```sh
LEAN_PATH=.:.. lake env lean NilIdealJacobson.lean
```

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
