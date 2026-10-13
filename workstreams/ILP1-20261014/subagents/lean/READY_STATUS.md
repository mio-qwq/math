# Forced-state structural bridge checkpoint

Baseline: `bf7b46cf258d357fdf2ba85d59b0299f68cf4d2c`.
`git fetch origin` completed at task start, with a clean worktree.
Read theory `FORCED_SEGMENT_DP.md` at
`a9408865e844cd05ea7fefda10bf9139f671075c`.

New module `formal/ROBReady.lean` compiles against Lean 4.34.1 with Std only.
Twenty-five main statements are audited. Actual-state coherence is proved
from ROBTrace before any readiness/count conclusions are derived. The
non-delay predicate means ready-subset plus exact maximal allowed cardinality;
actual issue lanes are constructed from list ranks, so width is not assumed
by cardinality notation alone.

Closed results: readiness persistence under actual completion supersets;
ready+holes<=B; holes=completed-retired; unique all-ready actions at h>=B-W;
branching only at h<B-W; B=W+1 non-prefix states forced; forward+positive
resource progress; all non-delay actual traces finish within N cycles.

Not formalized: full continuation simulation, non-delay optimum existence,
macro endpoint existence/recurrence, full-window branching classification,
prefix DP correctness, its complexity, or the Python implementation.
These boundaries are explicit in `formal/ROB_READY.md`.

Next smallest useful theorem: a finite ROB continuation from an arbitrary
coherent state can be replayed from any coherent completed superset by
deleting already-completed jobs, proving final completion and no greater
length. That needs a real finite continuation transition object, rather
than using the current ready persistence as an unproved whole-trace bridge.
Afterward prove action extension and existence of optimal non-delay
continuations by finite induction. All such work will use a separate file.

Fresh replay command:

```sh
python workstreams/ILP1-20261014/formal/verify_ready.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-ready-root-check
```

formal-dp was notified, but currently has a different independent review
assignment. No independent Ready review is claimed until actually completed.
Root is coordinating integration and reviewer order.
