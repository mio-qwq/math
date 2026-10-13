# Lean verification of the unit-time ROB model

The development uses **Lean 4.34.1**, compiler commit
`5045d0056413266e57c625dcd7c365b10e377c52`, and its bundled `Std` library.
It has no Mathlib dependency and does not modify the repository's shared
Lean or Lake configuration.

## Exact coverage

`ROBModel.lean` defines jobs as `Fin n`, nonnegative integer issue times,
forward true-data dependencies, exact issue capacity through interchangeable
issue lanes, and the canonical in-order retirement prefix. It proves:

- existence, uniqueness and monotonicity of the retirement prefix;
- equivalence of ROB visibility at issue time and every additional edge
  `i + B <= j`, with strictly earlier issue of `i`;
- the equivalent blocking-distance criterion;
- equivalence with the augmented precedence relation;
- serial feasibility for positive `B,W` and forward data dependencies;
- existence and uniqueness of the optimal horizon, bounded by `n`;
- exact optimality certificates, including infeasibility at horizon `K-1`;
- feasibility/resource monotonicity and optimal-time antitonicity;
- the empty-program boundary and positive horizon for nonempty programs.

`ROBOperational.lean` defines an explicit cycle transition with completed-job
predicates, retirement/admission frontiers, issue eligibility and issue lanes.
An issue batch completes at the cycle boundary, the entire completed prefix
retires, and the next cycle begins with an eagerly refilled window. It proves
`Legal <-> Nonempty ROBTrace` and equivalence of feasible horizon `K` with full
retirement at boundary `K`. The execution trace may have empty cycles; each
job has one assigned issue time, so no job is issued twice.

The zero-based time convention is: jobs issued at cycle `c` have results
available in cycle `c+1`; after `K` cycles every job must have issue time `< K`.
Same-cycle dependence chains are prohibited. Completed jobs blocked from
retirement continue to occupy the canonical interval.

Issue capacity is expressed by existence of lane labels in `{0,...,W-1}`
with no same-cycle collisions. This is an operational encoding of at most
`W` issuances. The cardinality equivalence to a particular list-counting
implementation has not been separately formalized.

## Exclusions

These files do not verify the Python exact solvers, their memoization or
enumeration completeness. They do not prove SSA semantic preservation,
properties of arithmetic operations, an online scheduler, or claims about
real processors. The operational state is the specified ideal eager ROB,
without finite retirement bandwidth, fetch bandwidth, speculation, variable
latencies, memory constraints or exceptions. Mathematical novelty is not
claimed for the classical minimization or augmented-precedence results.

## Reproduction

Install the official `lean-4.34.1-linux.tar.zst` release from
<https://github.com/leanprover/lean4/releases/tag/v4.34.1>. Extraction on a
container may require `tar --zstd --no-same-owner -xf ...`.
The archive used for the recorded run is the official Linux x86-64 archive;
its SHA-256 is recorded in `../subagents/lean/STATUS.md`.

```sh
python workstreams/ILP1-20261014/formal/verify.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --output /tmp/ilp1-independent-lean-check
```

On the current host `/proc/self/exe` is readable but
`/proc/<current-pid>/exe` is not. Lean 4.34.1's executable-location routine
uses the latter. The optional `--proc-self-compat` flag builds and loads
`proc_self_compat.c`, which redirects **only this same-process executable
lookup** to `/proc/self/exe`. It changes no Lean definitions, tactics, kernel
checks, axioms, file contents or other path lookups. This flag is unnecessary
on ordinary hosts. The exact compatibility source is included for inspection.

```sh
python workstreams/ILP1-20261014/formal/verify.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-independent-lean-check
```

The runner builds local imported `.olean` files in a new temporary directory,
records source hashes, compiler version, exit codes, timing and every printed
axiom dependency. It rejects failed compilation or any axiom outside
`propext`, `Classical.choice`, and `Quot.sound`. The checked source contains no
`sorry`, `admit`, or added axioms. Existing run evidence is in
`../subagents/lean/evidence/`; it is author-run verification, not a claim of
independent review or journal peer review.
