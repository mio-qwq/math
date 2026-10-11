# Source-backed candidate gate — 2026-10-11

## 1. Remaining circulant orders for related differentials — SELECTED

Kumar, Yadav, Samanta, arXiv:2605.27535v1, Theorem 5 and unnumbered final
question in Section VI. All matrices in this paper are over F_(2^m).
Theorem 5 covers n not congruent to ±2 mod 12. The final paragraph mentions
the remaining cases without giving a numbered conjecture or full formula.
We therefore distinguish that source question from our exact proposed
theorem: every invertible circulant of order n>=3 over every F_(2^m)
has distinct nonzero u,v with u_i v_i(u_i+v_i)=0 and
(Mu)_i(Mv)_i((Mu)_i+(Mv)_i)=0 for every i.

- A counterexample would be one such invertible matrix for which every
  distinct nonzero pair fails at least one condition; a universal existence
  proof would fill the source's remaining MDS orders n>2.
- Verify certificates by field arithmetic and raw matrix multiplication,
  never by just trusting the constructor's quotient or support labels.
- First key hypothesis: a periodic restriction remains invertible, though
  it need not be MDS. Deal with non-MDS quotients explicitly.
- Stop if the property needs stronger nontriviality not preserved by lifting,
  or if a same-scope theorem is found. Do not expand numerical searches to
  substitute for a missing proof.
- Substantively disjoint from CRYPTO: object = linear diffusion matrix;
  goal = existence of related differential pairs; mechanism = invariant
  coordinate subspace and linear algebra. No APN/Sidon-period argument.
- Gate: only v1 displayed by arXiv on retrieval. Title, equivalent-property,
  quotient/periodic, author-page and public-code searches found no later
  same-scope theorem. This is bounded evidence, not proof of openness.

## 2. Characterization of general 4-by-4 MDS matrices without RD — DEFERRED

Same authors/version, Section VI first future direction: extend their
3-by-3 characterization (Theorem 7, 15 polynomial tests) to order four.
Exact objective would quantify over every m>=1 and every 4-by-4 MDS M
over F_(2^m), and give necessary and sufficient conditions for absence of
the distinct nonzero pair defined above. It is a classification request,
not a conjectured equality to refute.

- Substantial output: a provably complete reduced condition set, or a
  structural classification beyond the known generic rank-search method.
- Direct verification: enumerate admissible zero/equality patterns and
  exact kernels; cross-check small fields using original vectors.
- Important antecedents: Daemen–Rijmen 2009 Section 8 already supplies
  generic algorithms. Jha–Li–Gligoroski 2025 Theorem 3 handles the Hadamard
  subclass with 28 conditions. Reprinting a generic algorithm is not new.
- First test: determine whether symmetry-free support types actually yield
  new structure. Stop if output is only a larger list of known determinants.
- No visible project member owns this matrix scope. Latest title/author
  searches did not locate a complete general 4-by-4 classification; the
  same-source author page is stale (April 2026), so it cannot certify this.
- Lower priority than Candidate 1: higher duplication and bookkeeping risk.

## 3. Tu–Deng modular pair-count bound — CLOSED AT THE GATE

Tu–Deng 2011 conjecture, exact formulation restated in Liu–Luo–Xie,
arXiv:2608.05187: for every integer k>=2 and 1<=t<=2^k-2, with N=2^k-1,
the number of (a,b) in {0,...,N-1}^2 satisfying a+b=t mod N and
wt(a)+wt(b)<k is at most 2^(k-1). A violating (k,t) with an exact count
would refute it. An integer carry-transfer proof could establish the bound.
This is about binary-weight combinatorics for cryptographic Boolean functions,
not APN differential-support periods.

However, current retrieval finds full-proof claims by Liu–Luo–Xie
(2608.05187) and Cusick (2608.14821), and Cheng (2608.22451) explicitly
claims all equality cases and resolves Flori et al. Conjecture 3.20.
These proof claims were not independently audited here. They suffice to
reject a fresh claim that the old bound/equality problem remains untouched.
No discovery computation or further author/code gate is warranted for this
rejected route; no novelty claim is made. Reopen only on a precise, sourced
unresolved statement not covered by those papers.

## Sources and retrieval limits

- https://arxiv.org/abs/2605.27535 (version history)
- https://arxiv.org/html/2605.27535v1 (definitions, Theorems 2,4,5,7, Section VI)
- https://cs.ru.nl/~joan/papers/JDA_VRI_LinearMaps_2007.pdf
  (Daemen–Rijmen, *New criteria for linear maps in AES-like ciphers*,
  Cryptography and Communications 1, 47–69, 2009; Sections 7–9).
- https://cic.iacr.org/p/2/1/37/pdf (Jha–Li–Gligoroski, IACR CiC 2(1), 2025,
  DOI 10.62056/a6ksdk5vt; publisher PDF read through search service).
- https://ssamanta.org/research (author's public publication list).
- https://arxiv.org/abs/2608.05187
- https://arxiv.org/abs/2608.14821
- https://arxiv.org/abs/2608.22451

No private author communications, submission, DOI creation, or code-repository
contact occurred. A search that finds no code is not an audit of nonexistent
or undiscovered code. Post-result source refresh remains mandatory.
