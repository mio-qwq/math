# Literature and originality gate

Search date: 2026-10-11 UTC. **Mathematical result independently reviewed;
historical originality and publication significance NOT certified.**

## Exact original task

Kumar–Yadav–Samanta (KYS), arXiv:2605.27535v1, 26 May 2026, Theorem 5
and Section VI. The source leaves circulant orders congruent to ±2 modulo
12 outside its general result. Its last paragraph presents these as a future
problem. There is no numbered conjecture with full quantifiers. Our precise
statement and the n=2 exception are in PROOF-v2.md; neither is silently
attributed as a verbatim conjecture of KYS.

Primary source HTML, formula text, and the current arXiv version-history page
were read. The history displayed only v1. The full downloaded HTML is pinned
in SOURCE-HASHES.json. Relatedness is checked against both KYS Definitions
1–2/Section V and Daemen–Rijmen (2009) Sections 7–8: zero and identical
differentials do not count.

## Antecedents and coverage

| Source | Inspected scope | Relationship to result |
|---|---|---|
| Daemen–Rijmen, *New criteria for linear maps in AES-like ciphers*, Cryptogr. Commun. 1 (2009), 47–69, DOI 10.1007/s12095-008-0003-x | Original author-hosted PDF, definitions, rank algorithms, Section 9.1 | Definitions, general search methods and 4-by-4 circulant obstruction are prior work. |
| *Whirlwind: a new cryptographic hash function*, DCC 56 (2010), 141–162 | Primary institutional PDF search excerpt identifies the 4q-by-4q circulant claim; direct download returned 403 | Multiple-of-four attribution is not novel here. Full PDF inspection remains incomplete; our proof also gives this argument explicitly and KYS Lemma 1 states it. |
| Jha–Li–Gligoroski, *Construction of Hadamard-based MixColumns Matrices Resistant to Related-Differential Cryptanalysis*, IACR CiC 2(1) (2025), DOI 10.62056/a6ksdk5vt | Publisher PDF through search service: definitions, Theorem 3, 4/8-dimensional scope and code footnote | 28 tests for 4-by-4 Hadamard subclass. Does not establish an all-order circulant theorem in the inspected portions. |
| Otal–Sülçe–Yayla, ePrint 2025/2240, revised **2026-06-11** | Current landing page, abstract and initial PDF pages obtained through search service | Explicitly studies 2/3-dimensional matrices; latest introduction cites KYS. Abstract still limits circulant result to 3-by-3. Full PDF download and later reopening returned 403; no complete post-revision coverage audit claimed. |
| KYS, arXiv:2605.27535v1 | Full HTML | Non-MDS, odd symmetric/circulant, 4-divisible cases are attributed bases. Proposed delta: period restriction/lifting completes omitted orders. |
| Lin–Xu–Li–Wang–Sun, *On the Construction of Toeplitz MDS Matrices without Related Differentials*, DOI 10.1007/s11704-026-61301-6, online **2026-09-16** | Publisher abstract and version dates | Reported scope is Toeplitz matrices of orders 3/4 and XOR-cost constructions. Complete text not obtained (page presents sign-in form; exposed PDF icon led only to an image). This is an explicit remaining full-text gap, not certified nonoverlap of every theorem. |

## Author pages and public code

- `https://ssamanta.org/` and `/research` were read. Homepage says last
  updated April 2026; no matching related-differential entry was found in
  research page. This stale author page cannot establish current openness.
- Direct author/source URLs for Daemen–Rijmen and their paper list were
  found; the original paper was read locally.
- Public code linked by Jha et al. was cloned read-only:
  `https://github.com/sjsonucool/hadamard-matrices-resistant-to-related-differentials-cryptanalysis`,
  commit `abdc445c55baba482e3b9d0927e81983a1853adc`.
  README and file inventory establish 4-by-4 Hadamard construction/XOR-cost
  scope; text search of repository for circulant/periodic/quotient/conjecture
  found the README's 4-by-4 conversion mention, not an all-order lifting
  theorem. This is a scope inspection, not a full correctness audit or a run
  of that code. None of its code was copied into our implementation.
- Exact KYS title/arXiv-ID searches with GitHub qualifier did not locate a
  corresponding proof/code repository. This does not show none exists.
- No reliable distinct public homepages for both other KYS coauthors were
  established; no author-contact or private inquiry was attempted.

## Repeated search rounds

Before reservation: circulant MDS/open-problem search; exact KYS title;
`related differentials circulant conjecture`; author publications; Tu–Deng
recent results. The Tu–Deng old conjecture was closed at the candidate gate
because current papers claim complete solutions, without auditing them.

Before and after the proof: combinations of `related differentials` with
`circulant`, `quotient`, `periodic`, `lifting`, `every`, `all orders`;
`MDS circulant quotient matrix`; exact KYS ID with `github`; exact Otal
title; current 2026 related-differential papers with derivative aggregation
sites excluded. Both available search engines were used; several queries
returned irrelevant results, so their apparent emptiness has low evidential
weight. Only original paper/publisher/author/code sources support coverage
judgments. Search summaries that strip dimensions or invert a congruence
were rejected in favor of the source.

## Novelty assessment and stopping rule

No same-scope all-order theorem or published period-lifting application was
located in this bounded search. This is **not** a priority certificate.
The new-to-this-work argument is short and follows from an elementary
invariant subspace plus known bases, so it may be folklore, a direct
corollary elsewhere, or already covered in a source not retrieved here.
The MDS-descent bound is also elementary and is not advertised as a new
general coding-theoretic method.

The mathematically justified deliverable is a full written extension of the
circulant result in the inspected KYS version, with independent review and
exact witnesses. Its likely scale is a focused structural note, not a
major break of a standardized cipher. Before any paper/priority claim,
read the outstanding revised/full texts and check equivalent invariant-code
or quotient formulations. If an equivalent theorem is found, downgrade to
an attributed derivation and close the novelty route. Do not accumulate
more random matrices as a substitute for this check.

## URLs

- https://arxiv.org/abs/2605.27535
- https://arxiv.org/html/2605.27535v1
- https://cs.ru.nl/~joan/papers/JDA_VRI_LinearMaps_2007.pdf
- https://research.utwente.nl/files/6728185/whirlwind_final_DCC.pdf
- https://cic.iacr.org/p/2/1/37/pdf
- https://eprint.iacr.org/2025/2240
- https://eprint.iacr.org/2025/2240.pdf
- https://journal.hep.com.cn/fcs/EN/10.1007/s11704-026-61301-6
