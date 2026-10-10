# Triangle expansion preserves sequential edge orderability in the cubic three-colour case

## Source and boundary

Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (2026-09-10), Conjecture 10, https://arxiv.org/html/2609.11832v1. This is an **affirmative reduction**, not a counterexample or complete proof of the conjecture. Historical novelty, independent ROOT acceptance and Lean formalization are not claimed.

For a proper edge colouring w and a total edge order ≺, write f(v) for the incident colours in that order. Sequential orderability means f(u)≠f(v) at every edge uv.

## Theorem — triangle expansion lemma

Let H be a **loopless cubic multigraph** with a fixed **proper three-edge-colouring** and an edge order that distinguishes the incident-colour sequences of all adjacent vertices. At a vertex z, replace z with a triangle A,B,C and attach each of its three old edges to a distinct triangle vertex, assigning internal edge colours to make the resulting cubic graph properly three-edge-coloured. Then the expanded graph G has a successful edge order preserving the relative order of all original edges.

**Proof.** Name the three old edges e0,e1,e2 according to their order at z; relabel their distinct colours 0,1,2. Name triangle vertices so that e0 meets C, e1 meets A and e2 meets B. Properness forces x=AB to have colour 0, y=BC colour 1 and t=CA colour 2. The original vertex z has sequence (0,1,2). Each of its three old neighbours has a sequence different from (0,1,2).

Insert only x,y,t relative to e0<e1<e2. All three templates below respect the original external order (other old edges remain in their original relative order):

| Six-edge template | f(C) | f(A) | f(B) |
|---|---|---|---|
| x,y,t,e0,e1,e2 | (1,2,0) | (0,2,1) | (0,1,2) |
| t,x,y,e0,e1,e2 | (2,1,0) | (2,0,1) | (0,1,2) |
| t,e0,e1,x,y,e2 | (2,0,1) | (2,1,0) | (0,1,2) |

In each row, the three new triangle sequences are pairwise distinct. Vertex B always has sequence (0,1,2), automatically distinct from the neighbour of e2 by the old successful order. The three possibilities for f(A) are distinct, so the fixed external neighbour of e1 forbids at most one template. Likewise the three possibilities for f(C) are distinct, so the neighbour of e0 forbids at most one template. Hence at least one of the three templates avoids **every** external neighbour, as well as all triangle edges.

Only three internal triangle edges are inserted; the relative order of every original edge pair stays unchanged, so all original neighbours retain their sequences, and every old edge not at z remains good. The original old e0,e1,e2 need not be consecutive: any desired template is realized by inserting the three new edges into appropriate gaps. The argument also works if the external neighbours coincide (parallel edges after contraction), but no loops are allowed in H. QED.

## Corollary — infinite nonbipartite family

Start with **any simple cubic bipartite graph** B and apply any finite series of triangle expansions. Every resulting **simple cubic graph** G is sequentially orderable under every fixed proper **three-edge-colouring**: the supplied colouring contracts properly, the bipartite block theorem solves B, and the lemma lifts the order step by step.

If a connected cubic graph is properly coloured with four or more colours globally, its palettes cannot all agree across every edge, so the **published Theorem 5** of Gorzkowska–Kwaśny already supplies a successful order. Thus the entire triangle-expansion family satisfies the source's **every proper colouring** quantifier. This does NOT cover every nonbipartite cubic graph.

## Reproduction

Run `python3 workstreams/A/code/verify_triangle_expansion.py` from repository root. The independent checker constructs all local triangle sequences from the six-edge templates, checks exterior order and internal inequalities, exhausts **180 admissible triples** of external neighbour colour sequences, and tests a deliberately corrupted template. Actual standard-library run (Python 3): `PASS three explicit edge-order certificates; 180/180 admissible outside patterns; negative test`. The three explicit templates plus the choice argument, rather than a bound-limited graph enumeration, prove the infinite structural statement. No external independent review yet.
