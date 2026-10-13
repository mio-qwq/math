# Repeating the hidden choice without separator cycles

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED** by the theory role;
**NOVELTY_UNCONFIRMED**. The actual-model structural/offline/admission primitives are now Lean verified for arbitrary q; the probability and complete observation-history proof remain written.
Indices are zero-based. This note strengthens the finite strict lower bounds
at B=3,W=2 to the competitive definition allowing a fixed additive constant.
Independent reviews are `subagents/theory/REPEATED_GADGET_REVIEW.md` and `subagents/verification/REPEATED_PAIR_REVIEW.md`. The latter also checks all127 bit inputs through q6,8256 cross-block predecessor pairs and a full64-leaf probability tree. Formal scope is documented in `formal/REPEATED_GADGETS.md`.

## Construction and separation

Fix q>=1 and a bit vector x in {b,c}^q. Block k has four instructions

    a_k=4k, b_k=4k+1, c_k=4k+2, d_k=4k+3.

Within a block the only true edge is x_k -> d_k. For k>0, give each of
a_k,b_k,c_k exactly the two true predecessors c_(k-1),d_(k-1).
There are no other true edges. Each program has N=4q, every true indegree
is at most two, and the program is a forward DAG. Roots here mean roots
of the current block once earlier blocks have completed, not global roots.

**Separation lemma.** Every instruction of block k+1 issues strictly after
every instruction of block k has completed, under any legal schedule.

For the first instruction a_(k+1), the artificial window edges at B=3
include a_k and b_k as predecessors, while the true edges include c_k,d_k.
For b_(k+1), window edges already cover a_k,b_k,c_k, and its true edge
from d_k covers the last instruction. For c_(k+1), window edges cover
all four preceding instructions. Finally d_(k+1) has a predecessor in
its own block, so cannot precede completion of the previous block either.
The static/operational equivalence proves the lemma for actual ROB traces.
This argument applies to schedules with idle or underfilled cycles too.

After a block finishes, all earlier blocks have finished, no later job
has issued, the completed set is exactly a program prefix, and the next
window contains precisely the three next-block roots. Admission may have
made some of these roots visible earlier, but they could not execute.
No extra separator instruction or separator cycle is used.

**Offline optimum.** Every block needs at least two cycles by width, and
separation makes these costs add, so T*>=2q. For block k, issue
{a_k,x_k} and then the other root together with d_k. Each block takes two
cycles and returns to the next clear-prefix state; hence T*=2q.

## Indistinguishability and randomized lower bound

Choose x_0,...,x_(q-1) independently and uniformly before execution.
This is an oblivious distribution over fixed finite programs, not an
adversary that changes the input after observing the scheduler's random bits.
Fix any online randomized policy, which may know q, use arbitrary internal
state, correlate its random choices, and inspect all admitted operand lists.

Before the first action of block k, its d_k has not been admitted: the
oldest incomplete job is a_k, and B=3 exposes only a_k,b_k,c_k.
All previously visible instructions and operand lists, including any
earlier admission of these three roots, are independent of x_k.
The incoming edges of future-block roots refer to c_k,d_k by their fixed
identities, not to the hidden predecessor of d_k. In fact those roots are
not admitted at this decision, and even their identities would not reveal
x_k. Thus conditional on the complete preceding observation history and
the policy's random state, x_k is still a fair independent bit.

Completion of this block in two cycles forces the first action to equal
{a_k,b_k} if x_k=b_k, or {a_k,c_k} if x_k=c_k. Admission forces a_k;
data readiness forces x_k; the width-two bound leaves no extra slot.
These two actions are distinct. Consequently the conditional probability
of a two-cycle block is at most 1/2. Every other execution costs at least
three cycles (or does not terminate). Idle and underfilled choices do not
improve the bound. The expected duration per block is at least 5/2.
By separation and linearity of expectation, averaging over fixed inputs
and policy randomness gives

    average_x E[T_policy(P_x,3,2)] >= (5/2)q.

Therefore, for every q, some fixed input has E[T_policy]>=5q/2 and T*=2q.
No independence between a policy's choices in different blocks was assumed.
The proven fair-younger policy attains 5q/2 on every member of this family.

## Competitive constants

Suppose a policy satisfied E[T(P)] <= c T*(P)+alpha for all finite inputs,
where alpha is a fixed finite constant independent of input length. The
preceding inputs give (5/2)q <= 2cq+alpha for every q. Letting q grow forces
c>=5/4. Together with the global strict upper bound, the optimal randomized
competitive factor at these fixed resources is exactly 5/4 even when an
additive constant is allowed. This statement is against oblivious inputs.

For deterministic policies, choose each x_k to disagree with the uniquely
successful first action, if one was chosen. This recursively determines
one fixed complete program because x_k is not observed before that action.
Every block costs at least three cycles. Equivalently, induct on the fixed
prefix and complete the unseen suffix after computing the deterministic
decision. Hence some input has T>=3q and T*=2q. Graham's strict 3/2 upper
bound then also establishes the deterministic factor 3/2 with additive
constants. This is a deterministic adversary construction, not an adaptive
adversary claim against a randomized policy.

## Scope

This construction uses two-input operations and fixed-order ROB admission.
Its true outdegree need not be at most one. It strengthens only the B3,W2
lower bounds; it does not establish composition of every hidden-subset
family at arbitrary resources. Product-distribution and direct-sum methods
are classical; priority of this exact separator-free ROB instance is not
asserted. The original four-job Lean obstruction does not by itself verify
this arbitrary-q argument.
