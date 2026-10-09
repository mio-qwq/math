# Public open-problem candidates and precise remaining targets

Source review: 8 October 2026; C7 rechecked on 9 October 2026.
The questions below are explicitly left
unresolved in the cited primary works. This is a bounded literature
review, not certification that no subsequent proof exists. No new global
bound or solution is claimed in this document; small investigated branches
are distinguished from the public open targets.

The MUB structural target already has a separate
[source review](004-mub-triplets/LITERATURE.md) and
[conditional mathematical reduction](004-mub-triplets/spectral-companion.md).
In particular, a published claim about the maximum number of bases must
be considered before treating the original maximum-number problem as
untouched. The candidates below concern different public problems.

## C7: seven-cycle Shannon capacity

For a graph G, its Shannon capacity is
\[
\Theta(G)=\sup_{n\ge1}\alpha(G^{\boxtimes n})^{1/n}.
\]
In C7 two symbols are confusable when their difference modulo seven is
0 or ±1. Two distinct words are confusable when this holds at every
coordinate. A code is an independent set in the strong graph power.

[Tandon, August 2026](https://arxiv.org/html/2608.30273v1)
records the exact capacity as unknown and proves a heterogeneous
recursion giving the reported lower bound 3.2588326203532663… .
The cited Lovasz upper bound is
\[
\Theta(C_7)\le \frac{7\cos(\pi/7)}{1+\cos(\pi/7)}
=3.31766720\ldots .
\]
The lower-bound computation and
[author code](https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion)
have not been independently replayed here.

The 9 October source check also compared the authors' default branches:
BPZ commit aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65 reports
3.258827985920007…, and Tandon commit
c753408492dde92a239708986d16c15dbf6c3235 reports the stronger bound above.
An official arXiv metadata search over 31 August–9 October found no reliable
new C7 solution in the matching entries. This remains a bounded review:
non-default branches and issues were not exhaustively checked, and
unindexed work or older papers with new revisions may be missed.

Remark 3 and Section 5 explicitly leave a genuinely two-sided
heterogeneous extension: both factors may use unrelated codebooks,
so automatic cross-block separation is lost. A concrete research
target is a useful compatible gadget family with a proved recursion
for its separation data and exact size. Merely rewriting the basic
product-block independence condition would not settle this extension.
A new general construction, rigorous obstruction or improved lower
bound would be substantive; a numerical failure to find a larger code
would not be an upper bound.

BPZ's existing [general separation/substitution framework](https://github.com/spectra-research/shannon-capacity-lean/blob/aa21eeb12b75b0413d3fa9fb4208b5d0bf2c4d65/ShannonBounds/Layered.lean)
already accepts arbitrary finite separation systems and different input
dimensions. New labels or the elementary cross-block separation condition
alone would therefore repeat an existing interface.

### Proved limited result: an explicit fraction-graph family

The [parameter barrier](notes/c7-fraction-family-barrier.md) considers
exactly Buys–Polak–Zuiddam Theorem 1.7 in arXiv:2506.14654v1, with
the direct-transfer condition p/q≤7/2. Every displayed certificate
satisfies p²≤10ⁿ; dimensions at least three satisfy p≤3ⁿ.
The full arithmetic bound and integer-quotient definition are Lean-verified.
This excludes that one direct-transfer parameter family from improving
C7's lower bound. It does not bound the largest independent set of the
source graph or of C7, or exclude other lattices or nonlinear repair.

[Polak–Schrijver §3](https://arxiv.org/html/1808.07438v2) already reports
failure of every three-deletion/four-insertion exchange on its specified
367-word code. This covers smaller positive exchanges on that same code;
it is not a global proof that 368 words are impossible.

### Investigated branch: a pure neutral auxiliary set

For the product of the paper's one-dimensional toy gadgets, the propagated
transversals are PH={(0,3),(3,6)} and PV={(6,3),(3,0)}. A vertex is neutral
when it belongs to neither closed neighborhood. Its exact neutral region is

    ({0,1,5,6} x {0,1,5,6}) union ({2,3,4} x {2,3,4}).

Each factor set is covered by two cliques: {5,6},{0,1}, and {2,3},{4},
respectively. Their product cliques cover the region with eight cliques.
The eight-word independent set

    {(2,2),(2,4),(4,2),(4,4),(0,1),(6,5),(1,6),(5,0)}

attains the bound. It is the main code minus its two selected private-pair
centres. That neutral-core choice is an elementary consequence of the
private-pair definition, not a new general construction. Its profile is
(a,t,s,o,h,v)=(10,2,8,8,0,0). The specified fixed-anchor one-sided families
instead have o<=6: each of their three contributions has the independent
number-two bound of a three- or four-vertex induced path. Other anchors
and general two-sided profiles are not excluded by this comparison.

This neutral-core family closes under ordinary Gao self-products, with
b=a-t=s=o, h=v=0 and b'=b^2, t'=2bt, a'=a^2-t^2. Thus for t>0 each
self-product strictly decreases the code's dimension root. Starting from
the displayed two-dimensional gadget, after k self-products the root is

    sqrt(8) (1+2^(k-2))^(1/2^(k+1)),

which tends to sqrt(8)<3. This rules out root improvement from continuing
that pure-neutral self-product route. It does not exclude mixed auxiliary
sets, asymmetric partners or use within another recursion. The finite
gadget and clique checks were independently checked with exact modular
arithmetic; this branch has no Lean proof or certified originality claim.

## K5: five-dimensional kissing number

The kissing number tau_5 is the maximum number of unit vectors in R^5
whose distinct pairwise inner products are at most 1/2.
[Cohn and Rajagopal, published July 2026](https://link.springer.com/article/10.1007/s00454-026-00841-x),
[Section 2](https://arxiv.org/html/2412.00937v3), records
\[
40\le\tau_5\le44.
\]
Its four nonisometric 40-point configurations and uniform-packing
classification do not classify all spherical codes or prove tau_5=40.

A precise target is infeasibility of a real symmetric 41-by-41 matrix G
with
\[
G\succeq0,\qquad \operatorname{rank}G\le5,\qquad
G_{ii}=1,\qquad G_{ij}\le\tfrac12\quad(i\ne j).
\]
Such an exclusion would determine tau_5=40; a feasible matrix would
give 41 points. The PSD/rank conditions retain the common continuous
geometry. Restricting entries to a finite grid does not cover the
problem. A useful partial result would specify a genuine continuous
geometric branch and prove its exclusion or a new rank-coupled
inequality, rather than repeat the known D5 construction.

## SIC: Galois compatibility after ghost construction

The general SIC existence question asks for d^2 unit complex vectors
in dimension d with distinct squared inner products 1/(d+1).
The stronger Weyl–Heisenberg-covariant formulation is a separate
symmetry requirement; see
[Renes, Blume-Kohout, Scott and Caves](https://arxiv.org/abs/quant-ph/0310075).

[Radchenko and Wheeler, September 2026](https://arxiv.org/html/2609.21892v1)
and [Appleby, Flammia and Kopp, September 2026](https://arxiv.org/html/2609.39192v1)
prove algebraicity and the relevant twisted convolution identities.
The latter constructs the ghost r-SICs for admissible tuples. Those
steps should not be reproposed as remaining conjectures.

The AFK introduction explicitly states that the needed Galois
automorphism is not known to exist. The concrete target is its
compatibility with complex conjugation, the quadratic-field switch
and the displacement phases, so that the actual algebraic ghost
construction becomes Hermitian. Algebraicity alone does not imply
that compatibility. A Hermitian idempotent is positive semidefinite,
but that elementary fact does not supply the required field map.
The rank-one case is relevant to ordinary SICs; higher-rank ghost
statements must retain their actual rank and normalization.

A meaningful partial advance would prove the required field and
conjugation conditions for a genuinely uncovered admissible family.
Choosing arbitrary algebraic matrices or approximately Hermitian
numerical data would not identify the special-value construction.

## Evidence boundaries

These are source-defined candidates, distinct from the proposed
extensions and proved special cases in the
[research register](RESEARCH_QUESTIONS.md). They have no local Lean
theorem, compiler receipt or improved numerical bound yet. Proof
claims found during later review should update this record before
being treated as verified inputs or as uncontroversially open targets.
