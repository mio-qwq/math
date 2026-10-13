# Targeted review: large changes in minimum sufficient resources

Independent reviewer: literature subagent D. Date: 2026-10-13 UTC.
This follow-up reviews the research team's resource-threshold constructions,
checks their meaning, and performs a targeted prior-art search. It supplements
`LITERATURE_REVIEW.md`; it does not supersede that file's verification limits.
No Lean compilation or new solver test was performed by this reviewer.

## Assessment

The fixed-width layered family is the strongest current example. It proves,
within R1, an unbounded additive and multiplicative reduction in the *minimum
window required for exact optimality* when issue width changes from 2 to 3.
Both unrestricted-window benchmarks remain the same. The graph uses at most
two true inputs and two successors per instruction and has poset width three.

This is more informative than the general observation that resources interact.
It rules out any universal multiplicative or additive bound on this particular
threshold improvement, even at fixed small issue widths. It remains a short
extremal construction; claiming a major scheduling breakthrough, practical CPU
speedup, or confirmed originality would exceed the evidence.

The exact-window saving conceals a small approximation penalty: width two and
window two finish the same family only one cycle later. Thus approximate
saturation can behave very differently from exact saturation. This caveat is a
mathematical consequence of the example, not a hypothetical hardware concern.

## Independently checked layered construction

Use zero-based indices. Let `K≥2`, `N=2K`. Job 0 is independent. For
`1≤ℓ≤K-1`, layer `L_ℓ={2ℓ-1,2ℓ}` consists of two jobs. Add every edge from
`L_ℓ` to `L_(ℓ+1)` for `1≤ℓ<K-1`, and both edges from `L_(K-1)` to the final
job `z=2K-1`. There are no other true dependencies. All jobs are mandatory;
job 0 may be designated an observable program output. No dead-code elimination
or instruction-count change is allowed in R1.

The true DAG height is `K`, its largest antichain has size three, and its
maximum true indegree/outdegree is two.

### Exact threshold statement

`T*(P,N,2)=T*(P,N,3)=K`,

`B_sat(P,2)=2K`, and `B_sat(P,3)=3`.

For every `K`-cycle schedule, each job in `L_ℓ` must execute in cycle `ℓ-1` and
`z` in cycle `K-1`. To see this, for each such job choose a true path of `ℓ`
vertices ending there and a path of `K-ℓ+1` vertices beginning there. Their
strict timing constraints pin the job's time between `ℓ-1` and `ℓ-1`.

At issue width two, the first `K-1` cycles are therefore full. Job 0 must share
the final cycle with `z`. This schedule is feasible when the whole program is
initially admitted. But for any `B<N`, R1's added precedence includes `0→z`,
which forbids that same-cycle assignment. Hence precisely `B=N` first attains
the unrestricted benchmark.

At width three and capacity three, issue `{0,1,2}` in cycle 0, then each
successive pair layer, then `z`. Each pair retires in order, so the next pair
is admitted for the next cycle. This attains height `K`. Capacity at most two
cannot attain `K`: job 2 is not initially admitted, whereas the pinning argument
requires both jobs of `L_1` in cycle 0. Thus capacity three is necessary and
sufficient.

The difference `2K-3` and ratio `2K/3` are both unbounded. This is a comparison
of minimum exact-saturation capacities, not a ratio of makespans. It does not
contradict resource monotonicity of `T*`.

### Exact performance away from saturation

The following additional calculation was independently derived during review:

| Window range | `W=1` | `W=2` | `W≥3` |
|---|---:|---:|---:|
| `B=1` | `2K` | `2K` | `2K` |
| `B=2` | `2K` | `K+1` | `K+1` |
| `3≤B<2K` | `2K` | `K+1` | `K` |
| `B≥2K` | `2K` | `K` | `K` |

For the nontrivial upper bound at `B=2,W=2`, use the cycles
`{0,1}`, `{2}`, `L_2,…,L_(K-1)`, `{z}`. This takes `K+1` cycles and is legal:
after the first two cycles the next complete pair is at the ROB head, and every
subsequent pair frees its own two entries. For `K=2`, the middle layer list is
empty. Larger capacities inherit the schedule. The impossibility of `K` above
gives the matching lower bounds. Capacity one or width one forces serial work.

Consequently the full exact-saturation functions on this family are

`B_sat(P,1)=1`, `B_sat(P,2)=2K`, `B_sat(P,W)=3` for `W≥3`,

and

`W_sat(P,1)=1`, `W_sat(P,2)=2`,
`W_sat(P,B)=3` for `3≤B<2K`, and `W_sat(P,B)=2` for `B≥2K`.

The resource pairs minimally attaining `K` cycles are exactly `(B,W)=(2K,2)`
and `(3,3)`. The first width-threshold increase from 1 to 2 changes the target
makespan; the decrease from width 2 to 3 does not. Stating that difference
avoids attributing all threshold nonmonotonicity to a moving benchmark.

For an explicitly defined relative approximation target
`T*(P,B,2)≤(1+ε) T*(P,N,2)`, capacity two suffices whenever `K≥1/ε`, since
`(K+1)/K=1+1/K`. The unbounded exact-threshold ratio therefore does not imply
an unbounded approximate-threshold ratio. A robust P3 theory should eventually
state results for both exact and approximate saturation.

## Earlier two-cycle constructions: checked scope

Let `m≥2`. Put an isolated job first, then `m` parent roots, then `m-1`
children. Two parents feed one child, and each remaining parent feeds a
different child. Each parent is required exactly once. Here `N=2m`, true
indegree is at most two and outdegree at most one. A two-cycle schedule at
width `m` must issue all `m` parents first, delaying job 0 until the final
cycle. Hence `B_sat(P,m)=2m`. Width `m+1` executes all roots together;
the last required root must be initially admitted, so
`B_sat(P,m+1)=m+1`. The additive drop is unbounded but the ratio is less than
two. The layered family above removes that multiplicative limitation and keeps
the compared widths fixed.

For the general two-cycle family, let `1≤r≤floor(m/2)`. Order `r` independent
prefix roots, then `m` required roots, then `m-r` children whose parents
partition the required roots into `r` pairs and `m-2r` singletons. For
`m+r≤B≤2m`, the unlimited-width benchmark is two. All `m` required roots must
execute first. Admission of the final job for the second cycle requires
retiring at least `d=2m-B` jobs, adding exactly `min(r,d)` prefix roots to
the mandatory first issue set. This set suffices as well: it retires the
needed prefix, makes all children ready, and leaves at most `m` jobs for
cycle two. Thus

`W_sat(P,B)=m+min(r,2m-B)`.

This is an exact joint two-cycle feasibility frontier. It records a total
width-threshold drop of `r` across the indicated window range; it does not
assert that one extra window entry causes a drop of `r`.

## Targeted prior-art comparison

### Window/width saturation is an established subject

Dubey, Adams and Flynn (1994), *Instruction Window Size Trade-Offs and
Characterization of Program Parallelism*, IEEE TC 43(4), pp. 431–442,
[DOI](https://doi.org/10.1109/12.278481),
[primary abstract](https://research.ibm.com/publications/instruction-window-size-trade-offs-and-characterization-of-program-parallelism).
The title and abstract directly cover scope/resources/performance trade-offs.
Attempts to retrieve the full paper through DOI, IEEE Computer Society and
Unpaywall failed. Its contents therefore cannot be ruled out as prior art for
an exact threshold result. No theorem number was verified.

Tejas S. Karkhanis and James E. Smith (2004), *A First-Order Superscalar Processor
Model*, ISCA 31,
[author full text](https://jes.ece.wisc.edu/papers/isca04.tejas.pdf).
Inspected §§1.1, 2, 3 and 6.2. Section 3 explicitly models issue-rate saturation
versus window size and finite issue width, using trace-derived power-law curves
and an approximation at the width limit. Its issue window and ROB are separate,
issue is oldest-first, and issue/retire/pipeline widths are tied. These are
averaged performance models, not R1's minimum over all schedules or its exact
minimum saturation capacity. The read sections do not state our extremal family.

The already reviewed FIFO event-graph result of Navada, Choudhary and Rotenberg
(2010), §§5.1–5.2, remains relevant because the decisive `0→z` resource edge is
an elimination of established ROB entry/exit constraints. The new comparison
must be the extremal inverse-resource consequence, not the idea of adding a
buffer precedence.

### Register saturation is a different mathematical quantity

Sid-Ahmed-Ali Touati (2002), *Register Pressure in Instruction Level Parallelism*,
doctoral thesis, Université de Versailles,
[author page](https://www-sop.inria.fr/members/Sid.Touati/thesis.html).
The author's abstract defines register saturation as the maximum register need
over valid schedules, and register sufficiency as the minimum need. It discusses
adding serial arcs while preserving critical paths where possible. The linked
full thesis encountered an access challenge; only the author's abstract was read.

This is significant terminological and methodological prior art. Register
occupancy tracks value lifetimes until uses; ROB occupancy tracks admitted
instructions until a completed prefix retires. Our delayed isolated first job
blocks release of unrelated younger entries even when their results have no
remaining uses. A register-pressure theorem cannot be transferred merely by
renaming its resource as a window. Conversely, our result says nothing about
the minimum physical register count of a real processor.

### Memory/makespan trade-offs do not identify the occupancy semantics

Lionel Eyraud-Dubois, Loris Marchal, Oliver Sinnen, Frédéric Vivien (2014),
*Parallel scheduling of task trees with limited memory*, INRIA RR-8606,
[primary preprint record](https://arxiv.org/abs/1410.0329).
Inspected abstract: edge data occupies memory until the consuming task completes,
and both peak memory and makespan are optimized. That release rule and tree
structure differ from R1. It supplies established context for joint resource
optimization, not a verified implication of the ROB threshold formula.

Classic Graham scheduling anomalies concern the behavior of prescribed
list policies under resource or input changes. Here offline `T*` stays
nonincreasing with more capacity/width. The nonmonotone objects are the
*minimizers of sufficient resource* against particular performance benchmarks.
The broad word “anomaly” should be accompanied by this distinction.

## Exact searches and limitations

The following queries were actually executed in this targeted pass:

* `"Instruction Window Size Trade-Offs" pdf Dubey Adams Flynn`
* `"instruction window" "issue width" "minimum" "saturation"`
* `"reorder buffer" "issue width" "tradeoff" optimal`
* `"scheduling" "minimum buffer" "processors" "nonmonotonic"`
* `"278481" "pdf" "Dubey"`
* `"window size" "issue width" "analytical" saturation instruction`
* `"scheduling" "minimum buffer size" "parallel" tradeoff`
* `instruction scheduling register pressure resource tradeoff minimum registers parallelism`
* `reorder buffer minimum size instruction scheduling optimal width tradeoffs`
* `parallel task scheduling more processors less memory minimum memory makespan`
* `instruction window issue width saturation critical path mathematical model Michaud Seznec Jourdan`

Both available search engines were used. The DOI-only query returned substantial
irrelevant material; it was not treated as evidence. Full texts of Karkhanis–Smith
and Zhu–Wong, *Sensitivity Analysis of a Superscalar Processor Model* (2002),
[author PDF](https://www.comp.nus.edu.sg/~wongwf/papers/acsac2002.pdf), were
retrieved; the latter was only screened and no theorem is imported from it.
Dubey et al. and Touati full-text access remained incomplete. No exact matching
R1 threshold construction was located, but source coverage is insufficient to
claim that none exists.

## Status and next useful checks

For the displayed constructions and performance table: `WRITTEN_PROOF` and
`INDEPENDENTLY_REVIEWED` by this reviewer; `LEAN_VERIFIED` is not asserted here.
For originality: `NOVELTY_UNCONFIRMED` throughout.

An appropriate provisional contribution claim is: “We give exact extremal
resource-threshold examples for the stated ROB semantics, including an
unbounded decrease in minimum sufficient window at fixed issue widths 2 and 3.”
Avoid “first,” “unprecedented,” and claims about actual power, clock rate or
silicon area. The highest-value next theoretical question is whether similarly
large threshold changes persist for a fixed positive performance tolerance,
rather than merely exact attainment of the critical-path lower bound.
