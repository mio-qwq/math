# Manuscript verification record

Review date: 9 October 2026. Status: scientifically checked **public research draft**. Human author identity and accountable human approval remain pending; this is not an arXiv submission, journal acceptance or human peer-review report.

The manuscript is [main.tex](main.tex); the corresponding 14-page artifact is [paper.pdf](paper.pdf). The mathematical source baseline is [commit 613108f1fa107a88a1049ed5f25e6b9313d576ed](https://github.com/mio-qwq/math/tree/613108f1fa107a88a1049ed5f25e6b9313d576ed/006-strong-product-packing-counterexample). The [machine-readable build receipt](verification.json) identifies the final source and PDF bytes.

## Written proof and exact conjecture

The complete written argument proves

\[
\gamma_2^3(Q_6)=\infty,\qquad \gamma_2^3(Q_6\boxtimes H)\le64.
\]

The graph \(H\) is finite, nonempty, connected, simple and undirected, with 608 vertices and 9,168 edges. Its adjacency is constructed from singleton and distance-four pair supports. The proof checks the entire single-factor obstruction, all possible short paths between code vertices, and all three auxiliary vertex types. The same selected label covers both product coordinates. Connectedness and the edge count have explicit written proofs; the manuscript does not require a program to supply a missing mathematical step.

This contradicts the exact one-bad-factor implication of Conjecture 3.1 in [arXiv v1](https://arxiv.org/html/2510.02749v1) and the [published article](https://doi.org/10.1007/s00026-026-00814-0). An independently assigned AI reviewer rederived the factor obstruction using eight explicit omitted words, the support construction, all coverage cases and the edge count, then read the complete final manuscript. No substantive mathematical must-fix was identified. This AI review is distinct from human peer review.

The witness has 64 centers; its optimality is not proved. The separate nonlinear \(Q_6\boxtimes Q_6\) problem is not settled by this construction.

## Actual Lean evidence

The three mathematical sources are unchanged from the already checked baseline. The pinned environment is Lean `4.34.1` and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`. A separately executed fresh-object rebuild compiled the factor, geometry and actual-graph modules in dependency order with exit code zero, no Lean warnings or errors, and respectively 12, 12 and 26 printed axiom audits. These are 50 declaration audits, not a count of new mathematical theorems. Source-specific receipts, UTC intervals, object hashes and all audit outputs are retained in [the public Lean record](../results/lean-verification.json).

The final theorem `Q6PackingComplexCounterexample.original_existence_counterexample` states arbitrary-set factor nonexistence and product existence on actual finite `SimpleGraph` objects with standard Mathlib `Walk`s. The padded-reachability bridge is proved for every length bound and does not add graph loops. The strong-product definition is proved equivalent to the ordinary three edge cases. The endpoint has no additional geometry or external-certificate hypothesis. Its only axioms are `propext`, `Classical.choice` and `Quot.sound`. No `sorry`, `native_decide`, added axiom, Python certificate or solver oracle supplies a proof.

The auxiliary cardinality 608 is kernel checked. A numerical gamma-minimum function, connectedness of \(H\), its 9,168 edges and its exact diameter are not additional Lean endpoints in this version. The written cardinality argument supplies the explicit upper bound 64. The paper carefully separates these boundaries from the fully checked existence assertion.

## Exact-program evidence

The [primary checker](../verify_graph.py) and [separate reconstruction](../verify_independent.py) use integer and set operations. The first computes all 64 cube BFS rows and 64 auxiliary BFS rows from the code vertices. The second reconstructs the graph before reading the first checker's artifacts, checks all 184,528 unordered candidate edges, and performs all 608 auxiliary BFS rows, yielding 369,664 distances. It independently validates shortest distances using edge Lipschitz bounds and descending-neighbor paths.

Both implementations check all 2,016 center pairs and all 38,912 product targets with a single label satisfying both distance bounds. Subsequent artifact comparison matches the entire graph and certificate. These checks use the proved maximum-of-factor-distances formula; no full all-source BFS of the 38,912-vertex product is claimed. [Public comparison evidence](../results/independent-certificate-comparison.json) and the [replay instructions](../README.md) retain the precise assertions and source hashes. The finite outputs supplement the written proof and do not establish historical originality.

## Literature and attribution

A separately assigned AI literature reviewer checked all ten bibliography entries against primary publisher, arXiv or Crossref records, the original conjecture and relevant related theorems. Multiple identifier, author, terminology and support-construction searches did not locate a verified earlier complete result subsuming this construction. The 2009 perfect-code inheritance theorem concerns disjoint radius balls at \(p=2d\); this example uses \((d,p)=(2,3)\) with overlaps. The close-vertex theorem has a hypothesis absent from \(H\).

Historical firstness remains **unknown**. The searches do not exhaust the historical citation graph, differently named or unindexed work. Fisher's complete 1994 article and Plotkin's original full text were not accessible to the literature reviewer; their metadata and the manuscript's limited attributions were checked. The manuscript supplies its own complete Plotkin counting argument and product-distance proof. The 1994 Beineke–Henning publisher scan was separately read in full for the origin of the joint notion. The final bibliography fixes the conjecture-bearing arXiv v1 and the exact mathematical repository baseline.

## PDF build and visual inspection

The final source SHA256 is `2207f48d3dc5d3481a02a21ee16b35f1a3820860c6826c96b8391ffc02e07b3b`; it was unchanged before and after compilation. The PDF SHA256 is `ce38ceca74e055c4e14c1f4ad65bb4cf665a2435d779ea65aef8a4c6580bf383` (124,128 bytes). Tectonic `0.17.0+20260731` completed with exit code zero from **2026-10-09T08:36:32.9113124Z** to **2026-10-09T08:36:34.5880059Z**, including the required TeX rerun.

All final pages 1–14 were rendered with Poppler at scale-to 1600 and individually visually inspected by the primary AI agent. No clipping, overlapping text, missing visible glyphs, dangling reference or table overflow was observed. PDF parsing confirms 14 nonempty text pages, no Unicode replacement characters, all 20 fonts embedded, and the two final pinned bibliography links. The TeX log contains no warning, unresolved reference, overfull box, underfull box or missing-character diagnostic.

The engine emitted a nonfatal `Fontconfig error: Cannot load default config file` startup message. Two earlier built-in-editor compilation attempts failed with `Unable to find standard directories for platform`; neither is represented as a successful compile. The existing app-bundled executable then exported the checked PDF without installing a TeX distribution or changing system settings. Reproduction can use `tectonic main.tex` or two ordinary `pdflatex` passes with the listed standard packages. Different engine versions or creation timestamps may change PDF bytes even when the mathematical source is identical.

## AI participation and human responsibility

The manuscript discloses substantial OpenAI Codex / GPT-6-based agent-system participation in construction, derivation, Lean source, exact-checker implementation, literature search, AI-agent review and writing. AI is not listed as an author, and no artificial human-independent research history is supplied. See Section 11 of the manuscript.

Human authorship, actual responsible human examination and consent, and the applicable venue's policies must be resolved before any external submission. [arXiv's policy](https://info.arxiv.org/help/moderation/index.html), [Annals guidelines](https://link.springer.com/journal/26/submission-guidelines) and [Springer Nature's current guidance](https://group.springernature.com/gp/group/ai/ai-guidance-for-researchers-editors-reviewers) are separate requirements; truthful AI disclosure alone does not establish eligibility. No external submission or contact is claimed.
