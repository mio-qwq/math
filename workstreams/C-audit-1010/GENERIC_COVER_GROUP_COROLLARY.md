# Generic symmetry structure behind the Problem 5.3 asymptotic

**Agent C-audit-1010 | 2026-10-10.** Conditional corollary of the complete written asymptotic-count proof candidate in [GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md](GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md). No independent ROOT acceptance, universal Lean proof or historical novelty claim.

**Corollary candidate.** Among finite connected nonbipartite twin-free graph-isomorphism classes with nontrivially unstable canonical double cover, the proportion of graphs satisfying BOTH

\[
\operatorname{Aut}(G)\cong C_2
\qquad\text{and}\qquad
\operatorname{Aut}(\operatorname{CDC}(G))\cong D_8
\]

tends to one as the graph order tends to infinity. Here \(D_8\) explicitly denotes the **dihedral group of order eight**, not 16.

**Proof.** The global counting theorem shows that asymptotically every unlabelled target graph has a **unique unordered minimal non-diagonal TF support partition** \(\{a_1,a_2\}\sqcup\{b_1,b_2\}\), with all other non-diagonal TF pairs (beyond its factor swap) absent. Its old induced graph \(X\) on \(n-4\) vertices is asymptotically almost surely asymmetric, and the old-neighbour attachment subsets \(A,B\subset V(X)\) are asymptotically almost surely distinct.

Any ordinary graph automorphism preserves the unique minimal-support partition, hence the union of its four special vertices and the old induced graph \(X\). As \(\operatorname{Aut}(X)=1\), it fixes old vertices pointwise; as \(A\ne B\), it cannot interchange the special a-pair with the b-pair. On the four special vertices the chosen perfect-matching cross edges allow either **neither** or **both** pairs to be exchanged. Thus Aut(G) consists precisely of identity and the diagonal double transposition \(\gamma=(a_1a_2)(b_1b_2)\), a C2 group.

The **colour-preserving** automorphism group of CDC(G) is the group of TF pairs. Asymptotically its only elements are

\[
(id,id),\quad ((a_1a_2),(b_1b_2)),\quad
((b_1b_2),(a_1a_2)),\quad(\gamma,\gamma).
\]

These form a Klein four group \(V_4\). The deck involution exchanges the two non-diagonal TF pairs, fixes \((\gamma,\gamma)\), and adds a semidirect C2 factor. Thus the full cover automorphism group is \(V_4\rtimes C_2\cong D_8\), of order eight.

**Important interpretation.** The typical original graph is **not asymmetric**: it already has the ordinary symmetry \(\gamma\). This explains why blindly dividing the labelled count by n! would give the WRONG unlabelled leading constant. In the generic family each graph-isomorphism class has only n!/2 labelled realizations. The main manuscript avoids this mistake by counting canonical unordered attachment pairs directly.

This corollary depends on the global proof's two exclusion estimates and uniqueness. It is **not** a separately proven theorem if that manuscript fails independent verification. Historical priority and formalization remain open.
