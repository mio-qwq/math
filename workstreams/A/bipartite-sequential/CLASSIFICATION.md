# Complete classification for connected bipartite graphs

**Exact source and provenance:** Aleksandra Gorzkowska and Jakub Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026), Corollary 6 (all connected nonregular graphs), Theorem 5 (one adjacent palette difference suffices), and Section 4 (the two exceptional 2-edge-coloured even cycles). https://arxiv.org/html/2609.11832v1 . The **new step relative to those results** is precisely the worker-owned positive degree>=3 bipartite block theorem in PROOF.md. This is a conditional attribution to the source theorems, not a claim of global historical priority.

**Theorem (complete connected bipartite classification).** Let G be a finite, connected, simple **bipartite** graph with at least one edge, and w be any **fixed proper edge-colouring**, using any number of colours. There exists a total order of E(G) such that the induced ordered incident-colour sequences differ at every edge **if and only if** neither of the following holds:

1. G=K2;
2. G is an even cycle and w uses exactly two colours.

Proof. If G is not regular, source Corollary 6 gives sequential orderability for every proper colouring. Otherwise G is connected regular bipartite of degree d>=1. At d=1, G=K2, whose endpoints always have identical length-one sequences. At d=2, G is an even cycle. If w uses only two colours, source Section 4 proves impossibility by considering the first edge in an arbitrary total order: its endpoints see the same two colours in the same order. If w uses three or more colours, some adjacent vertices have distinct incident palettes: otherwise connectivity would force one identical two-element palette throughout G, contradicting the use of at least three colours. Source Theorem 5 gives orderability. At d>=3, the block theorem of PROOF.md supplies the global order for every w. All cases are exhaustive. QED.

This answers **all bipartite instances** of original Conjecture 10, including 2-connected cubic, quartic and quintic bipartite graphs, and identifies the precise colouring-dependent exception on even cycles. The general Conjecture 10 for nonbipartite connected d-regular class-one graphs with d=3,4,5 is still unresolved by this work. No contradiction of the original conjecture, no additional colours, no change of vertex/edge quantifiers, no Lean, no independent ROOT acceptance or historical originality certification are asserted.

Reproduction: proof PROOF.md and algorithm ALGORITHM.md; checker commands in HANDOFF.md. Only the degree>=3 bipartite statement is newly established in this worker packet; the other cases rely **explicitly** on the cited source Corollary 6, Theorem 5 and Section 4.
