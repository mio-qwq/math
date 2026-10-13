# Graham's full worst-case ratio survives one excess ROB slot

Status: **WRITTEN_PROOF**, finite computational checks passed, **NOVELTY_UNCONFIRMED**;
not Lean-verified and awaiting independent mathematical review. This note extends
`NONDELAY_RATIO.md`. Classical upper bounds are attributed there.

## Theorem

For every W>=2, with B=W+1, the smallest universal strict multiplicative bound
for arbitrary non-delay R1 schedules is exactly `2-1/W`. The same constant
is necessary even if a fixed input-independent additive constant is permitted.
The lower bound is realized by the single causal policy choosing the W largest
ready indices (or all ready indices when fewer than W exist). The repeated
family has true fan-in at most W-1; hence W=3 needs only two-input operations.

This result concerns the worst policy within the non-delay class, not the
minimax choice of an online policy. It supplies no online impossibility result
against a better choice rule.

## One independent block already attains the strict ratio

Let n=W² and E be empty. The increasing full-width schedule takes W cycles,
which is optimal by the work bound. Partition the first n-1 jobs into W-1
consecutive blocks of B=W+1 jobs. The largest-ready-index policy processes
each block by issuing its W newer jobs, then its oldest job. The last job
n-1 takes one more cycle. Thus its duration is `2(W-1)+1=2W-1`.
This attains `2-1/W` on entirely independent instructions.

A repeated lower bound needs more care: concatenating independent programs
without barriers does not preserve this finite-block ratio.

## A repeated family without additional jobs or cycles

For q>=1, use q blocks of n=W² jobs. All indices in this paragraph are local
to a block. Add the true edge `(n-W)->(n-1)`. For each block after the first,
its first B jobs have every job among the previous block's final W-1 jobs
`n-W+1,...,n-1` as a true parent. There are no other true edges.

All edges are forward. The first B jobs have W-1 parents, the last job has
one parent, and these sets of target jobs are disjoint: `W²-1>W` for W>=2.
So maximum true fan-in is W-1. Fan-out is not bounded by two.

**Barrier.** Write s for the first index of a new block. For j in its first
B jobs, all jobs through s-B=s-W-1 precede j by ROB window edges. The last
W-1 jobs `s-W+1,...,s-1` precede j through the true parent set. The remaining
previous job s-W precedes s-1 by the special true edge. Thus every previous
block job strictly precedes j. Any later new-block job has s as an augmented
window predecessor, so every job of the new block waits for all previous
block jobs. This establishes complete inter-block separation.

**Optimal schedule.** In each block, use W cycles:

1. For t=0,...,W-3, issue `tW,...,(t+1)W-1` (there are W-2 such cycles;
   none when W=2).
2. Issue the W-1 jobs `n-2W,...,n-W-2`, together with job n-W.
3. Issue job n-W-1, together with jobs `n-W+1,...,n-1`.

After step 1 the retired prefix is n-2W. The step 2 ROB window includes all
jobs through n-W, so that action is admitted. At step 3 the oldest unfinished
job is n-W-1; its ROB reaches n-1, and the special parent n-W is complete.
Previous-block parents are complete before this block starts. The schedules
concatenate into qW cycles. The work bound `N/W=qW` proves global optimality.
The displayed schedules are themselves non-delay.

**Poor causal policy.** For k=0,...,W-2, let a=k(W+1). Issue
`a+1,...,a+W`, then issue a. Finally issue n-1. The special edge never changes
these choices: its target is the final job, and its parent n-W lies in the
last full new-jobs action since that action is `n-W-1,...,n-2`. No future-block
job becomes ready before the current block ends, by the barrier. Each action
therefore consists of exactly the W largest ready jobs, or all ready jobs if
fewer remain. The duration is q(2W-1).

It follows that any proposed factor rho<2-1/W with additive constant alpha
would imply `q(2W-1-rho W)<=alpha` for all q, which is false.

**Upper bound.** The ready sets in R1 coincide with those of its augmented
precedence DAG. Thus the classical Graham factor `2-1/W` applies to every
non-delay schedule. Together with the family this proves the theorem.

## Evidence and boundaries

`general_family.py` independently constructs the family and directly replays
explicit admission, retirement, true-parent readiness, non-delay cardinality
and the largest-index priority. It does not call any optimizer or the earlier
completed-set search. Actual checks covered W=2..20 and q=1..10: 190 parameter
pairs and 380 complete schedules, up to 4,000 jobs. `general-results.json`
records the source hash and elapsed runtime. Work-count lower bounds certify
the displayed optimal schedules exactly. The arbitrary-W,q proof is the
mathematical argument above; finite tests are not its substitute.

This is not claimed as a novel scheduling bound. The upper bound is classical;
prior occurrence of this restricted-window tightness construction requires
separate audit. The key implication for this research is decisive even without
novelty: non-delay lifting alone cannot strengthen the classical competitive
constant, even with the smallest positive excess c=B-W=1.
