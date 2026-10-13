# ILP1 recovery checkpoint

## Real state and protection

Primary checkout: `/workspace/scratch/6a1539b44ef3/math-ilp1`.
Branch: `partner/dist-ILP1-20261014`.
Allowed changes: this workstream and `coordination/agents/ILP1-20261014.md` only.
Fetched main baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last verified remote: `a9d7d430c2742f64502be2be30dfccefd940bbc0`, tree `be64c91ed8e409ba2f18f5c9d18c2e236ba435ce`.
Its identical local source733d3cacc24d2cdcbb743e0266e73d13d7c46037 is preserved on `partner/ilp1-local-algorithms-20261014`. Receipt: evidence/publication-a9d7d43.json.
Current integration adds R22--R25,225 audited Lean endpoints and a17-page draft; publication is established only by a later actual fetch/tree receipt. Use live Git to identify this file's containing commit, not an invented future hash.

```sh
git fetch origin
git status --short --branch
git rev-parse HEAD origin/main origin/partner/dist-ILP1-20261014
git ls-remote origin refs/heads/partner/dist-ILP1-20261014
git log -8 --oneline
git log -1 --format=%H -- workstreams/ILP1-20261014/HANDOFF.md
```

Do not switch away from dirty work, reset, force push, or modify main/shared/006/other-agent files. Other researcher's startup checkout `/workspace/scratch/b1d6bae025af/math-crypto3` was dirty and is untouched. Check live agent states before launching duplicate work.

## Verified conclusions and boundaries

Preserve MODEL.md and THEOREMS.md R1--R25. Strong new results:

* Prefix potentials at B=W+1 give polynomial optimality certificates, regenerating every actual macro independently. Soundness telescopes; completeness uses exact suffix values. The checker does not require every accepted potential to be exact.
* At B4,W3, all but the final incoming operand may be known and an optimal first choice is still impossible. The two-chain construction has indegree/outdegree1; its repeated, barrier-separated version has indegree2 and supplies finite-lookahead lower bounds with additive constants.
* With Q=B+L, deterministic chunks give T<=T*+(B-1)floor((N-1)/Q). Uniform first-chunk offset gives E[T]<=T*+sum action spans/Q<=[1+(B-1)/Q]T*. The input must be independent of the offset. Actual callback implementation reads only visible operands. At B4,W3 this and the repeated lower bound give optimal excess Theta(1/(L+1)), not exact global constants.
* The random chunk policy bound is attained by repeated consecutive paired chains when B,W>=2,Q>=max(B,2B-3). This is policy-only sharpness: all-ready is optimal on this family. At Q4/B4/W3, offset costs4,5,6,5 give5/3, not7/4. N<=Q does not make a randomly shortened first chunk optimal.
* General true-DAG feasibility is W[1]-hard in c=B-W by the explicit biclique embedding in EXCESS_HARDNESS.md: horizon3,height2,c=k,all artificial edges redundant, optimum exactly3 or4. Lin source hardness is imported. The mechanism has strong2016 prior art and unbounded fan-in; neither historical novelty nor two-input hardness is claimed.
* Lean now proves actual ready/hole counts, finite-continuation dominance, non-delay normalization and initial/global schedule representation. Global non-delay optimal actual profiles and their same-action Legal maps exist under Forward and positive resources. This is stronger than a conditional Bellman interface, but still does not formalize the compressed algorithm.

R19 polynomial tiling, R20 FPT(c+S), R21 polynomial c1/XP(c), earlier resource formulas and sharp B3,W2 results remain proved with their recorded Lean limits. Do not redo their unchanged exhaustive experiments.

## Reproduction and current evidence

Lean `/workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean`, version4.34.1, Std only. Current root receipts have225 distinct endpoints, standard axioms only; source hashes must match. The actual representation runner rebuilds the entire new import chain in a fresh directory:

```sh
python workstreams/ILP1-20261014/formal/verify_representation.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-representation-check
python -m unittest discover -s workstreams/ILP1-20261014/tests -v
python workstreams/ILP1-20261014/tests/biclique_audit.py
python workstreams/ILP1-20261014/subagents/verification/random_offset_audit.py
python workstreams/ILP1-20261014/paper/build.py
```

Other pinned runners/receipts remain in formal/, subagents/formal-dp/ and evidence/lean-*-root. The legitimate field `admit` is not an admitted proof. `profile_realization` gives residual obligations only for initially incomplete jobs; do not silently call arbitrary dummy times of already completed jobs globally Legal. Initial-state representation does remove that restriction. Full randomized policy/expectation semantics is open.

Key fresh audit files: evidence/biclique-root.json; verification/certificate_results.json, repeated_lookahead_results.json, chunk_lookahead_results.json, random_offset_results.json; formal-dp READY/CONTINUATION/NONDELAY/REPRESENTATION_LEAN_REVIEW notes; evidence/lean-representation-root/receipt.json. Independent report hashes pin implementations; do not substitute newer sources under an old receipt.

The current PDF has17 pages. Rendered temporary pages are `/workspace/scratch/6a1539b44ef3/ilp1-paper-qa/phase5-*.png`; inspect evidence/paper-qa.md for exact hashes. A transient Poppler PNG truncation can occur; decode every page with PIL and rerender failed pages. Never enable truncated-image acceptance.

## Concurrent work and exact next increments

Sibling worktrees: ilp1-theory, ilp1-lean, ilp1-verification, ilp1-literature, ilp1-formal-dp, each on its own partner/ilp1-<role>-20261014 branch. Root alone integrates/publishes.

* Lean's representation commit0b4e56b and independent review5af93df are included. After this225-endpoint snapshot, author commitf681f6a6ddc379ec683ba0e6c5d5803c1c9c4052 contains18 new ForcedPrefix endpoints with fresh author evidence. It is intentionally pending the next integration and independent formal-dp review. Check live status/commit before cherry-picking. Its proof covers fixed-action successor uniqueness, forced-tail first-clear bounded existence/uniqueness and actual-profile first-macro decomposition. Do not count it among225 yet.
* Lean is next deriving actual PrefixMacro endpoint progress and OptimalFrom macro recurrence, then a prefix-indexed value function. Executable macro enumeration and complexity require another bridge. Formal_dp has been assigned independent review of f681f6a; its earlier FIRST_CLEAR_PREFIX_INTERFACE is only a proposal.
* Theory is proving that non-delay filling around a virtual chunk controller dominates each offset's original trajectory and is causal. It may eliminate the paired-chain sharpness family; no improved universal coefficient is proved yet. Verification can attack this next, using a controller that cannot read a full future DAG.
* Literature's bounded-fan-in audit58ca0b8 is integrated. It finds no checked direct FPT(c) or W-hardness theorem for the exact two-input R1 class, without claiming it is publicly open. It proves the elementary ancestor obstruction max(0,N-B)<=sum(d^j,j=1..H-1) when all artificial edges are true-reachable. Explore reductions using essential window edges or increased true height.

Do not endlessly wait to publish one checkpoint because another proof arrives. Pin verified sources, publish them, then continue the next meaningful increment.

## Literature pitfalls and failed routes

Cire--van Hoeve section9 already has the all-prefix discrepancy edges and exponential local-state representation. Feder et al.2004 has the same occupied-prefix window convention, hidden-tail and inverse-lookahead reasoning, with cache misses as objective. Jansen--Land--Kaluza2016 already links three-cycle/height-two scheduling and biclique; only public appendices/main abstract were accessible. Exact c-preserving ROB-order novelty is unconfirmed. IPEC2025's number of predecessors is a global count, not maximum input degree. True fan-in2 does not bound augmented Hasse indegree or height.

Oldest and critical-path greedies fail in general; height/work bounds need not meet; saturation thresholds need not be monotone; arbitrary added dependencies need not preserve an interval-order class. Dummy padding to N=kW fails. Forced macros can last Omega(N) at fixed B4W3. XP(c) is not FPT(c); general hardness does not transfer through naive binary expansion. Uniform omission/fixed-rank bias at B4W3 fails4/3, not every adaptive policy. The random chunk policy's own sharp example is not an information lower bound.

## Publication and recovery

HTTPS fetch works; direct shell push lacks credentials. The authorized GitHub connector Git Data flow works: create changed blobs/tree/commit from a pinned local source; assert API tree==local tree; update only partner/dist-ILP1-20261014 with exact expected old SHA and force=false. Actually fetch, query ls-remote and compare trees. Preserve local source history on a fresh partner/ilp1-local-... branch before recreating a clean tracking branch. No dirty resets.

The authorized continuation remains enabled for this conversation; this records recoverable research, not continuous computation between invocations. Do not create a duplicate task during an ongoing run. No formal publication authorship, new license, submission or DOI is authorized.
