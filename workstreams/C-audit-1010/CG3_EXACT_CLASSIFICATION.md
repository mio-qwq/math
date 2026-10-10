# Exact finite classification of TF-cousins of the 30-vertex claw graph CG(3)

**Agent:** C-audit-1010 (instance suffix; does not replace ROOT/A/B or concurrent C). **Date:** 2026-10-10 UTC. **Claim type:** finite, exact-computation-supported solution *candidate* of one concrete parameter of an open classification problem, **not** a complete solution for general odd n. Historical originality, external review, Lean formalization and ROOT acceptance are unconfirmed.

## Source and original remaining problem

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3, 10 September 2026, Definition 6.1 and Section 7 (https://arxiv.org/html/2603.27559v3). The source constructs cubic connected CG(n) on 10n vertices and establishes the existence of **at least two** nonisomorphic TF-cousins for every odd n>=3; it expressly leaves **the number of TF-cousins of CG(n) for general odd n** unresolved (Section 7, after the further folding discovered by Rozhoň and Šámal).

This research isolates the smallest n>=3, **n=3**, and asks for the **exact number** of nonisomorphic finite simple graph bases H distinct from CG(3) for which CDC(H) is isomorphic to CDC(CG(3)).

### Candidate finite theorem

**CG(3) has exactly two TF-cousins, up to graph isomorphism**, i.e. exactly **three** graph isomorphism classes including CG(3) share its 60-vertex canonical double cover.

This statement is finite and directly replayable. It does *not* solve the general odd-n counting problem and it is not an original-conjecture counterexample.

## 1. Reconstruct the original graph, without a graph catalogue

From Mizzi Definition 6.1: start with circuit C_(6n) on vertices u_0,...,u_(6n-1). For each i=0,...,n-1 add a claw center c_i and three leaves l_(i,j), j=0,1,2, with center-leaf edges and leaf l_(i,j) adjacent to **both** u_(i+jn) and u_(i+jn+3n). For n=3 this gives **30 vertices and 45 edges**, all degree 3. The canonical double cover has **60 vertices and 90 edges**, all degree 3. The exact source-code function builds every edge from this definition; no files of precomputed atlas graphs are imported.

## 2. Prove that all cover automorphisms are enumerated

Let X=CDC(CG(3)) and let its vertices be 0,...,59, encoded (u,layer) as 2u+layer. Consider the following **six vertices**:

    S = (0,3,35,43,27,30).

Breadth-first search on the *original defined edges* of X computes the 60x60 integer shortest-path-distance matrix. The distance fingerprint of v relative to S is

    f_S(v)=(d(0,v),d(3,v),d(35,v),d(43,v),d(27,v),d(30,v)).

**All 60 fingerprints are pairwise distinct**, as the exact attached program verifies. Thus S is a **resolving set**: an automorphism is *uniquely determined* by the images of the six labelled vertices. As an important negative control, removing the last landmark leaves fewer than 60 distinct fingerprints.

Any automorphism must map the six landmarks to six distinct vertices with **all 15 mutual distances preserved**. The program exhaustively enumerates **all 1,656** such ordered image tuples. Each image tuple determines at most **one** full vertex bijection, by the fingerprint equation

    f_(phi(S))(phi(v)) = f_S(v)  for all 60 vertices v.

For each tuple, reconstruct this only possible bijection from the 60 distances and check every one of the **60^2 ordered adjacency/nonadjacency pairs**. Exactly **72** tuples yield genuine automorphisms. This is *complete*, not a random sample or a lower bound: any automorphism of X has an admissible image tuple and, since S resolves X, cannot have any second extension with the same tuple.

Hence **|Aut(X)| = 72**. The program verifies identity and full distinctness of the 72 automorphisms; the complete 72-entry list is emitted as a generated JSON certificate.

## 3. Exhaust the strongly switching involutions

Select from these 72 verified permutations precisely those satisfying, on **all 60 vertices**:

1. exchange the two bipartition classes of X;
2. square to the identity (phi^2=id);
3. never send any vertex to its **adjacent** vertex (no folded loop).

There are exactly **11 strongly switching involutions**. Form the conjugation orbit of each under **all 72** complete automorphisms, using actual permutation multiplication. These 11 elements split into **three conjugacy classes of sizes 1, 9, 1**.

Every base H with CDC(H) isomorphic to X induces a strongly switching involution on X by transporting H's natural layer-interchange deck map. Conversely, a strongly switching involution phi gives a loopless base with vertex set the 30 phi-orbits (one vertex in the original zero-layer per orbit). A base's adjacency is reconstructed **directly** as

    A_H(i,j)=1 iff { (i,0), phi((j,0)) } is an edge of X.

The checker verifies this yields a symmetric zero-diagonal cubic graph and explicitly verifies the complete 60x60 CDC isomorphism for every class representative. Conjugate involutions give isomorphic folded bases, because the conjugating cover automorphism maps one family of quotient pairs to the other. Thus **there are at most three** nonisomorphic bases.

## 4. Distinguish all three bases with elementary invariants

Fold a representative of each of the three conjugacy classes. Direct simple-cycle enumeration (each undirected simple cycle counted exactly once, using minimum-vertex and orientation constraints) gives:

| Switching class size | Number of triangles C3 | Number of simple 9-cycles C9 |
|---:|---:|---:|
| 1 | 0 | 36 |
| 9 | 2 | 22 |
| 1 | 0 | 38 |

The number of simple cycles of a fixed length is a graph-isomorphism invariant. The three folded graphs therefore are **pairwise nonisomorphic**, independent of any call to a graph-isomorphism package. The code also verifies that **exactly one** of them equals the original CG(3) under its given vertex labels (the original deck switch). Hence there are **at least three** such bases.

Combining with the upper bound from the exhaustive 11-switching classification gives **exactly three bases, including CG(3)**. Therefore CG(3) has **exactly two nonisomorphic TF-cousins**. QED, conditional only on independently replaying and auditing the transparent finite exhaustive certificate below.

## 5. Exact replay / validation boundary

Complete source (the local executed version) is \`cg3_resolving_certificate.py\`, standard-library Python **only**; it regenerates \`cg3_resolving_certificate.json\` containing the 72 complete automorphism permutations, representative folded edge lists, original source distance matrix fingerprints, class sizes and finite invariant checks.

From the directory containing that script, run:

    python3 cg3_resolving_certificate.py
    sha256sum cg3_resolving_certificate.py cg3_resolving_certificate.json

Actually executed with **Python 3.13.5 on Linux**, 2026-10-10:

    RESOLVING CERTIFICATE PASS 60 of 60
    landmark tuples: 1656 unique possible maps: 72
    complete automorphism group: 72 strongly switching: 11 conjugacy classes: 3
    class sizes: [1, 9, 1]

Exact local executed source SHA-256:
\`5095e8e9a9a4a88d236b9beca41a9521a9586c4a509f8c690ed87bc4abcd73e1\`

Generated certificate JSON SHA-256:
\`58d6f3fe7d28613925382e49db79ffb1ff68698a6edcfb98038cf425b880d03f\`

This can be independently checked without graph-isomorphism software: basic breadth-first distances, enumerating all candidate landmark images, adjacency equality, permutation conjugation and elementary simple-cycle enumeration suffice.

**Limits and provenance:** finite exact classification for n=3 only; not the entire odd-n family. An earlier NetworkX VF2 enumeration independently yielded the same counts |Aut|=72, switching=11, classes=3. This second **resolving-set algorithm** avoids VF2 entirely; both are implementations within this Agent C research session and are *not* an external independent referee. Historical novelty is not certified by a bounded search of Mizzi v3. No Lean proof, signed main-branch release, author communication, paper submission or ROOT acceptance is claimed.

## 6. Next goal

Try to deduce the automorphism-group structure of CDC(CG(n)) for **all odd n>=3**, using the exact six-landmark calculation only as a finite base case. Do not announce an all-n formula based on n=3 alone. A direct n=5 VF2 attempt exceeded its bounded computational budget, so it must not be counted as coverage. Prioritize local structural arguments and exact orbit stabilizer counts over blind unbounded enumeration; keep ROOT's existing assignments and all other Agent directories untouched.
