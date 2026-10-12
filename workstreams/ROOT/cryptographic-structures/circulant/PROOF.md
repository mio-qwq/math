# Related differentials for invertible circulant matrices

Complete written theorem, integrated from the frozen version-2 proof. The theorem covers every characteristic-two field and every order n>=3. The prior mathematical review and the current bounded technical replay are identified in ../VERIFICATION.json; no Lean formalization, human peer review, historical priority, or cipher attack is claimed.

The original version-1 proof is preserved at https://github.com/mio-qwq/math/blob/7144a9245827c4cd1f45449e0776e46f2599f6fb/workstreams/CRYPTO2-20261011-7f3c/PROOF.md. Version 2 corrected the ancillary suggestion that an MDS periodic quotient might lose MDS and added the branch-number inheritance proof; the main existence theorem was unchanged.

## Statement and exact relation to the source

Let K be a field of characteristic two. Vectors are columns. For vectors
x,y in K^n write R(x,y) when, for every coordinate i,

    x_i = 0, or y_i = 0, or x_i = y_i.

Equivalently x_i y_i (x_i+y_i)=0. A **nontrivial related-differential pair**
for an invertible matrix M consists of u,v with

    u != 0, v != 0, u != v, R(u,v), R(Mu,Mv).

Invertibility then also gives Mu,Mv,Mu+Mv all nonzero. Thus no zero
differential or duplicate differential is silently admitted. This is the
notion of Daemen–Rijmen (2009), Sections 7–8, with nontriviality explicit;
it also matches the omitted (u,u,0) triplets in Kumar–Yadav–Samanta (2026),
Section V.

**Main theorem.** Every invertible circulant matrix over K of order n>=3
has a nontrivial related-differential pair.

In particular this holds for every circulant MDS matrix over every F_(2^m),
m>=1. For the source's unresolved MDS orders n≡±2 (mod 12), n>2, the
answer is affirmative. The source is arXiv:2605.27535v1, Theorem 5 and the
unnumbered final question of Section VI; it does not state a fully quantified
numbered conjecture. The completion uses the divisor-lifting
step below. The non-MDS, odd symmetric and 4-divisible ingredients are
attributed to prior work, not claimed as discoveries here.

The theorem is a property of a diffusion component. It supplies no new
round count, attack probability, data/time/memory bound or attack on AES.

## 1. Non-MDS invertible matrices (known ingredient, proved for exact scope)

Here MDS means every nonempty square submatrix is nonsingular, the standard
equivalent definition for a square MDS diffusion matrix.

**Lemma 1.** If an invertible n-by-n matrix M is not MDS and n>=2, it has
a nontrivial related-differential pair.

Proof. Choose row/column sets I,J of the same size r such that M[I,J] is
singular. Invertibility of M implies 1<=r<n. Choose nonzero s in its kernel,
and extend it to u on the column set J, with zeroes on J^c. Then

    u != 0, (Mu)_I = 0, and (Mu)_(I^c) != 0.

Put D=M[I^c,J^c]. If D is singular, take nonzero t in ker D and extend it
to v supported on J^c. Input supports are disjoint; output supports are
also disjoint, since (Mv)_(I^c)=0. Both vectors are nonzero and distinct.

If D is nonsingular, solve D t=(Mu)_(I^c) and extend t to v on J^c.
The right hand side is nonzero, so t!=0. Inputs again have disjoint supports.
On I, Mu is zero; on I^c, Mv equals Mu. Thus the outputs are related.
This proves all nontriviality assertions. QED.

This is the invertible specialization of KYS Theorem 2, with its possible
degenerate vectors explicitly excluded. We do not assert its printed
unrestricted-singular version under our stronger nontriviality convention.

## 2. Odd symmetric matrices (known ingredient with a direct scalar proof)

**Lemma 2.** Every invertible symmetric matrix S of odd order d>=3 over K
has a nontrivial related-differential pair.

Proof. If S is not MDS, apply Lemma 1. Otherwise write d=2r+1, r>=1,
and partition the indices into A,{c},B with |A|=|B|=r. Define

    H=S[B,A],   p=S[B,c],   q=S[A,c].

H is invertible because S is MDS. Choose u,v by

    u_A=H^(-1)p,  u_c=1,  u_B=0;
    v_A=0,         v_c=1,  v_B=(H^T)^(-1)q.

In characteristic two these equations give (Su)_B=0 and (Sv)_A=0.
The input pair is related. Since all entries of an MDS matrix are nonzero,
p!=0 and q!=0; hence u_A and v_B are nonzero, so u,v are distinct and
nonzero. At the one remaining output coordinate c, symmetry gives

    (Su)_c = q^T H^(-1)p + S_cc,
    (Sv)_c = p^T(H^T)^(-1)q + S_cc.

The scalar expressions are transposes of each other and therefore equal.
All output coordinates satisfy R. QED.

This proves the invertible form of KYS Theorem 4 together with their
non-MDS reduction; it is not claimed as a new theorem.

**Corollary 2.1 (known odd circulant case).** Every invertible circulant
of odd order d>=3 has such a pair.

Use the first-column convention C_ij=a_(i-j mod d). Let P reverse row
indices i -> -i mod d. Then (PC)_ij=a_(-i-j mod d), which is symmetric.
PC is invertible, so apply Lemma 2. Row permutation preserves R, hence
the same input pair works for C. (For the general invertible theorem no MDS hypothesis is used;
for an MDS input, quotient MDS does follow, as proved in Section 5a below.)

## 3. Multiples of four (known ingredient)

**Lemma 3.** Every invertible circulant of order divisible by four has
such a pair.

If it is not MDS, use Lemma 1. Otherwise identify cyclic convolution by
the first column a with multiplication by a(X) in K[X]/(X^n-1).
Separate a=e+o into even and odd exponent terms. Both e and o are nonzero
because MDS implies every coefficient a_i is nonzero. Take u=e, v=o.
Their input supports are disjoint, so they are nonzero and distinct.
The outputs are

    a e = e^2 + eo,       a o = o^2 + eo.

As 4 divides n, reduction modulo X^n-1 preserves residues mod 4.
In characteristic two e^2 is supported in residue 0, o^2 in residue 2,
and eo at odd indices. Thus the first output is zero at residue 2,
the second at residue 0, and their odd coordinates are equal. QED.

The n=4 construction is classical (Daemen–Rijmen 2009, Section 9.1).
The 4-divisible version appears in Whirlwind (2010) and KYS Lemma 1.

## 4. Divisor lifting

**Lemma 4.** Let d divide n, n=td, and let M be circulant with first
column (a_0,...,a_(n-1)). Set

    b_r = sum_(k=0)^(t-1) a_(r+kd),  0<=r<d,
    B_rs = b_(r-s mod d),
    (J x)_i = x_(i mod d),  0<=i<n.

Then M J = J B. If M is invertible then B is invertible. Every nontrivial
related-differential pair for B lifts via J to one for M.

Proof. For fixed i and each residue s mod d, grouping the summands gives

    (MJx)_i = sum_(j=0)^(n-1) a_(i-j mod n) x_(j mod d)
             = sum_(s=0)^(d-1) b_(i-s mod d) x_s
             = (JBx)_i.

J is injective since its first d coordinates equal x. If Bx=0 then
M Jx=0, whence Jx=0 by invertibility of M, so x=0. B is square and
therefore invertible. Repetition preserves nonzero vectors, inequality
of two vectors, and the coordinatewise relation R. The intertwining
identity supplies the output relations. QED.

No division by t occurs. In particular the step works in characteristic
two when t=2; replacing repetition by averaging would be invalid.
With only invertibility assumed, B need not be MDS. If M is MDS,
then B IS MDS, by Section 5a; no loss of MDS is asserted.

## 5. Completion of the main theorem

For odd n>=3 apply Corollary 2.1. For n divisible by four apply Lemma 3.
In the only remaining case n≡2 (mod 4), n>=3 implies n=2d with odd
d>=3. Apply Lemma 4 to obtain an invertible d-by-d circulant B; by
Corollary 2.1 it has a nontrivial related-differential pair. Lift it
with J. These three cases exhaust all n>=3. QED.

For the newly targeted residues n≡±2 (mod 12), n>2, the construction
simply uses the first-column sums b_i=a_i+a_(i+n/2) and repeats each
quotient witness twice. All previously covered orders remain prior work.

## 5a. MDS inheritance and a shorter proof in the original MDS scope

**Proposition 5a.** In Lemma 4, define the differential branch number by

    beta(T) = min_(x != 0) (wt(x) + wt(Tx)).

Then beta(B) >= ceil(beta(M)/t). In particular, if M is MDS of order
n=td, its quotient B is MDS of order d.

Proof. For each nonzero x, Jx is nonzero and the exact repetition gives

    t (wt(x)+wt(Bx)) = wt(Jx)+wt(MJx) >= beta(M).

Take the integer ceiling and then the minimum over x. If M is MDS,
beta(M)=td+1, hence beta(B)>=d+1. Conversely any d-by-d matrix has
beta(B)<=d+1 by testing a coordinate vector, so equality holds. QED.

This is a direct elementary weight consequence of the periodic subspace,
not an additional cryptanalytic attack claim. It corrects v1's suggestion
that an MDS input might lose MDS under this quotient; no such loss is
possible. The earlier complete invertible-matrix argument remains valid.

Consequently the source's unresolved MDS orders have a particularly short
proof: if n is congruent to ±2 modulo 12 and n>2, take d=n/2, which is
odd and at least 5. The quotient B is an odd MDS circulant. The known odd
circulant result supplies a nontrivial RD pair for B, and Lemma 4 repeats
it to give a pair for M. No non-MDS reduction is required for this special
case. This completes the MDS remaining-order direction using the source's
own proven odd-order statement plus the lifting
argument. Whether that application was previously published remains an
open literature question.

## 6. Necessary boundary and limitations

n=2 cannot be included. For a 2-by-2 MDS matrix, every nonzero graph
codeword (x,Mx) has weight at least 3. If a nontrivial RD pair existed,
the three nonzero graph codewords for u,v,u+v would have at least nine
nonzero coordinates in total. At each of four positions R forces zero
or two nonzero entries among the triple, giving at most eight. Contradiction.
For example [[1,alpha],[alpha,1]] over F4 with alpha^2+alpha+1=0 is
circulant and MDS. This boundary argument is a special case of the
classical related-differential MDS support count, not new.

No statement about arbitrary singular matrices is included. The argument
works over any characteristic-two field; characteristic other than two is
not covered. A proof of existence of an RD component does not by itself
yield an attack, so attack-model success and complexity are not specified.

## Attribution and historical limits

The proof closes the remaining invertible/MDS circulant orders in the
inspected source using the elementary invariant periodic subspace. That
invariant-subspace fact is standard linear algebra; historical originality
of this application is not certified. The exact original source and
independent AI review are linked in ../provenance.json and ../VERIFICATION.json.
The accepted scope remains the written theorem; no Lean proof or cipher
attack follows from the finite supporting checks.
