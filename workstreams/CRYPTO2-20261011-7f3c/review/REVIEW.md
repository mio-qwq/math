# Independent mathematical review

**Verdict: PASS for the full stated universal mathematical theorem.** No missing assumption or mathematical gap was found for an invertible circulant of order n>=3 over an arbitrary field of characteristic 2. This is a mathematical review, not a certification of historical novelty, formal verification, or cryptanalytic impact.

## Reviewed artifact and independence record

The artifact reviewed was `PROOF.md` with SHA256

`5526707c49ab8864f54a11c816f6bebd95bf981115577dc584ab25c221956fd4`.

Before opening that artifact, I reconstructed a complete proof and ran small exact checks using my own code. The reconstruction is `PRE-DISCLOSURE.md`, sealed at SHA256

`4204393f57b58417536e2db262e12e7dcd2648917cda7c86db3ea732a1ffc92a`.

This reconstruction was independent of the discoverer's proof and program. It was informed by reading the original source paper and original Daemen–Rijmen definitions, as requested. No discoverer constructor/checker was read or imported. No subagents were spawned, no external authors were contacted, and no files outside this review directory or Git refs were modified.

## Core conclusion

For every field K of characteristic 2 and every invertible n-by-n circulant M with n>=3, there exist nonzero distinct u,v such that each coordinate of (u,v), and each coordinate of (Mu,Mv), has a zero entry or equal entries. Invertibility also makes Mu,Mv,Mu+Mv nonzero. The proof establishes the full universal statement rather than merely checking bounded finite fields.

The central proposed step is valid. For every d dividing n, the repetition map J:K^d -> K^n is injective and its image is M-invariant. Grouping the circulant coefficients by residue modulo d gives a d-by-d circulant B satisfying MJ=JB. If Bx=0, invertibility of M and injectivity of J force x=0. Thus B is invertible even in characteristic 2 and even when n/d=2. Repetition preserves both nontriviality and the coordinatewise relation. Neither division by n/d nor a claim that B is MDS is needed.

For n=2 modulo 4 with n>=3, d=n/2 is odd and at least 3. Therefore the odd invertible circulant result applies to B and its witness repeats. This closes every excluded order n=+2 or -2 modulo 12 above 2. It is not invalidated by failure of MDS to descend to B: the odd result explicitly includes a separate non-MDS branch.

## Proof audit

| Step in reviewed proof | Result and reason |
| --- | --- |
| Lemma 1: invertible non-MDS fallback | PASS. The singular proper minor yields nonzero u with zero outputs on selected rows. A singular complementary minor gives disjoint output supports; an invertible complementary minor gives equality on the remaining outputs. Full-matrix invertibility ensures the solved v is nonzero. Disjoint input supports prove u!=v. |
| Lemma 2: odd symmetric invertible case | PASS. In the MDS branch, the cross block is invertible. The two linear solves give the required zero outputs. Equality at the central output is an equality of a scalar and its transpose. Nonzero entries and the positive cross-block size prove the two inputs are distinct. The non-MDS branch is already covered. |
| Corollary 2.1: odd circulants | PASS. Under the stated first-column convention, reversing the output row index produces entries a_(-i-j), a symmetric matrix. A common output permutation preserves the relation. |
| Lemma 3: multiples of four | PASS. The MDS hypothesis in that branch ensures nonzero even and odd coefficient polynomials. Their supports are disjoint. Frobenius squaring in characteristic 2 and reduction modulo X^n-1 with 4 dividing n give the stated output support classes. Non-MDS matrices use Lemma 1. |
| Lemma 4: divisor lifting | PASS. The coefficient grouping has the correct first-column orientation. J is injective. Restriction preserves invertibility and the witness without requiring MDS or division. |
| Main case split | PASS. Odd orders, multiples of four, and n=2 modulo 4 exhaust all n>=3. The last class has odd n/2>=3. |
| Boundary n=2 | PASS. The graph-code weight argument excludes nontrivial pairs for a 2-by-2 MDS matrix. The specified GF(4) example is invertible circulant and MDS. |
| Arbitrary characteristic-2 fields | PASS. Every step uses only finite-dimensional field linear algebra and characteristic-2 identities; no finite-field counting or perfection assumption is used. |

The reviewed proof's first-column convention differs from my reconstruction's first-row convention. I checked both directly; this is only an orientation choice, and the reviewed indices are consistent.

## Primary-source audit and attribution limits

The exact source is Yogesh Kumar, Akshay Ankush Yadav, and Susanta Samanta, *Analyzing Linear Layers in Related-Differential Cryptanalysis*, **arXiv:2605.27535v1**, submitted 26 May 2026:

* https://arxiv.org/abs/2605.27535v1
* Definitions 1 and 2: https://arxiv.org/html/2605.27535v1#Thmdefinition1 and https://arxiv.org/html/2605.27535v1#Thmdefinition2
* Theorem 2: https://arxiv.org/html/2605.27535v1#Thmtheorem2
* Theorem 4: https://arxiv.org/html/2605.27535v1#Thmtheorem4
* Theorem 5: https://arxiv.org/html/2605.27535v1#Thmtheorem5
* Concluding open direction: https://arxiv.org/html/2605.27535v1#S6.p2

The source's Theorem 5 covers circulant orders outside the residues +/-2 modulo 12 over finite characteristic-2 fields. Section VI refers to a natural conjecture for the remaining unresolved cases, but **does not print a fully quantified numbered conjecture**. A search of the original HTML and text confirms that the concluding paragraph is the only conjecture discussion. The accurate claim is that this argument resolves the remaining invertible/MDS circulant cases indicated there, with n>2. It should not be described as proving a specifically numbered conjecture, or as reproducing an exact universally quantified conjecture from the paper.

The source's Definitions 1 and 2 do not themselves spell out exclusion of zero and identical pairs. However, its Section V explicitly discards the trivial triplets (u,u,0): https://arxiv.org/html/2605.27535v1#S5.p4. This corroborates the reviewed proof's nontriviality convention.

The original source for that convention is Joan Daemen and Vincent Rijmen, *New criteria for linear maps in AES-like ciphers*, https://doi.org/10.1007/s12095-008-0003-x. In the supplied original PDF/text, Section 7.1, after Definition 8, excludes the all-zero difference vector. Definition 9 imposes the relation at both input and output. Section 8.2 excludes the solution corresponding to the original differential; Section 8.3 requires more than the two trivial binary codewords. Thus nonzero unequal u,v, with corresponding nonzero unequal outputs, is the appropriate substantive convention. The reviewed theorem satisfies it.

The source's unrestricted “non-MDS matrix” wording should not be imported blindly for singular matrices under that convention; for example, a zero map has only zero output differences. The reviewed proof correctly restricts that lemma and the universal statement to invertible matrices. It also correctly excludes order 1 from the odd base lemma. These are meaningful scope controls, not missing assumptions in the reviewed theorem.

The non-MDS, odd symmetric, odd circulant, and order-four/multiple-of-four ingredients are prior-source ingredients. The period restriction is elementary invariant-subspace algebra. Whether its use here is historically new remains unverified. I did not independently audit the additional Whirlwind (2010) attribution in the proof; its truth is unnecessary for the mathematics, since the multiple-of-four argument is proved in full and appears in KYS Lemma 1. No priority claim should rest on this review.

## Independent computational corroboration

The files `independent_check.py` and `independent_check_results.json` record a small independent exact check:

* All 27 invertible order-3 and all 192 invertible order-4 circulants over GF(4) passed (64 and 256 coefficient lists examined).
* 24 sampled invertible circulants each of orders 6,8,10,14 over GF(4) passed. For the reductions, the checker also verified the full intertwining identity on basis vectors.
* Explicit symmetric MDS Cauchy matrices of orders 3 and 5 over GF(16) passed the MDS-branch construction; all square minors were independently checked.

The independent check uses its own right-circulant order-four formula and then period lifting, so it is not merely a transcription of the reviewed proof's general multiple-of-four program. These tests corroborate the symbolic proof; they do not replace it. No large search or enumeration was repeated.

## Acceptance and limitations

Accept the exact theorem as mathematically proved, subject to ordinary human scholarly scrutiny. No mathematical revision is required to the pinned proof. Source phrasing should remain as careful as in the reviewed statement: completion of the remaining indicated cases with explicit nontriviality and n>=3, without a numbered-conjecture or historical-priority claim.

This review does not establish a Lean proof, acceptance by external referees, a new cipher attack, round counts, attack probabilities, or security complexity bounds. It also makes no assertion about arbitrary singular matrices or fields of other characteristic.
