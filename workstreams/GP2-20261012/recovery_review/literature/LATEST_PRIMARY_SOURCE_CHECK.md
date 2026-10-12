# GP2 primary-source and novelty gate after recovery

Checked 2026-10-13, Asia/Singapore (2026-10-12 UTC). Reviewer scope:
literature only. The GP2 mathematical inequalities are not independently
accepted merely by this source check. The source checkout initially had HEAD
`2e920b20a297fc471c833858cc858f84c4d8f24e`; the parent agent owns delivery,
proof acceptance and publication.

## Original problem and latest directly read author statement

The official arXiv abstract record for *The general position number of
digraphs*, [2604.15909](https://arxiv.org/abs/2604.15909), still displays only
v1, submitted 2026-04-17 10:10:49 UTC. Its
[v1 HTML](https://arxiv.org/html/2604.15909v1) was read again at Definition
2.1, Section 3.2, Table 1 and Problem 5.2. Problem 5.2 reads:

> Find a formula for the general position number of any tree, as well as permutation digraphs and Kautz digraphs for $k\geq 3$.

The graph parameter `m` is the total alphabet size. Adjacent letters are
different; arcs delete the first letter and append a different last letter.
General position excludes a third selected vertex from every shortest
directed path between selected endpoints. The original paper allows digons.
Its computed values `gp(Ka(3,4))=7` and `gp(Ka(4,4))=27` are prior results.

The official record of *The General Position Problem: A Survey*,
[2501.19385](https://arxiv.org/abs/2501.19385), still has latest v5, revised
2026-08-16 16:08:22 UTC. In the directly read
[v5 HTML](https://arxiv.org/html/2501.19385v5), Section 5.6 explains that
the Kautz value beyond word length two is unclear, and Section 6 again lists
determining the values for word lengths at least three as a research problem.
Its reference [25] identifies 2604.15909.

**Conclusion:** these official, dated author statements support continued
research on Ka4. No later public solution was located in this check. They
do not certify that the problem remains open in all published, unindexed,
unpublished or private work as of the retrieval date.

## Direct comma-free source coverage

| Primary source | Directly checked location | Mathematical relevance |
| --- | --- | --- |
| Golomb, Gordon and Welch, *Comma-Free Codes*, Canadian J. Math. 10 (1958), 202–209, [DOI](https://doi.org/10.4153/CJM-1958-023-9), [PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B78C35132E2BCD4A14459BE6A142FF30/S0008414X00045296a.pdf/comma-free-codes.pdf) | Theorems 1 and 5–7, printed pp. 202–203, 207–208 | Primitive-rotation upper bound, ordinary-code density-limit existence and classical length-four lower coefficient `2/9`. Alphabet blow-up is classical. |
| Jiggs, *Recent Results in Comma-Free Codes*, Canadian J. Math. 15 (1963), 178–187, [DOI](https://doi.org/10.4153/CJM-1963-021-1), [PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3F80EAEA1B86983AF9CCBB3410B93FF9/S0008414X00029382a.pdf/regent_results_in_commafree_codes.pdf) | Theorem 5, Section 3 and Section 5, printed pp. 183–186 | The 57-word four-letter dictionary is historical. For alphabet size and word length both four, cardinality greater than 56 forces disjoint initial/final trigrams. Section 5 improves a different even-length lower bound; it does not state the GP2 optimized weighted coefficient. |
| Tang, Golomb and Graham, *A New Result on Comma-Free Codes of Even Word-Length*, Canadian J. Math. 39(3) (1987), 513–526, [DOI](https://doi.org/10.4153/CJM-1987-023-7), [PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/71A7831337DAC1E7D03DF9AE4C096F08/S0008414X0000448Xa.pdf/a-new-result-on-comma-free-codes-of-even-word-length.pdf) | Introduction, Theorem 1.1 and comparison/compatibility-vector construction | Its threshold obstruction to representing every primitive rotation orbit is not automatically a positive limiting density loss. It confirms the historical value `W_4(4)=57<60`. |
| Fimmel, Michel, Pirot, Sereni and Strüngmann, *Diletter and triletter comma-free codes over finite alphabets*, Australasian J. Combin. 86(2) (2023), 233–270, [publisher PDF](https://ajc.maths.uq.edu.au/pdf/86/ajc_v86_p233.pdf), [author-hosted PDF](https://dpt-info.di.unistra.fr/~c.michel/Michel_Article93.pdf) | Printed pp. 236–238 and 245, Definition 2.1 and Section 4.1 | It explicitly says the even-length leading coefficient is undetermined. Its principal exact cardinality results concern lengths two and three. Strong comma-free means no proper prefix/suffix overlap and is a stricter class. The paper also recalls the classical split-graph characterization below. |
| Fimmel, Michel and Strüngmann, *n-Nucleotide circular codes in graph theory*, Phil. Trans. R. Soc. A 374 (2016), 20150058, [author-hosted PDF](https://dpt-info.di.unistra.fr/~c.michel/Michel_Article71.pdf) | Definition 2.1, Theorems 2.6 and 2.11, Appendix B | Codeword splits produce a directed graph; circularity is acyclicity and comma-freeness prohibits paths of length three. The literal statement of Theorem 2.11 says length equals two, whereas its proof and the 2023 account use at most two; singleton/strong codes require the latter formulation. |
| Stanovnik, Moškon and Mraz, *In search of maximum non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299–1326, [primary full text](https://link.springer.com/article/10.1007/s10623-023-01344-z) | Definition 1, Section 5 and Theorem 19 | For the stronger non-overlapping class, length-four maximum is `r^3(q-r)`, with `r` nearest to `3q/4`, half rounded down. Its limiting density is `27/256`. This is not a valid upper bound for all ordinary comma-free codes or GP2 strict codes. |
| Stanovnik, *Codes with restricted overlaps: expandability, constructions, and bounds*, Journal of Applied Mathematics and Computing 71 (2025), 591–616, [primary full text](https://link.springer.com/article/10.1007/s12190-025-02441-z) | Abstract, introduction, Definition 1 and references | Its forbidden proper prefix/suffix overlaps are not the GP2 strict-window definition. No arbitrary ordinary length-four comma-free upper bound replacing GP2's stated bound was identified in the inspected portions. |

The 2023 publisher PDF initially failed to open directly, but its Journal
link from [Sereni's official publication page](https://irma.math.unistra.fr/~sereni/pub-journals.html)
worked. [Michel's official page](https://dpt-info.di.unistra.fr/~c.michel/)
provided the accessible author PDF. Thus the leading-coefficient sentence was
directly reread in this pass, rather than taken on trust from the old gate.

## Important prior structural representation

The 2023 Section 4.1, attributing the method to the 2016 paper, gives a graph
`G_X` with vertices all nonempty proper words and arcs `u -> v` whenever
`uv` is a selected codeword. For ordinary comma-free codes this graph is
acyclic and its longest directed path has length at most two. Consequently
a three-level representation of its word states is available.

For word length four, the split types are `1+3`, `2+2` and `3+1`. Thus the
basic use of three layers on two-letter states should be attributed to the
existing code-theoretic framework. A new reciprocal-pair density inequality
can still be a separate contribution; its novelty must not be conflated with
the layer representation itself. Joint constraints from all split types are
a natural route to inspect in the continued research.

That last route suggestion is this reviewer's inference, not a result claimed
by the cited papers. The split graph controls ordinary comma-freeness; it
does not by itself encode all stricter GP2 five-window constraints or prove
that a fixed number of alphabet blocks suffices.

## Bounds and provenance conclusions

1. The classical rotation upper bound `(m^4-m^2)/4`, the coefficient `2/9`,
   and the literal 57-word dictionary are not new GP2 discoveries.
2. The inspected classical sources imply ordinary comma-free lower density
   at least `57/256` by the historical dictionary and the historical blow-up
   method. GP2's transfer to Kautz GP requires its additional strictness and
   valid-word checks; ordinary comma-freeness alone does not establish it.
3. No prior instance of `182/729`, the decimal `0.249657...`, or the exact
   fixed-Jiggs weighted optimum `0.224808115...` was located by the searches
   actually run. No stronger arbitrary ordinary length-four upper bound was
   identified in the directly read sources. **This is bounded search
   non-detection, not certified first discovery or best-known status.**
4. Weighted alphabet blow-ups are an elementary extension of classical
   blow-up constructions. The exact optimizer of one historical dictionary,
   a genuinely new code inequality, and the original-GP repair/bridge are
   separate provenance questions and should be described separately.
5. The project-recorded interval remains subject to the parent agent's
   independent mathematical acceptance. Nothing in this literature check
   supplies the exact value of `lambda_4` or upgrades a six-letter fixed-label
   certificate to a uniform bound.

## Access gaps and citation-network limits

Levenshtein, *Combinatorial problems motivated by comma-free codes*, Journal
of Combinatorial Designs 12(3) (2004), 184–196,
[publisher abstract/reference page](https://onlinelibrary.wiley.com/doi/abs/10.1002/jcd.10071),
was read. It records first publication 2004-01-26. The
[institute catalog](https://library.keldysh.ru/prep_vw.asp?lg=e&pid=2330)
was read and links the [2003 manuscript PDF](https://keldysh.ru/papers/2003/source/article/golomb4.pdf).
Both institute PDF and Wiley PDF still failed (502 and 503 respectively).
No unchecked theorem from that full text is imported.

The original arXiv citation outlinks to Semantic Scholar, Google Scholar and
ADS failed (unreadable redirect, bot challenge and 405 respectively). A
complete forward-citation network was therefore not obtained. Search-engine
title/identifier and phrase searches found the original paper, author survey,
mirrors and related coding papers, but no directly relevant later Ka4
solution. Mirrors were discovery aids, not mathematical sources.

The contemporaneous `SEARCH_LOG.json` records queries, source URLs, access
outcomes and transient browser references. These references are useful only
within the current session; URLs, dates and pinpoint locations are the
durable provenance. Do not claim all databases or all author manuscripts have
been checked.
