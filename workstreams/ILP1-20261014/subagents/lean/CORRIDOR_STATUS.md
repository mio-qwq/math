# General work bounds and corridor checkpoint

Base local commit: `0caf016f817478ad3521a841e12513669c98b55f`.
`git fetch origin` completed at resumption and the worktree was clean.
Read the main worktree's `CORRIDOR.md` and `src/corridor.py`; parent reports
independent theory review at `4a29b0a`.

Two new Lean modules give closed theorems about arbitrary actual schedules
and ROB traces. Counting is implemented with duplicate-free filtered
`List.finRange` lists and proved slot-pair injections. This fulfills the
formerly missing general width/work-count bridge without adding Mathlib.

`ROBWorkBounds.lean`: 16 primary audits, including general work bound,
completed/pending/issued cardinality bounds, true retirement-frontier
counting, and actual admission upper bound.

`ROBCorridor.lean`: 9 primary audits, culminating in the complete actual
`trace_corridor` strip containment and completed-count interval. Its lower
frontier proof counts all jobs completed by c+1 inside the true frontier
r_c+B and then counts all remaining slots until H. This avoids needing
an assumed occupancy bound or a prepackaged strip inequality.

The program may be empty; the horizon's terminal layer is proved separately.
All index arithmetic is natural with explicit truncated subtraction.
The lower cutoff is proved at most N, so `Fin N` does not conceal an
out-of-range part of the claimed completed prefix.

Still open: binomial state counting, finite corridor transition completeness,
algorithm extraction and Python correspondence. No formal complexity theorem
or implementation verification is claimed by this increment. Novelty remains
unconfirmed; the task was model-connected correctness, not priority.

Fresh independent replay:

```sh
python workstreams/ILP1-20261014/formal/verify_corridor.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-corridor-root-check
```

No prior sources/runners/evidence were changed. Parent and formal-dp have
been informed of the exact coverage and asked to review/recompile.
