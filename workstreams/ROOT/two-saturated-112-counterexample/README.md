# A seven-vertex counterexample to a published packing-coloring conjecture

We give a finite simple connected 2-saturated subcubic graph with no
(1,1,2)-packing coloring. This refutes **Conjecture 3 as printed** in
Ayman El Zein and Maidoun Mortada, [arXiv:2603.25113v1, Section 5](https://arxiv.org/html/2603.25113v1#S5).
The assertion there imposes no local-girth restriction. The paper's
separate Theorem 3 has an additional local-girth condition and is unaffected.

The graph is K4 with the three edges incident to one vertex subdivided
once. It has seven vertices and nine edges. A triangle forces the
radius-two color; every vertex lies within distance two of that triangle
vertex; deleting it leaves a five-cycle that cannot use the two remaining
colors. [PROOF.md](PROOF.md) gives the full argument and exact definitions.
This familiar pyramid shape is not claimed to be a new graph construction.

The Lean theorem `TwoSaturated112.original_counterexample` proves the
actual graph's subcubic and 2-saturated properties, connectedness, and
nonexistence of **any** function `Fin 7 -> Fin 3` satisfying the packing
conditions. It uses Mathlib's `SimpleGraph`, degrees, neighbor sets,
walks, and original-graph `edist`; repeated radius one means two distinct
colors. It does not assume an UNSAT table or compute distances after deleting
a color class.

The actual compilation ran 2026-10-10 07:34:11–07:34:26 UTC under Lean
4.34.1 and Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. It exited zero
with no warnings, errors, or panics. All 14 printed declarations use only
subsets of `propext`, `Classical.choice`, `Quot.sound`; there is no
`sorryAx`, custom axiom, `native_decide`, or admitted theorem.
The published source is byte-identical to the actual compiled source;
publication did not manufacture a second compilation. Receipts are
[lean-audit.json](lean-audit.json) and [lean-audit.log](lean-audit.log).

An agent uninvolved in discovery and implementation independently rebuilt
the graph and contradiction from the original definitions, ran a separate
seven-vertex check, then reviewed the complete Lean source and actual log.
See [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md). This is an AI-assisted
research review, not human peer review.

To replay from the repository root using its pinned Mathlib environment:

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../workstreams/ROOT/two-saturated-112-counterexample/TwoSaturated112.lean
```

An additional standard-library verifier, originally frozen on worker B's
branch, reconstructs the actual adjacency, checks degrees and saturation,
computes integer BFS distances, and tests all 3^7 assignments. It also
rejects two corrupted controls. It is supplied for reproducibility; the
Lean proof and elementary argument do not depend on its output.

```sh
python workstreams/ROOT/two-saturated-112-counterexample/verify_candidate.py
```

Historical originality remains uncertain. The primary version page still
listed only v1 at the 2026-10-10 check; multi-round searches did not locate
a readable correction or same-scope solution. That is not proof of
historical firstness. Earlier packing-coloring literature and gadgets
have not been exhausted. No minimum order, full classification, optimal
palette, or resolution of the paper's other conjectures is asserted.

The discovery and initial proof were developed in worker B's research
packet; this directory adds ROOT's actual Lean formalization, integrated
publication materials, and independent scope review. AI assisted mathematical
reasoning, implementation, checking, and writing. No AI system is designated
as a paper author; human authorship and any formal submission remain separate.
