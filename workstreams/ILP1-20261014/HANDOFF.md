# ILP1 recovery checkpoint

## Real state and protection

Primary checkout: `/workspace/scratch/6a1539b44ef3/math-ilp1`.
Branch: `partner/dist-ILP1-20261014`.
Allowed changes: this workstream and `coordination/agents/ILP1-20261014.md` only.
Fetched main baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last verified remote: `e49b3b0fbbe69c3da08e3dba2c9fd4a3061883ae`, tree `53dad76132619927a7b859024b5a5fe83f85bf84`.
Its identical local source `c593c38f9f5d7e91b57ef52cc35a3401b7b1de15` is preserved on `partner/ilp1-local-lookahead-20261014`. Receipt: evidence/publication-e49b3b0.json.
Current integration adds actual macro recurrence, causal non-delay lifting and sharp counterexamples, with263 audited Lean endpoints. Publication is established only by a later actual fetch/tree receipt. Obtain this file's containing SHA from Git, not a predicted future hash.

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

Preserve MODEL.md and THEOREMS.md, including the later R26 causal policy lift and R27 non-delay tightness. Strong new results:

* Prefix potentials at B=W+1 give polynomial optimality certificates, regenerating every actual macro independently. Soundness telescopes; completeness uses exact suffix values. The checker does not require every accepted potential to be exact.
* At B4,W3, all but the final incoming operand may be known and an optimal first choice is still impossible. The two-chain construction has indegree/outdegree1; its repeated, barrier-separated version has indegree2 and supplies finite-lookahead lower bounds with additive constants.
* With Q=B+L, deterministic chunks give T<=T*+(B-1)floor((N-1)/Q). Uniform first-chunk offset gives E[T]<=T*+sum action spans/Q<=[1+(B-1)/Q]T*. The input must be independent of the offset. Actual callback implementation reads only visible operands. At B4,W3 this and the repeated lower bound give optimal excess Theta(1/(L+1)), not exact global constants.
* The random chunk policy bound is attained by repeated consecutive paired chains when B,W>=2,Q>=max(B,2B-3). This is policy-only sharpness: all-ready is optimal on this family. At Q4/B4/W3, offset costs4,5,6,5 give5/3, not7/4. N<=Q does not make a randomly shortened first chunk optimal.
* General true-DAG feasibility is W[1]-hard in c=B-W by the explicit biclique embedding in EXCESS_HARDNESS.md: horizon3,height2,c=k,all artificial edges redundant, optimum exactly3 or4. Lin source hardness is imported. The mechanism has strong2016 prior art and unbounded fan-in; neither historical novelty nor two-input hardness is claimed.
* Lean now proves actual ready/hole counts, finite-continuation dominance, non-delay normalization and initial/global schedule representation. Global non-delay optimal actual profiles and their same-action Legal maps exist under Forward and positive resources. This is stronger than a conditional Bellman interface, but still does not formalize the compressed algorithm.

R19 polynomial tiling, R20 FPT(c+S), R21 polynomial c1/XP(c), earlier resource formulas and sharp B3,W2 results remain proved with their recorded Lean limits. Do not redo their unchanged exhaustive experiments.

## Reproduction and current evidence

Lean `/workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean`, version4.34.1, Std only. Current root receipts have263 distinct endpoints, standard axioms only; source hashes must match. The actual macro runner rebuilds the entire new import chain in a fresh directory:

```sh
python workstreams/ILP1-20261014/formal/verify_macro_optimality.py --lean /workspace/scratch/6a1539b44ef3/ilp1-tools/lean-4.34.1-linux/bin/lean --proc-self-compat --output /tmp/ilp1-macro-check
python -m unittest discover -s workstreams/ILP1-20261014/tests -v
python workstreams/ILP1-20261014/tests/biclique_audit.py
python workstreams/ILP1-20261014/subagents/verification/random_offset_audit.py
python workstreams/ILP1-20261014/paper/build.py
```

Other pinned runners/receipts remain in formal/, subagents/formal-dp/ and evidence/lean-*-root. The legitimate field `admit` is not an admitted proof. `profile_realization` gives residual obligations only for initially incomplete jobs; do not silently call arbitrary dummy times of already completed jobs globally Legal. Initial-state representation does remove that restriction. Full randomized policy/expectation semantics is open.

Key fresh audit files: evidence/biclique-root.json; verification/certificate_results.json, repeated_lookahead_results.json, chunk_lookahead_results.json, random_offset_results.json; formal-dp READY/CONTINUATION/NONDELAY/REPRESENTATION_LEAN_REVIEW notes; evidence/lean-representation-root/receipt.json. Independent report hashes pin implementations; do not substitute newer sources under an old receipt.

The PDF remains the phase5 document with17 pages and its225-endpoint boundary; the separate current source notes and evidence cover263 endpoints. Rendered temporary pages are `/workspace/scratch/6a1539b44ef3/ilp1-paper-qa/phase5final-*.png`; inspect evidence/paper-qa.md for exact hashes. A transient Poppler PNG truncation can occur; decode every page with PIL and rerender failed pages. Never enable truncated-image acceptance.

## Concurrent work and exact next increments

Check live agents before reassigning. Old author worktrees remain separate; the new ratio6 and review6 agents have separate `partner/ilp1-<role>-20261014` branches. Root alone integrates and publishes.

* ForcedPrefix author f681f6a and independent review533cc38 are integrated. MacroOptimality author10bb728 and independent review76cdeef are integrated. The38 new endpoints are included in263, with fresh root and independent compiles. `prefixCost` is noncomputable, F_N=0, and the nonterminal attained recurrence is proved over real first-clear macro transitions. The executable finite-action enumeration/forced simulator/backward evaluator and complexity are the next formal gap.
* Causal non-delay lift author2fc0fde and independent review40dccf3 are integrated. It preserves each completing virtual policy's fixed-tape bound in the prefix-lookahead model, but does not preserve a finite-memory hardware budget. The five-job counterexample E={(3,4)},B4,W3,L0 has all four implemented offsets cost3 while T*=2. The offset4 first batch differs from the other three; do not collapse those traces.
* Counterexample search ff328a8 and generalization6cb8b76 refute universal non-delay3/2 and prove classical2-1/W tight even at B=W+1. The true-independent N=W² example has optimumW, youngest-ready2W-1. Repeated family proves persistence under additive constants (fanin W-1; W3 hasfanin2). Independent review is maintained in subagents/review6/. Smallest N9 at W3 is finite-verified after299,595 effectivegraphsN<=8; do not rerun unchanged enumeration.
* Stronger oldest-inclusive restriction is proved and independently reviewed using the R17 nine-job graph and a prev8-dependent barrier. Its bad causal rule is oldest plus largest other ready indices. Independent reviews2ac327d/225dd49 are integrated; the latter includes a partial legal trace disproving universal block separation. Better policies may still improve the bound; tightness of the entire non-delay class is not a minimax impossibility.
* True-fan-in-two FPT(c) status is not resolved by the general biclique reduction. The ancestor obstruction and literature parameter distinctions remain in the previous notes. A fruitful next step is essential-window-edge reductions or more structured positive algorithms.

Immediate recovery commands after checking Git: inspect `evidence/phase6-integration.json`, `subagents/review6/`, and ratio6's latest written proof. Reuse reviewed source hashes. Next substantive targets are an implementable formal macro recurrence and improved specific causal choice guarantees, not another unchanged enumeration. The ratio6 agent is now checking the specific lifted random-offset implementation at B4,W3,L0 for a3/2 expected bound; this remains a conjecture, separate from the disproved arbitrary-non-delay claim.

Do not postpone one verified checkpoint indefinitely because another proof arrives. Pin sources, publish, and continue the next increment.

## Literature pitfalls and failed routes

Cire--van Hoeve section9 already has the all-prefix discrepancy edges and exponential local-state representation. Feder et al.2004 has the same occupied-prefix window convention, hidden-tail and inverse-lookahead reasoning, with cache misses as objective. Jansen--Land--Kaluza2016 already links three-cycle/height-two scheduling and biclique; only public appendices/main abstract were accessible. Exact c-preserving ROB-order novelty is unconfirmed. IPEC2025's number of predecessors is a global count, not maximum input degree. True fan-in2 does not bound augmented Hasse indegree or height.

Oldest and critical-path greedies fail in general; height/work bounds need not meet; saturation thresholds need not be monotone; arbitrary added dependencies need not preserve an interval-order class. Dummy padding to N=kW fails. Forced macros can last Omega(N) at fixed B4W3. XP(c) is not FPT(c); general hardness does not transfer through naive binary expansion. Uniform omission/fixed-rank bias at B4W3 fails4/3, not every adaptive policy. The random chunk policy's own sharp example is not an information lower bound.

## Publication and recovery

HTTPS fetch works; direct shell push lacks credentials. The authorized GitHub connector Git Data flow works: create changed blobs/tree/commit from a pinned local source; assert API tree==local tree; update only partner/dist-ILP1-20261014 with exact expected old SHA and force=false. Actually fetch, query ls-remote and compare trees. Preserve local source history on a fresh partner/ilp1-local-... branch before recreating a clean tracking branch. No dirty resets.

The authorized continuation remains enabled for this conversation; this records recoverable research, not continuous computation between invocations. Do not create a duplicate task during an ongoing run. No formal publication authorship, new license, submission or DOI is authorized.
