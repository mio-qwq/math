# Exact horizon feasibility near the width/work bounds

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED**,
**NOVELTY_UNCONFIRMED**. The completed-set strip and cardinality interval
are **LEAN_VERIFIED** for actual ROB traces in `formal/ROBCorridor.lean`.
The binomial count, parameterized algorithm and Python implementation are
not Lean verified. The primary agent proposed the general idle-slot
extension after the B=W+1 perfect-saturation tiling result.

## Definition and theorem

Assume a finite forward program of N jobs, positive W<=B, and a proposed
integer horizon H with WH>=N. Write

    c=B-W, S=WH-N.

Here c is the excess of window capacity over issue width; S is the total
number of unused issue slots in any H-cycle execution of exactly N jobs,
including terminal idle padding. These differ from the earlier parameter B.
For W>B, first apply the proved effective-width identity W'=min(W,B).

**Corridor theorem.** In every legal trace completing by H, after padding
idle cycles to H and writing D_t for completion after t cycles, 0<=t<=H,

    [0,max(0,tW-c-S)) subset D_t subset [0,min(N,tW+c)).

Thus only a strip of at most 2c+S indices around the nominal cut tW can
vary. In addition tW-S<=|D_t|<=tW. The number of candidate completed sets
at any layer is at most

    M(c,S) = sum_{j=c}^{c+S} binomial(2c+S,j) <= 2^(2c+S).

The legal H-horizon reachability problem can therefore be solved in
2^{O(c+S)} poly(N,|E|) time without enumerating subsets of all B ready jobs.
For S=0 the bound improves to binomial(2c,c). This is a parameterized
feasibility algorithm; it is not a polynomial general optimum algorithm.

## General proof of the strip bound

Let r_t be the first incomplete index (N at completion), d_t=tW-|D_t| the
unused slots in the first t cycles, and h_t=|D_t|-r_t the number of completed
but unretired instructions. Every completed but unretired instruction is
inside the current ROB: admission is an ordered prefix and retirement only
advances, so old admitted entries stay inside the current frontier window.

For t<H, write delta_t=W-|D_(t+1)\D_t| for the next cycle's unused slots.
These quantities are nonnegative, and d_t+delta_t=d_(t+1)<=S because the
whole padded execution has exactly S unused slots. The current number of
unfinished window entries is min(B,N-r_t)-h_t. Hence

    W-delta_t <= min(B,N-r_t)-h_t <= W+c-h_t.

Even when the next cycle is empty (delta_t=W), this count is valid. It
implies h_t<=c+delta_t and therefore

    r_t=tW-d_t-h_t >= tW-c-d_t-delta_t >= tW-c-S.

At t=H, r_H=N=HW-S>=HW-c-S, so the final layer also satisfies the lower
bound. Every index below r_t is complete, proving the left containment.

For the right containment, any job completed by time t issued in a cycle
s with 1<=s<=t. Its index was strictly less than r_(s-1)+B. Since
r_(s-1)<=|D_(s-1)|<=(s-1)W, its index is strictly less than
sW+c<=tW+c. Intersect with the actual index range [0,N). This proves
the upper containment, including traces with idle cycles and early finish.

## Counting candidate states and exact transitions

Consider the untruncated length-(2c+S) interval
[tW-c-S,tW+c). Regard any negative indices as fixed completed positions,
and any indices >=N as fixed uncompleted positions. There are exactly
c+S-d_t completed positions in this virtual interval. Since 0<=d_t<=S,
each actual D_t injects into a subset of size in {c,...,c+S} of a fixed
(2c+S)-element set. Boundary truncation only reduces the possibilities.
This gives M(c,S), and gives binomial(2c,c) when S=0.

For each t generate precisely the sets with the two fixed prefix/suffix
conditions and cardinality tW-S<=|D|<=tW. At t=0 retain only the empty set.
Join a candidate D at layer t to a candidate D' at layer t+1 exactly when
D subset D', |D'\D|<=W, and every job in D'\D is admitted and has all true
predecessors in D. An empty difference is allowed. Compute admission from
the actual first missing index of D, not from the nominal cut tW.

Every such edge is an actual ROB transition, so a path ending at D_H=all
gives a legal H-cycle trace. Conversely the corridor theorem places every
legal trace finishing by H (padded if necessary) among these candidates,
and every transition survives the checks. Reachability is therefore sound
and complete, and predecessors reconstruct a valid schedule.

There are at most M candidates per layer and M^2 candidate pairs between
successive layers. Direct mask or set operations, true-predecessor checks,
and schedule reconstruction contribute only polynomial factors in N,|E|.
No step enumerates 2^B possible issue subsets. If H>=N, the sequential
schedule directly proves feasibility; otherwise H<N, so the number of
layers is polynomial even if H was supplied in binary. This establishes
the stated fixed-parameter bound in c+S. Arithmetic-operation estimates
include polynomial costs for indices/masks rather than treating arbitrary
precision bit operations as constant time.

## Relation to the one-extra-entry tiling theorem

For c=1,S=0, the only two candidate states at a block boundary tW are the
clear prefix and the prefix through tW-2 together with completed job tW.
The second has one hole at tW-1. It cannot transition to another one-hole
state in a full cycle: that would require issuing job tW+W, while its
current exclusive admission bound is (tW-1)+(W+1)=tW+W. Thus every hole
state is surrounded by clear states, recovering the one-/two-block macros.

For S>0 this theorem does not claim that appending dummy instructions
reduces feasibility to S=0. That shortcut is false: at W3,B4,N5, the sole
true edge0->1 permits two cycles, whereas appending one independent job
gives N6 and needs three cycles. The explicit slack-dependent strip handles
the original length directly.

## The candidate count is sharp

For any c,S>=0 choose W>=max(1,c+S), let N=2W-S, H=2, B=W+c,
and take an empty true dependency graph. At t=1 the whole strip
[L,U)=[W-c-S,W+c) is inside [0,N). For every subset A of this strip
with c<=|A|<=c+S, issue D=[0,L) union A in cycle one. All selected
jobs are initially admitted, and W-S<=|D|<=W. Its retired prefix
r is at least L, so r+B>=N; every remaining job is then admitted.
There are N-|D|<=W remaining jobs, which all issue in cycle two.

Thus all M(c,S) distinct candidates occur as middle states of actual
horizon-feasible traces on one input. This proves a sharp state-count
bound, not a computational lower bound: independent jobs are easy to
optimize. Theory independently reviewed this construction in
`subagents/theory/SLACK_CORRIDOR_REVIEW.md`, section 5.

## Implementation and open coverage

`src/corridor.py` implements the layer-candidate algorithm, normalizes
oversized resources using the model's proved caps, and returns a schedule
or exact infeasibility. Layer sizes and pair counts are reported so the
parameter dependence is inspectable. Root tests cover all76 forward DAGs
through N4 over10,326 resource/horizon cases. Independent verification
compared4,797 cases with a time-variable CSP, replayed1,921 feasible
witnesses, and checked9,384 boundary inequalities on2,050 legal time maps.
Saved ranges, seeds, timings and hashes are in `evidence/corridor-root.json`
and `subagents/verification/corridor_results.json`; datasets overlap.
The previous Python solver remains a separate completed-set optimization
method and is not called by this implementation.

The actual-model strip proof was freshly compiled in Lean4.34.1, Std only,
with25 new audited work/count/corridor endpoints and standard axioms only;
see `formal/ROB_CORRIDOR.md` and `evidence/lean-corridor-root/receipt.json`.
Its lower-bound proof uses the equivalent split-capacity argument
N<=r_t+B+(H-t-1)W, with a separate terminal-layer case. The virtual-subset
injection, binomial count and its sharpness, finite-layer algorithm
completeness, and runtime bound remain written proofs. Banded/discrepancy
precedences and finite-state sequencing have substantial prior art.
Historical priority of this particular c+S parameterization is unresolved.
