# Colour-universal rooted cubic gadgets and high-girth nonbipartite family

**Original target:** Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1, Conjecture 10 (2026-09-10), https://arxiv.org/html/2609.11832v1 . This is an **affirmative partial result**, not a counterexample or a solution for all graphs. Prior-work screening is bounded; historical novelty, Lean formalization and independent ROOT acceptance are not certified.

## General rooted interface theorem

Let B be a simple cubic bipartite graph with parts U,W, root r in W and a fixed proper **three-edge-colouring** with colours 0,1,2. Denote by u_i the neighbour of r along its colour-i edge. A *root-aligned U order* is a total order on U such that (1) u_0<u_1<u_2, and (2) at every w in W\\{r}, the three incident edge colours read in increasing order of their U endpoints are **not** (0,1,2).

**Lemma.** If B admits such an order, replacing a vertex z of an orderable properly three-edge-coloured loopless cubic graph H with B−r, reattaching the old incident edges to the three u_i, preserves orderability under the given colours. Here colours 0,1,2 are renamed from the incident colours of z in the order in which its old incident edges occurred in the successful order of H.

**Proof.** Make a consecutive block of all three incident edges at each u in U, placing them in colour order 0,1,2. Concatenate the blocks in the root-aligned U order. Every internal gadget edge belongs to precisely one such block. This yields sequence (0,1,2) at **every** U vertex, whereas every W\\{r} vertex gets a different sequence by property (2). The three external edges occur in the same relative order as H by property (1), so insert the internal edges among old edges without changing the order of any pair of old edges. Every outside vertex retains its original sequence and is different from z's old sequence (0,1,2), so the external edges also remain safe. All internal edges are safe by bipartiteness, establishing the lemma. QED.

### Why this handles every fixed three-colouring

Assume B has a root-aligned order **for every proper three-edge-colouring**. Let G be the uncoloured graph obtained by this rooted substitution, and now choose an *arbitrary* proper three-edge-colouring of G (not necessarily the one used during construction). Each colour class of the cubic graph G is a perfect matching. The substituted gadget vertex set S=V(B)\\{r} has odd size and exactly three boundary edges. Every perfect matching crosses this boundary an odd number of times, because |S| is odd. Thus the three colour classes must cross **once each**. In particular the boundary colours are distinct. Adding back r gives a proper three-colouring of B; contracting the entire gadget gives a proper three-colouring of H. If H is orderable under **every** proper three-colouring, choose an order for that contracted colouring and apply the preceding lemma using B's root-aligned order for the induced colouring. Therefore substitution preserves the all-proper-three-colourings property.

For a connected cubic graph, a fixed proper edge-colouring using more than three global colours has two adjacent vertices with different three-colour palettes (otherwise every vertex would have the same palette by connectivity). This case was **already established in Theorem 5 of the source paper**. Thus the replacement also preserves the original conjecture's *every proper edge-colouring* quantifier for connected cubic graphs.

## Two rooted colour-universal gadgets

The following records specify their *uncoloured graphs* plus one legal reference colouring: each row "u:(v0,v1,v2)" means that u in U is adjacent to vertices v0,v1,v2 in W by colours 0,1,2, respectively. Root r=0. The separate exhaustive certificate below covers **all** proper three-colourings, not only the displayed one.

**Cube Q3**, |V|=8, U=(1,2,4,7), U order=(1,2,4,7):

    1: (0,3,5)
    2: (3,0,6)
    4: (5,6,0)
    7: (6,5,3)

The internal W sequences at 3,5,6 are respectively (1,0,2), (2,0,1), (2,1,0); root interface order is 1<2<4.

**Heawood graph**, |V|=14, U=(1,3,5,7,9,11,13), U order=(1,3,7,9,11,13,5):

    1:  (0,2,10)
    3:  (2,4,12)
    5:  (4,6,0)
    7:  (6,8,2)
    9:  (8,10,4)
    11: (10,12,6)
    13: (12,0,8)

The internal W sequences at 2,4,6,8,10,12 are (1,0,2), (1,2,0), (0,2,1), (1,0,2), (2,1,0), (2,1,0). The root neighbours in colour order are 1,13,5, occurring in that order of U blocks. Heawood has girth six; after removing r, its three boundary vertices have pairwise distance four.

**All-colourings finite certificate.** A standard-library DFS assigning colours to **each edge** under the original properness definition finds **exactly 24 proper labelled three-colourings of Q3 and 48 of Heawood**. For each of these 72 colourings an exhaustive search of U orders satisfying u_0<u_1<u_2 finds a valid root-aligned order. An independent enumeration based on choosing a perfect matching for colour 0 and alternately colouring the 2-regular complement 1/2 gives the same counts (24,48). Negative controls reject invalid edge colourings. Reproduce via \`python3 workstreams/A/code/verify_rooted_gadgets.py\`. Actual run: \`PASS cube 24; PASS heawood 48; PASS negative colouring tests\`. This is a *complete finite proof certificate for the two explicit gadgets*, not a graph-size extrapolation.

## Nonbipartite girth-six infinite family

A separate rank-sum argument in \`UNIVERSAL_VERTEX.md\` proves that **K4** admits a good edge order under every proper edge-colouring. Replace **each of the four vertices of K4** with a copy of Heawood−r. Each replacement adds 12 vertices, yielding a **simple connected cubic graph on 52 vertices and 78 edges**. The original K4 triangles expand to odd cycles because every path within the bipartite gadget between two boundary vertices has even length; thus the result remains nonbipartite. Heawood−r has girth six, and paths joining any two of its boundary vertices have length at least four. Any cycle crossing a gadget is no shorter than the old cycle, and the resulting 52-vertex graph has exactly girth **six** (verified by an independent shortest-cycle BFS). The full global edge order is constructed from a proper K4 order via four successive root-aligned gadget templates and independently checked against the exact incident-edge colour sequences.

**For every proper edge-colouring** of this 52-vertex graph the universal-gadget lemma and original source Theorem 5 now supply a good edge order. Further Heawood substitutions preserve cubic regularity, simplicity, connectedness, nonbipartiteness and girth≥6: paths between boundary vertices in B−r have even length at least four, so each old odd cycle can be rerouted without changing its parity and no new shorter cycle is introduced. This gives an **infinite family of nonbipartite, girth-at-least-six, cubic simple graphs** satisfying the original universally quantified edge-orderability claim. This does not resolve arbitrary nonbipartite cubic graphs.

## Reproduce / audit

From repo root, without third-party Python packages:

    python3 workstreams/A/code/verify_rooted_gadgets.py
    python3 workstreams/A/code/verify_heawood_substitution.py

The second checker rebuilds every edge from the explicit records, verifies the 52-vertex graph has 78 edges and a successful global order, computes its girth and bipartiteness directly, and deliberately rejects an incomplete order. Actual run: \`PASS Heawood interface, 4 substitutions, 52 vertices / 78 edges, girth 6, nonbipartite, original edge sequences\`.

These are **unsigned GitHub transport reconstructions** pending independent ROOT scope and mathematical review, not the previous missing signed frozen archive. No author contact, merged main commit, formal project number, claim of priority, or background automation.
