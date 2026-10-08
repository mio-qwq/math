# The actual ten-dimensional core and its dual extension

`TwentyDimCoreAlgebra.lean` applies the verified generic constructors to the
actual ten-label ARC core. Its polynomial contraction identities reuse the
existing core-basis associativity theorem; its two-sided unit reuses the
published twenty-label unit through the proved lower-block correspondence.
No new finite enumeration is used.

At every parameter in every commutative characteristic-two ring, the actual
core has a unital `Ring` and `Algebra R`, the prescribed structure constants,
an explicit ten-element module basis and finite/free module instances.
Its rank is ten under `StrongRankCondition R`, in particular over fields.
Its genuine dual-action extension is a unital algebra with rank twenty
under the same rank hypothesis, and its actual trace pairing is nondegenerate
over every such base ring, even with zero divisors.

The extension is the comparison target; an algebra isomorphism from the
existing twenty-coordinate table is not yet constructed here. The Ext
comparison and full ARC realization remain separate. The table provenance
is given in `../../ATTRIBUTION.md`.

After compiling its imported modules in this fixed package:

```sh
LEAN_PATH=.:.. lake env lean -o TwentyDimCoreAlgebra.olean TwentyDimCoreAlgebra.lean
```

Actual checks: Lean 4.34.1, the pinned Mathlib revision and unchanged manifest,
exit 0, zero warnings, and nine printed audits containing only `propext`,
`Classical.choice`, `Quot.sound`. No `sorry`, added axiom or `native_decide`.

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
