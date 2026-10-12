# Independent review of the S0 active-pair module theorem

**PASS, with an explicit scope boundary.** The complete module equivalence, its left and right boundaries, the reversed-image R-chain parametrization, and the fixed-mask mod-8 exclusion are correct at the frozen proof version below. The particular affine-fibre certificates and the reported 32/4 enumeration have only been hash-checked, not independently audited in this review.

## 1. Mathematical review

The independent derivation in `INTERFACES.md` starts from the original FIPS recurrence and S0. It gives all 48 unfiltered equations and exactly 24 nontrivial active rows. The author's Section 1 matches them: seven links make d(P0),d(Q1),d(P1),d(Q2),d(P2),d(Q3),d(P3),d(Q4) a common D; the other 17 rows are the stated interfaces. Substitution and sign changes prove equivalence in Z/(2^32); no division or field assumption on that ring is involved.

The reversed-image construction is complete. For a next pair (v,w), the independently reconstructed previous pair (a,a-G(v,w)) equals the author's (g(w)+c,g(v)+c) under the unique translation c=a-g(w). Conversely that difference equation forces precisely this translation. The original bit matrix of g has rank 32, as independently certified by all 32 inverse-basis equations, so an unequal terminal pair yields four unequal R pairs. The five-word parameterization does not assert that the later P/Q modules are nonempty.

The Section 2 module table supplies every remaining interface. Its modules use disjoint actual pairs once the R chain and D are fixed. It preserves Q0's distinct left boundary, including G(Q1)=-d(Q0), rather than silently setting d(Q0)=D. The nonzero D ensures all P and Q1,...,Q4 pairs are unequal; Q0 is explicitly required unequal, and the R chain already has that property.

The right completion is valid: the first middle module supplies an actual Q2 with d=D and G=-D, and that same ordered pair can be assigned at Q4 because only those two Q4 interfaces occur. This proves existence without identifying Q4 with Q2 in every solution. There is no omitted F(Q4), F(P3), or F(R3) constraint in the original t<64 range. Necessity follows by extracting these modules from any complete assignment; sufficiency follows by combining them and this terminal Q4. The criterion quantifies over actual pairs throughout, so it does not confuse independent d/F/G symbols with simultaneously realizable interfaces.

The mask exclusion follows directly from t45 and t54, which force G52=F30. Independent per-bit calculations give f(889b945b)=4314a785 and g(4314a785)=c722ccc1. Thus F30 mod 8 belongs to {3,5}, whereas G52 mod 8 belongs to {1,7}. These disjoint sets exclude precisely the stated fixed-mask family for arbitrary base words and all higher carries. The same argument also excludes the symmetric low-mask pair (1,5). It uses neither the chosen D nor P masks nor any 32/4 enumeration.

After comparison, the elementary signed-bit formula (3) and homogeneous condition (4) in Section 3 were also checked mathematically: the top output sign is immaterial modulo 2^32, and halving an even canonical residue gives a unique sum below 2^31. The resulting constraints on the common input word are binary linear. This validates that formula, without validating any particular stored matrix, affine basis, dimension, or enumerated fibre.

## 2. Finite verification and independence

The original-equation derivation, code, and run were frozen in `PRECOMPARISON_FREEZE.json` before any author construction file was read. The claimed masks and intended interface were supplied as review targets; this is not a claim of independently discovering them. All five precomparison hashes remained unchanged afterward.

The standard-library checker reconstructs the original five indices for every t=16,...,63 and compares the reduced rows with separate family formulas. It checks all 64 inverse-basis equations for f and g, one deterministic complete R-chain parametrization and recovery, and all eight possible low-bit bases for each output mask. It ran under Python 3.12.14, exited 0, and rejected eight damaged controls: omission of each of t16,t17,t18,t58,t59,t60; reversal of the G52 sign at t54; and an equal initial R pair. Raw output and the actual execution receipt are saved.

Read-only reproduction from the repository root:

```sh
python workstreams/CRYPTO3-20261012/sha256-word-distance/active-pair-review/check_interfaces.py
```

The optional `--record PATH` flag explicitly creates a new result record. No SAT solver or author module is imported. No author checker, probe, or enumeration was run.

## 3. Exact reviewed version and remaining limits

Author proof SHA256:

```text
3c1423e3bc45e926d506017a512a6ee266d37dd8c338575612a1a0559f9365eb
```

All 13 files in the author's manifest matched their stored hashes. This integrity check is not an endorsement of all claims in those files. In particular the Section 4 seed, particular affine bases and dimensions, 32 Q pairs, two triple-interface Q pairs, four P pairs, 16 remaining Q differences, and uniqueness of the surviving P target were not independently audited. No such fact is needed for the two accepted core statements.

This review supplies no complete 13-pair assignment and no true schedule. It does not re-establish support classification or the base-lift reduction, and it does not improve the known global lower bound 13. The review is an independent AI technical check, not external human peer review, a Lean proof, formal main integration, or a historical priority claim.

Definition source: [NIST FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf), sections 4.1.2 and 6.2.2.
