# Actual first-clear macros give the exact scalar prefix recurrence

Status: LEAN_VERIFIED, 20 audited declarations; independent review pending
for this increment. Lean 4.34.1, commit
`5045d0056413266e57c625dcd7c365b10e377c52`, Std-only, no Mathlib.

This increment connects the previously proved first-clear decomposition
to the original actual-continuation optimum and to the original global
`Optimal` value. It proves the mathematical prefix recurrence without
assuming it as an abstract interface. It does not claim executable DP
verification, runtime complexity, or established historical novelty.

## Actual structural and composition results

`profile_continuation`, `continuation_includes`, and `continuation_append`
prove, respectively, that labelled profiles are real finite continuations,
completion sets grow along them, and two such actual continuations compose
with the sum of their cycle counts.

For every finite forward dependency relation, `W>0`, and coherent
nonterminal clear state with retired prefix `r`, every `PrefixMacro` has:

* A strictly later clear endpoint: `r < final.retired`.
* Length at most `N-r`.

Such a macro exists. These properties are derived from actual non-delay
progress and first-clear stopping, including cases where the first action
omits the oldest job. The all-ready forced tail also has the independent
bound `length ≤ N - completedCountOfState start` for **every** witness,
not only for the witness constructed by the earlier existence theorem.

## Exact horizon and optimum decomposition

For a coherent clear state `s` with `s.retired < N`, without assuming
forwardness or positive width if a completing continuation already exists:

```
FinishesFrom s k ↔
  ∃ actual first-clear macro (s --actions--> middle), l,
    k = actions.length + l ∧ FinishesFrom middle l.
```

This is `finishesFrom_iff_macro` (parameters `dep`, `B=W+1`, `W` are
suppressed above). The forward proof normalizes an actual finishing
continuation to non-delay at the same horizon, and then splits its actual
profile. The reverse proof composes actual transitions. Padding after
completion is permitted exactly as in the original model.

`optimalFrom_first_macro` proves the attaining direction: an optimum
decomposes into an actual first macro plus an optimum from its endpoint.
Replacing a nonoptimal suffix would contradict the original optimum.
`optimalFrom_macro_bound` proves that the original optimum is no greater
than any actual macro length plus an optimal suffix.

`optimalFrom_iff_macro_min` combines these directions into an equivalence:
the optimum is exactly an attained minimum over the actual macro choices
with their optimal suffix costs. For the reverse direction, any competing
finishing continuation is decomposed; a least feasible horizon for its
actual suffix is then constructed by `exists_least_nat`. No recurrence,
suffix optimality, or final inequality is assumed in place of this proof.

## Closed scalar values from actual ROB semantics

For `Forward dep` and `W>0`, `prefixOpt_exists` proves optimum existence
at every one of the `N+1` concrete states `prefixState N (W+1) r`.
`prefixCost` chooses that proved optimum; write it as `F_r`.
This is explicitly a **noncomputable specification** of actual optimal
costs, not an executable dynamic program.

The following statements are proved:

* `prefixCost_terminal`: `F_N = 0`.
* `prefixCost_global_optimal`: `Optimal dep (W+1) W F_0` in the original
  global time-assignment model, including `N=0`.
* `prefixCost_recurrence`: for every `r<N`, there is an actual first-clear
  macro of length `ell` to `j>r` attaining `F_r = ell + F_j`. For every
  other actual first-clear macro from `r` to any `j'`, its length `ell'`
  satisfies `F_r ≤ ell' + F_j'`.

Thus the mathematical statement is exactly the minimum recurrence
`F_r = min_(actual first-clear macros from r) (ell + F_j)`, expressed as
attainment and a universal lower comparison rather than using an assumed
finite candidate list. Macro endpoints are identified with concrete
prefix states using actual state-field equality.

## Verification and remaining scope

```
python workstreams/ILP1-20261014/formal/verify_macro_optimality.py \
  --lean /path/to/lean-4.34.1-linux/bin/lean --proc-self-compat
```

The runner freshly rebuilds all nine modules and records source hashes,
compiler output, durations, version, and axiom audits in
`subagents/lean/evidence/rob-macro-optimality/`. All 20 new audit endpoints
use at most standard Lean `propext`, `Classical.choice`, `Quot.sound`;
three are axiom-free. No `sorry`, `admit`, or custom axiom occurs. Previous
reviewed modules are unchanged.

The unproved algorithmic layer is now specifically: a computable,
complete first-action list; deterministic forced-tail simulation with a
proved correspondence; executable backward evaluation and schedule
reconstruction; and its stated polynomial runtime/space bounds. The
Python implementation and finite tests do not certify that layer in Lean.
The general excess-window XP extension and randomized policies are also
outside this increment.
