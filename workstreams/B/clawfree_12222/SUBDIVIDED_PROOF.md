# Fully subdivided triangle expansions: a second affirmative subcase

Agent B, 2026-10-10. Pending independent review; not a full solution or counterexample to arXiv:2608.02566v1 Section 6 Conjecture 1. This supplements, and does not alter, frozen CUBIC_PROOF.md at b49a74f9ed65133a8c0e12ee998c44c5401e73d8.

## Statement

Take vertex-disjoint triangles. Choose any matching of their ports (triangle vertices), allowing paired ports in the same triangle. For each matched pair insert an internally disjoint path of length L>=2, with no other edges. Unmatched ports are allowed. The resulting finite simple claw-free subcubic graph has a (1,2,2,2,2)-packing vertex coloring. Every length may differ, there is no bound on lengths or the number of triangles, and the underlying core may have loops and parallel edges.

Colors 1,2,3,4 require pairwise distance greater than 2; color 0 requires greater than 1. Distances always refer to the entire original graph, not a suppressed core.

## Triangle colors

Construct an auxiliary simple graph on all triangle vertices: retain all triangle edges and add an edge for each connector of length exactly 2. A same-triangle added edge already exists and is not duplicated. Its maximum degree is at most 3. Every component is a union of entire vertex-disjoint triangles, so no component is K4. Brooks' classical theorem gives a proper 3-coloring (an odd-cycle component is just a triangle). Color these vertices with 1,2,3. Within each triangle these three colors are distinct. Triangle vertices in different triangles are within distance 2 precisely when they are the two ends of a length-2 connector; auxiliary properness excludes that conflict.

This use of Brooks' theorem is standard prior theory, not a claimed new theorem.

## Arbitrarily long connector words

Let the endpoint colors be p,q in {1,2,3}. The following are complete path words, including endpoints:

- L=2: p,0,q. Here p!=q by the auxiliary coloring.
- L=3: p,0,4,q.
- L=4: p,0,4,0,q.
- L=5: p,4,0,e,0,q, where e is any element of {1,2,3} different from q.

For L>=3 there is no restriction p!=q. Each word is valid on its path and has first and last internal colors in {0,4}.

Extend a valid word ending in t,q (t in {0,4}) by three edges: replace this final pair with t,q,r,t,q, where r is a radius-two color distinct from q and, when t=4, also distinct from 4. Such r exists. The retained prefix has the same compatibility with its next q as before. In the added suffix adjacent equal colors do not occur; equal positive colors cannot occur at distance 2. The repeated q and t are separated by 3. The new final internal color is still t. This proves the construction for every L>=3, by reducing to one of 3,4,5 modulo 3. Endpoint colors and the first internal color are unchanged.

## Why the path words remain valid in the full graph

An internal vertex can be within distance 2 of vertices outside its own path only through one of its endpoints. The first internal vertex may see that endpoint, its two triangle neighbors, and (for length 2) the opposite endpoint. Its color 0 or 4 avoids all triangle colors. The second internal vertex sees only the endpoint at distance 2, a restriction already checked by the path word. The same statements hold at the other end.

Distinct connectors use distinct ports. Thus internal vertices on different connectors have distance at least 3, even when their endpoints lie in the same triangle. A shortcut between internal vertices on the same connector through its endpoints also has length at least 3: reaching each endpoint costs at least 1 and joining distinct endpoints costs at least 1. Consequently no such shortcut creates a new radius-two conflict. This also handles loop connectors joining two ports of one triangle. Color 0's adjacency condition is weaker. These observations cover every pair of equal-colored vertices.

The graph is claw-free because every degree-three vertex has its two adjacent triangle neighbors; other vertices have degree at most two. Hence the theorem is a genuine affirmative subcase under all original hypotheses.

## Limits and verification

Length-1 connectors are expressly excluded. Mixing direct connections with subdivided connections is not resolved by this theorem or by the separate cubic theorem. Nor does this statement alone dispose of all diamond or nontriangle attachments. It does not imply the stronger (2,2,2,2,3) conjecture.

verify_subdivided.py uses original adjacency and BFS, independently checks every local word for lengths 2..50 and all endpoint-color pairs (subject to p!=q at length 2), and checks assembled examples with loops, parallel core edges, varying lengths, disconnected components and unused ports. A deliberate bad coloring must be rejected. These finite checks are error detection for the construction; the all-length and all-size statements depend on the written argument above and Brooks' theorem.

The exact-palette literature search was refreshed 2026-10-10 09:30 UTC; no same-scope statement located. This is not novelty certification. Sources and original statement are in SOURCE_GATE.md. No independent review or Lean compilation claimed.
