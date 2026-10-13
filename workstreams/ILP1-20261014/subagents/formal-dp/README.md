# Operational Bellman certificates and generic exact search

This addition is based on `d7e2e6eeae34479f9ecd123fcf4471c1c57575d7` and
owns only this directory. The underlying operational model is imported from
`../../formal/ROBOperational.lean`; no shared or other-agent file is changed.

## Proven scope

`ROBBellman.lean` proves the following for **arbitrary finite program size**:

1. Every operational ROB trace starts at the concrete state with no completed
   jobs, zero retired jobs, and exactly `min(N,B)` admitted jobs.
2. If a natural-valued potential is zero whenever all jobs are completed and
   satisfies `V(s) <= 1 + V(next)` for **every** legal `ROBStep`, then a trace
   finishing after `K` cycles satisfies `V(initial) <= K`.
3. This bound holds for every previously defined `Feasible` time assignment,
   by the already verified operational/time-assignment equivalence.
4. A legal schedule attaining `K = V(initial)` is globally `Optimal`.

The proof telescopes local inequalities along the actual transition trace.
It permits empty issue batches, idling, and repeated states. It does not
assume that a list of explored states covers all legal executions. The
potential is an explicit theorem premise: this module does not claim every
numerical table exported by an external program satisfies that premise.

`FiniteSearch.lean` supplies a separate, executable Lean algorithm:

- `within goal next fuel s` explores **every member of each supplied finite
  successor list**, allowing cycles and stopping at the fuel bound;
- `firstTrue` checks horizons from zero through the bound;
- `exactSearch_sound` proves that a returned horizon has a finishing path
  and is minimal among *all* finishing paths, including paths whose lengths
  exceed the supplied bound;
- `exactSearch_complete` proves success from any finishing path within the
  bound, and `exactSearch_none_iff` proves complete bounded exclusion;
- `exactSearch_optimal_of_enumeration` transfers the result to any external
  relation under the explicit premise `t in next(s) iff step(s,t)`.

The generic search is depth-bounded exhaustive search, not a memoized dynamic
program. No ranking/decreasing-state premise is needed. **The successor-list
interface has not been instantiated here for a finite encoding of ROB states
or the Python solver.** Concrete time/lane enumeration is owned by the separate
Lean-model task. No claim of verified Python code or concrete ROB enumeration
follows from this generic algorithm.

`BellmanExact.lean` closes the converse certificate direction for arbitrary
transition systems. If terminal states have potential zero, all edges satisfy
the lower-bound inequality, and each nonterminal state has one edge attaining
`V(s) = 1 + V(next)`, then strong induction on `V(s)` constructs a genuine
finishing path of length `V(s)`. Other edges may contain cycles. It proves
exactness and uniqueness of such a Bellman value and agreement with the
generic search when its list enumerates the complete transition relation
and the supplied horizon is large enough. All three certificate properties
are explicit hypotheses; they are not assumed to hold for arbitrary tables.

## Actual verification

Both additions compile under Lean **4.34.1** (commit
`5045d0056413266e57c625dcd7c365b10e377c52`) with bundled `Std` only, no Mathlib.
The 20 newly printed theorem audits use only `propext`, `Classical.choice`,
and `Quot.sound`; the generic finite-search proofs do not use Classical.choice.
No added axiom or unchecked proof placeholder is used.

The reproducible author run is recorded in `evidence/receipt.json`, including
source hashes, compiler version, compilation exit codes, and all axiom audits.
This is **author-run LEAN_VERIFIED evidence**, not an independent review.

```sh
python workstreams/ILP1-20261014/subagents/formal-dp/verify.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --output /tmp/ilp1-bellman-review
```

On this execution host add `--proc-self-compat`, for the documented
same-process executable lookup compatibility adapter in `../../formal/`.
The runner compiles this adapter from source and creates all `.olean` files
inside a temporary directory. It does not install or edit shared Lean config.

## Research status

| Property | Status |
| --- | --- |
| Arbitrary-size operational lower bound and witness optimality | LEAN_VERIFIED |
| Generic finite-list bounded search soundness/completeness | LEAN_VERIFIED |
| Exact Bellman local attainment implies a finishing witness | LEAN_VERIFIED |
| Concrete ROB-state enumeration/Python implementation verification | Not provided |
| Independent semantic review | Pending parent review |
| Historical novelty | No novelty claimed; classical Bellman/finite-search facts |
| Real processor or hardware-online optimum | Outside this ideal-model proof |
