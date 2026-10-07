# Primary agent status

Published milestones: `5af6c3f` proves all-vector associativity for the actual twenty-coordinate multiplication; `f54f9f6` adds generic units. Milestone `77698ad` publishes concrete units, symmetric left/right nondegenerate trace, and generic additive/scalar laws. The current update adds the actual Ring/Algebra instance, a 20-element basis, dimension 20 over fields, and trace invariance. All hold in the stated polynomial setting and every commutative characteristic-two specialization where applicable.

Current ownership under `003-arc-one-parameter/proof/mathlib/`: `TwentyDimAlgebra.lean` and `TraceInvariance.lean` are completed and published with this update. Proposed next files are `CochainBasisSemantics.lean` and `CochainCycleSemantics.lean`; the primary agent is taking over while subagents are blocked by their usage limit. The primary agent handles integration, documentation and dependency-ordered replay tooling. Check history and this file before choosing a new source file.

Actual checks: Lean 4.34.1 and the separately pinned Mathlib package; main-agent replays succeeded for concrete unit, trace and generic bilinear laws. Axiom audits use only `propext`, `Classical.choice`, and `Quot.sound` (some theorems use fewer). No `sorry`, added axioms or `native_decide`.

Remaining gaps: the actual library algebra and dimension theorem are now proved; the formal Hochschild complex, Ext realization and full ARC construction are not established. In 001, Newton identities and the original Hadamard-to-block construction remain separate; the general weighted rectangular theorem in 002 remains unformalized. Read FORMALIZATION.md for exact per-file scope.

Partner entry point: fetch main and partner branches, inspect COORDINATION.md and current ownership, then use a disjoint source and your own branch/status record. No external partner branch was present at the latest fetch. Never overwrite other agents' work or commit private credentials.

Next primary tasks: integrate the actual algebra and invariant trace, provide a reproducible semantic replay command, then advance the smallest concrete cochain bridge. The user requested periodic stage summaries and planning; a 30-minute follow-up is configured in this chat.
