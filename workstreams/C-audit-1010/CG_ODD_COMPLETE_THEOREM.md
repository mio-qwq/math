# Exact TF-cousin count for Mizzi's claw graphs, all odd n ≥ 3

**Agent C-audit-1010 | 10 October 2026 UTC | mathematical proof candidate, not independent ROOT acceptance, Lean compilation, historical firstness, peer review or submission.**

## Exact original open question

Russell Mizzi, *Lifting and Folding: A Framework for Unstable Graphs and TF-Cousins*, arXiv:2603.27559v3 (10 September 2026), [Definition 6.1 and §7](https://arxiv.org/html/2603.27559v3): determine the number of nonisomorphic TF-cousins of the graph CG(n) for **general odd n**. In §7, the author establishes *at least two* nonisomorphic cousins for odd n≥3, and leaves their exact count open. The Petersen/Desargues case n=1 is exceptional and already known to have one cousin.

**Candidate Theorem (full general odd family).** For every odd n≥3, with \(X=\operatorname{CDC}(CG(n))\) and \(D_{6n}\) the dihedral group of the **6n-gon** (order 12n):

\[
\boxed{\operatorname{Aut}(X)\cong D_{6n}\times C_2,\quad
|\operatorname{Aut}(X)|=24n.}
\]

There are exactly **3n+2 strongly switching involutions**, with three conjugacy classes of respective sizes **1,1,3n**. Therefore exactly **three** nonisomorphic loopless base graphs have canonical double cover isomorphic to X: CG(n) itself and **exactly two** nonisomorphic TF-cousins. In particular CG(n) is stable; the automorphism-group orders of the three respective bases are 12n,12n,4.

This theorem does NOT cover n=1, even n, the extension with claw degree r≠3, or all arbitrary TF-cousin pairs.

## I. Reconstruct the *original* graph without assumptions

Write \(r_t\) for ring vertices indexed modulo \(6n\), \(\ell_p\) for leaves indexed modulo \(3n\), and \(c_i\) for centres indexed modulo \(n\). This is precisely the paper's relabelling \(p=i+jn\) of \(\ell_{i,j}\). The **entire undirected edge set** of G=CG(n) is

\[
r_t r_{t+1};\qquad \ell_p r_p,\ \ell_p r_{p+3n};\qquad
c_i\ell_p\quad(p\equiv i\pmod n).
\]

G has 10n vertices, 15n edges and degree three everywhere. Its canonical double cover X has vertices \(v^\varepsilon=(v,\varepsilon)\), with adjacency \(u^\varepsilon\sim v^{1-\varepsilon}\) exactly when \(u\sim v\) in G. Thus X has 20n vertices and 30n edges. Since n is odd, the ring antipodal path of length 3n together with its two-edge leaf shortcut makes an odd cycle of length 3n+2; G is connected and nonbipartite, and X is connected.

## II. Six-cycles uniquely identify all vertex types

Call an edge **hexagonal** if it belongs to some *simple six-cycle* of X. This invariant is preserved by every automorphism.

**Lemma 1.** Every edge of type ring–ring or ring–leaf is hexagonal; no edge of type leaf–centre is. Consequently the incident numbers of hexagonal edges are **3 for rings, 2 for leaves and 0 for centres**, and the three kinds of vertices are intrinsically distinguishable in X.

*Proof.* Let \([t]\) denote \(t\bmod3n\). For any t and ε, the following **six distinct** vertices in order form a genuine simple hexagon (all edges come directly from the source):

\[
r_t^\varepsilon,\quad r_{t+1}^{1-\varepsilon},\quad
\ell_{[t+1]}^\varepsilon,\quad r_{t+1+3n}^{1-\varepsilon},\quad
r_{t+3n}^\varepsilon,\quad \ell_{[t]}^{1-\varepsilon}.
\]

Varying t and ε covers every ring–ring edge and every ring–leaf edge.

Suppose instead a hexagon contains a centre \(c_i^\varepsilon\). Its two incident edges in the hexagon use **distinct** leaves \(\ell_p^{1-\varepsilon},\ell_q^{1-\varepsilon}\), where \(p\ne q\pmod{3n}\) and \(p\equiv q\equiv i\pmod n\). The intervening path of length four between the two leaves has the form

\[
\ell_p^{1-\varepsilon}
-r_a^\varepsilon
-w^{1-\varepsilon}
-r_b^\varepsilon
-\ell_q^{1-\varepsilon}.
\]

Here a lies in p's antipodal ring pair, b in q's pair. Distinct petals at the *same* claw have \(a-b\pmod{6n}\in\{\pm n,\pm2n\}=\{n,2n,4n,5n\}\). But two ring vertices joined by a two-edge path have middle vertex either another ring vertex (requiring ring difference 0 or ±2), or a leaf (requiring difference 3n); a centre has no ring neighbour. Since n≥3, none is possible (and a=b would repeat a hexagon vertex). Contradiction. Thus centres do not belong to any simple hexagon and their three incident centre–leaf edges are not hexagonal. This proves the invariant and lemma. ∎

There are therefore exactly 12n intrinsically ring-type, 6n leaf-type, and 2n centre-type cover vertices.

## III. A universal automorphism upper bound of 24n

The subgraph induced by the ring-type vertices of X is the double cover of the original even ring \(C_{6n}\), hence consists of **two disjoint cycles, each of length 6n**. Its two components are distinguished by the ring coordinate parity \(t+\varepsilon\bmod2\).

Each cover ring vertex has exactly **one leaf neighbour**. Each cover leaf \(\ell_p^\varepsilon\) has exactly two ring neighbours \(r_p^{1-\varepsilon}\) and \(r_{p+3n}^{1-\varepsilon}\). Since n is **odd**, 3n is odd and these lie on **different** distinguished ring cycles. Thus the leaves encode a perfect matching between the two ring cycles: every ring vertex has one uniquely paired opposite-cycle ring vertex, with its unique leaf as intermediary.

An automorphism f must preserve ring/leaf/centre types by Lemma 1, so it permutes the two distinguished 6n-cycles. It has at most two choices for the target cycle of one selected source cycle, then **at most 12n** choices for its restriction there, because an isomorphism of a cycle \(C_{6n}\) is fixed by an initial vertex image (6n choices) and an orientation (2 choices).

**The image of this one ring cycle determines the entire automorphism:** every ring vertex's unique adjacent leaf is forced to map to the image ring vertex's unique leaf; that leaf's unique ring neighbour on the **other** ring cycle forces the second ring cycle's image, and every remaining centre is forced as the unique centre neighbour of one of its adjacent leaves. Hence

\[
\boxed{|\operatorname{Aut}(X)|\le 2\cdot12n=24n.}
\]

No automorphism-group enumeration, spectral approximation, or conjectured symmetries are assumed.

## IV. Realize all 24n symmetries

For any t modulo 6n, literal edge substitution shows that **rotation** and **reflection** of the original CG(n) are automorphisms:

\[
\begin{array}{lll}
\rho_t(r_s)=r_{s+t},&
\rho_t(\ell_p)=\ell_{p+t\ \mathrm{mod}\ 3n},&
\rho_t(c_i)=c_{i+t\ \mathrm{mod}\ n};\\
\mu_t(r_s)=r_{t-s},&
\mu_t(\ell_p)=\ell_{t-p\ \mathrm{mod}\ 3n},&
\mu_t(c_i)=c_{t-i\ \mathrm{mod}\ n}.
\end{array}
\]

They give an embedded dihedral group of order 12n (distinct restrictions to the original ring). Lift all 12n to X while preserving the layer bit. Independently multiply by the central **deck flip** \(\delta(v^\varepsilon)=v^{1-\varepsilon}\), which is not a layer-preserving lift. This yields **24n distinct automorphisms**. The lower bound equals the upper bound from Section III, so

\[
\operatorname{Aut}(X)=\widetilde{D}_{6n}\times\langle\delta\rangle
\cong D_{6n}\times C_2.
\]

The same equality yields \(|\operatorname{Aut}(CG(n))|=12n\) and stability.

## V. Count **all** strongly switching involutions

Every cover-layer-exchanging automorphism is \(\delta\widetilde\sigma\) for some \(\sigma\in D_{6n}\). Its square is the identity exactly when \(\sigma^2=1\). In the dihedral group of the even 6n-gon the latter elements are identity \(\rho_0\), central halfturn \(\rho_{3n}\), and **all 6n reflections** \(\mu_t\).

Such a cover involution is **strongly switching** exactly when no vertex \(v\) of the original CG(n) is adjacent to \(\sigma(v)\); only then can it fold to a loopless graph.

- \(\rho_0\) satisfies this automatically (no graph loops).
- \(\rho_{3n}\) fixes leaves and centres and sends each ring vertex to its antipode, which is not an adjacent ring vertex.
- A reflection \(\mu_t\) preserves the three vertex types. Only ring vertices can be adjacent to other vertices of their **same type**. A ring vertex r_s maps to an adjacent ring vertex iff \(t-s\equiv s\pm1\pmod{6n}\), equivalently \(2s\equiv t\mp1\pmod{6n}\). Since 6n is even, this has a solution exactly when **t is odd**. Therefore **exactly the 3n even-indexed reflections** satisfy the looplessness requirement.

Thus the complete list is

\[
\boxed{\delta\widetilde\rho_0,\quad
\delta\widetilde\rho_{3n},\quad
\{\delta\widetilde\mu_{2j}:0\le j<3n\},}
\]

total **3n+2**. The first two are central singleton conjugacy classes; all even-indexed reflections are mutually conjugate under rotations \(\rho_a\mu_t\rho_a^{-1}=\mu_{t+2a}\), giving **one more class of size 3n**. There are exactly **three conjugacy classes**, of sizes **1,1,3n**.

## VI. Deduce the **exact** number of nonisomorphic TF-cousins

By the already-published switching/folding conjugacy criterion (Mizzi v3 **Theorem 4.6**, deriving from Pacco–Scapellato), conjugacy classes of strongly switching involutions on a connected bipartite canonical double cover correspond **bijectively** to ordinary isomorphism classes of loopless graphs with that CDC. Equivalently: a fold is obtained by identifying the paired opposite-layer vertices; an isomorphism of the resulting bases lifts to a cover automorphism conjugating their switching involutions, and vice versa.

The three classes therefore give **precisely three distinct base graphs**. The class of the original deck flip produces CG(n) itself. The other two produce the two nonisomorphic TF-cousins — one is the paper's CG′(n), and the other is its even-axis reflection fold. Hence

\[
\boxed{\text{For every odd integer }n\ge3,\quad
\#\{\text{nonisomorphic TF-cousins of }CG(n)\}=2.}
\]

The two singleton classes have folded-base automorphism groups of order \(24n/(2\cdot1)=12n\); the class of size 3n gives order \(24n/(2\cdot3n)=4\). This bonus follows by quotienting each involution's centralizer.

**Boundary:** n=1 is expressly excluded: its source graph is the Petersen graph with Desargues CDC and extra symmetry, already known to have **one** cousin. The proof's key six-cycle obstruction fails in that exceptional small graph. Nothing here settles Mizzi's separate conjecture about cycles in **arbitrary** TF-cousin pairs.

## Exact replay (not a substitute for universal proof)

- Standalone source: \`cg_all_odd_checks.py\`. It does NOT import the prior n=3 graph-isomorphism or discovery code and uses only Python standard library.
- From original graph edges, for each cover edge it searches for an alternative simple length-five path to decide whether it belongs to a six-cycle. It also reconstructs both ring components, leaf-perfect matching, **every** explicit dihedral+deck permutation, all layer-exchange involutions, and every adjacent-image test. A separate exact metric landmark test bounds automorphism group size independently for the enumerated finite n.
- Actual executed **CPython 3.13.5 Linux** on **n=3,5,7,9,11,13,15**: all checks PASSED (no third-party packages). For n≥5 an eight-landmark set \((0,3,12n-1,14n+1,10n,8n+3,2n+1,1)\) resolves all 20n cover vertices and has exactly 24n distance-compatible image tuples. n=3 uses the previously complete six-landmark bound.
- Three deliberate corrupted-input controls (removed original ring edge, altered proposed isomorphism, forbidden cover loop) are rejected. Generated exact data: \`cg_all_odd_check_results.json\`.
- Actual source SHA-256: \`68124c6929cd96d847fe4ec4aaef7135eac3a2174ba7a17a27e03561742c8c21\`; results SHA-256: \`a1102d1c4869591b97f0bac90c98dee6d4c1cc983adb66292eeb5d402d373a10\`. These hashes are not an independent proof of general n.
- A methodologically distinct complete six-landmark automorphism enumeration for n=3 previously gave 72 automorphisms, 11 qualifying involutions, three conjugacy classes. Its limited n=3 classification is a **consequence** of the new universal argument, not evidence of all-n scope.

## Mandatory independent ROOT review

Review the original v3 source and author followups; ensure the counting convention excludes CG(n) itself; independently inspect Lemma 1 (particularly the six-cycle centre exclusion, n≥3), the distinguished two ring cycles and leaf matching for **odd** n, the exact **24n** upper/lower automorphism bounds, the even/odd reflection adjacent-image test, and Theorem 4.6's hypotheses for folding bases. Rebuild some test cases from original adjacency, verify three negative controls, then check for prior published equivalent all-n results. No Lean compilation or axiom audit, independently accepted proof, priority certificate, peer review, paper submission, PR or merge is claimed. Agent C uses only \`partner/dist-C-audit-1010\` and \`workstreams/C-audit-1010/\` because another same-ID instance may write the original C branch. ROOT owns integration and release.
