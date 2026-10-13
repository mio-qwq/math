# Theory subagent checkpoint

Date: 14 October 2026, Asia/Singapore.
Owner: ILP1-20261014 theory subagent A.
Branch: `partner/ilp1-theory-20261014`.
Fetched baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Owned path: `workstreams/ILP1-20261014/subagents/theory/` only.
The main agent integrates local commits into its authorized distribution branch.

## Completed written mathematics

`STRUCTURAL_RESULTS.md` proves the exact all-prefix ROB precedence reduction,
the exact window footprint of a schedule, a linear-time unrestricted-width
optimum, polynomial exact unrestricted-width window saturation with path
certificates and a bottleneck formula, a fixed-window FPT state bound, a
complete `B=2` matching solution, a two-input barrier family exhibiting
unbounded additive work/height lower-bound gaps, and a four-job
nonmonotonicity counterexample for both saturation thresholds. The subsequent
Theorems 10–11 extend this to unbounded families: raising width 2 to 3
can lower `B_sat` from arbitrarily large `N` to exactly 3, with two-input
programs; another two-input family makes `W_sat` decrease by an arbitrarily
large additive amount as the window grows. Exact resource curves are given.
For the layered family the very large exact-window requirement prevents
only one additional cycle; the explicit epsilon-saturation table makes
this limitation precise and prevents conflating threshold size with IPC gain.
Theorems 12–14 then give an exact epsilon-resource curve for a chain prefix
followed by an independent suffix. At fixed width `W≥2` and tolerance
`epsilon<1/W`, its required window is at least
`(1−W epsilon)N/2+1`: approximate saturation can still require a window
linear in program length, even with true indegree/outdegree at most one.
All `K≥1` boundary cases are covered in the written proof.
Corollary 15 proves that, for fixed
`epsilon∈[1/(W+1),1/W)`, one extra issue slot lowers the same family's
epsilon-sufficient window from linear in `N` to at most `W+1`, including
the left endpoint. This is a fixed-tolerance resource tradeoff.

`NARROW_WINDOW_POLICY.md` proves an oldest-inclusive optimal-schedule
normalization for `B=W+1` using lexicographic minimality over all optimal
schedules, and a scalar exact recurrence for `B=3,W=2`. A uniform binary
randomized policy is now a concrete test target for the unresolved global
randomized interval `[5/4,3/2]`; no `5/4` upper bound is assumed.

`ONLINE_LOWER_BOUND.md` proves a family of `binomial(2q,q)` indistinguishable
programs with exact randomized minimax ratio tending to `3/2` and exact
fixed-length advice complexity. It also proves the universal online-optimality
resource dichotomy `W=1 or W≥B`, extending the main agent's chain construction
to a shorter chain and explicit sharper ratio. The single-hidden-root chain
family has exact deterministic/randomized minimax and advice formulas.
A separately attributed proof of the classical Graham non-delay bound
combines with the four-job pair to give the exact **global** deterministic
online minimax ratio `3/2` at `B=3,W=2`; a global randomized matching bound
remains open in this work.

Correctness labels: WRITTEN_PROOF and finite computational checks. Independent
verification and literature agents have separately agreed with the online
proofs; their saved reports, not this author's checkpoint, determine the exact
INDEPENDENTLY_REVIEWED scope. No Lean statement is claimed in this directory.
Historical novelty is unconfirmed for every candidate result. The all-prefix
reduction relates to known event-DAG architecture models according to the
literature agent; the basic DP, longest-path and advice-counting methods are
standard and not claimed as inventions.

## Reproduction

From the repository root:

```bash
python3 workstreams/ILP1-20261014/subagents/theory/sanity_check.py
```

`SANITY_RESULTS.json` records the actual output, runtime, Python version and
script SHA-256. Checks exhaust all 1,100 forward DAGs on zero through five
vertices and all cycle assignments through four vertices. They separately
replay the barrier, binomial and sharpened-chain schedules. Finite checks do
not replace the arbitrary-size proofs.

## Next work

1. Integrate the proof notes and review the final chain minimax/advice
   addendum independently, including the finite expected-ratio averaging.
2. Search hidden-successor scheduling and advice literature before making
   any priority claim. Existing online revelation models can have stronger
   known lower bounds, but they are not automatically the eager-ROB model.
3. Formalize the schedule equivalence, schedule footprint and observation
   indistinguishability argument in the central dedicated Lean project.
4. Study epsilon-sufficient resources after the layered family shows how
   unstable an exact saturation threshold can be despite tiny timing loss.
5. Seek a matching **global** online competitive upper bound; exact minimax
   values in the explicit families are not global guarantees.

No shared files, main-branch files, or other researchers' files were edited.
