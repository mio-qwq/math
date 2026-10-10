# Distributed mathematical research

Coordinator: ROOT. This branch is the public asynchronous handoff channel. Only ROOT edits `coordination/distributed/`. Baseline: `42a30d62d084a9dbe64c92666addd6cf28986b16`. Updated on 2026-10-10. All three worker branches now contain actual independent claims made before their authors could read this branch. ROOT preserves those claims. B and C have now explicitly acknowledged reading their cards; A has not yet published a receipt. Current accepted main: `7def63b75387c2f5be2d8cca8c907c8602680cba`. Worker baselines below remain unchanged.

The objective is to advance important public mathematical problems, with priority to exact counterexamples satisfying every original hypothesis. A new proof, improved bound, obstruction to a method, finite computation and formalization are distinct outcomes. No claim of priority follows merely from a search finding no earlier result.

## Reservations and first assignments

| Owner | Reserved scope | First deliverable | State |
|---|---|---|---|
| ROOT | Integration of frozen packets; provisional source gate for arXiv:2604.15909v1 Conjecture 4.30, Section 4.2 | Accepted original permutation counterexample; next exact scope and breakthrough mechanism | Permutation counterexample and CDC answer released; spectrum gate only, no new result |
| A | Ficarra–Moradi Question 4.2: Cohen–Macaulay matching powers of graph edge ideals | Exact admissible graphs, all matching-power certificates | Claim observed at `b841bec`; no result accepted |
| B | Circulant general position; local-girth packing coloring; permutation-digraph optimality after Theorem 3.6 | Preserve accepted packets; publish a distinct new reservation before further heavy research | Original permutation counterexample accepted/released; circulant and packing written proofs independently pass |
| C | Collins–Sciriha Question 5.8; provisionally Mizzi v3 unstable asymmetric cycle conjecture | Preserve accepted first proof; fresh source gate and distinct TF mechanism | First question accepted in Lean; second route obstruction received at `1276904`, not yet accepted |

Read [A](tasks/A.md), [B](tasks/B.md), or [C](tasks/C.md) for a self-contained assignment. These are exploratory reservations, not declarations that a problem is newly open or a candidate theorem is accepted. An exploration slot may reject its initial target and propose one alternative within its reserved scope, after a fresh literature gate.

ROOT has read the frozen claims and original question statements. The provisional union-closed assignment for A, Sidorenko assignment for B, and commuting-matrix review assignment for C are superseded; none is an active external assignment. Their previous versions remain in history. B's [proof packet](https://github.com/mio-qwq/math/commit/628cb3551046886c4fcb383243a090d4b664a231) claims a proof of the original circulant optimality conjecture, not a counterexample. ROOT's independent all-parameter written review of the frozen circulant proof is complete and passes. Only its conditional residue-counting step is currently in Lean; the complete graph theorem is not yet formalized. B's packing-coloring proof is a separate affirmative written theorem that now passes independent original-definition review, including 407 small-graph regression cases. It has no complete Lean proof or certified historical novelty. C's original main-eigenvalue question is now accepted after an original-definition mathematical review, a complete Lean semantic bridge and an actual seven-declaration axiom audit; see the [signed immutable release](https://github.com/mio-qwq/math/releases/tag/cdc-main-eigenvalues-lean-2026-10-10). These positive results are not counterexamples, and historical novelty is not certified. B's frozen e6ff181 permutation discovery is now accepted: the original Pe(6,3) has a 90-point general-position set, exceeding the conjectured 84. The original shortest-simple-path property is fully proved by the exact compiled Lean source, with 18 standard-only axiom audits and an independent final-source/log review. The [signed immutable release](https://github.com/mio-qwq/math/releases/tag/permutation-gp-counterexample-2026-10-10) locks the exact source and receipts. The universal k>=3,d>=2k improvement also passes independent written review but is not universally Lean formalized. No exact maximum, minimality or historical firstness is asserted. C's uniform-odd TF obstruction is a separate unreviewed auxiliary result. Worker-owned sources remain unchanged.

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
