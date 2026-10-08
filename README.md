# Mathematical research notes and verification artifacts

This repository records explicit mathematical statements, complete proofs where available, and reproducible exact checks. The status of each result is stated separately from its computational or formal verification status. No claim of historical priority is made.

## Results

| Note | Mathematical scope | Verification scope |
| --- | --- | --- |
| [001 — Odd half-order Hadamard rigidity](001-odd-half-order-hadamard/README.md) | General theorem for every odd half-order; complete written proof | Exact examples and Lean proofs of support and actual complex block obstructions; the full rigidity theorem is not yet formalized |
| [002 — Product-weighted rectangular pruning](002-weighted-rectangular-pruning/README.md) | Product-weighted cover/pruning theorems with sharp constant; no finite uniform coefficient works for sums of two positive product systems | Independent rational checker, 67,132 exact instances, and Lean proofs of real-cost single-conflict criteria and the unbounded obstruction |
| [003 — ARC core certificate and extension spectra](003-arc-one-parameter/README.md) | Finite polynomial identities and an abstract spectrum theorem under explicit hypotheses; the one-variable ARC application remains conditional | Lean constructs the actual algebra, perfect trace, specified all-degree projective resolution and nonzero actual f-character Ext³ when q³ is nonzero, with full inverse-twist chain comparison and canonical Ext transport in every degree. General exact-functor/extMk naturality identifies the mapped-resolution class with its canonical image; the canonical action on the fixed Ext³ class has inverse-unit weight. Transport preserves all graded Yoneda compositions and the identity, and the actual m-fold class in Ext^(3m) has weight H^(-m), with its actual second power now proved nonzero when q^4 is nonzero, while powers at least three remain open. The actual f-character module is neither projective nor injective when q³ is nonzero. Over characteristic-two fields the algebra is self-injective and every positive Ext(M,A) vanishes. The full self-Ext profile, tensor-square realization and complete ARC remain open |

## Reproduction

See [FORMALIZATION.md](FORMALIZATION.md) for the exact Lean statements, commands, and remaining boundaries.

Each note has its own README and fixed inputs. Python checkers use exact arithmetic and the standard library. Lean is pinned by `lean-toolchain` to `leanprover/lean4:v4.34.1`. Most certificates use its bundled `Std` library; each additional `proof/mathlib` package pins Mathlib and its dependencies.

For example, from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
```

## Provenance and limitations

The starting point is [OpenAI's public mathematical collection](https://github.com/openai/math), snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Each note identifies the exact source and distinguishes the prior statement from the extension or checking work recorded here. Reading a source, running finite examples, and checking a portion in Lean do not amount to verification of all its surrounding claims.

Literature review and external mathematical review remain open. Correctness and precise disclosure of verification scope take precedence over claims of novelty.

For 003, the constructed all-degree suffix lift now gives a closed actual
degree-six cup Hom. An explicit six-letter witness proves that its
specified Ext^6 class is nonzero when q^4 is nonzero, including every
nonzero q over a characteristic-two field. The constructed whole shifted
comparison now identifies it with the actual Yoneda square of the fixed
third Ext class and its defined second power. Powers at least three,
the complete self-Ext profile and ARC realization are still open.

For 002, a [compatible pair-cost theorem](002-weighted-rectangular-pruning/compatible-pair-costs.md)
now gives a finite-threshold cover and pruning construction beyond
product costs when either relation is a disjoint union of complete
bipartite blocks. Its general proof is written analytically; the exact
certificate implementation has separate checks and is not a Lean proof.

Two [reflexive local-cost families](002-weighted-rectangular-pruning/reflexive-cost-families.md)
also have explicit cover and pruning constructions when both relations
may be nonblock. They treat proportional complete-grid costs and a
nonproportional exchange family on two paths. Their parameter-wide proofs
are written, with separate exact fixture checks; arbitrary independent
costs remain open.

For 001, the [exact all-half-order classification](001-odd-half-order-hadamard/general-patterns.md)
now eliminates the binary pattern and constructs every nonroot solution
from a compatible rectangle of a cyclic root seed and one unit phase.
Its [labelled dephased solution space](001-odd-half-order-hadamard/phase-geometry.md)
is a finite graph with smooth nonroot arcs and explicit root branch counts.
Both the classification and this geometric consequence have complete
written proofs; their complete Lean bridges remain separate.
The actual polynomial product obstruction is independently checked in Lean.

Licensed under Apache-2.0; see [LICENSE](LICENSE) and the attribution in each note.

The [actual square-zero splitting](003-arc-one-parameter/proof/mathlib/TwentyDimDualScaleEndomorphism.README.md)
also constructs every scalar dual-scaling endomorphism, including the zero
projection onto the lower subalgebra. Its actual two-sided kernel has
square-zero multiplication, and the algebra splits as the corresponding
R-modules. The dual-bimodule identification and full homological profile
are separate in that source. The subsequent
[explicit dual extension construction](003-arc-one-parameter/proof/mathlib/TwentyDimTrivialExtension.README.md)
identifies the actual kernel with the lower algebra's dual, intertwines
both lower multiplication actions, and gives the full algebra's explicit
split coordinates, unit and multiplication formula. The lower minimal
resolutions, derived triangle and full homological profile remain open.
