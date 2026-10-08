# Square-zero kernel and complete radical correspondence

`SquareZeroJacobson.lean` proves that an actual left ideal with all
two-element products zero is contained in the actual ring Jacobson radical.
For every surjective ring homomorphism with that property on its full
kernel, the whole source radical is exactly the inverse image of the whole
target radical. It also proves that the Jacobson ideal of an ideal already
contained in the ring radical is precisely that ring radical.

The argument uses the noncommutative maximal-left-ideal APIs. The rings
need no commutativity, field, characteristic or finiteness assumption.
Square-zero of the whole ideal is the hypothesis; an individual square-zero
element alone does not supply it. No explicit radical calculation,
simple-module classification or homological realization is asserted.

Actual checks: Lean 4.34.1, pinned Mathlib, exit 0, zero warnings and three
printed audits using only `propext`, `Classical.choice` and `Quot.sound`.
Dependencies: the pinned `Mathlib.RingTheory.Jacobson.Ideal` and Abel APIs.
Three missing Mathlib prerequisites were built serially from the pinned
source; the manifest is unchanged. No new finite enumeration.

```sh
LEAN_PATH=.:.. lake env lean SquareZeroJacobson.lean
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
