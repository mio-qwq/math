# Novelty audit

No historical-first or publication-readiness claim is made. Correctness, Lean coverage, independent review and novelty are separate attributes. Detailed independent reasoning is in [NOVELTY_REVIEW.md](subagents/literature/NOVELTY_REVIEW.md).

| Result | Current mathematical status | Novelty classification |
| --- | --- | --- |
| Finite optimum and exact Bellman DP | Complete written proof; model/optimum formally checked | Classical foundation |
| Eager ROB equals all-prefix augmented precedence | Written proof; general operational Lean equivalence; independent review | Strong prior-art overlap with event DAGs; specialized formal bridge |
| O(N+|E|) saturated-width optimum | Written proof and finite tests | Standard longest-path consequence |
| O((N+|E|) log N) unrestricted-width window saturation plus compact certificate | Written proof; implemented and independently checked | Standard monotonicity/longest-path ingredients; no major novelty claim |
| Exact fixed-schedule window footprint | Written proof; maximum existence/attainment and exact minimum window Lean verified | Equivalent representations not exhaustively ruled out |
| O(N 3^B poly(B)) frontier algorithm | Written proof with local representation | Elementary parameterized baseline; deeper prior-art audit pending |
| Both saturation thresholds nonmonotone | Four-job written counterexample; two solvers | NOVELTY_UNCONFIRMED; modest counterexample, not an open-problem resolution |
| Universal online optimality iff W=1 or W>=B | Full written proof; two independent reviewers; arbitrary-policy four-job case Lean verified | NOVELTY_UNCONFIRMED for this exact information/ROB model |
| Hidden-subset randomized minimax and advice count | Full written proof; independent review and finite audits | Method classical; exact R1 family originality unresolved |
| Hidden-chain resource-dependent loss/advice | Full written proof; independent review | Same unresolved novelty boundary |
| Fixed widths2 to3 reduce exact sufficient window fromN to3 | Full arbitrary-size proof; two independent reviews; finite checks | NOVELTY_UNCONFIRMED; prior resource trade-offs preclude broad first-idea claims |
| Depth-two exact saturated-width curve | Written proof; independent review and exhaustive family checks | NOVELTY_UNCONFIRMED |
| Chain-prefix exact epsilon-window formula, linear necessary window and robust single-slot collapse | Written proof; independent verification and literature reviewer agreement | NOVELTY_UNCONFIRMED; head-of-line blocking is a known phenomenon |

Do not claim that two-input instructions make the general scheduling problem easy. They impose at most two true producers per job but not a bounded number of consumers; window edges can add many predecessors. The hard resource/online examples here already have true indegree at most two, and the online dichotomy needs only a single path plus isolated jobs. Conversely, no new NP-hardness theorem is proved.

The main current candidates are precise resource thresholds and the separation of offline optimization from universal finite-information optimality. The layered exact-window collapse has only a one-cycle performance penalty at small windows; R13 was developed specifically to test robustness under fixed positive tolerance. Whether these results merit publication depends on deeper equivalence searches, stronger general results, and formalization. Independent AI review is not human peer review.

Next novelty queries should target bounded lookahead DAG scheduling, FIFO storage constraints, hidden-successor revelation, advice complexity and repeated finite-window adversaries. Publication authorship, licensing, submission and DOI decisions remain unset.
