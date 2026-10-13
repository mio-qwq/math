# Independent review of the biclique reduction for excess window

Construction proposed by the main agent. This theory review independently
checks the reduction, non-delay-free converse, ROB admission, and the
claimed exact width. Decision: **ACCEPTED as a written proof**. This is
not a novelty decision or a Lean verification. No computational run is
claimed in this review.

## 1. Construction

Take a bipartite graph `G=(U,V,F)` with `|U|=n`, `|V|=m`, and an integer
`1<=k<=min(n,m)`. The source question is whether it contains a complete
bipartite subgraph with `k` vertices on each side. Put

`f=m+k`, `B=n+m+k`, `W=n+m=B-k`, `N=2B`.

The first `B` jobs are roots. Their order is `f` forced roots followed
by `n` roots corresponding to `U`. The next `B` jobs are sinks:

* the first `m` correspond in any fixed order to `V`; the sink for `v`
  has all forced roots as parents and also every `U` root **not** adjacent
  to `v` in `G`;
* the remaining `B-m` padding sinks have every root as a parent.

All true edges point from a root to a sink. The input is a height-two
forward DAG, and the resource excess is exactly `c=B-W=k`.
The construction has `O(n+m+k)` jobs and `O((n+m+k)^2)` edges.
Maximum indegree is unbounded; no binary-input hardness conclusion
follows from this construction.

## 2. Every ROB edge is already a true edge

For a sink of index `B+j`, its artificial ROB predecessors are exactly
root indices `0,...,j`. If `j<m`, these are all forced roots because
`f=m+k>m`. If `j>=m`, the sink is padding and already depends on every
root. There are no artificial edges within the roots or within the
sinks, since each level has only `B` consecutive jobs.

Thus the augmented precedence graph equals the true dependency graph.
The supplied order satisfies the ROB constraints without adding any
new comparabilities. This observation does not remove the need to
check resource widths, but confirms that no accidental extra window
edge invalidates the reduction.

## 3. A biclique gives three cycles

Suppose `A subset U` and `C subset V`, both of size `k`, form a biclique.
Use the following actions:

1. Issue all roots except `A`, exactly `B-k=W` jobs.
2. Issue the `k` roots in `A` and the `k` sinks in `C`.
3. Issue all remaining sinks, exactly `B-k=W` jobs.

The second action fits because `n,m>=k` gives `W=n+m>=2k`.
Every selected `V` sink is ready at cycle two: none of the uncompleted
roots in `A` is a nonneighbor, and all its other parents issued in
cycle one. Its predecessors need not include the roots being issued
alongside it. There is no same-cycle dependency shortcut.

For the operational admission check, all `f` forced roots finish in
cycle one, so the retired prefix has length at least `f>=m`. This
admits every one of the first `m` sinks by cycle two. The uncompleted
roots also remain admitted. After cycle two, all roots are complete,
so the retired prefix is at least `B`; every remaining sink is admitted
and ready in cycle three. Hence the schedule is legal.

Since `2W=2B-2k<2B=N`, two cycles are impossible by the work bound.
The constructed instance therefore has optimum exactly three.

## 4. Every three-cycle schedule gives a biclique

Conversely, consider any legal schedule completing in three cycles.
No sink can issue in cycle one: every sink has forced-root predecessors.
At most `W=B-k` roots issue then, so the set `A'` of uncompleted roots
has size at least `k`.

There are `B` sinks and at most `W` cycle-three slots. At least `k`
sinks must therefore issue in cycle two. In particular some sink is
ready then. As every sink depends on all forced roots, all forced roots
must have issued in cycle one. Thus `A'` consists entirely of `U` roots.

No padding sink is ready in cycle two, because `A'` is nonempty and
every padding sink depends on every root. The at least `k` sinks issued
in cycle two all correspond to vertices of `V`. For each such `v`,
readiness implies that none of the roots in `A'` is a nonneighbor of
`v`. Consequently every vertex of `A'` is adjacent to every one of
these at least `k` vertices of `V`. Selecting `k` vertices from each
side gives a `K_(k,k)` in the input graph.

This argument permits empty and underfilled actions and makes no
non-delay or greedy assumption.

## 5. Exact gap, poset width, and parameter consequences

A four-cycle schedule always exists: issue the first `W` roots, then
the remaining `k` roots, then the first `W` sinks, and finally the
remaining `k` sinks. Each batch is ready and admitted, and `k<=W`.
Combining Sections 3–4 gives the exact dichotomy

`T*=3` if the source graph has a `K_(k,k)`, and `T*=4` otherwise.

The true poset has width exactly `B`. Its `B` roots and its `B` sinks
are antichains, proving the lower bound. An antichain mixing levels
can contain no forced root, because every sink lies above every forced
root, and no padding sink, because every root lies below every padding
sink. It is therefore contained in `U` roots together with `V` sinks
and has size at most `n+m=W<B`. Pure-level antichains have size at
most `B`. This proves the exact width, not merely an upper bound.

Hence the reduction also has `poset_width-W=k`, and every artificial
ROB edge is already true. It is a parameter-preserving reduction from
balanced biclique to the three-cycle decision problem with parameter
`c=B-W`. Using the source hardness cited below, the scheduling problem
is **W[1]-hard in c**, even for these height-two instances. The usual
consequence is the nonexistence of an `f(c) poly(N+|E|)` algorithm
unless `FPT=W[1]`. We do not claim W[1]-membership or a matching
fine-grained exponent lower bound.

This is consistent with the XP algorithm in `FORCED_SEGMENT_DP.md`.
It also does not contradict the FPT result in `c+S`: for horizon three,
the total unused-slot parameter here is

`S=3W-N=n+m-2k`,

which is not bounded by a function of `c=k` in the reduction.
The complexity status for true indegree at most two remains open
within this research; replacing a large-fanin sink by a binary tree
would change the horizon and may destroy the parameter preservation.

## 6. Independently inspected source and novelty boundary

Bingkai Lin, *The Parameterized Complexity of k-Biclique Problem*,
arXiv:1406.3700v3 (2019), Section 1.1, Corollary 1.3:
<https://arxiv.org/pdf/1406.3700>.

This review independently opened the original PDF and read the theorem
and the reduction preceding that corollary. It establishes W[1]-hardness
through a deterministic parameterized reduction, including bipartite
output graphs. The randomized-ETH qualification occurs in a separate,
stronger exponent statement later in the paper, and is not required
for the W[1]-hardness inference used here.

This source supplies the hardness of the **source** problem. It does
not itself establish that the scheduling reduction above is new.
Classical height-two unit-job scheduling and width-minus-machines
parameterizations require a separate novelty search. The exact
supplied-order/ROB assumptions must be retained in that comparison.
