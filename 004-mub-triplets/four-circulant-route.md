# The exact scope of the double-anticommutation route

The four-circulant companion construction below is classical Zauner theory,
as stated and proved in [Szollosi, Section 4, Proposition 4.2](https://arxiv.org/pdf/0811.3930).
This note identifies its relationship to the extra spectral symmetry in
[the companion criterion](spectral-companion.md) and gives a finite exact
test for that branch. It does not claim a new MUB construction, historical
originality of the test, or a solution of the general coupling conjecture.
All proofs here are written matrix arguments; they are not Lean proofs.

## 1. Fixed partitions and equivalent conditions

Star means conjugate transpose. Let H be a raw order-six Hadamard and
D=diag(I3,-I3). Keep the displayed row and column triples fixed.
The following conditions are equivalent:

1. Some complete companion K and some ordering of the six nodes
   {1,3,5,-1,-3,-5} give A=K diag(nodes) K*/6 satisfying
   DAD=-A and D(H*AH/6)D=-H*AH/6.
2. Block diagonal monomial unitaries R,S, respecting each displayed triple,
   make R H S four-circulant: each of its four 3-by-3 blocks is circulant.
3. For some permutations p,q, each a three-cycle on each displayed triple,
   the phase ratios t_ij=H_(p(i),q(j))/H_ij satisfy

       t_ij t_(i0,j0)=t_(i,j0) t_(i0,j)             (1.1)

   for every i,j, at any one fixed pivot (i0,j0).

There are four choices of p and four choices of q, hence sixteen candidate
pairs. For each pair only the 25 identities with i!=i0 and j!=j0 are
nontrivial. This is an exact algebraic criterion, not a tolerance test or
a reported numerical enumeration. Every denominator is nonzero because
all entries of H have modulus one.

The moments in the companion criterion follow from completeness of K;
condition 1 does not replace a whole basis by a single unbiased vector.
The implication 1 to 2 is the order-three argument in Theorem 4.1 of
the companion criterion. Sections 2 and 3 prove the other implications.

## 2. Classical companion construction, including zero modes

Assume first that H itself has four circulant blocks. Let F_jk=omega^(jk)
be the raw order-three Fourier matrix, f=F/sqrt(3) and Omega=diag(f,f).
Conjugating H/sqrt(6) by Omega diagonalizes each block. After interleaving
the two triples, the result consists of three unitary 2-by-2 modes
M_k=[a_k b_k;c_k d_k]. These normalized eigenvalues can be zero.

For any unitary M=[a b;c d] there are unit phases u,v,x,y such that

    M=(1/2)[u+v, y(u-v); (u-v)/x, y(u+v)/x].       (2.1)

If a,b are nonzero, put

    t=i(a/|a|)|b|,  u=a+t,  v=a-t,  y=b/t,  x=t/c.

Unitarity gives |c|=|b|, |d|=|a| and |a|^2+|b|^2=1.
Thus x,y,u,v have modulus one. Orthogonality of the columns, together
with conjugate(a)t=-a conjugate(t), gives d=ya/x, proving (2.1).
If b=0 then c=0; choose u=v=a, x=1, y=d/a.
If a=0 then d=0; choose t=b, u=t, v=-t, y=1, x=t/c.
The first row of a unitary cannot vanish, so these cases exhaust all modes.
No zero eigenvalue is divided by.

Apply (2.1) to each mode. Let U0,V0,X,Y be the diagonal unitary matrices
formed from its u,v,x,y phases. Define raw matrices

    K=[F U0, F V0; F U0 X*, -F V0 X*],
    L=[F,    F;    F Y*,    -F Y*].                (2.2)

All entries have modulus one, and F*F=FF*=3I gives
K*K=KK*=L*L=LL*=6I. Block multiplication yields

    KL*/sqrt(6)=(1/sqrt(6))[
       F(U0+V0)F*,       F(U0-V0)Y F*;
       F X*(U0-V0)F*,    F X*(U0+V0)Y F* ].        (2.3)

Conjugating its normalization by Omega recovers every mode in (2.1).
Consequently H=KL*/sqrt(6) and H*K/sqrt(6)=L. K is a complete companion,
including all six orthogonal columns and all 36 transition entries.

With T=diag(1,3,5), Lambda=diag(T,-T) and A=K Lambda K*/6, direct products give

    A=[0, f T X f*; f T X* f*, 0],
    H*AH/6=[0, f T Y f*; f T Y* f*, 0].           (2.4)

Both are off diagonal relative to D. A is Hermitian with the prescribed
simple spectrum. For every m>=0, flatness of K/sqrt(6) and L gives
(A^m)_ii=tr(A^m)/6 and (H*A^mH)_jj=tr(A^m).
This proves the entire spectral witness, including its five required moments.

For condition 2, apply the construction to Hc=RHS and transport it back:
K=R* Kc, L=S Lc and A=R* Ac R. R,S commute with D, so completeness and
both anticommutation equations persist. This proves 2 to 1.
The construction works in every even order 2n; the reverse implication
1 to 2 uses the special order-three Hadamard classification.

## 3. Elimination of the monomial phases

Assume (1.1). Set r_i=t_(i,j0) and
conjugate(s_j)=t_(i0,j)/t_(i0,j0), so t_ij=r_i conjugate(s_j).
Let monomial unitaries M,N act by

    M e_i=r_i e_(p(i)),  N e_j=s_j e_(q(j)).

The ratio equality says M H N*=H, or M H=H N.
On each three-cycle M^3 and N^3 are scalar identities, with scalars the
products of their three phases. Cubing M H=H N and using all 36 nonzero
entries forces the four cycle products to be the same phase rho.
Choose a unit cube root eta of rho. Dividing both M and N by eta retains
the intertwining equation and makes all cycle products equal to one.

A weighted three-cycle with product one is conjugate, by diagonal phases,
to its ordinary cycle: propagate a phase around the cycle; product one
ensures consistency on return to the starting vertex. Permutations within
each triple then orient the cycles to the same ordinary cycle P.
Thus blockwise monomial R,S arrange

    R M R*=diag(P,P),  S N S*=diag(P,P).

For Hc=R H S* the relation becomes diag(P,P) Hc=Hc diag(P,P).
Each block commutes with P, hence is constant on simultaneous cyclic
row/column shifts and is circulant. This proves 3 to 2.

Conversely, four circulant blocks commute with simultaneous cyclic shifts.
Transport these shifts through the blockwise monomial changes in condition 2.
They give M H N*=H with the requisite cycle types. Its entrywise phase
ratios factor as r_i conjugate(s_j), which implies (1.1). This proves 2 to 3.

## 4. Research boundary and attribution

The equivalence concerns existence of a suitably chosen companion and
spectral labelling. It does not assert that an arbitrary fixed companion
allows those signs. The genuine fixed-companion obstruction in
[the matching criterion](fixed-companion-witness.md) remains consistent
with this result.

It also does not prove that every complete-companion H satisfies (1.1).
Assuming the extra symmetry for all relevant H would require a substantive
circulantization theorem. The finite phase test makes that extra requirement
explicit; it does not discharge it.

For four circulant blocks C(a),C(b),C(c),C(e), write pa,pb,pc,pe for products
of their first-column phases. The first balanced character vanishes iff
pa pe+pb pc=0; either first-character zero then forces both cubic zeros.
In the canonical array [A B;B* -A*], this identity is immediate, with the
two terms -1 and 1. A subsequent [direct matrix proof](direct-circulant-character.md)
now proves the same identity for every displayed four-circulant raw Hadamard6,
covering all phase-retrieval branches and zero-mode degeneracies. It removes
the extra first-character assumption inside this symmetry branch, yielding
both first and cubic zeros at the fixed partitions. The complete written
phase-retrieval/rank proof remains distinct from its supporting Lean
character-formula interface and from general companion circulantization.

The complete-companion construction and its Fourier phase factorization
are prior results: [Szollosi, arXiv:0811.3930v2, Section 4](https://arxiv.org/pdf/0811.3930v2),
explicitly crediting Zauner, and [Matolcsi et al., Section 4, (4.3)-(4.5)](https://arxiv.org/pdf/2503.14752v2).
An order-(3,3) monomial automorphism obstruction is also present in
[Cardenes Wuttig and Tindall, Lemma S.20](https://arxiv.org/html/2608.18053v1).
The fixed-partition phase-gauge argument here uses standard linear algebra;
its historical originality is not established. External classification and
MUB exclusion claims are not imported as independently verified proofs.
