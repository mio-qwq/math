# Independent review of actual ROB work bounds and corridor containment

Reviewer: formal-DP subagent, independent of the Lean author and the root's
algorithm. Review date: 2026-10-13 UTC. No other agent's files were edited.

Reviewed final Lean commit: `bf7b46cf258d357fdf2ba85d59b0299f68cf4d2c`.

| Source | SHA-256 |
| --- | --- |
| ROBWorkBounds.lean | `d1abd7c738b8146a5a1f8c997218d54f17d0e997f621f6d5182fe4381105a408` |
| ROBCorridor.lean | `9796a1affd8ba18919af982fe49ef8117217cb9729e1bef75f73014e711f566d` |

For scope comparison, root HEAD was
`42be4b0dc19039d35ffb92eedc201bc70131dba8`.
The inspected root `CORRIDOR.md` hash was
`fd463a81718e573aaf6bdac9142bbb6ee0e4052ebbc9b6eb1c7f107bd9924fd0`;
`src/corridor.py` was
`98b28cbae3cff040a5f3ce3cc76fe4e8cf226de07c0c2977a6bc0e9308f0302a`.
Those active root artifacts contain broader written claims than the Lean
module, so their full coverage must not be inferred from this review.

## Verdict

**Accepted as general, actual-model Lean proofs of work/cardinality bounds
and horizon-dependent strip containment.** The final theorem quantifies
over every actual ROB trace that has retired all jobs by a specified H,
and every cut between zero and H. It neither postulates the target strip
nor leaves an uninstantiated transition-model interface.

Fresh independent compilation passed all four source files. The new
endpoint counts are **16+9=25**, not the preliminary 24: the ninth corridor
endpoint proves that the left cutoff is within the program. The 22+11
audited imported endpoints are recompilations, not additional results.
All audits use only standard `propext`, `Classical.choice`, and `Quot.sound`.

No defect was found in the final-layer case, empty-program case, arbitrary
completion-horizon quantifiers, or natural subtraction. The binomial
candidate-state bound, finite-layer reachability correctness, parameterized
runtime, and Python implementation remain **outside** the Lean coverage.
No novelty determination or academic-peer-review claim is made.

## Counting is genuinely derived

`completedJobs t c` and `pendingJobs t c` filter `List.finRange N` by
`t(i)<c` and `c<=t(i)` respectively. Their duplicate-free property and exact
partition of N are proved. The completed count is therefore a true finite
cardinality, rather than a free scalar constrained by assumed inequalities.

The generic injection lemma maps a duplicate-free source list into a target
list. Its proof establishes injectivity of the mapped list and membership
in the target before applying the standard length inequality. The target
list need not be assumed duplicate-free; this only makes its length a
possibly weaker upper bound and introduces no soundness issue.

Under the existing `WidthBound` predicate, each completed job maps to its
actual pair `(issue time,lane)`. Equal pairs imply equal jobs. The explicit
slot list has length `c*W`, proving completed count at most cW. The pending
proof instead maps into `(t(i)-c,lane)` for slots before H. Its membership
premise guarantees `c<=t(i)`, so subtracting c loses no information when
proving injectivity. If c>H, there are no pending jobs; the natural-zero
slot bound is still sound.

The total work bound `N<=HW` follows by identifying the completed list at H
with all jobs, not by assuming the work inequality. The lower count bound
then follows from the partition, pending-slot capacity, and the proved split
`HW=(H-c)W+cW` under `c<=H`.

The retired prefix is separately shown to inject into the completed list,
giving `r_c<=completedCount(c)<=cW` and the actual admission upper bound.
Finally `trace_completed_list` identifies membership in that list with the
actual state's completed predicate, using the previously compiled operational
equivalence. Thus even the final theorem's list-valued cardinality expression
counts the actual ROB state, not a surrogate schedule.

## Closed actual-state corridor theorem

Use `e` for window excess and `c` for the time cut, as in the Lean source.
The actual trace has B=W+e, and its premise is

```lean
(tr.state horizon).retired = n
```

`trace_finished_iff` converts this exact operational premise to all issue
times being below H. Together with `trace_legal`, it supplies every hypothesis
of the static theorem. No extra claim about a transition enumerator or a
policy is needed. For all `c<=H`, the conclusion is exactly

`[0,max(0,cW-e-S)) subset Completed(c) subset [0,min(N,cW+e))`,

and `max(0,cW-S)<=|Completed(c)|<=cW`, where S=HW-N.

The lower-frontier proof is different from the root note's completed-but-
unretired counting argument but proves the same statement. Let r be the
actual retirement prefix at c. Every job completed before c+1 has index
below r+B. Otherwise, if a job j had index at least r+B, r would be a valid
unfinished job and the verified all-pairs window edge would require

`t(r)<t(j)<=c<=t(r)`,

a contradiction. This argument includes jobs from earlier cycles; it does
not only bound the jobs issued in cycle c.

For c<H, completed jobs at c+1 therefore number at most r+B, while the rest
inject into `(H-c-1)W` remaining slots. Thus

`N<=r+B+(H-c-1)W`,

which gives `cW<=r+e+S`. Every index below r is complete, proving the lower
strip. The upper strip follows by looking at a completed job's actual issue
cycle s<c: its index is below `r_s+B<=(s+1)W+e<=cW+e`.

The proof does not assume non-delay execution, a particular ready-job
priority, or a forward dependency graph. An actual completing trace for
any dependency predicate is sufficient, so the theorem in particular covers
all legal forward-DAG traces in the research model. Every completing trace
is already defined at all natural cycles; idle terminal padding is allowed
by the actual transition semantics.

## Boundary and natural-subtraction checks

- **Final layer c=H.** The proof branches before using c+1. Retirement is
  exactly N because all jobs have issue times below H. The proved work
  bound then yields `HW<=N+e+(HW-N)`. No fictitious cycle after H is used.
- **Empty program N=0.** The job type and counted lists are empty; retirement
  is zero. For c<=H, the truncated lower cutoff is zero, even with positive
  terminal slack. H=0 is included. Conversely H=0 cannot complete a nonempty
  program, as the derived work bound shows.
- **Initial layer c=0.** There are no completed jobs and the count bound
  forces zero. The strip's left side is empty; its upper side may be loose
  but does not assert that any job has already completed.
- **Early completion and idling.** H need not be the minimum makespan, and
  no cycle is required to fill all W lanes. Enlarging H increases the slack
  budget, as intended.
- **Zero resources.** The formal theorem allows natural W and e without
  positivity assumptions. If a trace exists at zero width it must be empty;
  otherwise the assumptions are inconsistent. The research model's positive
  resources are a covered special case. No division by W is used.
- **Truncated subtraction.** The source expression
  `c*W-e-(H*W-N)` is exactly `max(0,cW-e-S)`. The work theorem separately
  guarantees N<=HW on a completing trace, so S is the actual nonnegative
  idle-slot budget, not an accidentally clipped negative quantity.
- **Finite-domain containment.** `trace_corridor` quantifies over `Fin N`.
  The independent endpoint `lower_cut_within_program` proves its left cutoff
  is at most N for every c<=H. Combining them really proves the stated
  natural-index prefix inclusion; no out-of-program indices are hidden by
  the finite quantifier. The right endpoint explicitly uses `min N`.

## Exact limits of the formalization

The helper `completed_count_of_index_bound` bounds the **number of jobs in
one completed state**. It is not a bound on the number of possible states.
Neither new module constructs the virtual strip-subset injection used in
the written binomial formula, proves its subset-cardinality count, nor
shows that the count is attained by a program family.

Likewise, no candidate-layer generator, adjacency checker, soundness or
completeness theorem for the corridor DP, path reconstruction, or runtime
analysis appears here. Those are separate written and computational
results. The modules do not import or verify `src/corridor.py`.

The pre-integration root note says its strip and model connection remain to
be formalized. Integration may update **those** statuses to Lean verified,
while leaving candidate counting, tightness, exact algorithm, and Python
correctness separate. The formal module's own coverage document already
makes these distinctions correctly. No additional CSP or large experiment
was run in this review, and earlier solver tests were not used as proof of
the formal endpoint's meaning.

## Actual independent reproduction

The author runner was inspected before execution. It compiles the unchanged
two imports and both new modules into a fresh temporary directory, with a
fresh LEAN_PATH, then records every printed axiom audit. This independent
run wrote only the reviewer's owned evidence directory:

```sh
python /workspace/scratch/6a1539b44ef3/ilp1-lean/workstreams/ILP1-20261014/formal/verify_corridor.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat \
  --output /workspace/scratch/6a1539b44ef3/ilp1-formal-dp/workstreams/ILP1-20261014/subagents/formal-dp/evidence/corridor-independent
```

All four processes exited zero. `ROBWorkBounds` compiled in 0.541233 seconds
and `ROBCorridor` in 0.573320 seconds; the import times were 0.607004 and
0.515279 seconds. Compiler: Lean 4.34.1, commit
`5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std, no Mathlib.
The new source contains no `sorry`, `admit`, new axiom, unsafe substitute,
or trusted native proof shortcut. The documented process-path shim does
not modify the compiler or kernel.

The receipt and all four raw logs are in `evidence/corridor-independent/`.
They preserve source/runner/shim hashes, exact audit lists, timings, and UTC
timestamps. Later source changes are not covered by this fixed-hash review.
