# CRYPTO2-20261011-7f3c — independent cryptography research

- Role: independent discovery; not Sora/CRYPTO and not project coordinator.
- Baseline: `a8c3f22e26b08c2d294e2b0e6df2d9cfa430cda0` (origin/main).
- Branch: `partner/dist-CRYPTO2-20261011-7f3c`.
- Exclusive output: `workstreams/CRYPTO2-20261011-7f3c/`.
- Started: 2026-10-11 UTC. No task card for this new ID exists in the inspected coordination tree.
- Read: AGENTS.md, COORDINATION.md, coordination/RESUME.md and ROADMAP.md;
  coord/distributed BRIEF and A/B/C task cards; visible A/B/C/C-audit status and
  CRYPTO progress. Coordination snapshot: `abd8e85628b1348f250c5d5c46a5450caae2876d`.
- Existing reservations respected: graph/ARC/001–006, coordination exclusions,
  CRYPTO APN-period/Sidon/APN-neighbor and fixed SHA3-384 scopes. CRYPTO's prior
  ChaCha local-correlation work is also avoided. Remote CRYPTO remains
  `551fcd76ebabe43971123d29d11a94319a3b0096` at inspection. No recovery archive
  was read or applied, and no uncommitted CRYPTO proof was reviewed.

## Reservation, before computation (historical checkpoint)

Source: Kumar–Yadav–Samanta, *Analyzing Linear Layers in Related-Differential
Cryptanalysis*, arXiv:2605.27535v1 (26 May 2026), Theorem 5 and Section VI.
The source proves existence for circulant orders n not congruent to ±2 mod 12,
and names the remaining circulant cases as an unnumbered future problem.
It does NOT print a numbered conjecture with a complete quantified formula.

Exact target adopted here: for every finite field K of characteristic two,
every n>=3 and every invertible n-by-n circulant M over K, find distinct
nonzero u,v such that each coordinate of both (u,v) and (Mu,Mv) is either
zero in one vector or equal in the two vectors. In particular, settle the
remaining MDS orders n≡±2 (mod 12), n>2. This is a positive structural result,
not an attack or an original-conjecture counterexample.

Mechanism under investigation: repeat d-coordinate vectors when d divides n;
prove M J = J B and preservation of invertibility; use the source's odd-order
symmetry and non-MDS lemmas with explicit nontriviality checks. This acts on
linear diffusion matrices, not APN functions or the prohibited SHA3 model.

Stage: source gate and proof construction. No expensive computation performed.
Evidence so far: primary HTML/abstract, original Daemen–Rijmen PDF definitions,
2025 Hadamard paper, author research page, bounded later-result/code searches.
No same-scope resolution located; historical originality remains unconfirmed.
No independent review or Lean claimed.

Next: complete self-contained proof; directly check exact field witnesses,
the quotient intertwining identity, n=2 exclusion, and corrupted certificates.

## Completed checkpoint — 2026-10-11 UTC

The main theorem is proved in **PROOF-v2.md**: every invertible circulant
matrix of order n>=3 over every characteristic-two field has a nontrivial
related-differential pair. This completes the remaining-order direction
in the inspected source, not a verbatim numbered conjecture. The quotient
identity MJ=JB also gives beta(B)>=ceil(beta(M)/t), so MDS descends.

Evidence: complete symbolic proof; 3,710 exact checked witnesses; genuine
10-by-10 MDS circulant over GF(2^16) with all 184,755 nonempty square minors
verified by two different determinant methods; n=2 exception proved and
all 210 candidate pairs checked; damaged-certificate controls rejected.
Independent reviewer reconstructed before disclosure, then reviewed the
proof and the correction; review receipts and test scope are in review/.
The discoverer's differently implemented checker alone is not described
as independent-agent review. No Lean, actual attack or priority certification.

V1 and its first review are immutable historical records. V2 corrects an
ancillary misleading claim about possible MDS loss; the main theorem is
unchanged. The review addendum records both parties' correction explicitly.
Final-file hashes are frozen in SHA256.json. See RESULT.md, RUNS.json,
SOURCE-GATE.md and HANDOFF.md for scope and reproducibility.

Stage: completed mathematical checkpoint; content published and fetched back.
Reservation already published as b407c26994978afc7432cf505d8d78cdd9712ff9.
Native push failed for missing local credentials; the authorized GitHub
connector succeeded. Final content publication is to this same exclusive
branch with an expected-head guard, no force and no main update.

Blockers: historical originality remains uncertain; the full revised
ePrint 2025/2240, September 2026 Toeplitz paper, and Whirlwind text were
not fully retrieved. No same-scope theorem was found in the bounded search.
Next useful work: fill those precise literature gaps and check equivalent
invariant-code formulations. If already covered, downgrade to an attributed
derivation. Do not repeat sample growth as a substitute for novelty work.


## Verified publication receipt

Content commit: `3353f163b9af525a7451f7f99c8246cce61d0c8e`. The fetched remote tree
`40fc35a4d73fb3ff8c5864b0985062fc687efc82` exactly matches the locally signed
snapshot `9584bb325621e1207dbabffe0c452d7adc3751ff`. Only this workstream differs
from the baseline. PUBLICATION.json records transport and signature limits.
This receipt and the updated manifest form a follow-up metadata commit;
the proof, certificates and review files remain unchanged.

## Active phase — 2026-10-12 Singapore / 2026-10-11 UTC

User requests continued autonomous work closer to high-impact modern
cryptography. Three source-backed candidates are in CANDIDATES-20261012.md.
New exclusive claim: projects/ascon-exact-propagation/STATUS.md, exact
two-round standard-width propagation and independence-error certificates.
The prior proof/certificates/review remain frozen at remote 7b4eda2.
SHA256.json describes that historical snapshot; the next delivery will
provide a separately versioned manifest rather than alter old proof files.

## Ascon result checkpoint — 2026-10-11 UTC

The new phase now has a complete bounded result. For uniform full-width
Ascon inputs, all two-round trails with at most two active input columns
have exact local-DDT products. Among all three-column supports, exactly
320 can violate universal equality; 41344 remain universally exact.
The former are the five translated lane rotation triples. An exact local
correction formula proves a sharp 0<=P<=2M bound for every three-column
trail. This is a two-round theorem, not an attack on the standardized AEAD.

See projects/ascon-exact-propagation/RESULT.md, PROOF.md and EXTENSION.md.
The evidence includes 10085 exact rank blocks, five reproducible certificate
files, 11 negative controls and independent reconstruction/review. The
latest quasidifferential literature makes clear that the generic correction
mechanism is prior art; possible novelty is the concrete classification.
Historical originality and practical attack relevance remain unconfirmed.
The independent review receipt binds the exact files. Publication is only
to this owner's branch; old proofs remain unchanged. SHA256-v3.json is the
new content freeze; ASCON-PUBLICATION.json will record remote verification.
