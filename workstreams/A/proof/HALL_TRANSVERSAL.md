# A Hall-theoretic proof of the component-avoiding transversal lemma

**Research status (2026-10-10):** This is a new, independent *proof simplification* of the key component-avoiding transversal from the already-frozen and independently written-PASS Conjecture 10 proof. It is not a new proof of the complete conjecture, not a new original public problem, not Lean-compiled, and not claimed historically novel. The original source paper is Gorzkowska–Kwaśny, *Distinguishing adjacent vertices by ordering edges*, arXiv:2609.11832v1 (2026). Classical Hall's marriage theorem is a standard imported result.

## Theorem — two partitions with all blocks of size at least two

Let X be a nonempty finite set, and let
\[
 X=P_1\sqcup\cdots\sqcup P_k
  =S_1\sqcup\cdots\sqcup S_m
\]
be two set partitions of X. Suppose \(|P_i|\ge2\) for every i and \(|S_j|\ge2\) for every j. Then there exists a set R⊆X such that
\[
  |R\cap P_i|=1\quad(\forall i), \qquad
  S_j\nsubseteq R\quad(\forall j).
\]
The proof is constructive by bipartite matching and needs no graph structure whatsoever.

**Proof.** For each \(P_i\) choose exactly two distinct candidates \(a_i,b_i\in P_i\). Let \(D=\{a_i,b_i:1\le i\le k\}\). Call an \(S_j\) *dangerous* if \(S_j\subseteq D\) **and** \(S_j\) intersects each candidate pair \(\{a_i,b_i\}\) in at most one element. Every other \(S_j\) is *safe*: either it contains a noncandidate (which will never be selected), or it contains both candidates of some \(P_i\) (of which exactly one will be selected). Consequently every safe block is automatically not contained in the final transversal.

Construct a bipartite incidence graph with left vertices the dangerous blocks \(S_j\), right vertices the indices i of the \(P_i\), and an edge \(j\sim i\) when \(S_j\) contains one of \(\{a_i,b_i\}\).

For any subset J of dangerous left vertices, \(|S_j|\ge2\) and the \(S_j\)'s are pairwise disjoint, so
\[
  2|J|\le\sum_{j\in J}|S_j|
       =\Bigl|\bigcup_{j\in J}S_j\Bigr|.
\]
Each candidate pair contains just two elements, and **every vertex of a dangerous block belongs to some candidate pair**, hence
\[
  \Bigl|\bigcup_{j\in J}S_j\Bigr|
  \le2\,|N(J)|,
\]
where \(N(J)\) is the set of right-neighbour indices. Combining these gives \(|J|\le|N(J)|\) for every J. Hall's marriage theorem therefore provides a matching saturating **all dangerous blocks**; let \(i(j)\) be the distinct \(P\)-index assigned to \(S_j\).

For each matched index \(i(j)\), choose the candidate of its pair **outside** \(S_j\). This is possible because \(S_j\) is dangerous and hence contains at most one candidate of each pair. No \(P_i\) is assigned to two dangerous blocks, so these choices are consistent. Choose an arbitrary candidate in each remaining \(P_i\). Let R be the resulting set of exactly one candidate per \(P_i\). A matched dangerous block is missing the candidate from its matched pair that belonged to it; a safe block was already automatically protected. Thus no \(S_j\) is contained in R. QED.

**Sharpness of hypotheses:** If the P partition is \(\{\{0\},\{1\}\}\) and S is \(\{\{0,1\}\}\), the only possible transversal saturates its S block. If P is \(\{\{0,1\}\}\) and S is \(\{\{0\},\{1\}\}\), every transversal saturates one S singleton. Hence neither minimum block-size condition can be discarded in general.

## Original graph-theoretic corollary

Let Q be a finite simple graph **without isolated vertices**, and partition its vertices into any blocks \(P_i\) of size at least two. Take the second partition to be the vertex sets of Q's connected components. Because Q has no isolates, every connected component has at least two vertices. The theorem gives exactly the component-avoiding transversal required as **Lemma 1** of the frozen complete Conjecture 10 proof.

This proof avoids *all* auxiliary multigraph orientation, including its parallel-edge 2-cycle and loop cases, and therefore presents a shorter formalization interface. It **does not change** the root-order lemma or the final single-global-order argument. The original proof's linear-time multigraph orientation is still valuable: bipartite matching in this Hall-based alternative is polynomial-time but does not establish the original linear-time algorithm bound.

## Independent executable witness and exact tests

The standalone \`workstreams/A/code/hall_transversal.py\` chooses candidates, identifies dangerous S-blocks, finds an augmenting-path matching saturating them, and reconstructs a certificate R. It does **not import** the original \`verify_all_regular.py\` orientation code.

Run \`python3 workstreams/A/code/verify_hall_transversal.py\` from the repository root using Python 3.13.5 and only the standard library. Actually checked:

- ALL pairs of partitions with blocks of size at least two for n=2,3,...,8, plus larger fixed-seed partitions: **541,389** tested pairs;
- an independent brute-force existence check for every tested n≤6 case;
- a 2-cycle incidence example \(P=\{\{0,2\},\{1,3\}\}\), \(S=\{\{0,1\},\{2,3\}\}\);
- loop/safe-component boundary examples; four invalid-hypothesis negative tests.

Actual result: \`PASS all two-partition pairs n=2..8 and larger deterministic checks: 541389 pairs; dangerous cases 314852, multicomponent cases 121720; parallel/safe/invalid controls PASS\`.

The infinite theorem relies on the Hall count, **not** the finite tests. The standard Hall theorem is imported with attribution. This packet is pending independent ROOT review and any Lean/formal kernel acceptance.
