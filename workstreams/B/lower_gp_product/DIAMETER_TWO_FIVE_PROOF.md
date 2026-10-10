# Universal truncation at five for diameter-two factors

B, 2026-10-10. **Computer-assisted all-orders partial theorem; independent review pending.**

## Original question and exact scope

Eartha Kruft Welton, Sharif Khudairi and James Tuite, *Lower General Position in Cartesian Products*, arXiv2404.19451v1 Conjecture2.10; final CCO10(1)(2025),110–125, Conjecture3 on printedp117, DOI10.22049/cco.2024.29171.1879. Primary final: https://oro.open.ac.uk/98050/9/98050final.pdf . Original claim is gp^-(G square H)>=min{gp^-(G),gp^-(H)}. Here gp^- means the minimum cardinality of an inclusion-maximal general-position set. All graphs below are finite, nonempty, simple and connected. GP excludes three DISTINCT selected vertices on a shortest path.

**Theorem.** If diam(G)<=2 and diam(H)<=2, then

    gp^-(G square H) >= min{5,gp^-(G),gp^-(H)}.

In particular the ORIGINAL conjecture holds on these diameter-bounded factors whenever the smaller factor parameter is at most5. Both graph orders are arbitrary. This does not resolve the original conjecture for arbitrary factors, or even for all diameter-two factors when both lowerGP parameters exceed5. It improves B's general truncation at4 (frozenebaa409418b53983ef1bd52abe34703c5dca6618) on this diameter class. It is not a numerical graph-order check or a counterexample.

## Reduction to a four-point extension statement

The previously frozen arbitrary-graph theorem handles all maximal GP sets of size at most3, and all cases with a factor lowerGP<=4. Thus suppose gp^-(G),gp^-(H)>=5. We prove that any four-element product GP set

    S={(a_i,b_i):0<=i<4}

has a GP extension. Coordinates may repeat; the product points must be distinct. Cartesian-product distances are sums of factor distances: every product walk must make the required number of steps in each coordinate, and concatenating shortest factor paths attains that bound.

Put A_ij=d_G(a_i,a_j), B_ij=d_H(b_i,b_j). They are symmetric pseudometrics on four labels with entries0,1,2. Zero distance means the corresponding landmarks are the SAME original vertex, not merely equivalent vertices. Triangle inequalities imply equality of rows for zero-distance labels. Every such matrix is included in the finite enumeration below, whether or not extra global graph hypotheses happen to permit it.

For a vertex outside the distinct A-landmarks, write v_i=d_G(x,a_i). Each entry is1or2; entries coincide on zero-distance labels; all metric triangle inequalities with A hold. Conversely it is safe to allow EVERY such vector, since this enlarges rather than shrinks the possibilities for an actual graph. Existing landmark vertices have their exact rows of A as known profiles. Define the analogous profiles for B.

For a GP subset T of distinct landmarks, an outside profile v extends T exactly when, for every distinct i,j in T,

    |v_i-v_j| < A_ij < v_i+v_j.                 (1)

These strict inequalities exclude all three possible shortest-path equalities. Consider only GP subsets T that are inclusion-maximal AMONG THE LANDMARKS. They have at most4elements. Because gp^-(G)>=5, T is not maximal in the full graph. Some actual vertex extends it, and this vertex is outside ALL landmarks by landmark maximality. Consequently the set X of actual outside distance profiles intersects every demand

    E_T = {allowed profiles v satisfying (1)}. (2)

Multiple vertices with the same outside profile need not be counted separately: only existence is used. Coordinate-zero profiles are separately retained as known vertices. The same demand rule holds for H.

For any profiles v,w (known or outside), their proposed product vertex has distances t_i=v_i+w_i to S. It is an eligible GP extension exactly when

    every t_i>0, and
    |t_i-t_j| < A_ij+B_ij < t_i+t_j for i<j.    (3)

Positivity excludes reusing a selected product point. Thus maximality of S forbids every compatible profile pair under (3).

## Exact finite decision and why it is complete

`verify_four_signatures.py` is standalone Python3 standard library, with no imports from the discovery script. It performs the following full exhaustive checks:

1. Enumerate all3^6 assignments to the upper triangle of a4by4 matrix. Keep exactly the symmetric pseudometrics with diagonal0 and triangle inequalities. There are127, including ALL repeated-coordinate patterns.
2. For each matrix compute all1/2profiles, all maximal landmark GP subsets and their demands (2). There are at most16 outside profiles. Enumerate ALL subsets of these profiles, retaining the inclusion-minimal demand-hitting sets. Minimality is checked by every single-element deletion, valid because hitting all demands is a monotone property. There are1629minimal sets over the127models.
3. Examine each unordered pair of models, exchanging factors if needed. Keep only those where the four product labels are distinct and GP. Exactly3956pairs remain.
4. Known profiles are unavoidable. If any known-known pair satisfies (3), maximality is already impossible. Otherwise remove outside A-profiles compatible with a known B-profile and outside B-profiles compatible with a known A-profile.
5. For every minimal A-demand-hitting set X not already removed, retain only B-profiles incompatible with ALL of X and with all known A-profiles. Verify that at least one B-demand has empty intersection with this remaining set. All522 surviving minimal-X cases fail a B-demand. All other minimal-X cases were already impossible due to a known profile. No factor pair admits the necessary profile system.

For completeness of step5, if actual outside profile sets existed, choose an inclusion-minimal demand-hitting subset X of the actual A-set. It appears in the exhaustive list and contains no profile removed in step4. Every actual B-profile must remain after step5's deletions, yet its nonempty intersection with each B-demand would contradict the verified empty demand. This contradiction does not assume that arbitrary profile systems can be realized as full graphs. Necessary constraints are sufficient for a NONEXISTENCE certificate.

The checker uses a different enumeration from discovery: discovery uses restricted-growth partitions, edge assignments and recursive minimal transversals; verification directly enumerates all pseudomatrices and all profile subsets. Both agree on127models,3956GP product patterns and no feasible local system. The verification program is an exhaustive finite component of the proof, not an independent reviewer's endorsement.

It follows that S has an extension. Combining with the previously proved size<=3 cases gives the theorem. QED.

## Semantic checks, limits and reproducibility

Run:

    python workstreams/B/lower_gp_product/verify_four_signatures.py

The checker additionally rebuilds original adjacency graphs for all127models: distinct landmarks with adjacency exactly at distance1, one vertex for each external profile adjacent to the indicated distance1landmarks, and a universal hub. Full BFS confirms every retained landmark distance and profile entry. These auxiliary graphs verify distance semantics only; they are NOT claimed to satisfy lowerGP>=5. Negative controls reject a triangle-inequality violation, a collinear claimed GP triple, and a repeated-point claimed extension.

Exact run counts, certificate-stream digest, environment and SHA256s are in DIAMETER_TWO_FIVE_REVIEW.md and verify_four_signatures.log. Source status/duplicate searches on2026-10-10 found no matching truncation-at5 result; historical priority is not certified. The original paper's terminal-set theorem for diameter<=3 concerns a different conclusion and is credited as prior, not reused as this lower-bound claim. No Lean, external review, exact product number, arbitrary-diameter extension or full original-conjecture resolution is claimed.
