# Independent review: actual ROB macro optimality

Decision: ACCEPTED for the mathematical specification stated in `ROB_MACRO_OPTIMALITY.md`.
Reviewer branch: `partner/ilp1-review6-20261014`; reviewed source commit
`10bb7282c07996f60a8438a1f3adbd35e058c977`, integrated baseline `6b36144`.
This review did not alter author sources or reuse compiled author objects.

## Fresh compiler evidence

Command, from this independent worktree:

```
python workstreams/ILP1-20261014/formal/verify_macro_optimality.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output workstreams/ILP1-20261014/subagents/review6/evidence/macro-optimality
```

The runner was inspected: it creates a fresh temporary `LEAN_PATH`, compiles nine
local modules in import order, records actual exit codes and every printed axiom
set, and rejects unexpected axioms. It succeeded for all nine modules. The
increment has exactly 20 audited declarations; the imported 131 declarations
are not counted as new. Lean 4.34.1, Std only, no Mathlib. Only `propext`,
`Classical.choice`, and `Quot.sound` occur; three new declarations are axiom-free.
The compatibility shim addresses the documented process-executable path only.
Full compiler logs and hashes are in `evidence/macro-optimality/`.

## Semantic checks

1. `PrefixMacro` has one genuine `ROBStep` selected by the actual ready-count
   `NonDelay` property, followed by `ForcedTail`. The latter stops exactly at the
   first clear state; its cons guard excludes every intermediate clear state.
   No abstract edge-cost relation or recurrence is postulated.
2. `OptimalFrom` means a real completing finite continuation plus comparison
   against every real completing horizon. Exact horizons can be padded after
   completion. Normalization and decomposition preserve that horizon, so the
   feasibility equivalence does not silently replace exact length by at-most.
3. Forward dependencies and positive width are needed for strict macro progress
   and the finite bound, and are present, together with coherent nonterminal
   start. At the terminal prefix the empty action yields a one-cycle macro
   self-loop: `PrefixMacro` alone does NOT imply strict progress. This is harmless:
   `prefixCost_terminal` separately proves zero and `prefixCost_recurrence`
   requires `r<N`. Do not export its minimum recurrence to terminal r.
4. The attaining direction normalizes and splits an optimal continuation, then
   proves suffix optimality by replacement. The converse constructs a least
   feasible suffix from each competing finishing continuation and applies the
   universal macro comparison. Neither direction assumes its desired optimum.
5. `prefixCost` is explicitly `Classical.choose` of proved actual optimum
   existence. Endpoint identification uses coherent clear-state field equality.
   The initial value is connected to original global `Optimal`, including N=0.
   Classical choice is a standard logical axiom here, not evidence of a computable
   dynamic program or a new unproved scheduling axiom.

## Scope and remaining gaps

This establishes the closed mathematical recurrence over actual first-clear
macros and its global optimum, plus existence/progress/length bounds. It does
not establish a computable complete first-action enumeration, executable forced
simulation, backward DP, schedule reconstruction, or polynomial runtime.
No historical novelty claim is endorsed. The result is a formalized model-specific
Bellman decomposition using the already proved non-delay and forced-tail facts.

Audited target SHA-256: `d1a55582c71fa7b94874d34b31f997c780731439732097e6e68b2c648187be59`.
