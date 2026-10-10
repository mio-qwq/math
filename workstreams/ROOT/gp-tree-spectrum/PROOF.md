# Constructive proof

Let D be an orientation of a finite forest. A set S is in directed general position if every shortest directed path between two vertices of S has no third vertex of S. Unreachable ordered pairs impose no condition.

## Rank characterization

A walk following an orientation of a forest cannot repeat a vertex: any repetition in a forest forces immediate backtracking, which would use both directions of an edge. Every directed simple path is also shortest, since the underlying undirected simple path is unique.

Thus S is GP exactly when every directed walk contains at most two selected vertices. If a walk contained three, truncate to its first and last selected vertices to contradict GP; the reverse implication is immediate. Define y(v) to be the maximum number of selected vertices on a directed walk ending at v, counting both endpoints. The zero-length walk supplies a witness, and all counts are at most two. Write chi(v)=1 for a selected vertex and zero otherwise. Then

    chi(v) <= y(v) <= 2,
    y(u) + chi(v) <= y(v) for every arc u -> v.

Conversely these inequalities telescope along every actual walk and bound its selected count by two. This equivalence uses undirected acyclicity; it does not extend merely from that assumption to every directed acyclic graph.

## Add a leaf constructively

Attach a new selected leaf ell to an old vertex p and retain all old labels. If y(p)<=1, choose p->ell and y(ell)=y(p)+1. If y(p)=2, choose ell->p and y(ell)=1. The only new arc inequality holds in either case. Therefore every old GP set extends by the new leaf in at least one of the two directions.

For any fixed leaf orientation, a GP set restricts to a core GP set and loses at most one vertex. Conversely every core GP set lifts with the leaf unselected: give the leaf label y(p) for p->ell and zero for ell->p. Hence, if the old GP maximum is m, every extension has maximum m or m+1. Extending an old maximum set in the successful selected-leaf direction gives exactly m+1, because the matching upper bound is m+1.

## Interval induction on actual trees

If the core spectrum is [L,U], every integer in [L+1,U+1] occurs in the enlarged spectrum, and every enlarged value lies in [L,U+1]. Its only optional integer is L. The new spectrum is therefore [L,U+1] or [L+1,U+1].

The singleton tree has spectrum {1}. Every finite non-singleton tree has a genuine degree-one vertex; its actual induced deletion remains a tree. The original tree is isomorphic to the Option-type leaf extension of this smaller induced tree. Transporting all orientations, actual paths, competing shortest paths and GP maximum cardinalities across that graph isomorphism preserves its spectrum. Strong induction on the actual vertex cardinality now proves the theorem for every finite tree.

## Forest corollary, paper scope

Different connected components admit no paths between them. The GP maximum of a disjoint union is the sum of the component GP maxima, for each independently chosen orientation. Its spectrum is the Minkowski sum of their spectra. Sums of integer intervals are integer intervals; the empty forest has spectrum {0}. This proves the forest corollary on paper. The standalone Lean file formalizes the forest rank characterization and the entire finite-tree theorem, but has no final component-sum forest-spectrum theorem.

## Relationship to the public problem

The target is [Chandran et al., arXiv:2604.15909v1](https://arxiv.org/html/2604.15909v1), Definitions 2.1 and 4.2, Conjecture 4.30 in section 4.2. Its Theorems 4.23/4.24 cover spiders/caterpillars, not all finite trees. The later [author survey, arXiv:2501.19385v5](https://arxiv.org/html/2501.19385v5), section 5.6, Conjecture 5.63 still poses the general interval question. These are bounded source observations, not proof of historical priority. This is an affirmative tree result, not a counterexample to the arbitrary-graph conjecture.
