# STRUCT2 continuation: published evidence and remaining scope

The CG/theta freeze is completely present at upload commit
`92e6939c75c87d4a6c5bd2c8459cbeafdfa13c89`. All 49 research files were
compared byte-for-byte with the attachment. Upload receipt commit:
`33ddb1b70219a5d11f30eacb9f18685043c2ead1`.

First continuation research commit:
`9f5b247be389ad9123afc6340b51f440424f2232`.

| Topic | New actual result | Verification boundary |
|---|---|---|
| CG formal semantics | [Universal actual folds and conjugacy iff isomorphism](cg/lean/STRONG_FOLD_SCOPE.md) | Lean 4.34.1, 11 audits, propext only; CG's exhaustive strong-switch/conjugacy classification remains written |
| CG all-odd coordinate bridge | [Original CDC/model isomorphism](cg/lean/ODD_COVER_SCOPE.md) | Every odd n>=1, all original edges and deck map; 37 dependency-chain audits and original-definition cross-checks through n=101 |
| CG connectedness and folds | [Actual connected model/CDC, strong decks and original fold](cg/lean/MODEL_STRUCTURE_SCOPE.md) | Universal graph-walk proofs; 50 dependency-chain audits; full automorphism count remains separate |
| CG universal type invariant | [Six-cycle characterization and arbitrary-automorphism type preservation](cg/lean/SIX_CYCLE_SCOPE.md) | Original CDC for every odd n>=3; 71 dependency-chain audits; original-edge cross-checks through n=101; n=1 exception retained |
| CG full automorphism upper bound | [Synchronized rings and actual finite embedding](cg/lean/UPPER_BOUND_SCOPE.md) | Every odd n>=3; all original CDC automorphisms inject into Fin(24n); 94 dependency-chain audits; matching family construction remains separate |
| CG exact automorphism family/count | [Explicit dihedral actions and original finite bijection](cg/lean/EXACT_AUTOMORPHISM_SCOPE.md) | Every odd n>=3; actual two-sided bijection with Fin(24n); 130 dependency-chain audits; strong-switch/cousin classification remains separate |
| CG exact strong-switch membership | [Necessary-and-sufficient parameter classification](cg/lean/STRONG_SWITCH_CLASSIFICATION_SCOPE.md) | Every odd n>=3; exactly the two half-turns and odd swapped reflections; 141 dependency-chain audits; universal conjugacy/cousin count remains separate |
| CG exact arbitrary-base classification | [External-base transport into the three folds](cg/lean/EXTERNAL_BASE_TRANSPORT_SCOPE.md) | Every odd n>=3; arbitrary simple external base, no finiteness needed; kernel-verified, independent written acceptance pending |
| CG/theta replay | [New execution receipts](verification/20261012-continuation/) | CG n=1,3,5,7; CG(3) Lean; 19 actual theta graphs; 1,942 legal scalar triples at n<=40 |
| Theta manuscript | [Seven-page draft](theta/paper/README.md) | Full written proofs retained; rendered PDF QA passed; this reorganization awaits new independent review |
| C66 expectation | [Second order and effective remainder](c66/SECOND_ORDER.md) | Written candidate and exact graph/DSU checks; independent acceptance pending |
| Sparse full TF | [Critical boundary and next correction](c66/CRITICAL_BOUNDARY.md) | Written all-n proof: c<8 converges, c>=8 diverges at np=4 log n-4-c(log n)^2/n; independent acceptance pending |
| Exact sparse window | [Matched expectation and finite remainder](c66/EXACT_WINDOW.md) | Written proof of E=1+B+o(1+B), B=(n!)^2(1-p)^binom(n,2), in the stated corridor; centered limit 1+exp(-x); independent acceptance pending |
| C66 formal structure | [Actual full-constraint component interface](c66/lean/README.md) | 12 clean Lean audits; endpoint/cycle-prefix transport; probability and entropy summation remain written |
| C66 singleton structure | [Actual singleton iff common endpoint action](c66/lean/SingletonComponent.lean) | Two-module chain: 21 clean audits; closure-based singleton classification; cardinality and analytic limit not Lean |
| Literature | [Existing C66 proof](c66/PRIOR_ART_2026-10-12.md), [new comparison](c66/PRIOR_ART_2026-10-13.md), original theta source gate | No firstness claim; access/recall limits recorded |

The complete Lean chain proves the advertised odd-parameter CG classification,
including arbitrary external bases with an isomorphic canonical double cover.
It is kernel-verified but not newly independently accepted.
The C66 limit overlaps an existing publicly posted proof claim; quantitative
formulas require review on their own scope.

Ownership and next steps are in `coordination/agents/STRUCT2-20261012.md`.
The matching upper bound in C66's finer window is now proved in writing in
`EXACT_WINDOW.md`: at `p=1-(n!)^(-2/binom(n,2))+2*x/n^2`, the full
expectation tends to `1+exp(-x)`. It includes explicit finite error bounds
and a nonempty-conditional limit of one. New receipts are under
`verification/20261013-c66-exact-window/`.
The next useful work is independent semantic acceptance of this exact-window
proof and the completed CG chain, then formalizing finite cardinality and
expectation interfaces. The first-coordinate projection's sparse interval
`2 <= c <= 4` remains a distinct unresolved question here. Further source
comparison is useful; no historical-firstness claim is made.

A recurring continuation task is enabled for this STRUCT2 conversation at
the user's request. Scheduled runs restore these checkpoints; this does
not represent uninterrupted computation between runs.
