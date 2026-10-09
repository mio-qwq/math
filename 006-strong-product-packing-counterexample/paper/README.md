# A counterexample to packing-domination inheritance in strong products

This directory contains the English [paper PDF](paper.pdf), its standalone [LaTeX source](main.tex), and the [manuscript verification record](VERIFICATION.md). The bibliography is embedded in the source; no additional TeX files are required.

The paper gives a self-contained proof that

\[
\gamma_2^3(Q_6)=\infty,
\qquad
\gamma_2^3(Q_6\boxtimes H)\le64,
\]

for the explicitly defined finite connected simple graph \(H\) with 608 vertices and 9,168 edges. This refutes Conjecture 3.1 as stated in [the original preprint v1](https://arxiv.org/abs/2510.02749v1) and [the published article](https://doi.org/10.1007/s00026-026-00814-0). The 64-center witness is not claimed to be optimal, and the separate \(Q_6\boxtimes Q_6\) feasibility problem is not resolved here.

The complete existence-level assertion has passed Lean checking on actual finite `SimpleGraph` objects and standard Mathlib `Walk`s. Connectedness of \(H\), its edge count and the numerical minimum function are separate boundaries: the first two have written proofs and exact graph checks, while the Lean sources do not define a numerical gamma function. See the paper and [source-specific verification records](../results/lean-verification.json).

**Academic status:** public research draft. Human author information and accountable human approval are pending. OpenAI Codex with a GPT-6-based agent system participated substantially in the construction, mathematics, formalization, exact-checker implementation, AI-agent reviews, literature searches and writing; the manuscript discloses these roles. No AI is listed as an author. Separate program implementations and AI-agent reviews do not constitute human peer review. This paper has not been submitted to arXiv or a journal; historical firstness is not established.

**PDF status:** compiled successfully on 9 October 2026 with Tectonic `0.17.0+20260731`; all 14 final PDF pages were rendered and individually inspected by the primary AI agent. All 20 PDF fonts are embedded. The TeX log has no unresolved references, warnings, overfull boxes or underfull boxes. The compiler also emitted a nonfatal Fontconfig startup diagnostic; it is recorded separately rather than described as an entirely silent build. See the [exact source/PDF hashes and build receipt](verification.json).

To compile independently, use a standard LaTeX engine with the common AMS packages, `geometry`, `booktabs`, `longtable` and `hyperref`, for example:

```sh
pdflatex main.tex
pdflatex main.tex
```

Two passes resolve cross-references. Alternatively, `tectonic main.tex` compiles the same standalone source and resolves references automatically. In this recorded environment, two attempts through the built-in editor's compiler failed to locate platform directories. The PDF was exported successfully using the already bundled Tectonic executable; no TeX distribution was installed. The environment failures are not counted as successful builds.

The [complete topic materials](../README.md) include the Lean modules, explicit graph, same-center certificate, two separately implemented Python checkers, replay script and literature scope record.
