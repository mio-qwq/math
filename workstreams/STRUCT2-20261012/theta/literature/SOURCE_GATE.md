# Theta facet extremality: source and overlap audit

Date checked: 2026-10-12. This note records source scope and mathematical domain checks. It does not certify historical priority or the absence of an unpublished solution.

## 1. Primary sources and numbering

The controlling source is Benjamin Braun and Kaitlin Bruegge, *Facets of Symmetric Edge Polytopes for Graphs with Few Edges*, Journal of Integer Sequences **26** (2023), Article 23.7.2. The journal article is dated 24 July 2023; its landing page records revisions received 7 and 11 July 2023.

- Journal landing page: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.html>
- Journal PDF: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf>
- Public journal TeX: <https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.tex>
- Preprint history: <https://arxiv.org/abs/2201.13303>

The preprint versions are v1 (31 January 2022), v2 (17 June 2022), v3 (8 March 2023), and v4 (6 July 2023). The following mapping prevents references to different numbering systems from being mistaken for different conjectures.

| Subject | Journal | arXiv v4 | arXiv v1 |
| --- | --- | --- | --- |
| Definition of M | Definition 12 | Definition 3.3 | Definition 3.3 |
| Bicyclic extremal bound | Conjecture 13 | Conjecture 3.4 | Conjecture 3.4, stated as an upper bound |
| Equal-parity F transfers | Conjecture 31 | Conjecture 5.1 | Conjecture 3.15 |
| Mixed-parity theta bound | Conjecture 32 | Conjecture 5.2 | Conjecture 3.18 |
| Four proposed theta maximizers | Conjecture 33 | Conjecture 5.3 | Conjecture 3.19 |

Journal page numbers below are the printed page numbers, starting at 1. The PDF has 29 pages. Exact retrieved-byte hashes are in `source_hashes.json`; copies of copyrighted source papers are not included here.

## 2. The actual graph domain

For a finite simple connected graph G on vertices 1,...,n, the symmetric edge polytope is

\[
P_G=\operatorname{conv}\{\pm(e_i-e_j):ij\in E(G)\},
\]

and N(G) denotes its number of facets (Definition 3, p. 4).

For the three-path graph CB(a,b,c), take two distinct endpoints and three paths between them, with pairwise disjoint sets of internal vertices. The lengths count edges. In the simple bicyclic graph domain, a,b,c are positive and **at most one length is 1**. Then

\[
|E|=a+b+c,
\qquad |V|=2+(a-1)+(b-1)+(c-1)=a+b+c-1.
\]

Thus a+b+c=n+1. This reconstruction follows Definition 20 (p. 12) together with the source's simple-graph convention. If two alleged paths both have length 1, they use the same simple edge. Treating them as separate edges changes the domain to a multigraph; identifying them changes the asserted edge count. Neither interpretation supplies a simple n-vertex, n+1-edge counterexample.

### Small n and C1/C2

Definition 12 is printed with n>=3, but for n=3 and n=4 its displayed graph expression contains C1. The journal text and public TeX contain no definition of C1 or a one-cycle convention. The inspected arXiv v1-v4 texts likewise contain no such convention. The discussion after Lemma 7 (p. 5) deals specifically with **C2**: it is a multigraph, and its facet-labeling count agrees with that of a single edge. That statement does not define C1.

For n=3, no simple graph has n+1=4 edges, since \(\binom 32=3\). Therefore the literal maxf(3,4) extremal graph family is empty. This is a source-domain defect, not a counterexample to the intended extremal assertion.

For n=4, the arithmetic expression for M in the proof of Theorem 18 gives 12. The unique simple graph with four vertices and five edges is K4 minus an edge, equivalently CB(2,2,1), and it has 12 facets. This can be proved directly: normalize one common endpoint to 0; the other endpoint has label -1, 0, or 1. In each case there are four facet-defining labelings of the two internal vertices. No use of C1 is needed. A precise theorem should state the valid n>=5 graph-defined range and handle n=4 explicitly, or explicitly state an arithmetic extension M(4)=12. It should not attribute an unstated C1 convention to the authors.

Conjecture 13 itself states \(\operatorname{maxf}(n,n+1)=M(n)\) for n>=3, where maxf takes the largest facet count among connected simple graphs with the prescribed vertex and edge counts. The qualification above is necessary when stating a rigorous resolution of that printed formula: n=3 has no eligible graph, while n=4 has the numerical answer 12 without the undefined C1 notation.

## 3. Exact M and the mixed-parity formulas

Definition 12 (p. 7) uses the one-vertex wedge operation \(\vee\), not a complete graph join:

\[
G_n=\begin{cases}
C_{k+1}\vee C_{k-1},&n=2k-1,\ k\text{ even},\\
C_k\vee C_k,&n=2k-1,\ k\text{ odd},\\
C_{k+1}\vee C_{k-1}\vee e,&n=2k,\ k\text{ even},\\
C_k\vee C_k\vee e,&n=2k,\ k\text{ odd}.
\end{cases}
\]

Here e is a single extra edge attached by a wedge. Applying the cycle formula and multiplicativity gives the arithmetic expression on p. 9:

\[
M(2k-1)=\begin{cases}
(k+1)(k-1)\binom{k}{k/2}\binom{k-2}{(k-2)/2},&k\text{ even},\\
k^2\binom{k-1}{(k-1)/2}^{\!2},&k\text{ odd},
\end{cases}
\quad M(2k)=2M(2k-1).
\]

For equal-parity positive a>=b>=c, Proposition 22 (p. 12) gives

\[
F(a,b,c)=\sum_{j=0}^{c}\binom cj
\binom b{(b-c)/2+j}\binom a{(a-c)/2+j}.
\]

The source sorts arguments before evaluating F. Its positive-length formula does not itself define F on zero or negative lengths. Extending a centered-binomial definition to nonnegative rows is possible, but any such extension must be stated and justified separately.

The two parts of Corollary 25(ii), p. 15, are:

\[
\begin{aligned}
N(CB(o_1,o_2,e))&=eF(o_1,o_2,e-1)+o_1o_2F(o_1-1,o_2-1,e),\\
N(CB(e_1,e_2,o))&=oF(e_1,e_2,o-1)+e_1e_2F(e_1-1,e_2-1,o).
\end{aligned}
\]

All three lengths in these two formulas must be at least 2; letters o and e designate odd and even integers. Consequently every odd length in this part is at least 3.

For a single path of length 1, Corollary 25(iii)-(iv) instead gives

\[
\begin{aligned}
N(CB(e_1,e_2,1))&=e_1e_2F(e_1-1,e_2-1,1)+N(C_{e_1}\vee C_{e_2}),\\
N(CB(e,o,1))&=eF(e-1,o,1)+oN(C_{o-1}\vee C_e),\qquad o\ge3.
\end{aligned}
\]

The cycle terms are evaluated by

\[
N(C_r)=\begin{cases}\binom r{r/2},&r\text{ even},\\
r\binom{r-1}{(r-1)/2},&r\text{ odd},\end{cases}
\quad N(A\vee B)=N(A)N(B).
\]

The C2 occurrences in these contracted expressions have the expressly discussed single-edge labeling meaning. Corollary 25(v) also prints a formula for CB(e,1,1); it is not a legitimate additional family in the simple bicyclic domain described above.

An equivalent zero-row extension is not silently assumed in any claim here. In particular, the exterior length coefficients in the two mixed-parity terms remain part of N; inequalities for F alone do not prove inequalities for this weighted sum.

## 4. What would close Conjecture 13

The original assertions relevant to the reduction are:

| Source | Assertion used |
| --- | --- |
| Theorem 14, p. 7; proof pp. 10-11 | N(H)<=M(n) for connected n-vertex, n+1-edge graphs with two edge-disjoint cycles |
| Theorem 18, p. 8 | 2M(n)<=M(n+1) |
| Corollary 19, p. 11 | Deleting a leaf reduces both vertex and edge counts by one and divides N by 2 |
| Theorem 27, p. 17 | F(a,b,c)<=M(n) when n>=4, a+b+c=n+1, and the positive lengths have the same parity |
| Conjecture 32, p. 24 | The corresponding inequality for mixed-parity CB |

For completeness, the relevant graph reduction can be checked without interpreting a drawing. Repeated leaf removal preserves the cyclomatic number two. In the remaining minimum-degree-two connected core,

\[
\sum_v(\deg(v)-2)=2.
\]

Thus the core has either one degree-four vertex or two degree-three vertices, with all other vertices of degree two. Suppressing degree-two paths gives either a configuration with two edge-disjoint cycles or three paths joining two branch vertices. The former is already covered by Theorem 14; the latter is the theta case. Reattaching removed leaves is controlled by Theorem 18. For n>=5 the graph in Definition 12 is a genuine simple graph and gives equality in the proposed maximum. The n=4 case is the explicit K4-minus-an-edge calculation above.

Accordingly, proving the simple-domain version of Conjecture 32, together with these existing results, establishes the intended bicyclic maximum. The equal-parity transfer conjecture is neither the sole missing step nor a replacement for the mixed-parity weighted inequality.

## 5. The stronger proposed theta maximizers

Conjecture 33 (p. 24) asserts a maximum over triples with a+b+c=n+1 for n>=10. It does not assert that the listed maximizer is unique. Its four listed triples are

| Vertex parameter | Proposed maximizing triple |
| --- | --- |
| n=2k-1, k even | (k-1,k-1,2) |
| n=2k-1, k odd | (k,k-2,2) |
| n=2k, k even | (k,k,1) |
| n=2k, k odd | (k+1,k-1,1) |

All four are mixed-parity simple theta graphs in the stated n>=10 range. The source reports checking n+1<=535. Such computations are evidence reported by the authors, not executions performed here.

The even-n upper bounds for the two listed candidates are already the content of Proposition 30. Its printed proof contains incorrect intermediate and final identities. `PROPOSITION30_CORRECTION.md` gives the corrected algebra and finite definition-based checks. The proposition's inequality survives the correction. A correction to those identities should not be presented as a first proof of the proposition's conclusion.

## 6. Mori-Mori-Ohsugi: precise comparison

Aki Mori, Kenta Mori and Hidefumi Ohsugi, *Number of facets of symmetric edge polytopes arising from join graphs*:

- arXiv: <https://arxiv.org/abs/2312.11287>, v1 18 December 2023, v2 24 January 2025, v3 30 April 2025.
- Latest accessible full text: <https://arxiv.org/html/2312.11287v3> and <https://arxiv.org/pdf/2312.11287v3>.
- Journal: *European Journal of Combinatorics* **127** (June 2025), Article 104165, <https://doi.org/10.1016/j.ejc.2025.104165>.
- Publisher record: <https://www.sciencedirect.com/science/article/pii/S0195669825000484>.

The full v3 preprint was read; v1/v2 were retrieved for version comparison. A comparison of pdftotext output for v2 and v3 found only the arXiv version stamp and Kenta Mori's affiliation changed. The publisher record and its indexed contents identify the same title, authors, journal and join-graph scope. Direct publisher PDF/XML retrieval returned a site-unavailable response, so a line-by-line comparison with the version of record was **not** completed. No unobserved journal-only strengthening is ruled out by that partial access.

In this paper, G1+G2 adds every cross edge between the disjoint vertex sets. This is explicitly distinguished from the one-vertex 1-sum/wedge. Theorem 1.4, p. 3, proves the *global* Braun-Bruegge Conjecture 2 bounds for this graph class:

\[
N(G)\le\begin{cases}6^{(n-1)/2},&n\text{ odd},\\
14\,6^{n/2-2},&n\text{ even}.
\end{cases}
\]

These are not the fixed-edge-count bound M(n). Proposition 2.11 reduces those global bounds to blocks, and Proposition 2.6 treats bipartite graphs. Neither removes the mixed-parity theta case merely by its statement.

There is a direct scope exclusion. A simple three-path theta has exactly two degree-three vertices; every other vertex has degree two. If it were A+B, both |A| and |B| would be at most 3. For n>=7 this is impossible. For n=6 the only possible split is 3+3, forcing every vertex to have degree at least 3, also impossible. For n=5 the only split is 2+3, and the degree sequence forces exactly K2,3=CB(2,2,2), which is bipartite. Therefore **every mixed-parity simple theta on at least five vertices has connected complement** and is outside that join-graph theorem's input class. It is also 2-connected, so the block reduction does not split it further.

This argument excludes a direct application of the specified follow-up theorem. It is not a universal claim that no other method or later paper proves the target.

## 7. Search coverage and bounded conclusion

Two web search engines were used on 2026-10-12. Queries covered the exact Braun-Bruegge title; combinations of the authors with Conjectures 13, 32, 33 and preprint numbers 3.4, 5.2, 5.3; theta/bicyclic/sparse graph facet terminology; erratum/correction; and the exact Mori-Mori-Ohsugi title and DOI. A recency-filtered query included the 2025-2026 period. Primary pages consulted also include:

- Braun's publication list: <https://sites.google.com/view/braunmath/mathematical-work>.
- Braun's IPAM 2025 slides: <https://helper.ipam.ucla.edu/publications/ACD2025/ACD2025_20597.pdf>. The final slides still label the equal-parity F-transfer statement as a 2023 conjecture; they do not establish the current status of Conjectures 32-33.
- Bruegge's 2023 dissertation record: <https://uknowledge.uky.edu/math_etds/102/>; direct full-text retrieval was blocked. Its chapter-level theta material was not treated as independently read.
- The related Braun-Bruegge-Kahle paper: <https://dmtcs.episciences.org/en/articles/9925> (random graph facets and clustering; its scope is not the exact theta extremum).
- The 2026 Mori-Mori-Ohsugi poset paper: <https://link.springer.com/article/10.1007/s00454-026-00879-x>. Its stated main theorem concerns twinned chain polytopes; no theta-M(n) bridge was obtained from it.

An OpenAlex citation query for the preprint was used only as a discovery aid, not as an authoritative proof of completeness. It yielded five indexed citing records: a volume-count paper, a regular-matroid generalization, the random-graph paper, an Oberwolfach report, and the join-graph paper. Citation indexing is incomplete and may split preprint and journal records.

A final targeted search pass used the queries `"Braun" "Bruegge" "Conjecture 32" solved binomial Vandermonde`, `"Braun" "Bruegge" "Conjecture 13" proof bicyclic facets`, and `"symmetric edge polytopes" "theta" "central binomial"`. No matching theta upper-bound proof appeared in the returned results. The results included the join-graph paper, random-facet work, and papers on Ehrhart theory and generalized symmetric edge polytopes. Those nearby titles were not treated as equivalent solutions solely because they involve the same polytope family.

**Bounded outcome:** no equivalent proof of Conjectures 32 or 33 was identified in the inspected primary material and search results. The specified join-graph follow-up does not directly cover the mixed-parity theta domain, for the proved degree reason above. This permits further mathematical work with a provisional literature gate; it does not justify the phrases "still open as of today", "first solution", or "no previous solution" without further evidence.
