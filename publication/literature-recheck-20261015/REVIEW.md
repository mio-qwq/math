# Literature and originality recheck of two graph-theory preprints

Review date: **15 October 2026**. Manuscripts reviewed: **version 0.3** of *A sharp lower general-position bound for Cartesian products* and *A structural obstruction to (1,1,3,3,4)-packing colorings*.

The reviewed files are fixed by repository commit [`35dacdc7cdc767c0591c60b79c5bae51e8b42b01`](https://github.com/mio-qwq/math/commit/35dacdc7cdc767c0591c60b79c5bae51e8b42b01). [BINDINGS.json](BINDINGS.json) records their exact TeX, PDF, source-archive and reproducibility-archive SHA256 values; [SHA256SUMS](SHA256SUMS) binds this report and its version record.

## Assessment

The searches and comparisons described below did **not identify and verify an earlier public answer covering the main claims of either manuscript**. The preceding qualified originality assessment is unchanged. No literature overlap requiring withdrawal of a main claim was established in this review.

This is a bounded, AI-assisted literature assessment. It does not certify historical priority, external human peer review or a text-similarity percentage. Residual originality risk remains **moderate and unresolved**, reflecting mature underlying methods, possible parallel work, incomplete indexing and access limitations. This review does not claim new Lean compilations, new mathematical executions or a fresh independent audit of the proofs.

## Lower general position in Cartesian products

### Original statement and current versions

The [arXiv record for 2404.19451](https://arxiv.org/abs/2404.19451) displayed only v1, submitted on 30 April 2024. The product conjecture is Conjecture 2.10 in the [preprint](https://arxiv.org/html/2404.19451v1), and Conjecture 3 on printed page 117 of the [published article](https://oro.open.ac.uk/98050/9/98050final.pdf), DOI [10.22049/cco.2024.29171.1879](https://doi.org/10.22049/cco.2024.29171.1879).

The parameter minimizes the cardinality of an inclusion-maximal general-position set. It must be distinguished from ordinary GP maximization, terminal-set parameters and mutual visibility. The review compared the manuscript with that precise statement, including the graph assumptions.

The [record for *The General Position Problem: A Survey*](https://arxiv.org/abs/2501.19385) displayed v5, revised on 16 August 2026. Its [Conjecture 5.14 and final problem list](https://arxiv.org/html/2501.19385v5) still reproduced the product conjecture. This is evidence about that version of the survey, not proof that no later solution exists.

### Comparisons and contribution boundaries

| Material checked | Existing result or method | Relationship to the manuscript |
| --- | --- | --- |
| [Di Stefano et al., 2306.09965v2, Theorems 5.3 and 5.4](https://arxiv.org/html/2306.09965v2) | Exact lower-GP formulas for products of complete graphs | The familiar complete-factor equality cases are prior results. The direct-product formula with a cap of four concerns a different graph operation; it is not the manuscript's universal Cartesian-product theorem. |
| [Brešar and Yero, 2307.02951v2, Section 2.2, Proposition 5](https://arxiv.org/html/2307.02951v2) | Clique enlargement and comparison of lower mutual visibility with lower GP | These are prior methodological context. The manuscript does not claim to invent true-twin enlargement or these established parameters. |
| Original product paper | Gap examples involving lower terminal parameters | Those factor parameters differ from the lower-GP parameters in the manuscript's counterexample family. |
| [James Tuite's institutional profile](https://profiles.open.ac.uk/j-tuite) and [Sandi Klavžar's paper list](https://users.fmf.uni-lj.si/klavzar/papers-all.htm) | Public author bibliographies and related work | Relevant entries were checked; neither page was treated as an exhaustive, continuously updated publication database. |

No same-scope earlier answer was identified and verified for the fixed counterexample, arbitrary-gap family or sharp universal replacement bound in this search. The particular construction and reduction must be distinguished from the established tools they use.

The manuscript's fixed 319-vertex counterexample has a Lean proof. The all-parameter family and universal corrected bound have written/computer-assisted proofs; this report does not extend their formalization scope.

## Claw-free subcubic packing coloring

### Original statement and current versions

The [arXiv record for 2608.02566](https://arxiv.org/abs/2608.02566) displayed only v1, submitted on 3 August 2026. The target is [Section 6, Problem 1](https://arxiv.org/html/2608.02566v1#S6), concerning `(1,1,3,3,4)`-packing colorability of connected claw-free subcubic graphs other than the specified exception.

The preceding paragraph of the original paper already supplies a noncolorability example for `(1,1,3,3,5)`. Failure for radius five does not by itself establish failure for the weaker radius-four requirement. Conversely, the original positive `(1,1,3,3,3)` theorem is compatible with the manuscript's obstruction.

### Comparisons and contribution boundaries

| Material checked | Existing result or method | Relationship to the manuscript |
| --- | --- | --- |
| [Brešar, Kuenzel and Rall, 2409.15455v1](https://arxiv.org/html/2409.15455v1) | `(1,1,2,2)` colorability and standard claw-free cubic structures | Rings of diamonds and triangle replacement are existing constructions. The palette differs from the manuscript's target. |
| [Mortada and El Zein, 2512.24001v1](https://arxiv.org/html/2512.24001v1) | Shorter proof of `(1,1,2,2)` colorability | Related positive result, not a same-scope counterexample or a new contribution of this manuscript. |
| [Anderson, Kuenzel and Marcano Cuellar, 2607.25198v1, Theorem 4](https://arxiv.org/html/2607.25198v1) | `(1,1,2,3)` colorability of diamond-free, claw-free cubic graphs | Different distance sequence; consistent with the five-label obstruction. |
| [El Zein and Mortada, *A step toward an S-packing coloring conjecture for subcubic graphs*, AJC 95(3) (2026), 459–467](https://ajc.maths.uq.edu.au/pdf/95/ajc_v95_p459.pdf) | A local-girth condition giving `(1,2,2,2,2,2)` colorability | The abstract, main theorem and final problem were checked; their scope does not coincide with the manuscript's negative result. |
| [El Zein and Mortada, 2603.25113v1](https://arxiv.org/html/2603.25113v1) | Local-girth/saturation results and related conjectures | Relevant conclusions and open-problem sections were compared, without treating different palettes or hypotheses as interchangeable. |

No same-scope earlier negative answer covering the manuscript's radius-four obstruction was identified and verified in this search. No claim to a smallest counterexample, an exhaustive classification or historical firstness follows from this assessment.

Lean covers the fixed 36-vertex instance. The odd-parameter family and diamond-freeness are established in the written proof, not by a universal Lean theorem.

## Search method and limitations

Searches combined exact titles and identifiers, author names, statement fragments and terms including `counterexample`, `correction`, `erratum`, `refutation`, `sharp` and `solution`. Alternate spacing of packing sequences and adjacent terminology were compared. Representative executed queries included:

- `"Lower general position in Cartesian products" counterexample`
- `"lower general position" "Cartesian" correction OR refuted OR sharp`
- `"lower general position" "product" "sharp" "five"`
- `"2404.19451" site:github.com`
- `"2608.02566" correction OR erratum OR counterexample`
- `"(1, 1, 3, 3, 4)" "claw-free"`
- `"packing colorings" "Mortada" "counterexample"`
- `"2608.02566" site:github.com`

Supplementary searches included a recent-date filter. Search-engine misses were not treated as proof of absence. Unrelated results and this project's own material were not counted as independent prior work. The GitHub-limited queries were not an exhaustive examination of public proof repositories.

Direct retrieval of the original journal DOI landing page and [Togni's publication page](https://o.togni.u-bourgogne.fr/index.php?n=Research.Publications) was unavailable during the review. The published lower-GP article was checked through its Open University full-text copy. The USAL faculty page was accessible but was not treated as a complete bibliography. DBLP was used only as a discovery aid because its visible author data could lag behind recent work.

The review did not exhaust subscription databases, nonindexed preprints, private manuscripts, all code repositories or all equivalent formulations. No commercial text-similarity service was run. The report therefore supports continued, qualified manuscript preparation rather than a global priority claim. Newly located same-scope work would require renewed comparison and, where appropriate, revised attribution.

## Manuscripts and reproducibility materials

- [Lower-GP version 0.3](../lower-gp-cartesian-v0.3/README.md)
- [Packing-coloring version 0.3](../clawfree-packing-v0.3/README.md)

This report supplements the preserved originality reports in the reproducibility archives. It does not replace their dated evidence or alter the frozen manuscript files.
