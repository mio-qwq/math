# Independent review: bounded excess window and total idle slots

Construction proposed by the main agent after the one-extra-entry
tiling theorem. The theory subagent independently checked the strip
bounds, clamped boundaries, and exact finite-state reduction below.
Decision: **ACCEPTED as a written proof**. This note makes no Lean
verification or historical novelty claim, and introduces no new
large-scale computation.

## 1. Definitions and range

Use zero-based job indices `0,...,N-1`, a forward true-dependency DAG,
positive issue width `W`, and eager ROB capacity `B=W+c` with integer
`c>=0`. Fix a horizon `H>=ceil(N/W)` and put

`S=WH-N>=0`.

The decision problem is whether a legal schedule completes within
`H` cycles. Such a schedule may be extended with empty terminal
actions to exactly `H` cycle positions. Conversely, an `H`-position
schedule finishing all jobs is a within-`H` schedule. Empty actions
are legal here; non-delay is not an assumption.

At the boundary after `t` cycles, let `D_t` be the set of all completed
jobs (including retired jobs), and let `r_t` be the retired prefix
length. Thus `[0,r_t)` is completed and, unless all jobs are complete,
job `r_t` is the first uncompleted job. Define

`d_t=tW-|D_t|`.

This is the total number of unused issue slots among the first `t`
cycles. Along a complete `H`-position trace it satisfies
`0<=d_t<=S`, with `d_0=0` and `d_H=S`.

## 2. The corridor lemma

**Lemma 1.** Every such complete trace satisfies, for all `0<=t<=H`,

`[0,L_t) subset D_t subset [0,U_t)`,

where

`L_t=max(0,tW-c-S)` and `U_t=min(N,tW+c)`.

In particular, all uncertainty about completed jobs is confined to
at most `2c+S` consecutive indices.

**Upper-bound proof.** At the beginning of cycle `t>=1`, the admitted
indices are strictly below `r_(t-1)+B`. Since
`r_(t-1)<=|D_(t-1)|<=(t-1)W`, any job issued in that cycle has index
strictly below `tW+c`. Jobs completed in earlier cycles satisfy a
smaller such upper bound. Thus every completed index lies below
`min(N,tW+c)`. At `t=0` the completed set is empty, so the same statement
holds without referring to a previous cycle.

**Lower-bound proof.** Suppose first that `t<H`, and let the next
cycle issue `W-delta_t` jobs, where `0<=delta_t<=W`. There are

`h_t=|D_t|-r_t`

completed but unretired jobs. They all occupy entries of the current
window. The number of unfinished window entries is therefore exactly
`min(B,N-r_t)-h_t`. Readiness can only reduce the available set, so

`W-delta_t <= min(B,N-r_t)-h_t <= W+c-h_t`.

Hence `h_t<=c+delta_t`. The cumulative unused-slot count after the
next cycle is `d_t+delta_t<=S`. Consequently

`r_t=|D_t|-h_t >= tW-d_t-c-delta_t >= tW-c-S`.

The retired prefix is completed, which proves the lower inclusion.
At the terminal boundary `t=H`, all jobs are completed and `r_H=N`;
the proposed lower bound is `HW-c-S=N-c<=N`, so the terminal case
also holds. This separate argument avoids assuming an extra cycle
after the horizon. ∎

**Boundary checks.** If the next cycle is full, `delta_t=0` yields
the sharper local bound `h_t<=c`. If it is empty, `delta_t=W`; its
cost is charged to the same total budget `S`, so the proof still
holds. Truncating the window at the program end only decreases the
unfinished-window count and strengthens the inequality. Already
finished states during terminal padding also satisfy it. Finally,
`L_t<=U_t` for every `t<=H`: when the upper bound is clipped at `N`,
`tW-c-S<=HW-c-S=N-c<=N`.

## 3. Exact state graph and the parameterized algorithm

For every layer `t`, enumerate sets of the form

`D=[0,L_t) union A`, where `A subset [L_t,U_t)`.

One may additionally discard candidates unless
`0<=tW-|D|<=S`. Keep only the empty set in layer zero and the full
job set in layer `H`.

Place a directed edge from a candidate `D` in layer `t` to a candidate
`D'` in layer `t+1` exactly when:

1. `D subset D'` and the issue set `Q=D'\D` has size at most `W`;
2. every `j in Q` belongs to the current eager window
   `[r(D),min(N,r(D)+B))`;
3. every true predecessor of every `j in Q` belongs to `D`.

Here `r(D)` is the largest completed prefix, computed from the candidate
set itself. The set `Q` may be empty. These conditions are the actual
unit-latency ROB transition conditions, not an approximation to readiness.

**Theorem 2.** A legal within-`H` schedule exists if and only if this
layered graph has a path from the empty initial state to the full
terminal state.

**Proof.** Every legal complete trace lies in the enumerated corridors
by Lemma 1 and obeys all three transition conditions, giving a path.
Conversely, start with the empty operational state and issue each
successive set difference on a graph path. The transition conditions
ensure admission, issue width, and strictly earlier-cycle dependency
availability. Completion adds exactly that difference, maximal in-order
retirement produces `r(D')`, and eager refill gives the next specified
window. Induction realizes the entire path as a legal ROB trace.
The terminal set completes all jobs. ∎

There are at most `M=2^(2c+S)` states per layer. Testing all adjacent
state pairs with ordinary indexed-set and edge scans gives, for example,

`O(H M^2 (N+|E|)) = 2^(O(c+S)) poly(N,|E|)`

time, and polynomial factors of the same form in the space bound.
Candidate enumeration also fits this bound. A path stores an explicit
schedule certificate; absence of a path is an exact dynamic-programming
certificate. The parameter is the excess window plus the total unused
issue capacity, not the full window size.

To keep the layer count polynomial when `H` is binary encoded, first
handle `N=0` directly and answer yes with the sequential schedule whenever
`H>=N`. Every forward program has a legal `N`-cycle sequential schedule
for positive capacity. Only `H<N` needs the state construction. If
`H<ceil(N/W)`, the ordinary work bound already answers no.

## 4. Sharper state counts and the perfect-saturation specialization

The filtered candidate count has the stronger bound

`M(c,S)=sum_(j=c)^(c+S) binomial(2c+S,j)`.

To see this uniformly at the boundaries, embed the clamped strip in
the virtual interval `[tW-c-S,tW+c)` of length `2c+S`. Treat negative
job indices as fixed completed dummy positions and indices at least
`N` as fixed uncompleted dummy positions. A state with cumulative
deficit `d_t` then has exactly `c+S-d_t` selected virtual positions.
Different actual states give different virtual subsets, and
`d_t in [0,S]`. This proves the binomial-sum bound. The dummies are
only a counting injection, not extra instructions or operational states.

When `S=0`, necessarily `N=HW`, and the lemma simplifies to

`[0,max(0,tW-c)) subset D_t subset [0,min(N,tW+c))`,

with exactly `tW` completed jobs. The number of candidates at layer
`t` is exactly

`binomial(a_t+b_t,a_t)`,

where `a_t=min(c,tW)` and `b_t=min(c,N-tW)`. It is at most
`binomial(2c,c)`, including the unique initial and terminal states.
One can also prove this by padding the actual strip with fixed selected
and unselected positions to `c` positions of each kind.

For `c=0`, each layer is the single completed prefix; all full-width
cycles must execute consecutive W-job blocks. For `c=1` and a
nonterminal internal cut `m=tW`, the two candidates are the ordinary
prefix `[0,m)` and the boundary-swapped set
`[0,m-1) union {m}`. Two swapped states cannot occur consecutively:
the next swapped state would require issuing job `m+W`, but the
current window ends at that index exclusively, since its oldest
unfinished job is `m-1` and its capacity is `W+1`. Thus a swapped
state must return to a normal prefix next cycle. Collapsing these
two-step visits recovers exactly the one-block/two-block tiling
theorem in `PERFECT_SATURATION.md`.

## 5. Tightness of the per-layer count

The main agent proposed the following sharpness construction; this
review independently accepts it. Fix `c,S>=0` and choose an integer
`W>=max(1,c+S)`. Take `N=2W-S` independent jobs and horizon `H=2`.
At the middle boundary, the entire virtual strip is real:

`L=W-c-S>=0`, `U=W+c<=N`, `U-L=2c+S`.

For any subset `A` of `[L,U)` whose size `j` lies in `[c,c+S]`, let
`D=[0,L) union A`. Issue exactly `D` in the first cycle. Every selected
job lies in the initial window `[0,W+c)`, and

`W-S <= |D|=W-c-S+j <= W`.

All true dependencies are absent. After that cycle the retired prefix
has length `r>=L`, so `r+B>=L+W+c=N`; the entire remaining program is
admitted. Its size `N-|D|<=W` permits issuing every remaining job in
cycle two. This also covers an empty first action when allowed by the
parameters.

Thus all `M(c,S)` counted subsets occur as middle states of valid
two-cycle traces. The binomial-sum state-count bound cannot be uniformly
reduced merely by discarding states unreachable on horizon-feasible
traces. This is a sharp combinatorial count, **not** an algorithmic
complexity lower bound: these independent instances are easy to solve.

## Review limits and next step

The corridor is a necessary state restriction for traces that finish
within the declared total slot budget. It is not claimed for every
arbitrary full-issue prefix that cannot be extended within the horizon.
Transitions still need exact dependency and window checks; the corridor
alone is not a sufficient graph test.

The review establishes the arbitrary-size written reduction and its
parameter dependence. It has not implemented or formally compiled this
general algorithm. Literature comparison and Lean formalization remain
separate work. No broad enumeration was run for this review.
