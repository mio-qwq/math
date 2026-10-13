# Literature audit: excess window, forced segments, and idle-slot corridors

Reviewer: literature subagent D. Retrieval date: **2026-10-13 UTC**.
This is a finite follow-up to `PERFECT_SATURATION_NOVELTY.md`, focused on
the stronger arbitrary-makespan algorithm and its parameterization.
Historical novelty remains **NOVELTY_UNCONFIRMED**.

## Results actually reviewed

Use the fixed forward order and exact R1 semantics. Let `c=B-W`, after
normalizing ineffective resource values. These are separate claims:

| Claim | Mathematical content | Current scope of this review |
|---|---|---|
| One extra ROB entry | For arbitrary `N` and `B=W+1`, compute the exact offline optimum in `O(N min(B,N)(N+|E|))` time and linear working space | Written proof read and accepted; implementation execution not independently repeated here |
| General excess window | An exact macro-state algorithm with at most `N(2^c-1) binomial(B,c)` outgoing macro arcs | Written algorithm/counting argument accepted; **XP in c**, not FPT in `c` |
| Horizon corridor | For proposed horizon `H`, set `S=WH-N>=0`; a strip of at most `2c+S` variable completion bits gives FPT feasibility in `c+S` | Written proof read and accepted; separate from the first two claims |

The first two proofs are in theory commit
`a9408865e844cd05ea7fefda10bf9139f671075c`, file
`subagents/theory/FORCED_SEGMENT_DP.md`, SHA-256:

```text
55ff3a3c14d452548fb6b7cfb29ac19d1d0907960cd0a68274fbd767af7973dd
```

The corridor proof was read from the parent's then-untracked `CORRIDOR.md`,
SHA-256 `fd463a81718e573aaf6bdac9142bbb6ee0e4052ebbc9b6eb1c7f107bd9924fd0`.
This pins the actual reviewed text without claiming an unpublished parent
commit. No Lean compilation or semantic bridge is supplied by this review.

The key argument checked independently is short. If `h` entries are
completed but blocked from retirement, at most `B-h` admitted jobs remain
unfinished. A non-delay schedule can branch only when `h<c`. With `c=1`,
every nonclear state therefore has exactly one non-delay action. Branches
occur only at clear prefixes; unique segments between them can be
contracted. There are `N+1` possible clear prefixes and at most `B` first
actions per prefix, even when `W` is part of the input. Dominance justifies
restricting to non-delay schedules, but does not prescribe a priority rule.

For general `c`, the counting inequality is valid term by term:
`C(B-1,h) C(B-h,c-h) <= C(B,c) C(c,h)` for `0<=h<c`.
Unreachable masks may be counted for an upper bound; the constructed
search must still start from the actual initial state and use legal
transitions. The macro proof does not assume perfect issue saturation.

For the corridor, the lower prefix bound is stronger than the elementary
work bound because future unused issue slots limit the number of
completed, unretired entries. The terminal layer must be handled separately.
The corridor only restricts candidate states; it does not replace the
true dependency/admission transition check.

## Closest current structural source: degeneracy of the incomparability graph

**Alix Munier-Kordon and Claire Hanen (2026)**, *Exploiting Structural
Degeneracy for FPT Results on Problems over Directed Acyclic Graphs*.
[SSRN record](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6403481),
DOI `10.2139/ssrn.6403481`, posted **March 12, 2026**, 11 pages according
to the primary record returned by search. Its abstract claims FPT
enumeration of predecessor-closed sets using degeneracy of the
co-comparability graph, with applications including
`P|prec,p_j=1|Cmax`. Direct retrieval of both record and PDF returned 403;
only the primary indexed abstract/metadata was accessible. No theorem
number, completed proof review, or peer-reviewed status is asserted.

The authors' [March 19, 2026 lecture](https://graal.ens-lyon.fr/~yrobert/slides-frejus/Munier.pdf),
*A New Parameter for Scheduling Dependent Tasks*, was read in full.
Slides 7–11 represent predecessor-closed sets by maximal elements
(borders), enumerate borders as cliques of the incomparability graph,
and solve unit-time parallel scheduling by shortest paths through border
states. Slide 11 claims time `O(n^3+delta^2 n^2 4^delta)`.
The standard degeneracy definition on slide 8 makes slide 9's displayed
`delta>=width` and `|border|<=delta` off by one: a clique of size `q` has
degeneracy `q-1`. The corrected elementary bounds are `width<=delta+1`
and `|border|<=delta+1`. This observation does not refute the qualitative
FPT approach, but prevents treating every displayed bound as checked.

**Claire Hanen, Alix Munier-Kordon, and Istenc Tarhan (PMS 2026)**,
*A New Parameterized Complexity Analysis for Scheduling
Precedence-Constrained Tasks on Parallel Machines*, appears in the
[conference book](https://pms2026.sciencesconf.org/data/book_pms2026_en.pdf),
beginning on printed p.114. The primary indexed introduction identifies
degeneracy as its structural parameter. The full book retrieval timed
out; its complete theorem and proof were not read. This is a related
lead, not a separately verified stronger result.

**Parameter comparison, proved here for this audit.** For the augmented
R1 order, incomparable indices differ by at most `B-1`. The least-indexed
vertex in any induced incomparability subgraph has at most `B-1`
neighbors. Thus its standard degeneracy satisfies `delta<=B-1`. This
connects the prior degeneracy algorithm to the existing fixed-`B`
baseline, but it does not give the new dependence on `c=B-W`.

For a concrete separation, take `N=B=W+1` and no true dependencies.
There are no artificial edges either; the incomparability graph is
`K_B` and `delta=B-1=W`, unbounded while `c=1`. Likewise `N=B=W`,
`H=1`, and no edges give `c=S=0` but `delta=W-1`. Therefore the
retrieved FPT-in-degeneracy statement does **not directly imply**
polynomial time uniformly in variable `W` at `c=1`, XP in `c`, or FPT
in `c+S`. This comparison is not a proof that no more sophisticated
reduction to the prior algorithm exists.

## Time-window and active-schedule parameterizations

These papers use release/deadline windows in **time**, not the R1 count
of admitted but unretired instructions. Their parameters must not be
identified merely because both literatures use the word "window".

**Alix Munier Kordon (2021)**, *A fixed-parameter algorithm for scheduling
unit dependent tasks on parallel machines with time windows*, Discrete
Applied Mathematics 290, 1–6, DOI `10.1016/j.dam.2020.11.024`.
[Primary article](https://www.sciencedirect.com/science/article/am/pii/S0166218X20305126).
Primary indexed body text, including the model and Theorem 1's
path/schedule correspondence, was retrieved. It gives an FPT algorithm
for precedence-constrained unit tasks parameterized by maximum overlap
of feasible time windows (equivalently the associated interval-graph
pathwidth plus one). Direct article and HAL document retrieval failed;
the entire proof was not independently audited.

**Feng Shi, Yicong Zhu, Guangwei Wu, Jingyi Liu, and Jianxin Wang**,
*Improved Parameterized Algorithms for Scheduling with Precedence
Constraints and Time Windows*, COCOON 2025, LNCS 15984, 253–267.
[Publisher](https://link.springer.com/chapter/10.1007/978-981-95-0218-9_19).
The primary page was read: first online August 3, 2025, with publisher
copyright/citation year 2026. Its abstract states an
`O(2^mu mu m n^3)` unit-processing-time bound, where `mu` is maximum
time-window overlap. The subscription body was unavailable. A 2026
[journal record](https://www.sciencedirect.com/science/article/pii/S0304397526002069),
DOI `10.1016/j.tcs.2026.115947`, was also found through primary indexed
abstract/introduction text; its full proof was not retrieved.

**Istenc Tarhan, Jacques Carlier, Claire Hanen, Antoine Jouglet, and
Alix Munier Kordon (2023)**, *Parameterized Analysis of a Dynamic
Programming Algorithm for a Parallel Machine Scheduling Problem*,
Euro-Par 2023, LNCS 14100, 139–153.
[Publisher](https://link.springer.com/chapter/10.1007/978-3-031-39698-4_10).
The publisher abstract describes a state graph representing active
schedules, adapting earlier implicit enumeration and obtaining FPT
dependence on maximum time-window overlap and processing duration.
The abstract was read; the complete paper was subscription-blocked.

**Istenc Tarhan, Claire Hanen, Alix Munier Kordon, Jacques Carlier, and
Antoine Jouglet (2025)**, *FPT implicit enumeration of active schedules*,
Discrete Applied Mathematics 376, 235–250,
DOI `10.1016/j.dam.2025.06.031`.
[Primary article](https://www.sciencedirect.com/science/article/pii/S0166218X25003488).
Primary indexed abstract/introduction sections describe a compact graph
of active schedules for resource-constrained scheduling with time
windows, parameterized by maximum window overlap and processing time.
Direct publisher retrieval returned 403 and the HAL copy was unavailable.
This establishes relevant prior state-graph and dominance methodology;
it does not establish the current excess-ROB-entry bound.

**Claire Hanen and Alix Munier Kordon (2024 issue; online July 17, 2023)**,
*Fixed-parameter tractability of scheduling dependent typed tasks subject
to release times and deadlines*, Journal of Scheduling 27, 119–133.
[Publisher](https://link.springer.com/article/10.1007/s10951-023-00788-4).
The accessible primary abstract combines time-window pathwidth with the
smaller of maximum processing time and job-window slack. The article's
job-window slack is not `S=WH-N`, the aggregate unused capacity of a
proposed R1 horizon. The body was unavailable.

**Comparison.** Even `W` independent unit jobs all forced into a single
time slot require overlapping feasible time windows for those `W` jobs,
so `mu` can be `W` although the associated R1 instance has `c=S=0`.
No retrieved time-window theorem therefore directly yields the desired
parameter bound by just substituting `c` or `S` for `mu`. Transformations
that guess a separate precise time for each job would already solve the
unknown scheduling problem and are not a free reduction.

## What should and should not be claimed

The previous review establishes that the artificial ordered-pair edges
are known as **discrepancy precedence constraints** (Balas;
Balas–Simonetti; Cire–van Hoeve), and connects the supplied order to
poset linear discrepancy. Their finite-state methods are important prior
art; merely converting ROB capacity to such edges is not a newly named
graph class. Their reviewed bounds are exponential in the discrepancy
parameter `B`, not in `B-W`.

The following ingredients are foundational: completion-set dominance,
non-delay normalization for this unit-time precedence model, Bellman
recursion, contracting forced transitions, and shortest paths in a
finite acyclic state graph. None should be advertised independently as
a novel general scheduling algorithm.

The potential additional contribution is the **specific structural
count** showing that R1 branch states have fewer than `c` completed
unretired entries, and the resulting uniform-in-`W` bounds. At `c=1`
this computes arbitrary optima and strictly extends the preceding
perfect-saturation decision criterion. The corridor's potentially new
part is its `c+S` completion-set restriction, not subset dynamic
programming itself. This finite search found no primary theorem stated
with these exact implications, and did not establish historical novelty.

The remaining consequential gap is checking the full 2026 degeneracy
preprint and the complete active-schedule papers for refinements beyond
their retrieved statements. A future paper should cite them even if the
parameter separation survives that reading. No claim of a new solution
to unrestricted fixed-machine precedence scheduling follows: the
supplied order and discrepancy constraints are essential hypotheses.

## Search record and reproducibility

Both search engines were used; recent-source checks used a one-year
recency filter with the stronger engine. Representative exact queries:

```text
"discrepancy precedence" scheduling machines
"scheduling" "bounded" "frontier" unit jobs
"scheduling" "greedy" "width" "m+1"
"scheduling" "linear discrepancy" poset
"unit" "precedence" "idle" "parameterized"
"scheduling" "pathwidth" "slack" "Alix"
"precedence" "scheduling" "non-delay" "polynomial"
"scheduling" "incomparability graph" bandwidth
"scheduling" "width minus" machines
"A fixed-parameter algorithm for scheduling unit dependent tasks" pdf
"Improved Parameterized Algorithms for Scheduling with Precedence Constraints and Time Windows" pdf
"Parameterized Analysis of a Dynamic Programming Algorithm for a Parallel Machine Scheduling Problem" pdf
"FPT implicit enumeration of active schedules"
"A New Parameterized Complexity Analysis for Scheduling Precedence-Constrained Tasks on Parallel Machines"
"A New Parameter for Scheduling Dependent Tasks"
"Hanen" "Munier" "degeneracy" scheduling 2026
"Exploiting Structural Degeneracy" scheduling
"Exploiting Structural Degeneracy" site:papers.ssrn.com
```

Negative search outcomes are only a retrieval boundary. Full-text access
failures, abstract-only inspection, and the lecture's off-by-one issue
are recorded above rather than silently replaced by stronger claims.
The literature branch fetched `origin` successfully at
`2026-10-13T20:03:50Z`; `origin/main` remained
`bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`. Only this subagent's owned
directory was edited. No new solver experiment was run for this audit.
