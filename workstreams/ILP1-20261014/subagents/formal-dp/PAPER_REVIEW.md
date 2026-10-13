# Independent mathematical and formal-scope review of the ILP1 draft

Reviewer: formal-DP subagent. Review date: 14 October 2026, Asia/Singapore.
Reviewed main-worktree base commit: `30631e7750c2e5e8e355723794752ff224e747e6`,
with the paper and other active files read directly as uncommitted work.
No main-worktree file was edited by this reviewer.

Initial paper SHA-256:
`5a16a66ab1458f9c11538e040675e02775666f1d64ace7e6ab49c769dcda1b2b`.
Final inspected revision SHA-256, including the corrected certificate boundary,
106-endpoint count, 1998 citation, and the approximate-threshold corollary:
`11bc37e5a430c05afa38fad910987b9f205580dbb46c64c102451483b5d31b8f`.
Later changes are not automatically covered by this review.

## Verdict and independence boundary

No remaining blocking mathematical error was found in the inspected revision.
The one concrete certificate-boundary error reported during review was corrected.
The principal resource families, robust-tolerance formula, and online
classification passed independent written-proof review under the stated R1
model. This is research-agent review, not journal peer review or novelty
clearance. No large experiment was rerun, and this review is not a new Lean
compilation receipt.

This reviewer wrote the three supplementary Bellman/search modules. Therefore
this report does **not** count as an independent proof review of those own
20 endpoints. Their inclusion/scope was checked against the main agent's
independent compilation receipts. The operational model, concrete time/lane
enumerator, resource modules, online obstruction, and paper's structural
proofs were written by other agents and were read independently here.

## Findings and dispositions

| ID | Finding | Disposition |
| --- | --- | --- |
| R1 | The compact minimal-window certificate originally required a longer augmented path at `B_sat-1` unconditionally. If `B_sat=1`, no smaller positive capacity exists, and `E_0` has self-loops rather than being the DAG used by the longest-path proof. | **Corrected and re-read.** The final inspected revision requires this path only when `B>1`, and explicitly handles `B=1`. The Python checker already had the correct branch. |
| R2 | The initial paper's total was 68+20=88 audited declarations, omitting the 18 new footprint endpoints. | **Corrected and verified.** The union of names in the three current root receipts has exactly 106 distinct declarations: 68+18+20. Recompiled imports were not counted again. |
| R3 | The initial related-work paragraph omitted the already located 1998 Tullsen–Calder report, earlier direct prior art for instruction-window dependency edges. | **Corrected and independently sourced.** The revised paragraph and bibliography cite the October 1998 report; original §3 was opened and read during this review. |
| R4 | Dubey's bibliography item lacks a stable URL/DOI; the OpenAI item records a commit but links mutable `main`. | Nonblocking reproducibility improvements: add Dubey DOI `10.1109/12.278481`, and replace the OpenAI URL with its already-recorded commit-pinned equivalent. |
| R5 | The abstract's phrase "only one extra cycle at small windows" is less precise than the proved range: the layered family costs one extra cycle for `2 <= B < 2K`, but costs `K` extra cycles at `B=1`. | Optional wording correction: say "at window two" or give the proved range. The body already states the exception correctly. |

The `O(N)` compact-certificate size is naturally a count of vertices/integer
entries. If bit complexity is discussed in a later version, distinguish this
from `O(N log N)` bits for binary indices and times.

## Independent mathematical checks

### Model, reduction, and algorithmic baseline

The added relation contains **all** edges `i+B <= j`, not just `j-B -> j`.
Necessity uses the whole retired prefix, and sufficiency gives both
`r <= j` and `j < r+B`. It retains unit latency and excludes same-cycle
chains. The displayed four-job offset-edge counterexample is valid.

The Bellman recurrence ranges over nonempty batches, with the terminal value
specified separately. This is legitimate because removing empty cycles does
not change any resource or precedence condition. A potential lower bound on
all legal transitions also covers empty cycles: their inequality is automatic.
The frontier state and transition bounds are upper bounds, not assertions
that every encoded state is reachable. Width at least B admits earliest
augmented-DAG layering because every antichain spans less than B index gaps.
The longest-path recurrence and prefix-maximum implementation match this claim.

The fixed-schedule footprint must include **equal** times as reversals and
must use `j-i+1`; both are present. Its positive-capacity convention gives
beta=1 for an empty schedule, compatible with the paper's positive B domain.
No efficient general threshold algorithm follows merely from minimizing the
footprint over optimal schedules; the draft explicitly avoids that claim.

### Exact and approximate resource families

For the layered `P_K`, every nonisolated vertex lies on a K-vertex path and
is therefore forced into its layer's cycle in a K-cycle schedule. At width
two this puts isolated job 0 in the last cycle; every B<N adds the conflicting
edge `0 -> N-1`. At width three the initial batch `{0,1,2}` attains K at B=3;
B<=2 hides forced-first-cycle job 2. The proof includes K=2. The K+1 witness
at B=2 is legal, so the displayed tolerance table and the warning against
interpreting threshold collapse as large runtime speedup are correct.

For the depth-two family, every required root must complete initially.
Admission of the last job forces the first `2m-B` indices initially too.
The union has exactly `m+min(r,2m-B)` members when `B>=m+r`. Issuing that
union admits all remaining jobs and leaves at most m of them. Thus both
directions and the stated width-saturation domain are correct, including
r=1 and r=floor(m/2).

For `Q_K`, before completion of the last chain job the admission frontier
can expose at most B-1 independent jobs, regardless of whether the chain
was delayed. This proves the tail-work lower bound; the displayed no-gap
chain and paired-independent witness attains it. The formula includes K=1,
B=1, and B>N. The integer condition for tolerance is exactly
`K+1 <= B+q min(B,W)`, with `q=floor(epsilon K)`; splitting the minimum gives
the two terms in the claimed threshold. The W=1 exception is separated.

The added single-slot corollary also holds at the lower tolerance endpoint:
`q>=floor(K/(W+1))` implies `K+1 <= (W+1)(q+1)`, bounding both terms at
width W+1. The linear lower bound at width W needs the strict condition
`epsilon<1/W`, which is retained. This proves the unbounded ratio at fixed
positive tolerance; it does not claim the exact threshold of Q_K changes
with width. The appended interleaving example is valid at B=W=2 and makes
clear that fixed topological program order is part of the instance.

### Online quantifiers and randomized bounds

The common initial observation has the same B visible roots and the same
known length B+L. Selecting a bad hidden x after inspecting a deterministic
rule's fixed first action is a legitimate fixed-instance construction.
For randomization, the proof averages over an x chosen independently of
coin flips: any first action covers at most W-1 of B-1 candidates, and
omitting job 0 covers none. Thus the conclusion is about some **fixed** input
with excess expected makespan, not an adaptive input observing realized coins.

The attaining chain schedule's prefix bound is valid because
`1 <= L <= B-W < B` and W-1>=1. After a miss, the extra root-only cycle
reveals/schedules x; taking the smallest unfinished roots thereafter gives
legal admission and adequate total throughput. Consequently the exact ratio
`1+(B-W)/((B-1)(L+1))` is properly stated only for this family.

The deterministic 3/2 *global* value at B=3,W=2 combines the four-job
information lower bound with Graham's non-delay upper bound on the augmented
DAG. Its randomized global value is correctly left between 5/4 and 3/2.
All are strict ratios without an additive term; the draft explicitly states
that finite examples alone do not prove an asymptotic competitive bound.

## Formal-coverage and evidence audit

The current source hashes in each listed root receipt were recomputed and
all matched. Each receipt reports PASS, exit code zero, and no unexpected
axioms. The distinct endpoint count is:

| Modules | Distinct printed endpoint count | Actual coverage |
| --- | ---: | --- |
| ROBModel, ROBOperational | 33 | Static/operational equivalence, retirement semantics, feasibility and optimum existence |
| OnlinePair | 16 | Arbitrary initial-window-local deterministic first action on the fixed four-job pair; integer cycle bound |
| ExactEnumeration | 12 | Literal finite time/lane assignment enumeration, checker equivalence to Feasible, returned optimal legal schedule |
| ResourceBounds | 7 | Effective-width cap and full-window equivalence |
| ResourceFootprint | 18 | Actual maximum reversal-distance specification and fixed-schedule minimum window |
| ROBBellman, FiniteSearch, BellmanExact | 20 | Operational lower potentials; separate generic finite-list search and attaining-potential certificates |
| **Total** | **106** | Names deduplicated across repeated imported-module compilation |

`ExactEnumeration.solve_complete` quantifies over every finite forward
Boolean dependency relation and positive B,W. Its witness is not conditional
on an unproved successor-enumeration axiom. By contrast, the generic
`FiniteSearch` transfer theorem explicitly requires the successor-list
membership equivalence. The manuscript distinguishes these correctly.

`ResourceFootprint` does not prove the cardinality formula for width footprint,
optimization over all optimal schedules, or unbounded saturation families.
`OnlinePair` does not formalize probability or the all-resource dichotomy.
The final paper lists only the fixed-schedule **minimum-window** formula in
its formal coverage and excludes the general online/family results. It does
not describe the Python implementation or frontier-DP optimization as verified
by the unrelated Lean exhaustive solver. These boundaries are accurate.

Existing JSON evidence was inspected, not rerun: 1,100 graphs/26,706 exhaustive
resource cases, 17,378 independent comparisons on 684 small graphs plus 1,000
larger seeded cases, 216 layered-family decisions, 5,720 depth-two decisions,
2,020 exact chain comparisons, 1,185 tolerance thresholds, and 350 compact-
certificate checks agree with the report. The root's 32,106 total includes
random resource cases; it must not replace the 26,706 exhaustive count or be
added to overlapping independent datasets. The paper currently preserves
that distinction and explicitly warns of overlap.

## Primary-source metadata checks and remaining literature limits

Opened during this review:

- [Wall, WRL 93/6](https://davidwall.info/papers/WRL-TR-93.6.pdf): original
  title page confirms David W. Wall and November 1993.
- [Tullsen–Calder report](https://cseweb.ucsd.edu/~calder/papers/UCSD-CSE98-CPProfile.pdf):
  cover confirms October 1998; §3 explicitly treats ordered instruction-window
  entry/exit and added dependencies for admission blocked by a full window.
- [Dubey institutional record](https://research.ibm.com/publications/instruction-window-size-trade-offs-and-characterization-of-program-parallelism):
  confirms the title, three authors, 1994, and links the publisher through
  [DOI 10.1109/12.278481](https://doi.org/10.1109/12.278481).
  Full-text mathematical comparison remains incomplete.
- [Coffman–Graham original scan](https://fanchung.ucsd.edu/ron/papers/72_04_two_processors.pdf):
  page-one screenshot confirms Acta Informatica 1, 200–213 (1972), the title,
  authors, and the exactly-two-processor unit-task setting. This review did
  not re-prove the entire original algorithm.
- [Navada et al. original](https://ericrotenberg.wordpress.ncsu.edu/files/2025/06/paper_PACT-19.pdf):
  confirms all three authors and PACT 2010; the 2025 hosting path is not the
  publication year.
- [Graham author bibliography](https://fanchung.ucsd.edu/ron/papers/papers.html):
  confirms the 1966 title, BSTJ 45, and pages 1563–1581.

The Fields PDF request failed in this review; its primary-agent original-PDF
inspection is recorded separately in LITERATURE.md. The September 2026 OpenAI
artifact's complete proof closure was not independently re-audited here.
The manuscript appropriately describes a current claim rather than either
unconditionally accepting it or asserting the old question remains open.
No exhaustive originality claim is justified by these source checks.
