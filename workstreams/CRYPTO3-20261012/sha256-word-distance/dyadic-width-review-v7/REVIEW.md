# Exact-version independent review of the uniform dyadic width lemma

**Decision: accepted, with no required mathematical revision.** The
author's `../dyadic-width-v7/PROOF.md` is accepted at SHA256
`574b5a39fb4ee0f9768401544027448f6593928f44e615b5cb5c0b49c93fa9fe`.
The five author artifacts are pinned by manifest SHA256
`a6eebd06e58db8b6ec1c98b4fa20e4c6cffdbd56e97cd36b14b8a6851dd27d35`.

The reviewer first reconstructed the bit rows, common term, sharp joint
integer bound, full residue lifting and reversal independently from the
proposed statement and FIPS function definition. That proof, checker and
successful run were frozen in `PRE-AUTHOR-CHECKPOINT.json` before any
author file was inspected. The author's source was then read and compared
with this frozen reconstruction. This is independent AI-assisted review;
it is not external human review, Lean verification or a novelty finding.

The accepted quantified statement is: three actual pairs with nonzero
input differences D,D,-D and sigma1 gaps GY-GX=2D and GY-GR=D must,
for exact k=v2(D) in 10,...,18, have

```
D = +/-q*2^k+h*2^(k+14) modulo2^32,
q odd, 1 <= q <= 2^(22-k)-1,
0 <= h < 2^(18-k).
```

The usual equality of their sigma0 derivatives may be imposed by the
larger necessary core, but is not needed for this width theorem.

The exact FIPS g row j>=22 is {j-15,j-13}. Modulo M=2^(k+14), the
rows 22,...,k+12 are fixed within a pair, and row k+13={k-2,k} flips
because D/2^k is odd. The negative input difference has the same parity.
Each modular derivative is therefore the common term M/2 plus an
ordinary low22-bit difference q_i. This common term cancels in both
required gaps, including every sign and wrap case.

The decisive joint argument is

```
A=qY-qR, B=qY-qX,
B-2A=2qR-qY-qX,
|B-2A| <= 4*(2^22-1) < 2^(k+14).
```

This is valid already at k=10. It forces the multiple of M to be zero;
B=2A then bounds |A| by 2^22-1. Exact valuation, complete lifting and
nonzero D give precisely the stated odd q and h ranges. The independent
proof uses L=2^22 and strict inequalities; the author's L=2^22-1 and
weak integer inequalities express the same bounds.

Every negative representative reduces by global pair reversal to positive
q with the lift permuted to (-h) modulo 2^(18-k). Keeping h unchanged
would omit or misidentify cases; the author's formula correctly retains
this permutation. The signed intervals are disjoint and all N/M lift
classes are present, so no high-word residue or modular wrap is dropped.

The k=9 boundary is correctly limited. Common-half decomposition still
holds, but the modulus is 2^23 and the joint norm can reach a nonzero
multiple. The author and reviewer give different valid free-integer
examples of B-2A=M. Neither example is claimed to be actual word pairs.
The author's example only refutes B=2A; the reviewer's example also shows
that the unreduced A can lie outside the proposed ordinary width. The
final signed-domain formula at k=9 nevertheless covers its entire exact
valuation stratum, so it is vacuous rather than false. At k=8 the top
row21 also contains input31, invalidating the common-parity mechanism.

The independent finite run checks all 32 rows, all nine nontrivial
valuation-layer budgets, integer norm constants and reversal lifts. It
also checks k=9's distinct boundary, 162 lift fixtures and 486 actual
pair fixtures, each with its reverse orientation. Four malformed
controls are rejected, including the insufficient 3*2^23 bound at k=10.
The fixtures exercise implementations, not full-core feasibility.

After disclosure, `compare_author.py` verifies the pre-author frozen
hashes, all five author file byte identities and the entire author
certificate against the independently reconstructed nine-layer data.
It checks the author's recorded checker identity and exit code without
rerunning that checker. The new mathematical and finite acceptance rests
on the independent proof and implementation, not the recorded author run.

Acceptance does not establish the separate high-valuation exclusion
certificates, sigma0 joint feasibility, actual base interpolation,
full-support feasibility, distance13 attainment, a lower bound of14,
cryptanalytic advantage, historical priority or Lean compilation. Those
are separate objects and are not upgraded by this receipt.
