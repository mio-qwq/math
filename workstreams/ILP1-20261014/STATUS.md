# ILP1 status

Snapshot: 14 October 2026, Asia/Singapore.

Branch `partner/dist-ILP1-20261014`, fetched baseline `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3` (`origin/main`). Changes are confined to this workstream and its own coordination status. Other agents' working copies were not edited.

## Completed first checkpoint

* R1 model and self-contained written proofs of existence, Bellman exactness, full prefix-edge reduction, resource monotonicity, saturated-width recurrence and bounded-frontier state count.
* Operational DP solver plus independent set-based operational replay/Bellman certificate checker.
* Nine semantic unit-test groups passed; exhaustive audit includes all 1,100 forward DAGs on N=0..5, 26,706 parameter cases, and 100 additional random fan-in-two DAGs. Exact counts and source hashes are in `evidence/exhaustive.json`; this is finite testing, not an arbitrary-size proof.
* A four-job counterexample to oldest-ready optimality and an indistinguishable online pair; a four-job counterexample to monotonicity of both resource saturation thresholds.

## Active independent tasks

* Theory: general online optimality resource dichotomy; randomized/advice family. Written proofs under independent review.
* Verification: independent time-assignment exact solver, cross-checks and online-family audits. Integration pending.
* Lean: pinned Lean 4.34.1 downloaded; subagent reports actual compilation of general model theorems. Root review/recompilation and integration pending. This checkpoint does not yet claim accepted LEAN_VERIFIED scope.
* Literature: older ROB event-DAG sources identified; September 2026 claimed three-machine polynomial result under source audit. Do not state this classical question is simply still open or newly solved by ILP1.

All prospective new results remain NOVELTY_UNCONFIRMED. Independent agent review is not journal peer review.

## Continuation

An enabled two-hour recurring automation was successfully created for this research conversation, first scheduled 14 October 2026 04:15 Asia/Singapore. It requests checkpoint recovery, real research and authorized Git publication. Future tool/runtime availability is not guaranteed; no continuous between-trigger computation is claimed.
