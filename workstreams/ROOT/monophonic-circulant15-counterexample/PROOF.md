# Order 15 disproves the circulant monophonic-position existence conjecture

Complete mathematical exclusion, with an original-definition Lean proof.

## Original statement and exact negation

James Tuite, Elias John Thomas, and Ullas Chandran S.V., *On some extremal position problems for graphs*, Ars Mathematica Contemporanea 25(1) (2025), #P1.09, Section 4, Conjecture 4.5, printed page 17; DOI [10.26493/1855-3974.3094.bc6](https://doi.org/10.26493/1855-3974.3094.bc6). [Final primary PDF](https://oro.open.ac.uk/92086/13/92086final.pdf); preprint arXiv:2106.06827v3, 8 February 2022. The published statement and original definitions were reread on 10 October 2026.

The conjecture asserts that every integer n >= 11 is the order of a simple undirected circulant graph with diameter 2 and monophonic position number 2. A monophonic position set meets every induced path in at most two vertices; mp(G) is its maximum cardinality.

**Theorem. No simple undirected circulant graph of order 15 has both diameter 2 and mp(G) = 2.**

The counterexample object is the admissible integer **n = 15**, together with a complete exclusion of all circulants at that order. Giving a single unsuccessful graph would not refute the existential conjecture. The source's Theorem 4.4 about arbitrary graphs, without the circulant restriction, is unaffected.

## 1. Complete representation and two obstructions

Every order-15 circulant admits a labeling by Z/15Z under which x and y are adjacent exactly when y-x belongs to S, for an inverse-closed subset S of the nonzero residues. There is no nonzero self-inverse residue. Thus S = P union (-P) for a unique subset P of {1,2,3,4,5,6,7}. This gives all 128 possible connection sets, without needing to identify isomorphic presentations.

If G contains a triangle, its three vertices form a monophonic position set: an induced path cannot contain all three, since its induced subgraphs contain no triangle. Hence mp(G)=2 requires triangle-freeness. In the circulant representation, a triangle exists exactly when some a,b in S satisfy a+b in S, modulo 15. Indeed 0,a,a+b are distinct and form a triangle; conversely translate one triangle vertex to zero.

A second obstruction is a set of three independent vertices with identical open neighborhoods (false twins). Such a triple is a monophonic position set. To see this, suppose an induced path contains all three and choose the one that occurs between the other two along the path. One of its path neighbors is adjacent to all three twins. Those twins are distinct from that neighbor and belong to the induced path, giving degree at least three within the path, a contradiction.

## 2. Elementary classification of all triangle-free possibilities

Triangle-freeness forbids the following subsets of positive generators:

- {5}: 5+5=10=-5.
- {1,2}: 1+1=2.
- {1,7}: 1+7=8=-7.
- {2,4}: 2+2=4.
- {3,6}: 3+3=6.
- {4,7}: 4+4=8=-7.
- {1,3,4}: 1+3=4.
- {2,6,7}: 2+6=8=-7.

All equalities are modulo 15. These necessary restrictions already give the entire list of possibilities. The four forbidden pairs involving {1,2,4,7} are precisely all cross pairs between {1,4} and {2,7}. Consequently P uses at most one of those two parts, together with at most one of {3,6}; it never uses 5. It has at most three elements. The two forbidden triples then leave only **{1,4,6} and {2,3,7}** at size three. The allowed size-two sets are precisely

    {1,3}, {3,4}, {2,6}, {6,7},
    {1,4}, {1,6}, {4,6}, {2,3}, {2,7}, {3,7}.

The remaining possibilities are the empty set and the six singletons other than {5}. Thus every triangle-free connection set is among 1+6+10+2=19 explicitly described sets. Direct sum checking shows these 19 are indeed triangle-free, but only the exhaustive necessary implication is needed below.

## 3. Diameter excludes every set of size at most two

Vertices reachable from 0 in at most two steps lie in R = {0} union S union (S+S). If |P| <= 1, this set has at most five elements, so the graph cannot have diameter 2 on 15 vertices.

For the ten possible pairs, the following table gives the exact complement of R. Every row is nonempty. This table is verified by the four generators +/-p,+/-q and their sixteen ordered sums, so requires no graph search or unproved classification.

| P | Residues not reachable from 0 in at most two steps |
|---|---|
| {1,3} | 5,7,8,10 |
| {3,4} | 2,5,10,13 |
| {2,6} | 1,5,10,14 |
| {6,7} | 4,5,10,11 |
| {1,4} | 6,9 |
| {1,6} | 4,11 |
| {4,6} | 1,14 |
| {2,3} | 7,8 |
| {2,7} | 3,12 |
| {3,7} | 2,13 |

## 4. Both remaining sets have a forbidden false-twin triple

For P={1,4,6}, S={1,4,6,9,11,14}. For P={2,3,7}, S={2,3,7,8,12,13}. In each case S+5=S modulo 15. Therefore the distinct vertices 0,5,10 have identical open neighborhoods S. They are independent because neither 5 nor 10 belongs to S. Section 1 proves that {0,5,10} is a monophonic position set, and hence mp(G)>=3.

These graphs actually are the independent-three-vertex blow-up of a 5-cycle: group vertices by residue modulo 5, with adjacent classes differing by +/-1 in the first case and +/-2 in the second. In particular both have diameter 2. This description is not needed to infer mp>=3.

Every order-15 circulant either has a triangle, fails diameter 2, or is one of these two graphs with mp>=3. Since 15>=11, this disproves the exact printed Conjecture 4.5. QED.


## Formal verification and provenance

The mathematical argument above is reproduced from the [frozen distributed proof](https://github.com/mio-qwq/math/blob/6022d2bcb52324f834028e21c458e0f890e23d14/workstreams/B/monophonic_circulants/COUNTEREXAMPLE_PROOF.md). Its two Python verifiers and historical run logs remain at that frozen source; no old run is presented as a new independent execution.

The [Lean source](MonophonicCirculant15.lean) quantifies over every actual mathlib simple chordless walk, without restricting induced-path length. It proves the maximum-cardinality semantics, the general open-twin obstruction, the complete 128-presentation kernel classification, and the coverage of arbitrary connection sets and vertex labels. The final `MonophonicCirculant15.not_originalConjecture45` negates the original all-orders existence statement using n=15. The exact compiled bytes and seven axiom audits are in [lean-audit.json](lean-audit.json) and [lean-audit.log](lean-audit.log).

No minimum counterexample order, classification of other orders, exact survivor mp value, human peer review or historical priority is claimed. Mathematical derivation, formalization and writing used AI assistance; AI systems are not paper authors.
