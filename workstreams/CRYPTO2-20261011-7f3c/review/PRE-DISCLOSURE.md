# Independent reconstruction before disclosure of the candidate proof

Reviewer scope: the candidate universal mathematical assertion only, together with its source attribution and nontriviality conventions. This document was completed before opening the discoverer's `PROOF.md` or any constructor/checker code. The reviewer did read the original Kumar–Yadav–Samanta source (including its proofs) and original Daemen–Rijmen text. Thus this is an independent reconstruction relative to the discoverer's proof, not a claim of independent discovery from no literature.

## Statement reconstructed

For every field K of characteristic 2, every integer n >= 3, and every invertible n-by-n right circulant M over K, there are u,v in K^n with u != 0, v != 0, u != v such that at every input and output coordinate one of the two entries is zero or the two entries are equal. Invertibility also makes Mu,Mv nonzero and unequal.

My reconstruction proves this statement. It uses only finite-dimensional linear algebra, so K need not be finite or perfect.

## 1. Non-MDS fallback, with its precise hypothesis

Use “MDS” to mean that all square submatrices are nonsingular. Let M be invertible and non-MDS. There are equally sized index sets I,J of cardinality r with 1 <= r < n for which A = M[I,J] is singular. Choose nonzero x in ker A, and let u be x on J and zero on J-complement. Then Mu vanishes on I, and (Mu)[I-complement] is nonzero because M is invertible.

Put D = M[I-complement,J-complement]. If D is singular, choose nonzero y in ker D. If D is nonsingular, choose y = D^{-1}(Mu)[I-complement], which is nonzero. Let v be y on J-complement and zero on J. Thus u,v are nonzero with disjoint supports, hence unequal and coordinatewise related. In the singular-D case their output supports are disjoint. In the nonsingular-D case their outputs agree on I-complement and Mu is zero on I. Both cases give the asserted relation.

The invertibility of M is essential to the stated proof of nonzero y in the second case. I do not import the original source's blanket statement about every square non-MDS matrix without this check. In particular, under the original convention excluding the zero output difference, a zero linear map is an immediate obstruction to such a blanket singular-matrix statement.

## 2. Odd symmetric invertible matrices

Let n = 2k+1 >= 3 and let S be symmetric invertible. If it is non-MDS, use section 1. Otherwise split the coordinates as L, c, R, with |L|=|R|=k, and write

    S = [ A    a     B ]
        [ a^T  alpha b^T ]
        [ B^T  b     C ].

Here B is nonsingular, since S is MDS. Define

    x = (B^T)^{-1} b,    y = B^{-1} a,
    u = (x,1,0),         v = (0,1,y).

Characteristic 2 gives (Su)[R] = B^T x + b = 0 and (Sv)[L] = a + B y = 0. Their c coordinates agree because

    a^T x = a^T (B^T)^{-1} b = b^T B^{-1} a = b^T y.

The inputs are related: disjoint outside c and equal at c. The outputs are related by the stated zero supports and equal central coordinate. Both u,v have a central 1. Moreover a and b are nonzero (indeed all their entries are nonzero in an MDS matrix and k>=1), so x,y are nonzero. Thus u != v.

This explicitly verifies the nontriviality that is not automatic from merely finding a nonzero solution of an odd alternating linear system. It also avoids the characteristic-2 pitfall that “skew-symmetric” without the zero-diagonal condition does not imply the usual odd-order determinant conclusion.

## 3. Odd circulants

Index from 0, with M_ij = a_(j-i mod n). Let P invert row indices: (Pz)_i = z_(-i mod n). Then S=PM satisfies S_ij=a_(i+j mod n), hence is symmetric and invertible. Apply section 2 for odd n>=3. A common output permutation preserves the coordinatewise relation, so the same input pair works for M. No preservation of MDS under any quotient has been assumed.

## 4. Order four base case

For the right circulant with first row (a,b,c,d), if both (a,c) and (b,d) are nonzero pairs, choose

    u=(a,0,c,0),    v=(0,d,0,b).

Direct multiplication gives

    Mu=(a^2+c^2, ad+bc, 0, ab+cd),
    Mv=(0, ad+bc, d^2+b^2, ab+cd).

These vectors are related, while u and v are nonzero and have disjoint supports. If either parity pair (a,c) or (b,d) is identically zero, take u=e_0,v=e_1. Their images are supported on opposite parities, so this also works. Invertibility guarantees nonzero output differences. Thus the order-four base case needs no MDS assumption.

## 5. Restriction to period-d vectors

Let d divide n, and let T:K^d -> K^n repeat coordinates: (Tx)_i=x_(i mod d). T is injective. Define

    b_r = sum_{0 <= t < n/d} a_(r+td),   0 <= r < d,
    C_ij = b_(j-i mod d).

Directly grouping j by residue modulo d proves M T = T C. In particular, if Cx=0, then MTx=0; invertibility of M implies Tx=0 and then x=0. Thus C is invertible. This is a restriction to the invariant periodic subspace. It is not the invalid assertion that arbitrary compression preserves invertibility, and it requires no averaging or division by n/d. In particular the characteristic-2 case n/d=2 is harmless.

If p,q witness the property for C, then Tp,Tq witness it for M. The repetition preserves nonzero vectors, inequality, and every coordinatewise relation on inputs and outputs.

## 6. Complete case split

* n odd: section 3.
* 4 divides n: use d=4 in section 5 and section 4.
* n = 2 mod 4: use d=n/2, which is odd and >=3 since n>=3 excludes n=2; sections 3 and 5 apply.

This proves the universal statement, including every formerly excluded n = +2 or -2 modulo 12 with n>=3. It does not prove anything at order 2. The d=n/2 reduction there reaches d=1, outside the valid odd base case. MDS order-2 examples do avoid nontrivial related differentials.

## Source and nontriviality checks

Primary source: Yogesh Kumar, Akshay Ankush Yadav, Susanta Samanta, *Analyzing Linear Layers in Related-Differential Cryptanalysis*, arXiv:2605.27535v1 (26 May 2026), https://arxiv.org/abs/2605.27535v1 and https://arxiv.org/html/2605.27535v1.

* Definitions 1 and 2 give the coordinatewise polynomial relation and input/output relation. As printed, these definitions do not explicitly exclude zero vectors or identical pairs. Theorem 2 says “nontrivial,” and the surrounding problem must be read with the older convention; otherwise every linear map admits the trivial pairs.
* Theorem 2 is the non-MDS source; Theorem 4 is the odd symmetric MDS source; Lemma 3 obtains odd circulants by output permutation; Theorem 5 covers n not congruent to +/-2 modulo 12. The source works over finite fields F_(2^m); the reconstruction above proves the stated extension to arbitrary characteristic-2 fields.
* Section VI says the results suggest a natural conjecture for the remaining unresolved circulant cases. I inspected both the full text and HTML: there is no fully quantified numbered conjecture in this version. The phrase occurs only in the concluding prose. Therefore the correct attribution is completion of the remaining cases indicated by the paper, not “proof of Conjecture X” or a verbatim fully quantified conjecture from the source.
* Original convention: Joan Daemen and Vincent Rijmen, *New criteria for linear maps in AES-like ciphers*, DOI https://doi.org/10.1007/s12095-008-0003-x, original local PDF and extracted text. Section 7.1, immediately after Definition 8, excludes the all-zero difference vector. Definition 9 imposes the related input and output conditions. Section 8.2 explicitly removes the codeword corresponding to the original differential; section 8.3 requires more than the two trivial binary codewords. Thus requiring u,v nonzero and distinct is substantively appropriate. Under invertibility this also excludes zero and identical output differentials.

No claim is made here about historical novelty, external peer review, Lean formalization, or a complete cipher attack.

## Independent finite checks before proof disclosure

`independent_check.py` was written from the reconstruction above without consulting the discoverer's code. It uses exact GF(4) and GF(16) arithmetic and checks the inputs and both output relations directly.

* Exhaustive coefficient lists only at n=3 and n=4 over GF(4): respectively 27 and 192 invertible circulants all passed (64 and 256 total coefficient lists).
* 24 independently seeded invertible samples each at n=6,8,10,14 over GF(4) all passed. The code also checks the intertwining identity columnwise for each period restriction.
* Symmetric Cauchy MDS matrices of orders 3 and 5 over GF(16), with entries 1/(8+i+j) in field notation, passed the direct MDS construction after every square minor was checked.

These checks are corroboration only; the universal proof is sections 1–6. Results are in `independent_check_results.json`.
