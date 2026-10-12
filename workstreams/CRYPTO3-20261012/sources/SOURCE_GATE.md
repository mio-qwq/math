# Source gate: real SHA-256 schedule word distance

Screened on 2026-10-12. This is a literature and scope audit, not a new
cryptographic theorem, proof replay, or assertion of historical originality.

## 1. Exact object and decision

Let `ME` map an arbitrary vector of sixteen 32-bit words to the sixty-four
words `W[0],...,W[63]` specified in FIPS 180-4, Sections 4.1.2 and 6.2.2.
All additions in the schedule are modulo `2^32`. The object under study is

```
D = min #{t in {0,...,63} : ME(M)[t] != ME(M')[t]} over M != M'.
```

The first sixteen words count. Neither message is fixed to zero. There
are no padding, IV, compression-output, independence, or random-message
conditions. Bit numbering in local work is least-significant-bit first;
the integer recurrence is the standard one. [S1]

**Gate decision:** no source inspected here directly determines this `D`,
attains `D=13`, or proves `D>=14`. This supports continued investigation of
the precise object, but is not evidence that its present lower bound or
future improvements are historically new. Several important methods and
nearby questions demonstrably precede this work. The access limitations
in Section 5 keep the novelty gate open.

The project's statements about a lower bound of thirteen and its candidate
supports are not independently reverified by this document.

## 2. SHA-256 sources and scope boundaries

| ID | Source and inspected version | Scope actually supported | Relation to the present question |
| --- | --- | --- | --- |
| S1 | NIST, *Secure Hash Standard*, FIPS 180-4, August 2015; original PDF | Sections 4.1.2 and 6.2.2 specify the small sigma functions, sixteen initial message words, sixty-four schedule words, and modulo-`2^32` addition. | Exact definition; no minimum-distance theorem in the cited sections. |
| S2 | Pramstaller, Rechberger, Rijmen, *Preliminary Analysis of the SHA-256 Message Expansion*, NIST First Cryptographic Hash Workshop, 2005; author paper in the archived workshop PDF | Section III studies bit Hamming weights in XOR-linearized schedules. Its original-modular-addition comparison uses a zero starting vector and single-bit changes. It explicitly says a linearized vector need not be a valid difference for the real expansion. | The reported weights, including the full-length linearized example, are not this universal nonlinear word distance. |
| S3 | Matusiewicz, Pieprzyk, Pramstaller, Rechberger, Rijmen, *Analysis of simplified variants of SHA-256*, WEWoRC 2005; author-university publication record | Abstract identifies experiments on expanded-message Hamming weights and low-weight XOR-linearized variants. | Nearby historical analysis. The publisher PDF did not load in this session, so this row relies on the primary institutional abstract only. |
| S4 | Mendel, Pramstaller, Rechberger, Rijmen, *Analysis of Step-Reduced SHA-256*, FSE 2006; full paper from the authors' institutional publication archive | Section 3.1 and Theorem 1 show restrictions on perturbation/correction vectors and invalid message expansions; the argument extends from a linearized model to unmodified SHA-256. Section 3.2 separately changes shifts to rotations in SHA-256-3R. | Precedent for genuinely invalid nonlinear expansion patterns. This is not an exhaustive classification of every size-thirteen support. |
| S5 | Jutla and Patthak, *A Simple and Provably Good Code for SHA Message Expansion*, ePrint 2005/247; related *Provably Good Codes for Hash Function Design*, SAC 2006 / later journal publication | The author's Stanford seminar abstract describes dimensional reduction for lower bounds on quasi-cyclic linear-code distance and a SHA-1-like replacement expansion. | Computer-assisted expansion-distance proofs are established methodology. The linear SHA-1-like object does not give the real SHA-256 word distance. |
| S6 | Alamgir, Nejati, Bright, *SHA-256 Collision Attack with Programmatic SAT*, arXiv:2406.20072v1, 28 June 2024; also author-hosted corrected PDF and errata | Sections 3-5 encode both real instances, derive two-bit inconsistency cycles, and propagate modular differences using carries. Their application constructs reduced-step collision characteristics, including a 38-step SFS collision. | Relevant method attribution. The paper does not claim an unrestricted full-schedule distance optimum. |
| S7 | Li, Liu, Wang, *New Records in Collision Attacks on SHA-2*, ePrint 2024/349 / EUROCRYPT 2024; extended seven-author Journal of Cryptology article, 2026 | The ePrint abstract uses SAT/SMT and controlled sparsity of signed differential characteristics. The journal abstract includes practical 31-step SHA-256 collisions and 39-step SFS collisions. | Modern sparsity-based characteristic search predates this project. Available abstracts do not state the present distance result; full latest journal text was inaccessible. |

### Version correction relevant to S6

The arXiv submission history still lists only `v1`. Curtis Bright's own
publication page links a separate errata page and corrected paper. The
erratum says Table 4 omitted a zero in the fifth chaining word. Its corrected
chaining value is:

```
afea2566 1e0a73e2 da747de7 34381a7f 06f4c0d9 8897dd98 c592ba6a d2aa5e80
```

This matters when replaying that collision example. The message-schedule
distance object itself does not depend on an IV. The public implementation
identified in S6 is `nahiyan/cadical-sha256`; it was located, not executed
or certified by this source audit.

### Latest-version correction relevant to S7

The Journal of Cryptology article was published **27 July 2026**, DOI
`10.1007/s00145-026-09582-9`, volume 39, article 27. Its seven authors are
Yingxin Li, Fukang Liu, Gaoli Wang, Haifeng Qian, Xiaoyang Dong, Siwei Sun,
and Danping Shi. The publisher records an update on **22 September 2026**
to correct the first and fourth authors' affiliations. The three-author
2024 ePrint is therefore not the latest publication version. An October
2026 issue date shown by an institutional record is not its first-online
publication date.

## 3. Limited Ascon prior-art comparison

This section compares only the existing two-round full-state theorem to
ePrint 2026/1162. It does not open a new Ascon research line or rerun the
rank enumerations.

**A1:** Kai Hu, Thomas Peyrin, Quan Quan Tan, Hongyi Zhang, Chunning Zhou,
*Finer-Grained Fixed-Key Differential Probability Distributions via
Quasidifferential Decoupling*. The ePrint metadata says received
2026-06-03 and last revised 2026-09-02; it identifies ToSC 2026-3.
Thomas Peyrin's publication list independently identifies ToSC 2026-3 /
FSE 2027.

The inspected abstract connects quasidifferentials with constraints on
intermediate bits and key parities. It explains why retaining an incomplete
threshold-selected trail set can give invalid probabilities, and uses
locally complete sets to repair the aggregation. Its listed experimental
targets are GIFT-64, GIFT-128, SKINNY-64, SKINNY-128, and RECTANGLE. [A1]

The comparison below is our scope analysis, not a claim made by A1:

| Axis | Existing repository Ascon result | A1 as established by accessible source |
| --- | --- | --- |
| Probability space | Uniform input on all `2^320` permutation states; constants fixed | Fixed-key differential probabilities and their distribution over key space |
| Exact object | Specified two-round event `(A,B,C)` and the local-DDT product `M` | Quasidifferential trail aggregation and constraint-dependent key-space partitions |
| Mechanism | Free-input projection ranks; a residual parity; exact local-fiber character averages | Nonzero masks encode constraints; decoupling restores local completeness |
| Concrete classification | At most two columns universally exact; only 320 three-column supports admit an error; all three-column paths satisfy `0<=P<=2M` | These Ascon counts and support families are not stated in the inspected abstract |
| Historical assessment | The general conditioning/character identity is already treated by the repository as elementary prior methodology | A clear additional citation for dependency-aware probability corrections; full theorem-by-theorem overlap remains unchecked |

The generic idea that dependencies invalidate a naive product, and that
parity/constraint information supplies a correction, must not be promoted
as a new cryptanalytic method. Conversely, the absence of Ascon from A1's
abstract does not prove that its general results cannot specialize to the
repository's formula. Only the concrete Ascon support classification and
its sharp bounded statement are possible candidates for a distinct result;
their historical originality remains unresolved.

The local comparison used these files at main commit
`61488e05c9fe41984f483853f99e79f5715dc893`:

| File | SHA256 |
| --- | --- |
| `workstreams/ROOT/cryptographic-structures/ascon/PROOF.md` | `b524b3592cf20a8029119cc7aa79903b166f6091a3cb45bf55668f47fc428b4a` |
| `workstreams/ROOT/cryptographic-structures/ascon/EXTENSION.md` | `192baaf0412d8e02f761503ed84653d28b93b689652fc442fe67109ad069378b` |

These files distinguish the path event from an endpoint differential,
allow arbitrary fixed constants, and identify `f0/e1` as the first two
constants of `p[12]`, not `p[2]`. This note does not independently verify
their S-box tables or the current standard-convention implementation.

## 4. Actual retrieval queries

The following are representative exact queries executed on 2026-10-12,
using both available web search systems. Multiple variants were necessary
because highly constrained queries often returned unrelated results.
Failure to locate an exact phrase is weak negative evidence.

```
SHA-256 message expansion minimum word distance nonlinear modular addition 13
SHA-256 message expansion code minimum distance Sanadhya Sarkar word
"SHA-256" "active words" "message"
"SHA-256" "word distance"
"SHA-256" "message expansion" "13" "minimum"
"SHA-256" "word weight"
"SHA-256" "active words"
"SHA-256" "word-wise" "expansion"
"SHA-256" "minimum distance" "nonlinear"
"Preliminary Analysis of the SHA-256 Message Expansion"
"SHA-256" "nonzero words"
"SHA-256" "non-zero words" "expansion"
"SHA-256" "truncated differential" "message expansion"
"SHA-256" "minimum" "word" "schedule"
"SHA-256" "lower bound" "message expansion"
"SHA-256" "minimum" "active" "message"
"SHA-256" "truncated" "MILP"
"SHA-256" "message schedule" "distance"
SHA-256 message expansion minimum weight lower bound
SHA-256 message schedule stopping sets
SHA-256 truncated message difference sparse schedule cryptanalysis
"SHA-256" "message expansion" "Hamming"
"SHA-256" "word-distance"
"SHA-256" "message expansion" "2025"
"SHA-256" "message expansion" "2026"
"SHA-256" "13" "distance" "expansion"
"New Records in Collision Attacks on SHA-2"
"A Simple and Provably Good Code for SHA Message Expansion" Jutla Patthak
"Finding SHA-2 characteristics" pdf
"Provably Good Codes for Hash Function Design"
"SHA-256" "stopping set"
"2026/1162" Ascon quasidifferential
"Finer-Grained Fixed-Key Differential Probability Distributions via Quasidifferential Decoupling"
"Finer-Grained" "Quasidifferential" "Ascon"
"Finer-Grained Fixed-Key" "tosc.iacr.org"
"Finer-Grained Fixed-Key" "pdf"
```

The 2025 and 2026 queries used recency windows of 730 and 365 days,
respectively. One lower-bound query restricted domains to `eprint.iacr.org`
and `iacr.org`. Results from blogs, search aggregators, and unrelated
implementations were not used to establish mathematical conclusions.

## 5. Access limitations and unresolved leads

- FIPS 180-4, the S2 workshop PDF, the S4 institutional paper, S6 arXiv
  HTML, its author PDF/errata, and the primary publication records were
  readable. S2 was accessed through a public archive mirror; it is the
  authors' paper, not a newly authored secondary summary.
- S3's GI Digital Library PDF and S5's original ePrint PDF did not load.
  The institutional/author abstracts establish their broad scope, not a
  line-by-line proof comparison.
- The 2024/349 PDF returned HTTP 403. The 2026 journal publisher exposed
  its abstract and update history but a subscription wall for full text.
  This is a concrete coverage gap, not permission to infer absence of an
  uninspected theorem.
- A1's PDF and version-history endpoint returned HTTP 403. Its ePrint
  abstract, metadata, and author publication list were readable; the
  public mirror and ToSC search endpoint did not yield the full text.
  Its general propositions have therefore not been compared in full.
- Search also surfaced the self-published record titled *Aperture Threshold
  Geometry in the SHA-256 Message Schedule*, Zenodo record 20423538.
  Follow-up parsing did not expose usable body text; it was not relied on,
  and its mathematical content remains unassessed.
- No exhaustive citation graph, dissertation corpus, patent corpus, or
  all versions of all implementations was inspected. Before any priority
  claim, retrieve the blocked primary texts and search again using the
  exact newly proved mechanism and statement.

## 6. Primary references and original URLs

**S1** NIST FIPS 180-4:
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>

**S2** Archived 2005 workshop paper and slides:
<https://csrc.nist.rip/groups/ST/hash/documents/Rechberger_PreliminaryAnalysisOfSHA256.pdf>

**S3** Author-university publication record:
<https://researchers.mq.edu.au/en/publications/analysis-of-simplified-variants-of-sha-256/>
; original publisher PDF endpoint:
<https://dl.gi.de/bitstreams/de5469bf-fa60-4633-807f-b35e4b92cf50/download>

**S4** Authors' institutional full paper:
<https://cosicdatabase.esat.kuleuven.be/backend/publications/files/conferencepaper/1353>
; DOI <https://doi.org/10.1007/11799313_9>
; IACR archive URL located:
<https://www.iacr.org/archive/fse2006/40470131/40470131.pdf>

**S5** Original ePrint <https://eprint.iacr.org/2005/247>
; author seminar abstract <https://crypto.stanford.edu/seclab/sem-05-06/jutla.html>
; later journal DOI <https://doi.org/10.1109/TIT.2008.2008129>.
The journal proof was not retrieved in this audit.

**S6** Original paper <https://arxiv.org/html/2406.20072v1>
; submission history <https://arxiv.org/abs/2406.20072>
; author list <https://cs.curtisbright.com/>
; corrected paper <https://cs.curtisbright.com/reports/sc2-hash.pdf>
; errata <https://cs.curtisbright.com/reports/sc2-hash-errata.html>
; public code <https://github.com/nahiyan/cadical-sha256>.

**S7** 2024 ePrint <https://eprint.iacr.org/2024/349>
; EUROCRYPT DOI <https://doi.org/10.1007/978-3-031-58716-0_6>
; 2026 journal version and change history
<https://link.springer.com/article/10.1007/s00145-026-09582-9>
; author-university record
<https://pure.ecnu.edu.cn/en/publications/new-records-in-collision-attacks-on-sha-2/>.

**A1** ePrint <https://eprint.iacr.org/2026/1162>
; author publication record <https://thomaspeyrin.github.io/web/publications/>.

Unassessed lead: <https://zenodo.org/records/20423538>.

