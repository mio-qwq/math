# Work counting and the actual ROB corridor

Status: the general work/count/admission bounds and the complete corridor
containment are **LEAN_VERIFIED** in the actual existing ROB model.
The candidate-state binomial bound, the fixed-parameter reachability algorithm,
and the Python implementation are **not** formalized by these modules.
Originality remains **NOVELTY_UNCONFIRMED**.

New sources: `ROBWorkBounds.lean` and `ROBCorridor.lean`, using only Lean
4.34.1's bundled Std and the unchanged `ROBModel` / `ROBOperational` imports.

## Counting is derived from the model

For a natural issue-time assignment t on `Fin N`, `completedJobs t c` filters
`List.finRange N` by `t(i)<c`; `completedCount` is its length. A companion
list contains exactly the jobs with `c<=t(i)`. Their no-duplicate property
and exact partition length N are proved.

`list_injection_length_le` derives a finite cardinality inequality from a
genuine injection and list membership, using Std's
`List.Nodup.length_le_of_subset`. Each completed job maps to the pair
`(t(i),lane(i))` in a list of c*W slots. Equality of such pairs forces
equality of jobs by the existing `WidthBound` predicate. No count bound
is an additional hypothesis.

The resulting arbitrary-program theorems include:

| Theorem | Exact conclusion |
| --- | --- |
| `issued_count_le` | At most W jobs issue in each cycle. |
| `completed_count_le` | The actual completed list has length at most cW. |
| `pending_count_le` | If all jobs issue before H, at most (H-c)W remain at c. |
| `work_bound` / `feasible_work_bound` | A completed horizon satisfies N<=HW. |
| `completed_slack_lower` | cW-(HW-N)<=completedCount(c), for c<=H. |
| `retired_le_completed` | Every actual retirement-prefix length is at most the completed count. |
| `trace_admission_upper` | The actual admitted frontier is at most min(N,cW+B). |

`trace_completed_list` proves that membership in the counted list is
equivalent to membership in the actual trace state's completed predicate.
Thus the trace counting theorems are not counts of a surrogate schedule.

## Exact corridor statement

Write B=W+excess and S=HW-N. Theorem `trace_corridor` quantifies over every
actual `ROBTrace dep (W+excess) W t`, every horizon H at which all N jobs
have retired, and every natural layer c<=H. It proves:

1. Every index below `cW-excess-S` is in that actual completed state.
2. Every actual completed index is below `min(N,cW+excess)`.
3. `cW-S<=completedCount(c)<=cW`.

Natural subtraction in (1) and (3) truncates at zero. This is the stated
max(0,...) convention, not integer subtraction treated as natural equality.
`lower_cut_within_program` additionally proves that the left cutoff never
exceeds N; the `Fin N` quantification omits no index of the claimed prefix.

The theorem permits empty programs, zero resources when a trace actually
exists, arbitrary dependency predicates, idle cycles, early completion, and
the final layer c=H. Forward dependencies and positive resources are not
needed as extra hypotheses once existence of the actual completing trace
is given. In particular it covers the research model's positive resources,
forward DAGs and padded H-cycle executions. Its static counterpart is
`legal_corridor`.

## The lower-frontier proof

The formalization uses a shorter counting route than the original written
proof's number of completed-but-unretired jobs. Let r be the exact retirement
prefix at layer c. Every job completed before c+1 has index below r+B:
otherwise the verified window edge from job r to that job would require
job r to finish before its own first possible completion, a contradiction.
This argument covers jobs completed in earlier cycles as well.

Therefore the first c+1 cycles complete at most r+B jobs. Remaining jobs
inject into the actual `(H-c-1)*W` future issue slots. Hence

    N <= r+B+(H-c-1)*W.

For c<H, substituting B=W+excess gives
`cW<=r+excess+(HW-N)`. At c=H, the frontier is N and the same bound follows
from the proved work inequality. All indices below r are completed.

For the upper frontier, a job issued in cycle s has index below r_s+B,
while the proved counting inequality gives r_s<=sW. If it is completed at
layer c then s+1<=c, giving index<cW+excess. No upper or lower strip
inequality is assumed as an interface condition.

## Audit and remaining boundaries

There are 16 individually audited primary declarations in `ROBWorkBounds`
and 9 in `ROBCorridor`. The final endpoints transitively check their helper
lemmas too. All actual Lean axiom reports contain only the standard
`propext`, `Classical.choice`, and `Quot.sound`; no new axiom, `sorry`,
`admit`, or trusted native proof shortcut is used.

```sh
python workstreams/ILP1-20261014/formal/verify_corridor.py \
  --lean /absolute/path/to/lean-4.34.1/bin/lean
```

The runner freshly compiles the two existing imports and both new modules,
records hashes/timing/version, and rejects unexpected axioms or errors.
The documented sandbox-only `--proc-self-compat` flag is available.
Source-specific receipts are in `subagents/lean/evidence/rob-corridor/`.

Not established by Lean here: injection into the binomial family of virtual
strip subsets; the count `sum(j=excess..excess+S) choose(2excess+S,j)`;
finite-layer transition completeness; the parameterized runtime bound; or
the correctness of `src/corridor.py`. These remain distinct next results.
