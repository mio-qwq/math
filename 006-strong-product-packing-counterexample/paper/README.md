# A counterexample to packing-domination inheritance in strong products

[PDF](paper.pdf) · [Standalone LaTeX](main.tex) · [BibTeX](references.bib) · [Verification](VERIFICATION.md) · [Exact build receipt](verification.json).

Manuscript **v1.2**, 10 October 2026, gives a self-contained proof that

\[
\gamma_2^3(Q_6)=\infty,\qquad \gamma_2^3(Q_6\boxtimes H)\le64
\]

for an explicit finite connected simple graph H with 608 vertices and 9168 edges. This refutes Conjecture 3.1 of [the original preprint](https://arxiv.org/abs/2510.02749v1) and [published article](https://doi.org/10.1007/s00026-026-00814-0). The 64 centers are a witness, not a proved optimum; neither Q6×Q6 nor minimum auxiliary order is decided.

The complete existence assertion has an actual finite-SimpleGraph and standard-Walk Lean proof. Numerical gamma, H connectedness/edge count/diameter are not separate Lean endpoints. The first two auxiliary facts have written proofs and exact checks. [Actual source-specific compilation evidence](../results/lean-verification.json) is retained; this paper revision does not recompile unchanged mathematical sources.

Draft metadata: **River Zhang**, **Chengdu Neusoft University**, ORCID [0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566). Human accountability, actual contributions/declarations, contact, paper deposit license and external approval remain pending. Substantial OpenAI Codex/GPT-6-based agent-system involvement in construction, mathematics, Lean, programs, literature, independent AI review and writing is disclosed in Section 12. No AI author, external human peer review, completed human supervision or historical firstness is asserted.

Installed Tectonic 0.17.0+20260731 successfully built the 15-page PDF. All pages were rendered and inspected, all 20 fonts are embedded, and no unresolved-reference/overflow/missing-character TeX diagnostic remains. Native-editor platform-directory failures and a nonfatal Fontconfig startup message are recorded separately. The editor source remains main.tex.

```sh
tectonic main.tex
```

Alternatively run pdflatex main.tex twice with standard packages. The bibliography is embedded; references.bib provides the same 10 entries for journal adaptation and is not an extra build input. Different engines/timestamps can alter PDF bytes.

[Topic sources](../README.md) · [v1.2 supplement](../../publication/006-v1.2/README.md) · [Review](../../publication/006-v1.2/REVIEW.md) · [Originality](../../publication/ORIGINALITY_REVIEW.md) · [Preparation report](../../PUBLICATION_READINESS.md).

Old immutable releases and dated receipts remain intact. No Zenodo record/DOI, arXiv/journal submission or author contact was made.
