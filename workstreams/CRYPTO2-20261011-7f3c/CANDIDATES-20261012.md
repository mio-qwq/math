# Modern-standard source gate — 2026-10-12 Singapore / 2026-10-11 UTC

Three candidates, with bounded goals and no invented numbered conjectures.
Visible CRYPTO branch remains 551fcd7; coordination remains abd8e85.
Other visible agents retain graph/ARC scopes. All initial exclusions apply.

## 1. Ascon: certify error/exactness of propagation approximations — selected

Original direction: Kai Hu, Zhongfeng Niu, Meiqin Wang, *Round-Based
Approximation of (Higher-Order) Differential-Linear Correlation*, EUROCRYPT
2026, ePrint 2026/358, latest revision 2026-06-05. Section 7.4 explicitly
leaves quantification of approximation error open; Assumptions 1 and 2
separate column independence and dropping value masks. This is an
unnumbered future-work direction, not a universal exactness conjecture.

Our initial quantified subproblem: for ALL 320-bit A,B,C, for the actual
two-round Ascon permutation and uniform initial X, compute exactly the
probability of the two specified S-box-layer differences and characterize
when it equals the local DDT product. A general exact low-parameter formula
with useful full-width certificates would be restricted progress; it does
not settle all-round error estimation. A single mismatching certificate
would refute only universal exact-product extrapolation, not the paper.

Direct verification: S-box truth table, binary matrices for actual
rotations, exact fiber counting and rational probability, with no Monte
Carlo acceptance. First risk: output fibers need not be affine (already
seen in a 32-point check). Stop if only generic character orthogonality is
obtained without a useful Ascon conclusion or if same-scope work is found.

Follow-ups checked: official Ascon publication list; 2025 expanded DATF
article DOI 10.1007/s00145-025-09564-3 (already proves selected exact biases);
Courtois et al. ePrint 2024/802 (2026-06-24 revision, partial linearization);
2016/490 undisturbed bits and inverse diffusion; new trail-bound papers.
Full comparison is unfinished. Public code link from source:
https://github.com/hukaisdu/Round-based-approximation (not copied or run).
Originality is unconfirmed. NIST SP 800-232 final (2025-08-13) establishes
the standard relevance. No actual attack complexity claim is intended.

## 2. ML-KEM: dependency-preserving correctness bound — deferred

Original direction: Barbosa, Kannwischer, Lim, Schwabe, Strub, *Formally
Verified Correctness Bounds for Lattice-Based Cryptography*, ePrint
2025/1562 / CCS 2025. Distinguish the formally verified heuristic event
from the actual compression-dependent decryption event.

Exact potential target: upper-bound honest failure for each standardized
parameter set, over explicitly specified primitive randomness and all
messages fixed independently of it, without replacing compression residuals
by independent noise. Direct verification would need exact distributions,
dependency-preserving bounds and a rational terminal certificate.

Source gate found Duriez–Tommasini arXiv:2609.09983, which already claims
a bound <=2^-164.81 for ML-KEM-768 in an explicit fixed-message ROM/CBD
model. We have NOT audited its proof. Thus the natural initial target is
occupied; other parameters or adaptive correctness are separate problems,
not automatically easy extensions. A fixed-SHAKE information-theoretic
claim would also change the model. Stop rather than copying its method or
presenting the old heuristic gap as wholly untouched.

## 3. AES-GCM / GHASH: constrained forgery probabilities — deferred

Source: Saarinen, *Cycling Attacks on GCM, GHASH and Other Polynomial MACs
and Hashes*, ePrint 2011/202, revised 2012-03-16. Its explicit unnumbered
future question concerns mapping weak GHASH generators to block-cipher
keys. That is not solved by another count of field subgroups.

Potential exact target would fix a nonempty subgroup class W and an actual
block cipher E, and find/characterize keys K with E_K(0) in W more efficiently
than the appropriate generic benchmark. Exact candidate K is checked by
encryption and field order; any attack must account for key-search cost,
message length, allowed modifications and success probability. A mere
polynomial-root bound is already classical and is not progress on this
question. Later polynomial/collision literature and GCM-SIV bounds make
repetition risk high. No promising non-generic mechanism established, so
defer before computation. No uncertainty is turned into an openness claim.

## Continuity note on previous result

The full tool-extracted 2026-06-11 revision of Otal–Sulce–Yayla 2025/2240
is now available and inspected for its theorem statements and final
questions. Its scope remains orders 2/3 plus diagonal equivalence; Section
7 still cites KYS as partial progress for n>=5. It does not supply the
all-order circulant completion in the inspected text. The earlier frozen
source gate remains historical; Toeplitz full text and Whirlwind full text
are still missing. This narrows a gap but does not certify originality.
