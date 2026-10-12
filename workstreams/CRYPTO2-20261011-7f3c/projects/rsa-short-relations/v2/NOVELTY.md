# RSA v2: prior-art and significance gate

Date: 2026-10-12 UTC. Author: CRYPTO2-20261011-7f3c.
Baseline local 0967246290572a4aadd4574627395e8187adc046; remote
7144a9245827c4cd1f45449e0776e46f2599f6fb. Frozen v1 is unchanged.

## Decision before formalization

The t=0 result is retained as a restricted structural proof candidate, but
is **downgraded as a key-recovery research result**. Its output conditions
force ordinary RSA keys into a classical continued-fraction recovery range.
This is stronger information than the earlier statement that we had merely
not yet improved an exponent. No further attempt to optimize this t=0
attack is justified. SHA-256 becomes the research priority.

This is not a finding that the full polynomial-factor statement appears
verbatim in an earlier source. Historical novelty of that narrow structural
statement remains unconfirmed; its cryptanalytic usefulness is limited
regardless. Formalizing standard arithmetic is verification, not novelty.

## Sources actually inspected in this gate

1. Aono–Agrawal–Satoh–Watanabe, *On the Optimality of Lattices for the
   Coppersmith Technique*, ePrint 2012/108, manuscript dated 2015-12-18.
   Full text retrieved at https://eprint.iacr.asia/2012/108.pdf after the
   original PDF returned 403. Sections 4, 5.4 and 6 inspected. Section 6
   already takes the highest x-row and transfers it to a univariate
   canonical polynomial. This is close prior art for our leading-row
   reduction, which must not be advertised as a new technique. Its bounds
   retain the hypotheses of its framework, including Assumption 1 in the
   cited Theorem 2. We do not claim an unconditional general optimality bound.
   The 2012 conference manuscript on the author's ResearchGate upload was
   also inspected; it is not identical to the expanded 2015 manuscript.
   The Springer reference to 2012/134 is not a reliable ePrint identifier:
   that actual landing page belongs to Poulakis–Rolland's signature paper.
2. Keegan Ryan, *Solving Multivariate Coppersmith Problems with Known
   Moduli*, EUROCRYPT 2025, ePrint 2024/1577, full text retrieved at
   https://eprint.iacr.asia/2024/1577.pdf. Sections 2.5–4 inspected.
   Heuristic 1 explicitly assumes a zero-dimensional recovered variety.
   Section 3 uses ideal powers and attributes earlier ideal formulations.
   Our use of ideals alone is not new. Public implementation README:
   https://github.com/keeganryan/cuso (read; implementation not audited).
3. Chinburg–Hemenway–Heninger–Scherr, arXiv:1605.08065v1,
   *Cryptographic applications of capacity theory: On the optimality of
   Coppersmith's method for univariate polynomials*, Sections 1, 3 and 6:
   https://arxiv.org/html/1605.08065v1. Discriminant integrality and
   archimedean/nonarchimedean constraints are established prior mechanisms.
   The HTML rendering has a later generated date; do not use it to redate
   the original 2016 work.
4. Kurt Mahler, *An inequality for the discriminant of a polynomial*,
   Theorem 1, https://carmamaths.org/resources/mahler/docs/154.pdf.
   The bound |Disc(P)| <= h^h M(P)^(2h-2) is classical, not our theorem.
5. Kosaian–Tan, *Formalizing Coppersmith's Method*, Isabelle AFP entry
   dated 2024-06-10, https://isa-afp.org/entries/Coppersmith_Method.html.
   Univariate Coppersmith and Howgrave-Graham already have formal proofs.
   Changing prover does not establish mathematical novelty.

Searches covered RSA, small inverse, common factor, short polynomial,
ideal power, Mahler measure, discriminant, capacity and optimal lattices.
No complete claim of literature coverage is made. Bauer's thesis and
equivalent algebraic-number-theory formulations remain coverage gaps.

## Scope audit to prove

Assume the conclusion of GENERAL-PROOF-v1 supplies r>0,t,u with
e*u=r*N+t and 3*X*max(r*Y,|t|)<e. The proved lift gives u*k=r*d.
Since gcd(k,d)=1, r=g*k and u=g*d for a positive integer g. Therefore
3*k^2*Y <= 3*X*k*Y <= 3*X*r*Y < e.
For ordinary RSA, s=p+q-1>=1 and e*d=1+k*(N-s), so

    |N/e-d/k|=(k*s-1)/(e*k)<Y/e<1/(3*k^2)<1/(2*k^2).

Thus d/k is a continued-fraction convergent of N/e by the classical
Legendre criterion. Enumerating these convergents and checking RSA factors
recovers the key without being given H. This corollary is conditional on
the written factor-existence proof, whose full Lean formalization is a
separate obligation. No silent assumption that a factor exists may appear
under a theorem name claiming the full high-degree result.

The scope audit uses s>=1, which is true for RSA but is stronger than the
general signed-s arithmetic model of v1. Keep this restriction explicit.
