# ILP1 status

Snapshot: 13 October 2026 UTC / 14 October Asia/Singapore. Branch: `partner/dist-ILP1-20261014`.
Actually fetched baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3` (origin/main).
Last remotely verified publication before preparing this integration: `4379581865cb3c7cf81ccd6397ade07faa9bbff4`.
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

A proof status is not a historical-priority assertion. Independent agents are not journal referees. All online ratios are strict multiplicative values without an additive constant; repeated-adversary claims require additional proof.

## Actual verification

Lean4.34.1, compiler commit5045d0056413266e57c625dcd7c365b10e377c52, bundled Std, no Mathlib. Root fresh recompilation and axiom audit passed:68 core declarations,18 footprint declarations,20 supplementary Bellman/search declarations,106 distinct audited endpoints. Shared imported declarations are not counted twice. Only standard propext/Classical.choice/Quot.sound occur. See evidence/lean-root, evidence/lean-footprint-root and evidence/lean-bellman-root. No unproved placeholders or new axioms are accepted. A documented host process-path shim is used without modifying Lean or its kernel.

Python unit tests:12 groups passed. The unchanged baseline audit covers all1100 forward DAGs on N0..5,26706 resource cases plus100 seeded random DAGs,32106 checked certificates overall. Independent solver agreement covers17378 cases including all684 fan-in-two DAGs on N0..5 plus1000 random cases. The assignment/replay audit covers264121 cases. These datasets overlap.

Additional focused audits:216 layered-family horizon decisions;5720 depth-two decisions;2020 chain-prefix optimum/replay comparisons and1185 approximate thresholds;350 compact-resource cross-checks with24 malformed-certificate rejection controls. Sources, seeds, measured timings and hashes are stored alongside each result. Counts are finite evidence, not universal proofs.

The seven-page research draft contains full proofs and explicit coverage boundaries. Actual build and visual-review records are in evidence/paper-build.json and evidence/paper-qa.md. The fixed-positive-tolerance single-slot corollary is also independently reviewed: for 1/(W+1)<=epsilon<1/W, required windows drop from Omega(N) to at mostW+1.

## Active next work

1. Publish the reviewed fixed-positive-tolerance single-slot window trade-off, formal proofs and manuscript.
2. Oldest-inclusive normalization at B=W+1 is now proved and independently reviewed; use the resulting B3,W2 scalar recurrence to investigate the unresolved randomized ratio, currently bounded by5/4 and3/2.
3. Formalize structural resource families and improve the concrete efficient frontier-DP connection.
4. Continue prior-art searches: the window-edge idea already appears explicitly in Tullsen–Calder1998; missing Dubey1994 full text remains a gap.

## Continuation

An enabled recurring automation was actually created for this conversation, every2h starting14October2026 04:15 Asia/Singapore. It requests recovery, real research, checkpointing and authorized Git publication. It is not a claim of continuous computation between triggers; future runtime/tool availability is not guaranteed. Keep it enabled until the user asks to stop.
