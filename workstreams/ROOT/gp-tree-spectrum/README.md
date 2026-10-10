# General-position spectra of finite trees

Every finite undirected tree has an integer-interval general-position spectrum over all its edge orientations. This proves the tree case of [Conjecture 4.30, arXiv:2604.15909v1](https://arxiv.org/html/2604.15909v1#S4.SS2).

`TreeGPSpectrumFinal.finite_tree_spectrum_interval` in [TreeGPSpectrum.lean](TreeGPSpectrum.lean) proves the complete statement for Mathlib's actual `SimpleGraph.IsTree`. It uses all shortest directed simple paths and all orientations; unreachable ordered pairs impose no constraint. No leaf-step, graph-isomorphism or GP/rank equivalence is assumed in the final theorem.

The standalone source compiled under Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. The exact source passed 44 declaration audits with zero warnings, errors or panics and only `propext`, `Classical.choice`, `Quot.sound`; see [receipt](lean-audit.json) and [log](lean-audit.log). In the repository's fixed package workspace, reproduce with:

```powershell
Set-Location 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/gp-tree-spectrum/TreeGPSpectrum.lean
```

The proof combines an original-definition rank characterization, constructive leaf extension, actual GP maximum cardinalities, finite-tree deletion and shortest-path transport under graph isomorphisms. [PROOF.md](PROOF.md) gives the mathematical argument and [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) records its independent semantic review.

The original paper proves spectra for spiders and caterpillars, among other families. This theorem covers every finite tree. An all-forest corollary follows on paper by connected-component sums; that corollary is not a final Lean theorem in this file. The conjecture for arbitrary graphs remains unresolved by this result. Multiple source checks did not locate an earlier all-tree interval proof, but historical novelty has not been certified.

Mathematical reasoning, code and this note were developed with AI assistance. The independent mathematical review used a separate AI agent uninvolved in discovery and proof drafting; it is not external peer review. No AI system is listed as an author.
