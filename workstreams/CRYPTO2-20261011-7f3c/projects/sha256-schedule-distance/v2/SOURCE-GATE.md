# Post-discovery source gate — 2026-10-12 UTC

Outcome: **specific parameter novelty unconfirmed; no new generic technique
and no attack claimed**. The exact target remains the universally quantified
actual 64-word distance question in ../CANDIDATES.md. That target is our
explicit research question, not a purported numbered public conjecture.
The new claims are the complete relaxation equality list and two actual
universal exclusions. The underlying 32-bit sigma chain is fully stated
in PROOF.md, including signs and quantifiers.

## Primary sources inspected

1. NIST, FIPS 180-4 (August 2015), Sections 4.1.2 and 6.2.2:
   https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf .
   The frozen v1 source gate fixed this actual word recurrence; no
   XOR-linearized replacement is made in the new exclusions.

2. Pramstaller, Rechberger, Rijmen, *Preliminary Analysis of the SHA-256
   Message Expansion*, first NIST hash workshop, 2005, Sections III–V:
   https://csrc.nist.rip/groups/ST/hash/documents/Rechberger_PreliminaryAnalysisOfSHA256.pdf .
   Retrieved full author slides plus paper in this continuation. The paper
   studies low bit weights in linearized variants and cautions about
   translating them to the nonlinear expansion. This is related context,
   not a proof of or counterexample to our actual-word classification.
   A guessed modern NIST media URL was inaccessible; the mirror succeeded.

3. Jutla, Patthak, *Provably Good Codes for Hash Function Design*, SAC 2006,
   LNCS 4356, pp. 376–393 (proceedings 2007), Theorems 2, 5, 6:
   https://scispace.com/pdf/provably-good-codes-for-hash-function-design-4idf45wk3a.pdf .
   Full author-paper copy retrieved; relevant theorem statements read.
   The results concern bit distance of quasi-cyclic XOR-linear expansion
   codes, including a modified SHA-1 code and SHA-1. They demonstrate prior
   exact code-distance techniques, not this nonlinear SHA-256 word result.
   This closes access to the conference text, not to every revision of
   ePrint 2005/247 or a later journal version. Those version gaps remain.

4. Alamgir, Nejati, Bright, *SHA-256 Collision Attack with Programmatic SAT*,
   arXiv:2406.20072v1, 2024-06-28, Sections 3–5:
   https://arxiv.org/html/2406.20072v1 . The current abstract page lists
   only v1. Full text, especially inconsistency blocking and wordwise
   propagation, inspected. It explicitly builds on earlier two-bit
   conditions and detects globally incompatible local conditions. Thus
   neither detecting such contradictions nor using SAT is new here.
   It does not state our 15-support/two-exclusion classification in the
   inspected text. No inference of novelty from that absence is justified.
   Author-linked code https://github.com/nahiyan/cadical-sha256 : README
   and scope inspected; implementation not audited or copied. Its published
   collision results and IV freedoms are not results of our project.

5. Dean A. Kulik, *Aperture Threshold Geometry in the SHA-256 Message
   Schedule*, Zenodo 20423538, v1, 2026-05-28:
   https://zenodo.org/records/20423538 . The long author description contains
   the recurrence/dependency taxonomy and pseudocode. It tracks a Boolean
   OR dependency trace for a seed perturbation, not cancellation-aware
   support feasibility for arbitrary message pairs. Its Section 15.3
   leaves cryptanalytic use for future work. No same-scope classification
   was found there; this is not an endorsement of its other claims.

6. Matusiewicz, Pieprzyk, Pramstaller, Rechberger, Rijmen,
   *Analysis of simplified variants of SHA-256*, WEWoRC 2005:
   https://researchers.mq.edu.au/en/publications/analysis-of-simplified-variants-of-sha-256/ .
   University author metadata/abstract checked. CiteSeer PDF retrieval
   returned 502. Its full text was not newly read here; do not treat the
   related NIST note as a substitute for every section of this paper.

## Search boundaries and decision

Search phrases covered SHA-256 message-expansion minimum word/bit weight,
code distance, modular sigma differences, impossible differentials and
programmatic SAT. Both available engines were used; some searches returned
mostly irrelevant material. This is a bounded search, not a completeness
guarantee. The earlier gate already records 2026 collision/preimage work,
the Eichlseder thesis, and conditional-affine clauses. No later erratum or
exact matching classification surfaced, but author code and later versions
have not been comprehensively audited.

No original cryptanalytic method is asserted. At most we have a concrete,
reproducible parameter exclusion with uncertain priority and uncertain
impact. Prior-art discovery covering the same supports should downgrade
this immediately to an attributed derivation. Do not rename a standard
carry implication as a new attack mechanism. The result does not yet meet
the user's requested major-result standard.
