# Independent AI review of the frozen lower-GP manuscript

Date: 12 October 2026. Reviewer: the independent AI subagent assigned to mathematical and manuscript review. This reviewer did not discover the construction, develop its proofs, integrate the accepted sources, or write the manuscript. This is an AI review, not external human peer review or a certification of originality. This report remains local and private.

## Verdict and exact version

**No blocking mathematical gap, misstatement of the original conjecture, or mismatch between the manuscript and the audited mathematical sources was found.** The frozen version gives a self-contained written counterexample and all-parameter construction, and a complete mathematical reduction for the explicitly computer-assisted universal bound. Its exact finite obstruction is supplied as executable, source-bound code. The manuscript accurately limits the Lean proof to the fixed original-conjecture counterexample.

Acceptance here concerns this private working mathematical manuscript. It does not approve public release, certify human responsibility review, or establish historical priority. In particular, the universal theorem remains computer-assisted rather than fully Lean formalized or purely noncomputational.

The following hashes were computed directly from the actual final files with Python `hashlib.sha256`, rather than copied from a PASS label:

| File | SHA256 |
| --- | --- |
| `paper/main.tex` | `81104eac829996435ed5076a56745c4b5ef2494db33fd9321b76bebfdd97b815` |
| `paper/references.bib` | `012b8a5a1ec7e03b44b44f5e2361bd7b792d07b5217da40543956e0195683ac6` |
| `paper/main.pdf` | `fe923b7017dd04c03126aa07a48c3538a48a31855e4bb2ec973d4f5397392cb4` |
| `REPRODUCE.md` | `213c84f34c048b96d0d7f9adb8d9d70609c98788fc73371ef35b1ef80423e338` |
| `source-bindings.json` | `1822fa4238e449352cc678d5182a42bebdf394b1d2dc0f76931d11ca3b2d6496` |
| `verification/certificate-replay.json` | `e882bc00f0781d977620f7a0817621324eb5bd9b41ad8ed2df5abe15c88e1fe1` |
| `verification/lean-fresh-object.json` | `e1e3cc7e076a9cfceea9390c548e102c859d76d1603e8585e763d18eac7ac859` |
| `verification/lean-fresh-object.log` | `ae4012df450c56958ccf56aef2f014f8724cf629dfe9cf21b3c3ae32093087bf` |
| `verification/latex-compilation.json` | `a89ce6e67d1162aacd17ca8132cfa574211fccc89112c989f2ba75922f94cd4b` |

The mathematical baseline is public repository revision `61488e05c9fe41984f483853f99e79f5715dc893`. All seventeen copied inputs listed in `source-bindings.json` were checked against their actual bytes; every supplied SHA256 matched. The manuscript's Lean source digest is `d1608a26b68eface444fc2c2feb53ebe8b24e364021213f589bd51e3aa52ab3e`.

## 1. Coverage, execution, and final changes

I read the entire English TeX manuscript, including the abstract, preliminary definitions, construction, full proofs, computational reduction, disconnected case, sharpness argument, verification statements, AI declaration, both appendices, and embedded bibliography. I also read all four entries in the separate BibTeX file, the complete reproduction instructions, the source bindings, the new certificate and Lean receipts and their substantive output logs, the final LaTeX compilation receipt, and the structural PDF receipt. TeX label/citation consistency was checked by a small read-only Python control: no duplicate labels, unresolved references, or missing cited bibliography keys were found.

The full mathematical-source audit had already been completed separately in `INDEPENDENT_MATHEMATICS.md`. It covered the specified written proofs, fixed Lean source, exact metric-ray code, profile/demand code, and exhaustive-search code. Its actual bounded controls used three- and four-label cones, small BFS graph products, and artificial Boolean profile systems; they did not constitute the full five-label computation. I did not rerun those controls in this manuscript review. I did not compile Lean or execute the full MET5 or large graph enumerations in either review. ROOT performed the new full replay and fresh-object compilation; I inspected and bound their concrete evidence.

I compared the final TeX against the fully read first frozen TeX retained at `verification/pre-figure-fix/main.tex`, whose hash is `4b544f2f7c89a7f077eecf91fac31bc71631c30bd5c071f07d085225ca068ac2`. The complete difference consists of three changes: the full surname Kruft Welton in the Introduction, separation of the construction figure into two minipages, and the search-state negative-control clarification. No theorem, proof, algorithm, source input, or certificate digest changed. The separate bibliography is unchanged.

I computed the final PDF hash but did not independently inspect every rendered PDF page. Complete visual inspection is ROOT's assigned responsibility. The final structural receipt records thirteen pages and successful Poppler rendering, but its visual-review field was still pending when I read it; structural success is not a substitute for visual review. This report does not claim visual acceptance of the PDF.

## 2. Original question, definitions, and hypotheses

The original question was checked independently against both [arXiv 2404.19451v1](https://arxiv.org/html/2404.19451v1) and the [final journal version](https://oro.open.ac.uk/98050/9/98050final.pdf). The manuscript correctly identifies Conjecture 2.10 in v1 and Conjecture 3 on printed page 117 in the final version. Both ask whether

    gp^-(G □ H) >= min{gp^-(G), gp^-(H)}.

The paper correctly uses the minimum size of an inclusion-maximal GP set, not the ordinary maximum GP parameter or the lower terminal parameter. It connects the actual shortest-path definition to the triangle-equality criterion and proves the one-point maximality criterion using heredity. The Cartesian-product adjacency and connected distance formula are correct.

The source's simple-undirected convention and conjecture contain no extra explicit connectedness or nontriviality qualifier. The manuscript's counterexamples are finite, connected, nontrivial and of diameter two, so they refute the conjecture even under those stronger usual hypotheses. The new universal theorem explicitly states finite nonempty simple undirected graphs and separately handles disconnected graphs; it does not rely on infinite distances being numerical pseudometrics.

The discussion of the original unbounded-gap result correctly distinguishes its lower-terminal factor parameter from the lower-GP factor parameter in the present family. It also leaves the separate terminal-set existence conjecture unresolved.

## 3. Elementary construction and sharpness

The factors and their edge descriptions agree with the frozen source. The true-twin lemma is proved rather than assumed: swapping adjacent true twins preserves all distances to other vertices, and a triple containing both has distances `(1,t,t)` with `t >= 1`, so no triangle equality is introduced.

For `G_r`, the proof classifies all maximal GP sets as the two complete `K_r` blocks and `A union B`, giving sizes `r,r,2r-2` and hence `gp^-(G_r)=r`. For `H_r`, the exact six maximal GP sets among the five landmarks are identified: the two opposite nonadjacent pairs and the four triangles `{z,u_i,v_j}`. Every such landmark set has an outside GP extension. A global maximal set therefore meets an `r`-vertex true-twin clique and contains it, proving the required `gp^-(H_r) >= r`. No unjustified exact value for the second factor is asserted.

The selected five product points have all off-diagonal distances two or three, so no selected triple is collinear. The maximality proof separates first-coordinate roles `c,A,B` and exhausts the second-coordinate landmark/clone roles. Each listed blocking equality is valid; the symmetric cases are justified by the factor's role symmetry. Multiplicity of the clone cliques does not enter these equalities, so the upper bound five is proved for every integer `r >= 6`, rather than inferred from regression samples.

The dependency is stated accurately: the elementary construction alone proves factor growth and product upper bound five, and therefore an unbounded additive deficit and ratio tending to zero. Product equality five uses the universal lower bound. This distinction is preserved in the abstract, theorem qualification, proof, and verification discussion.

For `r=1,...,5`, the complete-factor examples supply the exact equality cases. A GP set with fewer than `r` points in `K_r □ K_r` leaves both a row and a column unused; their intersection has distance two to every selected point and is a valid extension. A full row is maximal for `r >= 2`, and the singleton case is explicitly covered. Together with the constructed family and universal bound, this proves the stated scalar optimum `Phi(r)=min{r,5}`. The known complete-factor formula is credited to prior work.

## 4. Complete reduction of the universal bound

The manuscript supplies the substantive lemmas needed to turn the computation into a theorem. I specifically checked the following possible failure points.

**Repeated coordinate landmarks.** Product vertices are distinct, but either projection may repeat. The manuscript uses pseudometrics, retains zero-distance information and all three triangle-equality roles for every selected pair, and aligns middle labels across factors. Product triangle slacks are sums of two nonnegative factor slacks; equality requires the same middle role in both factors. A candidate coincides with a selected product vertex exactly when the two coordinate zero masks share its index. Thus the two disjointness tests correctly encode a new GP extension, including repetitions.

**No distance cutoff.** With at most four selected labels, an outside factor vertex can occupy label four in `MET_5`, and unused labels can duplicate label zero. This places every actual factor configuration in the five-label cone without any bound on graph order, diameter, or integral distance magnitude. Allowing all cone patterns is a safe enlargement of actual graph configurations.

**Double-description completeness.** The ten coordinate inequalities and thirty triangle inequalities are specified. Every intermediate cone is pointed and full-dimensional, with the all-one vector strictly satisfying its inequalities. The sum-of-coordinates-one section is compact. The minimal common face of two old vertices is defined by their common active inequalities; it is an edge exactly when it contains no third vertex. This justifies the code's active-mask adjacency test. Halfspace clipping keeps feasible old vertices and creates the new vertices on crossing old edges, with the exact integer combination given in the paper. Induction from the orthant therefore covers every extreme ray; the argument does not merely observe the number twenty-five.

**Zero-pattern closure.** Each of the forty forms is nonnegative on every cone ray. A nonnegative ray combination has a zero form exactly when every positively weighted support ray has that zero. Consequently all and only zero patterns are support-mask intersections, including the origin as the empty-support intersection. The queue procedure exhausts this closure and stores exact integer representatives. The numerical count 9484 is computational; the reason that those patterns cover all real pseudometrics is proved in the manuscript.

**Extension demands.** Distinct landmarks are obtained by quotienting zero-distance labels only for the within-factor GP subsets. Every inclusion-maximal GP subset `T` of that distinct landmark set has at most `k` vertices. If the factor lower-GP parameter exceeds `k`, `T` has a one-point extension in the whole factor. No distinct landmark can be that extension, by local maximality. Therefore an actual outside profile must meet every demand. This argument does not incorrectly assume that the projection of the product GP set is itself GP.

**Relaxed profiles and exhaustive search.** The manuscript explicitly admits that profiles sharing only an equality type may not be simultaneously realizable. Their union enlarges the search space, so infeasibility still excludes every actual pair of factor systems. Known profiles are mandatory. Removing an outside profile compatible with any opposite known profile is necessary; after selecting a second-factor profile, deleting first-factor profiles compatible with it is the correct pruning direction. Branching over every profile in an unmet demand lets any hypothetical actual system follow a branch. The state `(U,A)` contains all information relevant to remaining feasibility, so merging equal states is valid. If all second demands are hit and every first demand still meets `A`, taking all first profiles in `A` gives a feasible relaxed system, because no same-factor compatibility is required. Empty demands correctly have no feasible branch.

These arguments cover all unordered type pairs, with factor exchange justifying the reduction to unordered pairs. The aligned zero and triangle-equality filters remove precisely impossible distinct/GP product types. The four exact infeasibility results therefore rule out all maximal product GP sets of sizes one through four with both factor parameters exceeding the selected size. I found no missing semantic bridge, unjustified pruning, or reliance on a supplied discovery table.

**Disconnected factors.** GP and inclusion maximality are componentwise, since a shortest path stays within one component. Thus lower GP is the sum of component lower-GP values, and product components are exactly `G_i □ H_j`. The manuscript correctly applies the connected bound and the inequality `sum_j min(t,y_j) >= min(t,sum_j y_j)` twice. Nonempty components ensure the sums are legitimate. The resulting bound is exactly the stated `min{5,gp^-(G),gp^-(H)}`.

This is self-contained as an explicitly computer-assisted argument with its executable supplement. It is not a claim that the four numerical infeasibility outcomes have been replaced by hand calculations.

## 5. Concrete counter-accounting finding, now corrected

The substantive finding during manuscript review was a reporting detail in the search-state column. In `verify_arbitrary_four.py`, the final demand-removal negative control calls `infeasible` on an otherwise complete landmark model with an empty demand list. It enters one feasible state and increments `nodes`, while its default `record=False` excludes it from the deterministic certificate digest.

Consequently the emitted state totals `2,3,15,2508` each include one negative-control state. The obstruction-search portions alone contribute `1,2,14,2507`. The final table caption now explicitly says that one additional demand-removal negative-control state is included in each run. This preserves the real output rather than relabeling it as a different computation.

The finding is resolved in the bound final TeX. It does not invalidate the nonexistence result, alter mathematical inputs, or change any of the four stream digests. I checked the source call, ROOT's explanation, the actual output counts and the final caption, rather than accepting an unchanged PASS heading.

## 6. Actual receipts and the Lean/computation boundary

The new replay receipt gives actual commands, UTC start/end times, source hashes and zero exit codes for the fixed, universal, and finite-family checks. I read the numerical outputs: universal landmark types `1,2,8,106`, outside-profile totals `1,5,87,9101`, surviving GP type pairs `1,2,14,2381`, final twenty-five rays, all 9484 patterns, and the thirty intermediate ray counts. The four stream digests agree with the appendix. The fixed output checks the actual 11-, 29-, and 319-vertex graphs and 314 outside blockers; the finite-family output covers `r=6,7,12,31` and complete factors `r=1,...,5`. The text correctly labels those family runs as regression checks supporting the written all-parameter argument.

The new Lean receipt records a successful fresh-object compilation on 12 October 2026, with Lean 4.34.1, pinned Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, exit code zero, fifteen standard-only declaration audits, and zero Lean errors or warnings. I read the fifteen audit lines and independently hashed the produced object; its actual SHA256 matches the receipt:

    a043f51762770ec515a4d0d2fd1ea15ddf4e8be2c247dc4b13a072e3884557a3.

This is evidence of ROOT's actual run, not a separate compilation by this reviewer. The text faithfully describes the audited semantic endpoints: actual finite `SimpleGraph` factors and Mathlib `boxProd`, original shortest-path GP, inclusion-maximality and genuine minimum lower GP, connectedness, both fixed factor parameters at least six, and product parameter at most five. The fixed source proves the original conjecture false. It does not establish an audited equality endpoint `gp^-(G_6)=6`, the arbitrary-`r` family, universal min-five theorem, or product equality five. The manuscript explicitly makes all of those scope distinctions.

The Lake file and resolved manifest pin the stated Mathlib revision and toolchain. The reproduction document accurately says that a new empty-cache machine was not tested and records the actual package-root flag in the fresh-object command. Historical audit records retain historical dates. Assertions are part of the Python checkers, and the reproduction instructions correctly prohibit `python -O`.

The final two Tectonic passes have zero exit codes and their receipt binds the final TeX/PDF hashes above. The successful TeX log contains no unresolved-reference or overfull-box issue identified by the structural check. Tectonic stderr nevertheless contains a nonfatal Fontconfig configuration message; this review does not describe all tool stderr as empty. The manuscript's statement of no errors or warnings applies specifically to the successful Lean run and is accurate. The built-in editor timeout is separately disclosed and is not counted as a successful compilation.

## 7. Citations, English, AI disclosure, and remaining human responsibility

The embedded bibliography and separate BibTeX contain the same four references. The original paper's authors, title, conjecture numbering, final volume/pages and DOI agree with the primary source. The five authors and published 2025 volume/pages for the foundational lower-GP paper were checked against primary institutional/version-of-record material, as well as its [arXiv record](https://arxiv.org/abs/2306.09965). The related clique-enlargement attribution was checked against [Brešar and Yero, arXiv v2, Section 2.2 and Proposition 5](https://arxiv.org/pdf/2307.02951v2). That citation supports a related factor-saturation mechanism; the manuscript does not incorrectly attribute the present Cartesian theorem to it. The [Avis exposition](https://cgm.cs.mcgill.ca/~avis/epc/epc.html) appropriately credits the standard polyhedral method; the required local completeness argument is also supplied in the manuscript.

The prose distinguishes the original conjecture, the elementary family, the computer-assisted universal theorem, the fixed Lean certificate, and finite regression checks. I found no English ambiguity that changes the mathematical meaning and no unsupported claim of a formula for every product, a smallest counterexample, or an exact second-factor parameter. The historical-priority disclaimer is necessary and present. I have not conducted a separate exhaustive originality search in this manuscript pass, and neither this review nor the manuscript's search report certifies firstness.

The AI declaration accurately describes substantial AI contributions and says that the independent reviewer did not discover the construction or write the proofs. It expressly distinguishes AI review from external human peer review, lists no AI author, and leaves human authorship and declarations pending. This is faithful to this reviewer's role.

Before any external release, a responsible human must still read and accept the mathematical and computational claims, confirm author identities/order and contribution statements, and approve funding, competing-interest and license declarations. Those are pending responsibility and publication matters, not mathematical holes filled by an AI PASS label. ROOT must finish its assigned complete PDF visual inspection and package-integrity checks; this report does not certify those unperformed-by-reviewer steps. No further theorem/proof amendment is required by the mathematical issues found in this audit.
