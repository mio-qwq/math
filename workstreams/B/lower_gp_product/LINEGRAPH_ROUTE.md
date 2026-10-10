# New pure support-counting route, 2026-10-10 11:29UTC

Candidate theorem: the ORIGINAL lower-GP product inequality holds for L(K_n) square L(K_m), all n,m>=2. Distinct from the already-frozen Kneser family: adjacency here is INTERSECTION, not disjointness. Original factor formula is known from Di Stefano et al. arXiv2306.09965v1 Theorem5.2: even n gives n/2, odd n gives(n+3)/2. Not a new factor claim.

Proof mechanism to finish/check: suppose a maximal product GP-set has k<both factor lowerGP values. Frozen universal truncation implies k>=4; the factor formula implies n,m>=2k-1. Each factor projection is a list of k edges.

If a projection has k distinct GP points, extend it in that factor. If it has k-1 distinct GP points, only one fiber repeats (twice); extend the projection and the opposite repeated-fiber pair separately. Both constructions extend the product set.

If a projection has k distinct points but is NOT GP, its edges contain a three-edge P4, because line-graph distances are1for intersecting distinct edges and2for disjoint edges. Hence support uses at most2k-2 symbols. With two unused symbols, choose their edge u and choose any opposite factor vertex outside its projection. New product distances are3or4. A selected pair at product distance1 must have the same opposite coordinate and adjacent first coordinates, so its two new distances are equal; all other old pairs have distance>=2. Thus no new triple is collinear.

The only critical case has just ONE unused symbol, requiring n=2k-1 and exactly2k-2 used symbols. The projection must then be one P4 plus k-3 disjoint isolated edges. Choose an isolated selected edge at index i, and let u join one of its endpoints to the unused symbol. Then d(u,a_i)=1 and d(u,a_j)=2 for j!=i. In the other factor select v outside all projected vertices and disjoint from b_i. Such v exists since C(m-2,2)>=C(2k-3,2)>k for k>=4. New product distances again lie in{3,4}; any selected pair at distance1 uses adjacent first-coordinate edges, neither the isolated edge i, and identical opposite coordinates, so its new distances agree. Hence this case also extends.

If neither projection matches an earlier case, each has either <=k-2 distinct edges or k-1distinct non-GP edges. Its support has at most2k-4 symbols, leaving at least3 unused symbols. Pick an unused-symbol edge in each factor. The new point is distance4from every selected point and hence extends, since the product diameter<=4.

This would exclude every counterexample in this whole family, with no finite-to-universal inference. Still needs full proof writeup and original-BFS constructor checks. Kneser result remains frozen0949c807e9ce28b4066509066ee06433a593b4ff. No new subagents or other branches used.
