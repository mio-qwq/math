# Research questions and results register

Last mathematical/source review: 9 October 2026.

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
| R004.1 | Public conjecture: classification of six-dimensional MUB triplets, Matolcsi–Matszangosz–Varga–Weiner, Conjecture 1 | Stated in the [2026 journal source](https://link.springer.com/article/10.1007/s10801-026-01506-x). Not proved here. [Subsequent source review](004-mub-triplets/LITERATURE.md) distinguishes a maximum-three proof claim from actual triplet classification |
| R004.2 | Public conjecture: transition-matrix character identities in the same source, Conjecture 2 | First-character vanishing has an external OpenAI exact-paper/Lean endpoint; the cubic/adjoint condition is a separate structural target. Neither endpoint nor maximum-three computation has been independently replayed here |
| R004.3 | Literal source statement: Corollary 4.7 without an orthogonality assumption | Refuted as written by the exact example below. Adding orthogonality supplies the intended usable statement; the correction does not refute the source's main conjectures |
| R004.4 | Proposed exact interface for the cubic target: a complete companion as a fixed-spectrum Hermitian observable | [Proved in writing](004-mub-triplets/spectral-companion.md), with a conditional double-anticommutation branch proving both cubic zeros from either first zero. Three supporting Lean declarations reconstruct the six spectral weights. General witness symmetry and general coupling remain unproved |
| R004.5 | Public Conjecture 3: Szollosi's two-circulant family cannot occur in a quadruplet | The journal corrects an earlier wrong proof; a September 2026 unrefereed candidate directly overlaps it. [Review](004-mub-triplets/LITERATURE.md) flags that claim without independently accepting it |
| R004.6 | Proposed stronger route: every fixed complete companion permits the extra simple-spectrum anticommutation witness | Refuted by an [exact actual MUB triplet](004-mub-triplets/fixed-companion-witness.md). The same H has another companion that permits it; this is not a counterexample to general cubic coupling or to existential choice over all companions |
| R004.7 | Proposed exact scope question for the extra anticommutation route | [Proved in writing](004-mub-triplets/four-circulant-route.md): witness existence iff fixed-partition four-circulantization iff a sixteen-pair phase test. The companion construction is classical Zauner theory, not a new MUB construction. Requiring this witness at every fixed partition is refuted by R004.9; selection of other partitions and the published cubic condition remain unproved |
| R004.9 | Proposed stronger proof route: both cubic characters vanish at every prescribed balanced partition of an actual MUB triplet | Refuted by a [closed concrete Lean matrix triplet](004-mub-triplets/fourier-character-asymmetry.md): cubic values 0 and (243-351i)/125, latter norm square 1458/125. The original conjectured product stays zero. Classical Fourier construction; historical numerical originality not established; fixed-partition witness consequence is written only |
| C7 | Public problem: determine the Shannon capacity of the seven-cycle; source-stated two-sided heterogeneous construction question | [Candidate review](OPEN_PROBLEM_CANDIDATES.md) cites Tandon's August 2026 theorem and remaining extension. A small neutral-core branch is sharp at eight words but its pure self-product roots decrease; no new capacity bound or general two-sided construction |
| K5 | Public problem: determine the five-dimensional kissing number | The 2026 Cohn–Rajagopal source records 40<=tau_5<=44. The continuous 41-point Gram feasibility problem is a candidate, not a finite-grid test or an exclusion proved here |
| SIC | Public problem: SIC existence, with the remaining Galois/Hermitian compatibility in a specific ghost construction | September 2026 sources prove twisted convolution and algebraicity but explicitly leave the needed automorphism unknown. [Candidate review](OPEN_PROBLEM_CANDIDATES.md) records that narrower gap without reproposing the already proved steps |

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

## R003.4: actual structural interfaces

The [selected structural replay](003-arc-one-parameter/structural-bridge-replay.md)
now closes the bundled core-dual algebra equivalence and actual Jacobson
radical identification. Every commutative characteristic-two coefficient
ring receives the radical preimage formula; the eighteen-coordinate
kernel description retains semisimple coefficients. Eight actual source
replays and 77 fresh standard-axiom audits support this implementation.
The underlying trivial extension and field radical statement are prior
OpenAI mathematics. These are verified formalization interfaces with
the stated coefficient scope, not a public conjecture resolution.
The derived triangle, full twenty-dimensional self-Ext and complete ARC
remain open implementation tasks; literature-wide originality is not asserted.

## R004.8: direct first character in the displayed symmetry branch

The [direct four-circulant theorem](004-mub-triplets/direct-circulant-character.md)
proves pa pe+pb pc=0 for every displayed four-circulant raw Hadamard6,
without a genericity assumption. Both fixed-partition first and cubic
characters follow. All phase-retrieval cases, repeated ratios and zero
Fourier modes are covered by the written proof. Six Lean audits support
the actual matrix and adjoint character formulas and cubic consequences
given cancellation; the Gram-to-cancellation proof is not yet formalized.
The [scalar zero-mode interface](004-mub-triplets/zero-mode-obstruction.md)
now connects to [actual Gram bounds and block inverses](004-mub-triplets/gram-block-invertibility.md).
Actual six-by-six Gram multiplication derives all four mode bounds; actual
flatness excludes every zero mode, and actual determinant factorization
constructs four block inverses with eight equations. Five plus three new
audits close this supporting gap without assuming a mode bound or inverse.
Three additional [opposite-power audits](004-mub-triplets/mode-power-matching.md)
now derive the actual a/e and b/c equal-power premise from the same Gram
equation, without flatness, block inverses or a second Gram assumption.
Six further [correlation/multiset audits](004-mub-triplets/ratio-multiset-retrieval.md)
now derive actual opposite cyclic correlations and actual flat-Gram ratio
multisets, with all root multiplicities preserved. Three further
[actual reconstruction audits](004-mub-triplets/phase-retrieval-alternatives.md)
now derive both opposite-block cyclic-shift/adjoint alternatives, including
repeated ratios. One further
[connected adjoint-branch audit](004-mub-triplets/adjoint-branch-cancellation.md)
now proves product cancellation with either genuine adjoint alternative as
an explicit extra premise. Four further
[actual spectral/real-rank audits](004-mub-triplets/real-mode-product-squares.md)
now prove the equal product squares of two actual flat triples with nonzero
real-ratio modes. The [final three audited endpoints](004-mub-triplets/flat-gram-cancellation.md)
now supply those hypotheses by actual phase/shift normalization and exhaust
the retrieval alternatives. Actual flat Gram alone gives product cancellation
and first/cubic character vanishing for H and its actual adjoint at the
displayed partitions.
These are classical supporting ingredients,
not a new independently solved public conjecture.
This closes a project-local branch gap, not the source-stated general
MUB conjecture. Historical originality is not established.

## R004.1–R004.2: source-stated MUB questions

The fixed source is Matolcsi, Matszangosz, Varga and Weiner,
[*Triplets of Mutually Unbiased Bases*, arXiv:2503.14752v2](https://arxiv.org/html/2503.14752v2),
19 July 2025. Conjecture 1 concerns classification up to
permutational unitary equivalence, rather than just the maximum
number of bases. The [journal paper](https://link.springer.com/article/10.1007/s10801-026-01506-x),
published 4 March 2026, also states these structural conjectures.

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

The [current literature review](004-mub-triplets/LITERATURE.md)
separates OpenAI's computational maximum-three claim from its exact
Fourier/Lean first-character result and upper bound five. The actual
solution module exists; a `sorry` in a challenge template is not that
implementation. These source endpoints were read, without independently
compiling the external dependency graph or replaying the full exclusion.
Maximum-number and individual-Hadamard claims alone do not supply the
cubic/adjoint identity.

The [spectral criterion](004-mub-triplets/spectral-companion.md)
reconstructs the complete third basis, with all six orthogonal columns,
from one simple-spectrum Hermitian observable and two sets of diagonal
moments. With an additional simultaneous anticommutation witness at the
fixed three-versus-three partitions, and either first-character zero,
it proves both cubic zeros. The anticommutation condition has not been
shown to follow from arbitrary complete companionship. The supporting
Lean proof treats only six scalar spectral weights; the full matrix
criterion and conditional branch remain written mathematics.

The [fixed-companion matching theorem](004-mub-triplets/fixed-companion-witness.md)
now completely decides the additional symmetry for a specified third
basis. The two coordinate involutions must be monomial with the same
three paired columns. Their product being diagonal with simple spectrum
is sufficient; repeated spectrum can conceal dense mixing. A complete
triplet demonstrates that failure with defect four, but an alternative
companion of the same H succeeds. Thus this result does not close the
existential companion-selection question or disprove the cubic target.

The [matrix-support Lean source](004-mub-triplets/proof/SpectralMatchingSupport.lean)
now proves actual anticommutation with the fixed diagonal spectrum iff
off-matching entries vanish. This is a real matrix-multiplication
interface, with three separate audited declarations; it does not prove
unitary monomial phases, the complete companion conjugation bridge or
the full fixed-companion criterion.

The [unitary phase Lean theorem](004-mub-triplets/proof/SpectralMatchingUnitary.lean)
now derives unit norms from actual Gram multiplication and describes the
entire fixed-pairing Hermitian unitary family, with a complete converse.
It has three additional independent audits; the companion conjugation and
shared-pairing selection remain separate gaps.

The [exact symmetry route](004-mub-triplets/four-circulant-route.md) closes
the converse of the earlier written branch at the fixed partitions.
Its classical construction covers all zero modes. The sixteen-pair phase
test identifies precisely the known four-circulant symmetry requirement;
it does not establish that requirement for every eligible H or close
the general cubic/adjoint target.

The broader candidate problems C7, K5 and SIC are specified with
current primary-source bounds and remaining gaps in
[OPEN_PROBLEM_CANDIDATES.md](OPEN_PROBLEM_CANDIDATES.md).
None is represented as a solved conjecture or a newly established bound.

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
