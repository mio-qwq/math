# The whole actual table radical through the augmentation

The published sixth-power vanishing makes every element of the full augmentation kernel nilpotent, so that entire nil left ideal is contained in the actual noncommutative ring radical. For every commutative characteristic-two coefficient ring, the entire table radical is the augmentation inverse image of the radical of R×R. If R is semisimple as a ring, including if R is a field, the whole radical is exactly the augmentation kernel: both idempotent coordinates vanish. Its exact eighteen-label span and full six-factor word vanishing are proved under that hypothesis. Every parameter, including zero, is covered.

General coefficients receive the radical preimage formula; the explicit
zero-coordinate radical formula requires the stated semisimple coefficient
hypothesis. No simple-module classification or Ext comparison is established.
The complete ARC realization remains open.

Actual checks: Lean 4.34.1, pinned Mathlib, exit 0, zero warnings and 8
printed audits using only standard axioms. Eleven missing published
prerequisite sources were replayed unchanged in dependency order, including
the frozen closure certificate, with exit 0, zero warnings and 77 separate
printed standard-axiom audits. These are prerequisite checks rather than new
research declarations. Three additional pinned Mathlib prerequisites were
built serially for the nil-ideal argument. The manifest is unchanged.
No new finite enumeration is introduced.

Replay after the published augmentation/nilpotence dependencies and the
partner structural modules have been compiled:

```sh
LEAN_PATH=.:.. lake env lean TwentyDimAugmentationJacobson.lean
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
