# Original statement, related work and historical limits

Checked on 9 October 2026. Mathematical correctness and historical firstness
are separate questions.

## Exact original target

Csilla Bujtás, Vesna Iršič Chenoweth, Sandi Klavžar and Gang Zhang,
*On d-distance p-packing domination number in strong products*:

- [arXiv:2510.02749v1, 3 October 2025](https://arxiv.org/html/2510.02749v1).
- [Annals of Combinatorics, published 26 March 2026](https://link.springer.com/article/10.1007/s00026-026-00814-0), DOI 10.1007/s00026-026-00814-0.

Section 1 defines packing with distinct-center distance at least p+1 and
domination with radius d. Conjecture 3.1 in both checked versions says that
nonexistence in G implies nonexistence in G strong-product H for every H.
It does not require nonexistence in both factors, cycles, regularity or
identical factors. The remaining nontrivial interval identified in Section 3
is d<p<2d, including d=2,p=3.

The constructed factors are finite, nonempty, simple, undirected and
connected. We do not attribute an explicit blanket connectedness assumption
to the conjecture where the original statement does not repeat one.
Theorem 3.3 adds a close-vertex hypothesis on H; the construction's complete
proof explains why H has no such (2,3)-close vertex.

The [README proof](README.md) and the [actual Lean endpoint](proof/Q6PackingComplexCounterexample.lean)
refute this precise original statement. Neither establishes optimality of
the 64-center witness or resolves the separate nonlinear Q6 strong-product
Q6 packing question.

## Subsequent-status and related-work checks

Multiple targeted rounds checked the original identifier, DOI, exact title,
authors, correction/revision and counterexample terms, and mechanism terms
including packing complex, compatibility graph, support unions, Steiner
nodes, hypercubes and the older (p,d)-domination notation. The current arXiv
[submission history](https://arxiv.org/abs/2510.02749) displayed only v1;
the current publisher text retained Conjecture 3.1. No verified earlier
complete resolution or statement revision subsuming this construction was
located within these searches. This is a bounded search observation, rather
than proof that no earlier result exists.

The related paper by the same authors,
[*The d-distance p-packing domination number: complexity, cycles, and trees*](https://link.springer.com/article/10.1007/s00010-026-01266-w),
published 20 February 2026, develops complexity, cycle and tree results.
Its checked full text does not supply the joint strong-product counterexample;
it precedes publication of the original strong-product paper.

David C. Fisher's
[*Domination, Fractional Domination, 2-Packing, and Graph Products*](https://epubs.siam.org/doi/10.1137/S0895480191217806),
SIAM Journal on Discrete Mathematics 7(3), 493–498 (1994), treats related
product bounds. Only its accessible publisher abstract was checked in this
round; it does not itself provide this joint radius-two/three-packing
construction. That access limit leaves its full results and citation
descendants to further historical review.

## Attribution and remaining historical uncertainty

The cube packing size argument is classical Plotkin counting. The
strong-product maximum-distance formula is standard and is recalled in the
original source. Compatibility graphs, clique supports and flag-complex
language are existing general tools. No novelty claim is made for these
ingredients or the general terminology.

The specific graph, full proof, finite certificates and actual Lean
implementation are recorded here without a historical first-discovery
claim. The searches are not a complete MathSciNet/Zentralblatt review,
citation-graph audit, old (p,d)-domination bibliography review or search of
unpublished notes and folklore. An unchanged current source page also
does not exclude a separately posted resolution.

Before a journal submission, further useful checks include the original
1994 domination bibliography and perfect-code product literature,
specifically for prior support-clique realization mechanisms. If an earlier
complete result is identified, the attribution can be corrected while
preserving the original public commits and actual publication dates.
