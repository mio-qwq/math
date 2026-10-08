# A finite spectral test for complete MUB companions

This note gives a written equivalence for a complete third basis and a
conditional structural branch of the cubic-character question. The spectral
theorem, Vandermonde interpolation and Fourier diagonalization are standard
tools. Historical originality of this reformulation is not established.
The general six-dimensional coupling conjecture is not proved here.

## 1. Normalization and the target

All matrices have complex entries. A raw Hadamard matrix of order six has
unit-modulus entries and satisfies H*H=6I; star denotes conjugate transpose.
Because H is square, this also gives HH*=6I. A complete companion of H is
a raw Hadamard matrix K such that every entry of H*K has squared modulus 6.
Thus I,H/sqrt(6),K/sqrt(6) are three actual mutually unbiased bases.
The six columns of K must be mutually orthogonal.

Write alpha=(1,1,1,-1,-1,-1) and

    g_H(delta) = sum_j product_i H_ij^(delta_i).

The source-stated cubic target is g_H(3alpha)g_H*(3alpha)=0 on the whole
complete-companion class. Relabellings are relevant to its full permutation
form; the statements below keep the displayed row and column partitions
fixed. Negative powers cause no singularity because all entries are nonzero.

## 2. Reconstruction of six spectral weights

Let Lambda=(-5,-3,-1,1,3,5), with six distinct real entries. For arbitrary
real weights w_t, the following conditions are equivalent:

    for m=0,...,5: sum_t Lambda_t^m w_t = (sum_t Lambda_t^m)/6;
    for every t: w_t=1/6.

Proof: the coefficient matrix is Vandermonde, with nonzero determinant
product_(s<t)(Lambda_t-Lambda_s). The constant weights solve the system,
so they are its unique solution. This includes signed weights.
[SpectralMomentWeights.lean](proof/SpectralMomentWeights.lean) proves this
exact fixed six-node system in both directions, using exact real arithmetic.
It does not formalize the matrix arguments in the following sections.

## 3. A complete-companion equivalence

**Theorem 3.1.** Fix a raw Hadamard H. It has a complete companion if and
only if there is a Hermitian A with characteristic polynomial

    (x^2-1)(x^2-9)(x^2-25)

such that, for m=1,...,5 and all indices i,j,

    (A^m)_ii = tr(A^m)/6,
    (H* A^m H)_jj = tr(A^m).                         (3.1)

These are conditions on complete spectral projections, not only one
unbiased vector. No additional companion classification is assumed.

Proof, forward direction: given K put U=K/sqrt(6), choose the six
eigenvalues Lambda in any order, and set A=U diag(Lambda) U*.
This is Hermitian with the specified characteristic polynomial. Since
|U_it|^2=1/6,

    (A^m)_ii = sum_t Lambda_t^m |U_it|^2 = tr(A^m)/6.

Also |(H*U)_jt|^2=1, by the companion assumption, so

    (H* A^m H)_jj = sum_t Lambda_t^m |(H*U)_jt|^2 = tr(A^m).

Reverse direction: the finite-dimensional spectral theorem gives
A=U diag(Lambda) U* with U unitary. For a fixed i take
w_t=|U_it|^2. The m=0 equation follows from UU*=I, and (3.1) gives
the other five equations. Section 2 forces |U_it|^2=1/6.
For a fixed j instead take w_t=|(H*U)_jt|^2/6. Its m=0 equation follows
from H*UU*H=6I, and (3.1) gives the other equations. Thus
|(H*U)_jt|^2=1. Consequently K=sqrt(6)U is raw Hadamard and
|(H*K)_jt|^2=6, as required. This reconstructs all six orthogonal columns.

The zero-degree conditions are automatic and must not be omitted without
these unitarity arguments. The distinct prescribed spectrum is what makes
five nonconstant moments sufficient.

## 4. A double anticommutation branch

Put D=diag(1,1,1,-1,-1,-1). The added hypothesis in this section is that
a witness A from Theorem 3.1 also satisfies

    D A D = -A,
    D (H* A H/6) D = -H* A H/6.                     (4.1)

**Theorem 4.1.** Under (4.1), H can be transformed by separate monomial
unitaries within its two row blocks and its two column blocks into a matrix
whose four 3-by-3 blocks are circulant. If in addition either
g_H(alpha)=0 or g_H*(alpha)=0, then both g_H(3alpha) and g_H*(3alpha) vanish.

Proof: choose unit eigenvectors of A for the positive eigenvalues 1,3,5.
Anticommutation pairs them with their D images at eigenvalues -1,-3,-5.
Use these six vectors in that order to form the unitary U from Theorem 3.1.
All six are flat by Section 3. The associated raw companion has the form

    K = [ P  P ; Q -Q ].

The identities K*K=6I show P*P=Q*Q=3I; all entries of P,Q have modulus
one. They are raw order-three Hadamards.

Let L=H*K/sqrt(6). It is raw Hadamard and its normalized columns are
eigenvectors of B=H*AH/6 with the same eigenvalues. The second identity
in (4.1) pairs its positive and negative columns. Simplicity of each
eigenvalue implies that each actual negative column differs by a unit
phase from the D image of the corresponding positive column. Hence

    L = [ X XZ ; Y -YZ ],

where Z is diagonal unitary and X,Y are raw order-three Hadamards.
As HH*=6I we have H=KL*/sqrt(6), yielding

    H = (1/sqrt(6)) [
          P(I+Z*)X*   P(I-Z*)Y* ;
          Q(I-Z*)X*   Q(I+Z*)Y* ].                 (4.2)

Every raw order-three Hadamard W has a representation W=M F E with
M monomial unitary, E diagonal unitary, and F_jk=omega^(jk), j,k in Z/3.
For completeness, dephase its first row and column to one. A remaining
row (1,a,b) satisfies 1+a+b=0 and |a|=|b|=1, forcing {a,b}={omega,omega^2}.
The other row has the opposite ordering by orthogonality. This is F up to
row and column permutations. Each permutation of Z/3 is affine k->ak+b,
a=1 or -1, so a right column permutation of F can be absorbed into a
left row permutation and left phases. This proves the stated representation
without needing a further right permutation.

Apply that representation independently to P,Q,X,Y in (4.2). Removing
their left monomial factors by blockwise row and column operations leaves
four blocks of the form F E' F*, with E' diagonal. Each is circulant because
its (i,j) entry depends only on i-j modulo three. The resulting matrix is
still raw Hadamard, so all entries of all four blocks have modulus one.

Call the four blocks C(a),C(b),C(c),C(d), where C(a)_ij=a_(i-j), etc.
For the top-row versus bottom-row character alpha, the three left column
ratios are all u=product(a)/product(c); the three right column ratios are
all v=product(b)/product(d). Thus g(alpha)=3(u+v).
For the adjoint character, the three top-row products are all
s=conjugate(product(a)/product(b)), and the three bottom-row products are
all t=conjugate(product(c)/product(d)). Thus g_*(alpha)=3(s+t).
Write a0=product(a), b0=product(b), c0=product(c), d0=product(d).
Then u+v=(a0*d0+b0*c0)/(c0*d0) and
s+t=conjugate((a0*d0+b0*c0)/(b0*d0)). All four products are nonzero.
Thus either first-character equality implies the other, and gives
v=-u and t=-s, so both cubic sums vanish.

Finally the blockwise monomial transformations preserve the zero and
nonzero status of these fixed balanced characters. Within-block
permutations preserve alpha; left phases multiply g_H(alpha) by one
unit scalar; right phases cancel because sum_i alpha_i=0. The adjoint
calculation interchanges left and right. This completes the proof.

## 5. What this branch excludes and what remains

Theorem 4.1 excludes a precise bad branch: a complete-companion H with
both first characters zero and both cubic characters nonzero cannot have
a spectral witness satisfying the two additional anticommutation equations.
No proof is given that such a witness exists for every eligible H.
Consequently this is a conditional structural result, not a solution of
the general coupling or triplet-classification conjecture.

Theorem 3.1 is an exact replacement for the complete companion condition;
it is not a computational complexity bound. It replaces one feasibility
formulation with another and may expose a useful extra symmetry. Numerical
solutions of the new equations would still require exact certification.

## 6. Prior work and verification boundary

The public conjecture and character notation come from
[Matolcsi, Matszangosz, Varga and Weiner (2026)](https://link.springer.com/article/10.1007/s10801-026-01506-x).
Hermitian observables, orthogonal commutative algebras and Fourier
diagonalization are established MUB tools; see the primary review
[Durt et al., On mutually unbiased bases](https://arxiv.org/abs/1004.3348).
No claim that spectral interpolation or circulant matrices are new is made.
The specific conditional reduction above has a self-contained proof;
its equivalence to a previously published characterization has not been
settled by the bounded literature review.

Only Section 2 has the Lean proof supplied here. Sections 3 and 4 are
written matrix proofs using the standard finite-dimensional spectral
theorem. The general companion coupling remains a research target.
