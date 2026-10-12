# STRUCT2 continuation: published evidence and remaining scope

The CG/theta freeze is completely present at upload commit
`92e6939c75c87d4a6c5bd2c8459cbeafdfa13c89`. All 49 research files were
compared byte-for-byte with the attachment. Upload receipt commit:
`33ddb1b70219a5d11f30eacb9f18685043c2ead1`.

First continuation research commit:
`9f5b247be389ad9123afc6340b51f440424f2232`.

| Topic | New actual result | Verification boundary |
|---|---|---|
| CG formal semantics | [Universal actual folds and conjugacy iff isomorphism](cg/lean/STRONG_FOLD_SCOPE.md) | Lean 4.34.1, 11 audits, propext only; CG's all-odd full automorphism classification remains written |
| CG all-odd coordinate bridge | [Original CDC/model isomorphism](cg/lean/ODD_COVER_SCOPE.md) | Every odd n>=1, all original edges and deck map; 37 dependency-chain audits and original-definition cross-checks through n=101 |
| CG connectedness and folds | [Actual connected model/CDC, strong decks and original fold](cg/lean/MODEL_STRUCTURE_SCOPE.md) | Universal graph-walk proofs; 50 dependency-chain audits; full automorphism count remains separate |
| CG universal type invariant | [Six-cycle characterization and arbitrary-automorphism type preservation](cg/lean/SIX_CYCLE_SCOPE.md) | Original CDC for every odd n>=3; 71 dependency-chain audits; original-edge cross-checks through n=101; n=1 exception retained |
| CG full automorphism upper bound | [Synchronized rings and actual finite embedding](cg/lean/UPPER_BOUND_SCOPE.md) | Every odd n>=3; all original CDC automorphisms inject into Fin(24n); 94 dependency-chain audits; matching family construction remains separate |
| CG/theta replay | [New execution receipts](verification/20261012-continuation/) | CG n=1,3,5,7; CG(3) Lean; 19 actual theta graphs; 1,942 legal scalar triples at n<=40 |
| Theta manuscript | [Seven-page draft](theta/paper/README.md) | Full written proofs retained; rendered PDF QA passed; this reorganization awaits new independent review |
| C66 expectation | [Second order and effective remainder](c66/SECOND_ORDER.md) | Written candidate and exact graph/DSU checks; independent acceptance pending |
| Sparse full TF | [Leading constant and twin-free scale](c66/SPARSE_THRESHOLD.md), [constant-order refinement](c66/SPARSE_SHIFT.md) | Written candidate; groups kept distinct; K=4 boundary unresolved |
| Literature | [Existing C66 proof and comparison](c66/PRIOR_ART_2026-10-12.md), original theta source gate | No firstness claim; access/recall limits recorded |

The generic Lean theorem formalizes prior classical graph theory. It does
not promote the whole CG classification to a universal Lean theorem.
The C66 limit overlaps an existing publicly posted proof claim; quantitative
formulas require review on their own scope.

Ownership and next steps are in `coordination/agents/STRUCT2-20261012.md`.
The next useful work is the CG explicit dihedral parameter-family and strong-switch classification, independent
acceptance of C66, and the sparse boundary p=(4 log n-4)/n. Further prior-art
search should include incidence-matrix stabilizers and Burnside expectations.

A recurring continuation task is enabled for this STRUCT2 conversation at
the user's request. Scheduled runs restore these checkpoints; this does
not represent uninterrupted computation between runs.
