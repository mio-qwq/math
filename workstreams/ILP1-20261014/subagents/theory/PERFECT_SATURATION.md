# Perfect width saturation with one extra window entry

Status: **WRITTEN_PROOF**, **NOVELTY_UNCONFIRMED**. The main agent and
the theory subagent independently arrived at the same two-macro
structure while analyzing the width-three counterexample. Independent
verification is saved in verification commit
`d566e057cf3cd7b2e9eaf597c5851cda5921b6df`, so the written theorem is
also **INDEPENDENTLY_REVIEWED**. No Lean verification is claimed here.

## 1. Scope and the two legal macros

Let `W>=2`, `B=W+1`, and `N=kW` with integer `k>=0`. True dependencies
form an arbitrary forward DAG on jobs `1,...,N`. Use the declared
eager, unit-latency ROB model with unlimited in-order retirement.
The question is whether the exact work lower bound `T*=k` is attained.
This note does **not** decide attainability of `ceil(N/W)` for arbitrary
nonmultiples of `W`.

Partition the program into consecutive blocks `C_1,...,C_k` of `W`
jobs each. There are two candidate macros, always starting after a
completed prefix of whole blocks:

* `A_j`: execute all of `C_j` in one cycle.
* `D_j`: for two adjacent blocks `C_j,C_(j+1)`, let `h` be the last
  job of `C_j` and `x=h+1` the first job of `C_(j+1)`. In its first
  cycle execute `(C_j\{h}) union {x}`; in its second cycle execute
  `{h} union (C_(j+1)\{x})`.

A macro is called legal if every true edge with both endpoints in its
one- or two-block interval points from an earlier macro-cycle to a
strictly later macro-cycle. Thus `A_j` is legal exactly when `C_j`
has no internal true edge. For `D_j`, edges within either issue set,
as well as the reversed boundary edge `h->x`, are forbidden.
True edges entering from the earlier completed prefix are already
satisfied; all other true edges leave toward jobs issued later.

These true-edge conditions suffice for ROB legality. In `A_j`, the
whole block is initially admitted, and finishing it returns to a
clear-prefix state. In `D_j`, all first-cycle jobs are in the first
`W+1` entries. Exactly the first `W-1` entries retire; the next window
contains `h`, completed job `x`, and the remaining `W-1` jobs of the
second block. Its `W` unfinished entries are exactly the second-cycle
issue set. After that cycle the entire two-block prefix retires.

## 2. Exact tiling theorem

**Theorem 1.** `T*=k` if and only if the `k` consecutive blocks can
be tiled by legal one-block macros `A_j` and legal two-block macros
`D_j`.

Moreover, **every** `k`-cycle schedule has this macro decomposition;
no separate oldest-inclusive normalization is needed for this claim.

**Proof.** Any `k`-cycle schedule must issue exactly `W` jobs in every
cycle, because there are `kW` jobs in total. Begin at a clear-prefix
state containing an integral number of remaining blocks. If exactly
one block remains, its `W` jobs must all issue next cycle, giving `A`.
Otherwise at least `2W` jobs remain, and the full `W+1` entry window
is admitted. Its first action consists of `W` entries and omits
exactly one, say the `r`-th entry in program order, `1<=r<=W+1`.

After this action, only the first `r-1` entries can retire. The other
`W+1-r` completed entries still occupy the window. Refilling therefore
leaves at most `r` unfinished window entries at the next cycle. A
full-width next action is impossible when `r<W`. Since every cycle
must issue `W`, only `r=W` or `r=W+1` is possible.

When `r=W+1`, the first `W` consecutive jobs issue and retire, so
the action is `A` and returns to a clear-prefix state one block later.
When `r=W`, the first issue set is exactly the first set of `D`.
The next window has exactly `W` unfinished entries; every one must
issue in the next cycle. This is precisely the second set of `D`,
and the state becomes a clear prefix two blocks later. True-edge
legality follows from the schedule's own legality. Repeat this
argument until the program ends.

Conversely, each legal macro executes at full width and returns to a
clear-prefix state. Concatenating a tiling is therefore a legal
schedule of exactly `k` cycles. The work lower bound makes it optimal. ∎

The omitted-position argument also gives a useful necessary condition
outside the divisible case: if a candidate schedule attains the work
bound `ceil(N/W)` with total unused issue capacity
`s=W ceil(N/W)-N`, and its first action issues `W` jobs from a full
window, then its unique omitted position `r` must satisfy `r>=W-s`.
Its next cycle has at least
`W-r` unused slots. This condition alone is not sufficient.

## 3. A graph property and a short obstruction certificate

Form a path on the `k` block positions. Keep edge `j--(j+1)` exactly
when `D_j` is legal, and mark vertex `j` when `A_j` is legal. A tiling
is equivalent to a matching whose uncovered vertices are all marked.
This is a standard path matching problem; no new matching algorithm
is claimed.

The remaining edges partition the blocks into maximal path components.

**Theorem 2.** The work lower bound is attained if and only if every
odd-size component has a marked vertex at an odd local position,
counted from one at the component's left end. Even-size components
impose no further condition.

**Proof.** An even-size component can be covered by consecutive
two-block macros. In an odd-size component, choose a marked vertex
at an odd local position, use its one-block macro, and pair all
vertices to its left and right; both side lengths are even.

Conversely, a tiling cannot use a two-block macro across a missing
component edge. An odd component must therefore have a one-block
macro somewhere. Consider its leftmost such macro. Every preceding
vertex of the component is covered by two-block macros, so this
vertex's local position is odd. Its macro is legal, hence it is
marked. ∎

A positive certificate is an explicit macro tiling and its `k`-cycle
schedule. A negative certificate is a single odd component with all
odd-position vertices unmarked. Such a component proves that no
`k`-cycle schedule exists, hence `T*>=k+1` for a nonempty program.
This is a structural impossibility certificate, not an enumeration
of every ROB state or every schedule.

The negative certificate can be even shorter: an odd block interval
isolated by illegal `D` macros at its two boundaries (or a program
endpoint), with every odd-position `A` macro illegal, already suffices.
Its internal `D` flags need not be checked. No tiling can cross the
boundaries, and the leftmost singleton inside would have an odd local
position. Each illegal macro is witnessed by one actual true edge
that is simultaneous or reversed under that macro. The implementation
returns these witness edges, permitting a checker to validate the
negative certificate without trusting the macro-flag computation.

## 4. Linear implementation and edge accounting

`perfect_saturation.py` implements the component criterion and returns
the legal macro flags, a positive tiling/schedule, or a negative
component witness. Its `analyse_edges` entry point accepts a forward
edge iterable; `analyse` also accepts predecessor bit masks.
Its public routine rejects `W` not dividing `N` instead of silently
applying this theorem to `ceil(N/W)`.

Initialize every `A_j` and `D_j` as legal. Process each true edge `u->v`:

1. If its endpoints belong to the same block, mark that block's
   one-cycle macro illegal.
2. Consider the at most two adjacent-block intervals containing both
   endpoints. For each, compute the endpoints' macro-cycle numbers
   using the boundary swap, and reject the candidate unless the
   source's number is strictly smaller than the target's.

There are at most two such intervals because any particular block
belongs to only its left and right adjacent-block pair. An edge
spanning more than one block boundary belongs to neither interval
and can never violate an internal macro. The boundary-cycle number
is computed by constant-time index comparisons; the code does not
scan `W` entries afresh for each edge or each candidate.

After this pass, scan the `k` block vertices and legal edges to find
components and choose marked odd vertices where required. The total
number of inspected component vertices is `k`. Writing the output
schedule touches each job once. Thus the arithmetic-operation bound
is `O(N+|E|)` time and `O(N)` output/storage, uniformly in `W`.
The edge-iterable entry point realizes this standard indexed-graph
operation bound directly. The convenience Python bit-mask wrapper
additionally carries the underlying arbitrary-precision extraction cost.

For `N=0`, the empty tiling is a zero-cycle optimum. For `W=1`, every
forward program has optimum `N`; the implementation returns the
sequential schedule directly. For `k=1`, the criterion reduces to
the necessary and sufficient absence of any true dependency. Then
`B=W+1>N` is harmless: the window is truncated at the program end.

This result is stronger than merely specializing an exponential
fixed-window algorithm to one numeric window size: `W` is an input
parameter here. It only solves perfect-width saturation, and it
does not supply the general optimum when the criterion fails.

## 5. Actual implementation checks

`perfect_saturation_check.py` compares the implementation with the
earlier independent completed-set optimizer and operationally replays
every positive schedule. It also checks each negative certificate's
actual edge witnesses, including the two boundaries and forbidden
odd-position singletons, rather than trusting an infeasible flag.

`PERFECT_SATURATION_CHECK.json` records 38,506 exhaustive effective-graph
cases through `N=6` at every dividing width at least two, 31 empty and
width-one boundaries, 90 seeded random cases through width six with
two to four blocks, 19 forced-swap witnesses at widths two through
twenty, and three rejected invalid inputs. All passed. The seed is
20261014, Python version 3.12.14, and measured runtime 1.757167 seconds;
the report contains both source hashes and the complete range table.

The independent verification agent separately used a time-assignment
constraint solver, 540 bounded-indegree random examples, and 2,731
abstract macro-flag patterns. Its saved review, rather than this
author's tests, establishes the independent-review status. Neither
finite test collection is substituted for the arbitrary-size proofs.
