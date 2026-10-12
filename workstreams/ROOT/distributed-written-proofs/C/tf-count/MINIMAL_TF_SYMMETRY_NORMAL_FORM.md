# Exact local TF normal form and fixed-symmetry asymptotic enumeration

Existing-construction structural corollary. Source: Hujdurović–Mitrović, *Some conditions implying stability of graphs*, JGT 105 (2024), Construction 5.1 / Proposition 5.2 and open **Problem 5.3**, https://doi.org/10.1002/jgt.23018 . All graphs below are simple undirected.

## Fixed TF pair — exact classification for every order

Fix N≥4 labelled vertices, with four distinct marked vertices a1,a2,b1,b2 and old set W of size m=N−4. Let α=(a1 a2), fixing everything else, and β=(b1 b2), fixing everything else. This is a genuinely *non-diagonal* two-fold permutation (α≠β). It is a TF-automorphism of a simple graph G exactly when

\[
A_G(u,v)=A_G(\alpha(u),\beta(v))
\quad\text{for every ordered pair }u,v.
\tag{TF}
\]

**Proposition (complete local normal form).** The exact TF condition (TF) holds if and only if ALL the following statements hold:

1. The induced subgraph on W is **arbitrary**.
2. There are **arbitrary** subsets A,B⊆W such that a1 and a2 both connect to precisely A, while b1 and b2 both connect to precisely B.
3. There are **no** edges a1a2 or b1b2.
4. The 2×2 cross-edge matrix between ordered pairs (a1,a2) and (b1,b2) has the exact pattern \(\begin{pmatrix}p&q\\q&p\end{pmatrix}\) for independent Boolean p,q.

**Proof, necessity.** For each old w, applying (TF) to (a1,w) and (w,b1) gives the respective equal attachments. Applying it to (a1,a2) yields A(a1,a2)=A(a2,a2)=0, by the loopless original; similarly (b1,b2) yields A(b1,b2)=0. For cross edges, (TF) sends (a1,b1) to (a2,b2) and (a1,b2) to (a2,b1), proving the two equalities. No other edges can be constrained, because all other pairs are fixed or carry exactly these equalities. **Sufficiency** follows by directly partitioning all ordered pairs into the same cases and checking each equality. ∎

**Exact count, fixed marked pair:** Choose the \(\binom m2\) old edges, m bits for A, m for B, and two bits p,q. There are **exactly**

\[
\boxed{2^{\binom m2+2m+2}
      =2^{\binom N2-2N+4}}
\]

labelled simple graphs whose adjacency satisfies this one specified TF symmetry, with *no* connectedness or twin-free constraints. Since (p,q)=(0,0) or (1,1) makes a1 and a2 open-neighbourhood twins, a twin-free graph necessarily has \(p\ne q\), giving the **exact upper bound**

\[
\#\{\text{twin-free, source-constrained graphs with this pair}\}
\le 2^{\binom N2-2N+3}.
\]

When p≠q, the cross edges are exactly one of the TWO matchings used in [UNSTABLE_DENSITY_SHARPENED_LOWER.md](UNSTABLE_DENSITY_SHARPENED_LOWER.md), a free-attachment form of the source's Construction 5.1. Any connected nonbipartite twin-free old graph X with nonempty A,B yields a valid connected nonbipartite twin-free G, so the explicit probability argument in that note shows:

\[
\boxed{(1-o(1))\,2^{\binom N2-2N+3}
\le \#\{\text{nontrivially unstable connected nonbipartite twin-free graphs with this fixed }(\alpha,\beta)\}
\le 2^{\binom N2-2N+3}.}
\]

This is an **asymptotically exact count for one specified local TF-permutation pattern**, not for the union over all possible nontrivial TF symmetries. Multiple patterns can coexist, and this fixed-pattern argument does not bound large-support TF automorphisms. The complete global asymptotic is proved separately in GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md.
