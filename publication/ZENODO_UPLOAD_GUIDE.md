# Manual Zenodo preprint upload

Prepared 15 October 2026. The two manuscripts are separate publications, not new versions of 006. Neither has a newly reserved or registered DOI yet.

## Files and creator

| Paper | Manuscript | Source | Metadata |
| --- | --- | --- | --- |
| A sharp lower general-position bound for Cartesian products | [13-page PDF](lower-gp-cartesian-v0.2/lower-gp-cartesian-v0.2.pdf) | [LaTeX ZIP](lower-gp-cartesian-v0.2/lower-gp-cartesian-v0.2-latex-source.zip) | [Title, abstract and keywords](lower-gp-cartesian-v0.2/zenodo-upload-metadata.json) |
| A structural obstruction to (1,1,3,3,4)-packing colorings | [8-page PDF](clawfree-packing-v0.2/clawfree-packing-v0.2.pdf) | [LaTeX ZIP](clawfree-packing-v0.2/clawfree-packing-v0.2-latex-source.zip) | [Title, abstract and keywords](clawfree-packing-v0.2/zenodo-upload-metadata.json) |

For each record use **River Zhang** (family name Zhang, given name River), ORCID **0009-0004-2437-8566**. Correspondence is **mioqwq@hotmail.com**. No additional author or affiliation has been assumed. Resource type: **Publication / Preprint**. Version: **0.2**. Language: **English**. Manuscript license: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

## Separate DOI workflow

1. Sign in to Zenodo and create a **new upload** for the first paper. Upload its PDF and LaTeX-source ZIP. Do not upload the outer delivery ZIP as the paper itself.
2. Copy the title, abstract and keywords from that paper's metadata JSON; fill the creator/ORCID, preprint type, version and license above. Leave an existing DOI field empty. Do not reuse the 006 DOI or choose a new version of the 006 record.
3. Use **Reserve DOI** if a number is needed before publication. A reserved DOI is not a registered, resolving DOI until the record is published. The PDFs do not require the reserved number to be printed inside them.
4. Add the GitHub reproducibility archive and its verification page as related material, then preview and check the correct PDF, creator, abstract and license. Use the actual publication date rather than an earlier preparation date.
5. Publish when the human author's final review is complete. Save the record URL and version DOI. Repeat with a **second new upload** for the other paper.

The manuscript PDF and LaTeX ZIP are both CC BY 4.0. Proof software is a separately licensed component: its original repository license and component boundaries are included in the full GitHub reproducibility ZIP. To keep the manuscript record's license unambiguous, the recommended Zenodo upload contains only the manuscript and LaTeX ZIP, with the separately licensed reproducibility archive linked as related material. Full reproducibility bundles remain downloadable from GitHub, with manifests and SHA256.

Official documentation: [reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/) and [Zenodo deposit metadata](https://developers.zenodo.org/#deposit-metadata). The official API documents DOI registration at publication and states that the selected record license applies to deposited files. This guide therefore preserves the manuscript/software license boundary explicitly.

## Original references and scope

- Lower-GP paper: Kruft Welton, Khudairi and Tuite, *Lower general position in Cartesian products*, DOI **10.22049/cco.2024.29171.1879**, published Conjecture 3, preprint Conjecture 2.10. The fixed 319-vertex counterexample has Lean; the universal bound and infinite family do not have full Lean proofs.
- Packing-coloring paper: Mortada, El Zein and Al Hajjar, arXiv **2608.02566v1**, Section 6, Problem 1. The fixed 36-vertex counterexample has Lean; the odd-parameter family is a written structural proof.

Both papers disclose substantial AI assistance. Independent AI review is not human peer review; no historical-first claim or journal acceptance is asserted. The complete originality and execution reports are inside each reproducibility bundle. No Zenodo account credential is needed to use this manual workflow, and none should be placed in this repository.
