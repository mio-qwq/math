# Agent C: affirmative proof candidate for Mizzi's first TF-cousin conjecture

**Date:** 10 October 2026 (UTC). **Status:** full written proof candidate; NOT independently accepted, Lean-formalized, historically certified as novel, or submitted. This is a *positive* resolution candidate, NOT a counterexample. It belongs exclusively to Agent C and must not be integrated without ROOT's independent mathematical review.

## Exact original statement and source

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3, dated 10 September 2026, Section 7: https://arxiv.org/html/2603.27559v3#S7 . **FIRST** clause: for every pair of **nonisomorphic finite simple undirected graphs** G,H with isomorphic canonical double covers, one graph has **two vertex-disjoint simple cycles C_k** and the other has a **simple C_(2k)** for some odd k>=3. The source assumes connected, nonbipartite, vertex-determining graphs by default. Here the argument also allows disconnected and bipartite graphs. Do not confuse this with the separately studied SECOND conjecture about unstable **asymmetric** single graphs, or with the disproved older unrestricted single-graph version.

The original article's Theorem 3.1 states that CDC(G) isomorphic to CDC(H) iff G and H are TF-isomorphic. A TF-isomorphism is a pair of vertex bijections (alpha,beta) satisfying the full edge/nonedge biconditional for **all ordered pairs**.

Theorem claimed here: **every such nonisomorphic TF-cousin pair satisfies the first cycle-pair conclusion.** This is a mathematical proof candidate for independent review; historical firstness remains unknown. The 2024 Bychawski odd-order rigidity work is prior art, but the universal proof below does not rely on an originality claim for it.

## 1. Normalize the TF-isomorphism

Let A be G's symmetric 0-1 adjacency matrix, and let B be H's adjacency after relabelling the H vertices via alpha. For the permutation q=beta^(-1) alpha (now acting on the vertices of G), the TF biconditional yields

(1) B(u,v) = A(u,q(v))

for every ordered pair u,v. Since B is symmetric, A satisfies

(2) A(u,v) = A(q(u),q^(-1)(v))

for every ordered pair. Both A and B are symmetric and have zero diagonal. We must show the desired cycles in A and B; ordinary relabelling preserves cycles and isomorphism.

Decompose q into disjoint orbits O_i of lengths m_i>=1, and label each O_i with x in Z/m_i so q acts by x -> x+1. The lengths may be unequal, even, odd, or one. No assumption about ordinary automorphisms is needed.

## 2. No internal edges; full gcd-sum classes between orbits

**Lemma 1.** Neither A nor B has an edge whose ends lie in the *same* q-orbit.

Suppose A has an intra-orbit edge with endpoints a,b mod m. Repeated use of (2) forces (a+t,b-t) to be an edge for every integer t. If b-a is even modulo even m, or m is odd, solve 2t=b-a (mod m), obtaining a forbidden loop. If m is even and b-a is odd, solve 2t=b-a-1 (mod m), obtaining an edge (x,x+1). But then B(x,x)=A(x,q(x))=1, contradicting B's zero diagonal. A size-one orbit cannot have an edge internally. Finally, B=Aq cannot have internal edges either.

**Lemma 2.** For distinct q-orbits O_i,O_j, put g_ij=gcd(m_i,m_j). There is a subset S_ij of Z/g_ij such that

(3A) A((i,x),(j,y))=1  iff  x+y mod g_ij belongs to S_ij,

(3B) B((i,x),(j,y))=1  iff  x+y mod g_ij belongs to S_ij-1.

To prove this, apply (2) repeatedly to an edge (i,a)--(j,b). Its orbit is all pairs (i,a+t)--(j,b-t). The generalized Chinese remainder theorem says that a pair (i,x),(j,y) is in this orbit exactly when x+y=a+b (mod g_ij). These classes partition the pairs. Equation (1) shifts the second label by +1, shifting the class by -1 in B. The result covers all edges and **all nonedges** and includes g_ij=1.

## 3. Nonisomorphism forces an odd cycle in the EVEN-orbit quotient

Let Q be the simple graph whose vertices are **only the even-length q-orbits**, with O_i and O_j adjacent when at least one A edge joins them (S_ij nonempty).

**Lemma 3.** If Q were bipartite, A and B would be ordinarily isomorphic.

Choose a proper 0/1 coloring c_i of Q. Write each orbit size as m_i=2^(a_i) u_i, with u_i odd. For each orbit select e_i mod m_i with

- 2e_i=1 mod u_i (vacuous if u_i=1);
- e_i=c_i mod 2^(a_i) when a_i>=1 (vacuous for odd m_i).

Such e_i exist by CRT. If a graph edge joins **distinct** O_i,O_j, then

(4) e_i+e_j=1 mod gcd(m_i,m_j).

On the odd part of the gcd this follows by doubling and inverting 2. If the gcd is even, both orbit sizes are even and the orbits are adjacent in Q, so their Q-colors are opposite. Therefore c_i+c_j=1, which proves the congruence on their common 2-primary part. This reasoning holds for **every selected edge class**.

Define an actual vertex permutation R(i,x)=(i,x+e_i). By (3A),(3B),(4), for any two distinct orbits and all labels we have

A(R(i,x),R(j,y)) = B((i,x),(j,y)).

For two vertices in the same orbit both matrices have no edge, by Lemma 1. Thus R is a complete adjacency-and-nonadjacency isomorphism B -> A. This contradicts the original nonisomorphism. Therefore **Q is nonbipartite**, and has a simple odd cycle O_0,...,O_(k-1), with k>=3 odd, comprising **distinct EVEN-length** q-orbits.

## 4. Cycle lift for arbitrary unequal even orbit sizes

Let m_0,...,m_(k-1) be the even orbit lengths on that simple quotient cycle. Put g_j=gcd(m_j,m_(j+1)) and L=lcm(m_0,...,m_(k-1)); both L and all g_j are even. On every quotient edge choose an actual nonempty edge class s_j in S_(j,j+1). By Lemma 2, A includes **every** pair whose labels satisfy

(5A) x_j+x_(j+1)=s_j mod g_j,

and B includes every pair with

(5B) x_j+x_(j+1)=s_j-1 mod g_j.

Lift each s_j to any integer S_j modulo L. For A use S_j and for B use S_j-1. Let

(6) D = SUM[j=0..k-1] (-1)^(k-1-j) S_j mod L.

Because k is odd, changing all S_j to S_j-1 changes D by **exactly -1**, so precisely one of A,B has even D and the other has odd D. Their chosen classes retain all required edges, whether additional classes are present or not.

**Lemma 4 (even D => two vertex-disjoint C_k).**

For even D, the cyclic system z_j+z_(j+1)=S_j (mod L), with j modulo odd k, has a solution: start with 2z_0=D (mod L), solvable since gcd(2,L)=2 divides D, and recurse z_(j+1)=S_j-z_j. Since the orbit labels are in **distinct fibers**, the vertices (j,z_j mod m_j) form a simple C_k using the chosen edges.

For a disjoint second C_k, rotate the numbering of the quotient cycle so m_0 has minimal 2-adic valuation r=min_j v_2(m_j)>=1. Write L=2^R U with U odd. Set d=2^(r-1) U and delta_j=(-1)^j d. For every j, delta_j is nonzero modulo m_j because v_2(delta_j)=r-1 < v_2(m_j). Along all nonclosing edges delta_j+delta_(j+1)=0. Along the closing edge k-1 -> 0, the sum is 2d=2^r U, divisible by g_(k-1) because g_(k-1) divides L and has 2-adic valuation at most r (since m_0 has valuation r). Hence labels (j,(z_j+delta_j) mod m_j) also form a simple C_k via the selected **gcd** edge congruences. The two cycles are vertex-disjoint since on each of the k distinct orbits their vertices differ by a nonzero residue. No existence of a second solution modulo full L is asserted or needed.

**Lemma 5 (odd D => a simple C_(2k)).**

Follow the actual selected edges in order via recurrence x_(j+1)=S_j-x_j (mod L), starting with x_0=0 and traversing the quotient cycle **twice**. One full traversal (k odd) maps the initial label by F(x)=D-x; F is an involution. Since D is odd and each m_j is even, the two visits to orbit j have labels differing by +/- (D-2x_0), an **odd** number, which cannot vanish modulo m_j. Thus the 2k consecutive vertices visit exactly two distinct vertices in each of k distinct q-orbits before returning to the start. Every edge is licensed by (5A) or (5B), as appropriate. This is a **simple** C_(2k), with no repeated internal vertices.

Since one of A,B has even D and the other has odd D, Lemmas 4 and 5 produce **two vertex-disjoint C_k in one graph and C_(2k) in the other**. Undoing the original relabelling gives the same cycles in G,H. QED.

This uses the original assertion's precise quantifiers and no assumption of equal orbit lengths, connectedness, nonbipartiteness, or vertex determination.

## 5. Evidence, genuine limitations, and independent review

- **Original-source gate:** Mizzi arXiv v3 Section 7 and Theorem 3.1, checked 2026-10-10. Later-title and same-wording searches did not establish a prior complete resolution; that is a **bounded search, not a novelty certificate**.
- **Exact computed evidence available locally:** 1890 deterministic heterogeneous twist instances (967 explicit isomorphisms when Q bipartite and 923 exact cycle pairs when Q odd), 4608 complete involutive-family instances, and 4912 qualifying TF-cousin pairs from full enumeration of 25344 edge-orbit choices across five restricted configurations. All were actually replayed with standard-library Python 3.13 on 2026-10-10. The 4912-pair test includes full original hypotheses and an independently checked n=10,m=20 nonisomorphic pair. This is not a universal computational proof.
- **Original tested local artifacts:** the complete research packet and source hashes are preserved as agent-C-mizzi-v3-first-clause-full-proof-candidate-2026-10-10.zip; the original raw 10-vertex graph/checker are also preserved under a separate C-only local study. This newly published note is an independent compact transcript of the mathematics, not an unverified claim that the whole local bundle was pushed.
- **Independent ROOT review REQUIRED:** independently derive normalization (1); check no same-orbit edges using B looplessness; verify CRT edge orbit invariance; inspect the bipartition/CRT isomorphism for *odd and even* orbit mixtures; check last-edge divisibility in Lemma 4; prove no vertex repeats in Lemma 5; replay raw source checkers; refresh historical-priority research. No external reviewer acceptance or Lean compilation of this theorem is claimed by Agent C.
- **Publication limits:** Agent C may publish only to partner/dist-C and workstreams/C/. This note itself is an unsigned branch-local research claim, not a signed release, merged manuscript, submission, or notification to ROOT's live process. Preserve existing frozen files and all other streams.
