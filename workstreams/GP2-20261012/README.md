# Kautz length four: structural repair and improved density bounds

Research record GP2-20261012, 2026-10-12. Candidate for repository integration.
The results below have complete written arguments and independent internal
AI-agent reviews. They are not external human peer review or complete Lean
formalizations. Historical priority is not certified.

## Latest proved interval

Let `m` be the **number of letters**, and let `Ka(m,4)` have all words
`abcd` with unequal adjacent letters, with arcs `abcd -> bcde` for `d!=e`.
General position means that no three distinct selected vertices lie on
**any** shortest directed path. Digons and nonadjacent repetitions are kept.

Let `rho` be the unique root in `(0,1/2)` of

    24rho^3-24rho^2+9rho-1=0,

and define

    beta=3/16+rho/2-9rho^2/4+4rho^3-3rho^4
        =11/48-rho^2/8
        =0.224808115216882691... .

The current verified conclusion is

    beta <= lambda_4 = lim_(m -> infinity) gp(Ka(m,4))/m^4
         <= 182/729 = 0.249657064471879286... .

A convenient completely rational lower endpoint, almost the same size, is

    14733/65536 <= lambda_4 <= 182/729.

This reduces the inherited interval `[26/125,377/1320]` from width about
`0.0776061` to about `0.0248489`, a reduction of about 68 percent.
Neither the exact limit nor the exact finite formula is established.
No conclusion for all other Kautz word lengths is inferred.

## Main proof chain

| Result | Complete source | What it establishes |
| --- | --- | --- |
| Elementary repair | [construction/STRICT_WINDOW_REPAIR.md](construction/STRICT_WINDOW_REPAIR.md) | Delete at most `73m^3` vertices from any original GP set to obtain a strict window code of four-distinct-letter words. |
| Exact asymptotic model | Same source, Sections 6–7 | `lambda_4` is the supremum of densities of **all finite** strict window codes, including arbitrary block weights. No fixed block count is proved complete. |
| Uniform positive gap below a quarter | [pair_color_bound/PROOF.md](pair_color_bound/PROOF.md) | Three levels on two-letter states and nine reciprocal-pair kernels give density at most `182/729`; this code inequality also holds for ordinary length-four comma-free codes. |
| Historical 57-word lift and optimal weights | [literature_lifts/JIGGS57_WEIGHTED_LIFT_V2.md](literature_lifts/JIGGS57_WEIGHTED_LIFT_V2.md) | A directly verified classical dictionary gives the rational all-parameter family below; an exact sum-of-squares compression optimizes this fixed template at beta. |
| Simple three-block formula | [construction/LOWER18_INDEPENDENT_REVIEW.md](construction/LOWER18_INDEPENDENT_REVIEW.md) | The classical eighteen-word ternary code gives exact counts at every alphabet size and density `2/9`; balancing is proved only within that template. |
| Finite upper bound with degree-two correction | [cyclic_moments/PROOF.md](cyclic_moments/PROOF.md) | Seven/nine cyclic moment coupling and an exact 877-type collision certificate give the finite radical bound below, without using repair. |
| Exact fourteen-state representation | [construction/FOURTEEN_STATE_REDUCTION.md](construction/FOURTEEN_STATE_REDUCTION.md) | Fourteen labels on triple states, 138 allowed transitions and 20 marked transitions represent every strict code after a count-preserving, idempotent completion. Independently reviewed; no bound on alphabet size is inferred. |

A strict code selects at most two occurrences among the five four-letter
windows in **every** eight-letter word, including repetitions. At a fixed
alphabet this is stronger than original GP. The repair proof is what makes
its universal upper bounds applicable to arbitrary original GP sets.

The 57-word dictionary is from B. H. Jiggs (1963), and the eighteen-word
dictionary is the reversal of a Golomb–Gordon–Welch (1958) construction.
Neither dictionary nor the classical rotation-orbit argument is claimed
as a new construction here. The actual source pages were read; the Kautz
bridge, counts and weight arguments are explicitly verified in this package.

## Explicit all-parameter bounds

For every integer `q>=1`,

    gp(Ka(16q,4)) >= 14733q^4-2528q^3+94q^2.

The four block sizes are `(5q,5q,3q,3q)`; every valid original word whose
block pattern is in the exact 57-word file is selected. More generally its
displayed 57-term polynomial counts arbitrary four block sizes exactly.
Rounding block proportions approaching the unique optimal weights proves
the algebraic lower endpoint beta for the limit.

For every integer `m>=3`,

    gp(Ka(m,4)) <= floor(182m^4/729)+73m^3,
    gp(Ka(m,4)) <= (m)_4/4+73m^3.

The second is the earlier rotation bound and can be smaller at some finite
values of m. Independently put

    P_m=8(m)_2+12(m)_3+15(m)_4+3(m)_5.

Then, for every integer `m>=2`,

    gp(Ka(m,4))
      <= floor(m^4 [9-sqrt(33-72P_m/m^7)]/12).

Its expansion is `((9-sqrt(33))/12)m^4+(9/sqrt(33))m^2+O(m)`.
Although its limiting coefficient is weaker than `182/729`, the smaller
finite error remains useful. `cyclic_moments/bound.py` evaluates this floor
with integer arithmetic and no floating-point certification. Any available
valid upper bounds, including the ambient vertex count, may be minimized.

The eighteen-word construction gives a simple exact lower formula for
every `m=3q+r>=3`, `r=0,1,2`:

| r | Proved lower bound |
| ---: | --- |
| 0 | `18q^4-16q^3+3q^2` |
| 1 | `18q^4+8q^3-2q^2` |
| 2 | `18q^4+32q^3+18q^2+4q` |

These formulas are construction sizes, not asserted GP optima. All valid
inherited lower constructions remain available; none was altered.

## Validation and mathematical status

Independent review reconstructs the original graph by its actual
shift/append adjacency and BFS. The 877-type upper certificate includes an
attaining local set and an explicit geodesic rejection for **every** local
subset exceeding its capacity. The lower certificates contain the original
adjacency, exact selected sets and all selected-pair distances for their
audited finite lifts. Damaged objects, distances, alphabet bindings and
certificate fields are rejected by deliberate negative controls.

The universal proofs are separate from those finite audits. The weighted
57-word optimization uses coefficient-level rational arithmetic and a
certified algebraic root interval. No floating-point solver optimum,
timeout or sample without a counterexample is used as a universal proof.

The final algebra review binds revision 2 directly. Revision 1 is preserved
with its disclosed erroneous decimal display for the root; its exact cubic
and proof identities were unchanged. The two versions' original-GP and
counting sections are byte-identical, as recorded in
[literature_lifts/REVISION_BINDING.md](literature_lifts/REVISION_BINDING.md).

See [REPRODUCE.md](REPRODUCE.md) for exact commands, the independent review
entries, checksums and the formalization boundary. The official Lean 4.34.1
executable could not start in this runtime; no new successful Lean compilation
or theorem-prover acceptance is claimed. No new unproved axioms or placeholder
Lean theorems were introduced.

## Evidence chronology and inherited sources

The seven/nine moment bound and the quarter bound are retained as proved
intermediate results. Their original proof and review files may state the
weaker interval known when each was completed. This README and the manifest
identify the latest result; a weaker number in a frozen earlier note is not
a withdrawal of a later theorem.

The starting main was `61488e05c9fe41984f483853f99e79f5715dc893`, with B
freeze `802e030aa8ac47a2018c9441a6b19f59b2db2535`. The inherited written
Kautz proofs and all other workstreams are unchanged. Public question and
literature coverage, including inaccessible-source limitations, are in
[SOURCES.md](SOURCES.md) and
[review/COMMA_FREE_LITERATURE_GATE.md](review/COMMA_FREE_LITERATURE_GATE.md).
No search non-detection is treated as a proof of openness or first discovery.

## Continuing structural questions

The exact limit remains the main question. The next useful restrictions must
couple the three pair levels with the complete prefix/suffix overlap data;
the general colored-C4 density alone loses information. A fixed fourteen-state
representation of all strict codes is recorded separately in
`construction/FOURTEEN_STATE_REDUCTION.md`. It labels **three-letter states**,
not alphabet blocks, and does not imply that fourteen blocks suffice.

Deleting a lower-order number of selected words to obtain independence is
false in general; a complete bipartite adjacency construction in
`global_upper/ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md` proves the obstruction.
The proposed generic three-color inequality `Pr(E)>=1/9` is also false.
Its exact obstruction is preserved in the corresponding C4 note. Neither
failed shortcut is used in the bounds above.

[ROUTE_NOTES.md](ROUTE_NOTES.md) records which earlier prospective claims
are superseded and why the completed exploratory searches are not being
repeated. The weighted 57-word construction in particular disproves the
earlier project conjecture `lambda_4=2/9`.
