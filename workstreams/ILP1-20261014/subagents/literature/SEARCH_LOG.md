# Literature search and access log

Date: 2026-10-13 UTC; research ID date 2026-10-14. Last shell clock check during
source inspection: `2026-10-13T18:22:20Z`. This file records a reproducible subset
of the actual queries, direct source inspections, and retrieval limits. It is
not an assertion that a complete database search or citation-network closure
was performed.

## Exact recorded queries

The following queries were actually issued after the main source-identification
pass. Engine names describe the available search service's two systems.

| Engine | Query | Purpose/outcome |
|---|---|---|
| system1, recency 3650 days | `bounded lookahead online precedence scheduling instruction reorder buffer window optimal policy` | No usable direct R1 theorem; returned substantial irrelevant material |
| system1 | `"Note on on-line scheduling" Epstein pdf precedence` | Publisher PDF lead, later retrieval failed |
| system1 | `"reorder buffer" "online" "optimal" scheduling window theory` | Hardware/other buffer terminology; no verified exact theorem |
| system2 | `bounded window instruction scheduling reorder buffer precedence constraints optimal scheduling` | Follow-up for ROB equivalence; no exact new source established |
| system2 | `precedence constrained scheduling interval orders Coffman Graham 1972 two processors` | L05, L08 and related-class references |
| system2 | `online precedence constraints finite lookahead unit time jobs hidden successors` | L13, L15 and lookahead models with different semantics |
| system2 | `Lean Coq Rocq formal proof optimal scheduling EDF Prosa` | L18 and current formal scheduling leads |
| system2 | `online precedence constrained scheduling advice complexity hidden successors lookahead` | L15/L16 and known hidden-graph/advice work |
| system2 | `instruction scheduling reorder buffer advice competitive ratio` | Reordering-buffer papers whose slots release on service, not retirement |
| system2 | `online scheduling precedence constraints advice bits optimal algorithm` | L16 and general scheduling advice complexity |

Earlier exploration also covered Wall's ILP limits, the notation
`P|prec,p_j=1|C_max`, bounded-window/critical-path scheduling, exact scheduling,
parameterized complexity, interval/semiorders, and the current three-machine
claim. Exact earlier query strings were not all retained in this file; no
reconstructed string is labeled as a verbatim query. The source catalogue
records what was actually read.

## Direct primary inspection inventory

| Source key | Inspection performed | Restriction |
|---|---|---|
| L01 | Author publication page; original/expanded PDFs; window/latency sections and appendix | No independent reproduction of trace measurements |
| L02 | IBM abstract and metadata | Full proof text not read |
| L03 | Author project/publication pages; two-page author retrospective | Original ISCA full PDF failed retrieval |
| L04 | Primary full PDF, Table 2, §§5.1–5.2 | Particular execution graph, not optimized R1 theorem |
| L05 | Primary scan retrieved; author bibliography; L06 cross-check | Scan parser returned zero text lines; original theorem number unverified |
| L06 | arXiv v1 HTML; Theorems 1.1–1.2; publisher metadata | Later publisher full text was not successfully retrieved |
| L07 | Manuscript TeX, challenge definition, comparator JSON, actual Main.lean, release README | No full dependency build, comparator execution or axiom audit |
| L08 | Publisher abstract | Exact class definition/theorem not read |
| L09 | Primary arXiv PDF introduction and stated algorithm/hardness scope | Full reductions not independently checked |
| L10 | Dagstuhl full text §§1–3, Lemma 1, Theorem 2 | Later reductions not independently checked |
| L11 | Publisher primary records; subsequent primary descriptions | Original theorem numbering not inspected |
| L12 | Institution/author metadata and abstract | Full publisher/author paper retrieval failed |
| L13 | Primary institutional and publisher abstracts | Full theorem assumptions unavailable |
| L14 | Author PDF, online model and §3 Theorem 1 proof | Heterogeneous model, not R1 |
| L15 | PMLR full text §§1–1.3 | Weighted completion/nonclairvoyant scope |
| L16 | Renault et al. arXiv abstract; Adamaszek et al. primary PDF §§1–2 | Different advice and buffer models |
| L17 | arXiv abstract/PDF, model and main theorem statements | General resource requirements/processing lengths |
| L18 | Official proof-displaying HTML declarations and assumptions | No local Rocq build |

## Failed retrievals and misleading matches

* Original Fields et al. links at `www.cs.wisc.edu/~bodik/research/isca01a.pdf`
  and redirected `pages.cs.wisc.edu`, plus a Berkeley teaching copy, failed.
  A CiteSeer copy was also inaccessible. The later author retrospective was
  successfully retrieved. The primary 2010 paper provides the exact inspected
  resource edge instead.
* Coffman–Graham author-hosted scans were returned as PDFs, but extracted text
  had zero lines; do not report having inspected a specific numbered theorem.
* Epstein's publisher PDF and author-paper link returned internal retrieval
  errors. The institutional abstract remains the verified source for its stated
  bounds and reveal-on-completion model.
* Some searches with several broad or separately quoted words yielded dictionary
  entries and unrelated allocation/buffer pages. Those are not scientific
  evidence and weaken any inference from failure to find a match.
* “Time window” often meant release/deadline feasibility; “reordering buffer”
  often meant removing any selected item immediately. Neither is automatically
  R1's completed-but-unretired occupancy model.
* Search-index upload/crawl dates were not used as publication dates. In
  particular L04 remains PACT 2010 despite its 2025-hosted PDF path.

## Pinned current-claim artifacts

Actual command: `git ls-remote https://github.com/openai/math.git refs/heads/main`.
Observed commit: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`.
Key files were fetched again using that exact ref, and returned blob SHAs are
recorded in `NOVELTY_REVIEW.md`. The inspection used the actual solution endpoint
as well as the separate comparator challenge, avoiding the false inference that
a challenge placeholder is the submitted proof.

## Remaining novelty-search gaps

No complete search of paywalled proceedings, theses, patents, architecture
simulator implementations or equivalent queueing/event-graph formulations was
performed. Non-English literature and citation chains remain incomplete.
The exact R1 universal-online-optimality classification was not found, but this
negative search observation does not prove originality. Proposed publication
claims should remain `NOVELTY_UNCONFIRMED` until stronger comparison and external
review occur.
