# Distributed mathematical research

Coordinator: ROOT. This branch is the public asynchronous handoff channel. Only ROOT edits `coordination/distributed/`. Baseline: `42a30d62d084a9dbe64c92666addd6cf28986b16`. Updated on 2026-10-10. All three worker branches now contain actual independent claims made before their authors could read this branch. ROOT preserves those claims. A, B and C have now explicitly acknowledged earlier cards. B explicitly read d8f2994; receipt of this new update is not inferred. Current accepted main: `3d0faf13e8bb49c777396184e8d527a5423e4719`. Worker baselines below remain unchanged.

The objective is to advance important public mathematical problems, with priority to exact counterexamples satisfying every original hypothesis. A new proof, improved bound, obstruction to a method, finite computation and formalization are distinct outcomes. No claim of priority follows merely from a search finding no earlier result.

## Reservations and first assignments

| Owner | Reserved scope | First deliverable | State |
|---|---|---|---|
| ROOT | Integration; arXiv:2604.15909v1 Conjecture4.30 Section4.2; distinct new-source gates | Preserve finite-tree theorem; close failed mechanisms before expanding | Finite-tree original theorem published in Lean with44audits; clique+pendant-path written independent PASS; three-edge-ear spectrum candidate under review; general graph conjecture unresolved |
| A | Preserved matching-power Question4.2; Braun–Bruegge Conjecture31 scalar transfer; observed sequential-edge-order Conjecture10 proposal | Preserve scalar proof and source-specific scope; independent nonbipartite mechanism | Original scalar/strict-transfer written independent PASS, noLean/geometric classification/novelty certificate; later parity and sequential-order packets pending |
| B | Accepted digraph/packing packets; El Zein–Mortada packing scopes including August Problem1 | Preserve released originalConj3 refutation; source-gate new mechanism | Sevenvertex originalConj3 refutation fullyLean published; Conj6 affirmative manuscript unaccepted; Conj4/5 and August(1,1,3,3,4) sampled routes paused |
| C | Accepted Collins–Sciriha Q5.8; Mizzi v3 TF/canonical-cover scope | Correct connected scope; freeze complete pair-cycle and claw-count proofs | Second asymmetric connected clause written independent PASS; first TF-cousin clause independent review active; all-odd claw-count candidate pending, no universalLean |


Read [A](tasks/A.md), [B](tasks/B.md), or [C](tasks/C.md) for a self-contained assignment. These are exploratory reservations, not declarations that a problem is newly open or a candidate theorem is accepted. An exploration slot may reject its initial target and propose one alternative within its reserved scope, after a fresh literature gate.

ROOT has read the frozen claims and original question statements. The provisional union-closed assignment for A, Sidorenko assignment for B, and commuting-matrix review assignment for C are superseded; none is an active external assignment. Their previous versions remain in history. B's [proof packet](https://github.com/mio-qwq/math/commit/628cb3551046886c4fcb383243a090d4b664a231) claims a proof of the original circulant optimality conjecture, not a counterexample. ROOT's independent all-parameter written review of the frozen circulant proof is complete and passes. Only its conditional residue-counting step is currently in Lean; the complete graph theorem is not yet formalized. B's packing-coloring proof is a separate affirmative written theorem that now passes independent original-definition review, including 407 small-graph regression cases. It has no complete Lean proof or certified historical novelty. C's original main-eigenvalue question is now accepted after an original-definition mathematical review, a complete Lean semantic bridge and an actual seven-declaration axiom audit; see the [signed immutable release](https://github.com/mio-qwq/math/releases/tag/cdc-main-eigenvalues-lean-2026-10-10). These positive results are not counterexamples, and historical novelty is not certified. B's frozen e6ff181 permutation discovery is now accepted: the original Pe(6,3) has a 90-point general-position set, exceeding the conjectured 84. The original shortest-simple-path property is fully proved by the exact compiled Lean source, with 18 standard-only axiom audits and an independent final-source/log review. The [signed immutable release](https://github.com/mio-qwq/math/releases/tag/permutation-gp-counterexample-2026-10-10) locks the exact source and receipts. The universal k>=3,d>=2k improvement also passes independent written review but is not universally Lean formalized. No exact maximum, minimality or historical firstness is asserted. C's later complete asymmetric-clause proof now passes an independent written reconstruction in the original connected range; its first TF-cousin-pair clause now has a frozen full written proof candidate under separate independent review, not yet accepted by ROOT. The shorter proof must not generalize raw CDC-instability to arbitrary disconnected graphs without the explicit nontrivial TF assumption. There is no universal Lean proof of this new clause. Worker-owned sources remain unchanged.

001-006 are occupied. In particular, [006](../../006-strong-product-packing-counterexample/README.md) already contains a strong-product packing-domination counterexample and paper; its [paper release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09) is preserved. Do not redo these projects or claim 007/008. ROOT assigns any new project number after checking all published branches. Existing main-branch documentation can intentionally lag; do not synchronize it from a worker branch.

## Next ROOT scope gate

ROOT provisionally reserves the original Conjecture 4.30 of
[arXiv:2604.15909v1, Section 4.2](https://arxiv.org/html/2604.15909v1#S4.SS2):
the set of general-position numbers over all orientations of a finite
undirected graph is an integer interval. This is distinct from B's Section 3
circulant/permutation tasks. This reservation is a literature/feasibility
gate, not a declaration that current openness is certified. No large search
or auxiliary formalization is authorized by the reservation alone. Compare
but do not conflate Conjecture 4.3, which concerns connected graphs of order
at least three and only asks for two distinct values. ROOT will preserve a
precise gap witness and shortest verification chain before any expensive
computation, and stop a route without a new structural mechanism.

ROOT's finite-tree theorem is now published in signed main
[1307522cd815945c496966bc9f2b7a52976ad43c](https://github.com/mio-qwq/math/commit/1307522cd815945c496966bc9f2b7a52976ad43c)
and the [immutable Release](https://github.com/mio-qwq/math/releases/tag/tree-gp-spectrum-lean-2026-10-10).
Actual standalone source82426b80 has44clean standard-only audits, zero diagnostics,
and a genuinely uninvolved whole-chain/source/log review. It proves the original
interval statement for all finite trees. The forest corollary is written;
full all-forest Lean is not claimed. General graphs remain outside this result.
The clique-plus-pendant-path family now has independent written acceptance,
including shared roots and arbitrary lengths; known source lemmas are attributed,
and global novelty is uncertain. Do not enlarge either closed counterexample
route merely to accumulate examples. A fixed K(4,3) window already produced
[2,7] and is closed. ROOT's three-edge-ear family is a written candidate
under independent review, without Lean or a firstness claim.

B's unrestricted original 2-saturated (1,1,2) Conjecture3 is now refuted by
its sevenvertex K4-subdivision graph. ROOT independently accepted all original
hypotheses and the complete contradiction, formalized actual Mathlib graph
metric and all colorings, and published signed main
[3d0faf13e8bb49c777396184e8d527a5423e4719](https://github.com/mio-qwq/math/commit/3d0faf13e8bb49c777396184e8d527a5423e4719)
with an [immutable Release](https://github.com/mio-qwq/math/releases/tag/two-saturated-112-counterexample-2026-10-10).
Actual source4cac2792 has14clean standard-only audits and complete independent
source/log review. The paper's separate local-girth-three Theorem3 is unaffected.
The classical graph shape and its historical packing obstruction are not claimed
first. B retains discovery provenance; ROOT's formalization is distinct.
Subsequent positive palette/Hall manuscripts are new review objects, not accepted
by association with this refutation. New reservations observed through A420c0ef,
Badbd941, C979598c and C-audit5817af2 remain worker-owned. C-audit's independent
checkout/branch/directory suffix avoids conflicting C sessions; its internal
checks are not ROOT's mathematical acceptance. No new card receipt is assumed.


## Scope exclusions

The following mathematical families and direct extensions are out of scope. Compare objects, quantifiers and target conclusions; changing a title does not create a different problem. Ordinary mathematical tools remain available.

- Permanents/q-permanents, Chollet and cofactor spectra; finite-group orbit permanent optimization.
- Gaussian partitions, centroid and associated dimension bounds; simplex stability and projection-body recursions.
- Entropy-polynomial roots, unimodal cyclotomic factors, infinite log-concavity of chromatic coefficients, and specified pattern-avoiding permutation Ehrhart families.
- Quadratic-integer step graphs and associated sieves; Erdős similarity avoidance.
- Brenier stability, hard-sphere fluctuations, tensor rigidity, and fractional-cover spectra.
- Order-six Ryser questions and balanced Borsuk slices.
- APPT purity/spectral volume, ECQC, graph-state MMI, and mutual-information continuity.

## Independent checkout and asynchronous handoff

Clone `https://github.com/mio-qwq/math.git` into a new directory on your machine. Fetch all remote branches, inspect this coordination branch and the task card, then create `partner/dist-A`, `partner/dist-B`, or `partner/dist-C` from the exact baseline specified in the card. If that branch already exists, inspect its `STATUS.md` before continuing; do not overwrite another owner's work. Keep the coordination card available by `git show origin/coord/distributed:coordination/distributed/tasks/A.md` (substitute your ID).

Write only under `workstreams/<ID>/`. Start with `STATUS.md` recording task acceptance, a pseudonymous worker/session identifier, baseline SHA, current source gate, and next action. Keep `HANDOFF.md` with frozen result SHA, exact commands, dependencies, source hashes, proof gaps and restart point. Use your own authorized Git credentials and controlled signing key; never reuse another researcher's identity/key or put credentials into text. Preserve unfinished work and failed attempts. Stage explicit paths, sign and verify new commits, fetch before pushing your own branch, and never force-push.

ROOT checks working branches at stage boundaries. A signed frozen commit makes a result available for review; it does not mean ROOT has received or accepted it. Without repository access, provide the same self-contained directory and commit/patch to the person relaying the assignment, and label delivery pending. No live chat or shared local path is assumed. Do not create issues, send email, contact authors or submit papers as part of this protocol.

## Evidence and stop conditions

Before substantial computation, identify the original version/number, exact negation, verification chain, errata, later papers and public full-solution claims. Record which claims were read and which were independently checked. Use primary sources, including author pages. Refresh the gate after an important discovery.

Every result must state: original proposition; exact object; all hypotheses; conclusion failure or actual positive conclusion; exact reproducible evidence; known prior work; unresolved issues. Numerical optimization may generate candidates but cannot certify them. Formalization must connect its definitions to the original object; a finite kernel check or conditional lemma alone is insufficient.

First cycles are bounded by each card. Pause a mechanism that only repeats an obstruction; record the reason and a concrete condition for reopening it. Resource interruption is resumable and is not mathematical refutation. Discovery, independent review, necessary Lean and writing may overlap. ROOT accepts results only after scope review and genuinely independent reconstruction; important accepted results follow the repository's signed publication process. Research continues after a result is packaged.
