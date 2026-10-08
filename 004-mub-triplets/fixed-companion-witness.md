# When a fixed companion admits the extra spectral symmetry

This note determines the extra double anticommutation condition for a
fixed complete companion. It gives an exact failure example inside a
genuine MUB triplet. The example does not refute the general cubic
coupling or show that H has no suitable alternative companion.
The results here are written matrix proofs, not Lean theorems.

## 1. Fixed basis and normalization

Use raw order-six Hadamards H,K with every entry of H*K of squared
modulus six, as in the [spectral criterion](spectral-companion.md).
Put

    U=K/sqrt(6),   L=H*K/sqrt(6),
    D=diag(1,1,1,-1,-1,-1),   D'=HDH*/6,
    B=U*DU,   C=U*D'U,   W=BC.

Both B,C are Hermitian unitary involutions with zero diagonal.
For B this follows from |K_ia|²=1 and the three positive and three
negative entries of D. For C use C=L*DL/6 and that L is raw Hadamard.

A fixed-companion witness means A=U diag(lambda) U*, with lambda a
permutation of (-5,-3,-1,1,3,5), and DAD=-A, D'AD'=-A. The latter
equation is exactly the second condition in the spectral note after
conjugation by H/sqrt(6). Each such A automatically has the required
two sets of diagonal moments because K is a complete companion.

## 2. An exact matching criterion

**Theorem 2.1.** A fixed-companion witness exists if and only if B,C
are monomial matrices with the same fixed-point-free involution as
their support permutation. Equivalently, B is monomial and W is
diagonal in this fixed U basis.

Proof: write T=diag(lambda). Anticommutation is TB+BT=TC+CT=0.
Entrywise this says

    (lambda_a+lambda_b)B_ab=(lambda_a+lambda_b)C_ab=0.

Each nonzero lambda has one distinct negative partner. Hence each row
of B,C can have support only at that partner. Unitarity forces that
entry to have modulus one; Hermitian symmetry gives an involution.
Both supports use the same three pairs. Conversely assign the positive
labels 1,3,5 to one vertex of each pair and their negatives to the
partners. These entrywise equations then give a witness.

Two such monomial involutions have diagonal product. Conversely, if B
is monomial, its Hermitian involution property and zero diagonal give
three pairs. Since C=BW, a diagonal W preserves that support, proving
the second equivalence.

An exact scalar version is

    M4(B)=sum_ab |B_ab|^4,
    Off(W)=sum_(a!=b) |W_ab|^2,
    witness exists  <=>  6-M4(B)+Off(W)=0.          (2.1)

Indeed in every unitary row the nonnegative numbers p_b=|B_ab|² sum
to one. Thus sum_b p_b²<=1, with equality exactly when a single p_b
equals one. Summing gives M4(B)<=6, with equality exactly for a
monomial B. Off(W)>=0 vanishes exactly when W is diagonal. This proves
(2.1); a small floating residual is not an exact certification.

## 3. Simple products and the degeneracy issue

**Corollary 3.1.** If W is diagonal in the fixed U basis and its six
diagonal entries are distinct, a fixed-companion witness exists.

Proof: W=BC gives BWB=W*, so if W=diag(nu),

    (nu_b-conjugate(nu_a))B_ab=0.

Distinct nu permit only one nonzero entry per row; unitarity guarantees
one exists. A real nu would force this entry to be diagonal, contradicting
B_aa=0. Thus the support pairs conjugate eigenvalues without fixed
points, and Theorem 2.1 applies.

With repeated eigenvalues the corresponding block of B can be dense.
Diagonal W alone then does not give a witness. Rotating such an
eigenspace may change the companion's entrywise flatness in either
basis; it is not an automatically valid replacement of K.

## 4. A complete triplet with a failing fixed companion

Let omega be a primitive cubic root of unity, F_jk=omega^(jk) for
j,k in Z/3, and i²=-1. Set

    T_a=diag(1,omega^a,omega^a)F,   a=1,2,
    H=[F F;F -F],   K=[T_1 T_2;iT_1 -iT_2].       (4.1)

Every entry has modulus one. FF*=3I and T_a*T_a=3I give H*H=K*K=6I;
the off-diagonal block of K*K is T_1*T_2-T_1*T_2=0.
The entries of F*T_a are 1+2omega^a on the diagonal and 1-omega^a
off it. Since omega^a+omega^(-a)=-1, both squared moduli equal three.
Moreover

    H*K=[(1+i)F*T_1 (1-i)F*T_2;
         (1-i)F*T_1 (1+i)F*T_2].

All thirty-six entries have squared modulus six. Thus (4.1) supplies
a complete companion and three actual mutually unbiased bases.

Direct block multiplication gives

    D'=[0 I_3;I_3 0],
    R=T_1*T_2/3=F*diag(1,omega,omega)F/3,
    B=[0 R;R* 0],   C=[0 -iR;iR* 0],
    W=diag(iI_3,-iI_3).                           (4.2)

R is unitary. Its entries are (1+2omega)/3 on the diagonal and
(1-omega)/3 off it, all of modulus 1/sqrt(3). Each row of B has
three nonzero entries, so B is not monomial. There is no fixed-companion
witness, despite diagonal W. Indeed anticommutation with B alone forces
T=diag(tI_3,-tI_3), which cannot have six distinct eigenvalues.
The exact defect in (2.1) is 6-18/9+0=4.

For this same H choose instead

    K_0=[T_1 T_1;iT_1 -iT_1].

The identical Hadamard and unbiasedness calculations prove completeness.
Now R_0=I_3 in (4.2); B_0,C_0 share the pairing a<->a+3.
The labels (1,3,5,-1,-3,-5) therefore give a witness. This distinguishes
failure for a fixed K from nonexistence over all companions of H.

Finally, the column characters of H and H* at alpha are each
(1,1,1,-1,-1,-1), since every row and column product of F equals one.
Their first and cubic sums vanish. The example agrees with the coupling
target and supplies no counterexample to it.

## 5. What remains and prior methods

For an arbitrary eligible H it is still unproved here that some complete
companion makes B,C share the required matching. Theorem 2.1 decides
the fixed-basis question; it does not remove that existential gap.
The spectral criterion and the general cubic coupling remain separate.

Monomial support, spectral pairing and qutrit quadratic chirps are
standard tools. The ingredients diag(1,omega^a,omega^a)F occur in
[Durt et al., On mutually unbiased bases, Appendix B](https://arxiv.org/abs/1004.3348).
Historical originality of this particular fixed-companion obstruction
has not been established. No new Lean compilation or axiom audit is
attributed to this note; the earlier scalar interpolation proof does
not formalize its actual matrices or support argument.
