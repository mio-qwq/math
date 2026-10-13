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
randomized policy was tested against the initially unresolved global
randomized interval `[5/4,3/2]`.
The first actual exhaustive policy search covers all 2,796,203 effective
graphs through 12 vertices, with no ratio above `5/4`, and independent
optimal/expected-time crosschecks on 683 graphs through six vertices.
This remains computational evidence only. A separate arbitrary-size proof
is now written in `RANDOMIZED_FIVE_QUARTERS.md`: it establishes
`4E<=N+3F<=5F` by a two-part descending induction on
`K_i=3F_i+n_i-4E_i`, with auxiliary inequality
`F_i=F_(i+1) => K_i+K_(i+1)>=1` restricted to nonempty suffixes.
This proves the fair policy's `5/4` bound and, with the established
four-job lower bound, the exact global randomized minimax ratio `5/4`.
Status is WRITTEN_PROOF and INDEPENDENTLY_REVIEWED: verification commit
`8566370336bd87985b5a3296725c70b426450e3e` saves a separate reconstruction
and independently generated finite checks of the auxiliary invariant.
No Lean or historical originality claim is made by this directory.

`ONE_EXTRA_ENTRY_FAMILY.md` then refutes the attempted stronger
oldest-`W-1` normalization: `B=4,W=3,N=5`, true edges `3->5,4->5`,
requires omitting job 2 in every two-cycle schedule. A hidden-omission
family at `B=W+1` has exact randomized family minimax
`3/2-1/[2(W+1-m)]`, with maximum indegree `d` whenever `W-m<=dm`.
In particular, `W=2q,m=q,d=1` gives a global lower bound tending to
`3/2` on disjoint-edge graphs despite a window only one larger than
issue width. This is a written proof with independent review underway.
The unified hidden-cover extension in the same note subsumes the earlier
binomial family and has now been independently reviewed in verification
commit `71d0ba7509ac193ae4686f41d37dc1eefc636ea9`.

The `B=4,W=3` uniform-younger-omission `4/3` conjecture is now REFUTED.
After exact search over all 299,595 effective graphs through eight
vertices, a nine-job graph with edges `2->5,3->5,3->6,6->9` gives
optimum three and exact expectation `37/9`, ratio `37/27>4/3`.
`WIDER_POLICY_COUNTEREXAMPLE.md` records the full nine-branch probability
tree, scope of computational minimum-length evidence, and a proof that
no fixed rank bias can guarantee `4/3`. The global minimax value for
fully adaptive policies is still unresolved. The four-input restricted
fixed-bias minimax is exactly `(13+sqrt(73))/16`; this is not a bound
for all online policies.

`REPEATED_GADGET_REVIEW.md` independently accepts the main agent's
no-extra-cycle block construction. It establishes randomized `5/4`
and deterministic `3/2` lower bounds at `B=3,W=2` even when an
input-independent additive constant is allowed. Cross-block admission,
information leakage, and history dependence were explicitly reviewed.

`PERFECT_SATURATION.md` gives a new closed structural result:
for variable `W>=2`, `B=W+1`, and `N=kW`, the work bound `T*=k`
is attained exactly when the consecutive W-job blocks admit a tiling
by one-cycle blocks and two-cycle boundary-swap pairs. Every k-cycle
schedule has this structure. A path-component parity condition yields
an O(N+|E|) algorithm, explicit schedules, and short negative edge
witness certificates. `perfect_saturation.py` implements it and passes
38,506 complete graph cases, 90 seeded random cases, all returned
certificate checks, and stated boundaries. Verification commit
`d566e057cf3cd7b2e9eaf597c5851cda5921b6df` independently accepts the
arbitrary-size proof. Originality remains unconfirmed; no Lean claim
is made for this new theorem.

`SLACK_CORRIDOR_REVIEW.md` independently accepts the main agent's
general `B=W+c`, horizon `H`, total idle-slot budget `S=WH-N` corridor.
It records exact state-pair transition equivalence, a sharper
`sum_(j=c)^(c+S) binomial(2c+S,j)` state count, and the distinction
between an FPT algorithm in `c+S` and unrestricted fixed-window DP.
The main agent's two-cycle independent-job construction attains every
counted state; this count sharpness is not a complexity lower bound.

`FORCED_SEGMENT_DP.md` now gives a stronger all-horizon result for
`B=W+1`: every nonclear completed state has a unique non-delay action,
so every choice occurs at one of `N+1` clear prefixes. A scalar macro
recurrence computes the exact optimum in
`O(N min(B,N)(N+|E|))` time and linear working space, even when `W`
is part of the input. The implemented predecessor-counter solver passes
7,605 complete resource cases, 60 seeded all-suffix comparisons and
stated boundaries. The same branch-state argument gives a written XP
algorithm for general excess `c`; its arc count is at most
`N(2^c-1) binomial(B,c)`. Independent review now accepts the proof,
implementation and complexity in verification commit
`dedfdb8f24cd385ef02e85db0e842ddbce48e4a8`; historical novelty and
Lean coverage remain unconfirmed for this new algorithm. A later
explicit chain-plus-isolates family shows forced segments can require
exactly `N/2` cycles even at fixed `B=4,W=3`.

`LOOKAHEAD_BOUNDARY.md` proves a new information boundary at `B=4,W=3`.
For every `N>=7`, two programs with true indegree/outdegree at most one
agree on all incoming edges except the last instruction, yet require
disjoint optimal first-action sets. Thus even knowing `N` and all
first `N-1` operands does not guarantee an optimal first decision;
every fixed extra-lookahead budget fails on some finite input. The
two-input family's exact randomized minimax is
`1+1/[2(M+2)]`, tending to one as its common prefix grows, so it does
not establish a constant asymptotic ratio above one. All 40 finite
programs and 600 first-action checks pass; independent review is in
progress. No Lean or originality claim is made for this addendum.
The single-block result is now independently accepted in formal-dp
commit `386e0c8ecd6b831ebc1c28b224a6bb9c8f8ef364`.

`REPEATED_LOOKAHEAD_REVIEW.md` independently accepts the verification
agent's no-extra-job block repetition. It gives fixed-lookahead lower
bounds that survive any input-independent additive constant, and exact
fixed-length advice `q` bits for `q` blocks. Maximum true indegree two
is preserved; the repeated construction does not retain outdegree one.

`LOOKAHEAD_UPPER_BOUND.md` gives the complementary chunk policy: with
`Q=B+L` visible jobs, solve one consecutive block at a time. Projecting
a global optimal schedule into blocks and counting crossing cycles
proves `T_chunk<=T*+(B-1)floor((N-1)/Q)`. At `B=4,W=3`, this gives
ratio at most `1+9/(L+4)`, and together with the repeated lower family
establishes that the optimal deterministic and randomized competitive
excess is `Theta(1/L)` as lookahead grows. Constants are not claimed
optimal. A causal callback implementation rejects forbidden reads and
passes 4,560 stated finite cases; independent review is underway.
The verification agent's random-offset improvement is independently
proved in the same note: choosing the initial block length uniformly
from `1,...,Q` gives `E[T]<=T*+sum(action spans)/Q`, hence the stronger
randomized ratio `1+3/(L+4)` at `B=4,W=3`. The causal implementation now
includes this genuine uniform draw with an injectable RNG. Exact
averaging over 26,616 finite offsets and 4,427 sampled-wrapper checks
passes; no Monte Carlo estimate is used for the expectation bounds.
Independent implementation and bound review is now saved by the
verification agent in `ae81ad4570f382793cda8eca66d46634b73f0a01`.
`RANDOM_OFFSET_SHARPNESS_REVIEW.md` independently accepts that agent's
two-chain construction: the specific random-offset chunk policy has
exact worst-case ratio `1+(B-1)/(B+L)` when `B,W>=2` and
`B+L>=2B-3`. This is a policy-specific sharpness result; all-ready
is optimal on that family, so it is not a minimax lower bound.
The random version need not be optimal even when the entire program
is initially visible; that statement belongs only to the default
deterministic single-block case.

`EAGER_POLICY_LIFT.md` proves a causal non-delay domination theorem
for every completing policy in the stated prefix-information model.
It maintains a separate virtual controller, retains its unfinished
planned jobs, fills actual free slots with currently ready jobs, and
skips virtual actions already completed in reality. Actual completion
always contains virtual completion, preserving visibility and ROB
admission. The lift is no slower for each fixed input/random tape.
The original chunk policy remains frozen; a separate callback module
implements the lift and its uniform-offset wrapper. All 20,238 finite
offset comparisons and 3,366 sampled wrapper calls pass, including
2,597 physically skipped virtual cycles. The two-chain sharpness
family becomes exactly optimal. No better universal ratio coefficient
has been proved; independent review of this increment is pending.

`EXCESS_HARDNESS_REVIEW.md` independently accepts the main agent's
balanced-biclique reduction, with exact makespan three versus four,
`c=k`, height two, true poset width `B`, and all artificial ROB edges
already true. It implies W[1]-hardness for unbounded true indegree,
using the independently inspected deterministic hardness source.
This is a parameter/order-preserving use of a known biclique scheduling
mechanism; historical novelty remains unconfirmed, and the binary-input
case is not settled by the construction.

`ONLINE_LOWER_BOUND.md` proves a family of `binomial(2q,q)` indistinguishable
programs with exact randomized minimax ratio tending to `3/2` and exact
fixed-length advice complexity. It also proves the universal online-optimality
resource dichotomy `W=1 or W≥B`, extending the main agent's chain construction
to a shorter chain and explicit sharper ratio. The single-hidden-root chain
family has exact deterministic/randomized minimax and advice formulas.
A separately attributed proof of the classical Graham non-delay bound
combines with the four-job pair to give the exact **global** deterministic
online minimax ratio `3/2` at `B=3,W=2`. The newly written randomized
matching upper bound is in the separate note just described.

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

1. Obtain independent semantic and callback review of the new causal
   non-delay lift. Seek a sharp family or a better universal constant
   for the lifted policy; removing one old family does not settle this.
2. Narrow the constant gap in the `Theta(1/L)` lookahead loss at
   `B=4,W=3`; preserve the oblivious-input and additive-constant scopes.
3. Determine whether the excess-only parameterized hardness survives
   maximum true indegree two. The reviewed biclique construction has
   unbounded fan-in and does not settle this restriction.
4. Continue targeted prior-work checks of the supplied-order excess
   parameter, prefix lookahead and conditional scheduling formalizations.
   Keep known scheduling techniques attributed and novelty unconfirmed.
5. Coordinate the central Lean work with the parent. The current theory
   notes are written proofs; claims of compiled formal coverage belong
   to the actual checked declarations and separate semantic reviews.

No shared files, main-branch files, or other researchers' files were edited.
