# Literature search and provenance log

Date: 2026-10-11 UTC. Reviewer: `survey_hashes`. Scope: independent novelty audit of the exact signed **linear** seven-input-bit relation specified in `../NOVELTY_REVIEW.md`; no verification implementation was written or reused.

## Search families actually executed

- Exact paper titles for Coutinho 2021, Latin Dances Reloaded 2022/2023, Okada–Nagai–Miyaji 2025, Li et al. Mixderive and New Derivation Rule 2025/2026, Mealy 2026.
- `linear sum of three modular additions cryptanalysis`, `linear approximations three inputs modular`, and combinations of `Wallén`, `SNOW 2.0`, `three-input addition`.
- `On Approximating Addition by Exclusive OR`, `Cryptographic significance of the carry`, and `Addend dependency differential linear probability addition`.
- Follow-up `Approximating Addition by XOR: how to go all the way` found the actual ePrint **2010/072**; some citing snippets incorrectly report 2011/072. Only the verified ePrint date and identifier are used.
- Exact Japanese report identifiers `ICSS2024-90`, `ICSS2025-73`, and ChaCha/Nagai/Okada follow-up searches.
- Fixed-addend/constant linear approximations, consecutive modular additions, half-quarter XDP, state functions, exact carry dependencies, and signed differential-linear approximation, including 2026 publications.
- Literal ChaCha bit-28 and correlation-size searches did not identify a confirmed matching formula. Search absence is not used to establish originality.

Routine searches used the system2 engine; representative titles/current authoritative coverage were also submitted to system1. Publisher, ePrint, IACR, IEICE, author/institutional full papers and public official code were used to evaluate claims. Generic search snippets and bibliographic aggregators were discovery aids, not sufficient evidence of mathematical content.

## Primary source locations and access result

| Source | Location | Access actually achieved |
|---|---|---|
| Okada–Nagai–Miyaji INDOCRYPT 2025 | https://link.springer.com/chapter/10.1007/978-3-032-13301-4_4 | Abstract, publication dates, references; chapter paywall |
| Its withdrawn ePrint | https://eprint.iacr.org/2025/2128 | Metadata, abstract, withdrawal history, note identifying Version of Record |
| Nagai–Miyaji March 2025 | https://ken.ieice.org/ken/paper/20250306fcJC/eng/ | English abstract, issue date, bibliography; PDF missing |
| Okada et al. November 2025 | https://ken.ieice.org/ken/paper/20251104EcoL/eng/ | Abstract and bibliography; PDF missing |
| Okada–Miyaji March 2026 | https://ken.ieice.org/ken/paper/202603176ctX/ | Japanese/English abstracts and report metadata; PDF missing |
| Author laboratory bibliography | https://bigdata.comm.eng.osaka-u.ac.jp/miyaji-lab/activity/paper.html | Follow-up title lead; not proof of final ICICS 2026 publication |
| Coutinho–Souza Neto 2021 | https://eprint.iacr.org/2021/224 | Metadata; direct PDF failed |
| Official full-paper collection | https://www.gov.br/abin/pt-br/assuntos/tecnologia/CEPESC_coletanea.pdf | Downloaded 140-page collection; printed pp. 711–740 inspected |
| Author public code | https://github.com/murcoutinho/cryptanalysisChaCha | README/repository existence inspected; no verification code copied |
| Latin Dances 2022 IACR archive | https://www.iacr.org/archive/asiacrypt2022/137910004/137910004.pdf | Search-index text; later web and direct download 403 |
| Latin Dances publication copy | https://jackgiffin.com/main/pdfs/Coutinho-Latin-Dances-Reloaded-2022.pdf | Downloaded full 31-page publisher paper; title, authors, DOI, pagination checked against primary publisher metadata |
| Latin Dances JoC 2023 | https://link.springer.com/article/10.1007/s00145-023-09455-5 | Publisher abstract, accessible appendix proofs, expansion notice; main body not accessible |
| Mixderive ePrint | https://eprint.iacr.org/2025/1670 | Metadata and abstract; PDF 403/robots |
| Mixderive proceedings | https://link.springer.com/chapter/10.1007/978-981-95-9284-5_8 | Publisher abstract, date, references |
| New Derivation Rule | https://link.springer.com/chapter/10.1007/978-981-95-8034-7_25 | Publisher abstract, date, references; no full paper |
| Mealy CRYPTO 2026 | https://eprint.iacr.org/2026/1193 | Metadata; publisher publication date separately checked |
| Mealy author full version | https://hukaisdu.github.io/files/papers/2026-1193-mealy-machines.pdf | Downloaded 53 pages; Theorem 2, constant-add section and conditional-correlation application inspected |
| Sarkar 2009 | https://eprint.iacr.org/2009/047 | Metadata, revision acknowledgment; indexed PDF text describes general finite-position computation and explicit n<=4 cases; direct download 403 |
| Alquié 2010 | https://eprint.iacr.org/2010/072 | ePrint metadata, revision/older-Holte acknowledgment; PDF indexed text through explicit finite-matrix and spectral method inspected |
| Nyberg–Wallén 2006 | https://link.springer.com/chapter/10.1007/11799313_10 | Publisher metadata and abstract |
| Nyberg–Wallén author copy | https://www.tcs.hut.fi/Publications/knyberg/snowpreproc.pdf | Download failed 502; web timed out |
| Miyano 1998 | https://globals.ieice.org/en_transactions/fundamentals/10.1587/e81-a_1_106/_p | Publisher metadata and abstract; no full paper |
| S-functions SAC 2010 | https://mouha.be/wp-content/uploads/sfunction.pdf | Full search-readable author paper; §2 and §3.6 inspected |
| Bellini et al. state functions | https://www.inderscience.com/info/inarticle.php?artid=138416 | Publisher year/pages checked |
| Bellini institutional copy | https://iris.polito.it/retrieve/handle/11583/2987931/707706 | Direct download 403 |
| Bellini author-posted publication | https://www.researchgate.net/publication/380109947_Finding_differential_trails_on_ChaCha_by_means_of_state_functions | Full author-posted text, published version dated 2024, inspected |
| Liu et al. 2026 | https://link.springer.com/article/10.1186/s42400-026-00671-7 | Full HTML, published 2026-10-09; modeling assumptions, signed cluster, future work inspected |
| Walsh DL 2026 | https://eprint.iacr.org/2026/2013 | ePrint received 2026-09-14; publication metadata |
| Walsh DL author paper | https://hukaisdu.github.io/files/papers/2026-2013-walsh-transform-differential-linear.pdf | Downloaded 65 pages; abstract/method scope inspected |

## Retrieval execution

Commands were executed from the repository root using Python's standard-library `urllib.request` and installed `pypdf`:

```
python3 workstreams/CRYPTO/projects/chacha-three-add/literature/fetch_public_sources.py
python3 workstreams/CRYPTO/projects/chacha-three-add/literature/fetch_public_sources.py latin_dances_2022_mirror sarkar_2009
python3 workstreams/CRYPTO/projects/chacha-three-add/literature/fetch_public_sources.py nyberg_wallen_2006
```

All three commands exited 0; the helper records individual HTTP failures in its JSON manifest instead of treating them as successful retrievals. The first command ran before the latter three source entries were added to the helper. No access-control bypass, authenticated session, author contact, purchase, or external publication was attempted.

`cache/` is excluded by the scoped `.gitignore`. The public mirror's hosting is not author-controlled; it is only a copy of the primary publication, not an independent authority. No claims are based on alterations unique to that mirror. PDF hashes and extracted text make the inspected copy identifiable, but this is not a publisher-provided authenticity signature.

## Scope update from discovery agent

The audit was expanded to the proposed arbitrary-output-bit rotation-elimination formula with at most `n` masked two-add terms, and the fixed-first-word special-bit sign classification. The exact three-input mask mapping, the extra intermediate-output mask when `k!=0`, and direct-corollary risk are recorded in the addendum to `../NOVELTY_REVIEW.md`. These were not promoted to confirmed original claims. The separate verifier owns implementation and mathematical validation.
