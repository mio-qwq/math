# A structural obstruction to (1,1,3,3,4)-packing colorings

Private manuscript v0.1, 12 October 2026. Human author information and
publication permission have not been confirmed for this paper. No new DOI or
submission is claimed. The published 006 paper is a different result and is
not changed by these materials.

## Mathematical result

For every odd integer k >= 3, replace each vertex of a ring of k diamonds by
a triangle, joining reciprocal incidences. The resulting graph G_k is simple,
connected, cubic, claw-free and diamond-free, has 12k vertices and 18k edges,
and has no (1,1,3,3,4)-packing coloring. Distinct vertices with the same label
must have distance strictly greater than that label's radius in the entire
graph. Equal radii designate different labels.

This gives a negative answer to Mortada, El Zein and Al Hajjar,
[arXiv:2608.02566v1, Section 6, Problem 1](https://arxiv.org/html/2608.02566v1#S6).
Their excluded graph H has 12 vertices; every graph in this family has at
least 36. It does not refute their (1,1,3,3,3) theorem or settle the separate
(1,1,2,3) problem.

The proof is self-contained in [paper/main.tex](paper/main.tex) and
[paper/main.pdf](paper/main.pdf). It derives a necessary private-neighbor
condition from arbitrary existing high-color representatives, and then an
odd-cycle contradiction. It needs no global coloring enumeration. Diamond
rings and triangle expansion are established constructions, appropriately
cited; no historical firstness or minimum counterexample order is asserted.

## Verification and entry points

| Material | Scope |
| --- | --- |
| [Paper](paper/main.pdf) and [BibTeX](paper/references.bib) | Full written odd-k proof, definitions, original problem, limitations and AI disclosure |
| [Lean source](supplement/frozen/ClawFree11334.lean) | Fixed k=3 graph, actual Mathlib graph/walk/distance semantics, all Fin36-to-Fin5 colorings; not the whole family or diamond-freeness |
| [Fixed JSON](supplement/frozen/counterexample.json) | Exact adjacency, incidences, core and palette |
| [Bounded checker](supplement/check_structural.py) | Definition-first BFS checks, damaged-input and positive controls; not proof by samples |
| [Independent mathematics review](review/INDEPENDENT_MATHEMATICS.md) | Separate AI reconstruction and independently written small checks |
| [Final manuscript review](review/FINAL_MANUSCRIPT_REVIEW.md) | Exact-version manuscript and reference review |
| [Reproduction](REPRODUCE.md) | Commands and explicit current/historical evidence boundary |
| [Originality review](ORIGINALITY_REVIEW.md) | Checked primary sources, classical constructions and remaining uncertainty |
| [Readiness report](PUBLICATION_READINESS.md) | Mathematical value, publication risks and human decisions |

Current execution records are in `verification/`. The new serial Lean
compilation passed 18 standard-only axiom audits. Final LaTeX was actually
exported twice and all seven pages were visually inspected. Source provenance
is bound to Git commit `61488e05c9fe41984f483853f99e79f5715dc893` in
`source-bindings.json`; the manuscript itself is a new private file, not a
public commit at that revision.

`manifest.json` and `SHA256SUMS` in the delivery archive identify all payload
bytes. Hashes are version identifiers, not proof of validity or priority.
Historical frozen files are unchanged. The original paper's PDF and rendered
figure used in local review are not redistributed in this package.

AI contributed substantially to exploration, proofs, Lean, code, searches,
independent AI review and writing. No AI author or external human peer review
is claimed. Authors, order, contributions, responsibility review, ORCID,
affiliation, correspondence, funding, conflicts and license remain pending
for this specific paper.
