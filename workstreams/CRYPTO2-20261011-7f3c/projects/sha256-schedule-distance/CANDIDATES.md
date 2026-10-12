# SHA-256 source gate and candidate selection

Search date: 2026-10-12 UTC. Primary-source searches included later papers,
version histories, author repositories and equivalent message-expansion /
truncated differential / code-distance terminology. No search can certify
that every later result was found. Sources and remaining gaps are explicit.

## 1. Standard-IV collision beyond the currently claimed 39 steps

Original source baseline: Li, Zhang, Li, Liu, Qian, Zhu, *Pushing Collision
Attacks on SHA-2 to 39 Steps*, ePrint 2026/1120, September 9 revision,
Table 1 and the 39-step discussion. Full text inspected at
https://eprint.iacr.asia/2026/1120.pdf . The original landing page served an
older June author list; do not conflate versions. It gives SHA-256 costs
2^57, 2^79.1, 2^104.3 for 36,37,38 steps; its 39-step SHA-256 estimate
2^168 is not better than birthday search. The 39-step effective attack in
the title applies to SHA-512. The cited nldtool repository is prior tooling,
not evidence that the authors' complete latest implementation was audited.

Later claim: Omer Goldzweig, *Improved Collision Attacks on 36- to 39-Step
SHA-256*, Zenodo 23066177 v1.2, 2026-09-30:
https://zenodo.org/records/23066177 . Landing page inspected; PDF extraction
failed and the 46MB artifact has not been audited. It reports standard-IV
two-block costs 2^44.6,2^65.9,2^83.6,2^91.2, with a 17GiB table for 38/39
steps. Theoretical costs rely on stated probability assumptions; the
author declares AI-agent research and no human cryptanalyst independent
verification. This is a prior claim to account for, not a verified record
endorsed here. Do not copy this team's constructions or research sequence.

Adopted target: a randomized algorithm producing distinct equal-length,
validly padded messages colliding under standard-IV 40-step SHA-256 with
success >=1/2 and total expected cost below 2^128 compression evaluations;
include setup, data, memory, all freedoms and probability assumptions.
No source prints this exact numbered conjecture; it is our frontier target.
Direct verification: two implementations, exact bitwise compression,
padding and IV checks; validate the complete cost model separately.
First uncertainty: attainable global message-schedule conditions beyond
39 steps. Stop if the proposal only reuses existing trails, changes IV,
or shifts uncontrolled cost into an uncounted table. Not selected now.

## 2. Standard-IV 48-step preimage improvement

Guo, Li, Liu, Wang, Zhang, *Dual-Syncopation Meet-in-the-Middle Attacks:
New Results on SHA-2 and MD5*, EUROCRYPT 2026, ePrint 2026/353,
https://eprint.iacr.asia/2026/353.pdf , full text inspected. Its Table 1
gives 47-step SHA-256 preimage time 2^255.6 and memory 2^5; the lower
pseudo-preimage number must not be substituted for this hash result.
Public code README inspected: https://github.com/desert-oasis/dual-sync-MITM .
Its 44-step experiments include partial-target/pseudo-preimage checks and
are not executions of a full 47-step preimage attack. Code not audited.

Older baseline checked: Khovratovich–Rechberger–Savelieva,
*Bicliques for Preimages*, ePrint 2011/286, revision 2012-02-07,
https://eprint.iacr.asia/2011/286.pdf , Table 1 and definitions inspected.
The 52-step SHA-256 result is a **pseudo-preimage** attack, not a 52-step
standard-IV hash preimage attack. Its 45-step hash preimage cost is 2^255.5.

Adopted target: for a uniformly sampled 256-bit target, find a valid
standard-IV 48-step SHA-256 preimage with average success >=1/2 and
expected time <2^256, counting all setup, with explicit memory/data bounds.
Again no exact numbered public conjecture. Bounded searches found no
same-scope 48-step standard-IV solution; this is not an openness proof.
Verify output by FIPS equations; separately prove work and success counts.
First obstacle: extend neutral freedoms without losing independence or
paying more than their benefit. Stop if gains require a free IV, omitted
padding or fewer matching bits. Defer: no independently derived mechanism.

## 3. Actual 64-word message-expansion distance — selected

Specification: NIST FIPS 180-4 (August 2015), Sections 4.1.2 and 6.2.2,
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf .
Research source: Pramstaller–Rechberger–Rijmen, *Preliminary Analysis of
the SHA-256 Message Expansion*, NIST first hash workshop (2005), Sections
III–V, full text inspected at
https://csrc.nist.rip/groups/ST/hash/documents/Rechberger_PreliminaryAnalysisOfSHA256.pdf .
It supplies **upper** bounds on bit weight in XOR-linearized variants
(e.g. extending a 42-step weight-35 word gives 64-step weight 356), and
explicitly cautions that these need not be differences of the actual
nonlinear expansion. No numbered claim that our exact minimum is open.

Quantifiers: for all distinct M,M' in (Z/2^32)^16, lower-bound the count
of unequal words in the actual E(M),E(M') in (Z/2^32)^64; determine the
minimum if possible. A counterexample to a proposed L is one explicit
pair with fewer than L unequal words, checked from all recurrence equations.
A sharp result needs both the universal lower bound and a real pair.
Neither a support pattern nor a XOR-linearized codeword is such a pair.

Novelty risks: truncated-differential branch constraints, stopping-set
distance and finite-state trellises are established techniques. No new
method is claimed. The exact parameter result and whether it improves
existing bounds require another source gate after computation. Latest
collision trail tools already encode strong local conditions. A weak
word-support bound alone is unlikely to constitute important progress.

First falsifiable assumption: support-minimal patterns might lift to
actual 32-bit schedules. Start with exact support constraints and test
the equality case algebraically. Stop growing this direction if no new
constraint beyond the standard model is obtained. It has a direct link to
collision-path feasibility, but no implication of a practical attack or
collision-resistance theorem follows from word activity alone.

All three differ from Sora's reserved SHA3-384/APN/ChaCha objects and
mechanisms. Current coordination claims were checked before this gate.
Chosen target 3 is an exploratory bridge to the original SHA-256 question,
not a replacement of the user's major-result standard by a toy result.

## Additional avoided overlap

Feng–Gao, *Conditional-Affine Redundant Clauses for SHA-256 Differential
SAT*, ePrint 2026/1505, 2026-07-23, Sections 3–4 inspected at
https://eprint.iacr.asia/2026/1505.pdf . Its Ch/Maj cofactor characterization
and redundant clause synthesis already cover obvious conditional-affine
local clauses. It explicitly does not claim a new cryptanalytic attack.
We will not repackage those local identities as new SHA progress.
