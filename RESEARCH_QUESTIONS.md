# Research questions and results register

Last mathematical/source review: 8 October 2026.

This register separates the origin of a statement from its proof
status. A theorem written in an outside manuscript is a prior claim;
it is not automatically a theorem verified here. A conjecture
explicitly stated in a source is different from a question proposed
during this research. Neither an unsuccessful search nor a Lean
implementation gap establishes that a mathematical problem is
globally open. Historical originality remains unresolved unless a
specific comparison establishes otherwise.

## Current map

| ID | Origin and statement | Status and evidence |
| --- | --- | --- |
| R001.1 | Existing research: for m>=2, exhaust all order-2m Hadamard matrices whose entrywise powers 1 through m-1 are Hadamard | Proved in writing: [exact patterns and phase circles](001-odd-half-order-hadamard/general-patterns.md); [labelled graph](001-odd-half-order-hadamard/phase-geometry.md) and [standard-equivalence quotient](001-odd-half-order-hadamard/equivalence-quotient.md). Full Lean and exhaustive original-literature comparison remain incomplete |
| R001.2 | Proposed realization question: which even m>2 admit a cyclic GH(m,2) seed with a compatible balanced rectangle? | Unresolved here. The phase-circle construction is proved conditional on that seed; it is not an existence theorem at every order |
| R002.1 | Existing research: independent nonnegative costs satisfying xy<=hz only at actual conflicts | Proved in writing when either coordinate relation is [chordal bipartite](002-weighted-rectangular-pruning/chordal-bipartite-costs.md), the other arbitrary. Includes partial families and sharp coefficient one; full Lean remains incomplete |
| R002.2 | Proposed extension: does the same coefficient-one bound hold for arbitrary pairs of finite relations? | Unresolved here. This is our precise extension question, without a claim that no equivalent theorem exists in the literature |
| R002.3 | Proposed first obstruction/test: both coordinate relations are induced six-cycles | [Proved for simultaneously translation-invariant independent costs](002-weighted-rectangular-pruning/cyclic-six-costs.md); [Lean](002-weighted-rectangular-pruning/proof/mathlib/README.md) now proves the full-input actual cover/pruning bound and sharp cover coefficient. Exact optimum, invariant partial inputs and the non-dominated infinite family remain written results. Arbitrary asymmetric costs remain unresolved here |
| R002.4 | Proposed convexification of product costs by adding two positive product systems | Refuted: [the exact single-conflict obstruction](002-weighted-rectangular-pruning/boundary.md) also proves that no finite uniform coefficient repairs this extension. These summed costs need not satisfy R002.1's local condition |
| R002.5 | Literature question: can the local-conflict theorem be derived from a known four-functions, mincut or correlation inequality? | Under comparison. The universal all-pair premise of Ahlswede–Blinovsky's function-space theorem is stronger than the direct local-conflict substitution; a deeper equivalence remains possible |
| R003.1 | Prior lower-algebra resolutions and Ext calculations | Actual Lean implementations are complete within their stated assumptions; [attribution](003-arc-one-parameter/ATTRIBUTION.md) identifies OpenAI and Tang's prior mathematical conclusions. These are formalization contributions |
| R003.2 | Existing research: full Tate algebra of the actual finite triangular module at every twist-ratio order | Proved in writing: [finite resonant algebra](003-arc-one-parameter/finite-resonant-tate-algebra.md) and [equal-twist seam](003-arc-one-parameter/order-one-tate-algebra.md). Its complete Lean construction is unfinished |
| R003.3 | Proposed continuation: ordinary endomorphism ring of that same finite module, including maps through projectives | Unresolved here. The proved degree-zero Tate ring is the stable quotient and does not determine the ordinary ring |
| R004.1 | Public conjecture: classification of six-dimensional MUB triplets, Matolcsi–Matszangosz–Varga–Weiner, Conjecture 1 | Explicitly conjectured in the [fixed v2 source](https://arxiv.org/html/2503.14752v2). Not proved here; its subsequent global resolution status is not certified |
| R004.2 | Public conjecture: transition-matrix character identities in the same source, Conjecture 2 | Explicitly conjectured in the fixed source. Exact hypotheses below; numerical agreement or absence of four MUBs alone does not prove these identities |
| R004.3 | Literal source statement: Corollary 4.7 without an orthogonality assumption | Refuted as written by the exact example below. Adding orthogonality supplies the intended usable statement; the correction does not refute the source's main conjectures |

## R001.2: a concrete existence problem

A cyclic GH(m,2) root seed is a 2m-by-2m matrix over the mth
roots of unity for which every ratio of two distinct rows contains
each root twice. A compatible rectangle has m selected rows and
m selected columns, and every cross-group row ratio restricted to
the selected columns contains each root once.

At m=2 a compatible seed gives the classical order-four phase family.
The [exhaustion theorem](001-odd-half-order-hadamard/general-patterns.md)
shows that every nonroot solution arises from such a rectangle,
and odd m is excluded. For even m>2 the existence problem
remains separate. The smallest useful advance is an explicit
seed/rectangle at a new order, or an impossibility proof under
these exact assumptions. It must not be confused with questions
that require a shorter range of entrywise powers.

The comparison with Craigen and Woodford's *Power Hadamard matrices*
is still incomplete. Classical switching and affine Hadamard
families are prior methods; they are not claimed as discoveries here.

## R002.2–R002.5: the boundary beyond chordal relations

Use the actual graph and independent cost definitions in the
[chordal theorem](002-weighted-rectangular-pruning/chordal-bipartite-costs.md).
The unrestricted question asks whether its two bounds and initial
retention remain true for all finite E,F under the same local
inequalities, with no structural hypothesis.

For the first induced-cycle test, take
\[
P=I=S=J=\mathbb Z/3\mathbb Z,\qquad
E=F=\{(t,t),(t,t+1):t\in\mathbb Z/3\mathbb Z\}.
\]
Both coordinate graphs are six-cycles. With full originals there
are nine R, nine C, nine H and nine Z corners, and 36 original
conflicts. A proof must handle all independent nonnegative
costs; a counterexample must provide exact costs, every local
constraint, and an actual augmented-cover lower bound.
A bounded numerical search would only be evidence for its
tested inputs.

The [invariant six-cycle theorem](002-weighted-rectangular-pruning/cyclic-six-costs.md)
now proves the sharp bound for costs depending on coordinate differences,
and for partial inputs that are unions of simultaneous-translation
orbits. It gives an exact nine-expression augmented optimum for full
invariant inputs and an infinite positive family with no common
coordinate-product domination. Arbitrary partial patterns need not
preserve the symmetry, and neither they nor general asymmetric
costs are covered by that theorem.

The full-input bound now has Lean proofs from all actual local
constraints through actual covers and actual uncovered-corner pruning,
including the unit-cost cover sharpness witness. The written exact optimum
and invariant partial-input extension are not formalized by those files.

The current preservation lemma normalizes attached pivots using
nested old neighborhoods. In a six-cycle the two neighbors of
each right coordinate are incomparable, so that normalization
cannot be assumed. A useful next theorem would replace this
step by a valid coupled decision, or identify an exact obstruction.

The prior correlation comparison includes Ahlswede and Blinovsky,
[*Correlation inequalities in function spaces*](https://www.math.uni-bielefeld.de/ahlswede/homepage/public/197.pdf),
LNCS 4123, pp. 572–577 (2006). Its all-pair function inequality
and all-Borel-set measure compatibility are not automatically
implied by local conditions on graph conflicts. This is a
hypothesis comparison, not an originality verdict or a proof
that no other reduction exists.

## R003.3: ordinary versus stable endomorphisms

Keep the same field, parameters, finite algebra, kernel bimodule
and triangular module fixed in the [finite construction](003-arc-one-parameter/finite-resonant-realization.md).
The desired ordinary ring is \(\operatorname{End}_\Lambda(Z)\),
together with its ideal of maps factoring through projectives
and the quotient map to the already calculated stable ring.

The smallest useful step is an explicit description of a module
endomorphism in the chosen triangular coordinates and its
composition, before claiming an all-parameter ring formula.
A Lean proof of an existing Ext calculation addresses a different
question; a cochain quotient with the same dimensions does not
by itself identify this ordinary ring.

For prior conclusions and the characteristic assumptions see
[the attribution table](003-arc-one-parameter/ATTRIBUTION.md).
No claim that the general Auslander–Reiten conjecture remains
globally unresolved is made by this implementation boundary.

## R004.1–R004.2: source-stated MUB questions

The primary source is Matolcsi, Matszangosz, Varga and Weiner,
[*Triplets of Mutually Unbiased Bases*, arXiv:2503.14752v2](https://arxiv.org/html/2503.14752v2),
19 July 2025. Conjecture 1 concerns classification up to
permutational unitary equivalence, rather than just the maximum
number of bases.

For an actual MUB triplet define transition Hadamard matrices
\(H_1=\sqrt6 X_1^*X_2,\ H_2=\sqrt6 X_2^*X_3,\
H_3=\sqrt6 X_3^*X_1\).
For a matrix H with columns h_k let
\(g_H(\gamma)=\sum_k\prod_i(h_k)_i^{\gamma_i}\) and
\(G_H(\gamma)=|g_H(\gamma)|^2\).
Writing \(\alpha=(1,1,1,-1,-1,-1)\), Conjecture 2 asks, for
every permutation pi and every transition H,
\[
G_H(\pi\alpha)=0,\qquad
G_H(3\pi\alpha)G_{H^*}(3\pi\alpha)=0.
\]
These are character identities on actual triplets. A proof excluding
four mutually unbiased bases would not automatically classify
triplets or establish the identities.

The initial tractable question is the exact consequence of
independent row and column relabelling for the coupled identity.
A same-label zero-product condition on one fixed matrix must
not be silently strengthened to all cross-label products.
Literature resolution and the mathematical reduction are
separate checks.

## R004.3: exact missing-hypothesis check

In the fixed v2 source, Corollary 4.7 assumes only unimodularity
and opposite three-versus-three multiplicative characters.
Take
\[
a=(1,1,1,1,1,1),\qquad b=(-1,1,1,1,1,1).
\]
For any three-element I the two characters are 1 and -1,
but the six ratios a_i/b_i sum to 4. There is only one
negative ratio and five positive ratios, so they cannot be
partitioned into three cancelling pairs across I and its complement.
This refutes that literal statement.

The proof in the source uses Proposition 4.6, which additionally
requires the ratios to sum to zero. For distinct columns of a
Hadamard matrix this orthogonality is automatic. Adding it
repairs the invocation in that intended setting; this example
does not refute the main MUB conjectures or their Hadamard-column
applications.

## Evidence status

Written mathematical proofs, exact finite checks and Lean theorems
are separate forms of evidence. The detailed boundaries and actual
compiler receipts are in [FORMALIZATION.md](FORMALIZATION.md).
The questions above have explicit identifiers so later proofs,
counterexamples and literature corrections can update their status
without erasing earlier results or representing unverified work as
a solved problem.
