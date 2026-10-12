# Verification of the written CG and theta results

Date: 2026-10-12. This receipt covers the written-result freeze. Subsequent
formalization or quantitative work has separate records.

## Objects actually reviewed

| Object | Bytes | SHA256 | Review scope |
|---|---:|---|---|
| Frozen C-audit CG candidate at commit `9ad1f91d953060d01a504481eb857daf57758ab0` | 12769 | `9544fbd1529f2815660d6f4b5ef5f52b6f114ef7682e0fa60997801c4a1255d8` | Full all-odd classification, compared after independent reconstruction |
| `cg/independent/INDEPENDENT_RECONSTRUCTION.md` | 13323 | `9d1133c9413b228b905189f0d5025d9027ed812ee34d338ce7f372ef3cf6c1e7` | Original graph, cover, intrinsic types, full group, exhaustive folds, base groups |
| `theta/PROOF.md` | 15452 | `81f7c5f4326828b16a34204e1a84b3dec136ea1d61c30cfb60b17e6395616655` | Complete geometric bound, simple-domain boundaries, bicyclic reduction and equality block data |
| `theta/MAXIMIZERS.md` | 14079 | `c0c02847ae525260d65dd5b11c1ee940b4b63aec6e2167c39fa8a9c12fc12fab` | Complete all-order unique-maximizer proof and exact maximum ratios |

The independent CG reconstruction was written before that reviewer read
the earlier candidate. The theta proofs were written by the lead
research process and reviewed by separate agents. These are AI
mathematical reviews; no independent human referee or formal publication
decision is represented.

The CG source hash discrepancy is explained in
`cg/independent/COMPARISON.md`: the actual frozen blob and its only
visible content-introduction commit have the same bytes. The inconsistent
older digest is not used to infer prior acceptance.

The theta source receipts are
`theta/independent/FINAL_SOURCE_REVIEW.json` and
`theta/maximizers_review/REVIEW_RECEIPT.json`. The former reviews the
complete global proof; the latter reviews the complete maximizer proof
and its facet-label/counting dependencies.

## Actual finite executions

| Run | Method independent of the target formula | Actual range | Main checks |
|---|---|---|---|
| CG original-definition checker | Literal source adjacency, CDC, complete individualization search | \(n=1,3,5,7\) | Entire cover group; all strong involutions and conjugacy classes; fold recovery, base groups, pairwise nonisomorphism |
| Theta graph-label checker | Integer vertex labels from spanning-tree increments, original edge and active-connectivity tests | 19 graphs at \(n\le10\) | Exact facet counts; equal normalized label sets from different spanning trees |
| Theta maximizer review checker | Fresh original-graph label enumeration, no \(T\)-count oracle | All 16 legal triples at \(4\le n\le8\) | Actual class maxima and compression/balancing boundary instances |
| Theta scalar checker | Original Proposition 22 shortest-path \(j\)-sum and separate Corollary 25 boundary clauses | All 1942 legal unordered triples at \(4\le n\le40\) | Compression, strictness, boundary identities, balancing, parity exclusion, unique maxima, four closed values and ratios |

Every run used exact integers or rational arithmetic. Each has saved
execution metadata, output and source hashes. No floating-point convex
hull calculation establishes a counterexample or a theorem here.
The bounded regressions are not substitutes for the universal proofs.

Damage controls target concrete mistakes: missing source edges or
corrupted cover coordinates, loop-producing folds, disconnected saturated
subgraphs, edge differences greater than one, duplicate length-one paths,
the missing \(xy\) multiplier, and the erroneous constant 4 in place of 5.
They were rejected in the respective run logs.

Historical executions in old branches have not been relabelled as new
runs. No old large enumeration was expanded to justify the all-parameter
group bound or theta extremum.

## Primary sources and coverage

The original CG source is Mizzi, arXiv:2603.27559v3, Definition 6.1 and
the unnumbered count question in Section 7. The known companion
constructions and classical fold correspondence are credited in the
CG package. Its dated literature report checks both available Bolzano
versions and the inspected public source tree.

For theta, the retrieved JIS PDF has SHA256
`52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a`.
The source comparison includes Braun--Bruegge arXiv v1--v4 and
Mori--Mori--Ohsugi arXiv v1--v3. The latter's inspected v3 PDF has SHA256
`698018a3ecb8ae432774a6eaad679b069e90dd15800289be5f2baf99a2cfeb6a`.
Journal metadata was checked, but that follow-up's publisher full text
was not retrieved. No complete journal-text audit is claimed.

No equivalent complete result was identified within the recorded
searches. This is a bounded evidence statement, not a certificate of
historical priority. Full third-party papers are not redistributed here.

## Formal and signing scope

The written theorem freeze does not require a completed Lean theorem.
An actual finite CG formalization, if included in a later commit, has its
own toolchain, statement list, execution log and axiom audit. It must not
be read as a formal proof of the universal group classification.

`WRITTEN_SHA256SUMS` binds the files in this written freeze. It excludes
itself and any ongoing `cg/lean/` or `c66/` work. The commit is signed
by the task's own Ed25519 key; `SIGNING_KEY.pub` supplies the public key.
Its fingerprint is
`SHA256:cq86z2y0s7GGtCbhW85swEA9ks8S5ImjqmAjTu7l1Fs`.
The signature authenticates this workstream freeze, not a human author's
identity, review endorsement, or registration of that key with GitHub.
