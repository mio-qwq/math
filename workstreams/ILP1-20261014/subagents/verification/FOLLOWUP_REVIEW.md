# Follow-up independent review

Date: 14 October 2026, Singapore. Reviewer: verification subagent C.
This review covers the new exact chain-family minimax/advice statement, the
compact unrestricted-issue saturation certificate, and a source-level semantic
inspection of two Lean modules. The reviewer did not recompile Lean during
this follow-up and makes no independent bibliographic or originality claim.

## Exact single-hidden-root chain minimax and advice

Theorem 6 of `subagents/theory/ONLINE_LOWER_BOUND.md` is accepted in its stated
prefix-only observation model, with a program fixed independently of scheduler
randomness. Set `L=ceil((B-W)/(W-1))` for `B>W>=2`.

A first action, including an empty or underfull one, can allow an `L+1`-cycle
completion only when it contains the oldest root `0` and hidden root `x`.
If it contains `0`, it covers at most `W-1` of the `B-1` possible hidden roots;
otherwise it covers none. Therefore a uniform hidden root gives any randomized
policy success probability at most `(W-1)/(B-1)`. Failure costs at least one
additional cycle. This proves the lower bound on some fixed program, without
using an adversary that observes the scheduler's random choices.

The proposed upper policy is genuinely online: initially choose root `0` and
a uniform `(W-1)`-subset of the remaining roots. Retiring `0` admits the first
suffix job, whose visible operand reveals `x`. If `x` was selected, run the
chain while filling each cycle with up to `W-1` smallest unfinished roots. If
it was missed, first execute `x` plus available roots in the second cycle, then
run that continuation. The root capacity inequality is `B<=W+L(W-1)`.

The sampled first action need not contain the first `W-1` roots. The correct
general admission invariant in the hit case is that before suffix job `k`,
the retired initial prefix has length at least
`min(B,1+(k-1)(W-1))>=k`. The extra root-only cycle in the miss case only helps.
Thus the attained makespan is exactly `L+1` on a hit and `L+2` on a miss.
For every fixed `x`, the hit probability is `(W-1)/(B-1)`, proving exact ratio

`1 + (B-W)/((B-1)(L+1))`.

For fixed-length deterministic advice, each message's initial action covers
at most `W-1` hidden roots. The necessary message count is therefore
`ceil((B-1)/(W-1))`. Partitioning roots into groups of that size bound achieves
the count; pad the first action as needed and use the hit continuation. The
binary bit count `ceil(log2 ceil((B-1)/(W-1)))` is correct. This is a family
result, not a general-program advice characterization.

Independent finite verification covers all `3<=B<=12, 2<=W<B`: 40,830 explicit
policy replays verify the exact hit/miss durations and expected ratio with
rational arithmetic for every hidden root, and 440 advice-encoding replays
attain the offline optimum. Arbitrary first-action lower-bound exclusions were
already separately checked in `sharpened_chain_results.json`; those runs were
not repeated here.

## Compact unrestricted-issue saturation certificates

Reviewed `src/resources.py` SHA-256:

`d3e8deaac531f3353ce68afd08c8c93f9203d2b6b462515bc957956f175f87a3`.

The builder and checker are accepted for nonempty forward-DAG programs and
the advertised unrestricted issue regime `W=N`. The checker does not need to
trust the builder's dynamic program:

1. A true-dependency path of length `H` proves every schedule needs at least
   `H` cycles, even at unrestricted window size.
2. Direct ROB replay verifies an `H`-cycle schedule at the claimed `b`, so
   unrestricted optimum equals `H` and window `b` achieves it.
3. If `b>1`, a valid augmented path at window `b-1` of length greater than `H`
   rules out every smaller window because smaller windows add constraints.
   If `b=1`, there is no smaller positive window to exclude.

Strictly increasing path vertices prevent repetitions, and every link is
checked as either a supplied original edge or an allowed synthetic edge.
The original path accepts only original edges. The replay independently checks
dependencies, admission, issue width, retirement, uniqueness and completion.

An implementation complexity defect was caught during review: the initial
schedule construction scanned all jobs for each cycle, taking `O(N*H)` time.
The primary agent replaced it with one allocation of `H` buckets and one pass
over jobs before the final audited hash above. The revised implementation has
the advertised `O((N+|E|) log N)` construction time under the standard unit-cost
index/arithmetic convention. The schedule and two paths contain `O(N)` job
indices, in addition to the embedded instance `O(N+|E|)`; checking takes linear
time in that instance and witness representation.

New independent checks compared saturation against the separate time-assignment
CSP for 350 fixed-seed random programs with `6<=N<=14`. All agreed. Twenty-four
negative controls reject invalid resource bounds, altered duration, empty,
repeated, backward, out-of-range or false-edge paths, incomplete, repeated,
unready or unadmitted schedule jobs, trailing cycles, invalid dependencies, and
a spurious smaller-window obstruction at `b=1`.

The checker certifies its embedded `n` and `edges`; a caller intending to verify
a separately supplied program must compare that instance. This is a mathematical
certificate checker, not an authentication mechanism or a full hostile-input
schema validator. No false mathematical certificate was accepted in this audit.

## Semantic inspection of the Lean bridge

Reviewed files and SHA-256 values:

| File | SHA-256 |
|---|---|
| `formal/ROBModel.lean` | `1a01548dfa80474fd6cfcffb5acada166c558b95855de7fea2fe4cce94fc896c` |
| `formal/ROBOperational.lean` | `359eac6b66e7cce5483f877992a95e122de59e8be2e4e03994206830feecc4a6` |

No semantic mismatch was found between these definitions and the R1 model:

- Completion before cycle `c` is exactly `t_i<c`, excluding same-cycle operand
  forwarding. The retirement prefix ends at the first unfinished instruction.
- Canonical admission is `min(n, retired+B)`. Completed jobs beyond the retired
  prefix still occupy entries because this expression does not subtract them.
- `ROBStep` admits only unfinished window jobs with already-complete parents;
  completion is the union with the current batch, followed by maximal prefix
  retirement and eager admission for the following cycle.
- Lane injection expresses per-cycle capacity without an unintended fixed-lane
  dependency restriction. The per-cycle lane witnesses are combined into a
  per-job witness using each job's single assigned issue time.
- `legal_iff_operational` links time assignments to explicit traces;
  `feasible_iff_finished_trace` identifies the horizon with full retirement at
  that cycle boundary. Empty programs and positive horizons for nonempty
  complete programs are handled consistently.

The traces are parametrized by a total finite-job time assignment, so they
represent executions in which every job eventually issues. Infinite starving
policies are not represented, which is appropriate for complete-schedule
feasibility but should not be misdescribed as a formalization of all online
policy behavior. The modules do not formalize the Python solver, operation
semantics, online lower bounds, or the saturation builder.

There are no placeholder proof tactics or new axiom declarations in the
inspected sources. The `admit` identifier in `ROBStep` is an admission-equation
field, not an `admit` proof tactic. The files print their axiom dependencies;
actual compilation and axiom output remain the separate primary/formal-agent
evidence. This review must not be counted as another Lean compilation run.

## Additional review: classical list bound and global deterministic ratio

The subsequent Theorem 7 and Corollary 8 in the theory note are also accepted
by direct proof inspection. Following latest-issued predecessors from a final
job constructs a path of length `ell<=h_B`. Every cycle without a path job
contains an available but unissued next path job and must therefore be full
under a non-delay policy. Counting gives `N>=W(T-ell)+ell`, and hence

`T<=floor((N+(W-1)h_B)/W)<=(2-1/W)T*`.

ROB readiness equals augmented-DAG readiness, so this argument does not grant
the scheduler unseen information. At fixed `B=3,W=2`, the four-job pair gives
the matching deterministic lower bound `3/2`; the global deterministic minimax
ratio is therefore exactly `3/2`, including the disjoint-edge subclass. The
global randomized value at those fixed resources is not determined: the
reviewed lower and upper bounds remain `5/4` and `3/2`. The upper bound is
explicitly classical in the theory note; this review is not a priority claim.
