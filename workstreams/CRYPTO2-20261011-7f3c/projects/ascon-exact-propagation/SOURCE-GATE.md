# Source and novelty gate — 2026-10-11 UTC

Owner CRYPTO2-20261011-7f3c. This is a bounded search, not a certificate that
no earlier or equivalent result exists. Public sources were accessed without
contacting authors. No external cryptanalytic code was copied into the work.

## Original question and exact adopted scope

Kai Hu, Zhongfeng Niu, Meiqin Wang, [Round-Based Approximation of
(Higher-Order) Differential-Linear Correlation](https://eprint.iacr.org/2026/358),
EUROCRYPT 2026. Landing page: received 2026-02-22, latest of four revisions
2026-06-05. Its current note corrects typos in the PRESENT result table.
The complete tool-extracted PDF was obtained and Sections 3 and 7.4 inspected.
Section 7.4 leaves measurement of approximation error as an unnumbered
future-work direction. This is NOT a numbered universal-exactness conjecture.
Assumptions concerning columns and value masks are expressly assumptions.

Our formal subproblem fixes the actual 320-bit Ascon permutation, arbitrary
fixed constants, uniform unconstrained initial state X, and specified
differences A,B,C at the two S layers. For every such triple, compare the
joint event probability P to the product M of local DDT entries/32. The
delivered quantified results cover all A with at most three active input
columns. PROOF.md and EXTENSION.md give all quantifiers, including zero
local transitions and the distinction between a trail and an endpoint
differential. This is restricted progress on error measurement; no general
all-round error problem or reported HNW distinguisher is settled or refuted.

The object is pinned by [NIST SP 800-232 final](https://csrc.nist.gov/pubs/sp/800/232/final),
published 2025-08-13, specifically Section 3's five-word permutation,
Table 6 and rotation constants. The final standard's indexed PDF text was
read. A direct local PDF request returned HTTP 403; there is no claimed
raw-PDF byte hash. Our independently coded table/circuit agree after an
explicit five-bit convention conversion. f0/e1 are the first two p[12]
round constants, not the last-two-round p[2] constants. The theorem permits
all fixed constants and so is not restricted to that illustrative pair.

## Closest prior work and what is not claimed as new

1. Vahid Jahandideh, Bart Mennink, Lejla Batina,
   [Probing Secure Composability Without Fresh Randomness: Theory and
   Application to Ascon](https://eprint.iacr.org/2025/179), TCHES 2025,
   latest landing revision 2025-07-14. Full extracted text read at Section
   6.2 (Lemmas 5/6), Definition 8 and Theorem 1. Diffusion-induced joint
   independence and branch-number reasoning are clear prior art. Their
   composition theorem concerns masked gadgets and probing security;
   the inspected statements do not give this exact Ascon differential
   support classification. We make no claim to have invented the general
   independence mechanism or a new masking composition theorem.
2. Kai Hu, Thomas Peyrin, Quan Quan Tan, Hongyi Zhang, Chunning Zhou,
   [Finer-Grained Fixed-Key Differential Probability Distributions via
   Quasidifferential Decoupling](https://eprint.iacr.org/2026/1162),
   ToSC 2026(3), latest landing revision 2026-09-02. Obtained the full
   62-page author-hosted extraction and inspected the introduction,
   definitions and quasidifferential/constraint discussion. General exact
   probability reconstruction, character expansions and corrections for
   value dependencies are already established, including the earlier
   Beyne–Rijmen framework cited there. Its applications concern GIFT,
   SKINNY and RECTANGLE; no occurrence of Ascon was found in that extracted
   text. Our one-character formula is not a new general probability theory.
3. Christof Beierle, Patrick Felke, Gregor Leander, Patrick Neumann, Lukas
   Stennes, [On Perfect Linear Approximations and Differentials over
   Two-Round SPNs](https://eprint.iacr.org/2023/725), CRYPTO 2023, landing
   received 2023-05-19. Its abstract concerns probability-one differentials
   and perfect linear approximations for all keys. Author publication page
   also checked. Full PDF retrieval returned 403; full-scope exclusion is
   not claimed. This remains a comparison gap.
4. Meicheng Liu, Chengan Hou, Xiaojuan Lu, Shichang Wang, Dongdai Lin,
   [Differential-Linear Cryptanalysis from an Algebraic Perspective](https://doi.org/10.1007/s00145-025-09564-3),
   published 2025-11-18, JoC 39(7), 2026. The publisher abstract reports
   DATF estimates and two exact biases. Only publisher metadata/abstract
   were available behind the full-text subscription wall. A universal
   assertion that exact Ascon biases were previously unavailable would
   therefore be false. Detailed theorem comparison remains open.
5. Solane El Hirch, Silvia Mella, Alireza Mehrdad, Joan Daemen,
   [Improved Differential and Linear Trail Bounds for ASCON](https://eprint.iacr.org/2022/1377),
   landing revised 2022-10-20. Two-round trail enumeration and longer-round
   bounds are already studied. Landing and abstract read; PDF retrieval
   failed. No claim that its formal probability assumptions are incorrect.
6. Mathieu Degre, Patrick Derbez, Lucie Lahaye, Andre Schrottenloher,
   [New models for the cryptanalysis of ASCON](https://doi.org/10.1007/s10623-025-01572-5),
   published 2025-02-08. Publisher abstract concerns SAT/MILP models and
   longer-round trail bounds; full text unavailable. Also checked official
   Ascon bibliography and search results for Tezcan's 2016/490 impossible,
   truncated and improbable differential work. An impossible local trail
   here is not a new claim to impossible-differential cryptanalysis itself.

## Author pages, code and later-result checks

The [official Ascon publication list](https://ascon.isec.tugraz.at/publications.html),
[Kai Hu's homepage](https://hukaisdu.github.io/) and
[publication list](https://hukaisdu.github.io/publications/) were read.
The latter revealed 2026/1162 above and
[2026/1473](https://eprint.iacr.org/2026/1473), Chang–Hu–Peng–Wang,
*An Exact Four-Wise Framework for Boomerang Cryptanalysis* (received
2026-07-19). The latter's landing abstract covers quartet probabilities,
including impossible Ascon boomerangs; only its abstract was inspected,
not its complete proof. Two-point trails here have different quantifiers.
Separate complete publication audits for all coauthors were not performed.

HNW's linked public repository
[Round-based-approximation](https://github.com/hukaisdu/Round-based-approximation)
was cloned read-only at `783e8edc560b848d0f2ba63f11838aecd23da40f`.
README and file inventory were inspected, plus a bounded text search for
independence/error/rank terminology. This is not a full code audit and the
code was not executed or used as the discovery implementation. No explicit
same-scope theorem was located there; keyword absence proves nothing.

Searches included Ascon exact differential probability, Markov assumption,
two-round independence, three active columns, branch-number independence,
fixed-key probabilities and later HNW publications. Some search-engine
results were irrelevant; those were discarded rather than counted as
negative evidence. Primary sources and author pages supplied the usable
evidence. The retrieved latest HNW revision still leaves the broad error
question for future work, but this does not establish that every restricted
case is open as of the search date.

## Current assessment and stop condition

Mathematical claim: complete standard-width classification for at most
three active input columns, 320 exactly described three-column supports
admitting product error, and the sharp factor-two bound with explicit local
correction. This is a restricted-model theorem, not an attack and not a
counterexample to the source paper's expressly approximate method.

Possible originality lies in this concrete classification, not in Gaussian
elimination, Fourier/character correction, general dependence phenomena,
or independently rediscovering the source algorithms. No exact same-scope
statement was found in the inspected material. Historical originality and
academic importance remain unconfirmed; missing full texts above prevent
a priority claim. If any covers the same quantified Ascon result, downgrade
to an attributed derivation and close the novelty claim rather than rename it.

This work differs from existing team claims in object (standard Ascon
5x64 permutation), target (exact two-round value-conditioned trail laws),
and mechanism (free-coordinate projections and finite support classification).
It does not revisit APN/Sidon periods, graph maximality, ortho-derivatives,
ChaCha local-correlation claims, or the fixed SHA3-384 model.
