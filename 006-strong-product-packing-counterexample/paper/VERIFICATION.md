# Manuscript verification: v1.2

Checked 10 October 2026. [main.tex](main.tex), [paper.pdf](paper.pdf), [references.bib](references.bib) and [verification.json](verification.json) bind the current version. The [mathematical baseline 613108f](https://github.com/mio-qwq/math/tree/613108f1fa107a88a1049ed5f25e6b9313d576ed/006-strong-product-packing-counterexample) does not claim to contain this manuscript revision. Dated v1 and intermediate v1.1 receipts are preserved.

## Proof and source correspondence

The paper refutes the exact original Conjecture 3.1 for d=2,p=3,G=Q6 and explicit connected simple 608-point H. All cube subsets, all short code paths and all three vertex types are treated; one center covers both coordinates. The 9168-edge count and connectedness have full written proofs. Definitions through Discussion are identical to the earlier reviewed mathematics. An independent AI reviewer rederived the core argument and reviewed final source; no mathematical/reference must-fix remains. [Current review](../../publication/006-v1.2/REVIEW.md) is not external human peer review.

## Lean

Lean 4.34.1/Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612 is pinned. Unchanged three sources match actual primary and fresh-object replay logs; 12/12/26 declaration audits, exit code 0, no diagnostics. These 50 audits are not 50 new mathematical results.

`original_existence_counterexample` quantifies over every factor subset and provides explicit product existence on finite SimpleGraph/standard Walk. The strong product matches ordinary adjacency; reachability bridge holds for every bound without adding loops. No geometry premise, idealized metric or external certificate is assumed.

Final axioms are only `propext`, `Classical.choice`, `Quot.sound`, with no sorry/native_decide/added axiom/oracle. Cardinality 608 is kernel checked. Numerical gamma, H connectedness/edge count/diameter as separate Lean endpoints, optimal 64, smallest 608 and Q6×Q6 are not claimed.

This preparation rechecks source/log hashes, not a new heavy Lean compilation. The improved replay queries actual complete version, Mathlib Git root/HEAD and pin, tracked clean and configuration hashes. rc/dev/other-version synthetic controls fail closed. [Environment-only](../../publication/006-v1.2/evidence/environment.json) has proof_compiled=false; no empty-cache new-machine bootstrap or retroactive new-check claim.

## Exact programs

[Primary](../verify_graph.py) computes 64 cube and 64 code-source auxiliary BFS rows. [Separate reconstruction](../verify_independent.py) reads no primary artifact first, checks 184528 unordered adjacency candidates, all 608 auxiliary BFS rows / 369664 distances, edge-Lipschitz bounds and descending-neighbor paths.

Both check 2016 center pairs, 38912 same-center targets and zero violations. Full comparison matches 608 vertices, 9168 edges, 38912 code distances and witnesses. This uses the proved factor-max distance formula, not full-product all-source BFS. [Historical comparison](../results/independent-certificate-comparison.json) remains unchanged.

ROOT actually reran both implementations and comparison on 10 October; [new receipts](../../publication/006-v1.2/evidence/) keep distinct dates and hashes. [Extracted-archive replay](../../publication/006-v1.2/archive-replay.json) validates the distributed commands separately. Finite programs do not prove arbitrary-set obstruction or priority.

## Literature and six-aspect review

[Original v1](https://arxiv.org/html/2510.02749v1) and [published Conjecture 3.1](https://doi.org/10.1007/s00026-026-00814-0) agree. Perfect-code p=2d, close-vertex positive theorem and our overlapping-ball example have separate hypotheses. Classical counting and strong-product metric are attributed and proved here.

Fisher 1994, original Plotkin and some successors remain full-text gaps. Multi-round searches found no verified earlier complete result, which does not establish firstness. No commercial text similarity score. [Readiness report](../../PUBLICATION_READINESS.md) separately evaluates correctness, originality, significance, literature, readability and submission rules.

## PDF

- TeX SHA256: `f831f59c14d25f3b83134be4366fbdd1926af6f7e5bfa2c9467097f4a281c24e`.
- PDF SHA256: `67321311374782d68511a6ff3847dbdad61c6d626f7733c4fd5540ed3f99ad8f`; 129556 bytes, 15 pages.
- Bib SHA256: `b5901171ea86152430b558c13ba309a3ef22c836fa2c8998a9e60dbcdecfe529`.

Tectonic 0.17.0+20260731 exit code 0 from **2026-10-10T14:59:14.3598768Z** to **2026-10-10T14:59:15.8010914Z**; source hash unchanged before/after. All 15 pages rendered with Poppler scale-to 1600 and individually checked. Final pages 3 and 10–15 viewed directly; pages 1–2 and 4–9 match byte-identical already inspected preceding formal PNGs. [PDF receipt](../../publication/006-v1.2/evidence/pdf-check.json) gives method.

All 20 fonts embedded, nonempty text pages, no replacement/overlap/clipping/table overflow/missing glyph/undefined reference observed. All citation keys resolve; no TeX warnings/overfull/underfull diagnostics. Nonfatal Fontconfig startup message retained. Three v1.2 native-editor attempts failed on platform directories, not successful builds. Existing bundled executable exported the PDF without installing TeX or changing system settings.

## Identity and disclosure

Draft River Zhang / ORCID 0009-0004-2437-8566 / Chengdu Neusoft University supplied. Section 12 discloses substantial AI core mathematics, formalization, exact programs, literature, review and writing. No AI author or invented human-only process.

Human responsibility/contributions/contact/funding/conflicts, final authorship, paper license and external approval remain pending. Unspecified fields are not declared absent. [Version package](../../publication/006-v1.2/README.md) is preparation material, not a Zenodo record; no DOI created/reserved or submission/contact made.
