# Packing literature gate, 2026-10-10 UTC

## Recommendation
Proceed with a structural all-length proof, especially mixed/odd connector lengths and a reduction covering the entire conjectured graph class. No primary source located in this pass resolves the full conjecture or proves the entire unrestricted square-chain/necklace family. This is a scoped negative search result, not a novelty certificate. Do not advertise the all-even opposite-port subclass as new: it follows from existing super-subdivision results.

## Exact target and source version
Primary source: https://arxiv.org/html/2603.25113v1 ; version ledger https://arxiv.org/abs/2603.25113 . The ledger shows v1 only, submitted 26 March 2026 at 07:38:59 UTC. Section 5 Conjecture 1 asserts chi_rho(G)<=4 for 0-saturated subcubic G with g_3(G)<=4. Section 1 specifies finite, simple, undirected graphs; subcubic means maximum degree at most 3; saturation means at most k degree-3 neighbors per degree-3 vertex. No connectedness, minimum degree, planarity, or bipartiteness assumption appears in the conjecture. Local girth is infinity off all cycles, and g_3 is the maximum over degree-3 vertices. Thus each degree-3 vertex must belong to a triangle or quadrilateral. The empty maximum is not explicitly settled; handle components of maximum degree 2 separately. Theorem 1 gives (1,2,2,3) and a six-color ordinary packing bound, not the target four-color bound.

Source caveats: the introduction's claimed equivalent condition of 3-k degree-2 neighbors omits possible leaves; rely on the actual saturation definition. The prose following the maximum definition is also imprecise; use the displayed maximum. These are observed wording issues, not a located author erratum.

## Later author work and version checks
- https://arxiv.org/abs/2608.02566 and https://arxiv.org/html/2608.02566v1 . Mortada, El Zein, Al Hajjar, submitted 3 August 2026; ledger shows v1. Proves claw-free subcubic (1,1,2,3)-colorability and (1,1,3,3,3) except a specified connected exception. It cites 2603.25113 and settles the separate claw-free conjecture, not its Conjecture 1. Distinguish color-sequence length from ordinary packing chromatic number.
- https://arxiv.org/abs/2503.20239 . Current title is Advances on the Packing Coloring Conjectures of Subcubic Graphs; v3, 24 September 2025. Nonregular connected subcubic (1,1,2,2), yielding ordinary packing <=5 after subdivision. This is not ordinary packing <=4 of the original graph.
- https://kalma-lu.com/authors/11/Ayman-EL-ZEIN . Author institutional page accessible; short selected bibliography, no correction or target resolution found. It is not a complete up-to-date publication ledger.
- Author arXiv search links failed to fetch in this pass. Mortada homepage search yielded institutional/social and bibliographic listings, not a comprehensive maintained primary publication page. Togni publication page was discovered at https://o.togni.u-bourgogne.fr/index.php?n=Research.Publications but direct open returned internal error.
- Exact-ID, exact-title, correction, erratum, proof, solved, and counterexample searches found no primary resolution/correction. MathDB and AI summaries were not treated as evidence; a search result conflating older conjectures was ignored.

## Known overlap: super subdivisions
Lemdani, Abbas, Ferme, Packing Chromatic Numbers of Finite Super Subdivisions of Graphs, Filomat 34(10) (2020), 3275–3286, DOI 10.2298/FIL2010275L. Primary publisher PDF: https://web1.pmf.ni.ac.rs/filomat-content/2020/34-10/34-10-9-12153.pdf . Preprint https://arxiv.org/abs/2001.00469 ; direct arXiv PDF fetch failed, publisher PDF succeeded.

Definition: FSSD_m(G) replaces every edge with K_{2,m}. Proposition 2.8 gives chi_rho(FSSD_m(C_n))=3 when n is even and 4 when n is odd, n>=3, m>=1. Proposition 2.1 records subgraph monotonicity. Proposition 2.7 covers bipartite base graphs; use connected nontrivial paths here, rather than its excessively broad literal wording for arbitrary isolated bipartite graphs.

Independent implication for this project: a necklace of q disjoint squares with opposite attachment ports and even connector lengths ell_i is a subgraph of FSSD_2(C_N), N=q+sum_i ell_i/2, provided N>=3. Each square uses a full K_{2,2} replacement; each connector consists of ell_i/2 replacements with one twin deleted. Hence <=4, and <=3 when N is even. Open all-even chains similarly embed in super-subdivided paths and are <=3. This inference assumes the stated disjoint-square opposite-port model; arbitrary attachments or extra branches need separate verification. Odd connector lengths are not covered by this embedding.

## Other adjacent primary results screened
- Gastineau, Holub, Togni: https://arxiv.org/pdf/1703.05023 . Theorem 11 provides <=305 for connected subcubic outerplanar graphs with no internal face and block graph a path; this is a broad upper bound, not four-color duplication.
- Bresar, Gastineau, Togni: https://arxiv.org/abs/1809.05552 , v3 11 April 2020. Gives <=7 for 2-connected bipartite subcubic outerplanar graphs, and separate repeated-entry S-packing bounds. Neither gives the target ordinary <=4.
- Kostochka, Liu: https://par.nsf.gov/servlets/purl/10327485 . Published Discrete Applied Mathematics 302 (2021), 8–15: (1,1,2) for 2-connected subcubic outerplanar graphs and (1,1,2,4) in general. Not ordinary packing <=4.
- https://arxiv.org/abs/2605.03912 . May 2026 cactus critical-graph classification restricted to radius 2 and diameter 2 or 3; no unrestricted all-length theorem.
- A search hit for circular-necklace packing led to https://recentscientific.com/sites/default/files/11839-A-2018.pdf . Inspection showed a domination paper and separate unrelated references, not the sought packing-coloring theorem.

## Investment gate
1. Credit/reuse the existing even-connector result rather than spending proof effort rediscovering it.
2. Prove genuinely uniform odd/mixed-connector closure and endpoint conditions; finite SAT evidence alone is not this theorem.
3. Keep the family theorem separate from the full conjecture until a complete structural reduction handles triangles, overlapping short cycles, leaves, degree-2 tails and disconnected graphs.
4. Before any novelty/publication claim, run citation-database and author-page checks again; this read-only gate establishes reasonable research value, not exhaustive novelty.

No contacts, repository actions, other-team artifacts, or concrete other-team research sequences were used.
