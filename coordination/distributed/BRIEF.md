# Distributed mathematical research

Coordinator: ROOT. This branch is the public asynchronous handoff channel. Only ROOT edits `coordination/distributed/`. Baseline: `42a30d62d084a9dbe64c92666addd6cf28986b16`. Updated on 2026-10-10. All three worker branches now contain actual independent claims made before their authors could read this branch. ROOT preserves those claims. Receipt of these updated cards is not yet confirmed.

The objective is to advance important public mathematical problems, with priority to exact counterexamples satisfying every original hypothesis. A new proof, improved bound, obstruction to a method, finite computation and formalization are distinct outcomes. No claim of priority follows merely from a search finding no earlier result.

## Reservations and first assignments

| Owner | Reserved scope | First deliverable | State |
|---|---|---|---|
| ROOT | Independent acceptance of B's frozen circulant proof; existing directed-girth and commuting-matrix mechanisms | Original-definition review and necessary Lean bridge | Active locally |
| A | Ficarra–Moradi Question 4.2: Cohen–Macaulay matching powers of graph edge ideals | Exact admissible graphs, all matching-power certificates | Claim observed at `b841bec`; no result accepted |
| B | Consecutive-generator circulant general position; earlier local-girth packing coloring paused | Frozen proof packet and literature record | Packet observed at `628cb35`; ROOT acceptance pending |
| C | Collins–Sciriha Question 5.8: canonical double covers and main eigenvalue sets | Exact cover isomorphism and main-spectrum comparison | Claim observed at `8e1fa77`; no result accepted |

Read [A](tasks/A.md), [B](tasks/B.md), or [C](tasks/C.md) for a self-contained assignment. These are exploratory reservations, not declarations that a problem is newly open or a candidate theorem is accepted. An exploration slot may reject its initial target and propose one alternative within its reserved scope, after a fresh literature gate.

ROOT has read the frozen claims and original question statements. The provisional union-closed assignment for A, Sidorenko assignment for B, and commuting-matrix review assignment for C are superseded; none is an active external assignment. Their previous versions remain in history. B's [proof packet](https://github.com/mio-qwq/math/commit/628cb3551046886c4fcb383243a090d4b664a231) claims a proof of the original circulant optimality conjecture, not a counterexample. Its internal review is evidence to examine, not ROOT's acceptance. ROOT will independently review it without modifying B's frozen files. A and C continue their disjoint discovery mechanisms; no immediate reassignment is inferred from a publication.

001-006 are occupied. In particular, [006](../../006-strong-product-packing-counterexample/README.md) already contains a strong-product packing-domination counterexample and paper; its [paper release](https://github.com/mio-qwq/math/releases/tag/006-paper-v1-2026-10-09) is preserved. Do not redo these projects or claim 007/008. ROOT assigns any new project number after checking all published branches. Existing main-branch documentation can intentionally lag; do not synchronize it from a worker branch.

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
