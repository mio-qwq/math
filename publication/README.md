# Papers and reproducibility materials

This index distinguishes published DOI records, prepared preprint files, and branch manuscripts that still need publication preparation. Mathematical correctness, Lean coverage, independent AI review and journal peer review are separate attributes.

## Manuscripts

| Paper | Mathematical contribution | Current files | Status |
| --- | --- | --- | --- |
| **A counterexample to packing-domination inheritance in strong products** | Complete counterexample to the original strong-product conjecture | [Version 1.3](006-v1.3/README.md) · [Published DOI](https://doi.org/10.5281/zenodo.23293088) | Existing published preprint by River Zhang and Yongxian Zhang; authors, DOI and old archives unchanged. |
| **A sharp lower general-position bound for Cartesian products** | Fixed counterexample, arbitrary-gap family and sharp universal corrected bound | [Version 0.3: 13-page manuscript, source and supplement](https://github.com/mio-qwq/math/tree/05f490cb168169bc9f3d1f8279a294dab1812ca7/publication/lower-gp-cartesian-v0.3) · [Version 0.2](lower-gp-cartesian-v0.2/README.md) · [Preserved version 0.1](lower-gp-cartesian-v0.1/README.md) | River Zhang; manuscript/LaTeX CC BY 4.0. Files ready for manual Zenodo upload; no new DOI yet. Fixed counterexample has Lean; universal bound and family are written/computer-assisted. |
| **A structural obstruction to (1,1,3,3,4)-packing colorings** | A 36-vertex counterexample and all-odd-parameter structural family | [Version 0.3: 8-page manuscript, source and supplement](https://github.com/mio-qwq/math/tree/05f490cb168169bc9f3d1f8279a294dab1812ca7/publication/clawfree-packing-v0.3) · [Version 0.2](clawfree-packing-v0.2/README.md) · [Preserved version 0.1](clawfree-packing-v0.1/README.md) | River Zhang; manuscript/LaTeX CC BY 4.0. Files ready for manual Zenodo upload; no new DOI yet. Lean covers the fixed instance, not the full family. |

The final version-0.3 manuscript archives are fixed at commit `05f490cb168169bc9f3d1f8279a294dab1812ca7`; the links above identify those exact directory snapshots.

The version-0.3 author is **River Zhang**, [ORCID 0009-0004-2437-8566](https://orcid.org/0009-0004-2437-8566), correspondence [mioqwq@hotmail.com](mailto:mioqwq@hotmail.com). Proof software retains its original licenses. Optional affiliation, funding and competing-interest declarations have not been invented.

Version 0.3 provides a concise AI use disclosure. All other manuscript text, except the version label, and all supplemental mathematical source bytes are unchanged from version 0.2. Current PDFs were exported twice, all 21 pages inspected, references and embedded fonts checked, and complete packages extracted and hash-verified. Earlier versions and their reports and hashes are preserved as historical evidence; they are not relabeled as new Lean runs or new independent reviews.

## Scientific review and subsequent manuscripts

The [15 October literature and originality recheck](literature-recheck-20261015/REVIEW.md) compares both frozen version-0.3 manuscripts with original statements and related primary sources. It found no verified same-scope earlier answer in the documented search; historical priority remains unconfirmed. The report includes exact file hashes and access limitations.

The [complete publication assessment and all-branch snapshot](PUBLICATION_STATUS_20261015.md) explains the decisions for the 14 remote branches.

The frozen [theta/bicyclic seven-page manuscript](https://github.com/mio-qwq/math/tree/fcd8dbf1084bcca44d67fc0e6ba6d46d301bb9e5/workstreams/STRUCT2-20261012/theta/paper) has now received a fresh independent complete mathematical/manuscript review. It is the next publication candidate, not a completed author-identified upload package in this batch. Its simple-graph domain and written proof scope remain explicit; no full Lean polytope theorem or historical-firstness certification is claimed.

Permutation-digraph counterexamples, nontrivially unstable graph enumeration and order-15 monophonic exclusion are subsequent paper candidates. Kautz-4, actual-message SHA feasibility, TF sparse/projection questions and ILP1 retain separate research and acceptance boundaries. See the [scientific catalog](../RESEARCH_RESULTS.md) for the existing formal and written results.

AI systems contributed substantially to research, proof derivation, code, Lean, literature checks, independent AI review and writing; the manuscripts disclose this and do not list AI as an author. Independent AI review is not external human peer review. No new journal submission, journal acceptance or registered DOI is asserted by this GitHub update.
