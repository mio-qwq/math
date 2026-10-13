# Independent audit: a two-cycle family with B=W+1

Verification subagent C, 2026-10-13 UTC. Status: written proof independently
accepted; finite CSP/replay checks passed; no novelty or Lean claim.

## Exact statement

Fix integers `W>=2`, `1<=m<=W-1`, and `B=W+1`. The first `B` jobs are roots.
Partition them into the prefix `F={0,...,m-1}` and the pool `C={m,...,W}`.
For each hidden `x` in `C`, append `m` sinks. Their predecessor sets partition
`C\{x}`: each required root appears in exactly one sink, and empty sets are
allowed. A maximum indegree `d>=1` is achievable precisely when
`W-m<=dm`. Maximum outdegree is one. The number of jobs is `N=B+m`.

For each program the offline optimum is two. Its unique first action that
can finish in two cycles is the set of all initial roots except `x`.
On this fixed-parameter promised family the exact randomized minimax ratio is

`3/2 - 1/(2 |C|)`, where `|C|=W+1-m`.

The exact deterministic family ratio is `3/2`. Fixed-length advice that ensures
the offline optimum on every member requires and suffices to use
`ceil(log2 |C|)` bits. These family results give lower bounds for unrestricted
online scheduling, not corresponding universal upper bounds.

## Proof and the admission check

To issue the last sink in cycle two, the first `N-B=m` roots must all have
retired after cycle one. Thus every two-cycle first action contains `F`.
Every root in `C\{x}` has a sink successor, so it too must issue in cycle one.
These two requirements are disjoint and together have size
`m+(W-m)=W`; capacity makes their union the unique possible first action.

Conversely, execute precisely this union in cycle one. It includes all of `F`,
so all `m` sinks enter for cycle two. They are ready because every required
predecessor was executed. Execute them with the omitted root `x`. The second
action has size `m+1<=W`. Since `N>W`, one cycle is impossible and the
optimum is exactly two.

All family members expose the same first window and have the same length.
For an arbitrary randomized first action, including empty or underfull ones,
the probabilities of the `|C|` distinct successful actions sum to at most one.
Under a uniform input distribution, two-cycle completion therefore has
probability at most `1/|C|`. Other executions require at least three cycles,
so average expected duration is at least `3-1/|C|`. At least one fixed input
has that expectation or greater; division by two gives the lower bound.

For the family upper bound, choose `y` uniformly in `C` and issue all roots
except `y`. All of `F` finish, admitting all sinks next cycle. If `y=x`,
finish in cycle two. Otherwise the omitted root `y` blocks exactly one sink,
because every required root belongs to just one predecessor set. In cycle
two execute `y` and the other `m-1` sinks, a total of `m` jobs. Finish the
remaining sink in cycle three. This is an online policy on the promised
family: its first action depends only on the fixed parameters; all suffix
dependencies become visible before its second action. The two possible
durations are exactly two and three, giving the matching expectation.

Choosing a fixed omitted `y` instead gives the deterministic upper bound
three, while another hidden `x` supplies the lower bound. For advice, each
message can produce at most one of the unique optimal first actions, so at
least `|C|` messages are necessary. Encoding `x` supplies that many messages.

The family upper policy assumes the promised parameter `m` is known, or can
be inferred from a known program length. The universal lower bound needs no
such assumption: disclosing the common `m` or `N` does not reveal `x`.

## Degree-restricted consequences

For `W=2q,m=q`, every sink can have one distinct predecessor. The DAG is
exactly `q` disjoint edges plus isolated roots, with

`B=2q+1`, `N=3q+1`, `|C|=q+1`, ratio `3/2-1/(2(q+1))`.

Thus lower bounds approach `3/2` even for matching dependence graphs and a
window only one slot larger than the issue width. This does not contradict
the sharp global `5/4` value when `W=2`: then `q=1` gives exactly `5/4`.

With maximum indegree two, choose `m=ceil(W/3)`. The pool then has size
`W+1-ceil(W/3)`, and the same lower bound approaches `3/2`. Its smallest
`W=3,m=1` example has four initial roots and one two-input sink, giving
the family ratio `4/3` at `B=4,W=3,N=5`.

There was an incorrect informal candidate in this reviewer's message: use
`N=2W` and arbitrarily omit any younger root. That candidate overlooks the
first `W-1` roots needed for last-job admission. It was immediately withdrawn
before inclusion in any theorem or test file. The explicit prefix `F` in
the reviewed construction is the necessary correction.

## Reproducible independent checks

`window_plus_one_family_audit.py` uses the time-variable CSP to check all
`W=2,...,7`, `m=1,...,W-1`, and hidden roots, with deterministic round-robin
partitions. It checks 77 programs and 10,675 first actions, including empty
and underfull actions, against the exact two-cycle feasibility claim.
It also directly replays 329 family-policy runs and 90 matching-family
runs for `q=1,...,5`. Every assertion passed. The scope, runtime, source
hashes, degrees, and parameter-specific ratios are saved in
`window_plus_one_family_results.json`. The finite audit does not enumerate
every possible partition; the general proof above applies to all partitions
with the stated degree bound and unique-parent-use property.

## General hidden-subset extension

The root/theory agents subsequently generalized the construction to
`W<B<=2W-m`, still with `1<=m<=W-1`. There are `B` initial roots, a fixed
prefix `F` of size `m`, and a pool `U` of size `B-m`. A hidden subset
`A` of `U` has size `W-m`; `m` appended sinks have dependency union `A`.
They can partition `A` into predecessor groups of size at most `d` precisely
when `W-m<=dm`, retaining outdegree at most one.

I independently accept this extension. Its only two-cycle first action is
`F` union `A`: admission forces `F`, dependencies force `A`, and the union
has size `W`. Conversely that action admits all sinks for cycle two, whose
work consists of `B-W` unissued roots and `m` sinks, with total at most `W`
by the upper bound on `B`. Hence the offline optimum is two.

Let `M=binom(B-m,W-m)`. Guess `A'` uniformly among the `M` subsets, and
issue `F` union `A'`. All sinks are admitted in cycle two. Issue every
unissued root together with every ready sink; their number is at most
`B-W+m<=W`. If the guess was correct this completes the program in two
cycles. Otherwise a root in `A\A'` blocks at least one sink during that
cycle, but all these roots now finish, so the remaining at most `m` sinks
finish in cycle three. Thus the duration is exactly two on a correct guess
and exactly three on an incorrect guess. The disjoint-success-action
argument gives the matching lower bound for every randomized policy:

`exact family randomized ratio = 3/2 - 1/(2M)`.

The exact deterministic ratio remains `3/2`, and fixed-length optimum advice
requires and suffices to use `ceil(log2 M)` bits. As before, these are family
upper bounds and global lower bounds. The upper policy knows the promised
parameters. Its correctness only requires that the sinks' dependency union
is exactly `A`; the partition condition is needed for the advertised degree
restrictions, not for the online upper-bound proof.

`hidden_subset_audit.py` checks four new parameter triples `(W,B,m)`:
`(5,7,2)`, `(5,8,2)`, `(6,8,2)`, and `(5,7,3)`. It checks 51 programs,
1,927 first actions, and 761 direct policy replays; all passed. These cover
both strict and tight `B<=2W-m`, maximum indegree at most two, and the
possibility of an empty predecessor group. Old large audits were not rerun.
Results and source hashes are in `hidden_subset_results.json`.
