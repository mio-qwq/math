# First-clear proof checkpoint

Owner: ILP1 Lean subagent; branch `partner/ilp1-lean-20261014`.
Parent source checkpoint:
`0b4e56b3fe5e9dbf2d7e3132d991886a0b88a4f7` (finite/global representation).

New module `formal/ROBForcedPrefix.lean`: 18 actual-model audited endpoints.
Proved clear-state representation, fixed-action step uniqueness,
nonclear non-delay determinism for `B=W+1`, first-clear forced-tail
existence within remaining-job count and exact uniqueness, and
first-clear/first-macro decomposition of any finishing non-delay profile
using exactly its original action list.

Actual Lean 4.34.1 fresh verification:
`formal/verify_forced_prefix.py`; evidence in
`subagents/lean/evidence/rob-forced-prefix/`. Only standard logical axioms;
no `sorry`, `admit`, or custom axiom. Independent review of this new
increment is pending. Prior-file reviews do not certify these new proofs.

No prior reviewed source was modified. Remaining concrete steps:
derive macro endpoint strict advance and bounded length; prove actual
profile/continuation concatenation; prove optimum suffix/first-macro
attainment and minimality; only then formalize enumeration or executable DP.

Reproduce from worktree root:

```
python workstreams/ILP1-20261014/formal/verify_forced_prefix.py \
  --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /tmp/ilp1-forced-prefix-replay
```
