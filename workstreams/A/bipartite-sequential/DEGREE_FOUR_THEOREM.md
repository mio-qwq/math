# General two-factor transversal method: the complete four-regular case

**Original public problem:** A. Gorzkowska and J. Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026), Conjecture 10, https://arxiv.org/html/2609.11832v1. A fixed proper edge colouring w is given; we must exhibit ONE global total edge order making the sequence of incident edge colours distinct at endpoints of EVERY edge. No recolouring is permitted. The original paper already proves nonregular, class-two and d>=6 regular cases but explicitly lists d=3,4,5 regular class-one as unresolved.

**External standard theorem used:** Haxell's independent-transversal theorem: for a finite graph with maximum degree Δ and any vertex partition into sets of size **at least 2Δ**, there is an independent transversal choosing exactly one vertex from each part. The original theorem is from Penny E. Haxell (1995/2001), *A Note on Vertex List Colouring*, Combinatorics, Probability and Computing 10 (2001), 345–347; statement restated explicitly as Theorem 1 in Haxell–Wdowinski (2024), https://doi.org/10.1002/jgt.23085 . We invoke the theorem as known mathematics; no formal Lean implementation or separate proof of Haxell is claimed.

## Main theorem (any regular degree subject to a precise cycle condition)

Let d>=3, and let G be a finite simple d-regular graph with a **fixed proper edge colouring using exactly d colours** 0,1,...,d-1. Suppose that the 2-regular spanning subgraph formed by colours 0 and 1 decomposes into cycles C_1,...,C_k, **each of length at least 2(d-2)**. Then that given colouring is sequentially orderable.

### Proof

Every colour class is a perfect matching, since exactly d distinct colours meet each vertex of degree d. Hence the 0/1-coloured edges form vertex-disjoint alternating **even cycles** of length at least four (G is simple). Their vertex sets partition V(G). Form the auxiliary graph Q using **all remaining colours 2,...,d-1**, ignoring 0/1 edges. Its maximum degree is Δ(Q)=d-2. By the cited Haxell independent-transversal theorem and the cycle-length hypothesis, there is a choice of one vertex r_i from each C_i such that **no Q edge joins any two chosen roots**.

Choose any ordering C_1,...,C_k. Rotate and orient each cycle so the root is v_0 and its outgoing cyclic edge e_0=v_0v_1 has colour 0; label its cyclic edges e_j=v_jv_{j+1} for 0<=j<m-1 and e_{m-1}=v_{m-1}v_0. The colours of e_0,...,e_{m-1} alternate 0,1,0,1,...,1. Place all these 0/1 edges in the consecutive cycle blocks e_0(C_1),...,e_{m_1-1}(C_1),e_0(C_2),...,e_{m_k-1}(C_k).

Now insert every edge xy of colour c>=2 **immediately after** the outgoing cycle edge e_j at a designated endpoint v_j. Designate its root endpoint if it has one (it cannot have two, by the independent-transversal choice); otherwise designate the earlier endpoint under lexicographic order (cycle-block index, local cyclic index). Each vertex has **one edge of each extra colour**, so a slot may receive as many as d-2 edges. Sort the edges assigned to each slot by colour, yielding a unique well-defined global total edge order.

At each root, the colour-0 edge e_0 occurs first, all extra-colour edges are inserted immediately after e_0, and the colour-1 edge e_{m-1} occurs last among edges incident with that root. Thus the root sequence has the pattern

    (0, a permutation of all colours 2,...,d-1, 1).

Because d>=3, 0 and 1 are **not adjacent** within a root's sequence.

At each nonroot v_j (1<=j<=m-1), its two 0/1 edges e_{j-1}<e_j are **adjacent within its sequence**: every extra-colour edge at v_j occurs either before both or after both. Indeed, a colour-c edge designated at v_j goes after e_j; if designated at a vertex of another cycle, the entire foreign cycle block precedes or follows this cycle; and if designated at another vertex of the same cycle then that vertex has strictly lower local index, at most j-2, because designating an earlier endpoint is mandatory unless it is a root and the graph is simple (the extra edge cannot duplicate an adjacent 0/1 edge). Its insertion precedes e_{j-1}.

Every 0/1 cycle edge joining a root to a nonroot is therefore distinguished, because the root's two 0/1 colours are separated by extra colours and the nonroot's are adjacent. Every other 0/1 cycle edge is distinguished because its two nonroot endpoints see 0 and 1 in **opposite relative orders** along the alternating cycle.

Every extra-colour edge joining a root to a nonroot is distinguished by the same adjacent-versus-separated 0/1 pattern. For an extra-colour edge xy between two nonroots, its designated endpoint is earlier in lexicographic cyclic order. Its matching colour c is **after both 0 and 1** at that endpoint, and **before both 0 and 1** at the later endpoint: within the same cycle this follows because their positions are separated by at least two, since G is simple; between different cycles it follows from block order. Therefore their full sequences differ.

All edges are distinguished. No local orders are inconsistent because all were inserted into a *single* prescribed global edge order. QED.

## Consequence 1 — solves original complete d=4 regular class

For d=4, Δ(Q)=2 and **every** alternating 0/1 cycle in a simple graph has length at least 4=2Δ. The independent transversal therefore always exists. Hence **every fixed proper four-edge-colouring of every finite simple 4-regular graph is sequentially orderable**, including nonbipartite examples. For a connected four-regular graph whose fixed proper colouring uses **more than four colours**, the original authors' established unequal-palette Theorem 5 supplies an order (not reproved here). Therefore all connected 4-regular graphs satisfy their Conjecture 10 for **every** fixed proper colouring.

Combining with the independently proved complete d=3 case in ALL_CUBIC_THEOREM.md and the source's already published nonregular and d<=2 cases proves Conjecture 10 for **all connected graphs of maximum degree at most four except the original K2 and properly two-coloured even-cycle obstructions**.

## Consequence 2 — major fifth-degree subfamily, not all d=5

For d=5, Δ(Q)=3, so the same theorem applies whenever the chosen pair of colour classes has **no alternating 4-cycle**, since then its cycles have even length at least six. In particular, every 5-regular **C4-free** graph with a proper five-edge-colouring satisfies the fixed-colouring claim. Colourings using more than five colours in connected graphs follow from the source's unequal-palette result. The only unresolved regular degree-five class-one cases under this argument are fixed five-colourings in which **every pair of colours has at least one bichromatic 4-cycle**. We do not claim they are counterexamples, nor that the general conjecture is solved.

## Exact regression / interpretation

The Python-standard-library independent checker workstreams/A/code/verify_degree_four.py constructs full proper d-colourings, searches for roots separately by exhaustive backtracking (not by trusting a Haxell oracle), constructs the full edge order and directly recomputes all endpoint sequences. Actual Python 3.13.5 output:

    PASS 4-regular complete two-factor/matching enumeration {'(8,)': 446, '(4, 4)': 504} plus nonbipartite K4xK2, 5-regular K6, negative control

This includes 950 distinct complete 4-colouring instances from two possible two-factor partitions on eight vertices, with independently verified sequences, plus explicit nonbipartite degree-four and degree-five controls. These bounded checks are not the proof for arbitrary order. The infinite assertion relies on the displayed argument and the cited Haxell theorem.

**Provenance and acceptance:** Frozen candidate for independent ROOT scrutiny; GitHub API transport unsigned, no Lean source/audit, historical originality unverified. Not a claimed counterexample; the remaining fifth-degree case is explicitly outside the result. Only workstreams/A/ is written, no numbered project/merges.
