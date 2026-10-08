# The concrete table is the actual core dual extension

`TwentyDimDualIsomorphism.lean` constructs an actual `R`-algebra isomorphism
from the published `TableAlgebra q` to `CoreDualExtension q`. It applies to
every commutative characteristic-two ring and every parameter `q`, including
zero parameters and rings with zero divisors. The core and extension have
the actual multiplications installed by `TwentyDimCoreAlgebra.lean` and
`DualTrivialExtension.lean`.

The comparison sends the first ten coordinates to the actual core, and the
last ten coordinates to the linear functional with those values on the
core basis. `compare_mul` checks both components of the genuine product,
using the eight polynomial table blocks and finite sum splitting.
`compare_one` checks the unit. `compareAlgebra` combines the mutually inverse
linear maps and these laws into the algebra isomorphism.

`compare_trace` identifies evaluation at the core unit with the actual
table trace `x.coords 10 + x.coords 18`. `compare_tracePairing` identifies
the corresponding actual bilinear trace forms. No new finite enumeration
is used. Table provenance is recorded in `../../ATTRIBUTION.md`.

This identifies the actual algebra with its structural dual-extension
description. It does not construct an Ext comparison, an all-degree
resolution, or the complete ARC homological realization.

After compiling the imported local modules in the pinned package:

```sh
LEAN_PATH=.:.. lake env lean -o TwentyDimDualIsomorphism.olean TwentyDimDualIsomorphism.lean
```

Actual checks: Lean 4.34.1, the pinned Mathlib revision and unchanged
manifest, exit 0, zero warnings, and seventeen printed audits containing
only `propext`, `Classical.choice`, `Quot.sound`. No `sorry`, added axiom
or `native_decide`.

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
