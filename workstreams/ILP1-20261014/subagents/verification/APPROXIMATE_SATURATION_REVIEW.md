# Independent review: approximate saturation obstruction

Date: 14 October 2026, Singapore. Independent verifier: subagent C.
Status: complete written proof, independently reviewed and finitely checked;
not Lean-verified here, and historical novelty unconfirmed.

## Program and exact optimum

Fix `K>=1`, with `N=2K`. Jobs `0,...,K-1` form a directed chain in program
order. Jobs `K,...,2K-1` are independent of every other job. Resources `B,W`
are positive integers; windows larger than the program are allowed and have
the usual capped admission semantics.

For `W>=2`, the claimed formula is accepted:

`T*(P_K,B,W) = K + ceil(max(0,K-B+1)/min(B,W))`.

For `W=1`, separately, `T*=2K` for every positive `B`.

### Lower bound: count after the last chain cycle

Number execution cycles starting at one, and let `S` be the cycle in which
the final chain job completes. The chain requires `S>=K`. Before the issue
phase of cycle `S`, that final chain job is still incomplete, so no more than
the first `K-1` jobs have retired. The admitted prefix consequently has length
at most `K-1+B`, capped by `2K`. Thus at most `min(K,B-1)` independent jobs
have been admitted by the issue phase of cycle `S`.

This upper bound counts **every** independent job that can finish by the end
of `S`, including ones issued in `S` itself. A completed independent job
cannot have retired earlier past the unfinished final chain job. Admission
after the end-of-cycle retirement cannot supply another issue in the same
cycle. Hence at least `max(0,K-B+1)` independent jobs remain **after** cycle
`S`. Each subsequent cycle issues at most `min(B,W)` jobs. Therefore

`T >= S + ceil(max(0,K-B+1)/min(B,W))`

and then `S>=K` gives the desired lower bound. Delaying the chain cannot
evade this count; the bound on admitted independent jobs still applies.

### Matching construction

Issue the chain as early as possible, one chain job per cycle, for `K` cycles.

If `B>=K+1`, issue one independent job alongside each chain job. The `j`-th
independent job is admitted by cycle `j` because the earlier chain prefix
has retired. Width two is sufficient and all jobs finish in `K` cycles.

If `1<=B<=K+1`, label the independent jobs `j=1,...,K` in their program
order. For `j<=B-1`, issue independent job `j` alongside the chain in cycle

`K+j-B+1`.

These are distinct cycles between one and `K`. Before its assigned cycle,
the completed chain prefix is long enough to admit that independent job.
Width two suffices. Exactly `B-1` independent jobs have completed when the
chain finishes. All these jobs form the completed initial program prefix and
retire at that boundary. The remaining `K-B+1` independent jobs then execute
in program-order batches of size `min(B,W)`, with each batch retiring before
the next is admitted. This takes precisely the ceiling term above. At `B=1`
the overlapping part is empty, which is consistent with the same construction.

The lower bound and construction coincide for every allowed resource pair.

## Exact approximate-window threshold at arbitrary width

For `W>=2`, the unrestricted-window optimum is `K`. For a real `epsilon>=0`,
define the approximate threshold by

`B_epsilon(P_K,W) = min{1<=B<=2K : T*(P_K,B,W) <= (1+epsilon)K}`.

Set `q=floor(epsilon*K)`. An exact generalization of the proposed width-two
formula, independently derived during this audit and also checked by the
theory agent, is

`B_epsilon(P_K,W) = max(ceil((K+1)/(q+1)), K+1-q*W)`.

**Proof.** The optimum duration is integral, so its allowed excess above `K`
is exactly `q`. The exact makespan formula yields

`ceil(max(0,K+1-B)/min(B,W)) <= q`

if and only if

`K+1 <= B + q*min(B,W)`.

Here `q>=0`, so

`B+q*min(B,W) = min((q+1)B, B+qW)`.

The inequality is therefore equivalent to both
`B>=ceil((K+1)/(q+1))` and `B>=K+1-qW`. Taking their maximum gives the least
integer window. The first term is at least one and both terms are at most
`K+1<=2K`, so the declared threshold domain needs no further correction.

### Width two and linear necessary windows

At `W=2` and `0<=epsilon<1`, window one fails because it takes `2K` cycles.
For `B>=2`, the effective width is two, so the exact specialization is

`B_epsilon(P_K,2) = max(2,K+1-2*floor(epsilon*K))`.

For `epsilon>=1`, window one succeeds and the threshold is one.

More generally, at any fixed `W>=2` and fixed `0<=epsilon<1/W`,

`B_epsilon(P_K,W) >= (1-W*epsilon)K+1`

because `floor(epsilon*K)<=epsilon*K`. In terms of program length this is
`(1-W*epsilon)N/2+1`, a linear necessary window. In particular, at width two
every fixed approximation factor strictly below `3/2` requires windows
growing linearly in this family, even though its true dependency graph is
only one chain plus isolated vertices.

These are lower bounds for this explicit family. They do not establish
general approximation impossibility for all other models or for schedulers
allowed to transform the program order or remove operations.

## Boundary audit

| Boundary | Correct interpretation |
|---|---|
| `K=1` | Two independent jobs: time two at `B=1`, time one at `B>=2,W>=2`; the formula remains valid. |
| `B=1` | All `2K` jobs execute serially regardless of the nominal issue width. |
| `B>2K` | Admission is capped at the program length; the formula still gives `K` when `W>=2`. |
| `W>B` | Effective per-cycle throughput is bounded by `B`, as used in the exact formula. |
| `W=1` | Time `2K` for every window; relative to its own unrestricted baseline `2K`, every nonnegative approximation threshold is `B_epsilon=1`. The `q=floor(epsilon*K)` formula is not applied. |
| `epsilon=0` | Exact saturation window is `K+1` for every `W>=2`. |
| `epsilon>=1` | Window one suffices and is minimal. |
| `K=0` | Outside this nonempty-family statement; no assertion above uses this case. |

## Independent evidence

`approximate_saturation_audit.py` imports only the independent time-assignment
solver. It checks all `1<=K<=10` and all `1<=B,W<=2K+2`: 2,020 exact-optimum
comparisons, each accompanied by direct ROB replay of the explicit construction.
All passed. The included range covers `K=1`, `B>2K`, `W=1`, and `W>B`.

It also checks 1,185 exact approximate thresholds across all those widths
`W>=2` and slack values `q=0,...,K+2`. Every regime, including zero slack and
`epsilon>=1`, agrees with the general formula and its width-two specialization.
Rational test values `epsilon=q/K` realize the stated floor regimes exactly.
General real `epsilon` is covered by the written floor argument, not by a claim
of exhaustive numerical testing. Exact source hashes and run metadata are in
`approximate_saturation_results.json`.
