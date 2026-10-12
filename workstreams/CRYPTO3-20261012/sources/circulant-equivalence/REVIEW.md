# Circulant RD: quantifiers, equivalent formulations, and bounded source review

Review date: 2026-10-12. This note reviews the accepted written theorem at
main `61488e05c9fe41984f483853f99e79f5715dc893`; it does not replace that proof,
replay the old minor enumeration, or establish historical priority.
Exact input and retrieved-byte hashes are in `SOURCES.json`.

## 1. Scope that survives the review

Let (K) be any field of characteristic two, let (n\ge3), and let

\[
M_{ij}=a_{i-j\bmod n}\quad(0\le i,j<n)
\]

be invertible. The accepted conclusion is the existence of (u,v\in K^n)
such that (u,v,u+v\ne0) and, for every coordinate,

\[
u_i v_i(u_i+v_i)=0,
\qquad (Mu)_i(Mv)_i(Mu+Mv)_i=0.
\]

Invertibility also makes (Mu,Mv,Mu+Mv) nonzero. The theorem includes all
circulant MDS matrices over every finite field (K=\mathbb F_{2^m}), but
does not require MDS or finiteness. Its final statement does not cover
singular matrices, characteristic other than two, or (n=2). The last
boundary is substantive: every (2\times2) MDS matrix lacks such a
nontrivial pair. These are diffusion-component statements; they supply no
cipher attack complexity or probability.

This scope is the one stated by [the frozen main proof][main-proof],
Sections 1–6. Its upstream version-2 source and exact transformation are
recorded by [main provenance][main-provenance]. In particular, v1's
ancillary suggestion of possible MDS loss under a periodic quotient was
corrected before integration.

## 2. The periodic quotient, in matrix, ring, and code language

For **every** positive divisor (d\mid n), write (n=td), and define

\[
b_r=\sum_{k=0}^{t-1}a_{r+kd},\quad
B_{rs}=b_{r-s\bmod d},\quad
(Jx)_i=x_{i\bmod d}.
\]

Then (MJ=JB) and (J) is injective. Hence invertible (M) implies
invertible (B); a nontrivial RD pair for (B) repeats to one for (M).
There is no division by (t). In particular, (t=2) is valid in
characteristic two. This is not an averaging operator.

Here is an equivalent algebraic description, included to fix search
terminology rather than claim a new result. Put

\[
A_n=K[X]/(X^n-1),\quad A_d=K[X]/(X^d-1),\quad
q_d(X)=1+X^d+\cdots+X^{(t-1)d}.
\]

The quotient homomorphism (A_n\to A_d) sends (a(X)) to (b(X)).
An invertible circulant is multiplication by a unit, and a ring
homomorphism sends units to units. The **embedding** (J:A_d\to A_n)
is instead (x(X)\mapsto q_d(X)x(X)). It is well defined because

\[
q_d(X)(X^d-1)=X^n-1,
\]

and is injective because a degree-(<d) polynomial is sent to its (t)
disjoint coefficient copies. These two maps are different: reducing
(Jx) to (A_d) gives (t x), which is zero when (t=2). Confusing
quotient and embedding would invalidate a characteristic-two argument.
Their valid intertwining identity is precisely (MJ=JB).

Define the graph code (C_M=\{(x,Mx):x\in K^n\}\), with column encoder
(\binom I M). Its minimum word weight is the branch number
(\beta(M)=\min_{x\ne0}(\operatorname{wt}(x)+\operatorname{wt}(Mx))).
This graph-code interpretation is already explicit in
[Daemen–Rijmen, Section 2.4][dr09]. The periodic subcode is

\[
\{(Jx,JBx):x\in K^d\}\subseteq C_M.
\]

Every word in it has exactly (t) times the weight of ((x,Bx)). Thus

\[
\beta(M)\le t\beta(B),\qquad
\beta(B)\ge\left\lceil\frac{\beta(M)}t\right\rceil.
\]

If (M) is MDS, then (\beta(M)=td+1), while always
(\beta(B)\le d+1). Therefore (\beta(B)=d+1): the quotient **is MDS**.
The bound is a lower bound on the quotient's branch number, not an
equality assertion for arbitrary (M).

The previously uncovered orders (n\equiv\pm2\pmod{12}), (n>2), use
(d=n/2), an odd integer at least 5. The previously known odd circulant
case applies to the quotient. The use of this elementary periodic
subspace is the completion identified by main; the underlying ring,
invariant-subspace, and weight facts are not new algebraic principles.

## 3. Exact three-word separation formulation

Call a code **3-separating** here if every three distinct codewords have
some coordinate containing three pairwise distinct symbols. For the
linear graph code (C_M),

\[
\text{(M) admits a nontrivial RD pair}
\quad\Longleftrightarrow\quad
\text{(C_M) is not 3-separating}.
\]

Indeed, translate any three distinct graph codewords by the first one.
The resulting triple is (0,(u,Mu),(v,Mv)), where (u,v,u+v\ne0).
At one coordinate, the three symbols fail to be distinct exactly when
the other two symbols are equal or at least one is zero. These are
exactly the RD coordinate conditions above. Translation preserves
equality and inequality of symbols. This proves both directions and
also makes the nontriviality requirement explicit.

For finite (K=\mathbb F_q), this is equivalently failure of the family
of (2n) linear coordinate functionals

\[
x\mapsto x_i,\qquad x\mapsto(Mx)_i\quad(0\le i<n)
\]

to be a linear ((q^n,q,3))-perfect hash family: one functional must be
injective on each three-element input set. That family terminology is
standard in [Barwick–Jackson, ePrint 2005/465][bj05]. When (M) is
circulant, a row generator is ([I\mid M^T]), so this is the associated
double-circulant graph code. The equivalence here is a direct
reformulation, not an additional existence theorem or a priority claim.
No result on minimal perfect hashing of one fixed dictionary is relevant
to this three-element separation condition.

## 4. Primary-source attribution and scope comparison

| Source inspected | Precisely relevant content | Effect on the accepted theorem |
|---|---|---|
| Daemen–Rijmen, *New criteria for linear maps in AES-like ciphers*, 2009, §§2.4, 7–8, 9.1 ([author PDF][dr09]) | Graph code/branch number, RD definition, and the (4\times4) circulant construction; MDS inputs make that construction nontrivial. | These ingredients are prior work. No all-order quotient application was identified in the inspected sections. |
| Barreto–Nikov–Nikova–Rijmen–Tischhauser, *Whirlwind*, 2010, §4.2, Theorem 1 ([publisher PDF][whirlwind]) | Explicit even/odd coefficient construction for circulant order (4q). | The (4\mid n) ingredient predates KYS. The inspected proof does not state the all-divisor quotient/branch-number proposition. |
| Kumar–Yadav–Samanta, arXiv:2605.27535v1, 2026-05-26, Theorems 2, 4, 5 and §VI ([versioned text][kys]) | Non-MDS reduction, odd symmetric case, circulant coverage (n\not\equiv\pm2\pmod{12}), and an unnumbered remaining-order question. | This is the exact source boundary. Its unrestricted wording for singular matrices is not imported into main's nontrivial invertible theorem. |
| Jha–Li–Gligoroski, IACR CiC 2(1), 2025, §1 and Theorem 3 ([paper][jha]) | (4\times4) Hadamard RD avoidance via 28 parameter conditions; §1 restricts its familiar circulant observation to (4\times4). | A different matrix family/condition, not an all-order circulant completion. |
| The Jha paper's [author repository][jha-code], HEAD `abdc445c55baba482e3b9d0927e81983a1853adc` | README describes the (4\times4) Hadamard constructor, MDS/RD tests and implementation-cost tools. | Read-only scope inspection; no code execution or all-minor rerun. |
| Otal–Sülçe–Yayla, ePrint 2025/2240 ([official metadata][osy]) | Current abstract concerns (2\times2), (3\times3) circulant, (3\times3) involutory and (3\times3) parameter conditions. | Official history lists a **2026-06-11 revision**, later than KYS v1. The PDF/history archive returned 403; the revised proof and whether earlier criticism was addressed remain unreviewed. |
| Barwick–Jackson, ePrint 2005/465 ([official metadata][bj05]) | Linear perfect-hash-family definition and sequence constructions. | Establishes the relevant equivalent vocabulary; no double-circulant obstruction theorem was identified. PDF returned 403, so this is an abstract-level comparison. |

The search also reached the publisher abstract of
[Mousavi–Esmaeili–Gulliver][meg], which constructs particular circulant,
circulant-like and orthogonal MDS generalized Cauchy matrices. Its
divisibility condition concerns constructing matrices of order dividing
(2^k-1); it is not a statement of branch-number inheritance when
quotienting an arbitrary circulant. Full-text equivalence was not
asserted from that abstract. The author PDF for
[Cauchois–Loidreau's involutory circulant study][cl] returned 403 and
remains an unreviewed lead. Conditions such as (M^2=I) or (MM^T=I)
add hypotheses absent from main and therefore cannot be silently used as
equivalent formulations of its quantified claim.

## 5. Bounded conclusion and remaining gate

The quantifiers, quotient invertibility, and branch-number/MDS
inheritance are consistent. The ring and three-word separation
formulations give exact alternative descriptions useful for further
literature comparison. Searches of the RD, periodic quotient,
double-circulant separation and linear perfect-hash terminology did not
identify a same-scope published completion in the inspected primary
sources. This is a bounded search outcome, **not evidence of first
discovery**. No claim of new formalization, human peer review, or cipher
attack is added.

The actionable literature gap is precise: obtain the revised
Otal–Sülçe–Yayla full text before repeating claims about deficiencies in
its earlier (3\times3) characterization, and inspect any primary result
explicitly relating periodic graph subcodes to RD/three-word separation.
No further circulant computation is justified by this review alone.

[main-proof]: https://github.com/mio-qwq/math/blob/61488e05c9fe41984f483853f99e79f5715dc893/workstreams/ROOT/cryptographic-structures/circulant/PROOF.md
[main-provenance]: https://github.com/mio-qwq/math/blob/61488e05c9fe41984f483853f99e79f5715dc893/workstreams/ROOT/cryptographic-structures/provenance.json
[dr09]: https://cs.ru.nl/~joan/papers/JDA_VRI_LinearMaps_2007.pdf
[whirlwind]: https://link.springer.com/content/pdf/10.1007/s10623-010-9391-y.pdf
[kys]: https://arxiv.org/html/2605.27535v1
[jha]: https://cic.iacr.org/p/2/1/37/pdf
[jha-code]: https://github.com/sjsonucool/hadamard-matrices-resistant-to-related-differentials-cryptanalysis/tree/abdc445c55baba482e3b9d0927e81983a1853adc
[osy]: https://eprint.iacr.org/2025/2240
[bj05]: https://eprint.iacr.org/2005/465
[meg]: https://www.aimsciences.org/article/doi/10.3934/amc.2024020
[cl]: https://perso.univ-rennes1.fr/pierre.loidreau/articles/dcc/MDS_WCC.pdf
