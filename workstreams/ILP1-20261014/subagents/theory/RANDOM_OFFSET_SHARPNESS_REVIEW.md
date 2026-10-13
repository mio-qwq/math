# Independent review: sharpness for the random-offset chunk policy

Construction proposed by the verification agent. The theory agent
independently checked the schedules, cut losses, block additivity and
averaging argument, and slightly weakened the sufficient threshold from
`Q>=2(B-1)` to `Q>=2(B-1)-1`. Decision: **ACCEPTED as a written proof**.
This note concerns the specific policy in `LOOKAHEAD_UPPER_BOUND.md`;
it does **not** determine the best possible online competitive ratio.
No historical novelty or Lean verification is claimed.

## 1. A family that an all-ready policy already schedules optimally

Fix `B>=2`, `W>=2`, put `k=B-1`, and choose `q>=1`. Each consecutive
block contains `2k` jobs: first a chain of `k` left jobs, then a chain
of `k` right jobs. For every block after the first, both chain roots
have the two preceding block leaves as true parents. Every other
job has its preceding same-chain job as sole true parent.

Maximum true indegree and outdegree are at most two. Both roots of
a later block depend on both previous leaves, so every later-block
job follows every previous-block job strictly. This is a true-edge
barrier, independent of the ROB.

Inside one block, issue its `i`th left and `i`th right jobs together
for `i=0,...,k-1`. Before pair `i`, the oldest uncompleted index is
the left job `i`, and the corresponding right job has index `k+i`.
Their difference is `k=B-1`, so both lie in the window of capacity
`B`. Each predecessor issued earlier. The width requirement is only
two. Each block takes exactly `k` cycles, attaining its chain lower
bound. Therefore the global optimum is `qk`.

In fact the policy that simply issues all ready jobs attains this
optimum without extra lookahead. This observation makes the scope
clear: any loss below is caused by the chosen chunk barriers, not by
unavoidable hidden information on these particular instances.

## 2. The exact loss from one internal cut

Cut a block after its first `t` jobs, where `1<=t<=2k-1`, and require
completion of its prefix before executing its suffix.

If `t<=k`, the prefix is a chain of length `t` and takes `t` cycles.
The suffix consists of chains of lengths `k-t` and `k`. They can be
run together while both are nonempty, then finish the longer chain,
taking `k` cycles. This schedule obeys the ROB: the distance from
the current left job to its paired right job is `k-t<=B-1`; once
the left chain finishes, the remaining right suffix is sequential.

If `t>=k`, the prefix consists of chains of lengths `k` and `t-k`,
and takes `k` cycles by the same pairing argument. The suffix is a
single chain of length `2k-t`. In either case chain lower bounds
match the displayed schedules exactly. The extra cost relative to
the uncut block is therefore

`ell(t)=min(t,2k-t)`.

In particular,

`sum_(t=1)^(2k-1) ell(t)=k^2`.

The middle cut `t=k` causes a loss of `k`; the other cut losses are
the two copies of `1,...,k-1`.

## 3. Additivity across blocks and the random offset

Use `Q=B+L` and assume `Q>=2k-1`. The possible internal cut positions
of one block range from 1 to `2k-1`, whose extreme difference is
`2k-2<Q`. Two grid cuts, which are `Q` apart, cannot both lie strictly
inside the block. Each block is therefore uncut or has precisely one
internal cut. A boundary exactly at a block endpoint has no cost.

Even if a policy chunk contains the end of one family block and the
start of the next, the true-edge barrier prevents overlap of their
jobs. Removing already completed jobs outside that chunk does not
remove this barrier among its remaining jobs: every next-block root
still waits for each remaining previous-block chain to finish. Thus
the exact optimum of every chunk is the sum of the optimum times
of its family-block pieces. Summing across chunks gives the exact
global cost

`qk + sum_(internal grid cuts) ell(relative position)`.

Choose the initial chunk length uniformly from `1,...,Q`, independently
of the fixed input. Every integer position inside every family block
has probability exactly `1/Q` of being a grid cut. Linearity of
expectation, without any independence assumption between blocks,
therefore gives

`E[T_offset] = qk + q k^2/Q`,

`E[T_offset]/T* = 1+k/Q = 1+(B-1)/(B+L)`.

This matches the universal upper bound for this policy. It is its
exact worst-case expected ratio under the stated range of parameters.
The equality persists for arbitrarily large `q`, so an input-independent
additive constant cannot improve this policy's coefficient either.

## 4. Boundary checks and limits

The sufficient range can be written `Q>=max(B,2B-3)`, since `Q=B+L`
already enforces `Q>=B`. At `B=4,W=3`, equality holds for every
`L>=1`, including `Q=5=2k-1`. The originally proposed safer condition
`Q>=2k` also remains valid.

The next lower endpoint illustrates why a condition is needed. With
`B=4,W=3,k=3,q=1,L=0,Q=4`, the four offset costs are
`4,5,6,5`. Their mean is five, so the ratio is `5/3`, strictly below
the generic upper bound `7/4`. The first offset cuts twice inside
the six-job block; summing independent one-cut losses would overcount.

The width assumption `W>=2` is essential for the paired witnesses.
At width one, every schedule takes the job count, regardless of the
chunk boundaries. Empty programs can be handled separately; this
family uses `q>=1` to define the ratio.

The verification agent reports an independent actual audit of 84
resource/family cases and 624 offsets, including `B=2,...,6`, widths
two and three, one through three blocks, and the strengthened
`Q=2k-1` boundary. It also checks the `B=4,L=0` negative control.
The exact saved audit commit belongs to that agent and should be
cited separately; this review did not rerun those computations.

No lower bound for the optimal randomized policy class follows from
this construction: as Section 1 shows, an elementary all-ready policy
is optimal on the entire family. A better lookahead policy can thus
potentially improve the constant three at `B=4,W=3`; only the current
random-offset chunk policy has been shown sharp.
