# Independent review of an additive-constant-robust online lower bound

Verification subagent C, 2026-10-13 UTC. The construction was supplied by
the main agent. The proof below was independently reconstructed; no defect
was found. It concerns the exact eager ROB model at fixed `B=3,W=2`, with
incoming dependencies visible only after instruction admission.

## Construction and exact isolation

For `q>=1`, use `q` consecutive four-job blocks. In block `k`, write
`a=4k,b=4k+1,c=4k+2,d=4k+3`, with zero-based `k`. Its hidden bit determines
whether the sole within-block true edge is `b -> d` or `c -> d`.
For every block after the first, give each of its three initial jobs
`a,b,c` the two true predecessors `c_prev,d_prev` of the preceding block.
No other true edges occur. Every job has at most two true predecessors.

At `B=3`, every index gap at least three creates an artificial ROB precedence.
For the first job of a later block, the preceding block's `a_prev,b_prev`
are artificial predecessors, while `c_prev,d_prev` are true predecessors.
The other two initial jobs also have all four preceding jobs as direct
augmented predecessors. The later block's final job has all four as artificial
predecessors by index distance. Thus **every job of a later block must issue
strictly after every job of the preceding block**. No two consecutive blocks
can overlap in an issue cycle.

This is stronger than merely an abstract dependency barrier: the next block
may partly enter the ROB early, but none of its jobs can execute early. At a
block boundary all preceding jobs are complete, none of this block or later
blocks is complete, and eager refill presents exactly its initial three jobs.
They are ready, and its final job `d` is not yet admitted. There is no extra
cycle between a completed block and the next block's first legal issue.

Offline, execute `{a,parent(d)}` and then `{other_root,d}` in each block.
The concatenated schedule takes `2q` cycles and is legal. The work bound
`4q/2=2q` proves `T*=2q`.

## No information leakage before the necessary decision

Changing the current bit changes only the incoming edge of its final job `d`.
Admission of `d=a+3` into a three-entry ROB requires the completed retired
prefix to extend through `a`. The preceding-block barrier prevents `a` from
executing before that preceding block is complete. Therefore `d` cannot be
observed before the first issue decision after the preceding block completes.

Some current roots can be admitted earlier, but their incoming edges are the
same under both bit values. Even the complete observation history up to this
decision, including all earlier visible instructions and their dependency
lists, is unchanged by switching the current bit. Later instructions cannot
leak it: ordered admission cannot reach them before admitting `d`. Future
successor lists of visible roots are excluded by the information model.

This argument uses all observed history, not only a comparison of the current
ready sets. It remains true when the scheduler knows `q` or the total length,
and when its action depends on arbitrary memory of prior blocks.

## Lower bounds for arbitrary online policies

Choose all hidden bits independently and uniformly before the run. Let `C_k`
be the cycle at which the first `k` blocks are complete, with `C_0=0`.
The block barrier implies that block `k` has not started by `C_(k-1)`.
Let `D_k=C_k-C_(k-1)`. A finite terminating run has `T=sum D_k`.
Nontermination makes the corresponding lower bound immediate.

Each block needs at least two cycles. It can finish in two only if its first
action after `C_(k-1)` is exactly `{a,parent(d)}`. Both cycles must use both
issue slots by the four-job work bound; `a` must be in the first action to
admit `d` for the second; and the hidden parent must precede `d`. This gives
one unique successful first action for each bit. Empty, underfull, or delayed
first actions do not evade the argument: each forces at least three cycles.

Condition on all prior observations and policy randomness available for that
first decision. The current bit is still fair by the non-leakage argument.
The two successful actions are distinct, so conditional two-cycle success
has probability at most one half. Hence

`E[D_k] >= 2*(1/2)+3*(1/2)=5/2`,

and `E[T]>=5q/2`. This is an average over fixed complete input programs.
Therefore some fixed bit vector has policy expectation at least `5q/2`;
the input need not adapt to the realized random choices.

The reviewed uniform-younger policy has exactly one fair decision per block.
A correct choice finishes that block in two cycles and an incorrect choice
in three. On every fixed bit vector its duration is distributed as
`2q+Binomial(q,1/2)`, with expectation `5q/2`.

For a deterministic policy, choose the bit of each block to defeat its first
decision. Earlier observations do not depend on that bit, so this recursion
defines a single fixed complete program, rather than an adversary changing a
program during execution. Every block takes at least three cycles, yielding
`T>=3q`. There may be additional idle cycles, which only strengthen the bound.

Consequently no randomized online policy can satisfy
`E[T(P)] <= r T*(P)+C` on all these programs with any fixed `C` and `r<5/4`.
Indeed, `5q/2 <= 2rq+C` fails for sufficiently large `q`. Similarly no
deterministic policy can have an additive-constant guarantee with `r<3/2`.
The known upper bounds establish sharpness at these fixed resources. This
strengthens a single finite witness to an asymptotic competitive lower bound.

## Independent finite evidence

`repeated_pair_audit.py` checks every bit string for `q=0,...,6`, a total of
127 programs including the empty boundary. The independent time-assignment
CSP returns `2q`; explicit two-cycle-per-block schedules pass direct replay;
the independently implemented ROB policy recursion returns `5q/2`.
The audit also checks 8,256 direct augmented cross-block predecessor pairs.

On one six-block input, a full direct probability tree has exactly 64 leaves
and the precise shifted-binomial duration distribution. Every random decision
is checked to occur at a clear-prefix block boundary whose visible window is
the three initial jobs and excludes the current hidden final job. These finite
checks support, but do not replace, the all-`q` and all-policy argument above.
Actual runtime and source hashes are in `repeated_pair_results.json`.

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED**;
**NOVELTY_UNCONFIRMED**; no Lean verification claimed by this subagent.
