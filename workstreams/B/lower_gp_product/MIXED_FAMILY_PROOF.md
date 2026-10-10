# Closing the two pair-graph families under mixed Cartesian products

B,2026-10-10. **Complete elementary mixed-family proof; independent review pending.** Combined with the separately frozen Kneser and complete-line-graph results, the original lower-GP product inequality now holds whenever EACH factor is either K(r,2),r>=5, or L(K_r),r>=2. This is one combined subclass result, not three resolutions of the arbitrary-factor conjecture.

## Mixed theorem

For all n>=2 and m>=5,

    gp^-(L(K_n) □ K(m,2)) >= min{gp^-(L(K_n)),gp^-(K(m,2))}.

The opposite order of factors is isomorphic. The original product conjecture is Kruft Welton–Khudairi–Tuite arXiv2404.19451v1 Conjecture2.10/finalConjecture3. We retain the distinction between intersection adjacency in L(K_n) and disjointness adjacency in K(m,2).

Known factor values (Di Stefano et al., arXiv2306.09965v1 Theorems5.1and5.2) are credited as prior. The arbitrary-graph truncated-at4 theorem is frozenebaa409418b53983ef1bd52abe34703c5dca6618. The Kneser-family proof is frozen0949c807e9ce28b4066509066ee06433a593b4ff. The pure complete-line-graph family proof is frozen95acdcd925c881809b7dee6c62ab7abf8ac18628. None of these author-side freezes is independent acceptance.

## Proof

Suppose there is a maximal product GP-set S={(a_i,b_i):1<=i<=k} with k smaller than both factor lowerGP-numbers. The truncated theorem gives k>=4. Since gp^-(K(m,2))<=6, necessarily k=4or5. The known formulas imply

    n>=2k-1, and m>=2k+2.

Each coordinate is a two-element symbol set. Distances between distinct points are1for intersection and2for disjointness in the first factor, with these roles reversed in the second. Both factors have diameter at most2.

If the first-coordinate projection has k DISTINCT points and is GP, extend that projection in L(K_n); pairing the extension with any second coordinate extends S. If it has k-1distinct GP points, there is exactly one repeated fiber of size two. Extend the first projection and also extend the corresponding distinct second-coordinate pair in K(m,2). Pairs in different fibers are protected by the first extension, and the unique same-fiber pair by the second. These arguments use strict factor-parameter inequalities, not assumptions about the proposed construction.

Now suppose the first projection has k distinct points and is NOT GP. Its k underlying edges contain a three-edge P4, so use at most2k-2symbols. If at least two symbols are unused, choose their pair u. It is distance2from every a_i in the line graph. The k second coordinates use at most2k symbols, so m>=2k+2 provides two unused symbols there as well. Their pair v is DISJOINT from every b_i and hence distance1from each in the Kneser graph. Thus(u,v) has distance3from every selected point. No new triangle equality is possible, because all old pair distances are positive and at most4, while new distance sums are6and differences0.

The critical case has exactly one unused first-factor symbol. Equality forces n=2k-1 and the first projection to be one P4 plus k-3disjoint isolated edges, exactly as in the pure line-graph proof. Pick one isolated edge a_i and let u join one of its endpoints to the unused symbol. Then its first-factor distance is1to a_i and2to every other a_j.

Choose v that intersects b_i in exactly one symbol and is not any selected second coordinate. There are2(m-2)>k choices before deleting the at most k forbidden projected vertices, so such v exists. In the Kneser graph d(v,b_i)=2, while every d(v,b_j) is1or2. Therefore all new product distances lie in{3,4}. Their sums exceed the product diameter, and their differences are at most1. An old pair at product distance1 must have equal second coordinates and adjacent distinct first coordinates. Neither first coordinate can be the isolated a_i, so their distances from u both equal2, and their new product distances are equal. Hence even distance1pairs cannot cause an endpoint equality. This gives another extension.

If none of the earlier cases occurs, the first projection has at most k-2distinct edges, or k-1distinct non-GP edges. Its support has at most2k-4symbols, leaving at least3unusedsymbols. Choose an unused-symbol pair u in the first factor, and an unused-symbol pair v in the second as above. Again(u,v) has constant distance3from S and extends it.

Every first-projection case is exhausted. The contradiction proves the mixed theorem. Small factors and singletons were already covered by the universal truncated theorem. QED.

## Combined scope and verification

The three proved factor combinations are Kneser–Kneser, line-graph–line-graph, and the mixed combination above. They jointly establish the ORIGINAL inequality on the union of these two infinite graph families. The arbitrary-factor conjecture remains unresolved, and no additional exact product values are claimed by this mixed argument.

`extend_mixed.py` implements the proof. `verify_mixed_extension.py` independently constructs both adjacency conventions, computes original BFS distances and checks the new product vertices. It tests explicit one-unused-symbol/fiber cases, the full metric bridge from actual product BFS, and negative controls. The all-parameter result follows from the elementary proof, not the test sample. No Lean, external acceptance or firstness claim.
