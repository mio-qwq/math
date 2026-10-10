# Constructive affirmative proof of the complete sequential edge-order conjecture

**Research submission — independent acceptance pending.**

**Original public statement.** A. Gorzkowska and J. Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (10 September 2026), **Conjecture 10**, https://arxiv.org/html/2609.11832v1 : every proper edge colouring of a finite connected simple graph other than `K_2` or an even cycle is *sequentially orderable*. With a fixed edge colouring `w`, this means there is one global total order of all edges such that the sequences of incident edge colours, in that edge order, differ at endpoints of every edge. No recolouring is allowed.

The authors' **Theorem 5** already handles a connected graph with an edge joining unequal colour palettes. Their Theorem 9 handles regular degrees >=6. The proof below treats the missing **all regular class-one degrees d>=3**, indeed without a degree upper bound, using elementary graph theory. Combined with their Theorem 5 and cycle discussion, it proves the complete Conjecture 10. It is a *positive proof*, not a counterexample. It has not been independently validated by the coordinating ROOT Agent, peer reviewed, accepted by a journal, or formally compiled in Lean. A bounded source search on 10 October 2026 did not locate another complete proof; this does **not** certify historical novelty.

## Lemma 1: component-avoiding transversal

Let `Q` be a finite simple graph **without isolated vertices**, and let its vertices be partitioned into nonempty parts `C_1,...,C_k`, each containing **at least two vertices**. Then one can select one vertex from each part to form a set `R` such that **no connected component of Q is entirely contained in R**. Moreover, the set can be found by a finite constructive algorithm.

**Proof.** In each part `C_i`, choose any two distinct candidates `a_i,b_i`. Write `P={a_i,b_i : 1<=i<=k}` and let `S_1,...,S_t` be the vertex sets of the connected components of `Q`. Form a *multigraph* `T` with vertices `1,...,t` and one edge `i` from the component containing `a_i` to that containing `b_i`. Loop edges are allowed.

Call a vertex `j` of `T` **dangerous** if (i) every vertex in `S_j` belongs to `P`, and (ii) `S_j` contains *at most one* of the candidates from any single part `C_i`. All other component vertices of `T` are **safe**: irrespective of which candidate per part is eventually selected, a safe `S_j` will have at least one vertex outside the selection (either a noncandidate, or one of two candidates from the same part).

For any dangerous vertex `j`, every vertex of `S_j` contributes an incident edge of `T`, and distinct vertices of `S_j` come from **different** parts. Therefore the degree of `j` in `T`, counted with multiplicity, is exactly `|S_j|`. Since `Q` has no isolated vertices, `|S_j|>=2`. Thus every dangerous vertex of `T` has degree at least two and no loop.

Orient `T` so that every dangerous vertex has an **outgoing** edge. This is possible in each connected component: if it contains a safe vertex, orient a spanning tree towards that safe vertex; every other vertex has an outgoing tree edge. If the connected component contains *only* dangerous vertices, all its vertices have degree at least two, so it contains an undirected cycle (possibly a 2-cycle formed by parallel edges). Orient that cycle cyclically, and orient a spanning forest of the remaining vertices towards the cycle. Orient all still-unoriented edges arbitrarily. In either case each dangerous vertex has an outgoing edge.

For each original part `C_i`, choose the candidate `a_i` or `b_i` at the **head** of edge `i` of `T` (for a loop choose either). The selection `R` is a transversal. For each dangerous `S_j`, an edge of `T` is oriented *out of j*, so the corresponding candidate in `S_j` was not selected. For each safe `S_j`, the previous paragraph already guarantees an unselected vertex. Hence no `S_j` is contained in `R`. QED.

*The condition "without isolated vertices" is necessary for the lemma as stated: if Q is edgeless, any chosen root itself is a full Q-component.*

## Lemma 2: order roots so each owns a leftover-colour edge

Let `R` satisfy Lemma 1 for `Q`. Each connected component of the induced graph `Q[R]` has a vertex with a neighbour in `V(Q)\R`: otherwise that component would itself be a whole connected component of `Q`, contradicting Lemma 1. In each `Q[R]` component choose such a **boundary root** `r`, choose a spanning tree rooted at `r`, and list all vertices **child before parent**. Concatenate the lists from different components arbitrarily.

Every selected root `x` is then either a boundary root with a neighbour in `V(Q)\R`, or has a neighbour **later** in the root ordering (its parent). Thus if a Q-edge is assigned to its root endpoint when exactly one endpoint is in `R`, or to its **earlier** root endpoint when both are in `R`, then **every root is assigned at least one Q-edge**. QED.

## Theorem 3: one good global edge order for every proper d-edge-coloured d-regular graph

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

## Corollary 4: complete Conjecture 10

Let `G` be a finite **connected** simple graph other than `K_2` or an even cycle, and `w` any fixed proper edge colouring. If `G` is nonregular, the **published Theorem 5 / Corollary 6** of Gorzkowska–Kwaśny already gives a good order. If `G` is regular of degree `d>=3`, either (i) there are adjacent vertices with distinct colour palettes, in which case their published Theorem 5 applies, or (ii) every edge joins equal palettes; connectedness implies *all* vertex palettes coincide, consisting of exactly `d` colours, and Theorem 3 applies after relabelling those colours. Degree `1` gives precisely `K_2`; degree `2` gives a cycle, and the original paper explains that any proper colouring of a cycle with at least three colours has adjacent unequal palettes, whereas even cycles coloured by only two alternating colours are the genuine excluded obstruction. `K_1` (if included in the convention) has no edge to distinguish and is vacuous. Therefore the original **Conjecture 10 holds as stated**. QED.

## Exact validation and independent review boundary

Three executable standard-library checks, all separately constructed from the original definitions:

- `python3 workstreams/A/code/verify_all_regular.py`: constructs orders across d=3,4,5,6,7,9 and complete graphs d=5,7,9; the actual run in Python 3.13.5 passed **4,042** generated test runs (not deduplicated by graph isomorphism), spanning **50** parameter cases, plus deliberately omitted-edge negative test.
- `python3 workstreams/A/code/verify_d5_exhaustive.py`: exhausts all ordered triples of disjoint perfect matchings completing the fixed two-colour factors on eight vertices, for factor partitions `(8,)` and `(4,4)`; actual run passed **2,502 + 3,096 = 5,598** fully checked five-colour regular instances.
- `python3 workstreams/A/code/verify_component_transversal.py`: independently brute-checks the root-avoidance lemma on all labelled simple graphs on 6 vertices with no isolated vertices and a fixed partition into three pairs; verifies the returned root set avoids every original Q-component, and checks the isolated-vertex counterexample to the necessity of the hypothesis. Report actual invocation/results in `STATUS.md`.

The finite checks are corroboration **not a substitute** for Lemma 1, Lemma 2, Theorem 3 and Corollary 4. The exact source/commit SHA and execution receipts must be frozen before external acceptance. In particular, no claim of Lean-checked semantics, anonymous peer review, journal publication, external mathematical acceptance or historical world firstness is made. A separate ROOT reviewer should check the two-candidate multigraph orientation in Lemma 1, root ordering in Lemma 2, each of the six endpoint cases in Theorem 3, original source quantifiers and possible prior results without presupposing this proof is correct.
