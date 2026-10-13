# Arbitrarily many repeated gadgets: actual ROB formalization

Status: the finite dependency family, its block barrier, hidden-job admission
condition, and exact offline optimum are **LEAN_VERIFIED**. The full online
observation/probability argument in the research note is **not** formalized
here. Originality is **NOVELTY_UNCONFIRMED**.

Source: `RepeatedGadgets.lean`, importing the existing `ROBOperational.lean`.
The earlier sources are unchanged. Lean 4.34.1 with bundled Std is used;
no Mathlib or external theorem package is used.

## Exact family and quantifiers

For every natural `q` (including zero) and every `bits : Nat -> Bool`, the
program has `4*q` jobs. Only bits at indices below `q` occur in its true edges.
Write `block(i)=i/4`, `offset(i)=i%4`. True dependencies are exactly:

* Within block k, offset 1 (bit true) or offset 2 (bit false) precedes offset 3.
* Offsets 2 and 3 of block k precede each of offsets 0, 1, 2 of block k+1.

There are no other true edges. `dep_forward` proves all true edges strictly
respect program order. `indegree_at_most_two` proves any three predecessors
of one job contain a duplicate, the exact at-most-two-input property.

## Closed mathematical and operational endpoints

`block_separation` says that for **every** time assignment legal at B=3 and
any width W, `block(i)<block(j)` implies `t(i)<t(j)`. There is no assumption
of work conservation, no-idling, or the proposed optimal schedule. The proof
uses actual true edges and the already verified all-pairs window equivalence.

`trace_block_separation` applies this to an arbitrary actual `ROBTrace`:
at the cycle when j issues, i is in that trace's completed set. This proves
the claimed non-overlap directly for the existing operational semantics.

The explicit two-cycle schedule is:

| Within-block job | Relative issue cycle | Lane |
| --- | --- | --- |
| a (offset 0) | 0 | 0 |
| Selected parent (offset 1 or 2) | 0 | 1 |
| Other younger root | 1 | 1 |
| d (offset 3) | 1 | 0 |

Block k's base cycle is `2*k`. `schedule_legal` proves true-dependency,
canonical ROB, and width-two constraints separately. The local four-entry
phase/lane table is proved by finite `decide`; all arbitrary-block claims
use general arithmetic, index arguments and induction, not bounded search.

`lastJob_lower_bound` proves `t(d_k)>=2*k+1` for every legal execution at
B=3 and any width. Each block's true parent-to-d edge and the inter-block
barrier form a chain with two jobs per block. Thus the exact lower bound
does not require a general cardinality/work-bound theorem.

The strongest endpoint is

```lean
optimal_two_per_block (q : Nat) (bits : Nat -> Bool) :
  Optimal (@dep q bits) 3 2 (2*q)
```

`operational_two_per_block` supplies an actual ROB trace for the explicit
schedule with all jobs retired at boundary `2*q`. Conversely,
`trace_finished_lower_bound` proves that every actual completed ROB trace
for this family at B=3 needs at least `2*q` cycles.

## Useful information-barrier primitives, without a probability claim

`hidden_not_admitted` proves that, at any cycle c before the completion of
the oldest job a_k, the actual admitted frontier is at most index d_k.
Thus d_k is outside the ROB. This is an exact state fact, including the
cycle when a_k issues, because results become available the next cycle.

`two_cycle_block_forced` says that if all four jobs of a block execute in
the interval `[start,start+2)`, then a_k and the selected parent both issue
at `start`, while d_k issues at `start+1`. It permits any width. At width two,
these forced jobs fill the first cycle, but a general online policy's
observation process is not defined in this module.

Still absent: joint distributions, policy randomness, conditioning on prior
observations, a fixed-input averaging theorem, expected duration `5*q/2`,
and the additive-constant competitive lower bound. None follows in Lean
merely from the statements above, and none is claimed Lean verified here.

## Reproduction and audit

```sh
python workstreams/ILP1-20261014/formal/verify_repeated_gadgets.py \
  --lean /absolute/path/to/lean-4.34.1/bin/lean
```

The documented sandbox path-compatibility flag `--proc-self-compat` can be
added where `/proc/<pid>/exe` is inaccessible. The runner rebuilds the two
local imports and this module in a fresh temporary directory. Twenty main
declarations are individually audited; their transitive axiom dependencies
are only `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`,
additional axiom or trusted native proof shortcut is used. Actual compiler
logs, source hashes, version and durations are stored separately in
`subagents/lean/evidence/repeated-gadgets/`.
