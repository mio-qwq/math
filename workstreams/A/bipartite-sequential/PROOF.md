# Bipartite block theorem for sequential edge orderability

Source: Aleksandra Gorzkowska and Jakub Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026), Sections 1, 4–5, Conjecture 10: https://arxiv.org/html/2609.11832v1. Read the full v1 original on 2026-10-10. Bounded follow-up search did not find a same-scope proof; novelty is not certified.

## Original definitions

Let G be a finite simple graph and w be a **fixed proper edge colouring**. For a total order prec on E(G), let f_prec(v) be the ordered list of colours on edges incident with v. "Sequentially orderable" means that *one global order* prec exists such that f_prec(x) != f_prec(y) for every xy in E(G). No freedom to recolour the edges is permitted.

## Theorem (affirmative subcase of the original Conjecture 10)

Let G have bipartition U,V. Suppose **every u in U has degree at least three**, and let w be *any proper edge-colouring*, using any finite set of colours. Then w is sequentially orderable. Connectivity and degrees in V are unrestricted.

**Proof.** Fix any ordering u_1,...,u_s of U and consider an edge order consisting of the consecutive blocks E(u_1),...,E(u_s), with each block's internal order to be chosen later. As G is bipartite every edge belongs to exactly one block. For a vertex v in V, each block contributes at most one incident edge **because G is simple**. Therefore its sequence f(v) is determined entirely by the order of the blocks, independent of the permutations inside them.

For any u in U of degree d>=3, its d incident edge colours are distinct by the proper-colouring hypothesis. Hence changing the order inside E(u) can realize precisely d! different sequences at u. There are only d neighbours of u in V, whose sequences are already fixed. At most d of the d! possibilities equal one of those neighbour sequences. Since d!>d for d>=3, at least one choice avoids every neighbour. Make this selection independently for every u and concatenate the chosen blocks. It leaves all sequences on V unchanged and distinguishes the endpoints of **every** edge, as required. QED.

In particular, every finite simple d-regular bipartite graph with d>=3 is sequentially orderable under every fixed proper edge-colouring. This includes the **bipartite parts of the originally unsolved 2-connected 3-, 4- and 5-regular class-one cases**. It neither proves the full Conjecture 10 for nonbipartite regular graphs nor supplies a counterexample. It also does not use the nonregular/unequal-palette cases already covered by Theorem 5 of the source.

The degree-three assumption is necessary for this *counting proof*, not claimed necessary for sequential orderability of every individual bipartite graph. Proper two-edge-coloured even cycles, excluded by the original conjecture, show a genuine degree-two obstruction.

## Validation, provenance and limits

The standalone stdlib checker at workstreams/A/code/verify_bipartite_block.py independently reconstructs local colour sequences from the final global order and checks 71 explicit graph/colouring instances, including cubic bipartite graphs, regular degrees 4–7, graphs with differing vertex degrees, and arbitrary distinct edge colours. Negative tests reject illegal colourings, invalid vertex partitions, missing/duplicated edges, and deliberately bad all-by-colour orders. Actual stdlib run (Python 3.13): PASS 71 graph/colouring cases; invalid/negative checks PASS.

The script checks **examples**, not all graphs. The preceding full d!>d argument supplies the unrestricted theorem. No independent ROOT acceptance, formal Lean statement, guarantee of historical novelty, external author notification or signed Git transport is claimed. Candidate reservation is recorded separately in CLAIM.md, pending ROOT scope review. No existing main project directories were changed.
