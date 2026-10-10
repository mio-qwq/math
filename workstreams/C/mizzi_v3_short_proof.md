# Agent C — Shorter proof of Mizzi's revised asymmetric-unstable clause

**2026-10-10. Status:** complete written **affirmative proof candidate**, not a counterexample or a historically certified first proof. This is an independent **presentation and simplification** of C's already frozen theorem packet, not a rewrite of its SHA. Independent outside review and Lean compilation of this statement remain pending.

## Statement and original scope

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 Sep 2026), §7, https://arxiv.org/html/2603.27559v3#S7, contains **two separate** conjectural assertions. We address only the **second**: every *unstable asymmetric* finite simple undirected graph has both a simple `C_k` and a simple `C_{2k}` for some odd `k`. We prove the cycles may in fact be taken **vertex-disjoint**, and a stronger bundle can be extracted as in `mizzi_cycle_bundle_extension.md`. Nothing here solves the **first** assertion, which relates **two nonisomorphic TF-cousin graphs**.

This argument uses the **2011 literature** to remove an unnecessary group-theoretic detour from the earlier C proof. Specifically:

- J. Lauri, R. Mizzi and R. Scapellato, *Two-fold automorphisms of graphs*, Australasian J. Combinatorics **49** (2011), 165–176, Proposition **3.1** constructs an inverse pair `(gamma,gamma^-1)` and Proposition **3.3** excludes even-order `gamma` in an asymmetric graph; see https://ajc.maths.uq.edu.au/pdf/49/ajc_v49_p165.pdf , journal pp. 173–174.
- Bychawski, arXiv:2406.06267v1, **Theorem 6.2**, already establishes abelian odd-order TF projection groups and that orbit-induced subgraphs are empty for asymmetric unstable graphs. Neither fact is claimed novel by C: https://arxiv.org/html/2406.06267v1#S6

## A complete short proof

Call `(p,q)` a two-fold (TF) automorphism if, for every **ordered** pair of vertices `u,v`, we have

\[
u v\in E(G)\iff p(u)q(v)\in E(G).
\]

A graph is asymmetric when `Aut(G)={id}`. We use the standard equivalence between instability and the existence of a nontrivial TF automorphism (Mizzi's Theorem 2.1).

**Step 1: an inverse TF pair of odd order, without full TF group theory.**

Pick any nontrivial TF pair `(p,q)`, where `p != q`. Because `G` is undirected, the component swap `(q,p)` is also TF, as is its inverse `(q^-1,p^-1)`. Multiplication gives

\[
(p,q)(q^{-1},p^{-1})=(\gamma,\gamma^{-1}),\qquad \gamma=pq^{-1}\ne \mathrm{id}.
\]

Suppose `gamma` has even order `2r`. Then the `r`-th power of the inverse TF pair is `(gamma^r,gamma^-r)=(t,t)`, where `t=gamma^r` is a **nonidentity involution**, hence a nontrivial *ordinary* graph automorphism. This contradicts asymmetry. Thus `gamma` has **odd** order, and at least one moving orbit of length >=3.

This short argument is exactly the known mathematical mechanism of **Lauri–Mizzi–Scapellato (2011), Propositions 3.1 and 3.3**. It replaces, but does not invalidate, the earlier C packet's longer finite-group lemma.

**Step 2: moving-orbit quotient is not bipartite.**

Take the permutation cycles of `gamma` as vertex blocks. Every cycle length is odd. Within one block of size `m`, any putative edge `(a,b)` is mapped by repeated `(gamma,gamma^-1)` to `(a+t,b-t)`. Choosing `2t=b-a\pmod m` (possible because `m` is odd) gives a loop, impossible. So **there are no edges inside any permutation block**.

Edges from a fixed vertex (`m=1`) to a moving block must be **complete or absent**, by repeated TF action.

Form quotient `Q` on *only the moving blocks*, with adjacency whenever some graph edge joins two blocks. If `Q` were bipartite with sides `X,Y`, define `sigma` by `gamma` on blocks in `X`, `gamma^-1` on blocks in `Y`, and the identity on fixed vertices. For an edge/nonedge between moving blocks, the quotient's bipartition ensures that this is exactly the TF relation (or its swapped version). Internal edges do not exist and fixed-vertex incidences are complete-or-absent, so **every edge and nonedge is preserved**. Hence `sigma` is an **ordinary automorphism**, nontrivial because at least one moving block exists, a contradiction.

Therefore `Q` is nonbipartite and has a **simple odd quotient cycle** of length `k>=3`.

**Step 3: explicit cycle lift for unequal odd orbit lengths.**

Label the successive `k` moving blocks along the odd quotient cycle by `Z/m_j Z`, with `m_j>=3` odd and `gamma(x)=x+1`. Choose **one real graph edge** between each consecutive pair of blocks. Repeated TF action yields every pair of labels `(x,y)` whose sum equals its fixed residue `s_j` modulo `gcd(m_j,m_(j+1))`, by the generalized CRT.

Put `L=lcm(m_0,...,m_(k-1))`, which is odd. Choose arbitrary lifts `S_j` of those residues modulo `L`. The odd cyclic equations

\[
z_j+z_{j+1}=S_j\pmod L
\]

have a solution because eliminating variables gives `2z_0=S_0-S_1+\cdots+S_(k-1)` and `2` is invertible modulo odd `L`.

The vertices `(j,z_j)` give a **simple** `C_k` using actual graph edges. The vertices in order

\[
(j\bmod k,\;z_{j\bmod k}+(-1)^j),\qquad j=0,\ldots,2k-1
\]

give a **simple** `C_{2k}`: successive offset signs cancel in their edge sums, and because `k` is odd each orbit contributes one `+1` and one `-1` vertex during the two traversals. The two cycles are vertex-disjoint, since `0,+1,-1` are distinct modulo every odd `m_j>=3`.

This proves the claimed stronger result. `QED`

**Bundle amplification:** The same argument with `+t,-t` for every `1<=t<=(min_j m_j-1)/2` simultaneously yields **one disjoint `C_k` and `(min_j m_j-1)/2` pairwise disjoint `C_{2k}`'s**, using exactly the minimum orbit length many vertices per selected block. The complete multiplicity argument, raw 29-vertex witness and independent corruption-tested checker are separately frozen under `mizzi_cycle_bundle_extension.md`, `cycle_bundle_example.json` and `verify_mizzi_cycle_bundle.py`.

## Source boundaries and review status

This direct argument relies on **ordinary graph edges and nonedges**, not an assumed label-level quotient model: the quotient and residue classes were deduced from the actual TF relation. It handles moving cycles of different odd lengths and arbitrary fixed points. The original paper convention assumes connected, nonbipartite and vertex-determining graphs; the proof in fact works for **every finite simple undirected asymmetric unstable graph**, which implies those cases.

We screened the arXiv v3 original, the primary 2011 results (PDF text; image screenshot service was unavailable), and Bychawski's 2024 theorem; **we have not exhaustively audited all publications, revisions or private/unindexed preprints for priority**. Some group and independent-orbit statements are **explicitly prior**. The new quotient/parity argument's priority is unestablished. This is **not** a verified journal submission, an independently refereed result, a complete Lean theorem or an accepted main-branch integration. A branch publication is merely a frozen candidate for ROOT's independent reconstruction.

The original Collins–Sciriha Question 5.8 result has already been independently accepted and released by ROOT, and is separate from the present candidate. No existing frozen file is altered here.
