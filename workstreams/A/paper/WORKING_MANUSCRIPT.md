# A constructive solution candidate to the sequential edge-ordering conjecture

*Working mathematical manuscript — 10 October 2026. For independent review; not an accepted theorem, journal publication, priority assertion or Lean-verified proof.*

## Abstract

Given a proper edge colouring of a finite graph, order the edges globally and record, at each vertex, the colours of incident edges in that order. Gorzkowska and Kwaśny conjectured that every connected simple graph other than the single edge or a properly two-coloured even cycle admits a global ordering in which adjacent vertices have different sequences. We present a deterministic constructive argument for the full conjecture. The new ingredient is a component-avoiding transversal: given a graph without isolated vertices partitioned into parts of size at least two, one may select one vertex per part without completely selecting any connected component. We prove this by orienting an auxiliary multigraph and use a forest ordering of the chosen vertices to orient additional edge insertions. The resulting construction handles every fixed properly d-edge-coloured d-regular graph for d at least three. Combining this with the distinct-palette theorem of the original authors gives the claimed full generality. Three independent exact finite tests support the proof but are not substitutes for independent proof review or formal verification.

**Keywords:** edge order; proper edge colouring; vertex-colour sequence; connected component transversal; constructive graph theory.

## 1. Research scope and attribution

The fixed-colouring, one-global-order problem is Conjecture 10 of A. Gorzkowska and J. Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026). Their Theorem 5 proves the case of adjacent vertices with distinct colour palettes; their Theorem 9 addresses regular degree at least six by the probabilistic local lemma. Both are their prior results. The statements and proofs below are a new working contribution within distributed research project \`mio-qwq/math\`; assignment of conventional authorship and mathematical originality awaits provenance and independent review. This draft was prepared with AI assistance.

We distinguish three validation levels: (a) a deductive proof written below; (b) computer regression tests against the *original* definition; (c) independent mathematical acceptance, which has **not yet occurred** for the complete theorem. No new axioms, Lean proof, peer-reviewed status, theorem acceptance by the coordinating agent or claim of first discovery is asserted.

## 2. Definitions and exact conjecture

Let \(G=(V,E)\) be finite and simple, and let \(w:E\to\mathcal C\) be a **fixed proper edge colouring**. For a total order \(\prec\) of all edges and \(v\in V\), write

\[
s_{\prec,w}(v) = (w(e_1),\ldots,w(e_{d(v)})),
\qquad e_1\prec\cdots\prec e_{d(v)}
\]

where \(e_1,\ldots,e_{d(v)}\) are exactly the edges incident with \(v\). The colouring is *sequentially orderable* if some total \(\prec\) has \(s_{\prec,w}(u)\ne s_{\prec,w}(v)\) for every \(uv\in E\). The proof never alters \(w\), and different vertices are not allowed separate edge orders.

**Conjecture (Gorzkowska–Kwaśny, Conjecture 10).** Every proper edge colouring of every finite connected simple graph other than \(K_2\) or an even cycle is sequentially orderable.

**Proposed main theorem.** This conjecture holds. Specifically, for every finite simple \(d\)-regular graph with \(d\ge3\) and every proper colouring using exactly \(d\) colours, a polynomial-time construction outputs the required single global order.

The next sections reproduce the complete frozen mathematical proof, rather than merely summarize an algorithm or its tests.

---

## 3. Component-avoiding transversal

Let `Q` be a finite simple graph **without isolated vertices**, and let its vertices be partitioned into nonempty parts `C_1,...,C_k`, each containing **at least two vertices**. Then one can select one vertex from each part to form a set `R` such that **no connected component of Q is entirely contained in R**. Moreover, the set can be found by a finite constructive algorithm.

**Proof.** In each part `C_i`, choose any two distinct candidates `a_i,b_i`. Write `P={a_i,b_i : 1<=i<=k}` and let `S_1,...,S_t` be the vertex sets of the connected components of `Q`. Form a *multigraph* `T` with vertices `1,...,t` and one edge `i` from the component containing `a_i` to that containing `b_i`. Loop edges are allowed.

Call a vertex `j` of `T` **dangerous** if (i) every vertex in `S_j` belongs to `P`, and (ii) `S_j` contains *at most one* of the candidates from any single part `C_i`. All other component vertices of `T` are **safe**: irrespective of which candidate per part is eventually selected, a safe `S_j` will have at least one vertex outside the selection (either a noncandidate, or one of two candidates from the same part).

For any dangerous vertex `j`, every vertex of `S_j` contributes an incident edge of `T`, and distinct vertices of `S_j` come from **different** parts. Therefore the degree of `j` in `T`, counted with multiplicity, is exactly `|S_j|`. Since `Q` has no isolated vertices, `|S_j|>=2`. Thus every dangerous vertex of `T` has degree at least two and no loop.

Orient `T` so that every dangerous vertex has an **outgoing** edge. This is possible in each connected component: if it contains a safe vertex, orient a spanning tree towards that safe vertex; every other vertex has an outgoing tree edge. If the connected component contains *only* dangerous vertices, all its vertices have degree at least two, so it contains an undirected cycle (possibly a 2-cycle formed by parallel edges). Orient that cycle cyclically, and orient a spanning forest of the remaining vertices towards the cycle. Orient all still-unoriented edges arbitrarily. In either case each dangerous vertex has an outgoing edge.

For each original part `C_i`, choose the candidate `a_i` or `b_i` at the **head** of edge `i` of `T` (for a loop choose either). The selection `R` is a transversal. For each dangerous `S_j`, an edge of `T` is oriented *out of j*, so the corresponding candidate in `S_j` was not selected. For each safe `S_j`, the previous paragraph already guarantees an unselected vertex. Hence no `S_j` is contained in `R`. QED.

*The condition "without isolated vertices" is necessary for the lemma as stated: if Q is edgeless, any chosen root itself is a full Q-component.*

## 4. Ordering chosen roots

Let `R` satisfy Lemma 1 for `Q`. Each connected component of the induced graph `Q[R]` has a vertex with a neighbour in `V(Q)\R`: otherwise that component would itself be a whole connected component of `Q`, contradicting Lemma 1. In each `Q[R]` component choose such a **boundary root** `r`, choose a spanning tree rooted at `r`, and list all vertices **child before parent**. Concatenate the lists from different components arbitrarily.

Every selected root `x` is then either a boundary root with a neighbour in `V(Q)\R`, or has a neighbour **later** in the root ordering (its parent). Thus if a Q-edge is assigned to its root endpoint when exactly one endpoint is in `R`, or to its **earlier** root endpoint when both are in `R`, then **every root is assigned at least one Q-edge**. QED.

## 5. The global edge-order construction

Let `d>=3`. Let `G` be a finite simple (possibly disconnected) **d-regular graph** and let `w` be a fixed proper edge colouring using **exactly d colours**. Then there exists a single total edge order making the induced incident-colour sequences different across every edge of `G`. Such an order is constructible in polynomial time.

**Proof.** Relabel the d colours `0,1,...,d-1`. At every vertex exactly one edge of each colour occurs. The edges of colours `0` and `1` form a spanning disjoint union of alternating **even cycles**, `C_1,...,C_k`. Since `G` is simple their lengths are all at least four. Let `Q` be the spanning subgraph whose edges have colours `2,...,d-1`; it is `(d-2)`-regular and therefore has **no isolated vertices**.

Apply Lemma 1 to the partition `(C_i)` of `V(G)` to select one **root** `r_i` on each cycle, avoiding complete connected Q-components. Apply Lemma 2 to obtain a total order of these roots in which **each root has at least one incident Q-edge either to a nonroot or to a later root**. Order the corresponding cycles in this root order.

For each cycle, rotate and choose its orientation so that its chosen root is `v_0` and the outgoing edge `e_0=v_0v_1` has colour `0`. Then list the cycle edges consecutively as

    e_0, e_1, ..., e_{m-1},

where `e_j=v_j v_{j+1}` for `0<=j<m-1` and `e_{m-1}=v_{m-1}v_0`. These edges alternate in colours `0,1,0,1,...,1`. Concatenate these ordered cycle-edge blocks according to the root order.

Assign every edge `xy` of `Q` to a designated endpoint: if exactly one of `x,y` is a root, designate that root; if both are roots, designate the earlier one in root order; otherwise designate the earlier endpoint in the lexicographic order `(cycle block, index j)`. For each designated endpoint `v_j`, insert the assigned edge **just after its outgoing cycle edge `e_j`**; if several Q-edges are designated to the same vertex, sort them by their (distinct) colours. This gives one unambiguous **global total order** `≺` of *all* edges; each Q-edge is inserted once and every cycle edge once.

We verify the induced sequences `f` directly.

1. **Root signature.** For each root `v_0`, its cycle edges occur as colour `0` then colour `1`. Every Q-edge assigned to that root is inserted after `e_0`, between these two cycle edges. Any Q-edge incident to the root but assigned elsewhere must be assigned to an *earlier* root in another cycle, hence appears before `e_0`. By Lemma 2, at least one Q-edge is assigned to every root. Consequently **colours 0 and 1 are not adjacent** in `f(v_0)`.

2. **Nonroot signature.** For every nonroot `v_j` (`1<=j<m`) its two incident cycle edges are `e_{j-1}<e_j`. A Q-edge assigned at `v_j` is inserted after `e_j`. An edge assigned in another cycle lies wholly before or after this cycle's block. An edge assigned at an earlier vertex `v_i` of the *same* cycle has `i<=j-2`, since an edge `v_{j-1}v_j` already exists in the alternating cycle and G is simple; therefore that Q-edge is inserted before `e_{j-1}`. This includes Q-edges assigned to the root `v_0`. So no Q-edge of `v_j` appears between `e_{j-1}` and `e_j`: **colours 0 and 1 are adjacent** in `f(v_j)`.

3. **Cycle edges.** Any colour-0/1 edge incident to a root has unequal endpoint sequences by (1)–(2). Every other cycle edge joins two consecutive nonroots `v_j,v_{j+1}` whose relative orders of colours `0` and `1` are **opposite** (because of the alternating cycle), so their sequences differ as well.

4. **Leftover-colour edges.** If a Q-edge joins a root to a nonroot, its endpoints are different by (1)–(2). If a Q-edge joins two roots, it is assigned to the earlier root: its particular colour occurs **between 0 and 1** at the earlier root, but **before both 0 and 1** at the later root (as the earlier cycle block precedes the later). If a Q-edge joins two nonroots, it is assigned to the earlier endpoint in lexicographic cycle order. Its particular colour is **after both 0 and 1** at the earlier endpoint, but **before both 0 and 1** at the later endpoint; within one cycle the endpoints are not consecutive, since G is simple and Q-edges are not cycle edges. Thus the two sequences differ in every case.

Every edge of `G` has colour either `0,1` or in `Q`, so all edges are distinguished. The argument never modifies `w`. Constructing connected components, spanning trees, auxiliary graph orientations and the edge order requires only polynomial time (sorting insertion slots by colour gives an elementary polynomial bound). QED.

## 6. Proof of the original conjecture

Let `G` be a finite **connected** simple graph other than `K_2` or an even cycle, and `w` any fixed proper edge colouring. If `G` is nonregular, the **published Theorem 5 / Corollary 6** of Gorzkowska–Kwaśny already gives a good order. If `G` is regular of degree `d>=3`, either (i) there are adjacent vertices with distinct colour palettes, in which case their published Theorem 5 applies, or (ii) every edge joins equal palettes; connectedness implies *all* vertex palettes coincide, consisting of exactly `d` colours, and Theorem 3 applies after relabelling those colours. Degree `1` gives precisely `K_2`; degree `2` gives a cycle, and the original paper explains that any proper colouring of a cycle with at least three colours has adjacent unequal palettes, whereas even cycles coloured by only two alternating colours are the genuine excluded obstruction. `K_1` (if included in the convention) has no edge to distinguish and is vacuous. Therefore the original **Conjecture 10 holds as stated**. QED.

## 7. Exact tests and the independent-review boundary

Three executable standard-library checks, all separately constructed from the original definitions:

- `python3 workstreams/A/code/verify_all_regular.py`: constructs orders across d=3,4,5,6,7,9 and complete graphs d=5,7,9; the actual run in Python 3.13.5 passed **4,042** distinct finite randomly seeded instances, spanning **50** parameter cases, plus deliberately omitted-edge negative test.
- `python3 workstreams/A/code/verify_d5_exhaustive.py`: exhausts all ordered triples of disjoint perfect matchings completing the fixed two-colour factors on eight vertices, for factor partitions `(8,)` and `(4,4)`; actual run passed **2,502 + 3,096 = 5,598** fully checked five-colour regular instances.
- `python3 workstreams/A/code/verify_component_transversal.py`: independently brute-checks the root-avoidance lemma on all labelled simple graphs on 6 vertices with no isolated vertices and a fixed partition into three pairs; verifies the returned root set avoids every original Q-component, and checks the isolated-vertex counterexample to the necessity of the hypothesis. Report actual invocation/results in `STATUS.md`.

The finite checks are corroboration **not a substitute** for Lemma 1, Lemma 2, Theorem 3 and Corollary 4. The exact source/commit SHA and execution receipts must be frozen before external acceptance. In particular, no claim of Lean-checked semantics, anonymous peer review, journal publication, external mathematical acceptance or historical world firstness is made. A separate ROOT reviewer should check the two-candidate multigraph orientation in Lemma 1, root ordering in Lemma 2, each of the six endpoint cases in Theorem 3, original source quantifiers and possible prior results without presupposing this proof is correct.


## 8. Source and reproducibility

**Original research statement.** A. Gorzkowska and J. Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (2026), https://arxiv.org/html/2609.11832v1 .

**Unaltered proof freeze.** \`workstreams/A/bipartite-sequential/ALL_DEGREES_THEOREM.md\`; Git blob \`84ab0860bb1fe9ca0812225bb01227f5b6d63d13\`; commit \`7168f6df66ba5518cd3420c4668eab5352e4be8c\`. The edited presentation in this working manuscript is NOT the immutable reviewed object.

**Source-based checks.** \`workstreams/A/code/verify_all_regular.py\`, \`verify_d5_exhaustive.py\`, and \`verify_component_transversal.py\`. The frozen Git blobs are \`dfd147219f4fb016e945daabfffea9bbe419919d\`, \`3106840ac93fbe3d5bbf2f35dcdbd7dd23134081\`, and \`5dae7d46b8830c21fcc328b4b8dc73ebe9bb2de1\`, respectively.

**Boundary of prior-art review.** A targeted review on 10 October 2026 of the original arXiv record, author listing, and recent topic searches did not find a same-scope subsequent proof. This is NOT a proof of historical novelty or a licence to claim priority. A renewed literature and referee review is required before any posting or submission.

**Open validation tasks.** Have an uninvolved reviewer reconstruct the auxiliary multigraph's loop/parallel-edge cases, the spanning-forest root order, and each equality-avoidance case from the original problem. Formalize the selected transversal lemma and the actual ordered-edge-list semantics in Lean with compiler/axiom receipts. These are required research follow-ups, not already-completed milestones.
