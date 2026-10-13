# Novelty audit

No historical-first or publication-readiness claim is made. Correctness, Lean coverage, independent review and novelty are separate attributes. Detailed independent reasoning is in [NOVELTY_REVIEW.md](subagents/literature/NOVELTY_REVIEW.md).

| Result | Current mathematical status | Novelty classification |
| --- | --- | --- |
| Finite optimum and exact Bellman DP | Complete written proof; model/optimum formally checked | Classical foundation |
| Eager ROB equals all-prefix augmented precedence | Written proof; general operational Lean equivalence; independent review | Strong prior-art overlap with event DAGs; specialized formal bridge |
| O(N+|E|) saturated-width optimum | Written proof and finite tests | Standard longest-path consequence |
| O((N+|E|) log N) unrestricted-width window saturation plus compact certificate | Written proof; implemented and independently checked | Standard monotonicity/longest-path ingredients; no major novelty claim |
| Exact fixed-schedule window footprint | Written proof; maximum existence/attainment and exact minimum window Lean verified | Equivalent representations not exhaustively ruled out |
| O(N 3^B poly(B)) frontier algorithm | Written proof with local representation | Strong prior art: discrepancy precedences and exponential-in-B MDD state compression, Cire–van Hoeve section9 |
| Both saturation thresholds nonmonotone | Four-job written counterexample; two solvers | NOVELTY_UNCONFIRMED; modest counterexample, not an open-problem resolution |
| Universal online optimality iff W=1 or W>=B | Full written proof; two independent reviewers; arbitrary-policy four-job case Lean verified | NOVELTY_UNCONFIRMED for this exact information/ROB model |
| Hidden-subset randomized minimax and advice count | Full written proof; independent review and finite audits | Method classical; exact R1 family originality unresolved |
| Hidden-chain resource-dependent loss/advice | Full written proof; independent review | Same unresolved novelty boundary |
| Fixed widths2 to3 reduce exact sufficient window fromN to3 | Full arbitrary-size proof; two independent reviews; finite checks | NOVELTY_UNCONFIRMED; prior resource trade-offs preclude broad first-idea claims |
| Depth-two exact saturated-width curve | Written proof; independent review and exhaustive family checks | NOVELTY_UNCONFIRMED |
| Sharp randomized5/4 bound at B3,W2 | General joint proof; two independent mathematical reviews; finite audits | NOVELTY_UNCONFIRMED; matching/revelation equivalence search still needed |
| Unified hidden-subset family, including B=W+1 with indegree bounds | Written proof; independent review and independent CSP checks | Counting/advice method classical; exact ordered-window instances unconfirmed |
| Separator-free two-input repetition at B3,W2 | General written proof; independent theory and verification review | Product/direct-sum methods classical; exact ROB composition unconfirmed |
| Nine-job failure of width-three uniform omission | Exact rational counterexample; independent probability-tree replay | Modest policy counterexample; no historical priority claim |
| Chain-prefix exact epsilon-window formula, linear necessary window and robust single-slot collapse | Written proof; independent verification and literature reviewer agreement | NOVELTY_UNCONFIRMED; head-of-line blocking is a known phenomenon |
| Linear perfect-saturation test at B=W+1,N=kW | Full written proof; independent CSP, abstract path-pattern and certificate-parser reviews | NOVELTY_UNCONFIRMED; path matching is classical, exact macro reduction requires separate comparison |
| Sharp completed-set corridor and FPT in c+S | Actual-model strip Lean verified; binomial count/sharpness/algorithm independently reviewed written proofs | NOVELTY_UNCONFIRMED; not a new general frontier-DP idea |
| Polynomial exact optimum for arbitrary W at B=W+1 | Complete proof, independent source/complexity review, CSP and operational checks | NOVELTY_UNCONFIRMED; searched discrepancy, width, degeneracy and time-window parameterizations |
| XP algorithm in c=B-W | General state/action counting proof; independent implementation audit | NOVELTY_UNCONFIRMED; no FPT-in-c or hardness assertion |

Do not claim that two-input instructions make the general scheduling problem easy. They impose at most two true producers per job but not a bounded number of consumers; window edges can add many predecessors. The hard resource/online examples here already have true indegree at most two, and the online dichotomy needs only a single path plus isolated jobs. Conversely, no new NP-hardness theorem is proved.

The main current candidates are precise resource thresholds and the separation of offline optimization from universal finite-information optimality. The layered exact-window collapse has only a one-cycle performance penalty at small windows; R13 was developed specifically to test robustness under fixed positive tolerance. Whether these results merit publication depends on deeper equivalence searches, stronger general results, and formalization. Independent AI review is not human peer review.

Next novelty queries should target bounded lookahead DAG scheduling, FIFO storage constraints, hidden-successor revelation, advice complexity and repeated finite-window adversaries. Publication authorship, licensing, submission and DOI decisions remain unset.


The targeted follow-up [NARROW_ONLINE_NOVELTY.md](subagents/literature/NARROW_ONLINE_NOVELTY.md) found classical two-machine scheduling/matching connections and recent related random-matching results, but no checked implication covering R15. A three-quarter double-issue pairing guarantee is not merely a generic two-neighbor random-matching guarantee: readiness and contiguous retirement matter. The general5/4 proof is complete and independently reviewed; its full Lean model bridge and its historical novelty are separate open tasks.

The current algorithm audit is [FORCED_SEGMENT_NOVELTY.md](subagents/literature/FORCED_SEGMENT_NOVELTY.md), following [PERFECT_SATURATION_NOVELTY.md](subagents/literature/PERFECT_SATURATION_NOVELTY.md). Cire–van Hoeve explicitly use the same all-prefix edges under the name discrepancy precedences, with a bounded-width MDD theorem. Thus R2/R4 must not be advertised as new graph constraints or a new finite-frontier idea. Recent incomparable-graph degeneracy and time-window overlap parameters can grow with W even when our c, or c+S, is fixed; the inspected results do not directly imply R20/R21 by substituting those parameters. This is a checked parameter distinction, not proof that no stronger prior theorem exists. The 2026 slides are not a fully audited published theorem, and the associated SSRN full text could not be obtained.
