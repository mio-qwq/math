# Mathematical research notes and verification artifacts

This repository records explicit mathematical statements, complete proofs where available, and reproducible exact checks. The status of each result is stated separately from its computational or formal verification status. No claim of historical priority is made.

## Results

| Note | Mathematical scope | Verification scope |
| --- | --- | --- |
| [001 — Power Hadamard rigidity and classification](001-odd-half-order-hadamard/README.md) | Odd-half-order rigidity, exhaustive all-half-order phase classification, and finite graph models before and after standard matrix equivalence | Complete written proofs, exact examples and Lean support/block obstructions; the full matrix classification and quotient topology are not yet formalized |
| [002 — Weighted rectangular pruning](002-weighted-rectangular-pruning/README.md) | Product-weighted bounds for arbitrary relations, sharp independent local-cost bounds when either relation is chordal bipartite, and a simultaneous-translation-invariant theorem with exact weighted optimum on two induced six-cycles; no finite uniform coefficient works for sums of two positive product systems | Lean proves the full invariant six-cycle actual cover/pruning bound and sharp cover coefficient, alongside single-conflict criteria and the unbounded obstruction. The chordal theorem, invariant partial-input extension and exact nine-expression optimum remain written results |
| [003 — ARC core certificate and extension spectra](003-arc-one-parameter/README.md) | Finite polynomial identities, an abstract spectrum theorem, and a written finite triangular construction with its full Tate algebra for every twist-ratio order, including the equal-twist seam; the construction is not a complete Lean certificate | Lean constructs the actual algebra, perfect trace, specified all-degree projective resolution and nonzero actual f-character Ext³ when q³ is nonzero, with full inverse-twist chain comparison and canonical Ext transport in every degree. General exact-functor/extMk naturality identifies the mapped-resolution class with its canonical image; the canonical action on the fixed Ext³ class has inverse-unit weight. Transport preserves all graded Yoneda compositions and the identity, and the actual m-fold class in Ext^(3m) has weight H^(-m), with its actual second power now proved nonzero when q^4 is nonzero, while powers at least three remain open in Lean. The actual f-character module is neither projective nor injective when q³ is nonzero. Over characteristic-two fields the algebra is self-injective and every positive Ext(M,A) vanishes. The full self-Ext profile, tensor-square realization and complete ARC remain open in Lean |

## Reproduction

See [FORMALIZATION.md](FORMALIZATION.md) for the exact Lean statements, commands, and remaining boundaries.

The [research questions and results register](RESEARCH_QUESTIONS.md)
distinguishes prior theorems, source-stated conjectures, proposed
extensions, proved or refuted statements, and remaining formalization
gaps. Literature status and proof status are recorded separately.

Each note has its own README and fixed inputs. Python checkers use exact arithmetic and the standard library. Lean is pinned by `lean-toolchain` to `leanprover/lean4:v4.34.1`. Most certificates use its bundled `Std` library; each additional `proof/mathlib` package pins Mathlib and its dependencies.

For example, from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
```

## Provenance and limitations

The starting point is [OpenAI's public mathematical collection](https://github.com/openai/math), snapshot `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Each note identifies the exact source and distinguishes the prior statement from the extension or checking work recorded here. Reading a source, running finite examples, and checking a portion in Lean do not amount to verification of all its surrounding claims.

Literature review and external mathematical review remain open. Correctness and precise disclosure of verification scope take precedence over claims of novelty.

For 003, a [conditional resonant multiplication theorem](003-arc-one-parameter/resonant-yoneda-algebra.md)
now goes beyond the dimension spectrum: the positive Yoneda algebra,
with only its scalar degree-zero identity adjoined, is a Veronese
algebra plus its shifted positive ideal with square-zero multiplication.
The proof retains explicit polynomial and bimodule action hypotheses.
It is written mathematics with independent proof reviews. A separate
[finite construction proof](003-arc-one-parameter/finite-resonant-realization.md)
now establishes those multiplicative hypotheses over characteristic-two
fields with an infinite-order base parameter, using a fixed finite
target, actual side-projective kernel and both natural branch actions.
For example, F_4(t) supplies ratio order three and first self-extensions
in degrees nine and ten. This reconstruction is written mathematics;
the full construction in Lean and the entire ordinary degree-zero ring
remain separate. The [full Tate calculation](003-arc-one-parameter/finite-resonant-tate-algebra.md)
now treats the same actual module for ratio order d>1. It determines
the negative contraction module, all mixed products, stable degree
zero and the exceptional degree-minus-one square-zero class.
The [order-one proof](003-arc-one-parameter/order-one-tate-algebra.md)
now closes its secondary products using explicit bottom lifts and
associativity. Stable degree zero is the dual numbers for equal
twists, and k otherwise. The finite-order formula now covers every
possible order; infinite ratio gives k plus the square-zero
degree-minus-one omega line.

For 003, the constructed all-degree suffix lift now gives a closed actual
degree-six cup Hom. An explicit six-letter witness proves that its
specified Ext^6 class is nonzero when q^4 is nonzero, including every
nonzero q over a characteristic-two field. The constructed whole shifted
comparison now identifies it with the actual Yoneda square of the fixed
third Ext class and its defined second power. Powers at least three,
the complete self-Ext profile and ARC realization are still open in Lean.

For 002, a [compatible pair-cost theorem](002-weighted-rectangular-pruning/compatible-pair-costs.md)
now gives a finite-threshold cover and pruning construction beyond
product costs when either relation is a disjoint union of complete
bipartite blocks. Its general proof is written analytically; the exact
certificate implementation has separate checks and is not a Lean proof.

Two [reflexive local-cost families](002-weighted-rectangular-pruning/reflexive-cost-families.md)
also have explicit cover and pruning constructions when both relations
may be nonblock. They treat proportional complete-grid costs and a
nonproportional exchange family on two paths. Their parameter-wide proofs
are written, with separate exact fixture checks.

The [binary-coordinate theorem](002-weighted-rectangular-pruning/double-path-independent-costs.md)
now removes every restriction on the independent cost tables for two
four-vertex paths, apart from the nine local inequalities. Its fifteen
candidate deletions compute the exact augmented optimum. Together with
the block theorem and zero-cost padding, it settles all relations and
partial original families on coordinate sets of size at most two.
The proof is analytic and includes zero costs; arbitrary larger
coordinate systems and the full Lean proof remain open.

The [expanded-four-path theorem](002-weighted-rectangular-pruning/binary-one-side-costs.md)
further permits arbitrarily large coordinates: one relation can be
a union of complete blocks and complete four-path expansions, with
the other entirely arbitrary. In particular only one coordinate
relation needs binary sides. The construction controls the actual
uncovered corners through a high-row threshold coupling and an
effective-cost residual block, handles zero costs directly, and lifts
through exact whole-group aggregation and partial-family restriction.
This written theorem remains separate from the general arbitrary
relation problem and its Lean formalization.

The subsequent [nested-component theorem](002-weighted-rectangular-pruning/nested-relation-costs.md)
extends the independent local-cost construction to any finite number
of nested neighborhood layers in every component of one relation,
with the other arbitrary. Its suffix induction preserves residual
local inequalities and lifts pooled zero-cost decisions to actual
conflict-free survivors. Complete expansions, components and partial
families are included. This sharp written theorem has a finite rational
construction; unrestricted relations, its full Lean implementation
and the original-literature comparison remain separate questions.

The [right-leaf extension](002-weighted-rectangular-pruning/right-leaf-extension-costs.md)
preserves this local-cost property when new right coordinates each
have one left neighbor. It also permits complete group expansions,
and reaches some relations with incomparable neighborhoods, including
the five-vertex path oriented with two left and three right coordinates,
against any other relation. The two-neighborhood corollary even permits
any relation with at most two distinct left neighborhoods per component:
only \(|P|\le2\), with I arbitrary, or \(|S|\le2\), with J arbitrary,
is needed. Its genuinely partial residual problem
controls actual shared and missing corner profits. This is a written
structural theorem; the opposite path orientation, general forests
and a full Lean implementation remain outside its proved scope.

The later [bipartite-forest theorem](002-weighted-rectangular-pruning/forest-pendant-star-costs.md)
settles those path and forest cases in written mathematics.
One relation may be any finite bipartite forest or complete forest
expansion, and the other arbitrary. A pendant-star preservation
lemma transfers auxiliary-left costs and H charges to a compatible
partial pivot problem; a rooted construction builds every tree.
Zero costs, partial originals, actual uncovered gains and the
sharp coefficient one are included. The complete Lean proof,
general cyclic relations and historical novelty remain open here.

The subsequent [chordal-bipartite theorem](002-weighted-rectangular-pruning/chordal-bipartite-costs.md)
extends the same sharp bounds to either relation having no induced
cycle of length at least six. The other relation is arbitrary;
four-cycles, partial families and zero costs are included.
A multiple-pivot preservation lemma uses nested old neighborhoods
only on the attached pivots. The classical beta-leaf elimination
theorem is cited from a primary proof, with an explicit incidence
translation. This is a written construction with independent
source readings, separate from the full Lean and unrestricted
relation problems.

For 001, the [exact all-half-order classification](001-odd-half-order-hadamard/general-patterns.md)
now eliminates the binary pattern and constructs every nonroot solution
from a compatible rectangle of a cyclic root seed and one unit phase.
Its [labelled dephased solution space](001-odd-half-order-hadamard/phase-geometry.md)
is a finite graph with smooth nonroot arcs and explicit root branch counts.
Both the classification and this geometric consequence have complete
written proofs; their complete Lean bridges remain separate.
The actual polynomial product obstruction is independently checked in Lean.

The [standard-equivalence quotient](001-odd-half-order-hadamard/equivalence-quotient.md)
now determines the corresponding moduli graph. The actual dephased
permutation formula forces a finite dihedral action on each circle;
reflection fixed points locate possible new endpoints, and root
valencies are stabilizer orbits of half-branches. This written proof
closes the quotient-geometry gap while preserving the separate
even-order realization and original-literature comparison questions.

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
split coordinates, unit and multiplication formula. The subsequent
[specified lower-algebra resolution](003-arc-one-parameter/proof/mathlib/LowerAlgebraCategoricalResolution.README.md)
constructs actual projective corner terms, all-degree exactness and an
augmentation quasi-isomorphism. Over characteristic-two fields with every
1+q^m nonzero for positive m, every positive actual self-Ext of the lower
f-character vanishes. This does not require q itself to be nonzero.
The subsequent
[actual regular-target Ext calculation](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularExt.README.md)
and [right-character action](003-arc-one-parameter/proof/mathlib/LowerAlgebraRegularRightAction.README.md)
now give the complete lower regular-target profile when also q is
nonzero: only degree two survives, with an actual K-linear equivalence
from K and the right f-character action. The
[provenance table](003-arc-one-parameter/ATTRIBUTION.md)
identifies the prior OpenAI and Tang mathematical conclusions separately
from these actual Lean implementations. The derived triangle and full
twenty-dimensional self-Ext profile remain open.
