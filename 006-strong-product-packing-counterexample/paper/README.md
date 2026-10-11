# A counterexample to packing-domination inheritance in strong products

**Preprint v1.3 — 11 October 2026.** Authors: **River Zhang** (corresponding author, Chengdu Neusoft University, [ORCID 0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566)) and **Yongxian Zhang** (School of Computer Science and Engineering, South China University of Technology, [ORCID 0009-0000-3864-3536](https://orcid.org/0009-0000-3864-3536)). Contact: mioqwq@hotmail.com. No equal-first-author designation is made.

**Published on Zenodo (11 October 2026):** [Version DOI: 10.5281/zenodo.23293088](https://doi.org/10.5281/zenodo.23293088) · [Concept DOI: 10.5281/zenodo.23293087](https://doi.org/10.5281/zenodo.23293087). Manuscript v1.3, first Zenodo release V1; this is a non-peer-reviewed preprint.

[Current PDF](paper.pdf) · [Standalone LaTeX](main.tex) · [BibTeX](references.bib) · [v1.3 build and text checks](verification-v1.3.json) · [v1.2 historical verification](verification.json) · [v1.2 mathematical review](VERIFICATION.md).

The paper gives a self-contained construction of a finite connected simple graph H with 608 vertices and 9,168 edges for which
\[
\gamma_2^3(Q_6)=\infty,\qquad \gamma_2^3(Q_6\boxtimes H)\le64.
\]
This refutes Conjecture 3.1 of the [published source](https://doi.org/10.1007/s00026-026-00814-0), using the exact original packing and domination notions. The 64 centers are not claimed optimal; no minimum graph order or global historical firstness is established.

**Proof scope.** The mathematical definitions, constructions, lemmas and proofs from the previously reviewed manuscript have not changed. Three Lean sources verify the existence-level counterexample for finite simple graphs and actual walks; numerical gamma, H's connectivity and edge count are separately proved in the manuscript and verified by exact programs rather than being claimed as Lean endpoints. The unchanged mathematical sources retain their dated [Lean verification evidence](../results/lean-verification.json). This v1.3 update does **not** claim fresh Lean recompilation.

**Academic and disclosure status.** Published on Zenodo as a publicly accessible two-author preprint on 11 October 2026 ([Version DOI](https://doi.org/10.5281/zenodo.23293088)). It has not undergone external human peer review or been accepted by a journal; no arXiv submission is claimed. The manuscript discloses substantial AI involvement in discovery, proof, implementation, formalization, verification, review and writing. **Both authors confirmed the published text, their declarations and CC BY 4.0 manuscript license.** Original software, Lean sources and third-party materials retain their separate licenses. No third author or equal-first designation is claimed.

The [v1.3 publication and reproducibility package](../../publication/006-v1.3/README.md) is linked to the published [Zenodo V1 record](https://doi.org/10.5281/zenodo.23293088). Its deposited ZIP remains immutable; this README records the DOI after publication. The v1.2 [fixed reproducibility archive](../../publication/006-v1.2/README.md) remains historical and unchanged. The current PDF and TeX are checked together in [verification-v1.3.json](verification-v1.3.json). To compile:

```sh
tectonic main.tex
```

See the [project proof](../README.md), the [originality audit](../../publication/ORIGINALITY_REVIEW.md), and the [publication readiness report](../../PUBLICATION_READINESS.md) for precise limitations.