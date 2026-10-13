# Executable exact enumeration with correctness proofs

`ExactEnumeration.lean` implements and proves an independent, deliberately
elementary exhaustive solver. It uses Lean 4.34.1 and bundled Std only.

The input dependency relation is an executable Boolean function on `Fin n`.
For a candidate horizon `K`, every job is assigned a pair in
`Fin K × Fin W`: an issue cycle and an issue lane. A recursive list enumerates
**all** such functions. The Boolean checker requires strict time order for
every true dependency and every ROB edge `i+B <= j`, and forbids simultaneous
jobs on the same lane. `assignments_complete` proves that the enumeration
contains every finite assignment; `feasibleCheck_iff` proves equivalence of
the executable Boolean result and the fully specified `Feasible` predicate.

The top-level `solve` searches horizons `0,...,n`, retrieves a successful
assignment, and returns the horizon, issue times and lanes.

- `solve_sound`: every returned solution has a globally optimal horizon,
  satisfies the actual model's `Legal` predicate, and finishes before the
  returned boundary.
- `solve_complete`: for **every** finite forward-dependence program and every
  positive `B,W`, the executable solver returns such an optimal schedule.
  This includes the empty program, whose optimum is zero.
- `feasibleCheck_iff` and the soundness theorem do not require positive
  resources or forward input edges. Completeness uses those assumptions
  to obtain the serial horizon bound `n`.

These theorems are universal correctness proofs, not bounded testing of the
algorithm. All 12 printed audits contain only standard Lean axioms.
The executable code itself does not invoke classical choice or noncomputable
definitions; classical reasoning is confined to its correctness proofs and
the already verified model bridge.

Actual compiler-interpreter executions returned:

| Input | Returned horizon and issue times |
| --- | --- |
| Empty program, `B=W=1` | `some 0` |
| Four jobs, edge `1 -> 3`, `B=3,W=2` | `some (2, [0,0,1,1])` |
| Four-job serial chain, `B=3,W=2` | `some (4, [0,1,2,3])` |

The finite slot-assignment search has up to `(K W)^n` candidates per horizon;
it is a proof baseline, not a practical performance claim or a novel
algorithm. It is separate from the Python state-DP and layer-enumeration
solvers. Their concrete implementation correctness is not proved by this
module. Source hashes and a fresh 61-declaration combined run are preserved
in `subagents/lean/evidence/exact-enumeration/`.
