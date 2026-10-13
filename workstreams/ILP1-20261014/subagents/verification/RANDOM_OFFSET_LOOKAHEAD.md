# Random-offset chunking: a stronger global bound and exact strategy sharpness

The offset construction and sharpness family were proposed by verification
subagent C following the theory agent's deterministic chunk policy. Both
arguments were independently reconstructed and accepted by the theory agent;
the root agent also reviewed the offset upper bound. Status: WRITTEN_PROOF
and INDEPENDENTLY_REVIEWED. Historical novelty is unconfirmed; random shifting
and averaging are standard techniques. No Lean verification is claimed.

The saved independent upper-bound review is in
`../theory/LOOKAHEAD_UPPER_BOUND.md`, commit
`d343d89826ec463a364aebeeaadcd67476e1ff91`; the independently reconstructed
sharpness proof is `../theory/RANDOM_OFFSET_SHARPNESS_REVIEW.md`, commit
`a6be8665150497ecc6c0aca0c6149dad478d139f`.

## Randomized causal policy

Use the eager unit-latency ROB with positive `B,W`, integer `L>=0`, and prefix
lookahead of incoming operands below `min(N,r+B+L)` at retired prefix `r`.
Put `Q=B+L`. Before execution draw one uniform integer `U` from `1,...,Q`,
independently of the fixed input. The first chunk has length `U`; every later
chunk has length `Q`, with terminal truncation. Optimize each chunk exactly
using its visible incoming operands and complete it before starting the next.

Every chunk is at most `Q` instructions long, so all its metadata is visible
at its clear-prefix starting state. External true predecessors are earlier
jobs and already complete. The projected-schedule and legal-concatenation
proofs in `CHUNK_LOOKAHEAD_REVIEW.md` apply unchanged.

The actual callback implementation at `B=4,W=3` is in the theory agent's
`chunk_lookahead.py`, commit `d343d89826ec463a364aebeeaadcd67476e1ff91`.
Its `run_policy(..., initial_chunk_size=U)` implements any selected offset.
Its `run_random_policy(..., rng=...)` makes exactly one uniform
`randrange(1,Q+1)` draw, then invokes the same policy. It receives only the
length, lookahead, and `read_parents`/`issue` callbacks, not a future graph.
The default random source is `SystemRandom`; a seeded generator can be
injected for reproducibility. The mathematical bound assumes that draw is
uniform and independent of the input.

The unmodified policy may split even a wholly visible short program: `N<=Q`
does not imply optimality for a random `U<N`. For instance, three independent
jobs at `B=4,W=3,Q=8` cost two cycles for `U=1,2` and one cycle for the other
six offsets. The deterministic default `U=Q` retains its exact one-chunk
property. These two policies' short-program claims must not be conflated.

## Global expected upper bound

For every fixed nonempty input, choose one fixed optimal non-delay schedule
`S_1,...,S_(T*)`. Its actions are nonempty. Let
`s_t=max(S_t)-min(S_t)`. All jobs in an action lie in one window, so
`0<=s_t<=B-1<Q`.

The internal chunk boundaries for offset `U` are positive integers
`U+mQ<N`, with `m>=0`. Every fixed internal position `c` belongs to exactly
one offset residue `U=1+((c-1) mod Q)`. Therefore it is a boundary with
probability exactly `1/Q`. A boundary crosses action `S_t` precisely when

\[
\min(S_t)<c\le\max(S_t).
\]

There are exactly `s_t` such positions. They are all in `1,...,N-1`; none is
the terminal position `N`. Their residues are distinct because `s_t<Q`.
Consequently an action touches at most two chunks, and the expected number of
extra projected copies of this action is exactly `s_t/Q`. No independence
between different boundaries or different cycles is needed.

The optimal chunk costs are at most the costs of projecting this fixed global
schedule. Summing and averaging gives the stronger instance-dependent bound

\[
\mathbb E_U[T_{\rm offset}]
\le T^*+\frac1Q\sum_{t=1}^{T^*}s_t
\le\left(1+\frac{B-1}{B+L}\right)T^*.
\]

For `N=0`, the schedule and both costs are zero. When `B=1` or `W=1`, all
actions have span zero and this argument gives exact optimality. No adaptive
adversary is permitted to select the input after observing `U`; the statement
is for fixed oblivious inputs and expectation over the policy's randomness.

At `B=4,W=3`, the global randomized upper bound improves to `1+3/(L+4)`.
Together with the repeated hidden-bit family, for
`M=max(1,ceil(L/2))` one obtains

\[
1+\frac1{2(M+2)}\le\rho_R(L)\le1+\frac3{L+4}.
\]

The deterministic bound remains `rho_D(L)<=1+9/(L+4)`. The previously proved
`Theta(1/(L+1))` order for both optimal competitive excesses is unchanged.
The leading constant of the optimal randomized online class remains open.

## A sharp family for this particular offset policy

Fix `B>=2`, `W>=2`, and put `k=B-1`. Each block consists of two consecutively
listed chains, each of length `k`: the first occupies positions `0,...,k-1`,
the second positions `k,...,2k-1`. Starting with the second block, each chain's
root has both leaves of the preceding block as true predecessors. Every true
indegree and outdegree is at most two. Let there be `q>=1` blocks.

Those two predecessor leaves force strict execution separation between
blocks. Within one block, the window `B=k+1` admits one job from each chain
per cycle: the corresponding jobs have index distance `k=B-1`. Hence every
block takes exactly `k` cycles and `T*=qk` for any `W>=2`.

Cut a single block after relative position `t`, where `1<=t<=2k-1`, and force
the two pieces to execute sequentially. If `t<=k`, the prefix is a chain of
length `t`, while the suffix consists of chains of lengths `k-t` and `k`.
The suffix can still issue one job of each chain together because their root
distance is at most `k`; its exact duration is `k`. The split loss is `t`.
For `t>=k`, the symmetric argument gives loss `2k-t`. Thus

\[
\Delta(t)=\min(t,2k-t),\qquad
\sum_{t=1}^{2k-1}\Delta(t)=k^2.
\]

Assume `Q=B+L>=max(B,2k-1)`. There is at most one chunk boundary strictly
inside any block: two such positions differ by at most `2k-2<Q`. Chunk
boundaries between blocks cause no loss. Because the true predecessor barriers
prevent any inter-block overlap, every chunk's optimum is the sum of the
optima of its block pieces. Consequently the split losses add exactly.

Every internal position is selected with probability `1/Q`, so on this family

\[
\mathbb E[T_{\rm offset}]=qk+\frac{qk^2}{Q},\qquad
\frac{\mathbb E[T_{\rm offset}]}{T^*}=1+\frac{k}{Q}
=1+\frac{B-1}{B+L}.
\]

Together with the global upper bound, this establishes the exact worst-case
competitive coefficient of the **specified offset chunk policy**, including
conventions allowing a fixed additive constant, whenever the stated threshold
holds. Letting `q` grow removes every such constant. The threshold above is
the theory agent's independently checked strengthening of the originally
proposed `Q>=2k` condition.

At `B=4,W=3`, the threshold is already `L>=1`, so this policy's coefficient
`1+3/(L+4)` is exact for every such `L`. This is not a lower bound for the
best online policy: the sharpness family itself is optimally scheduled by
issuing both ready chain jobs every cycle. The loss results from this policy's
voluntary sequential chunk boundaries.

For `B=4,L=0`, the threshold fails. With one six-job block the four offset
costs are `[4,5,6,5]`, giving ratio `5/3`, strictly smaller than the universal
policy upper bound `7/4`. No claim of sharpness at `L=0` is inferred from this
family. Multiple cuts inside one block can allow its middle pieces to be
rescheduled more efficiently than a sum of isolated-cut penalties.

## Actual exact-average and callback audit

Reproduce from this directory with:

```sh
python random_offset_audit.py --primary-directory ../theory
```

The independent code computes each offset's chunk optimum with the separate
time-variable CSP. It invokes the primary's actual random wrapper using an
enumerated draw result for every `U`, and uses its own persistent eager ROB
environment to reject any out-of-frontier operand read or illegal action.
Uniform means are exact `Fraction` values over all offsets, not estimates.

- Every forward DAG on `0<=N<=4` at `L=0,1,4`: 228 graph/lookahead cases and
  all 1,292 offsets.
- Seed `2026101413`: 50 binary-input random programs with `5<=N<=15` and
  `0<=L<=7`. Combined with the exhaustive range, there are 278 cases and
  1,672 exact-offset callback runs, 8,697 checked reads, and 5,578 issue cycles.
- For every case, the expected projected cost is exactly
  `T*+sum(action spans)/Q`; the actual policy expectation is no larger.
- Sharpness tests use `2<=B<=6`, `W=2,3`, `1<=q<=3`, and the distinct values
  `Q=max(B,2k-1),max(B,2k),3k+1`: 84 resource cases and all 624 offsets.
  Every mean equals the claimed sharp value, including `Q=2k-1`.
- The below-threshold `B=4,L=0` control reproduces the four costs above.
  Three malformed offsets are rejected before reads or issue. A real
  `Random(2026101413)` wrapper run also succeeds, drawing first size two.

All checks passed in 0.3187919880001573 seconds. The exact finish time, counts,
seed, bounds, and source hashes are in `random_offset_results.json`. The final
primary source hashes were unchanged throughout the run:

- `chunk_lookahead.py`:
  `13b3374f6e9bbe388e5865d93b96f0053861db1b725e1e53e26fad427b2da5ed`.
- `forced_segment_dp.py`:
  `6798ccdf97277f16731bafb86afcd68fe5623620b8541304c750057b0093a21d`.

The independently inspected source reads exactly the current chunk, shifts
only already-complete earlier operands out of its masks, and issues all local
actions before advancing to the next chunk. Its new randomness affects only
the initial size; no unavailable dependency information enters that draw or
the planner. Finite tests supplement the arbitrary-size proofs above.
