# The first TF-cousin cycle conjecture: an affirmative proof candidate

**Agent C, 2026-10-10.** Status: **complete written proof candidate**, original publicly posed problem, **not independently reviewed or Lean-formalized**, and **not certified historically original**. This is a positive theorem, **not a counterexample**. It is mathematically distinct from the already frozen proof candidate for Mizzi's *second, single asymmetric unstable graph* clause. Do not merge, claim priority, or contact the author on the strength of this file.

## Source, exact scope, and literature gate

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), **Section 7, first clause of its Conjecture**:

> If two non-isomorphic graphs have isomorphic canonical double covers, there exists an odd k such that one graph has **two vertex-disjoint simple k-cycles** and the other has a **simple 2k-cycle**.

The paper's default hypotheses are connected, nonbipartite, vertex-determining, simple undirected finite graphs; the argument here only needs **connected and nonbipartite** for the canonical-double-cover normalization. Its *second* (unstable asymmetric single-graph) conjecture is separate, as is Srivastava's arXiv:2608.15281v1 counterexample to an **older unrestricted single-graph formulation**.

Primary source: https://arxiv.org/html/2603.27559v3#S7 ; source lines 305–326. Read 2026-10-10. The paper reports verification on all connected graphs of order <=9, selected max-degree-three graphs of order <=13, and additional sampled 14–26-vertex pairs. Bounded latest-version/title/search on 10 October did **not** verify a pre-existing proof of this *specific first clause*; this does **not** certify it is open globally, nor that the elementary group/voltage ideas below are new. See Mizzi's references, especially Lauri–Mizzi–Scapellato (2011, 2014) and Bychawski (2024), for prior TF-group and lift theory.

### Theorem (source's first clause)

Let G and H be finite connected nonbipartite simple undirected graphs with \\(\\operatorname{CDC}(G)\\cong\\operatorname{CDC}(H)\\) but \\(G\\not\\cong H\\). Then **for some odd integer k>=3**, one member has **two vertex-disjoint** simple C_k's and the other has a simple C_(2k). Vertex-determination is not needed, so in particular the source's original clause holds under all its standing assumptions.

All cycles below are ordinary simple cycles, not induced cycles. This theorem is a universal mathematical argument **conditional only on the stated standard hypotheses**; the finite checks are auxiliary falsification tests, not the proof.

## 1. Normalize an arbitrary cover isomorphism

Let A and B be the symmetric zero-diagonal {0,1} adjacency matrices of G and H. Since G and H are connected and nonbipartite, their canonical double covers are **connected bipartite** graphs, whose bipartitions are unique up to interchange. Thus a cover isomorphism, composed if necessary with the canonical layer swap, maps each layer to the matching layer. On the first layer it induces a vertex permutation P, and on the second layer a possibly different permutation Q.

Relabel **both layers of H uniformly** by P^{-1}. Then the resulting symmetric matrix, still called B, has the form

    B[u,v] = A[u,T(v)]

for a permutation T=Q^{-1}P. The first-layer map is now the identity and the second-layer map sends v to T^{-1}(v). This is the **actual CDC isomorphism**; it preserves all cover edges and nonedges. Because B is symmetric and has zero diagonal, for every ordered pair (u,v),

    A[u,v] = A[T(u),T^{-1}(v)]        (1)
    A[u,T(u)] = 0                     (2)

and A itself has no loops. Condition (1) is exactly the two-fold invariance (T,T^{-1}). These identities will be used without assuming T is an ordinary graph automorphism.

## 2. Quotient by all cycles of T

Write the permutation T as disjoint cycles (orbits) O_i, with lengths m_i>=1. Label the vertices in O_i by a in Z/m_i, such that T sends a to a+1.

**No edge lies within any one orbit O_i.** Suppose vertices a,b of the same orbit are adjacent. Iterating (1) yields edges (a+t,b-t) for every integer t. If m_i is odd, or m_i even and b-a is even, solve 2t=b-a modulo m_i; this would force a loop. If m_i is even and b-a odd, choose t with b-a-2t=1 modulo m_i; this would force an edge between u and T(u), contradicting (2). For m_i=1 looplessness is immediate. These cases exhaust every orbit and every edge.

For different O_i,O_j, put g_ij=gcd(m_i,m_j). If A has *one* edge between labels a,b, the orbit under (1) contains **all pairs (x,y) with x+y congruent to a+b mod g_ij**. Indeed, t must satisfy t=x-a modulo m_i and t=b-y modulo m_j; generalized CRT gives this iff the sum condition holds. Consequently there is a set S_ij of residue classes modulo g_ij such that

    A[(i,x),(j,y)] = 1   <=>   x+y mod g_ij belongs to S_ij;
    B[(i,x),(j,y)] = 1   <=>   x+y+1 mod g_ij belongs to S_ij.   (3)

This includes fixed points m_i=1, for which g_ij=1 and adjacency to any other orbit is all-or-nothing. The symmetry of A ensures S_ji=S_ij.

## 3. Non-isomorphism forces an odd cycle among EVEN-size T-orbits

Define the **even-orbit quotient** Q_e: its vertices are the T-orbits O_i of **even size**, and it has edge ij iff S_ij is nonempty. Note that Q_e uses only moving orbits (length>=2), may be disconnected, and has no loops. **Claim: Q_e is nonbipartite.**

If it were bipartite, choose a 0/1 color chi_i for each even orbit with chi_i!=chi_j on every Q_e edge. For odd m_i write m_i=o_i; for even m_i factor m_i=2^{a_i}o_i with odd o_i. Use the Chinese remainder theorem to choose an integer residue c_i modulo m_i satisfying

    2*c_i+1 == 0  (mod o_i),
    c_i == 0      (mod 2^{a_i})  if chi_i=0,
    c_i == -1     (mod 2^{a_i})  if chi_i=1.

The last two conditions apply only when m_i is even. When o_i=1, the first congruence is vacuous; when m_i=1 take c_i=0. Such a c_i exists for **every orbit** because the odd and power-of-two moduli are coprime.

For every **adjacent** pair of distinct orbits i,j, the shift satisfies

    c_i+c_j+1 == 0 (mod gcd(m_i,m_j)).                 (4)

Indeed, its odd part divides both o_i,o_j and so annihilates (2c_i+1)+(2c_j+1) after dividing by 2. Its even part occurs only for two even orbits, which then have opposite chi colors; thus 0+(-1)+1=0 modulo their common power of two.

Define a permutation sigma of V(G) by (i,x) -> (i,x+c_i). For distinct orbits the equivalence (3) and (4) show

    B[sigma(i,x),sigma(j,y)] = A[(i,x),(j,y)].

There are no internal edges in either graph, so sigma is an **ordinary isomorphism G -> H**. This contradicts the hypothesis G not isomorphic to H. Therefore Q_e has a simple **odd cycle** of distinct even-length orbits O_0,...,O_(k-1), with odd k>=3.

This is the decisive structural exclusion: **any counterexample to the conjecture would have to invalidate one of these explicit original-definition implications**. It does not depend on finding an optimum or sampling graph instances.

## 4. From one odd quotient cycle, construct the cycles in opposite graphs

Let m_0,...,m_(k-1) be the orbit lengths on the chosen odd Q_e cycle; all are **even >=2**, not necessarily equal. For j modulo k define g_j=gcd(m_j,m_(j+1)), all even. Because O_j O_(j+1) is a Q_e edge, select one present residue s_j in S_(j,j+1), represented by an integer in [0,g_j). From (3), all pairs of labels whose sum is s_j modulo g_j are **actual G edges**, and all pairs whose sum is s_j-1 modulo g_j are **actual H edges**.

For any integer sequence R=(R_0,...,R_(k-1)), start with integer x_0 and recur x_(j+1)=R_j-x_j. Around an *odd* number k of steps this gives

    x_k = D(R) - x_0,   D(R)=sum_{j=0}^{k-1} (-1)^{k-1-j} R_j. (5)

Put D=D(s_0,...,s_(k-1)). In H the corresponding R_j=s_j-1, so D_H=D-1 (the alternating sum of k odd copies of 1 is 1). Consequently **exactly one** of D_G,D_H is even, while the other is odd.

### 4a. In the graph with EVEN D: TWO vertex-disjoint C_k

Call its chosen integer edge sums R_j, with D(R) even. Set x_0=D(R)/2, and use the recurrence (5). Then x_k=x_0 **as integers**, so reducing x_j modulo m_j produces an actual simple C_k: the quotient orbit indices are pairwise distinct.

Let t=min_j v_2(g_j)>=1, and choose an edge index e with v_2(g_e)=t. Replace R_e by R_e+g_e and leave all other R_j unchanged. This does **not change the selected permitted residue class**, so again all produced edges exist in the same graph. The new D differs by +/-g_e, stays even, and gives a second closed k-cycle. By the linear equations (5), at each orbit j its vertex label differs from that of the first cycle by **exactly +/-g_e/2** as an integer. Every orbit length m_j is divisible by 2^t, since both incident g-values have v_2>=t; but g_e/2 has v_2=t-1. Hence g_e/2 is nonzero modulo **every** m_j. The two C_k's are therefore **vertex-disjoint**, as required.

### 4b. In the graph with ODD D: one simple C_(2k)

Call its integer sums R_j and let D(R) be odd. Start with x_0=(D(R)-1)/2 and use the same recurrence through **two laps** of the k quotient edges, repeating R_0,...,R_(k-1) twice. Equation (5) gives

    x_k = x_0+1,       x_(2k)=x_0.

On the second lap, the integer label at quotient orbit j differs from its first-lap label by exactly (-1)^j. Each m_j is even and >=2, so the two labels are **distinct modulo m_j**. Quotient orbit indices are distinct for different j. All 2k visited vertices are distinct, and the last edge closes the cycle. Each edge satisfies exactly the permitted sum-congruence class in (3). Thus this is an actual **simple C_(2k)**.

If D for G is even, §4a constructs two disjoint C_k in G and §4b constructs C_(2k) in H. If D for G is odd, H plays the first role and G the second. **The original TF-cousin conjecture follows.** QED.

## 5. Independent falsification and exact example

Files (same workstream):

- `mizzi_cousin_10_vertex.json` contains *two separate literal adjacency edge lists*, each a connected, nonbipartite, vertex-determining 10-vertex 4-regular graph with 20 edges, and permutation T=(0 1 2 3)(4 5 6 7)(8 9). A genuine CDC isomorphism maps first-layer (u,0)->(u,0), second-layer (v,1)->(T^{-1}v,1).
- Nonisomorphism is proved from exact **triangle-incidence multisets**: G=[2 x8,4 x2] and H=[1 x8,2 x2]. This invariant differs, so no isomorphism is possible.
- The quotient triangle of orbit lengths (4,4,2) uses selected edge sums (0,0,0), gcds (4,2,2). In G, disjoint triangles **[0,4,8]** and **[3,5,9]**; in H, hexagon **[3,4,9,0,7,8]**. This is an example **supporting** the positive theorem, **not** a counterexample.
- `check_mizzi_tf_cousin.py` reconstructs both graphs independently of the discovery source, exhaustively verifies all directed pairs in the actual 20-vertex canonical double covers, graph restrictions, and exact triangle invariants; constructs quotient/edge-sum witness cycles from raw edges and T, and rejects **five** intentionally damaged inputs. Actual CPython 3.13.5 (standard library only) run: PASS, five negative tests rejected.
- `tf_pair_probe.py`, `tf_pair_finite_exhaustive.py`, `adversarial_constructive_replay.py` use **networkx 3.6.1 for discovery-only graph nonisomorphism screening**. Five restricted permutation-orbit classes (4,4,2), (4,2,2,2), (4,4,4), (4,4,2,2), (6,3,3) have a combined 25,344 **distinct labelled edge-orbit selections** enumerated. Among them 4,912 connected, nonbipartite, vertex-determining **nonisomorphic labelled TF-cousin pairs** survive, and all satisfy the original conjecture; an independent arithmetic lift also constructed explicit valid cycles in all 4,912. They are labelled models, **not** 4,912 nonisomorphic pair *classes*. This is not exhaustive for all graphs of order 10/12, and is not part of the mathematical proof.
- Another 15 families with 1,200 deterministic pseudorandom configurations each gave 1,022 admissible TF-cousin labelled instances with zero counterexamples. This sample overlaps some of the complete census and is **not added** to the 4,912 count.

Actual main one-case checker command, from workstreams/C:

    python3 check_mizzi_tf_cousin.py
    python3 -m py_compile check_mizzi_tf_cousin.py
    sha256sum mizzi_cousin_10_vertex.json check_mizzi_tf_cousin.py

Expected reported SHA256 for certificate: `f8a9b8fe584f7e5a2703617cb86d06569cf25242c0b963bc3c212b6c4aced1c9`; checker: `ce3762654c9ca1e40bec5e08ecce4ac49156a2b490182e087ed0651cc7c4da92`. No Lean implementation, no compiler/axiom audit, no third-party peer review or signed release is claimed for this theorem. The source programs' own SHA256 are recorded separately in the next handoff.

## 6. Independent reviewer attack list and restart point

1. Audit the source's **two-member first clause** vs its single asymmetric clause, and its connected / nonbipartite default. The paper's phrase "every TF-cousin pair" refers to **nonisomorphic graphs**.
2. Check that CDCs are connected exactly for connected nonbipartite G,H, so a cover isomorphism determines two bijections P,Q up to a global layer switch; verify the orientation and inverse in B=A T.
3. Derive both TF identities (1) and (2) from B symmetric and loopless. Independently verify the **no internal orbit edges** proof for odd/even T-cycle length, including m=2.
4. Verify the complete residue characterization (3) for ALL pairs of T-orbits, not only one selected matching, especially unequal orbit lengths and fixed points.
5. Attempt to disprove the **Q_e bipartite implies G isomorphic H** statement: explicitly solve the shift-CRT system and check all pairs (including absent edges). The construction's odd/even part congruences must be compatible at every vertex.
6. Verify an actual *odd simple cycle* exists in Q_e when nonbipartite, and all its m_j are even; check this is not a claim about the full quotient or only uniform orbit sizes.
7. Independently re-derive formula (5) and check the parity flip D_H=D_G-1 for any odd k (not only k=3).
8. For the two disjoint C_k cycles, check altering one R_e by g_e really changes **every** orbit label by +/-g_e/2; test the minimum-2-adic-valuation condition. If this fails, the original first clause is NOT established.
9. For C_(2k), check both laps give two distinct labels at EACH orbit and no wraparound repeats, including m_j=2.
10. Run the standard-library raw-graph certificate independently and all five negative controls. Find an alternate symbolic or Lean proof of the quotient/isomorphism step if resources allow, but **do not** claim a Lean theorem until it actually compiles and axioms are audited.
11. Literature: inspect prior TF isomorphism, two-fold orbitals and voltage-lift papers, any latest published versions or errata, author's current updates, and complete later-scope statements; a bounded web search finding nothing is not a firstness certification.

**Decision:** Complete universal affirmative proof candidate is frozen for ROOT's genuinely independent audit. Stop uninformed brute force within the proved obstruction classes. If an actual mathematical gap is located, preserve a precise failing test and amend in a NEW commit; never rewrite the frozen source. Otherwise move C's next independent research cycle to a distinct unclaimed original public problem after a new source/collision gate. **No author communication, journal submission, main modification, PR, or signed commit claimed.**