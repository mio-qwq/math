# Direct balanced characters for displayed four-circulant Hadamard6

Let H be a raw complex Hadamard of order six with four displayed circulant
blocks of order three. Write pa,pb,pc,pe for the products of their first
columns. The following complete written proof gives

    pa pe+pb pc=0.

Consequently, at these fixed row and column triples, both first characters
and both cubic characters of H and H* vanish. For the first side the
character is 3((pa/pc)^n+(pb/pe)^n); for the adjoint it is
3((conjugate(pa)/conjugate(pb))^n+(conjugate(pc)/conjugate(pe))^n).
Cancellation makes the two summands negatives, for n=1 and n=3.

This strengthens the previously conditional branch in
[the spectral companion theorem](spectral-companion.md) and
[the exact symmetry route](four-circulant-route.md): within that branch no
additional first-character vanishing assumption is required. The result
does not prove that an arbitrary complete-companion H has that prescribed
block symmetry. It does not solve the general triplet classification or
the general cubic/adjoint coupling conjecture.

The argument below is written matrix mathematics, independently checked
including all four phase-retrieval branches, repeated roots and zero modes.
The [supporting Lean source](proof/CirculantCharacter.lean) proves the
actual six-column character formulas, the first-character cancellation
criterion and both cubic implications **given** the phase-product
cancellation. It does not yet prove the Hadamard Gram equations imply
that cancellation; the full argument of Sections 2–7 is not yet formalized.
The subsequent [zero-mode interface](zero-mode-obstruction.md) and
[actual Gram/inverse bridge](gram-block-invertibility.md) now formalize
the Section 2 obstruction: actual Gram equations give all mode bounds,
flatness excludes zero modes, and four actual block inverses are constructed.
The subsequent [correlation and ratio-multiset proof](ratio-multiset-retrieval.md)
now formalizes the three-power correlation recovery and opposite ratio
multiset equality, including repeated roots. Actual cyclic-shift/adjoint
reconstruction and the real-rank arguments remain written mathematics.

Four-circulant companion construction and its general context are classical
Zauner theory; see [Szollosi, arXiv:0811.3930v2, Section 4](https://arxiv.org/pdf/0811.3930v2)
and [Matolcsi et al., arXiv:2503.14752v2, Section 4](https://arxiv.org/html/2503.14752v2).
The historical originality of this direct proof is not established.

## 1. Exact hypothesis and convention

Let
\[
 H=\begin{pmatrix}A&B\\ C&E\end{pmatrix},\qquad HH^*=H^*H=6I_6,
\]
where every entry has modulus one and each displayed block is a circulant 3-by-3 matrix. A raw square Hadamard needs only one of the Gram equations; the other follows by invertibility. They are both displayed here to make the Fourier use explicit.

Indices below are in Z/3Z. Let P e_j=e_(j+1), and set
\[
 C(a)_{ij}=a_{i-j},\qquad C(a)=a_0 I+a_1P+a_2P^2.
\]
The first column is a=(a0,a1,a2), and p_a=a0 a1 a2. Fix omega=exp(2 pi i/3). The Fourier eigenvector f_k has coordinates omega^(-ki), so P f_k=omega^k f_k. Define raw eigenvalues
\[
 \widehat a_k=\sum_{j=0}^2a_j\omega^{kj},\qquad
 a_j=\frac13\sum_{k=0}^2\widehat a_k\omega^{-kj}.
\]
Thus left or right multiplication by P^h multiplies eigenvalue k by omega^(hk), permutes the first column, and leaves p_a unchanged. Adjoint conjugates the phase product: p_(A*)=conjugate(p_a).

Simultaneous unitary Fourier transformation and interleaving turn H into three raw 2-by-2 modes
\[
 M_k=\begin{pmatrix}\widehat a_k&\widehat b_k\\
                    \widehat c_k&\widehat e_k\end{pmatrix},
 \qquad M_k M_k^*=M_k^*M_k=6I_2.
\]
Consequently
\[
 |\widehat a_k|=|\widehat e_k|,\quad
 |\widehat b_k|=|\widehat c_k|,\quad
 |\widehat a_k|^2+|\widehat b_k|^2=6,
\]
and
\[
              AC^*+BE^*=0.                       (1)
\]
Every raw block eigenvalue has modulus at most sqrt(6).

## 2. Zero Fourier modes are impossible for these flat order-three blocks

Suppose one eigenvalue of a flat triple a vanishes. The three unit numbers
z_j=a_j omega^(kj) then sum to zero. Divide by z0. From |1+z1/z0|=1, its real part is -1/2; the remaining number is the other primitive cube root. Therefore the three numbers are a common phase times {1,omega,omega^2}.

Every permutation of three cube roots has the form
\[
                   z_j=s\,\omega^{u+\epsilon j},
                   \qquad \epsilon\in\{1,-1\}.
\]
Indeed the six such affine permutations are all six permutations of Z/3Z. Absorb omega^u in s. The original triple is therefore a Fourier character times a common phase. One of its other raw Fourier eigenvalues has modulus 3. This contradicts the mode bound 3>sqrt(6).

Thus all three eigenvalues of each of A,B,C,E are nonzero, and all four blocks are invertible. This conclusion is special to flat length-three triples and the order-six mode bound. It is not a claim about an arbitrary 2-by-2 unitary mode or the classical construction in other even orders.

## 3. The six phase-retrieval alternatives, with multiplicity

For a unit triple a define
\[
 r_i=a_i/a_{i+1}=a_i\overline{a_{i+1}},\qquad
 s_a=r_0+r_1+r_2.
\]
Then each r_i has modulus one, their product is one, and
\[
 r_0r_1+r_1r_2+r_2r_0
     =\overline{r_0}+\overline{r_1}+\overline{r_2}
     =\overline{s_a}.
\]
They are precisely the three roots, with multiplicity, of
\[
                    t^3-s_a t^2+\overline{s_a}t-1.       (2)
\]
Equal Fourier absolute values imply equal cyclic autocorrelation. Under the convention above,
\[
 |\widehat a_k|^2=3+\overline{s_a}\omega^k+s_a\omega^{-k},
 \qquad
 s_a=\frac13\sum_k|\widehat a_k|^2\omega^k.
\]
Therefore a and e have the same ratio multiset, and b and c have the same ratio multiset.

A permutation of the three ratios is a cyclic rotation or a reflection. Recovering a triple from its three ratios fixes it up to one common unit phase. A rotation gives a cyclic shift of a. A reflection gives a cyclic shift of the adjoint first column (conjugate(a_(-i))). Thus there exist unit phases alpha,beta and j,l in Z/3Z such that
\[
 E=\alpha P^l A\quad\hbox{or}\quad E=\alpha P^l A^*,
 \qquad
 C=\beta P^j B\quad\hbox{or}\quad C=\beta P^j B^*.         (3)
\]
The conclusion does not require distinct ratios. Equal polynomials give equal multisets with multiplicity; one may label a bijection of their three occurrences, and that labeling is still one of the six permutations. Repeated ratios merely make alternatives coincide.

## 4. The three branches involving an adjoint

All circulant matrices, their adjoints and P commute. Use (1) and the invertibility proved in Section 2.

### 4.1. Adjoint/adjoint

If C=beta P^j B* and E=alpha P^l A*, (1) gives
\[
 AB(\overline\beta P^{-j}+\overline\alpha P^{-l})=0.
\]
Cancel AB. Distinct powers of P are not scalar multiples: their nonzero entries have disjoint support. Thus j=l and beta=-alpha. Alternatively, the k=0 mode already gives alpha=-beta, enough for the phase-product identity. Since |p_a|=|p_b|=1,
\[
 p_a p_e=\alpha^3|p_a|^2=\alpha^3,\qquad
 p_b p_c=\beta^3|p_b|^2=-\alpha^3.
\]
Their sum is zero.

### 4.2. E adjoint, C preserving

Suppose E=alpha P^l A* and C=beta P^j B. Equation (1) becomes
\[
 A(\overline\beta P^{-j}B^*+\overline\alpha P^{-l}B)=0.
\]
Cancel A and rearrange:
\[
 B^*=-(\overline\alpha/\overline\beta)P^{j-l}B.
\]
Using unit phases, this equivalently yields
\[
                       C=-\alpha P^l B^*.
\]
The pair is now the adjoint/adjoint branch with the same shift and opposite phases, so Section 4.1 applies.

### 4.3. E preserving, C adjoint

Suppose E=alpha P^l A and C=beta P^j B*. Then
\[
 B(\overline\beta P^{-j}A+\overline\alpha P^{-l}A^*)=0.
\]
Cancel B:
\[
 A^*=-(\overline\beta/\overline\alpha)P^{l-j}A,
 \qquad
                       E=-\beta P^j A^*.
\]
Again Section 4.1 applies. No division by a possibly zero Fourier eigenvalue is hidden in these cancellations: Section 2 already proved whole-block invertibility.

## 5. Precise reduction of the preserving/preserving branch

Assume C=beta P^j B and E=alpha P^l A. Put
\[
 r=-(j+l)/2,\qquad d=(l-j)/2
\]
in Z/3Z, where 2 is invertible. Multiply H on the left by diag(I,P^r) and on the right by diag(P^d,I). Let A'=A P^d, B'=B. Direct exponent calculation gives
\[
 r+j+d=0,\qquad r+l-d=0,
 \qquad
 H'=\begin{pmatrix}A'&B'\\ \beta B'&\alpha A'\end{pmatrix}.       (4)
\]
These operations preserve flatness, the raw Hadamard equations, circulant blocks and all four phase products.

Choose unit v with v^2=-beta/alpha, and set u=v/beta. Multiplying the lower block rows by u and the right block columns by v gives
\[
 H''=\begin{pmatrix}A'&D\\D&-A'\end{pmatrix},
 \qquad D=vB'.                                                (5)
\]
Indeed u beta/v=1 and u alpha v=-1. A unit square root always exists.

The expression G=p_a p_e+p_b p_c transforms by the same nonzero factor on both terms under block row/column phases: here G''=u^3 v^3 G. Thus zero transfers exactly between H and H''. In (5),
\[
 G''=-p_{A'}^2+p_D^2.
\]
It remains to prove the following lemma.

## 6. Real-rank lemma for the symmetric-minus form

**Lemma.** If flat circulant A,D form the raw Hadamard matrix [A D;D -A] of order six, then p_A^2=p_D^2.

Let alpha_k,delta_k be their raw Fourier eigenvalues. These are all nonzero by Section 2. The cross-mode equation is
\[
                   \alpha_k\overline{\delta_k}
                   =\delta_k\overline{\alpha_k}.
\]
Choose sigma_k=alpha_k/|alpha_k| and x_k=|alpha_k|>0. Then
\[
          \alpha_k=\sigma_k x_k,\qquad
          \delta_k=\sigma_k y_k,
\]
with y_k real and nonzero. Parseval and flatness give
\[
                    \sum_k x_k^2=\sum_k y_k^2=9.              (6)
\]

For any flat first column a, Fourier inversion gives
\[
 \sum_k\widehat a_k\,\overline{\widehat a_{k+1}}
       =3\sum_j |a_j|^2\omega^{-j}=0.
\]
Apply this to A and D and define t_k=sigma_k conjugate(sigma_(k+1)). Then
\[
 \sum_k t_k x_kx_{k+1}=0,\qquad
 \sum_k t_k y_ky_{k+1}=0,\qquad
                     \prod_k t_k=1.                         (7)
\]
Each t_k has modulus one. Consider the real-linear map L:R^3 -> C,
L(z)=sum_k t_k z_k. Its rank is either one or two; it cannot be zero.

### 6.1. Real rank two

The real kernel has dimension one. The two nonzero real vectors
(x_kx_(k+1)) and (y_ky_(k+1)) in (7) are proportional. For some rho≠0,
\[
 y_ky_{k+1}=\rho x_kx_{k+1}.
\]
Put q_k=y_k/x_k≠0. Thus
q0 q1=q1 q2=q2 q0=rho. Cancelling the nonzero q's shows q0=q1=q2=q. Equation (6) then gives q^2=1. Hence D=qA with q=±1, and their phase products have equal squares.

### 6.2. Real rank one

All t_k lie on one real line. Write t_k=epsilon_k tau with epsilon_k∈{±1} and |tau|=1. If delta=product epsilon_k, (7) implies tau^3=delta. Replace tau by kappa=delta tau and epsilon_k by epsilon'_k=delta epsilon_k. Then
\[
 \kappa^3=1,\qquad t_k=\epsilon'_k\kappa,\qquad
                      \prod_k\epsilon'_k=1.
\]
Write kappa=omega^m. Choose signs eta0=1,
eta1=epsilon'_0, eta2=epsilon'_0 epsilon'_1. Their cyclic neighboring products are precisely epsilon'_k. From the defining neighboring ratios for sigma, with s=sigma0, one obtains
\[
                    \sigma_k=s\,\eta_k\,\omega^{-mk}.         (8)
\]
The product-one sign condition verifies the return from k=2 to k=0, so there is no missing cyclic consistency condition.

Consequently
\[
                    \widetilde A=\overline{s}P^m A,
 \qquad             \widetilde D=\overline{s}P^m D
\]
have respective real eigenvalues eta_k x_k and eta_k y_k. Unitary Fourier diagonalization therefore makes both matrices Hermitian. They remain flat circulants.

The first column of a Hermitian flat order-three circulant is
(h0,h1,conjugate(h1)), where h0 is real of modulus one. Its phase product is h0 |h1|^2=±1. Thus
\[
 p_{\widetilde A}^2=p_{\widetilde D}^2=1,\qquad
 p_{\widetilde A}=\overline{s}^{\,3}p_A,\quad
 p_{\widetilde D}=\overline{s}^{\,3}p_D.
\]
This gives p_A^2=p_D^2. The rank cases exhaust (7), proving the lemma.

## 7. Return to the general four-block identity

Apply Section 6 to (5). It gives G''=0, and the nonzero covariance factor gives G=0. Equivalently, directly in the preserving/preserving branch,
\[
 p_D^2=v^6 p_b^2=-(\beta/\alpha)^3p_b^2.
\]
So p_A'^2=p_D^2 says alpha^3 p_a^2+beta^3 p_b^2=0, which is exactly p_a p_e+p_b p_c=0. Together with the other three branches in Section 4, this proves the theorem without a genericity assumption.


## 8. Verification and precise formal boundary

The supporting Lean carrier is `Sum (Fin 3) (Fin 3)`, with precisely six
indices. Each of its four blocks is the actual Mathlib `Matrix.circulant`,
and the balanced character sums products/quotients of actual matrix entries
over all six columns. The adjoint formula uses the actual matrix
`conjTranspose`, rather than a separate supplied scalar list. No flatness
or Gram premise is required for these formulas. Nonzero denominator
assumptions are explicit in the vanishing implications and follow from
flatness for the written theorem.

The actual compiler record and standard-axiom audit are provided with the
source. This interface is distinct from a full Lean proof of the Fourier
phase-retrieval and real-rank argument above. The separate
[unit-triple source](proof/UnitTripleZeroSum.lean) now proves the algebraic
zero-mode obstruction from supplied mode bounds, with its own six audits.
The [connected Gram and inverse modules](gram-block-invertibility.md)
discharge those bounds from actual matrix multiplication and construct all
four block inverses, with five plus three further audits. The full
Gram-to-product-cancellation theorem still awaits actual cyclic-shift/adjoint
reconstruction and the real-rank arguments. The correlation and ratio
multiset steps are now formalized separately, including repeated values.

From the existing pinned `002-weighted-rectangular-pruning/proof/mathlib`
package, after obtaining the cache for its imports:

```powershell
lake env lean ../../../004-mub-triplets/proof/CirculantCharacter.lean
```

Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`
are retained. All printed audits, actual source hashes and compiler
observation details are in the companion record. No complete general MUB
claim is imported from an external proof.
