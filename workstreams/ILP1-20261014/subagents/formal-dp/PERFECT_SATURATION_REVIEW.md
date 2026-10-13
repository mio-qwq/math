# Independent review: perfect saturation with B=W+1

Reviewer: formal-DP subagent. Date: 2026-10-13 UTC. No author-owned file
was edited. Final reviewed theory commit:
`69dc6527d69918972f8f5576410fde7d409a5ecc`.

- `PERFECT_SATURATION.md` SHA-256:
  `c561ae338ed3b16872c3620132780cc9f0b1097eb2d9642e7e5ca2f51e9be296`.
- `perfect_saturation.py` SHA-256:
  `2718784659ddb8aba84b8d0b5db200bacf518c4559f6a8cc80ee58aeafce125a`.

## Verdict and scope

**Accepted as an arbitrary-size written theorem and linear combinatorial
algorithm for N divisible by W.** The two-macro completeness argument,
path-component criterion, weaker odd-interval rejection certificate, and
edge accounting are sound under the stated eager ROB semantics. No
remaining blocking error was found in the final commit.

This review derives the proofs independently; it does not use the existing
finite CSP/ROB comparisons as proof. No large graph enumeration was repeated.
No Lean verification or historical novelty claim is made. The result decides
whether `T*=N/W` at `B=W+1`; failure does not compute the optimum, and the
criterion is not asserted for nonmultiples of W.

## Why the two macros are exhaustive

Use zero-based blocks in this review. Let `N=kW`, with W>=2. A schedule
finishing in k cycles must issue W distinct jobs in every cycle. Starting
after a completed prefix of whole blocks, one remaining block must issue
as a single macro A. With at least two blocks remaining, the window has
W+1 unfinished jobs and the first action omits exactly one position r,
numbered from one.

Only r-1 jobs retire. Of the original window, W+1-r completed jobs remain
behind the omitted job. There are consequently at most r unfinished entries
after refill. The next cycle exists, because at least W jobs remain after
the first action. Its required full issue width forces r>=W.

If r=W+1, the first whole block executes and the state is again a clear
whole-block prefix. If r=W, precisely the first W-1 jobs and the first job
of the next block execute. The next window has exactly W unfinished jobs:
the omitted boundary job and the remaining W-1 jobs of the second block.
All must execute next, returning to a clear prefix two blocks later.
These are exactly A and D in the note (D is the proposed two-block B tile).
Repeating this argument proves decomposition of **every** full-throughput
schedule, without an oldest-first normalization assumption.

Conversely, a legal A or D fits the actual ROB, as the refill calculation
also shows. The only potentially inverted program-order pair in D is the
swapped boundary pair. Checking every true edge internal to the tile for
strictly increasing tile-cycle number detects that reversed dependency and
every same-cycle dependency. True edges entering from earlier tiles are
already satisfied, and forwardness prevents edges entering from later
tiles. Concatenation therefore gives a legal k-cycle schedule. The width
work bound establishes optimality.

## Path criterion and the stronger rejection certificate

Keep a path edge exactly where D is legal, and mark a block where A is
legal. Every even component is tiled by D pairs. In an odd component, a
marked vertex at odd local position (one-based), equivalently even offset
from the left endpoint, permits its A tile and D pairs on both sides.
Conversely the first A in any tiling must occur at such a position, because
the preceding vertices are all covered by D pairs. An odd component cannot
be tiled with no A. This proves both directions of the component criterion.

For a negative certificate, **maximality and legal internal D edges are
unnecessary**. It is enough to supply an interval of block indices `[lo,hi)`
with the following properties:

1. `0<=lo<hi<=k` and `hi-lo` is odd.
2. The D crossing the left endpoint is forbidden, unless lo=0; the D
   crossing the right endpoint is forbidden, unless hi=k.
3. Every A at `lo,lo+2,...,hi-1` is forbidden.

Any whole-path tiling would restrict to a tiling of this interval because
no tile can cross its endpoints. If it has no A, an odd number of vertices
cannot be covered by D pairs. Otherwise its leftmost A has an even offset
from lo, contradicting condition 3. This proof never inspects an internal
D edge, so arbitrary additional forbidden D edges cannot invalidate the
certificate. Combining with the two-macro theorem rejects every k-cycle
ROB schedule, not merely the schedule selected by the producer.

The certificate is complete as a rejection format: when saturation fails,
the component criterion supplies an odd component satisfying these weaker
conditions. One violating actual edge witnesses each forbidden macro.
There are at most `(hi-lo+1)/2+2` such witnesses; each consists of a block
index and two job indices. This is an O(k)-entry certificate, not a claim
of O(k) bits for binary-encoded indices.

## Edge accounting and source audit

For any forward edge `u->v`, write `bu=floor(u/W)`. A two-block interval
containing u can start only at `bu-1` or `bu`. The implementation checks
exactly these candidates, retaining those within the block range and with
`v<(start+2)W`. Because u<v, the lower endpoint condition for v is automatic;
u already lies in each retained candidate by its block quotient. Thus the
test neither misses a containing tile nor checks an edge outside its tile.

The source's `batch` function exactly assigns cycle zero to the first W-1
jobs and the swapped next-block first job, and cycle one to the other W
jobs. It invalidates a D when `batch(u)>=batch(v)`. Same-block edges also
invalidate A. Edges spanning at least two block boundaries affect no
internal tile condition and are correctly ignored after this constant
candidate work.

The component scan, pivot search, and output generation each touch O(k) or
O(N) total items. Every edge is examined for at most two D candidates.
Consequently the edge-iterable core uses O(N+|E|) indexed arithmetic
operations and O(N) output/auxiliary storage, uniformly in W. The note
correctly distinguishes this from bit complexity and from the additional
arbitrary-precision extraction cost of its predecessor-mask wrapper.
Duplicated input edges merely repeat harmless constant work and should be
counted as input occurrences in that running-time statement.

Whenever a legality flag becomes false, its actual violating edge is saved.
A failed component therefore has a witness for each requested singleton
and each non-endpoint barrier. Witnesses are never inferred merely from a
false flag. The public producer, however, is **not** an external-certificate
parser; its author test script checks certificates generated by that same
producer. The independent validator below fills that narrower parsing gap.

## Boundary and domain checks

- W=1: every block is a singleton, so every A is legal in a forward DAG.
  The width bound requires N cycles, and the sequential schedule attains
  N at B=2. The implementation's special branch is correct.
- k=0: the graph and tiling are empty, the schedule has zero cycles, and
  no nonempty odd rejection interval exists. Any positive W is permitted.
- k=1: only A can cover the unique block; it is legal exactly when there
  is no true edge anywhere in that program. B=W+1>N is harmless because
  eager admission truncates at N. A single internal edge is a valid
  rejection witness, with both interval boundaries at program endpoints.
- Invalid width, nondivisible N, and nonforward/out-of-range edges are
  rejected before applying the criterion.

The final note's nondivisible side observation explicitly assumes the
first action issues W jobs from a full window. Under that guard, the
claimed next-cycle loss and necessary `r>=W-s` bound are valid. An earlier
uncommitted copy read during review omitted that guard. For example,
W=3, B=4, N=5 with independent jobs may execute `{1,3}` then `{2,4,5}`;
the first omitted position is 2 but the next cycle is full. This illustrates
why the guard matters; it is **not** a counterexample to final commit
69dc652 or to the divisible-input theorem. There is no outstanding fix.

## Independent rejection parser and actual targeted checks

`perfect_negative_certificate_check.py` implements `validate_negative`
without importing the producer or computing A/D legality arrays. It checks
the complete certificate shape, integer/end-point/parity bounds, exactly
the required singleton positions, actual graph-edge membership, tile
containment, and nonincreasing phase across each boundary witness. Endpoint
boundaries must be represented by None. It accepts lists or tuples as
obtained either directly or through JSON and rejects missing/extra fields.

In particular, the checker rejects an empty interval, a forged or deleted
true edge, a true edge belonging to the wrong tile, and a genuine edge that
does not violate the claimed D macro. After building its membership set,
checking takes O(k) time. This independent checker uses O(|E|) graph-set
storage in addition to the supplied certificate; this is distinct from
the producer's streaming O(N) auxiliary-space claim.

All **29** deterministic targeted checks passed on the final producer
hash. These include valid interior and one-block rejection witnesses, a
valid odd interval whose internal D edges are forbidden (so it is not a
component), and deliberate corruptions of bounds, parity, positions, edge
membership, boundaries, and input domain. Empty and width-one rejection
attempts are rejected. This finite parser evidence supports the code audit;
the arbitrary-size soundness argument is the proof above.

Reproduction:

```sh
python workstreams/ILP1-20261014/subagents/formal-dp/perfect_negative_certificate_check.py \
  --producer /absolute/path/to/subagents/theory/perfect_saturation.py \
  --output /tmp/perfect-negative-checks.json
```

Exact tested cases, Python version, time, and both source hashes are saved
in `evidence/perfect-negative-checks.json`. This independent parser is not
Lean verified and makes no claim to verify positive schedules or solve a
general scheduling problem.
