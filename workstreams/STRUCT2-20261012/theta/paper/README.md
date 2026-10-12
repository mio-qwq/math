# Consolidated theta and bicyclic manuscript

`main.tex` and `theta-facet-maximizers.pdf` contain the complete compression,
balancing, parity-exclusion and block-reduction proof in a seven-page draft.
The maximal path triples are unique for every simple theta order n>=4;
the graph-defined bicyclic maximum uses n>=5 and treats n=4 separately.
Original journal numbering and prior tools are credited.

Build with pdfLaTeX, running twice to resolve references:

```
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The actual PDF was rendered and every page visually inspected. The final
build has no overfull/underfull boxes or unresolved references/citations.
`BUILD_VERIFICATION.json` records the source/PDF hashes and QA scope.
Build caches and page previews are not committed.

This is a consolidated AI-assisted draft, not a submitted paper or a final
authorship decision. The frozen proofs' separate AI review receipts remain
available in the parent directory. This exact reorganization has not received
a new independent written review or human peer review. No full Lean
polytope theorem or certification of historical firstness is asserted.
