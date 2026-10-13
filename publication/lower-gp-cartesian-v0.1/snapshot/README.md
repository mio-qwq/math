# A sharp lower general-position bound for Cartesian products

Private manuscript version 0.1, 12 October 2026; author and license information
pending confirmation. This package is ready for a human responsibility review,
not an assertion of journal acceptance, external human peer review or a new DOI.

The paper refutes Conjecture 3 in the published *Lower general position in
Cartesian products* (Conjecture 2.10 of arXiv:2404.19451v1), constructs an
unbounded-gap family, and proves the optimal replacement

`gp⁻(G □ H) ≥ min{5,gp⁻(G),gp⁻(H)}`

for nonempty finite simple undirected graphs. The universal bound has an exact
computer-assisted proof. The fixed 319-vertex original-conjecture counterexample
is separately Lean verified; the entire paper is not Lean formalized.

## Reading and reproduction

- [Manuscript PDF](paper/main.pdf) and [standalone TeX](paper/main.tex).
- [BibTeX](paper/references.bib).
- [Actual scope and reproduction commands](REPRODUCE.md).
- [Originality comparison and primary sources](ORIGINALITY_REVIEW.md).
- [Preparation report](PUBLICATION_READINESS.md).
- [Independent mathematics audit](review/INDEPENDENT_MATHEMATICS.md) and
  [frozen-manuscript audit](review/FINAL_MANUSCRIPT_REVIEW.md).
- [Path-only replay adapter addendum](review/SUPPLEMENT_PORTABILITY_REVIEW.md),
  covering the subsequent optional-replay paragraph in REPRODUCE.md.
- [Exact copied-source provenance](source-bindings.json).

Run `python verify_manifest.py` before the three standard-library certificate
commands listed in REPRODUCE.md. Run without `-O`, which disables assertions.
Successful new receipts and logs are in `verification/`; copied historical
receipts retain their original dates. A separate delivered package-verification
receipt identifies the final archive hash and actual extracted-package replay.

The mathematical baseline is
`61488e05c9fe41984f483853f99e79f5715dc893` of
<https://github.com/mio-qwq/math>. No original primary-paper PDF or copyrighted
publisher file is redistributed; the references point to its source.

AI assistance in mathematics, code, Lean, literature review and writing is
disclosed in the manuscript. Author identities and responsibility, declarations
and license are not automatically inherited from another project paper.
