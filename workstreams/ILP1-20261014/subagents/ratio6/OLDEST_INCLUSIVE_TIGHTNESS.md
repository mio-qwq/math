# Requiring the oldest job still permits the sharp 5/3 loss

Status: WRITTEN_PROOF, finite independent direct replay passed;
NOVELTY_UNCONFIRMED, not Lean-verified, external independent review pending.
The underlying nine-job single block was already present in R17. This note
makes its poor deterministic trajectory explicit and adds a repeatable family.

## Theorem

At B=4,W=3, even restricting to non-delay policies that issue the oldest
unfinished job at every cycle does not lower the universal worst-case factor
below Graham's 5/3. The same is true with any input-independent additive
constant. The lower bound uses true fan-in at most two and the single causal
policy: issue the oldest job, then the two largest other ready jobs (or all
remaining ready jobs if fewer exist).

This says a necessary property of an optimal schedule need not be sufficient
for a good policy. It does not lower-bound every oldest-inclusive policy.

## Construction

For q>=1, use q consecutive nine-job blocks. In each block use the local
true edges

    1->4, 2->4, 2->5, 5->8.

For each block after the first, give each of its first four jobs the additional
parent which is the previous block's job 8. There are no other edges.
Every true edge is forward, maximum true fan-in is two, and operations remain
unit-time. The construction does not bound fan-out by two.

A legal three-cycle schedule in each block is

    {0,1,2}; {3,4,5}; {6,7,8}.

All cross-block parents complete before a subsequent block starts. Thus
concatenation gives a 3q-cycle schedule. Since N=9q and W=3, the work bound
proves `T*=3q` exactly. Every action displayed is itself oldest-inclusive and
non-delay in the global instance.

The stated fixed policy follows five cycles per block:

    {0,2,3}; {1}; {4,6,7}; {5}; {8}.

To prove the claim without appealing to a search, induct over blocks. At a
new block's clean prefix its first four jobs are ready (cross-block parents
have finished), so the policy selects local 0,2,3. The next oldest is 1 and
the window is [1,5): local 4 is blocked by 1, while 2,3 are already done.
Therefore only 1 is ready. Next all of 4,5,6,7 are ready; the fixed policy
selects 4,6,7. Now the oldest is 5, the window is [5,9), and local 8 is
blocked by 5, so only 5 is ready. At the last cycle the window contains local
8 and possibly the first three jobs of the next block. These future jobs
have local 8 as a parent, so only 8 is ready. Its completion clears the
current block, establishing the induction invariant. The final block is the
same with no future jobs admitted. Thus `T_policy=5q`.

The next block need not wait for the entire previous block under *every*
possible schedule. No such strong separation lemma is being assumed. Only
the displayed bad policy's five-cycle induction uses the boundary dependency;
the lower bound on the offline optimum is independently the work bound.
This distinction avoids needing a three-parent barrier for previous jobs 6,7,8.

Consequently no rho<5/3 can satisfy `5q <= rho*3q + alpha` for all q. The
matching upper bound is classical Graham via R1 augmented-DAG readiness.

## Checks and consequences

`oldest_family.py` independently constructs these graphs and directly checks
ROB admission, retirement, parent availability, non-delay cardinality,
oldest inclusion and the exact deterministic tie rule. Actual q=1..100 checks
cover 200 full traces, N up to 900. `oldest-results.json` records runtime and
source hash. This finite evidence supplements the universal induction.

Adding a true edge 6->8 to the R17 block in an attempt to use a complete
fan-in-two separator fails: direct exact search makes the optimum 4 rather
than 3. The weak policy-specific separator above is sufficient and retains
the original three-cycle optimum. No added jobs or extra cycles are needed.

The stronger R14 fact that *there exists* an oldest-inclusive optimal schedule
is fully compatible with this result. A useful improved guarantee must
constrain the other choices beyond requiring the oldest and maximum issue.
