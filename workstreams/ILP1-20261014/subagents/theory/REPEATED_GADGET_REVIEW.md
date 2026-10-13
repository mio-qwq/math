# Independent review: repeated four-job information gadgets

Construction proposed by the main agent. This is the theory subagent's
independent mathematical review, including attempted failure modes.
Decision: **ACCEPTED as a written proof under the stated observation
and ROB semantics**. No new Lean claim or novelty claim is made.

## Precise family

Fix `q>=1`, `B=3,W=2`, and `N=4q`. Number blocks `k=0,...,q-1`, with

`a_k=4k+1`, `b_k=4k+2`, `c_k=4k+3`, `d_k=4k+4`.

For each block independently choose a hidden bit `z_k` selecting
either edge `b_k->d_k` or edge `c_k->d_k`. For every `k>=1`, give
each of `a_k,b_k,c_k` the two true predecessors `c_(k-1),d_(k-1)`.
There are no other true edges. Every true indegree is at most two.
The total length and this family may be known to the policy; the bits
and unadmitted operand lists are not known.

## 1. The block barrier is real and costs no extra instruction

Under the exact ROB precedence reduction, job `j` additionally depends
on every `i<=j-3`. Thus, for `k>=1`:

* `a_k` has artificial predecessors through `b_(k-1)`, and the two
  added true edges supply `c_(k-1),d_(k-1)`.
* `b_k` has artificial predecessors through `c_(k-1)`; the added
  edge from `d_(k-1)` supplies the remaining preceding-block job.
* `c_k` already has artificial predecessors through `d_(k-1)`.

Every root of block `k` therefore issues strictly after **all** jobs
of block `k-1` complete. Job `d_k` depends on one of these roots and
cannot circumvent this barrier. Consequently two different blocks
never issue jobs in the same cycle, regardless of idling, underissue,
or out-of-order execution within a block.

The added edges do not obstruct a two-cycle schedule inside a block:
after the preceding block completes, issue `a_k` and the selected
parent of `d_k`, then issue the other root and `d_k`. Each block takes
two cycles, and the next block begins in the immediately following
cycle. The width-two work bound gives `T*>=N/2=2q`, so `T*=2q`.
There are no extra barrier instructions or uncounted barrier cycles.

## 2. The hidden bit remains hidden at the relevant decision

Admission of `d_k=4k+4` at `B=3` requires retirement through
`d_k-B=a_k`. Hence `d_k` cannot be admitted before the first cycle
that issues a job of its block: its own oldest root has not yet issued.
The barrier also prevents `a_k` from executing speculatively before
the preceding block finishes.

The initial visible instructions of the block are precisely
`a_k,b_k,c_k`. Their operand lists depend only on the fixed indices
`c_(k-1),d_(k-1)`, not on `z_k`. Any next-block roots that might become
visible later also have the same fixed predecessor indices `c_k,d_k`
for both choices of `z_k`. Such operand lists reveal no extra bit.
Before the first block action, those next-block roots cannot be
admitted anyway: their admission requires a prefix inside block `k`
to retire.

With independent uniform bits, conditioning on the entire earlier
execution history, the policy's random state, observed results, or
knowledge of `N` leaves `z_k` uniform at this first decision. Operations
and initial values can be chosen identically across the family; only
the unadmitted instruction `d_k`'s selected predecessor index varies.

If the policy issues just `a_k` to reveal `d_k` next cycle, it has
already spent one cycle on only one of four jobs. Three jobs remain
and require at least two more width-two cycles. Such information
gathering is therefore included in the lower bound, not an escape.

## 3. Randomized lower bound, including an additive constant

The unique first actions that can complete a block within two cycles
are `{a_k,b_k}` when the parent is `b_k`, and `{a_k,c_k}` when it is
`c_k`. These are distinct. Every other first action, including idling
or underissue, requires at least three block cycles. Conditional on
the earlier history, success probability is at most one half, so the
expected number of cycles occupied by block `k` is at least `5/2`.

By the strict block barrier, the total makespan is at least the sum
of these block durations, even when extra idle cycles occur between
blocks. Taking expectations gives at least `5q/2` under the product
distribution on the `2^q` fixed input programs. Therefore, for every
randomized online policy, some fixed program of length `4q` has

`E[T]>=5q/2=(5/4)T*`.

This uses an oblivious input distribution; the adversary does not
observe realized policy random bits. Given any proposed guarantee
`E[T]<=rho T*+alpha` with finite input-independent `alpha` and
`rho<5/4`, choose an integer `q` with
`(5/2-2rho)q>alpha`. The corresponding fixed-program lower bound
contradicts that guarantee. Thus the asymptotic randomized ratio is
also at least `5/4`. The independently reviewed global upper bound
from `RANDOMIZED_FIVE_QUARTERS.md` has no additive term and matches it.

## 4. Deterministic strengthening

The uniform product distribution alone gives `5/4`, not `3/2`, for a
deterministic policy. The stronger deterministic result requires a
separate fixed-program construction.

Fix a deterministic policy and `q`, hence also the total known length.
Construct the bits in block order. Before the first action in block
`k`, all observations are independent of its still unchosen bit by
Section 2. Choose the bit whose required two-cycle first action was
not selected. At least one such bit always exists; if neither required
action was selected, either bit works. Earlier chosen bits are never
changed, and all later root operand lists are fixed independently of
later bit choices. The resulting full bit string specifies one fixed
legal input program on which every block requires at least three
cycles. Hence `T>=3q=(3/2)T*`.

This construction is permitted for a worst-case deterministic input:
it determines one fixed program using the known policy, not a
run-time modification of an already selected program. The same
large-`q` argument rules out every asymptotic deterministic ratio
strictly below `3/2`, even with an additive constant.

## Review conclusion and limits

The original concern was that future-block admission or a hidden
pipeline overlap might break additivity. The explicit artificial
predecessor sets rule out overlap, and the exact admission threshold
for `d_k` rules out early observation. The argument permits known
program length, arbitrary policy memory, idling, and randomized
history-dependent decisions. It assumes the declared prefix-only
observation model and strict next-cycle dependency availability.

This review establishes the written argument's scope; it does not
claim an independently compiled Lean proof of the observation process
or the probabilistic lower bound.
