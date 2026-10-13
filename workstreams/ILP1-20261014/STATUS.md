# ILP1 status

Snapshot: 13 October 2026 UTC / 14 October Asia/Singapore. Branch: `partner/dist-ILP1-20261014`.
Actually fetched baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3` (origin/main).
Last remotely verified publication before preparing this integration: `070b17ec765389dfa6507735ba0cb03edba8f89b`.
The commit containing this status is obtained with `git log -1 --format=%H -- workstreams/ILP1-20261014/STATUS.md`; publication must be checked against the live remote, not inferred from a local commit.

## Mathematical result status

| Result | Written proof | Independent review | Lean scope | Novelty |
| --- | --- | --- | --- | --- |
| Existence, static ROB equivalence, monotonicity | Yes | Yes | General model and operational bridge | Classical/prior-art overlap |
| Exact search and optimality certificates | Yes | Yes | Executable full schedule enumeration; operational Bellman bounds; attaining-potential theorem | Classical foundations |
| Fixed-schedule minimum window | Yes | Yes | General maximum/attainment/minimum theorem | Unconfirmed |
| Resource caps W=min(B,W), full window | Yes | Source reviewed | General formal proof | Basic model identities |
| Saturated-width and compact B_sat algorithm | Yes | Yes | Python and general recurrence not formalized | Standard ingredients |
| Universal online optimality iff W1 or W>=B | Yes | Yes | Arbitrary-policy four-job case only | Unconfirmed |
| Global strict deterministic ratio3/2 at B3,W2 | Yes | Yes | Pair lower obstruction only | Classical upper bound plus model-specific lower witness |
| Width2 to3: exact window N to3 | Yes | Yes | Not formalized | Unconfirmed; one-cycle performance caveat |
| Depth-two exact saturated-width curve | Yes | Yes | Not formalized | Unconfirmed |
| Chain-prefix exact epsilon-window formula | Yes | Yes | Not formalized | Unconfirmed |
| Oldest-inclusive optimal continuation at B=W+1 | Yes | Yes | Not formalized | Unconfirmed |
| Exact randomized ratio5/4 at B3,W2; stronger4E<=N+3F | Yes | Two independent reviews | Conditional scalar kernel only; full policy bridge open | Unconfirmed |
| Unified depth-two hidden-subset and advice family | Yes | Yes | Not formalized | Classical counting method; instance unconfirmed |
| Same sharp B3,W2 factors with additive constants | Yes | Independent theory/verification review | Arbitrary-q block separation, offline2q and admission barrier verified; probability open | Classical product method; composition unconfirmed |
| B4,W3 uniform omission exceeds4/3 | Exact counterexample | Independent CSP and probability tree | Not formalized | No priority claim |

A proof status is not a historical-priority assertion. Independent agents are not journal referees. Finite family ratios are strict unless stated otherwise. R18 separately proves that the sharp B3,W2 randomized and deterministic factors persist when an input-independent additive constant is allowed; this uses an explicit two-input repeating construction.

## Actual verification

Lean4.34.1, compiler commit5045d0056413266e57c625dcd7c365b10e377c52, bundled Std, no Mathlib. Root fresh recompilation and axiom audit passed:68 core declarations,18 footprint declarations,20 supplementary Bellman/search declarations 10 conditional randomized-potential declarations and20 actual repeated-gadget declarations,136 distinct audited endpoints. Shared imported declarations are not counted twice. Only standard propext/Classical.choice/Quot.sound occur. See evidence/lean-root, evidence/lean-footprint-root evidence/lean-bellman-root, evidence/lean-uniform-root and evidence/lean-repeated-root. The new conditional kernel was also independently recompiled and reviewed in subagents/formal-dp/UNIFORM_POTENTIAL_REVIEW.md. No unproved placeholders or new axioms are accepted. A documented host process-path shim is used without modifying Lean or its kernel.

Python unit tests:12 groups passed. The unchanged baseline audit covers all1100 forward DAGs on N0..5,26706 resource cases plus100 seeded random DAGs,32106 checked certificates overall. Independent solver agreement covers17378 cases including all684 fan-in-two DAGs on N0..5 plus1000 random cases. The assignment/replay audit covers264121 cases. These datasets overlap.

Additional focused audits:216 layered-family horizon decisions;5720 depth-two decisions;2020 chain-prefix optimum/replay comparisons and1185 approximate thresholds;350 compact-resource cross-checks with24 malformed-certificate rejection controls. Sources, seeds, measured timings and hashes are stored alongside each result. Counts are finite evidence, not universal proofs.

The ten-page research draft contains full proofs and explicit coverage boundaries. Actual build and visual-review records are in evidence/paper-build.json and evidence/paper-qa.md. The fixed-positive-tolerance single-slot corollary is also independently reviewed: for 1/(W+1)<=epsilon<1/W, required windows drop from Omega(N) to at mostW+1.

## Active next work

1. Publish the now-proved sharp randomized5/4 guarantee, its independent reviews, evidence and expanded manuscript.
2. The B3,W2 gap is solved in R15 and extended to additive constants in R18. Next: history/context-aware policies at B4,W3, a complete Lean semantics bridge, and resource-parametric extensions of the repeating construction. Uniform omission is refuted by R17; merely changing a fixed rank-probability vector cannot restore4/3.
3. Formalize structural resource families and improve the concrete efficient frontier-DP connection.
4. Continue prior-art searches: the window-edge idea already appears explicitly in Tullsen–Calder1998; missing Dubey1994 full text remains a gap.

## Continuation

An enabled recurring automation was actually created for this conversation, every2h starting14October2026 04:15 Asia/Singapore. It requests recovery, real research, checkpointing and authorized Git publication. It is not a claim of continuous computation between triggers; future runtime/tool availability is not guaranteed. Keep it enabled until the user asks to stop.


## Most recent research loop

The fair-younger candidate was first checked on all2,796,203 effective local-edge graphs throughN12. A direct D=5F-4E induction did not immediately close. The stronger potential K=3F+n-4E, with the nonempty adjacent-equality invariant, yields a complete arbitrary-size proof. Two independent reviewers reconstructed all cases; a separate684-input CSP/operational audit checked the identities and delicate cases. This is now a proved strict5/4 upper and matching lower bound, with historical novelty unconfirmed. R18 subsequently supplied a separate, reviewed separator-free repetition proof, establishing the same factors with additive constants. The N9 width-three counterexample illustrates why the successful B3 strategy cannot simply be generalized.
