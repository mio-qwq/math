# Exact fixed-schedule window footprint

`ResourceFootprint.lean` formalizes the **window portion** of R5 and Theorem 2
in `subagents/theory/STRUCTURAL_RESULTS.md`. It uses the unchanged verified
`ROBModel` and `ROBOperational` modules and Lean 4.34.1's bundled Std library.
Eighteen new declaration audits pass using standard Lean axioms only.

For a zero-based time assignment `t : Fin N -> Nat`, define the seeded demand
set by the member `1` and every `j-i+1` with `i<j` and `t(j)<=t(i)`.
`IsFootprintMax` says that beta bounds this set **and is itself a member**.
The module proves existence and uniqueness of this maximum and defines
`footprint t` as that unique beta. This is a noncomputable specification,
not a claimed optimized algorithm for calculating a maximum.

The central conclusions are:

- For positive `B`, canonical ROB legality is equivalent to all inequalities
  `j-i+1 <= B` for `i<j` and `t(j)<=t(i)`.
- For `N>0`, `CanonicalROB t B <-> footprint(t) <= B`, including all B.
  The ROB condition itself rules out B=0 for a nonempty program.
- `1 <= footprint(t) <= N` for nonempty programs.
- `Legal dep B W t` is equivalent to true-dependence legality, width legality,
  and `footprint(t)<=B`.
- Given true-dependence and width legality, `footprint(t)` is a feasible
  capacity and every other feasible capacity is at least as large.

Neither true-dependence legality nor a separate finite horizon is required
for the **pure window equivalence**. They remain relevant when combining the
window condition with the complete scheduling problem. The formalization is
therefore slightly more general than the written theorem's window lemma.

Boundary details were checked explicitly:

- Equal issue times count as reversals; omitting them would miss the window
  occupied by a simultaneous issue batch.
- The demand is `j-i+1`, with the extra one forced by the strict admission
  inequality. A strictly increasing program-order schedule has footprint 1.
- For the empty program the seeded footprint is 1. The equivalence holds for
  positive B; it must not be extended to B=0, where an empty ROB is legal.

This module does **not** formalize the cardinality expression for the issue
width footprint, minimization over all optimal schedules in `B_sat`, or a
polynomial algorithm for the program-dependent saturation threshold. It
makes no historical novelty claim. The window proof was checked separately
against the written R5 argument; these new Lean proofs and their first run
were produced by the same subagent, so the build receipt alone is author-run
verification and does not certify independent review of the Lean source.

Reproduce without changing any existing file:

```sh
python workstreams/ILP1-20261014/formal/verify_footprint.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-footprint-independent
```

The optional compatibility flag has the same narrow purpose documented in
`README.md`; ordinary hosts can omit it. The new runner compiles the two
imports and this module in a fresh temporary directory, records source hashes,
and rejects failed compilation or any nonstandard axiom. Author evidence is
preserved separately under `subagents/lean/evidence/resource-footprint/`.
