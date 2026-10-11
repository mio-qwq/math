# Preselection novelty review: fixed a,b,c, uniform d

Date: 2026-10-11. Reviewer: the independent literature-review agent. This is a bounded preselection audit, not a new attack report. Only this new file was written. The preceding literature/METHOD_COMPARISON.md remains frozen.

## 1. Conclusion first

**Recommendation: use this model for calibration and reproduction; do not select “exact fixed-a,b,c correlation values” as an original first-paper claim.** Existing constant-addition and conditional Mealy methods directly provide the required exact evaluator. The two relevant input intervals are nested, and their overlap can be processed in the same order with two one-bit carries. There is no exponential state-width obstacle to overcome.

A useful research increment is to make the distribution explicit: fixing only the first ChaCha word still averages over the two key words in an initial column. Fixing all three of a,b,c produces a different, more relevant local conditional model. Neither the importance of that distinction nor addend-dependent correlations are new.

The precise coefficient family has not been located in a theorem of a predecessor. The closest ChaCha-specific full-text gaps prevent a certified historical-duplication claim. Nevertheless, the available evidence already blocks new-method, new-complexity, or new-attack claims based only on this evaluator or its numerical output.

| Assessment | Decision and reason |
|---|---|
| Mathematical feasibility | High: a direct ordinary four-state construction is given in Section 3. |
| Verification value | High: it distinguishes averaging over keys from fixing a particular key fragment. |
| Original methodological opportunity | Very low for the stated target; exact constant-dependent conditional correlations are established. |
| First-paper suitability | Low without a further theorem or a concrete connection to a published multi-round attack. |
| Resource recommendation | One bounded implementation/verification cycle is justified as a model baseline. Large key scans are not justified by the current goal. |
| Current grade | L0 for the method and model-calibration exercise; no certified-original L1/L2 and no L3/L4. |

## 2. Exact model and its relation to a fixed key

Let a,b,c be specified n-bit constants and let d be independent uniform on all n-bit words. All additions are modulo \(2^n\). Rotations \(R_r,R_q\) are left rotations with \(0\le r,q<n\).

\[
S=a+b,\quad T=R_r(d\oplus S),\quad U=c+T,\quad
Y=R_q(b\oplus U),\quad w=S+Y,
\]

\[
L=a\oplus b\oplus R_q(b\oplus c)
  \oplus R_{r+q}(a\oplus b\oplus d).
\]

For \(0\le i<n\), the target is the **signed linear correlation**

\[
C_{a,b,c}(i;r,q)=E_d[(-1)^{w_i\oplus L_i}].
\]

It is not half the correlation, a differential probability, or a differential-linear coefficient. The first output word of the complete ChaCha quarterround is precisely w: the subsequent operations change d,c,b but do not change w.

The [official RFC 8439 specification](https://www.rfc-editor.org/rfc/rfc8439), Sections 2.1 and 2.3, supplies the quarterround and the IETF input layout. For a first-column quarterround, a is a standard constant, b and c are two words of the fixed key, and d is a counter/nonce word. Thus this local model can describe one first-column component with a specified pair of key words and a uniformly varied full d word. Later quarterrounds do not automatically have this distribution; the 20-round permutation, feedforward and observable keystream are not analyzed here.

| Distribution | What it averages |
|---|---|
| a,b,c,d independent uniform | A local permutation experiment with all four words varying. |
| a fixed; b,c,d uniform | For an initial column, averages over both participating key words as well as d. |
| a,b,c fixed; d uniform | A local conditional experiment for one fixed pair of participating key words. |
| Complete ChaCha with a fixed 256-bit key and a specified public-input process | Includes all columns, diagonal mixing, 20 rounds and feedforward; not implied by the local result. |

For the same a, exact averaging must satisfy

\[
E_{b,c}[C_{a,b,c}(i;r,q)]
= C_{\text{a fixed; b,c,d uniform}}(i;r,q).
\]

This is the law of total expectation, not an attack or an originality claim. It is a useful cross-check between the project's models.

## 3. Direct reconstruction as an existing constant-state calculation

This is the reviewer's mathematical reconstruction of the root's proposed elimination. It does not reuse implementation code. No computational experiment or independent verification certificate is claimed in this file.

### 3.1 Removing the first rotation and the constant first addition

Write \(\kappa=a\oplus b\oplus S\), the carry-into-bit word of the fixed first addition. Let

\[
j=(i-q)\bmod n,\qquad k=(i-r-q)\bmod n,\qquad
\sigma=(-1)^{\kappa_i\oplus\kappa_k}.
\]

The map \(d\mapsto U=c+R_r(d\oplus S)\) is a bijection, so U is uniform. The two remaining carry bits are

\[
\beta_j=[\,U\bmod2^j<c\bmod2^j\,],
\]

\[
\gamma_i=[\,S\bmod2^i+Y\bmod2^i\ge2^i\,],
\qquad Y=R_q(b\oplus U).
\]

The carry/XOR identity gives exactly

\[
C_{a,b,c}(i;r,q)
=\sigma\,E_U[(-1)^{\beta_j\oplus\gamma_i}].
\]

The first-rotation distance r now occurs only in the constant sign \(\sigma\). Consequently the absolute correlation for this particular all-XOR mask is independent of r. This is a change-of-variables corollary, not a new rotation-security result and not a statement about arbitrary masks.

The two marginals are already ordinary constant-addition quantities:

\[
p_\beta=(c\bmod2^j)/2^j,\qquad
p_\gamma=(S\bmod2^i)/2^i.
\]

Their exact combination is

\[
C/\sigma=1-2p_\beta-2p_\gamma+4\Pr(\beta_j=\gamma_i=1).
\]

Replacing the joint probability by a product would introduce an unjustified independence assumption. Exact joint counting uses only the shared interval described next.

### 3.2 The relevant U intervals are nested

The borrow uses source indices \(0,\ldots,j-1\). The final carry uses the rotated source indices

\[
(-q)\bmod n,\ldots,(i-1-q)\bmod n
\]

in that cyclic order. There are only two cases.

**Case I: \(i\ge q\).** Then \(j=i-q\). The final carry first processes the q-bit U tail \([n-q,n)\), which is disjoint from the borrow input. It then processes \([0,j)\), in the same ascending order as the borrow.

The tail induces

\[
\Pr(\gamma_q=1)=\rho=(S\bmod2^q)/2^q,
\]

because those bits of Y are independent uniform even after XOR with fixed b. The first borrow is zero. Start the two-state-pair distribution, ordered as \((\beta,\gamma)=00,01,10,11\), at

\[
v_0=(1-\rho,\rho,0,0)^T.
\]

Process \(h=0,\ldots,j-1\), matching U index h with Y index \(t=h+q\).

**Case II: \(i<q\).** Put \(m=n-q\), so \(j=m+i\). The final carry uses U indices \([m,j)\). The borrow first processes the independent prefix \([0,m)\), then uses that same shared interval in the same order.

The prefix induces

\[
\Pr(\beta_m=1)=\theta=(c\bmod2^m)/2^m.
\]

The final-addition carry starts at zero, so initialize

\[
v_0=(1-\theta,0,\theta,0)^T.
\]

Process \(h=m,\ldots,j-1\), matching U index h with Y index \(t=h-m\).

The intervals are genuinely nested as sets: their union has \(\max(i,j)\) active source bits and their intersection has \(\min(i,j)\) bits. No retained input queue proportional to a rotation distance is needed.

### 3.3 The joint kernel has four states and one random input bit

In either case, let \(u=U_h\) be the sole random input to a shared position. It is a fresh uniform bit. For old state \((\beta,\gamma)\), update

\[
\beta'=[\,c_h+\beta>u\,],
\qquad
\gamma'=\left\lfloor
\frac{S_t+(b_h\oplus u)+\gamma}{2}
\right\rfloor.
\]

For the three constant bits \((c_h,b_h,S_t)\), define a \(4\times4\) matrix K by averaging these two possible transitions with weight \(1/2\). There are only eight constant-bit cases. After the shared interval, take the terminal row

\[
f=(1,-1,-1,1)
\]

and multiply \(fv\) by \(\sigma\). Carries are not constrained to be zero at the end; their parity is the output being averaged.

This is a literal finite-state linear-correlation evaluation with a fixed input-dependent kernel and a specified boundary distribution. It falls under Mealy Theorem 2 and its constant/conditional specializations. The only adaptation is an elementary scheduling of the two nested intervals.

Using integer counts, the initial distribution can be scaled by \(2^q\) in Case I or by \(2^m\) in Case II. Each shared step uses a matrix with entries 0,1,2 and adds one bit of denominator. The resulting denominator divides \(2^{\max(i,j)}\), although the original experiment averages over \(2^n\) values of d.

The construction uses \(O(\min(i,j)+1)\) constant-size updates after reading the constants, hence \(O(n)\) arithmetic operations, with \(O(n)\)-bit counters and \(O(n)\) auxiliary bits. Ordinary addition/shift arithmetic gives an \(O(n^2)\) bit-operation upper bound. These are bounds on a direct application of an established method, not a published-best improvement.

### 3.4 Boundary cases and recommended negative controls

The construction includes q=0, j=0, i=0 and coincident first-carry indices. There is no need to invent special “independent carry” factors.

Useful verification obligations for the implementation agent are:

- If a=b=c=0, w=L for every d, so every correlation is exactly +1.
- If c=0, the middle carry vanishes and the answer is
  \(\sigma(1-2(S\bmod2^i)/2^i)\), an ordinary fixed-addend coefficient.
- If S=0, the final carry vanishes and the answer is
  \(\sigma(1-2(c\bmod2^j)/2^j)\).
- At i=q, j=0 and the shared interval is empty; Case I must still return the correct fixed-addend result.
- Changing r must preserve the absolute correlation for the specified all-XOR mask.
- Averaging over b,c at small word lengths must recover the already established fixed-a model.

These are proposed checks, not claims that this reviewer executed them.

## 4. Why the method is already covered

The available full Mealy manuscript directly supplies the required evaluation principle. Its Theorem 2 uses signed state-transition products; Section 5.2 allows bit-dependent constants; Section 7.2 evaluates correlations restricted to input conditions and explicitly accounts for normalization of the restricted domain. The domain a=A,b=B,c=C is an especially simple bitwise restriction.

If one starts from the uniform four-word domain and imposes the three fixed-word constraints, the restricted signed sum must be divided by the restriction probability \(2^{-3n}\). Equivalently, using U alone from the outset has the correct conditional normalization automatically. This is a familiar restricted-domain calculation, not a new cryptanalytic conditioning operation.

The 1998 addend-dependency work and the later constant-addition matrices already explain why a key/addend changes a linear probability. The 2020–2022 partitioning literature and Mealy's exact conditional treatment explain why conditional correlations cannot be obtained by blindly multiplying marginal correlations.

The original ChaCha quarterround contains internal rotations, so simply citing a generic state theorem would not establish a small state bound. Section 3 resolves that issue explicitly for this target: only a terminal carry pair and nested source intervals are involved. That elementary reconstruction is the substantive reason the direct-application risk is high.

## 5. Eight nearest predecessor families

The entries distinguish full-text inspection from abstract or search-index evidence. Bibliographic dates are as verified in the prior audit or in this bounded search; an unavailable exact day is not invented.

### F1. Niu, Beyne, Hu, Wang — Cryptanalytic Properties of Mealy Machines

**Publication:** CRYPTO 2026, LNCS 16805, pp. 374–405, published 2026-08-11. [Publisher](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13), [ePrint 2026/1193](https://eprint.iacr.org/2026/1193), [author manuscript](https://hukaisdu.github.io/files/papers/2026-1193-mealy-machines.pdf). EPrint received 2026-06-07 and revised 2026-07-27.

**Access and overlap:** complete 53-page author manuscript previously obtained; Sections 5.2 and 7 were re-read here. It covers exact constant-addition and conditional signed correlations via transition matrices.

**Exact difference:** the inspected searchable manuscript does not name this ChaCha fixed-abc coefficient. Nevertheless, the four-state construction above is a direct instance of its theorem. The absence of a named application is insufficient for a new-method claim.

### F2. Miyano — Addend Dependency of Differential/Linear Probability of Addition

**Publication:** IEICE Transactions on Fundamentals E81-A(1), pp. 106–109, 1998-01-25. [Publisher](https://globals.ieice.org/en_transactions/fundamentals/10.1587/e81-a_1_106/_p).

**Access and overlap:** metadata/abstract checked in the earlier audit; full text not obtained. The subject is differential and linear probability of \(X+K\bmod2^w\) as a function of fixed K. F1 explicitly identifies this predecessor.

**Exact difference:** the candidate combines two such carry/comparison operations with fixed XOR and rotation. Addend dependence itself, or different answers for different fixed keys, cannot count as an original observation. An exact prior formula for the composed function has not been checked.

### F3. Beierle–Leander–Todo, and the extended author group — Improved Differential-Linear Attacks with Applications to ARX Ciphers

**Publication versions:** [CRYPTO 2020 chapter](https://link.springer.com/chapter/10.1007/978-3-030-56877-1_12), LNCS 12172, pp. 329–358, first online 2020-08-10; [ePrint 2020/775](https://eprint.iacr.org/2020/775), received 2020-06-24 and marked a major revision of the CRYPTO publication. The expanded [Journal of Cryptology 35, article 29](https://link.springer.com/article/10.1007/s00145-022-09437-z), published 2022-10-12, has eight authors: Beierle, Broll, Canale, David, Flórez-Gutiérrez, Leander, Naya-Plasencia and Todo.

**Access and overlap:** publisher metadata and abstracts verified; the ePrint PDF returned 403. A newly located institutional HAL preview showed an access challenge, so the full text was not obtained. F1 Section 7 independently documents the partitioning work on consecutive additions and its conditional-correlation estimates.

**Exact difference:** these papers develop differential-linear attacks on Chaskey and ChaCha; the current target is a single pure linear local coefficient. This is relevant prior art for conditioning and key-dependent analysis, not proof of identical masks. F1's corrections to some conditional estimates must not be generalized into a claim that this project corrects a specific ChaCha attack.

### F4. Flórez-Gutiérrez–Todo — Improved Cryptanalysis of ChaCha: Beating PNBs with Bit Puncturing

**Publication:** [EUROCRYPT 2025 chapter](https://link.springer.com/chapter/10.1007/978-3-031-91107-1_15), LNCS 15601, pp. 427–457, first online 2025-04-27. [EPrint 2025/437](https://eprint.iacr.org/2025/437), received 2025-03-07, approved 2025-03-08.

**Version caution:** the current ePrint metadata explicitly identifies it as **a major revision of the EUROCRYPT 2025 publication**. The ePrint and version of record must not be treated as word-for-word identical. The visible history does not establish which substantive revision contains a particular indexed passage.

**Access and overlap:** publisher/ePrint metadata and abstract were obtained; the current PDF returned 403. A search-index excerpt of that primary PDF includes a discussion headed “On the Variance of the Right-Key Distribution”: the correlation depends on the key, while the theoretical calculation averages over punctured key bits. Its discussion of excess variance is relevant to the distinction motivating this model.

**Exact difference:** the indexed passage concerns a multi-round key-recovery statistic and modular absorption of key material, not a verified match to the present fixed-abc, one-random-word quarterround coefficient. It establishes a serious prior-art lead for the motivation; its full context and exact normalization remain unchecked. The present local evaluator does not resolve that paper's variance problem.

### F5. Coutinho–Souza Neto — Improved Linear Approximations to ARX Ciphers and Attacks Against ChaCha

**Publication:** EUROCRYPT 2021, LNCS 12696, pp. 711–740. [DOI](https://doi.org/10.1007/978-3-030-77870-5_25), [ePrint 2021/224](https://eprint.iacr.org/2021/224), revised 2021-09-22. The publication text is available in the official [CEPESC collection](https://www.gov.br/abin/pt-br/assuntos/tecnologia/CEPESC_coletanea.pdf), PDF pp. 34–63.

**Access and overlap:** full publication inspected previously; Section 3 was re-read here. It builds quarterround approximations from carry masks and adjacent-bit cancellation. The paper already acknowledges dependence-related discrepancies.

**Exact difference:** the inspected rules do not state an exact all-constants fixed-abc evaluator with only d uniform. This restricted observation is not a proof that no equivalent theorem or immediate corollary exists elsewhere in the paper or its successors. The candidate must not be described as discovering the general failure of carry independence.

### F6. Coutinho et al. — Latin Dances Reloaded: Improved Cryptanalysis Against Salsa and ChaCha, and the Proposal of Forró

**Publication versions:** ASIACRYPT 2022, pp. 256–286, [DOI](https://doi.org/10.1007/978-3-031-22963-3_9); expanded [Journal of Cryptology 36, article 18](https://link.springer.com/article/10.1007/s00145-023-09455-5), published 2023-05-01.

**Access and overlap:** complete conference paper previously obtained through a [public copy](https://jackgiffin.com/main/pdfs/Coutinho-Latin-Dances-Reloaded-2022.pdf); journal main body unavailable. The conference paper's state layout, half-round conventions and quarterround rules were inspected. Its attack discussion distinguishes a guessed fixed key from public nonce/counter values.

**Exact difference:** the general-rotation half-round rules are close at the level of local algebra but do not certify the exact fixed-abc signed expectation above. Having a more explicit conditional distribution does not itself improve any of the paper's attack complexities.

### F7. Okada–Nagai–Miyaji — Refined Linear Approximations for ARX Ciphers and Their Application to ChaCha

**Publication:** INDOCRYPT 2025, LNCS 16372, pp. 70–91, first online 2025-12-11. [Publisher](https://link.springer.com/chapter/10.1007/978-3-032-13301-4_4); [ePrint 2025/2128](https://eprint.iacr.org/2025/2128), received 2025-11-21 and withdrawn 2025-11-23 in favor of the published version.

**Access and overlap:** abstract/references only; the full chapter remains unavailable and no failed retrieval was retried. Its stated exact treatment of consecutive additions and ChaCha approximation errors makes it a required comparison.

**Exact difference:** the abstract's three-independent-variable setting differs from fixed-abc with one uniform word. That is not a sufficient novelty distinction: the theorem's actual conditioning/generalization may contain the candidate as a specialization. This remains the most important ChaCha-specific theorem-level gap. Withdrawal of the ePrint is not treated as a mathematical retraction.

### F8. Bellini–Grados–Makarim–Sanna — Finding differential trails on ChaCha by means of state functions

**Publication:** International Journal of Applied Cryptography 4(3/4), pp. 156–175; canonical [publisher DOI 10.1504/IJACT.2024.138416](https://www.inderscience.com/info/inarticle.php?artid=138416), online 2024-05-03. [Institutional record](https://iris.polito.it/handle/11583/2987931); [author-posted full text](https://www.researchgate.net/publication/380109947_Finding_differential_trails_on_ChaCha_by_means_of_state_functions).

**Access and overlap:** author-posted publication text inspected in the earlier audit. It applies state functions and invertible variable changes to half-quarter differential probabilities.

**Exact difference:** XDP/ADP is a different property from the current signed linear coefficient. It does not by itself establish the exact target. It does rule out treating a routine ChaCha variable change followed by small-state exact evaluation as a newly invented general strategy. The author-cover DOI discrepancy is preserved in the earlier root audit; the canonical publisher DOI is used here.

## 6. Direct-application and publication-risk matrix

| Proposed claim | Evidence against novelty or current limitation | Safe description |
|---|---|---|
| Fixing key words changes a linear bias | F2 and F1 already study fixed-addend/conditional effects; F4 explicitly discusses key dependence | Model distinction or reproduction. |
| Exact values avoid exhaustive enumeration over d | Section 3 is a direct four-state calculation under F1 | Existing-method exact evaluation. |
| Internal rotations require a new exponential-to-polynomial breakthrough | Their supports are nested for this mask, with at most one independent prefix | Elementary scheduling within the old method. |
| This is the fixed-key behavior of ChaCha20 | Only one quarterround's first word and one free d word are modeled | Local conditional correlation for a specified initial-column fragment. |
| Some constants yield correlation +1 or -1 | Single addend circuits can have deterministic bits; no multi-round observable follows | A local special case requiring explanation, not a cipher weakness. |
| The result corrects an existing paper | No same-mask, same-distribution equation has been matched | No correction claim until equation-level comparison is complete. |
| The r-independence of the magnitude is a new invariant | It follows immediately from the bijection and the chosen input mask | Change-of-variables check within this model. |

A low-cost exact baseline can support further research. For a stronger next target, require one of the following concrete connections before expanding:

1. Identify an actual published attack whose probability or right-key distribution uses this same conditional coefficient, then prove a material correction in that same model.
2. Establish a structural theorem about the full distribution over fixed keys, with a quantified consequence for an observable reduced-round distinguisher and a rigorous predecessor comparison.
3. Extend to a coupled stage where the two nested-interval property fails, state the true prior state width, and prove an actual same-target complexity improvement.

These are selection gates, not claims that any one of them is feasible or new. In particular F4 already raises a right-key variance issue, so a future variance study must compare its exact statistic rather than presenting the general motivation as novel.

## 7. Search/access ledger for this bounded cycle

All searches and inspections were on 2026-10-11. The earlier retrieval manifest continues to describe previously cached papers; no new third-party PDF was saved and no earlier file was changed.

| Action | Result and evidence limit |
|---|---|
| Re-read cached Mealy manuscript, Sections 5.2 and 7 | Full text available; conditional normalization and bitwise restriction treatment confirmed. |
| Initial system1 queries on ChaCha/fixed-key/conditional correlation | Mostly unrelated broad results. They provide no negative evidence about prior art and were not used as sources. |
| Focused system2 queries with IACR/Springer domain restrictions | Located the primary-PDF indexed key-dependent-correlation passage in ePrint 2025/437 and the 2020/775 predecessor. Also returned unrelated items, which were discarded. |
| Open ePrint 2025/437 and 2020/775 metadata | Both succeeded. Publication/version annotations recorded above. |
| Open each newly identified PDF once | Both returned HTTP 403. No retry, alternate proxy or circumvention was attempted. |
| System1 exact-title metadata verification | Confirmed the EUROCRYPT 2025 chapter, the CRYPTO 2020 chapter and the Journal of Cryptology 2022 record. |
| Open newly located HAL preview for the 2022 journal paper | Access challenge page rather than the PDF. Recorded as unavailable, not as full-text inspection. |
| Re-read cached 2021 and 2022 conference sections | Full text available for the cited local carry/quarterround material. |
| Open official RFC 8439 | Quarterround and state layout verified; the RFC is informational, not mislabeled as a NIST standard. |

Exact new PDF endpoints whose access was unsuccessful:

- [ePrint 2025/437 PDF](https://eprint.iacr.org/2025/437.pdf): HTTP 403; the key-dependence paragraph was visible only in a primary-PDF search-index excerpt.
- [ePrint 2020/775 PDF](https://eprint.iacr.org/2020/775.pdf): HTTP 403.
- [HAL journal-paper preview](https://inria.hal.science/hal-03947756/preview/Advanced_Differential_Linear_Attacks__joc_.pdf): an access-challenge page, not the paper.

The primary metadata and publication URLs in Section 5 are the durable bibliography. A search excerpt is not substituted for full-text access.

## 8. Unresolved checks and stopping decision

The missing F4 PDF, F7 chapter and extended journal texts prevent a complete mask-by-mask novelty clearance. The Li ICISC/ISPEC 2025 papers and Japanese Okada/Nagai/Miyaji reports already flagged in the earlier review also remain unresolved; no claim of exhaustive latest coverage is made.

This review stops at a preselection judgment and a direct theoretical baseline. It does not grant originality because an exact formula was not found by search. It also does not declare the complete candidate historically published merely because generic theory can compute it. The narrower supported conclusion is that **the proposed ordinary evaluator, fixed-constant sensitivity and basic conditioning have very high direct-application risk and do not justify a new-attack claim**.

Proceed, if useful, with the small verification cycle needed to make the model distinction concrete. Archive the resulting exact numbers and implementation as a reproducible baseline unless a further same-model, independently reviewed contribution survives the predecessor checks above.

Provenance: the frozen METHOD_COMPARISON.md at handoff had SHA-256 baeb6af56157524af6d8fa4fa33f43b45b1817407cb625e27584183ecc1af685. The cached Mealy author manuscript used here has SHA-256 e754420549521a2e39ce898f1e66d303fa50b894c39efa3a603f2b83b3f3f3fb. No Git action, external author contact, publication or submission was performed by this reviewer.
