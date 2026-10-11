# Method comparison: reconstructing the candidate through existing carry-matrix theory

Audit date: 2026-10-11. Author: the independent literature-review agent, with mathematical specifications supplied by the root agent. This is a new, bounded audit supplement; it does not rewrite the frozen NOVELTY_REVIEW.md. No publication, Git mutation, implementation change, or external communication was performed by this reviewer.

## 1. Decision and exact scope

**No new cryptanalytic method, best-known attack complexity, or publication-level originality is established.** The special-bit moments and the overlapping-bit closed expression admit short, explicit derivations using ordinary finite-state linear-correlation matrices. Fixed-word and arbitrary-bit moments are also direct instances of that framework. A same-target matrix-product construction given below removes the apparent quadratic arithmetic cost of separately recomputing the moment mixture.

This conclusion is stronger than saying that a general framework could eventually calculate these values. Sections 3–4 reconstruct the actual moments and coefficients using a few matrix identities. It is weaker than claiming historical publication of precisely the same formula: the closest ChaCha-specific full text is still unavailable, and the identity which removes the rotated middle addition is a separate model-specific step.

All statements concern the function

~~~
s = a+b
t = R_r(d XOR s)
u = c+t
v = R_q(b XOR u)
w = s+v
L = a XOR b XOR R_q(b XOR c) XOR R_(r+q)(a XOR b XOR d).
~~~

Additions are modulo \(2^n\); rotations are left rotations. The correlation is
\(E[(-1)^{w_i\oplus L_i}]\), not half that quantity, an XOR-differential probability, or a differential-linear correlation.

**Quarterround equivalence:** the remaining ChaCha quarterround operations update only the other three words. Thus \(w\) is exactly the first output word of the complete quarterround. A predecessor analyzing that output uses the same function, even if it does not describe a three-addition prefix. Uniform independent words and a fixed first word are different distributions. None of these results constitutes a full ChaCha20 analysis or a fixed-secret-key attack.

## 2. Established tools and remaining literature gaps

The following are the specific prior tools used in this reconstruction. Full bibliographic comparisons and retrieval failures are already in the frozen novelty review and search log.

| Source | What is used here | Limitation of the comparison |
|---|---|---|
| Niu, Beyne, Hu, Wang, **Cryptanalytic Properties of Mealy Machines**, CRYPTO 2026; [author manuscript](https://hukaisdu.github.io/files/papers/2026-1193-mealy-machines.pdf), [publisher](https://link.springer.com/chapter/10.1007/978-3-032-35412-9_13), [ePrint 2026/1193](https://eprint.iacr.org/2026/1193) | Theorem 2 and Algorithm 1 give a product of signed state-transition matrices. Sections 4.4–4.6 explain boundary vectors, constant alphabet sizes, and changes of basis. Section 5.2 treats a constant addend. | These results do not alone show that arbitrary internal rotations have constant state width. The reviewer constructs the matrices below from their truth tables; the paper is not asserted to print this ChaCha coefficient. |
| Sarkar, **On Approximating Addition by Exclusive OR**, [ePrint 2009/047](https://eprint.iacr.org/2009/047) | The relation between multi-input addition and XOR, including finite-position formulas and carry-state analysis, predates this project. | The readily identified unmasked three-input coefficient is old territory. This source is not asserted to supply the exact two lower masks used here. The ePrint record does not establish a named formal venue. |
| Alquié, **Approximating Addition by XOR: how to go all the way**, [ePrint 2010/072](https://eprint.iacr.org/2010/072), [full text](https://eprint.iacr.org/2010/072.pdf) | Carry-matrix diagonalization and finite sums of powers already provide closed expressions for addition/XOR correlations. Theorems 4–5 are relevant to the spectral interpretation. | Its complexity parameter for the number of addends must not be confused with this project's word length. A three-exponential expression is not a new general method. |
| Mouha, Velichkov, De Cannière, Preneel, **The Differential Analysis of S-Functions**, SAC 2010, proceedings 2011; [author manuscript](https://mouha.be/wp-content/uploads/sfunction.pdf) | The small-state construction and exact treatment of joint operations are earlier foundations. | The differential formulas are not interchangeable with the present signed linear coefficient. Mealy Theorem 2 is the direct signed-linear reference. |
| Okada, Nagai, Miyaji, **Refined Linear Approximations for ARX Ciphers and Their Application to ChaCha**, INDOCRYPT 2025; [publisher](https://link.springer.com/chapter/10.1007/978-3-032-13301-4_4), [withdrawn ePrint record](https://eprint.iacr.org/2025/2128) | Its stated treatment of consecutive additions and ChaCha makes it the strongest unresolved specific predecessor. | **Full text remains unavailable.** Withdrawal of the preprint in favor of the version of record is not a retraction of its mathematics. No theorem-level absence or distinction can yet be certified. |

Mealy's discussion also points back to Wallén's modular-addition linear-correlation work and the non-stochastic matrix interpretation in Nyberg–Wallén, FSE 2006, Appendix A. Their full text was not successfully retrieved during the earlier audit; they should not be described as independently read here. The 2026 Li/ICISC and Mixderive/ISPEC full-text gaps also remain. No failed download was repeated in this subcycle.

## 3. Actual reconstruction of the special-bit moments

### 3.1 Mapping to an ordinary sum of three words

After the project's bijection and removal of the middle addition, write the independent words as \(S,B,Y\). Set \(x=S-B\). Then \(x,B,Y\) are independent and uniform; \(S=x+B\). Let \(c_t\) be the carry into bit \(t\) of \(x+B\), and let \(d_t\) be the carry into bit \(t\) of \((x+B)+Y\).

At the special bit \(i=r+q<n\), the needed moments are exactly

\[
M_0=E[(-1)^{c_i+d_i}],\qquad
M_{\ell,p}=E[(-1)^{c_i+d_i+B_\ell+Y_p}],\quad 0\le\ell<p<i.
\]

Thus \(M_{\ell,p}\) is the linear coefficient of ordinary three-input modular addition with input masks

\[
x:e_i,\quad B:e_i+e_\ell,\quad Y:e_i+e_p,
\quad\hbox{output mask }e_i.
\]

The identity \(c_i\oplus d_i=x_i\oplus B_i\oplus Y_i\oplus((x+B)+Y)_i\) proves this mapping. No independence between carries is used.

### 3.2 Four explicit matrices and their truth-table origin

Order the two-carry states as \(00,01,10,11\), with the first carry first. Matrices have **new state as row and old state as column**. For input bits \(x,b,y\), the update is

\[
z=x\oplus b\oplus c,\qquad
c'=\lfloor(x+b+c)/2\rfloor,\qquad
d'=\lfloor(z+y+d)/2\rfloor.
\]

Average the eight triples, optionally weighting by \((-1)^b\) or \((-1)^y\). This gives

\[
P=\frac18
\begin{pmatrix}
4&1&1&0\\2&5&1&2\\2&1&5&2\\0&1&1&4
\end{pmatrix},\quad
P_B=\frac18
\begin{pmatrix}
2&1&1&0\\0&1&1&2\\-2&-1&-1&0\\0&-1&-1&-2
\end{pmatrix},
\]

\[
P_Y=\frac18
\begin{pmatrix}
2&1&1&0\\-2&-1&-1&0\\0&1&1&2\\0&-1&-1&-2
\end{pmatrix}.
\]

The initial column is \(e=(1,0,0,0)^T\). The terminal row for the parity of the two carries is \(f=(1,-1,-1,1)\). These are a concrete application of Mealy Theorem 2; the Appendix regenerates their entries without using either the root implementation or the verification agent's implementation.

Define rows

\[
\mathbf1=(1,1,1,1),\quad v=(1,-1/2,-1/2,1),\quad
h=(1,0,0,-1),\quad z=(0,1,-1,0).
\]

Direct multiplication gives

\[
\mathbf1P=\mathbf1,\quad vP=v/4,\quad hP=h/2,\quad zP=z/2,
\qquad f=-\mathbf1/3+4v/3,
\]

\[
\mathbf1P_B=\mathbf1P_Y=0,\quad
vP_B=vP_Y=3h/8,\quad hP_B=\mathbf1/4.
\]

The four eigenvectors are independent, with row-basis determinant \(6\). The spectrum of \(P\) is \(1,1/2,1/2,1/4\).

### 3.3 The whole special-bit computation

The unmasked coefficient is immediately

\[
M_0=fP^i e=-\frac13+\frac4{3\,4^i}.
\]

The two-mask coefficient is

\[
\begin{aligned}
M_{\ell,p}
&=fP^{i-p-1}P_Y P^{p-\ell-1}P_B P^\ell e\\
&=\frac12\,4^{-(i-p-1)}
        2^{-(p-\ell-1)}\frac14
 =2^{\ell+p-2i}.
\end{aligned}
\]

There is no unknown carry-dependence lemma left in these moments. Substitution in the already derived rotation identity

\[
C=2^{-r}M_0-\sum_{\ell=0}^{r-1}2^{\ell-r}M_{\ell,\ell+q}
\]

and the geometric sum \(\sum_{\ell<r}8^\ell=(8^r-1)/7\) yields the project's stated special-bit formula.

**Novelty implication:** the moment evaluations are elementary corollaries of an established exact framework. Their reconstruction is not evidence that the same formula was previously printed, but it rules out treating the moment formula or the signed four-state machinery as a new foundational cryptanalytic technique. The separate question is whether the rotated-quarterround coefficient, and a useful consequence of it, were already treated.

## 4. The upper-bit formula is also explicitly reconstructed

This section addresses \(i=r+q+k<n\), \(r,q\ge1\), \(0\le k\le q\). It uses the candidate formula and then compares the reconstruction with the written discovery proof; it is not a blind discovery or a human peer review.

The extra earlier carry is represented by

\[
D=\operatorname{diag}(1,1,-1,-1).
\]

The rows above satisfy

\[
\mathbf1D=h+z,\qquad vD=h-z/2,\qquad hD=\mathbf1/3+2v/3.
\]

Hence

\[
M_0=fP^{i-k}DP^k e
=2^{-k}\left(-\frac13+\frac4{3\,4^{i-k}}\right).
\]

Let \(p=\ell+q\). Since \(k\le q\), one always has \(p\ge k\).

* For \(\ell\ge k\), insert \(D\) below the \(B\)-mask. The product is
  \(fP^{i-p-1}P_Y P^{p-\ell-1}P_B P^{\ell-k}DP^k e\).
  The identities of Section 3 give \(2^{\ell+p-2i-k}\).
* For \(\ell<k\le p\), the product is
  \(fP^{i-p-1}P_Y P^{p-k}DP^{k-\ell-1}P_B P^\ell e\).
  Here \(hD=\mathbf1/3+2v/3\), and the \(\mathbf1P_B\) term vanishes. The result is \(2^{1+\ell+p-2i-k}\).

Both boundary cases \(p=k\) and \(\ell=k\) have nonnegative exponents in the applicable product and are included. Thus

\[
M_{\ell,\ell+q}
=2^{2\ell+q-2i-k}
\begin{cases}2,&\ell<k,\\1,&\ell\ge k.\end{cases}
\]

Writing \(j=r+k\), the remaining sum is

\[
\sum_{\ell=0}^{j-1}8^\ell(1+\mathbf1_{\ell<k})
=\frac{8^j+8^k-2}{7}.
\]

It follows algebraically that

\[
C_k=\alpha4^{-k}+\beta2^{-k}+\delta16^{-k},
\]

\[
\alpha=-\frac1{3\,2^r}+\frac4{3\,2^{3r+2q}},\quad
\beta=-\frac1{7\,2^q}-\frac1{7\,2^{3r+q}},\quad
\delta=\frac2{7\,2^{3r+q}}.
\]

The characteristic polynomial then gives

\[
128C_{k+3}-104C_{k+2}+22C_{k+1}-C_k=0
\]

only when all four offsets satisfy \(0\le k\le q\) and \(r+q+k<n\). This is a derivation from actual matrix products; it is not an inference from three fitted values or from a suggestive list of eigenvalues.

The precise coefficient family still needs predecessor comparison. However, its exponentials and recurrence do not constitute an independent new finite-state technique. The short matrix derivation is material evidence that the claimed qualitative novelty should be judged as a possible application-specific corollary, not as a new general ARX theorem. A closed expression can still be useful; usefulness and historical originality require further evidence.

## 5. Fixed first word: an actual same-target matrix baseline

### 5.1 The constant changes the local kernel, not the method

For \(x=A\) fixed, average only the four input pairs \(b,y\). The unmasked transition is \(P_{A_t}\), with

\[
P_0=\frac14
\begin{pmatrix}
3&1&1&0\\1&3&1&2\\0&0&2&1\\0&0&0&1
\end{pmatrix},\qquad
P_1=\frac14
\begin{pmatrix}
1&0&0&0\\1&2&0&0\\2&1&3&1\\0&1&1&3
\end{pmatrix}.
\]

Their average is \(P\). The weighted kernels \(P^B_a,P^Y_a,P^{BY}_a\) are obtained from the identical four-pair truth table, with the appropriate sign. Crucially,

\[
\det P_0=\det P_1=\det P=1/16.
\]

The matrices are invertible over the rationals. This statement concerns unmasked kernels; it would be false to assume the masked kernels invertible.

Computing one constant-word moment using the product takes \(O(i)\) constant-size matrix-vector operations. This is an explicit instance of the older finite-state theory, after the project's rotation elimination. A correlation of a single constant addition and the entire candidate coefficient are different targets: their complexities cannot be compared without this reduction.

### 5.2 Prefix products compute the complete mixture in linear arithmetic cost

Let \(G_t=P_{A_{t-1}}\cdots P_{A_0}\), with \(G_0=I\). Define

\[
H_t^B=G_{t+1}^{-1}P^B_{A_t}G_t,\qquad
H_t^Y=G_{t+1}^{-1}P^Y_{A_t}G_t.
\]

For \(h<p\), cancellation of adjacent inverse prefixes gives exactly

\[
M^A_{h,p}=fG_i H_p^Y H_h^B e.
\]

No probabilistic assumption is involved. Therefore the same target

\[
C_A=2^{-r}\left(fG_i e-\sum_{h=0}^{r-1}2^h fG_iH_{h+q}^YH_h^B e\right)
\]

does not require \(r\) independent length-\(i\) products.

First form \(G_i\) and the prefix \(G_q\), in \(O(i)\) operations. During the sum, maintain two prefix/inverse-prefix pairs at positions \(h\) and \(p=h+q\). Each update uses the next constant \(P_{A_t}\) and its constant inverse:

\[
G_{t+1}=P_{A_t}G_t,\qquad
G_{t+1}^{-1}=G_t^{-1}P_{A_t}^{-1}.
\]

Each summand requires a constant number of \(4\times4\) products. Thus this direct application of the established kernel method plus elementary prefix-product algebra takes **\(O(i+r)\), hence \(O(n)\), exact arithmetic operations** for the same coefficient. It needs only a constant number of matrices, not a table of all prefixes.

This construction is a reviewer-derived baseline, not a claim that a prior publication already described precisely this optimization for this mask family. Its purpose is to make the complexity comparison fair. It depends on the same rotation-elimination identity as the project's closed form.

### 5.3 What the \(O(r)\) closed form can and cannot claim

At a family of standard-shaped parameters with \(r=\Theta(n)\), the closed expression's \(O(r)\) arithmetic cost and this \(O(n)\) baseline have the same asymptotic order. Comparing either one only with \(2^{3n}\) or \(2^{4n}\) enumeration does not establish an original complexity improvement.

If \(r\) is much smaller than \(q\), the operation counts \(O(r)\) and \(O(r+q)\) can differ in a word-arithmetic model. That conditional comparison would need an explicit parameter family and a best-known baseline; it does not follow from the single standard triple \((32,16,12)\). Neither algorithm has been timed against an optimized predecessor implementation in this audit.

The fixed-\(A\) triangular-sum expression and the classification of its sign for every \(A\) are additional mathematical statements. Generic matrix computability does not prove that their closed expressions or inequalities already appeared in the literature. They remain application-level candidates requiring separate historical checking, especially against the missing ChaCha-specific paper. No original L2 credit is assigned by this audit.

## 6. Arbitrary bits: four-state reduction and a linear-product refinement

### 6.1 Ordinary finite-state evaluation, including the intermediate carry mask

For arbitrary \(i\), set \(j=(i-q)\bmod n\), \(k=(i-r-q)\bmod n\). The root's proved decomposition is

\[
C_i=2^{-j}
\left(M_0-\sum_{\substack{0\le\ell<i\\h=(\ell-q)\bmod n<j}}2^hM_{h,\ell}\right).
\]

The moment sign is \(c_i\oplus c_k\oplus d_i\), optionally with \(B_h\oplus Y_\ell\). Under \(S=x+B\), \(c_k=x_k\oplus B_k\oplus S_k\) is an ordinary **intermediate-output mask** of the adjacent-addition network. There is no new state type here. The local state need only retain the two carries.

To place this explicitly inside the existing framework, emit the old carry bits as extra local output coordinates. Weight them by the desired signs. Equivalently use

\[
D_t=\operatorname{diag}_{(c,d)}
(-1)^{\,c\,(\mathbf1_{t=i}+\mathbf1_{t=k})+d\,\mathbf1_{t=i}},
\qquad T_t=P_tD_t,
\]

where \(P_t=P\) for independent uniform words and \(P_t=P_{A_t}\) for fixed \(A\). Repeated carry occurrences cancel because the exponent is modulo two. Phases are applied to the carry **before** processing that bit.

The initial vector is \(e\); the terminal row is \(\mathbf1\), summing all final carries. No final carry is constrained to zero. These boundary choices and coordinate emissions give a literal Mealy Theorem 2 instance.

### 6.2 The at-most-\(n\) terms need not cost \(O(n^2)\) arithmetic

Every \(D_t\) and \(P_t\) is invertible. Set \(G_t=T_{t-1}\cdots T_0\), and for \(X\in\{B,Y,BY\}\) set

\[
Q_t^X=P_t^X D_t,\qquad H_t^X=G_{t+1}^{-1}Q_t^XG_t.
\]

Then

\[
M_0=\mathbf1G_ne,
\]

\[
M_{h,\ell}=
\begin{cases}
\mathbf1G_nH_\ell^YH_h^Be,&h<\ell,\\
\mathbf1G_nH_h^BH_\ell^Ye,&h>\ell,\\
\mathbf1G_nH_h^{BY}e,&h=\ell.
\end{cases}
\]

The equal-position case requires the jointly weighted \(BY\) kernel. Multiplying two single-mask kernels at that position would compute the wrong function.

The eligible indices \(h=(\ell-q)\bmod n\), \(0\le\ell<i\), \(h<j\), form at most two contiguous increasing runs: the wrapped interval \(\ell<q\) and the interval \(\ell\ge q\), each intersected with the stated bounds. Within either run, \(h\) and \(\ell\) advance together. The two-prefix streaming construction of Section 5 applies to each run; initialization needs only a constant number of length-\(n\) scans. If \(q=0\), use the equal-position kernel instead.

Consequently, **given the proved sparse decomposition**, a direct matrix-product construction evaluates one arbitrary-bit coefficient in \(O(n)\) exact arithmetic operations and \(O(n)\) auxiliary bits. Evaluating all \(n\) coefficients independently gives an \(O(n^2)\) arithmetic upper bound. This is a mathematical construction and a comparison against the project's recomputation strategy. It is not an end-to-end benchmark, a replacement implementation, or a new published-best attack.

The proof of sparse rotation elimination remains logically necessary. Applying a generic finite-state theorem directly to a rotated word circuit does not automatically give a width of four; a naive bit order can retain rotated data. Thus the above observation does not by itself make that model-specific elimination historically old.

### 6.3 Cost model and the absence of an attack improvement

All entries are dyadic rationals. The constant matrices and their inverses have bounded-size entries. Products of \(O(n)\) such matrices, and the final weighted sum, have \(O(n)\)-bit numerators and denominators when powers of two are normalized. A constant number of streamed matrices therefore occupies \(O(n)\) bits, apart from the input and output.

The word-arithmetic comparison counts operations on those \(O(n)\)-bit quantities. The prefix method includes multiplications of growing integers; a safe bound is \(O(n\,\mathsf M(n))\) bit operations per coefficient, where \(\mathsf M(n)\) bounds \(n\)-bit multiplication. With schoolbook multiplication this is \(O(n^3)\). The project's original \(O(n^2)\) arithmetic dynamic program mainly uses additions and shifts and also has an \(O(n^3)\) elementary bit-operation upper bound. Therefore a smaller arithmetic count alone does **not** establish a smaller elementary bit-operation bound here.

No method in this comparison collects cipher oracle data. No multi-round linear trail, optimal mask search, success probability for key recovery, or attack time/data/memory triple has been improved.

## 7. Fair comparison and minimum remaining question

| Proposed contribution | Concrete older-method reconstruction or comparison | Current defensible assessment |
|---|---|---|
| Exact signed four-state counting | Direct local truth-table kernels and Mealy Theorem 2 | Established method application; L0 as methodology. |
| \(M_0\) for three uniform addends | Ordinary addition/XOR coefficient; one spectral decomposition | Existing territory, not a new carry theorem. |
| Two lower-input-mask moments | Three short row identities give the exact formula | Explicit elementary framework corollary. Historical printing of the same masks remains unchecked. |
| Special-bit quarterround coefficient | Rotation elimination, followed by those moments and one geometric sum | Possible model-specific corollary; no cleared originality or attack gain. |
| Upper-bit exponential expression and recurrence | The same kernels with one diagonal carry mask give all moments | Possible extension of the same application; not a new spectral technique. |
| Fixed-\(A\), \(O(r)\) computation | The same full coefficient has an \(O(r+q)\) prefix-matrix construction after elimination | Same order at \(r=\Theta(n)\); no measured or published-best complexity improvement. |
| Arbitrary-bit \(O(n^2)\) arithmetic algorithm | Shared invertible prefixes reduce recomputation to \(O(n)\) arithmetic | Project-internal optimization is available; originality of this elementary optimization is not claimed. |
| Fixed-\(A\) sign classification | Constant-kernel evaluation exists, but a uniform inequality is a separate assertion | Not historically cleared; requires comparison of exact statement and use. |

The smallest candidate statement not eliminated by this audit is:

> For the complete quarterround's first output and the all-XOR input mask, the specified input change and averaging operation expand the exact linear coefficient into at most \(n\) ordinary adjacent-addition coefficients, including fixed-first-word inputs and wrapped rotations; this expansion has the stated support and weights.

This is deliberately narrower than proposing a new finite-state method. The weighted average is an ordinary Fourier expansion once the conditioning is chosen. What still requires historical comparison is whether that conditioning, sparse support, and particular quarterround specialization were already given or follow immediately from the closest ChaCha-specific approximation rules. The fixed-word sign statement is another possible narrow application-level proposition.

Before treating either as a publishable contribution, obtain the missing predecessor text and compare the exact masks, output word, constant-word distribution, boundary conditions, and proof. A useful application to a new search bound or a genuinely better attack would materially strengthen the case. Without it, the present package is best presented as a rigorous, reproducible local-correlation study with unresolved originality, not as the first new cryptanalysis paper.

## 8. Provenance, limited verification, and metadata correction

The reviewer derived the kernels by their local truth table, without reading the root's code or the independent verifier's code. Candidate statements, the special-bit proof, GENERAL_REDUCTION.md, and the overlapping-bit proof were available; the matrix derivation is therefore an alternative mathematical reconstruction, not a blind discovery. The root reports that general-reduction experiments and two written proofs have passed. The frozen review's earlier “pending” description remains a timestamped earlier state.

Inputs inspected for this supplement had these SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Author Mealy manuscript | e754420549521a2e39ce898f1e66d303fa50b894c39efa3a603f2b83b3f3f3fb |
| GENERAL_REDUCTION.md | cb70223bbc6c58823d3df0392755433429ca2eb7f036bcee8fc402b889234ddd |
| proofs/special_bit_signed_correlation.md | 184c9f29b147e4035ac155a1e375accbc0fd58cb591fc222bdc84e3fe5281d73 |
| proofs/fixed_first_word.md | e96dbb4e8ef1ece9ec26bc8ff5bda58a1f63d441b6934084a07890bf43b812cb |
| proofs/overlap_bit_closed_form.md | 679893a5d746d0180215031b0b7c0ceed3d926d74f0d5969f5d7928cd8ba0fca |

The first disposable algebra-check command attempted to import SymPy and exited 1 with ModuleNotFoundError. No package was installed. A replacement used only the Python standard library, exited 0, checked all displayed basic eigenvector identities, and checked 84 special masked moments for \(1\le i\le8\). The Appendix supplies the complete reproducible standard-library check and additional boundary/product checks. These tests verify the algebraic reconstruction, not the earlier rotation-elimination derivation or a full cipher attack.

**Bellini state-functions DOI provenance:** the prior DOI 10.1504/IJACT.2024.10063705 came from the author-posted paper cover and metadata at [ResearchGate](https://www.researchgate.net/publication/380109947_Finding_differential_trails_on_ChaCha_by_means_of_state_functions). It was not invented. The [publisher's canonical record](https://www.inderscience.com/info/inarticle.php?artid=138416) gives 10.1504/IJACT.2024.138416, accepted 2023-03-08 and published online 2024-05-03. The root is correcting the main DOI while preserving this version-metadata discrepancy.

## Appendix A. Reproducible local-kernel algebra check

This deterministic check uses no random seeds, third-party packages, downloaded code, or original quarterround enumeration. It regenerates the matrices, verifies the row identities and the moment formulas, and checks conjugated-prefix products against their unreduced matrix products for coincident and reversed mask positions.

Run from the repository root:

~~~sh
python3 - <<'PY'
from pathlib import Path
import hashlib
p = Path("workstreams/CRYPTO/projects/chacha-three-add/literature/METHOD_COMPARISON.md")
code = p.read_text().split("~~~python\n", 1)[1].split("\n~~~", 1)[0]
print("embedded_source_sha256", hashlib.sha256(code.encode()).hexdigest())
exec(compile(code, str(p) + ":appendix", "exec"))
PY
~~~

~~~python
from fractions import Fraction as F
from itertools import product, permutations
import platform
import sys

states = list(product(range(2), repeat=2))

def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]

def scale(c, a):
    return [[c*x for x in row] for row in a]

def plus(a, b):
    return [[x+y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]

def eye(n=4):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def power(a, n):
    out = eye()
    for _ in range(n):
        out = mul(out, a)
    return out

def determinant(a):
    out = F(0)
    for p in permutations(range(len(a))):
        v = F((-1)**sum(p[i] > p[j] for i in range(len(a))
                       for j in range(i+1, len(a))))
        for i, j in enumerate(p):
            v *= a[i][j]
        out += v
    return out

def inverse(a):
    z = [row[:] + e for row, e in zip(a, eye())]
    for j in range(4):
        pivot = next(i for i in range(j, 4) if z[i][j])
        z[j], z[pivot] = z[pivot], z[j]
        v = z[j][j]
        z[j] = [x/v for x in z[j]]
        for i in range(4):
            if i != j:
                v = z[i][j]
                z[i] = [x-v*y for x, y in zip(z[i], z[j])]
    return [row[4:] for row in z]

def kernel(fixed=None, mb=0, my=0):
    a = [[F(0) for _ in states] for _ in states]
    choices = (list(product(range(2), repeat=3)) if fixed is None
               else [(fixed, b, y) for b, y in product(range(2), repeat=2)])
    for old, (c, d) in enumerate(states):
        for x, b, y in choices:
            z = x ^ b ^ c
            new = states.index(((x+b+c)//2, (z+y+d)//2))
            a[new][old] += F((-1)**(mb*b+my*y), len(choices))
    return a

def diagonal_carry(ci=0, di=0):
    return [[F((-1)**(ci*c+di*d)) if u == v else F(0)
             for v in range(4)] for u, (c, d) in enumerate(states)]

P, PB, PY = kernel(), kernel(mb=1), kernel(my=1)
one = [[F(1), F(1), F(1), F(1)]]
v = [[F(1), F(-1, 2), F(-1, 2), F(1)]]
h = [[F(1), F(0), F(0), F(-1)]]
z = [[F(0), F(1), F(-1), F(0)]]
f = [[F(1), F(-1), F(-1), F(1)]]
e = [[F(1)], [F(0)], [F(0)], [F(0)]]
D = diagonal_carry(ci=1)
zero = [[F(0)]*4]
checks = [
    mul(one, P) == one,
    mul(v, P) == scale(F(1, 4), v),
    mul(h, P) == scale(F(1, 2), h),
    mul(z, P) == scale(F(1, 2), z),
    f == plus(scale(F(-1, 3), one), scale(F(4, 3), v)),
    mul(one, PB) == zero, mul(one, PY) == zero,
    mul(v, PB) == scale(F(3, 8), h),
    mul(v, PY) == scale(F(3, 8), h),
    mul(h, PB) == scale(F(1, 4), one),
    mul(one, D) == plus(h, z),
    mul(v, D) == plus(h, scale(F(-1, 2), z)),
    mul(h, D) == plus(scale(F(1, 3), one), scale(F(2, 3), v)),
]
assert all(checks)
assert determinant(one+v+h+z) == 6
assert all(determinant(m) == F(1, 16) for m in [P, kernel(0), kernel(1)])
assert scale(F(1, 2), plus(kernel(0), kernel(1))) == P

def moment(i, k=0, ell=None, p=None):
    state = e
    for t in range(i):
        if t == k:
            state = mul(D, state)
        state = mul(kernel(mb=int(t == ell), my=int(t == p)), state)
    return mul(f, state)[0][0]

unmasked_checks = masked_checks = 0
for i in range(1, 8):
    for k in range(i):
        assert moment(i, k) == F(2)**(-k) * (
            -F(1, 3) + F(4, 3)*F(4)**(-(i-k)))
        unmasked_checks += 1
        for ell in range(i):
            for p in range(max(ell+1, k), i):
                expected = F(2)**(ell+p-2*i-k+int(ell < k))
                assert moment(i, k, ell, p) == expected
                masked_checks += 1

prefix_checks = 0
for fixed_word in [None, 0, 5, 15]:
    n = 4
    for i, k in [(0, 0), (0, 2), (3, 1), (3, 3)]:
        aa = [None]*n if fixed_word is None else [
            (fixed_word >> t) & 1 for t in range(n)]
        dd = [diagonal_carry(ci=int(t == i)+int(t == k), di=int(t == i))
              for t in range(n)]
        tt = [mul(kernel(aa[t]), dd[t]) for t in range(n)]
        gg = [eye()]
        for t in range(n):
            gg.append(mul(tt[t], gg[-1]))
        gi = [inverse(g) for g in gg]
        for a, b in zip(gg, gi):
            assert mul(a, b) == eye()
        hh = {}
        for t in range(n):
            for mb, my in [(1, 0), (0, 1), (1, 1)]:
                q = mul(kernel(aa[t], mb, my), dd[t])
                hh[t, mb, my] = mul(mul(gi[t+1], q), gg[t])
        for hb in range(n):
            for ly in range(n):
                direct = e
                for t in range(n):
                    q = mul(kernel(aa[t], int(t == hb), int(t == ly)), dd[t])
                    direct = mul(q, direct)
                direct_value = mul(one, direct)[0][0]
                if hb < ly:
                    middle = mul(hh[ly, 0, 1], hh[hb, 1, 0])
                elif hb > ly:
                    middle = mul(hh[hb, 1, 0], hh[ly, 0, 1])
                else:
                    middle = hh[hb, 1, 1]
                reduced = mul(mul(mul(one, gg[n]), middle), e)[0][0]
                assert reduced == direct_value
                prefix_checks += 1

print("row_identities", len(checks), "eigenbasis_det", determinant(one+v+h+z))
print("unmasked_moment_checks", unmasked_checks)
print("masked_moment_checks", masked_checks)
print("prefix_product_checks", prefix_checks)
print("kernel_determinants", [str(determinant(kernel(a))) for a in [None, 0, 1]])
print("python", sys.version.split()[0], "platform", platform.platform())
print("PASS: local kernels, analytic moment identities, and prefix algebra")
~~~

### Execution receipt

The complete Appendix check was run once after this file was written. Its actual source hash, exit code and output are recorded below.

Completed on 2026-10-11 in the repository root, with the exact command above. Exit code **0**. The tool recorded 0.229 seconds for the process; this is a small audit check duration, not a cryptanalytic performance benchmark.

~~~
embedded_source_sha256 d7d583fb9a1bea4adbe05a51185544279ff7c071c130aa9eb12cef9c308e286b
row_identities 13 eigenbasis_det 6
unmasked_moment_checks 28
masked_moment_checks 252
prefix_product_checks 256
kernel_determinants ['1/16', '1/16', '1/16']
python 3.12.14 platform Linux-6.18.44-x86_64-with-glibc2.39
PASS: local kernels, analytic moment identities, and prefix algebra
~~~

The limited checks include coincident carry indices, carry phases at bit zero, zero and all-one constant words, distinct mask orderings, and coincident \(B,Y\) masks. No claim is made that these finite checks alone prove the all-parameter formulas; the written matrix identities and cancellation proof above supply that argument.
