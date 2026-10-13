# ILP1 status

Snapshot: 14 October 2026, Asia/Singapore (13 October UTC).
Branch: `partner/dist-ILP1-20261014`.
Actually fetched main baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
Last remotely verified publication: `a9d7d430c2742f64502be2be30dfccefd940bbc0`.
The following integration is not remotely published until a separate fetch/tree receipt confirms it. Obtain this file's containing commit from Git; do not infer a future SHA from its text.

## Strongest current conclusions

| Result | Written and independently reviewed | Actual Lean coverage | Originality boundary |
| --- | --- | --- | --- |
| R21 polynomial optimum for arbitrary W at B=W+1, plus XP(c) | Complete proof, independent CSP/source audit | Actual dominance, forced action and global non-delay optimum; compressed algorithm remains open | Unconfirmed |
| R20 sharp horizon corridor and FPT(c+S) | Complete count, sharpness and algorithm proofs | Actual trace strip and work-count interval | Unconfirmed; frontier methods established |
| R22 polynomial prefix-potential certificate | Sound/complete proof; all macros independently regenerated | Not formalized | Classical potential certificate on R21 graph |
| R23 hidden-final-operand and repeated lookahead lower bounds | General proofs, independent observation/barrier review | Not formalized | Hidden-tail and repetition methods have close prior art |
| R24 chunk/random-offset upper bounds and inverse-lookahead order | General proofs and actual causal implementation audit | Not formalized | Same window convention and inverse-lookahead pattern precede this work |
| R25 W[1]-hardness in c=B-W for unrestricted true fan-in | Explicit c=k biclique embedding, two reviews and CSP checks | Not formalized | Known scheduling/biclique mechanism; exact R1 parameter/order combination unconfirmed |

At fixed B4,W3, with L extra visible incoming-dependency records, the best deterministic and oblivious-randomized competitive factors have excess Theta(1/(L+1)), even when additive constants are allowed and true indegree is at most two. With M=max(1,ceil(L/2)), the deterministic bounds are 1+1/(M+2) and1+9/(L+4); randomized bounds are1+1/[2(M+2)] and1+3/(L+4). Exact global constants remain open. The random-offset chunk policy's own upper factor1+(B-1)/(B+L) is exact for B,W>=2 and B+L>=max(B,2B-3). Its tight two-chain family is easy for another policy, so it is not an all-policy lower bound.

R25 settles the general FPT(c) search conditionally: such an algorithm would imply FPT=W[1]. Its graph has true height2 but unbounded fan-in. It does not classify two-input programs. The source problem hardness is imported from Lin; three-cycle/biclique scheduling reductions are prior work. A bounded-fan-in/height ancestor count explains why simply preserving the old redundant-window construction cannot work: max(0,N-B)<=sum(j=1..H-1)d^j if every artificial edge is already true-reachable. This is an elementary limitation, not a new hardness theorem.

Earlier R1--R21 results remain valid, including linear perfect-saturation tiling, exact/approximate resource families, sharp B3,W2 factors5/4 and3/2, and the B4,W3 uniform-omission counterexample. Precise quantifiers and proof-status attributes remain in THEOREMS.md.

## Actual verification

Lean4.34.1, compiler5045d0056413266e57c625dcd7c365b10e377c52, bundled Std, no Mathlib. Root receipts and current-source hashes cover225 distinct audited endpoints:68 core,18 footprint,20 supplementary Bellman/search,10 conditional randomized potential,20 repeated gadgets,25 work/corridor,25 ready,12 continuation,11 non-delay and16 finite/global representation. Imports are counted once. Only standard propext/Classical.choice/Quot.sound occur; no sorryAx or custom unproved axiom. The documented process-path compatibility shim does not modify compiler/kernel.

The64 new endpoints connect actual ROB state cardinalities, finite transition dominance, non-delay normalization and initial finite chains to the original Feasible/Optimal predicates. The global optimal non-delay actual profile has a Legal time assignment matching its same action list cycle by cycle. Independent fresh compiles and semantic reviews are saved in subagents/formal-dp/. This closes the initial representation gap. The first-clear-prefix macro decomposition, recurrence, executable optimized search and complexity are outside the225-endpoint checkpoint. Subsequent author-branch work must not silently change this count. Full randomized-policy semantics is also still unformalized.

Current integration checks:16 root unit-test groups pass (0.630 seconds). The new biclique audit passes1890 cases,898 YES/992 NO,898 CSP witnesses,2788 constructed replays and65663 redundant-edge checks. Prefix certificates:365 positive/33 adversarial cases. Random-offset independent audit:278 graph/lookahead cases,1672 exact offsets,8697 visibility-checked reads and5578 legal issue cycles; policy-sharpness audit:84 resource cases/624 offsets. These counts overlap earlier tests and are finite implementation evidence. Exact seeds/times/hashes live beside each report. Unchanged large exhaustive audits are reused.

The research draft is17 pages, with complete new lookahead and hardness proofs, certificate theorem and the225-endpoint formal boundary. Actual compilation and visual review are recorded in evidence/paper-build.json and evidence/paper-qa.md.

## Literature and next steps

Feder et al.2004 is close prior art for the occupied-window convention, last-item ambiguity, numerical3/2 and5/4 lower patterns and inverse-lookahead chunk reasoning; its objective is cache misses. Jansen--Land--Kaluza2016 is close prior for three-cycle/height-two biclique reductions; the public appendices were read, but full main-body access remains missing. No cost-preserving caching equivalence or exact earlier c-preserving ROB-order theorem was established. This is not novelty clearance. Other known constraints/frontier methods remain attributed to Cire--van Hoeve and resource-event DAG work.

Next concrete tasks already started on separate branches: actual first-clear-prefix decomposition and macro optimality in Lean; non-delay filling of chunk plans to remove avoidable barrier losses; complexity for true two-input programs at parameter c. A recent FPT result parameterizes the total number of predecessor jobs, not maximum indegree, and does not settle that restricted question. HANDOFF.md records exact pending commits, paths and commands.
