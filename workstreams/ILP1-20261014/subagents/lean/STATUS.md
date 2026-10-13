# Lean subagent B checkpoint

- Research ID: `ILP1-20261014`.
- Baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
- Independent branch: `partner/ilp1-lean-20261014`.
- Owned paths: `workstreams/ILP1-20261014/formal/` and this subdirectory.
- Repository instructions read; `git fetch origin` completed before edits.
- Compiler: official Lean 4.34.1 release, commit
  `5045d0056413266e57c625dcd7c365b10e377c52`; Mathlib not used.
- Official Linux x86-64 archive SHA-256:
  `47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4`.

## Verified first increment

`ROBModel.lean` and `ROBOperational.lean` have actually compiled and all
33 printed declaration audits contain only subsets of `propext`,
`Classical.choice`, `Quot.sound`. The universal operational ROB equivalence,
optimal-horizon existence and exact certificate criteria are covered.
See `formal/README.md` for exact scope and exclusions, and `evidence/` for
the fresh reproducibility run and source hashes.

The development does **not** yet prove correctness of the Python solvers or
formalize the deterministic-online impossibility pair. No historical novelty
is asserted. Independent mathematical review is requested from the parent.

## Environment and next action

Pinned release extracted to the session's `ilp1-tools/lean-4.34.1-linux/`.
A minimal current-process path compatibility helper is needed on this host;
its exact source and reason are documented in `formal/README.md`.

Next increment: formalize the four-job, `B=3,W=2` indistinguishable pair with
edges `1 -> 3` and `2 -> 3`. Establish optimum two cycles for each program
and show that no common first issue batch can complete both in two cycles.
This will use a new file, preserving the first increment during review.
