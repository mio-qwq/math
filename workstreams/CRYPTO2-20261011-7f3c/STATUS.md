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

## Reservation, before computation

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

