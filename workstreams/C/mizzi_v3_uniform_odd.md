# C — Uniform odd-order TF symmetry forces paired cycle lengths

**Date:** 2026-10-10. **Classification:** rigorous structural obstruction for a restricted family, **not** an original conjecture counterexample or an unrestricted proof; independent review and historical novelty checks pending.

## Source gate and alternative within the CDC scope

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3, Section 7, 10 September 2026 (https://arxiv.org/html/2603.27559v3#S7) conjectures that any **unstable asymmetric** graph contains both simple cycles C_k and C_(2k) for some odd k>=3, in its connected, nonbipartite, vertex-determining setting. This is separate from the author's TF-cousin-pair conjecture, which has two disjoint C_k cycles in one graph and a C_(2k) in the other.

A crucial source exclusion: Prateek R. Srivastava, *A Ten-Vertex Counterexample to a Conjecture on Unstable Graphs*, arXiv:2608.15281v1 (https://arxiv.org/abs/2608.15281), presents a counterexample to the **earlier unrestricted unstable-graph formulation**. The later v3 conjecture explicitly assumes **asymmetry** and is not automatically refuted by that earlier construction. This was a bounded screen, not a proof of 2026 open status or novelty. The Mizzi source reports independent small-order searches; they were not repeated.

## General exact theorem

Let m>=3 be **odd** and let a finite simple undirected graph G have vertex set
V(G) = { (i,a) : 0<=i<r, a in Z/mZ }.
Define alpha(i,a)=(i,a+1) and beta(i,a)=(i,a-1). Assume the ordered-edge **two-fold automorphism** identity

    uv in E(G)   iff   alpha(u) beta(v) in E(G)

for every ordered pair u,v, exactly as defined in the paper.

**Theorem.** If G is nonbipartite, G contains **one simple C_k and (m-1)/2 disjoint simple C_(2k)** for **some odd k>=3**. These cycles are mutually vertex-disjoint. Consequently no G in this uniform fixed-point-free odd-order TF class can refute the source's unstable-asymmetric cycle-pair assertion.

**Proof.**

1. There is no edge within a block. If (i,a)--(i,b) existed, repeated application of (alpha,beta) sends this edge to (i,a+t)--(i,b-t). Choose t with 2t=b-a modulo odd m. This would be a forbidden loop.
2. If (i,a)--(j,b) is present for i!=j, the full perfect matching with constant index sum s=a+b must be present: M_ij(s)={(i,x)--(j,s-x):x in Z/mZ}. Distinct sums give disjoint matchings. Thus G is a union of selected matchings between blocks.
3. Define quotient graph Q on blocks, connecting i and j whenever some such matching is present. A 2-coloring of Q would lift to a 2-coloring of G (no within-block edges), so nonbipartite G implies nonbipartite Q. Select a *simple odd cycle* (i_0,...,i_(k-1)) in Q, with odd k>=3.
4. For each edge of that quotient cycle select just one of its nonempty matchings M_ij(s_j). A step through a matching updates index x to s_j-x. Going around an **odd** number k of these matchings induces F(x)=c-x modulo m. Since m is odd, F has exactly one fixed point x=c/2, and (m-1)/2 disjoint 2-element orbits. The fixed orbit lifts to a simple C_k. Each two-element orbit lifts to a simple C_(2k). The cycles are vertex-disjoint because the quotient cycle visits distinct blocks and the F-orbits are disjoint within each fiber. All chosen edges belong to the actual graph G. QED.

This proof **does not apply** to arbitrary TF symmetries with fixed points, unequal orbit lengths, or a TF pair not of the displayed (alpha,alpha^-1) form. It does **not** settle Mizzi's full conjecture, let alone the distinct TF-cousin-pair conjecture.

## Exhaustive 12-vertex diagnostic (not needed for the theorem)

With four blocks of size m=3, the six unordered block pairs each have three independently selectable perfect matchings. The entire class has **2^18=262144 labelled graphs**. The independent C++20 program `uniform3_exhaustive.cpp` rebuilds the adjacency list from all such matchings, tests graph connectivity/bipartiteness, directly searches simple 3- and 6-cycles, and performs five intentional sanity/negative test families. Skipping masks with fewer than four matchings is sound: at most nine edges cannot connect twelve vertices.

Run from `workstreams/C`:

    g++ -std=c++20 -O2 -Wall -Wextra -Werror uniform3_exhaustive.cpp -o /tmp/verify_C_uniform3
    /tmp/verify_C_uniform3
    sha256sum uniform3_exhaustive.cpp

**Actual run, 2026-10-10:** GCC compiled without warnings, program exited zero:

    exhaustive_orbit_masks=262144
    checked_connected_possible=261156
    connected=257942
    connected_nonbipartite=245764
    connected_nonbipartite_with_C3=245764
    connected_nonbipartite_with_C6=245764
    counterexample_to_subfamily_lemma=0
    negative_tests=5 passed

Verifier SHA-256: `cbb7d6f9e1711ce69f8af6f58dbfbb32e2b8b6f2e3d605810fb781f7e81de367`; Git blob SHA-1: `067645db0e3ad9bff9eecd796145278bb189086e`. Unlike the finite enumeration, the written proof covers every odd m>=3 and any block count r.

## Decision

**Stop** all counterexample searches *within this uniform odd-order TF-shift family*: they cannot meet the desired negation. An admissible next mechanism would involve nonuniform odd orbit lengths or fixed points, only after checking other claims, original literature, and whether these constructions are already covered by Mizzi/Bychawski. The earlier Collins–Sciriha Q5.8 **affirmative proof candidate** remains frozen separately; no firstness, external referee, Lean proof, main-branch acceptance, submission or author communication is claimed.
