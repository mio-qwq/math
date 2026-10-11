# Source gate and novelty limits

Retrieved 2026-10-11 UTC. The workstream's dated RSA/AES/SHA-256 candidate
comparison contains the initial three-way selection. This file records the
RSA core follow-up. No recovery archive from Sora was supplied or read.

## Original question and quantifiers

Stephen D. Miller, Bhargav Narayanan and Ramarathnam Venkatesan,
*Coppersmith's lattices and “focus groups”: an attack on small-exponent RSA*,
[arXiv:1708.09445v3](https://arxiv.org/html/1708.09445v3),
16 December 2020, introduction Q2 and section 2. Full primary HTML read.
Q2 asks whether algebraic dependence obstructs the attack before its
enabling bound, and how to determine the valid range. It is a research
question, not a universally quantified theorem that two arbitrary short
vectors always suffice. Its fixed RSA model uses balanced p,q, public e
comparable with N, and ed=1 modulo phi(N). The full .284 shift family is
the baseline used here; the refined .292 attack must not be silently
identified with that full family. The theorem we would ultimately seek
must guarantee recovery for every key in an explicitly stated range,
without assuming the required independent equations. A finite failed basis
or an easy common-curve example does not refute such a recovery theorem.

The author's [homepage](https://sites.math.rutgers.edu/~narayanan/) and
the [Boneh author abstract](https://crypto.stanford.edu/~dabo/pubs/abstracts/lowRSAexp.html)
were also retrieved. The former is not an exhaustive bibliography audit.
The original Boneh–Durfee PDF at the author's site was fetched, but its
text extraction is severely garbled; it is not treated as a reliable
full-text novelty check. Cite the IEEE TIT 46 (2000), 1339–1349 paper,
DOI 10.1109/18.850673, for the established attack, with its independence
qualification as explained by MNV. We did not use MNV's focus-group
selection procedure or reproduce its experimental research sequence.

## Subsequent coverage checked

* Feng–Liu–Nitaj–Pan, *Practical Small Private Exponent Attacks against RSA*,
  [ePrint 2024/1331](https://eprint.iacr.org/2024/1331), full PDF read.
  Its root-recovery result uses Assumption 1 concerning a zero-dimensional
  ideal. It does not supply the unconditional no-leakage theorem sought here.
* Jorge Jiménez Urroz, *A new attack to RSA with small private exponent and
  partial information*, [arXiv:2606.24717v2](https://arxiv.org/html/2606.24717v2),
  full HTML read. Its extra information about p+q is a genuine hypothesis;
  its exponent must not be copied into the no-leakage RSA model.
* Abul Kalam, *A note on the analysis of Herrmann–May lattices for small
  exponent RSA*, Scientific Reports 15, 28544 (5 August 2025),
  [DOI 10.1038/s41598-025-10019-9](https://pmc.ncbi.nlm.nih.gov/articles/PMC12325772/),
  full primary text fetched. It corrects one lattice's determinant analysis
  and modifies that lattice. The extracted proof does not provide a new
  treatment of common integer components. Some displayed mathematics is
  missing from the extraction; this is not a complete audit or a claim
  that the paper's attack is invalid.

## Equivalent mechanisms and prior art

* Aurélie Bauer and Antoine Joux, *Toward a Rigorous Variation of
  Coppersmith's Algorithm on Three Variables*, EUROCRYPT 2007,
  [DOI 10.1007/978-3-540-72540-4_21](https://link.springer.com/content/pdf/10.1007/978-3-540-72540-4_21.pdf).
  Full paper retrieved; sections 2–4 and the applications examined. It
  already treats ideal membership, primary components, and additional
  independent equations using Gröbner bases. Claiming that “use ideals
  instead of resultants” is our new idea would be wrong. Its sufficient
  conditions do not establish our RSA target merely by citation.
* Bernstein–Chang–Cheng–Chou–Heninger–Lange–van Someren,
  *Factoring RSA keys from certified smart cards: Coppersmith in the wild*,
  [author PDF, 2013-09-16](https://smartfacts.cr.yp.to/smartfacts-20130916.pdf),
  common-factor discussion and surrounding sections examined. It reports
  shared linear factors and recovery despite failure of the usual
  independence heuristic. Our finite control is therefore not a novel
  discovery of this general phenomenon. Our theorem concerns ideal-power
  inheritance for the particular RSA polynomial, not these smart-card keys.
* Henry Cohn and Nadia Heninger, *Ideal forms of Coppersmith's theorem and
  Guruswami–Sudan list decoding*, [arXiv:1008.1284](https://arxiv.org/abs/1008.1284),
  full PDF fetched; ideal and valuation sections examined. This is broad
  prior art for ideal-based small-root theory, not evidence that the mere
  introduction of a valuation is original.
* Steven Galbraith, *Mathematics of Public Key Cryptography*,
  [chapter 19](https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch19.pdf),
  sections 19.1 and 19.3 examined for the standard univariate theorem and
  the distinction from bivariate integer equations. The projection identity
  in our proof is an elementary baseline, not a new Coppersmith theorem.

Searches included common factors, primitive/content conditions, ideal
powers, weighted Gauss valuations, saturation, and algebraic independence
in RSA lattice attacks. No exact match to Proposition A and its content
defect was found in the materials actually inspected. That is **not** an
originality certificate: these are elementary consequences of standard
valuation theory, and equivalent formulations may exist. Bauer's 2008
thesis and the full optimality literature remain substantive coverage gaps.
Some broad search results were irrelevant and were discarded.

Follow-up after the recovery candidates: Takayasu–Kunihiro,
[ePrint 2016/353](https://eprint.iacr.org/2016/353.pdf), full text retrieved;
section 2 explicitly retains the algebraic-independence assumption. It is
relevant prior art on general small-inverse bounds. Keegan Ryan,
*Solving Multivariate Coppersmith Problems with Known Moduli*,
[ePrint 2024/1577](https://eprint.iacr.org/2024/1577), EUROCRYPT 2025,
has a relevant ideal/optimal-lattice framework. Its abstract was checked;
the PDF fetch returned HTTP 403, while the attempted Springer PDF URL
returned landing-page text rather than the paper. Aono–Agrawal–Satoh–Watanabe,
*On the Optimality of Lattices for the Coppersmith Technique*, ACISP 2012,
[DOI 10.1007/978-3-642-31448-3_28](https://doi.org/10.1007/978-3-642-31448-3_28),
and its expanded journal version remain full-text coverage gaps. These
gaps matter especially for the general t=0 reduction; originality remains
unconfirmed. Searches also included powers of Wiener relations, auxiliary
polynomial discriminants, Mahler measure, and small-inverse optimality.

Public code search exposed kionactf/coppersmith and jvdsn/crypto-attacks
documentation warning about root-solving and nonzero-dimensional systems.
Their implementation internals were not audited or used. No external code
is evidence for an unconditional exponent here. No author was contacted.

## Status at the retrieval cutoff

No inspected later source closes MNV Q2 in the required no-leakage model.
We therefore retain it as an unresolved research target with a stated
coverage limit, not as a proven assertion that every subsequent paper has
been checked. Our v1 contains restricted structural and conditional
t=0 recovery proof candidates plus a failed-route certificate; it does not
meet the requested major-result goal.
