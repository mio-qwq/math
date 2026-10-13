# Originality and source review — lower general-position Cartesian products

Review date: 12 October 2026. Manuscript: private version 0.1.
Mathematical baseline: `61488e05c9fe41984f483853f99e79f5715dc893`.
The exact manuscript and supplement hashes are listed in the delivered manifest.
This is a literature and mathematical comparison, not a plagiarism-detector
score or a certification of historical priority.

## Original problem and version comparison

Eartha Kruft Welton, Sharif Khudairi and James Tuite, *Lower general position
in Cartesian products*, Communications in Combinatorics and Optimization
10(1) (2025), 110–125, DOI
[10.22049/cco.2024.29171.1879](https://doi.org/10.22049/cco.2024.29171.1879).

- [Original preprint, arXiv:2404.19451v1](https://arxiv.org/html/2404.19451v1):
  Conjecture 2.10.
- [Published text hosted by the Open University](https://oro.open.ac.uk/98050/9/98050final.pdf):
  Conjecture 3, printed page 117.
- The conjectured conclusion is `gp⁻(G □ H) ≥ min{gp⁻(G),gp⁻(H)}`.
  Its parameter is the minimum cardinality of an **inclusion-maximal**
  general-position set, not the maximum GP number or lower terminal number.
- Both factors in our counterexample are finite, nonempty, simple, undirected,
  connected and of diameter two. Thus the refutation does not depend on a
  disconnected-graph convention or weakening the original assumptions.
- The separately proposed existence of terminal sets is not resolved here.

## Searches actually undertaken

Multiple rounds compared the original and published statements, exact title
and DOI searches, the author institutional page, bibliographies and subsequent
survey material, and searches combining lower general position, Cartesian
product, counterexample, correction, sharp bound and the five-point bound.

Primary material consulted included:

1. The preprint and published paper above, and the
   [arXiv version record](https://arxiv.org/abs/2404.19451).
2. [Recent general-position survey, arXiv:2501.19385v5](https://arxiv.org/html/2501.19385v5),
   with its lower-GP section and references. The
   [author-hosted earlier survey](https://users.fmf.uni-lj.si/klavzar/preprints/2501.19385v2.pdf)
   was also located; that v2 file was not treated as the latest version.
3. [James Tuite's institutional profile](https://profiles.open.ac.uk/j-tuite).
4. Di Stefano, Klavžar, Krishnakumar, Tuite and Yero,
   [*Lower general position sets in graphs*, arXiv:2306.09965](https://arxiv.org/abs/2306.09965),
   published in Discussiones Mathematicae Graph Theory 45 (2025), 509–531.
5. Brešar and Yero,
   [*Lower (total) mutual-visibility number in graphs*, arXiv:2307.02951v2](https://arxiv.org/html/2307.02951v2),
   especially Section 2.2 and Proposition 5; the
   [published record](https://www.sciencedirect.com/science/article/pii/S0096300323005805)
   identifies Applied Mathematics and Computation 465 (2024), 128411.
6. Avis's primary exposition on
   [polyhedral computation](https://cgm.cs.mcgill.ca/~avis/epc/epc.html),
   to distinguish standard ray-generation theory from this application.

No verified earlier answer with the manuscript's complete scope was located
in those searches. This does **not** imply that every paper, nonindexed
preprint, proof repository or unpublished argument was examined. No commercial
text-similarity service was used. Before an external submission, repeat the
exact-statement searches and review any newly identified citations or answers.
An online problem catalogue continuing to label a problem open is not evidence
that an earlier solution does not exist.

## Contribution boundaries

| Item | Relationship to earlier work | What this manuscript establishes | Residual novelty risk |
| --- | --- | --- | --- |
| Connected 11-by-29 counterexample | The cited original paper proposed the opposite bound. | An explicit five-point maximal product GP set with both factor parameters at least six; actual shortest-path Lean verification. | Moderate: no located same-scope precedent, no firstness certification. |
| Family for every integer r ≥ 6 | True-twin saturation and clique enlargement are established mechanisms. Earlier product examples in the original paper use **lower terminal** factor numbers. | Factors of orders 2r−1 and 4r+5, smaller lower-GP number r, product parameter five after the universal lower bound; unbounded additive deficit and ratio tending to zero. | Moderate: the specific family is the contribution, not a claim to invent twin enlargement. |
| Universal min{5,factor parameters} bound | Standard halfspace clipping and metric-cone techniques are borrowed mathematical tools. | A complete equality-pattern relaxation and exact obstruction proof for product maximal sets of sizes one to four, extended to disconnected graphs. | Moderate historical uncertainty; computational proof is explicitly disclosed. |
| Optimal scalar bound | The complete-factor formula is already known in the original paper. | The combination of that formula, the family and the universal theorem determines Φ(r)=min{r,5}. | Do not count the familiar complete-factor cases as a separate new theorem. |
| Fixed Lean formalization | Formal certification is separate from the novelty of the underlying mathematics. | The fixed original-conjecture refutation with semantic bridges to shortest paths, inclusion maximality and the genuine minimum. | No claim of formalizing the entire paper or being the first formalization in history. |

The universal proof is **not** an inference from bounded-order graph searches.
Its finite enumeration follows a proof that the five-point pseudometric cone
covers all required distances. The numeric facts “25 rays” and “9484 patterns”
are computation within standard polyhedral theory, not separately claimed
original discoveries.

## Comparisons that prevent false equivalence

- Ordinary GP maximization differs from lower-GP minimization over maximal
  sets; statements about the former do not settle this conjecture.
- Lower terminal numbers differ from lower-GP numbers. The original paper's
  examples concerning the former do not already supply this refutation.
- Cartesian product `□` differs from categorical/direct product `×`.
  Results giving a lower-GP value four for direct products of complete graphs
  must not be substituted for this manuscript's Cartesian statement.
- General mutual visibility has different quantifiers from general position.
  The cited twin-block constructions supply prior methodological context,
  not an automatic theorem proving the present sharp product bound.

## Editorial treatment

The manuscript attributes known complete-factor results and standard methods,
gives its own proof of each elementary fact it uses, and describes its new
construction and computational reduction without claiming “world first”.
The main text is a new self-contained exposition of frozen project results,
not a claim that additional mathematical discoveries occurred while writing.
AI involvement in discovery, proof, code, formalization, review and prose is
disclosed. No external human peer review or editorial acceptance is claimed.

Overall assessment: **appropriate to prepare an external-readable manuscript;
historical originality remains qualified rather than certified**.

