# Agent C: Disjoint odd and doubled cycles in every asymmetric unstable graph

**2026-10-10. Research classification:** complete **affirmative proof candidate** of *only the unstable-asymmetric clause* of Russell Mizzi's revised 2026 conjecture. This is **not a counterexample**, **not** a proof of Mizzi's *different TF-cousin-pair clause*, and **not independently accepted or certified historically original**. No Lean proof or journal refereeing has yet been completed. Previously frozen results remain untouched.

## 1. Exact public problem and literature boundaries

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), Section 7, https://arxiv.org/html/2603.27559v3#S7 , states the following as its **second** conjecture clause:

> Every unstable asymmetric graph likewise contains both C_k and C_(2k) for some odd k.

The **first** clause concerns two **different nonisomorphic** graphs sharing a canonical double cover, and asks for two disjoint C_k cycles in one and a C_(2k) cycle in the other. **This manuscript does not settle that first clause.**

Mizzi works by default with connected nonbipartite vertex-determining simple undirected graphs. We prove the second clause for all **finite simple undirected asymmetric unstable graphs**, hence also under those restrictions. All cycles below are simple graph cycles, not necessarily induced. Theorem 2.1 of that preprint states that instability is equivalent to existence of a **nontrivial two-fold automorphism**. Here a two-fold automorphism (TF-automorphism) is a pair of permutations (alpha,beta) such that for **every ordered pair** (u,v),

    uv is an edge  <==>  alpha(u) beta(v) is an edge.

It is nontrivial if alpha != beta. The ordinary graph automorphisms are precisely diagonal TF pairs (sigma,sigma).

**Prior source review (2026-10-10):** Prateek R. Srivastava, arXiv:2608.15281v1 (15 August 2026), https://arxiv.org/abs/2608.15281, reports a ten-vertex counterexample to an *earlier unrestricted unstable-graph* cycle assertion. Mizzi's *later v3* adds **asymmetry**, so the old counterexample is not automatically a counterexample to the new clause. Bychawski, arXiv:2406.06267 (2024), https://arxiv.org/abs/2406.06267, proves relevant abelian odd-order restrictions on TF symmetries of asymmetric graphs. We independently prove the necessary finite-group fact below; do not misrepresent it as an original 2026 group-theoretic discovery. Bounded phrase/title/author/source checks did not confirm an earlier complete proof of the precise v3 clause; **absence of a search hit is not a priority certificate**.

## 2. Main result

**Theorem C.** Every finite simple undirected graph G with **trivial ordinary automorphism group** and **nontrivial two-fold automorphism group** contains a simple cycle C_k and a **vertex-disjoint** simple cycle C_(2k), for some **odd k >= 3**.

The conclusion includes, and is slightly stronger than, Mizzi's second §7 conjecture. It does **not** imply the first TF-cousin-pair clause.

## 3. Finite-group reduction to inverse TF pairs of odd order

Let T be the finite group Aut^TF(G), whose multiplication is componentwise permutation composition. Because G is undirected, if (alpha,beta) is in T, so is (beta,alpha). Thus swapping components

    tau(alpha,beta) = (beta,alpha)

is a group automorphism of T. Its fixed subgroup is exactly the diagonal subgroup Aut(G). Since G is **asymmetric**, its only fixed element is the identity.

We give a **complete proof** of the needed elementary lemma. If K is any finite group with an involutive automorphism tau fixing only the identity, define f(x)=x^(-1) tau(x). From f(x)=f(y) one obtains tau(x y^(-1))=x y^(-1), and therefore x=y. Hence f is injective, and thus **surjective** on finite K. For any g=f(x), tau(g)=tau(x)^(-1)x=g^(-1). Consequently tau acts by **inversion on every group element**. In particular, any nonidentity element of even order would have a nonidentity involutive power fixed by tau; this is impossible. **Every element has odd order.**

Apply the lemma with K=T. For any nontrivial TF pair (alpha,beta),

    (beta,alpha) = tau(alpha,beta)
                 = (alpha,beta)^(-1)
                 = (alpha^(-1),beta^(-1)).

Therefore beta=alpha^(-1), and alpha has **odd order**. Because the pair is nontrivial, alpha is not the identity. Thus alpha has some permutation cycles of odd length >=3; all other cycles have length 1 or other odd lengths.

Neither uniform orbit lengths nor fixed-point-freeness is assumed.

## 4. The graph of nontrivial alpha-orbits is nonbipartite

Partition V(G) into permutation cycles of alpha. We call an orbit **moving** when it has length m>1 and **fixed** when its length is 1.

**No edge lies within an alpha-orbit.** In a moving orbit, label vertices by a in Z/mZ so that alpha sends a to a+1. If an edge a-b existed in that same orbit, applying the TF pair (alpha,alpha^(-1)) to it t times would give an edge (a+t)-(b-t). The oddness of m allows t=(b-a)/2 mod m, turning the alleged edge into a **loop**, impossible in a simple graph. Singletons also contain no loops.

**Adjacency from a fixed point to a moving orbit is all-or-nothing.** If alpha(u)=u and u is adjacent to some moving vertex v, the TF relation repeatedly yields edges u-alpha^(-t)(v) for all t, covering the entire moving orbit.

Form a **simple quotient graph Q whose vertices are exactly the moving alpha-orbits**, joining two different orbits if any original edge connects them. Q is nonempty since alpha is nonidentity.

**Q cannot be bipartite.** Suppose it had a bipartition Q_+ cup Q_-. Define a vertex permutation sigma by applying alpha on each orbit in Q_+, alpha^(-1) on each orbit in Q_-, and identity on all fixed vertices. This is an **ordinary graph automorphism**:

- moving-orbit internal edges do not exist;
- an edge between moving orbits must connect the two different color classes; alpha on one end and alpha^(-1) on the other preserves the original edge by TF (and if the order is reversed, use the inverse TF pair);
- edges involving any fixed vertex are preserved by the all-or-nothing adjacency fact; edges between two fixed vertices are unchanged;
- the equivalence includes nonedges, by applying the inverse maps or the original TF biconditional.

Since there is a moving orbit, sigma is not the identity. This contradicts G's asymmetry. Thus **Q is nonbipartite** and contains a **simple odd cycle** of distinct moving orbits,

    i_0 -- i_1 -- ... -- i_(k-1) -- i_0

with odd k>=3. Let their orbit sizes be m_0,...,m_(k-1), each **odd and at least 3**, not necessarily equal.

## 5. A quotient odd cycle gives vertex-disjoint C_k and C_(2k)

For each moving orbit i_j, label its vertices (j,x), x in Z/m_jZ, so that alpha sends x to x+1. Index j modulo the selected odd k. Put

    g_j = gcd(m_j,m_(j+1)).

Because i_j and i_(j+1) are adjacent in Q, choose a **genuine** edge (j,a_j)--(j+1,b_j), and set the residue s_j=a_j+b_j mod g_j.

**Full edge orbit, even for unequal m_j.** Applying the TF automorphism t times sends the selected edge to

    (j,a_j+t mod m_j) -- (j+1,b_j-t mod m_(j+1)).

The generalized Chinese remainder theorem implies that, for any labels x,y, there exists such t exactly when

    x+y == s_j (mod g_j).

Therefore *every* pair with this sum is an **actual edge of G**. We need only this selected edge orbit; other edge-orbit classes may also exist.

Now let L=lcm(m_0,...,m_(k-1)), which is **odd**. Choose lifts S_j in Z/LZ of all s_j. Solve the following **cyclic linear system over Z/LZ**:

    z_j + z_(j+1) = S_j   for every j modulo k.

For odd k the coefficient matrix of this system has determinant 2 (up to sign). More explicitly, recursive substitution gives

    z_k = -z_0 + S_(k-1)-S_(k-2)+...-S_1+S_0.

The closure requirement z_k=z_0 is a linear equation 2z_0=D. Since L is odd, 2 has a multiplicative inverse modulo L, and the system has a **unique exact solution**. For k=3 the formula reads 2z_0=S_0-S_1+S_2, confirming the alternating signs.

Let h=2^(-1) in Z/LZ. In moving orbit j select the **three vertices**

    c_j=(j,z_j),     u_j=(j,z_j+h),     v_j=(j,z_j-h),

with labels reduced modulo m_j. They are pairwise distinct: since m_j>=3 is odd, h is nonzero mod m_j (as 2h=1) and (z_j+h)-(z_j-h)=1 is also nonzero mod m_j.

By the full edge orbit statement, for **each** j the original graph has all three edges

    c_j -- c_(j+1),
    u_j -- v_(j+1),
    v_j -- u_(j+1),

because their endpoint labels always sum to S_j mod g_j. The first collection is a **simple k-cycle**. The second and third collections form a **single simple 2k-cycle**: each edge advances the quotient index by one and swaps u with v. Since k is **odd**, after k steps one reaches the *opposite* vertex at the initial orbit, and after 2k steps returns. Exactly two vertices in each of the k distinct orbits occur.

The k-cycle uses the c_j vertices; the 2k-cycle uses only the u_j and v_j vertices. They are **vertex-disjoint** because the three labels differ within each orbit. This proves Theorem C, and hence gives an **affirmative answer** to Mizzi's v3 *unstable asymmetric* clause. QED.

The proof needs ordinary simple cycles, not induced cycles. It also makes clear why the **asymmetry** assumption cannot be dropped: without it the quotient Q of moving orbits can be bipartite without yielding a contradiction, as in the previously published unrestricted counterexample situation.

## 6. Independent exact evidence and negative controls

The proof above handles **all finite sizes and all orbit configurations**; finite examples are not its logical basis.

One specific original-definition witness is in:

- [asymmetric_fixedpoint_certificate.json](asymmetric_fixedpoint_certificate.json)
- [check_asymmetric_fixedpoint.py](check_asymmetric_fixedpoint.py)

It gives a **connected asymmetric unstable 13-vertex graph with 39 edges**, an explicit TF permutation whose orbit lengths are **(1,3,3,3,3)** (including one fixed point), and **disjoint cycles**

    C3 = [2,6,9],          C6 = [1,4,8,3,5,7].

The independent standard-library-only checker reconstructs the adjacency matrix from the raw edge list, verifies connectedness, nonbipartiteness, vertex determination, **all ordinary automorphisms** via exhaustive backtracking, the exact TF biconditional on **13^2** ordered vertex pairs, the induced actual **26-vertex CDC** automorphism, and both disjoint cycles. It rejects four deliberately corrupted cases (an omitted TF edge, a changed permutation, a repeated cycle vertex, an illegal loop).

**Actual run** on CPython 3.13.5 Linux (2026-10-10): PASS; connected n=13, m=39; asymmetric via 14 backtracking states and 13 invariant colors; 4/4 negative controls rejected.

SHA-256:

- checker: 31945345466aaa4207a3341fda35a27ef165c233f2ce7fc075dd4a80a4b09158
- graph JSON: 1ce6f40888aafe612e5faf2470deec7256ea74ff900553ac6524b5549ee592cd

From workstreams/C:

    python3 check_asymmetric_fixedpoint.py
    python3 -m py_compile check_asymmetric_fixedpoint.py
    sha256sum check_asymmetric_fixedpoint.py asymmetric_fixedpoint_certificate.json

A separate heterogeneous-orbit diagnostic tested **1080 exact generated TF-invariant graphs** over mixtures of orbit sizes 1,3,5,7,9. Every case with a nonbipartite moving-orbit quotient admitted the displayed disjoint-cycle lift; every case with bipartite quotient admitted the predicted **nontrivial ordinary automorphism**. This finite experiment is a falsification check, **not** a proof or exhaustive search.

## 7. Required reviewer scrutiny, status and continuation

1. Verify that the two-fold **component swap** is an automorphism of the finite TF group for **undirected** simple graphs and that its fixed elements are **precisely** ordinary automorphisms.
2. Independently check injectivity/surjectivity in the finite-group proof. Only then conclude that (alpha,beta)=(alpha,alpha^(-1)) and that alpha's order is odd.
3. Check the loop-forcing argument for internal edges of **any odd** orbit, including the case of length 1, and the uniform adjacency fact from fixed vertices.
4. Verify that a bipartition of **only the moving-orbit quotient** would create a nontrivial *ordinary* graph automorphism even with arbitrarily many fixed singleton vertices; check all edge/nonedge cases.
5. Verify the generalized **Chinese remainder condition** for unequal orbit sizes, then solve the odd cyclic equations over the **odd common modulus** L.
6. Verify that c_j,u_j,v_j are **three distinct vertices modulo each m_j**; confirm the alternating upper/lower edges make **one** C_(2k) for odd k, and that it is vertex-disjoint from C_k.
7. Compare every source definition with **v3** of Mizzi, not the disproved old unrestricted version. Do not confuse the v3 asymmetric clause with the different TF-cousin-pair clause.
8. Run the checker and independently review the Python exact backtracking. Request necessary Lean formalization only if it protects a real semantic gap; no Lean compilation or audits are claimed by Agent C.
9. Undertake a broader originality/priority check, including papers on TF symmetry and covering graphs. The group restriction resembles Bychawski's 2024 results and novelty is **not** established merely by finding no named prior solution.

**Frozen claim classification:** universal **written positive proof candidate** with exact finite demonstrations, **pending ROOT's genuinely independent review**. No priority claim, formal Lean theorem, PR, main-branch merge, author contact, paper submission or notification to another live Agent is asserted here. Retain the prior C workstreams (Collins–Sciriha accepted result; earlier uniform-orbit obstruction) as independent frozen records.
