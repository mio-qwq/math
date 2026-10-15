# Manual Zenodo preprint upload

Prepared 15 October 2026. The two manuscripts are separate publications, not new versions of 006. Neither has a newly reserved or registered DOI yet.

## Files and creator

| Paper | Manuscript | Source | Metadata |
| --- | --- | --- | --- |
| A sharp lower general-position bound for Cartesian products | [13-page PDF](lower-gp-cartesian-v0.3/lower-gp-cartesian-v0.3.pdf) | [LaTeX ZIP](lower-gp-cartesian-v0.3/lower-gp-cartesian-v0.3-latex-source.zip) | [Title, abstract and keywords](lower-gp-cartesian-v0.3/zenodo-upload-metadata.json) |
| A structural obstruction to (1,1,3,3,4)-packing colorings | [8-page PDF](clawfree-packing-v0.3/clawfree-packing-v0.3.pdf) | [LaTeX ZIP](clawfree-packing-v0.3/clawfree-packing-v0.3-latex-source.zip) | [Title, abstract and keywords](clawfree-packing-v0.3/zenodo-upload-metadata.json) |

For each record use **River Zhang** (family name Zhang, given name River), ORCID **0009-0004-2437-8566**. Correspondence is **mioqwq@hotmail.com**. No additional author or affiliation has been assumed. Resource type: **Publication / Preprint**. Version: **0.3**. Language: **English**. Manuscript license: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

## Separate DOI workflow

1. Sign in to Zenodo and create a **new upload** for the first paper. Upload its PDF and LaTeX-source ZIP. Do not upload the outer delivery ZIP as the paper itself.
2. Copy the title, abstract and keywords from that paper's metadata JSON; fill the creator/ORCID, preprint type, version and license above. Leave an existing DOI field empty. Do not reuse the 006 DOI or choose a new version of the 006 record.
3. Use **Reserve DOI** if a number is needed before publication. A reserved DOI is not a registered, resolving DOI until the record is published. The PDFs do not require the reserved number to be printed inside them.
4. Add the GitHub reproducibility archive and its verification page as related material, then preview and check the correct PDF, creator, abstract and license. Use the actual first-public-release date of the deposited manuscript version; the linked version-0.3 files were publicly released on 15 October 2026.
5. Publish when the human author's final review is complete. Save the record URL and version DOI. Repeat with a **second new upload** for the other paper.

The manuscript PDF and LaTeX ZIP are both CC BY 4.0. Proof software is a separately licensed component: its original repository license and component boundaries are included in the full GitHub reproducibility ZIP. To keep the manuscript record's license unambiguous, the recommended Zenodo upload contains only the manuscript and LaTeX ZIP, with the separately licensed reproducibility archive linked as related material. Full reproducibility bundles remain downloadable from GitHub, with manifests and SHA256.

Official documentation: [reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/) and [Zenodo deposit metadata](https://developers.zenodo.org/#deposit-metadata). The official API documents DOI registration at publication and states that the selected record license applies to deposited files. This guide therefore preserves the manuscript/software license boundary explicitly.

## Original references and scope

- Lower-GP paper: Kruft Welton, Khudairi and Tuite, *Lower general position in Cartesian products*, DOI **10.22049/cco.2024.29171.1879**, published Conjecture 3, preprint Conjecture 2.10. The fixed 319-vertex counterexample has Lean; the universal bound and infinite family do not have full Lean proofs.
- Packing-coloring paper: Mortada, El Zein and Al Hajjar, arXiv **2608.02566v1**, Section 6, Problem 1. The fixed 36-vertex counterexample has Lean; the odd-parameter family is a written structural proof.

Both papers disclose substantial AI assistance. Independent AI review is not human peer review; no historical-first claim or journal acceptance is asserted. The complete originality and execution reports are inside each reproducibility bundle. No Zenodo account credential is needed to use this manual workflow, and none should be placed in this repository.

## Copy-ready metadata for the two manuscript records

Create one record per paper. The values below match the existing version-0.3 metadata files; the manuscripts and their archives have not been regenerated for this guide.

| Field | Value for both records |
| --- | --- |
| Creator type | Person |
| Family name | Zhang |
| Given name | River |
| ORCID | 0009-0004-2437-8566 |
| Contact email, where applicable | mioqwq@hotmail.com |
| Resource type | Publication / Preprint |
| Version | 0.3 |
| Language | English |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| File visibility | Public |
| Existing DOI for either new manuscript | None supplied; select No unless a DOI has subsequently been assigned to that same manuscript |
| First public release of these version-0.3 files | 2026-10-15 |

Include an affiliation, funding or competing-interest declaration only when accurate and applicable. The two new manuscript records do not inherit the authors or DOI of paper 006. The JSON files are metadata references for manual entry, not files that must be uploaded with the paper. Their optional API reservation fields do not mean that a DOI has been reserved.

### Paper 1: A sharp lower general-position bound for Cartesian products

**Title**

A sharp lower general-position bound for Cartesian products

**Description / Abstract**

The lower general-position number of a finite graph is the smallest cardinality of an inclusion-maximal vertex set containing no three vertices on a geodesic. We refute the conjecture that the lower general-position number of a Cartesian product is at least the smaller of the two factor parameters. For every integer r ≥ 6, we construct connected diameter-two factors of orders 2r-1 and 4r+5 whose smaller factor parameter is r, while their product has lower general-position number exactly five. Thus the conjectured bound can fail by an arbitrarily large additive amount and an arbitrarily small ratio. We prove the sharp replacement gp⁻(G □ H) ≥ min{5,gp⁻(G),gp⁻(H)} for all nonempty finite simple graphs. The lower bound has a computer-assisted proof reducing arbitrary distances to equality patterns in the five-point pseudometric cone, followed by an exact finite obstruction check. The construction and unbounded-gap argument are elementary. An accompanying Lean proof verifies the fixed 11-by-29 counterexample at the level of actual shortest paths; it does not formalize the universal bound.

**Keywords**

lower general position; Cartesian product; graph distance; counterexample; metric cone; computer-assisted proof; Lean formalization.

**Optional MSC 2020 subjects**

05C12, 05C69, 05C76.

**Upload files**

- [Manuscript PDF](lower-gp-cartesian-v0.3/lower-gp-cartesian-v0.3.pdf)
- [LaTeX-source ZIP](lower-gp-cartesian-v0.3/lower-gp-cartesian-v0.3-latex-source.zip)

**Related reproducibility material**

Link the [separately licensed reproducibility archive](https://github.com/mio-qwq/math/blob/35dacdc7cdc767c0591c60b79c5bae51e8b42b01/publication/lower-gp-cartesian-v0.3/lower-gp-cartesian-v0.3-reproducibility.zip) and [verification and checksums](lower-gp-cartesian-v0.3/README.md). The manuscript record contains only the PDF and LaTeX ZIP under CC BY 4.0; the complete proof/software package remains available through that related link.

**Original problem reference:** Kruft Welton, Khudairi and Tuite, *Lower general position in Cartesian products*, DOI 10.22049/cco.2024.29171.1879; published Conjecture 3, preprint Conjecture 2.10. This is a cited source, not the DOI of the new manuscript.

### Paper 2: A structural obstruction to (1,1,3,3,4)-packing colorings

**Title**

A structural obstruction to (1,1,3,3,4)-packing colorings

**Description / Abstract**

Mortada, El Zein and Al Hajjar asked whether every connected claw-free subcubic graph, apart from their specified exception, admits a (1,1,3,3,4)-packing coloring. We give a negative answer. For every odd integer k >= 3, the triangle expansion of a ring of k diamonds is a connected cubic graph on 12k vertices that admits no such coloring. The proof selects an arbitrary existing high-colored vertex in each triangle. The selected labels give a proper three-coloring of the core, and the radius-four class forces an external private neighbor at each of its core vertices. This requirement excludes that class from every diamond tip, leaving an impossible two-coloring of an odd cycle. The proof is structural and requires no exhaustive search. A 36-vertex member is also certified in Lean using actual graph distances; that formalization does not cover the entire infinite family.

**Keywords**

packing coloring; claw-free graph; cubic graph; triangle expansion; counterexample; formal verification.

**Optional MSC 2020 subjects**

05C15, 05C12.

**Upload files**

- [Manuscript PDF](clawfree-packing-v0.3/clawfree-packing-v0.3.pdf)
- [LaTeX-source ZIP](clawfree-packing-v0.3/clawfree-packing-v0.3-latex-source.zip)

**Related reproducibility material**

Link the [separately licensed reproducibility archive](https://github.com/mio-qwq/math/blob/35dacdc7cdc767c0591c60b79c5bae51e8b42b01/publication/clawfree-packing-v0.3/clawfree-packing-v0.3-reproducibility.zip) and [verification and checksums](clawfree-packing-v0.3/README.md). The manuscript record contains only the PDF and LaTeX ZIP under CC BY 4.0; the complete proof/software package remains available through that related link.

**Original problem reference:** Mortada, El Zein and Al Hajjar, *On (1,1,2,3)- and (1,1,3,3,3)-Packing Colorings of Claw-Free Subcubic Graphs*, arXiv:2608.02566v1, Section 6, Problem 1. This is a cited source, not the identifier of the new manuscript.

The [public literature recheck](literature-recheck-20261015/REVIEW.md) records the latest bounded comparison. It is supporting documentation available on GitHub; it is not an additional file required for either manuscript upload.
