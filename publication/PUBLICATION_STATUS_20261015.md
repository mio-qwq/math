# Scientific results and publication readiness

Snapshot: 15 October 2026. All 14 remote branches were inventoried. A branch inventory is not a complete mathematical acceptance of every file on those branches. Prior public versions and frozen evidence are retained.

## Publication decisions

| Result | Current evidence | Publication assessment |
| --- | --- | --- |
| Strong-product packing-domination counterexample, 006 | Published version 1.3, complete counterexample and reproducibility package; [DOI](https://doi.org/10.5281/zenodo.23293088) | Already published. Both original authors, DOI and archives are preserved. |
| Lower general position in Cartesian products | Fixed 319-vertex counterexample, arbitrary-gap family and sharp universal replacement; [author-identified version 0.3](lower-gp-cartesian-v0.3/README.md) | Ready for a manuscript preprint. Fixed counterexample has Lean; universal bound and infinite family are written/computer-assisted mathematics. |
| Claw-free subcubic packing coloring | Fixed 36-vertex counterexample and all odd 12k-vertex family; [author-identified version 0.3](clawfree-packing-v0.3/README.md) | Ready for a manuscript preprint. The family proof is structural; Lean covers the fixed instance. |
| Theta and bicyclic facet maxima | Frozen [seven-page draft](https://github.com/mio-qwq/math/tree/fcd8dbf1084bcca44d67fc0e6ba6d46d301bb9e5/workstreams/STRUCT2-20261012/theta/paper); a [fresh independent complete review](theta-bicyclic-review-20261015/REVIEW.md) found no mathematical blocker | Next manuscript candidate. Conjectures 13/32 use the natural simple-graph domain n>=5 with n=4 handled separately; Conjecture 33 is proved on its stated range and extended to n>=4. This is written mathematics, not a universal Lean polytope theorem or a final authored publication package. |
| Permutation-digraph general position | [Fixed formalized counterexample and all-original-parameter construction](../workstreams/ROOT/permutation-gp-counterexample/THEOREM.md) | Suitable self-contained short paper. The construction size is not an exact GP optimum. |
| Nontrivially unstable graph enumeration | [Accepted asymptotic equivalents and typical cover group](../workstreams/ROOT/distributed-written-proofs/C/tf-count/README.md) | Strong candidate for a separate theory paper after manuscript-specific review of overlap, large-support and unlabelled-count arguments. |
| Order-15 circulant monophonic exclusion | [All-connection-set exclusion and induced-path Lean](../workstreams/ROOT/monophonic-circulant15-counterexample/README.md) | Suitable short note; no need to claim a smallest counterexample or classification of every order. |
| Finite-tree orientation spectra | [All-tree interval theorem](../workstreams/ROOT/gp-tree-spectrum/README.md) | Suitable special-case paper, lower priority. It does not solve the arbitrary-graph interval conjecture. |
| Kautz word length four | New branch has uniform bounds, endpoint loss and an injective-sampling transfer; exact values and exact limiting density remain undetermined | Continue the structural research. Fixed-label bounds are not uniform bounds; the proposed six-index certificate has not been obtained. |
| Actual SHA-256 schedule distance | Branch-reported independent review of the inherited lower bound and an exact message-equivalent normal form | Continue actual-message feasibility. The bound remains 13; no distance-13 input pair or lower bound 14 is provided. No complete cipher attack or full-algorithm Lean proof is claimed. |
| TF sparse expectation and odd-CG classification | New STRUCT2 notes report a matched sparse window and further formal classification bridges | Candidate proofs need their own independent semantic acceptance. Fixed-probability C66 overlaps a public proof claim. These new results are not automatically accepted by the theta review. |
| Finite-window instruction scheduling, ILP1 | A 17-page branch draft, formal semantics and algorithmic/online claims; latest formal scope differs from the older PDF | Potential algorithmic paper, not ready for this batch. Reconcile the manuscript with current theorems and audit overlap with classical scheduling/event-DAG theory. The idealized model is not a complete processor. |
| Circulant RD, Ascon, RSA and other legacy material | Precisely qualified evidence in the [scientific catalog](../RESEARCH_RESULTS.md) | Originality and actual cryptanalytic relevance remain separate gates. Do not present classical RSA recovery, fixed-path probabilities or limited formal lemmas as new complete attacks. |

The two new version-0.3 manuscripts name River Zhang, ORCID 0009-0004-2437-8566, correspondence mioqwq@hotmail.com. Manuscript PDF and LaTeX are CC BY 4.0; proof software retains original licenses. Their preprint files have been prepared, but neither has a new registered DOI or journal submission.

## Complete remote-branch snapshot

| Branch | Frozen commit | Evidence boundary |
| --- | --- | --- |
| main | bf732c32f1b8 | Integrated scientific baseline before this publication update. |
| coord/distributed | abd8e85628b1 | Historical coordination index; no separate mathematical contribution counted. |
| integration/dist-b-permutation | 7def63b75387 | Older permutation integration; main has the accepted endpoint. |
| integration/dist-c-q58 | ec55b0ef93f3 | Older CDC integration; original Theorem 3.3 already implies the answer. |
| partner/dist-A | 64bd9d130c21 | Frozen original structural/extremal packet; accepted portions are separately indexed on main. |
| partner/dist-B | 802e030aa8ac | Frozen original GP/packing packet; mathematical portions and scope are separately indexed. |
| partner/dist-C | 979598c30058 | Original TF packet and odd-CG candidate; no blanket acceptance inferred. |
| partner/dist-C-audit-1010 | 9ad1f91d9530 | Written TF audits and counting packet; C66 and later extensions have distinct gates. |
| partner/dist-CRYPTO2-20261011-7f3c | 80b71cb3b6a6 | SHA v2 finite certificate and support exclusions, with bounded scope. |
| partner/dist-CRYPTO3-20261012 | 05295737e7d0 | Actual-message/support normal-form continuation; global equality question remains unresolved. |
| partner/dist-GP2-20261012 | 5e436926da8c | Kautz-4 endpoint loss and finite sampling transfer; no exact limit. |
| partner/dist-STRUCT2-20261012 | fcd8dbf1084b | Theta draft, odd-CG formal chain and TF sparse window; each requires separate acceptance. |
| partner/dist-ILP1-20261014 | bff3f2c1fcea | Idealized instruction-scheduling model, algorithms and online results; literature gaps remain. |
| partner/dist-crypto | 551fcd76ebab | Known-method baseline and narrow cryptographic investigations; unavailable recovery-only objects are not assessed as if present. |

## Verification and academic boundaries

The version-0.3 editorial revisions shorten the AI use disclosure. All other manuscript text, except its version label, and all supplemental mathematical sources remain identical to version 0.2. Each final PDF was exported twice with Tectonic, all 21 current pages were visually inspected, and all fonts are embedded. Current ZIPs were extracted, all manifest hashes checked, and changed-source controls rejected. The native-editor timeout is retained separately; it is not counted as a successful compilation. No unchanged Lean source or frozen large enumeration was rerun in this publication pass.

Independent AI review is not external human peer review. Historical firstness is not certified. The additional theta review used original definitions and new bounded checks, not merely earlier PASS records. Optional affiliation, funding and competing-interest declarations have not been invented. Materials must still receive the human author's final reading before journal submission.
