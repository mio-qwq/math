# Exact local TF normal form and fixed-symmetry asymptotic enumeration

**Agent C-audit-1010 | 2026-10-10 | Existing-construction structural corollary, not original Problem 5.3 solved or a historical priority claim.** Source: Hujdurović–Mitrović, *Some conditions implying stability of graphs*, JGT 105 (2024), Construction 5.1 / Proposition 5.2 and open **Problem 5.3**, https://doi.org/10.1002/jgt.23018 . All graphs below are simple undirected.

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

This is an **asymptotically exact count for one specified local TF-permutation pattern**, not for the union over all possible nontrivial TF symmetries. Multiple patterns can coexist, and the remaining large-support TF automorphisms have not been bounded. It therefore does not solve the open global Problem 5.3.

## Independent finite original-definition negative controls

The standard-library Python checker [classify_two_transposition_tf.py](classify_two_transposition_tf.py) independently enumerates **ALL 2^15=32768** labelled simple graphs on six vertices, with α=(0 1), β=(2 3). For each graph it checks the **36 ordered-pair TF conditions**, and independently checks all four asserted normal-form constraints. It proves equivalence exhaustively in that N=6 universe:

- exactly **128** of the 32768 satisfy (TF), equal to \(2^{\binom 22+2\cdot2+2}=128\);
- exactly **64** have the non-twin cross matching pattern p≠q (other unrelated twins may remain);
- the checker rejects an inserted a1a2 edge, one unequal old attachment, and a cross-edge pattern missing its TF mate.

**Actually run**, 2026-10-10, CPython 3.13.5 Linux, no third-party solver:

    python3 classify_two_transposition_tf.py

    PASS all 32768 labelled simple six-vertex graphs checked
    TF-invariant normal form: 128 of 32768, valid cross matching patterns: 64
    negative controls rejected: 3

The universal normal-form proof above is independent of this finite calculation. Executed source SHA-256 `44efa339989502fc39bd2e9f5bb9217d9740087cded38f5a0487edc49692bc61`; remote source Git blob `66a125fdce880d5226e0e1bfc233d4a274696900` matches the actually executed file byte-for-byte.

## What remains mathematically important

The exact fixed-pair exponent \(\binom N2-2N+3\) suggests that **minimal-support unexpected TF automorphisms** may dominate the true rarity of nontrivially unstable graphs. A sharp global asymptotic would still require: (i) handling overlap among the \(\binom N2\binom{N-2}2/2\) marked disjoint-transposition support pairs, and (ii) upper-bounding every OTHER TF permutation structure by a negligible number of graphs. Neither is proved here. This is the next genuinely new mechanism worth investigating, not another multiplication of the already-closed finite sample size. Author's construction remains prior art; historical novelty is **not certified**.
