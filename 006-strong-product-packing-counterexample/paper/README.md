# A counterexample to packing-domination inheritance in strong products

**Preprint v1.3 — 11 October 2026.** Authors: **River Zhang** (corresponding author, Chengdu Neusoft University, [ORCID 0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566)) and **Yongxian Zhang** (School of Computer Science and Engineering, South China University of Technology, [ORCID 0009-0000-3864-3536](https://orcid.org/0009-0000-3864-3536)). Contact: mioqwq@hotmail.com. No equal-first-author designation is made.

[Current PDF](paper.pdf) · [Standalone LaTeX](main.tex) · [BibTeX](references.bib) · [v1.3 build and text checks](verification-v1.3.json) · [v1.2 historical verification](verification.json) · [v1.2 mathematical review](VERIFICATION.md).

The paper gives a self-contained construction of a finite connected simple graph H with 608 vertices and 9,168 edges for which
\[
\gamma_2^3(Q_6)=\infty,\qquad \gamma_2^3(Q_6\boxtimes H)\le64.
\]
This refutes Conjecture 3.1 of the [published source](https://doi.org/10.1007/s00026-026-00814-0), using the exact original packing and domination notions. The 64 centers are not claimed optimal; no minimum graph order or global historical firstness is established.

**Proof scope.** The mathematical definitions, constructions, lemmas and proofs from the previously reviewed manuscript have not changed. Three Lean sources verify the existence-level counterexample for finite simple graphs and actual walks; numerical gamma, H's connectivity and edge count are separately proved in the manuscript and verified by exact programs rather than being claimed as Lean endpoints. The unchanged mathematical sources retain their dated [Lean verification evidence](../results/lean-verification.json). This v1.3 update does **not** claim fresh Lean recompilation.

**Academic and disclosure status.** Public, non-peer-reviewed research preprint; no Zenodo DOI, arXiv identifier or journal acceptance is claimed. The manuscript discloses substantial AI involvement in discovery, proof, implementation, formalization, literature work, agent review and drafting. Corresponding-author funding/interest statements are included. **Before external Zenodo deposit or journal submission, the coauthor must confirm the final text, his personal declarations and the selected CC BY 4.0 manuscript license.** No third author is listed or presumed. Separate code and third-party licenses remain applicable.

The v1.2 [fixed reproducibility ZIP and hashes](../../publication/006-v1.2/README.md) remain a **historical version-locked archive**; they must not be presented as covering the new v1.3 PDF. The current PDF and TeX are checked together in [verification-v1.3.json](verification-v1.3.json). To compile:

```sh
tectonic main.tex
```

See the [project proof](../README.md), the [originality audit](../../publication/ORIGINALITY_REVIEW.md), and the [publication readiness report](../../PUBLICATION_READINESS.md) for precise limitations.