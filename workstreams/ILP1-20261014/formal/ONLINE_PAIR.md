# Four-job online information obstruction

`OnlinePair.lean` is an actually compiled extension of the ROB model.
It imports the verified operational model and uses only the pinned bundled
Std library. Its 16 printed declaration audits use standard Lean axioms only.

Jobs are numbered `0,1,2,3`, with `B=3` and `W=2`.

| Program | True data edge | A two-cycle offline schedule |
| --- | --- | --- |
| A | `1 -> 3` | `{0,1}`, then `{2,3}` |
| B | `2 -> 3` | `{0,2}`, then `{1,3}` |

The initial visible jobs are the same three roots in both programs.
The ROB constraint imposes `0 -> 3`. Any two-cycle execution of A must issue
both 0 and 1 first; any two-cycle execution of B must issue both 0 and 2
first. Equal first actions would therefore issue 0,1,2 together, contradicting
width 2. Each offline optimum is exactly two cycles because a real dependency
edge requires two different cycles.

The main theorem `ILP1.OnlinePair.local_policy_three_cycles` quantifies over
**every** first-decision policy satisfying `InitialWindowLocal`. There is a
program in the pair with offline optimum 2 such that every completing
execution following the policy's first action takes at least 3 cycles.
For terminating policies this gives the ratio lower bound `3/2` by ordinary
arithmetic. The formal endpoint states exact integer cycle counts, not a
rational-number division theorem.

`InitialWindowLocal` means that the first action agrees whenever the
dependency relation restricted to jobs 0,1,2 agrees. The pair also has the
same program length, window capacity, width, and initial completion state.
This assumption is the information boundary: the theorem does not cover a
policy supplied with hidden successor/dependence information, offline advice,
or random bits. No asymptotic ratio or repeated-instance composition result
is asserted. The general `W>=2, B=W+1` family is not formalized in this file.

The four-job feasible witnesses and visible-graph equality use ordinary
kernel-checked `decide`. The impossibility proof quantifies over arbitrary
time assignments and arbitrary local policies; it is not finite enumeration
of a predetermined collection of schedulers. Historical novelty remains
unconfirmed and no publication priority is claimed.

Reproduce all modules with `formal/verify.py`. The second-increment author
run is preserved separately at `subagents/lean/evidence/online-pair/` so the
first model/operational receipt remains unchanged.
