# ILP1 status

Snapshot: 14 October 2026, Asia/Singapore (13 October UTC).
Branch: `partner/dist-ILP1-20261014`.
Actually fetched main baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last remotely verified publication: `310fabfae3cf7d12f64068c13b8a4111fe5aa41b`.
The next integration is not remotely published until its separate fetch/tree receipt exists.
Obtain this file's containing commit with `git log -1 --format=%H -- workstreams/ILP1-20261014/STATUS.md`; never infer a future SHA from this text.

## Current strongest algorithmic results

| Result | Written proof | Independent review | Actual Lean scope | Originality |
| --- | --- | --- | --- | --- |
| R19: O(N+E) perfect-saturation test, B=W+1,N=kW | Complete macro decomposition and path criterion | CSP/replay, flag patterns, independent negative parser | Not formalized | Unconfirmed |
| R20: horizon corridor, c=B-W,S=WH-N | Complete strip, sharp binomial count, exact FPT(c+S) algorithm | Theory, independent CSP/replay, separate Lean review | Actual trace strip and work-count interval; not binomial count or algorithm | Unconfirmed |
| R21: polynomial optimum for arbitrary W at B=W+1 | Complete non-delay/dominance and prefix recurrence proof | Independent proof/source/time-space review and CSP | Algorithm and non-delay optimum not formalized | Unconfirmed |
| R21: XP in general c=B-W | Complete state/action count and compressed graph | Independent general-c implementation and proof review | Not formalized | Unconfirmed |

R21 takes O(N min(B,N)(N+E)) indexed-graph operations and O(N+E) working space. Its proof does not assume bounded macro duration; a forced segment can be linear in N at fixed B4,W3. R20's FPT parameter is c+S, not c alone. Its exact per-layer bound is sum(j=c..c+S) choose(2c+S,j), attained by independent two-cycle instances; this is not a computational hardness bound.

Earlier results remain valid: R1–R5 establish the model, exact algorithms/certificates, resource monotonicity and fixed-schedule window footprint. Reviewed resource families have exact and approximate window thresholds, with an explicit one-cycle limitation on one exact-threshold example. R15 proves the sharp randomized5/4 guarantee at B3,W2; R18 extends it and the deterministic3/2 factor to a fixed additive constant using a two-input repeated construction. R17 refutes the B4,W3 uniform-omission extension and every fixed rank-bias4/3 guarantee; fully adaptive policy minimax is open. Precise statements and proof-status boundaries are in THEOREMS.md.

## Actual verification

Lean4.34.1, compiler commit5045d0056413266e57c625dcd7c365b10e377c52, bundled Std, no Mathlib. Root fresh receipts cover161 distinct audited endpoints:68 core,18 footprint,20 supplementary Bellman/search,10 conditional randomized potential,20 actual repeated gadgets,25 actual work-count/corridor. Repeated imports are counted once. Only standard propext/Classical.choice/Quot.sound occur; no sorryAx or added axiom is accepted. A documented own-process path shim leaves the compiler/kernel unchanged.

The new25 declarations were independently recompiled and semantically reviewed in subagents/formal-dp/CORRIDOR_LEAN_REVIEW.md. They quantify over actual completing ROBTrace objects, derive cardinality from actual lane injections, and handle the terminal layer, empty programs and natural-number truncation. The binomial candidate count, its sharpness, Python implementation and parameterized algorithm are explicitly outside this Lean result. The earlier randomized-potential kernel remains conditional, with the full policy/expectation bridge open.

Root unit tests:16 groups passed, including10,326 corridor graph/resource/horizon cases. Independent new datasets:4,797 corridor/CSP comparisons and1,921 replays;9,384 boundary inequalities on2,050 legal time maps;4,472 c1 optimizer comparisons and26,746 suffix values;13,380 general-c compressed comparisons plus15 normalization boundaries. The tiling has separate graph, path-pattern and certificate-tampering checks. The older baseline/resource/randomized audits are unchanged and preserved. Counts overlap; none is an infinite proof. Exact ranges, seeds, timings and hashes live beside each report.

The expanded14-page draft includes full new algorithm/corridor proofs. Its actual build and final visual verification are recorded separately in evidence/paper-build.json and evidence/paper-qa.md.

## Literature boundary

The all-prefix window edges are established discrepancy precedences: Cire–van Hoeve's2013 manuscript section9 also gives exponential local-state compression. R2/R4 are not a new constraint family or a new generic frontier idea. Recent time-window overlap and incomparable-graph degeneracy algorithms use parameters that can grow with W even at fixed c or c+S; no direct implication covering R19–R21 was established in the inspected sources. This finite search is not novelty clearance. The associated2026 SSRN full text and Dubey1994 full text remain access gaps. See LITERATURE.md, NOVELTY_AUDIT.md and the independent source-level notes.

## Work already continuing on independent branches

1. Polynomial optimality certificates for R21: a legal K-cycle trace plus prefix potentials checked against every independently regenerated macro; negative controls in progress.
2. Actual-model Lean ready/hole cardinality, forced non-delay action and progress lemmas, followed by the missing dominance/non-delay-optimum bridge. Do not count an unmerged author-run module in the161 total.
3. Information boundary at B4,W3: a two-chain hidden-final-parent family may require near-total future dependency knowledge for universal optimality. Written construction and independent review are in progress; do not mark it proved in this checkpoint.
4. Decide whether the XP(c) bound improves to FPT(c), or find an appropriate parameterized obstruction. No hardness result has been proved.

## Recovery and continuation

An authorized recurring continuation remains enabled and scoped to this conversation. It requests actual recovery, research, checkpointing and Git publication; it is not a claim of computation between invocations. Preserve it until the user asks to stop, subject to actual runtime availability. HANDOFF.md records paths, commands, active roles and publication mechanics.
