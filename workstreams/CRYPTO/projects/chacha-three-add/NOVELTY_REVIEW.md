# Novelty review: exact signed linear correlation of the ChaCha three-add component

**Audit date:** 2026-10-11 UTC. **Reviewer:** independent Literature Review Agent (`survey_hashes`), not the discovery or implementation-verification agent. This is an internal agent audit, not human peer review.

**Decision: originality is NOT cleared.** Preserve the candidate identity and its evidence, but do not classify it as a confirmed original L2 result or an improvement of a published attack. The full local formula has not been matched to an accessible predecessor during this audit; several exceptionally close papers remain unavailable in full. Their absence is a material uncertainty, not evidence of novelty. The unmasked two-carry component and generic finite-state exact calculation are prior art.

The project proof inspected was `proofs/special_bit_signed_correlation.md`, SHA256 `184c9f29b147e4035ac155a1e375accbc0fd58cb591fc222bdc84e3fe5281d73`. Repository HEAD at inspection was `b3b24135d0c71fae7a97f48a8e1c00c73496fffd`; the project was uncommitted. This review does not certify subsequent edits. The experiments file was not used to establish originality or independently validate the theorem.

## 1. Exact object being compared

For independent uniform n-bit words `a,b,c,d`, write all additions modulo `2^n` and let `R_k` denote left rotation:

```
s = a + b
t = R_r(d XOR s)
u = c + t
v = R_q(b XOR u)
w = s + v
L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d)
```

The claim concerns `r,q >= 1`, `i=r+q<n`, and the **signed linear correlation**

\[
C=E[(-1)^{w_i\oplus L_i}]
 =-\frac{1}{3\,2^r}-\frac{1}{7\,2^q}
  +\frac{4}{3\,2^{3r+2q}}+\frac{1}{7\,2^{3r+q}}.
\]

Equivalently, the input masks are

| Word | Mask support |
|---|---|
| `a` | `{0,i}` |
| `b` | `{0,r,i}` |
| `c` | `{r}` |
| `d` | `{0}` |
| output `w` | `{i}` |

Thus for `(n,r,q)=(32,16,12)`, the compared relation is `w[28] XOR a[28] XOR a[0] XOR b[28] XOR b[16] XOR b[0] XOR c[16] XOR d[0]`, with claimed correlation `-47180567524833621/1180591620717411303424`. Equality probability is `(1+C)/2`, not `C`; bias in the convention `Pr[equality]-1/2` is `C/2`.

This is a uniform-state local linear coefficient. It has no input difference, so it is neither an XDP nor a differential-linear coefficient. It is not a key-recovery attack. Fixing the standard first-row word changes the distribution and requires a separate result. No published attack complexity follows by replacing a carry-product estimate with this coefficient without matching the actual masks, round positions, and distributions.

## 2. Ten nearest predecessor families

### N1. Okada, Nagai, Miyaji: *Refined Linear Approximations for ARX Ciphers and Their Application to ChaCha*

**Status/date:** INDOCRYPT 2025, LNCS 16372, pp. 70–91; first online 2025-12-11, book copyright 2026. [Publisher](https://link.springer.com/chapter/10.1007/978-3-032-13301-4_4); [ePrint 2025/2128](https://eprint.iacr.org/2025/2128).

**Established content:** exact probabilities for linear approximations of two consecutive additions with three independent variables, used to correct ChaCha bias estimates affected by unjustified independence. **Access:** publisher abstract and references; full chapter unavailable. The ePrint was received 2025-11-21 and withdrawn 2025-11-23; its note points to the published version. This is not evidence that the mathematics was retracted.

**Comparison:** strongest direct novelty risk. The project's proof reduces its three-add network to a weighted sum of two-add/three-input linear coefficients. The exact masks and generality of N1's theorem must be checked. An assertion that N1 covers only a different number of additions would be invalid: the transformed mathematical object, not the surface program, controls equivalence.

### N2. Coutinho, Souza Neto: *Improved Linear Approximations to ARX Ciphers and Attacks Against ChaCha*

**Status/date:** EUROCRYPT 2021, LNCS 12696, pp. 711–740; [DOI](https://doi.org/10.1007/978-3-030-77870-5_25), [ePrint 2021/224](https://eprint.iacr.org/2021/224). The ePrint was revised 2021-09-22. **Full text inspected:** official [CEPESC collection](https://www.gov.br/abin/pt-br/assuntos/tecnologia/CEPESC_coletanea.pdf), collection PDF pp. 34–63, printed pp. 711–740.

**Established content:** §3 uses Wallén's single-add carry rules, adjacent-bit cancellation, quarter-round approximations, and piling-up to build longer masks. Printed p. 731 explicitly acknowledges that independence does not hold and explains discrepancies with experiments.

**Comparison:** the paper already identifies the dependence problem. Its §3.1 masks and formulas are not the candidate's seven-input-bit forward relation or the general `(r,q)` closed form. That observation is restricted to inspected statements; it does not prove the candidate is not a consequence of its methods plus older carry theory. The project's deliberately false carry-product baseline must not be attributed to this paper without an equation-level match.

### N3. Coutinho et al.: *Latin Dances Reloaded: Improved Cryptanalysis Against Salsa and ChaCha, and the Proposal of Forró*

**Status/date:** ASIACRYPT 2022, pp. 256–286, [DOI](https://doi.org/10.1007/978-3-031-22963-3_9); expanded [Journal of Cryptology 36, article 18](https://link.springer.com/article/10.1007/s00145-023-09455-5), published 2023-05-01. The journal adds Santanu Sarkar to the six conference authors.

**Full text:** conference publication inspected from a [public copy](https://jackgiffin.com/main/pdfs/Coutinho-Latin-Dances-Reloaded-2022.pdf); publication identity checked against the publisher and [IACR archive](https://www.iacr.org/archive/asiacrypt2022/137910004/137910004.pdf). Journal abstract, references, and accessible appendices inspected; main body unavailable.

**Established content/comparison:** conference §3.1, Lemmas 4–7 give general-rotation half-round rules from zero carry, single-carry approximation, and adjacent-bit relations. They are not an exact evaluation of the candidate's coupled three-carry expression. Combining approximations uses piling-up. The candidate's rotations and seven-bit mask should be translated into these rules and compared with the additional journal proofs before declaring a new derivation rule.

### N4. Li, Ding, Wang, Wang, Wan: *New Derivation Rule for Linear Approximations and Its Application to ChaCha*

**Status/date:** ICISC 2025, LNCS 16487, pp. 471–491; published 2026-05-01. [Publisher/DOI](https://link.springer.com/chapter/10.1007/978-981-95-8034-7_25). **Access:** abstract and references; full text unavailable.

**Established content:** a general ARX rule reduces active bits; combinations improve stated 3.5-round correlation to `-2^-40` and 4-round correlation to `2^-48`.

**Comparison:** direct rule-level competitor, including signed linear coefficients. These are longer-round masks, not a verified match for the candidate. The exact local rule, its independence conditions, and whether the candidate masked moments are immediate corollaries remain unchecked. Merely observing a negative correlation is not novel in view of these and earlier works.

### N5. Li, Ding, Wang, Wan, Wang: *Mixderive: A New Framework of Deriving Linear Approximations and Improved Differential-Linear Distinguishers for ChaCha*

**Status/date:** ISPEC 2025, LNCS 16418, pp. 127–144; published 2026-05-01. [Publisher](https://link.springer.com/chapter/10.1007/978-981-95-9284-5_8); [ePrint 2025/1670](https://eprint.iacr.org/2025/1670), received 2025-09-15. ePrint has four authors and is marked a major revision relative to the proceedings with five authors; versions are not interchangeable.

**Established content:** three-case framework deriving 2-, 2.5-, 3.5-, and 4-round masks, then DL distinguishers with stated complexities `2^162.28` and `2^247.08` for 7 and 7.5 rounds. These are the paper's claims, not independently revalidated here or certified latest records.

**Comparison:** exact masks/rules unavailable, therefore a second substantial full-text gap. No time/data advantage over these attacks has been established by the candidate.

### N6. Niu, Beyne, Hu, Wang: *Cryptanalytic Properties of Mealy Machines*

**Status/date:** CRYPTO 2026, LNCS 16805, pp. 374–405; published 2026-08-11. [Publisher](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13); [ePrint 2026/1193](https://eprint.iacr.org/2026/1193), received 2026-06-07, revised 2026-07-27; [53-page author version](https://hukaisdu.github.io/files/papers/2026-1193-mealy-machines.pdf) inspected.

**Established content:** Theorem 2 evaluates cryptanalytic properties by state transition matrices; §5.2 gives explicit linear correlations of addition by a constant; §7 treats conditional linear correlations in partitioned Chaskey/LEA structures. It corrects an LEA conditional coefficient from `-3/4` to `-1`.

**Comparison:** finite-state signed counting, fixed-addend dependence, and exact conditional correlations are existing methods. The paper has no named ChaCha application in its searchable text. A new closed form or provable lower state complexity for this precise rotated network could still be a contribution; generic computability alone neither establishes nor disproves that narrower novelty. Any `O(r)` claim must state its arithmetic model and compare actual matrix dimensions and bit costs.

### N7. Sarkar: *On Approximating Addition by Exclusive OR*

**Status/date:** [ePrint 2009/047](https://eprint.iacr.org/2009/047), received 2009-01-29, revised 2009-02-03. Metadata says published elsewhere but does not identify where; no venue is invented here. [PDF](https://eprint.iacr.org/2009/047.pdf) was search-readable; local retrieval returned 403.

**Established content:** exact finite-position computation for the sum of any fixed number of independent uniform words versus their XOR; explicit closed forms for up to four inputs and an asymptotic formula involving Eulerian/Bernoulli numbers. For three inputs, equality probability tends to `1/3`. The revision explicitly credits Staffelbach–Meier's CRYPTO 1990 antecedent.

**Comparison:** the project's unmasked moment `M0` is precisely a three-input addition/XOR coefficient, so this component must be classified as L0. The rotation-dependent masked moments and weighted reduction are outside the unmasked statement identified here; their novelty still requires N1/N8 and general linear-mask comparison.

An additional predecessor is [Alquié, *Approximating Addition by XOR: how to go all the way*, ePrint 2010/072](https://eprint.iacr.org/2010/072), received 2010-02-11 and last revised 2010-06-24. It gives a systematic explicit-formula construction and acknowledges earlier carry-matrix work of Holte (1997). This reinforces that finite carry eigenvalues and closed forms for unmasked sums are old. It does not, from the inspected portions, certify coverage of the candidate's particular unequal input masks.

### N8. Nyberg, Wallén: *Improved Linear Distinguishers for SNOW 2.0*

**Status/date:** FSE 2006, LNCS 4047, pp. 144–162. [Publisher](https://link.springer.com/chapter/10.1007/11799313_10); [author paper](https://www.tcs.hut.fi/Publications/knyberg/snowpreproc.pdf). Full retrieval failed (502/timeout); abstract and bibliography verified.

**Established content:** improved linear-bias analysis of the SNOW 2.0 finite-state machine, and a stated distinguisher using about `2^174` words/work. N1 cites this paper alongside Wallén 2003 and linear-hull theory.

**Comparison:** a necessary older-source check for the exact three-input masked coefficients in the project's reduction. This audit does not assert an unread theorem covers those masks. Its full text, and its SNOW predecessors, remain required before calling the intermediate moment identities new.

### N9. Miyano: *Addend Dependency of Differential/Linear Probability of Addition*

**Status/date:** IEICE Transactions on Fundamentals E81-A(1), pp. 106–109, published 1998-01-25. [Publisher](https://globals.ieice.org/en_transactions/fundamentals/10.1587/e81-a_1_106/_p). Full text unavailable; bibliographic identity and abstract verified.

**Established content:** differential and linear probabilities of `Y=X+K mod 2^w` expressed as functions of fixed `K`. N6 explicitly acknowledges this predecessor and supplies an explicit linear-correlation algorithm.

**Comparison:** fixing a ChaCha constant is a meaningful change of distribution, but the fact that addend values change linear bias is not new. A fixed-first-word three-add formula must be compared to N6 §5.2 and this predecessor; one cannot claim novelty merely from computing four standard constants.

### N10. Bellini, Grados, Makarim, Sanna: *Finding differential trails on ChaCha by means of state functions*

**Status/date:** International Journal of Applied Cryptography 4(3/4), pp. 156–175, 2024; canonical publisher DOI `10.1504/IJACT.2024.138416`. [Publisher](https://www.inderscience.com/info/inarticle.php?artid=138416); [institutional record](https://iris.polito.it/handle/11583/2987931); [author-posted full publication](https://www.researchgate.net/publication/380109947_Finding_differential_trails_on_ChaCha_by_means_of_state_functions). Full author-posted text inspected. An institutional 2023 label is not used as the publication date. **Root bibliographic correction:** the inspected author-posted cover/metadata lists `10.1504/IJACT.2024.10063705`; the publisher lists the canonical DOI above and online date 2024-05-03 (accepted 2023-03-08). Both identifiers have observed sources and are retained as a version discrepancy, not silently conflated.

**Established content:** exact half-quarter XDP and ADP computations; heuristically combines halves for quarter-round differentials, with small-word checks. Publication Lemma 4 proves exact half-quarter XDP through an invertible change of variables.

**Comparison:** it does not compute the candidate pure linear coefficient. It does establish that simple fresh-half factorization and small-word tests of quarter-round independence are old. The first-word-fixed version of its half-quarter bijection remains a direct specialization when combined with known constant-add probabilities. Such a result should be archived L0, not promoted as a new ChaCha attack.

## 3. Equivalent mathematics: where a direct-corollary check must focus

The following is the reviewer's comparison of the project's written derivation, not an independent verification certificate.

The project's `M0` and `M_(ell,p)` arise from uniform `S,B,V` after the invertible variable change. Introduce `A=S-B mod 2^n`. Then `A,B,V` are again independent uniform words, and

\[
[B_{<i}>S_{<i}]\oplus[S_{<i}+V_{<i}\ge 2^i]
 =(A+B+V)_i\oplus A_i\oplus B_i\oplus V_i.
\]

Consequently `M_(ell,p)` is exactly the linear coefficient of **three-input modular addition** with input masks

\[
(e_i,\ e_i\oplus e_\ell,\ e_i\oplus e_p)
\quad\text{and output mask}\quad e_i.
\]

This turns the novelty question into a concrete comparison: do N1, N8, or earlier multi-input-addition Walsh formulas explicitly evaluate these masks, or produce `2^(ell+p-2i)` immediately? The project's unmasked coefficient is `-1/3+4/(3*2^(2i))`, the known three-input addition/XOR problem. The remaining assembly uses the elementary finite Walsh expansion of an affine integer-valued function and a geometric series. If the masked coefficients are already explicit, the final result may be only a straightforward application to a rotated network; that needs an honest assessment of the remaining insight and cryptanalytic utility.

Conversely, the presence of a general automaton method does not by itself prove that a compact, parameter-uniform closed form has previously been stated or that it can be obtained at the same cost. An originality decision needs a reduction and a comparable output/complexity, not a title match.

### Addendum: arbitrary-bit reduction and conditional-sign extension

The discovery agent subsequently reported a broader reduction. For an arbitrary output bit `i`, define `j=(i-q) mod n`, `k=(i-r-q) mod n`, and independent uniform transformed words `S,B,Y`. Let `beta` be the borrow vector for `S-B` and `gamma` the carry vector for `S+Y`. Define

\[
M_0=E(-1)^{\beta_i\oplus\beta_k\oplus\gamma_i},\qquad
M_{h,l}=E(-1)^{\beta_i\oplus\beta_k\oplus\gamma_i\oplus B_h\oplus Y_l}.
\]

Its proposed exact reduction is

\[
C_i=2^{-j}\left(M_0-
\sum_{\substack{0\le l<i\\ h=(l-q)\bmod n<j}}2^h M_{h,l}\right).
\]

This has at most `n` masked terms plus the base term. Each term can reportedly be evaluated with the two carry/borrow bits as four states, giving `O(n^2)` integer arithmetic operations; fixing `a=A` imposes `B=S-A` and reportedly retains four states. This is a discovery-agent statement awaiting its own exact proof/version and independent verification; this literature audit has not tested its implementation.

For novelty, `k=0` is the three-input-addition mask reduction above. When `k!=0`, substitute `S=a+b`: the additional factor `beta_k` is `a_k XOR b_k XOR (a+b)_k`. The reduced object is therefore two ordinary modular additions **with an intermediate-output linear mask**, precisely the sort of multi-output, signed, conditional state computation covered methodologically by N6. No new four-state DP principle is claimed. The remaining possible contribution is the explicit elimination of rotations/fresh variables and the proof that only linearly many coefficients survive. This must be checked against exact linear-hull composition and the sparse single-add carry spectrum from Wallén's theory. It may be a direct application rather than a new general algorithm; an unmatched numerical constant is insufficient evidence otherwise.

The subsequently inspected `proofs/fixed_first_word.md` gives an `O(r)` arithmetic expression via square-wave/triangular prefix sums. `proofs/fixed_word_sign.md` asserts `C_A>0` precisely for `A=a mod 2^(r+q)=0`, with `C_0=2^-(2r+q)`, `C_1=-2^-(2r+q)`, and a strictly smaller value for `A>=2`. This sign classification is a written project corollary, not a verified-original theorem. It is a more specific mathematical statement than merely fixed-addend dependence, but its provenance still depends on the novelty of the underlying conditional coefficients. N1, N6 §5.2, N9, and constant-addition Walsh theory remain the relevant comparisons. Neither a complete classification nor an arithmetic speed bound automatically establishes publication-level novelty.

## 4. Currentness checks and further necessary sources

The following are additional checks, not substitutes for the ten near-neighbor comparisons.

- **Earlier/later Okada–Nagai–Miyaji material:** [Nagai–Miyaji, ICSS2024-90](https://ken.ieice.org/ken/paper/20250306fcJC/eng/), issued 2025-02-27, presented 2025-03-06, pp. 162–169, already corrects two partial ChaCha linear approximations. [ICSS2025-73](https://ken.ieice.org/ken/paper/20251104EcoL/eng/), issued 2025-10-28, is a Japanese precursor to N1. [Okada–Miyaji, ISEC2025-132](https://ken.ieice.org/ken/paper/202603176ctX/), issued 2026-03-09, explicitly applies N1's two-add carry formula to new 6.5-round distinguishers. All three full texts remain missing. An author's list mentions an ICICS 2026 follow-up, but this audit has not verified its final publication or complete contents.
- **Foundational exact state methods:** [Mouha, Velichkov, De Cannière, Preneel, *The Differential Analysis of S-functions*](https://mouha.be/wp-content/uploads/sfunction.pdf), SAC 2010/proceedings 2011, defines general carry-state matrix evaluation. §3.6 already calculates exact dependent consecutive-add differential probabilities. Its property is differential, so N6 is the more direct linear predecessor. [Wallén, FSE 2003](https://doi.org/10.1007/978-3-540-39887-5_20) supplies the standard single-add linear theory used in N2/N3.
- **Liu, Ren, Sun, Yu, Li (published 2026-10-09):** [*Differential-linear cryptanalysis against ChaCha based on automated tools*](https://link.springer.com/article/10.1186/s42400-026-00671-7), Cybersecurity 9, article 228. Full article inspected. It reports model/measurement discrepancies and signed-cluster analysis, and proposes improved joint-carry modeling. It concerns broader DL modeling, not a verified occurrence of this local exact linear formula. Its reported truncated cluster is not a proof of the entire omitted tail.
- **He, Hu, Niu, Preneel, Wang:** [*Revisiting Differential-Linear Cryptanalysis via a Walsh-Transform Perspective*, ePrint 2026/2013](https://eprint.iacr.org/2026/2013), received 2026-09-14; metadata identifies an ASIACRYPT 2026 version. As of the audit, distinguish acceptance/metadata from an already held conference. [Author PDF](https://hukaisdu.github.io/files/papers/2026-2013-walsh-transform-differential-linear.pdf) gives exact single-add DL matrix methods. The candidate is pure linear, so this is methodological context rather than identical coverage.

## 5. Claim-by-claim disposition

| Proposed contribution | Current novelty disposition | What would change it |
|---|---|---|
| Carry dependencies invalidate naïve piling-up in ChaCha | L0, already explicit in N2 and central in N1 | No new claim permitted at this generality |
| Generic exact finite-state signed counting | L0 methodology, N6 and predecessors | Prove a specific efficiency improvement against an implemented comparable baseline |
| Exact half-quarter XDP / fixed-first-word specialization | L0, N10 plus constant-add theory | Must move beyond that scope |
| Unmasked `M0` identity / its negative limit | L0, multi-input-addition prior N7 | Attribute as background |
| Masked `M_(ell,p)` closed form | **Originality unresolved** | Read N1/N8; compare exact three-input masks, not operation counts |
| Complete uniform-state `(r,q)` identity | **Candidate result; originality not cleared** | Establish a nontrivial difference from N1/N3/N4/N5 and prior masked-addition formulas |
| Fixed `a=A` exact formula / four standard constants | **Candidate extension, not cleared** | Review the final proof and compare N6 §5.2/N9 plus N1; document arithmetic cost |
| Fixed-`A` special-bit sign classification | **Written project corollary; originality unresolved** | Check whether it follows directly from existing conditional-mask formulas; keep correctness review separate |
| Arbitrary output bit via at most `n` four-state coefficients | **Reported reduction; originality unresolved** | Supply proof/version; compare exact linear-hull composition, sparse carry masks, and N6; DP itself is L0 |
| Better reduced-round attack / L3 / full-cipher result | Not established by this project | Same-model attack construction, resource/success analysis, validated improvement over current literature |

## 6. Required next actions and publication decision

1. Keep the exact closed form and independent-verification artifacts as an auditable local research note. Do not broaden parameter sweeps solely to accumulate more examples of a theorem already proved.
2. Finish the fixed-constant derivation if it resolves the actual ChaCha first-column distribution, but label it a conditional candidate until novelty review is updated.
3. Obtain publicly available or legitimately supplied full texts of N1, N4, N5, the main body of the 2023 journal N3, N8, and the Japanese carry-formula follow-ups. This audit did not contact authors, buy access, or bypass access controls.
4. For each candidate, record the exact mask translation and determine whether it is a direct corollary. If so, preserve a useful L0 reproduction or an application note and switch the originality target.
5. A first-paper case would need added cryptanalytic value: e.g. an exact family of useful published masks, a certified failure/correction of a specific published estimate under identical assumptions, or an algorithm with a proved comparable-cost improvement. A single weak local coefficient without such a bridge has uncertain publication value even if its displayed formula is new.

**No external publication is recommended or authorized by this audit.** Level 3 pre-publication novelty checking has not occurred. This is a bounded search through accessible literature as of the date, not an exhaustive guarantee that all papers, theses, code, errata, and equivalent formulations have been found.

Confidence is high that the general carry-dependence and state-counting ideas are prior art, and high that the project's unmasked moment is the old three-input addition/XOR problem. Confidence in originality of the remaining displayed formulas or elimination identity is low while the closest full texts and exact-corollary comparison remain unresolved. This is a reason to narrow and verify the claimed contribution, not to assume an undiscovered breakthrough.

## 7. Retrieval record

See `literature/retrieval_manifest.json` for actual downloads, failures, byte sizes, and SHA256 values, and `literature/SEARCH_LOG.md` for search families, primary URLs, and unresolved access. The replay script is `literature/fetch_public_sources.py`. Third-party full PDFs and extracted text are in ignored `literature/cache/` and are not intended for repository publication. Only the audit, concise metadata, and retrieval helper belong in version control.
