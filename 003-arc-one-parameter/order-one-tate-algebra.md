# Closing the order-one seam in the finite triangular Tate algebra

Research note, 8 October 2026. Written mathematics, not a Lean theorem.
The underlying finite construction and ambient algebra are prior inputs
identified in the two linked notes below. Historical novelty is unresolved.

## 1. Setup and complete statement

Use the same actual finite Y,F,Lambda,Z and complete resolution P_Z of
[finite-resonant-realization.md](finite-resonant-realization.md).
Here k has characteristic two, q has infinite order, and the two
nonzero twists are equal: h_1=h_2=h. Thus their ratio has order one.
No finite target or module is replaced. Define
E=H^* End_Lambda(P_Z), the actual full Tate algebra. Positive degrees
are ordinary self-Ext, and degree zero is stable End.

Put S=k[x,y], |x|=|y|=3, and let S_m denote polynomial degree m.
Let

\[
 M=\bigoplus_{m\ge0}D S_m,\qquad |D S_m|=-3m-1.              \tag{1}
\]

Both S-actions on M are dual polynomial contraction:
x m_(a,b)=m_(a-1,b) for a>0 and zero for a=0, and similarly
for y and on the right. Set B=S plus M with M^2=0, and its
augmentation ideal B_0=S_+ plus M. Define

\[
 \mathcal B_1=(S\oplus M)\oplus\epsilon(S_+\oplus M)\oplus k\omega,
 \quad |\epsilon|=1,\quad|\omega|=-1.                       \tag{2}
\]

Multiplication in B plus epsilon B_0 is induced from
B[epsilon]/(epsilon^2). The omega line is a square-zero ideal
on which only the scalar augmentation acts. Hence omega
annihilates every other non-scalar summand on both sides.
There is no standalone epsilon.

**Theorem.** For the actual equal-twist finite module,

\[
 \widehat{\operatorname{Ext}}_\Lambda^*(Z,Z)\cong\mathcal B_1
                                                               \tag{3}
\]

as unital graded k-algebras. In particular

\[
 E^0=k\,1\oplus k\rho,\quad \rho=\epsilon m_{0,0},\quad\rho^2=0,
 \qquad E^{-1}=k\,m_{0,0}\oplus k\omega.                    \tag{4}
\]

Thus the stable degree-zero algebra is the dual numbers. It is not
the entire ordinary End_Lambda(Z).

Together with [the order-greater-than-one calculation](finite-resonant-tate-algebra.md),
this gives a uniform description for every finite ratio order d.
Namely R=S^(d), and replace M by

\[
 M_d=\bigoplus_{\substack{m\ge0\\d\mid m+2}}D S_m,
       \qquad |D S_m|=-3m-1.                               \tag{5}
\]

The full algebra is (R plus M_d) plus epsilon(R_+ plus M_d)
plus k omega with the same multiplication rules. Formula (5)
has a degree-minus-one term exactly when d=1, since finite
orders in characteristic two are odd. This explains the additional
degree-zero dual-number class in (4).

**Infinite-order corollary.** If the ratio r instead has infinite
order, the same actual finite construction has
E=k plus k omega, with |omega|=-1 and omega^2=0. Indeed every
positive and negative matrix in (6), with its two distinct twist
weights restored, is invertible: r^n!=1 for n>=1 and r^(m+2)!=1
for m>=0. Sequence (7) leaves only the scalar kernel of delta^0
and the exceptional coker delta^-2. The actual off-diagonal ideal
gives omega^2=0. This uses the arbitrary-twist calculation preceding
the equal-twist specialization and completes the parameter cases.

## 2. The actual exact sequence and the seam

The ambient algebra H has H^(3m)=S_m and H^(-3m-1)=D S_m,
for m>=0, with all other degrees zero. Both mixed actions are
contraction. The actual functor U_h acts by h^-m on S_m and
by h^(m+2) on D S_m. These base facts and their proof are
Sections 2-3 of the order-greater-than-one note; they did not
use d>1. The actual branch profile, also independent of ratio order,
has V^-3=0, V^-2=k, V^-1=(H^-1)^2, V^0=kv and V^1=0.
All other nonzero V groups are the two actual H branches.

For equal twists each connecting matrix has diagonal image:

\[
 \delta^{3n}(a,b)=(h^{-n}a+b,h^{-n}a+b)\quad(n\ge1),\qquad
 \delta^{-3m-1}(a,b)=(h^{m+2}a+b,h^{m+2}a+b)\quad(m\ge0).
                                                               \tag{6}
\]

Also delta^0 is the onto scalar-sum row, and delta^-2:0 -> k.
The actual cone projection gives

\[
 0\to J^a=\operatorname{coker}\delta^{a-1}
 \to E^a\xrightarrow{\pi}\ker\delta^a\to0.                 \tag{7}
\]

Here J is the image of the actual single off-diagonal DG ideal I.
Consequently pi is multiplicative and J^2=0.

| Part | Degree | Actual space or diagonal image |
| --- | --- | --- |
| Scalar identity | 0 | maps to (1,1) |
| Positive diagonal, n>=1 | 3n | (a,h^-n a), a in S_n |
| Positive cross, n>=1 | 3n+1 | J^(3n+1)=S_n |
| Negative diagonal, m>=0 | -3m-1 | (beta,h^(m+2) beta), beta in D S_m |
| Negative cross, m>=0 | -3m | J^(-3m)=D S_m |
| Exceptional cross | -1 | k omega, from coker delta^-2 |

There are no other groups. At m=0 the negative cross is rho in
degree zero; the actual stable identity splits its scalar diagonal.
At negative diagonal degree minus one, J contributes omega, so pi
has no unique lift. This is the seam that the preceding proof excluded.
We now construct a coherent lift directly in the actual algebra.

## 3. The height-two construction of the bottom negative lift

For a+b>=1 let b_(a,b) be the unique E^(-3(a+b)-1) lift of

\[
 (m_{a,b},h^{a+b+2}m_{a,b}).                               \tag{8}
\]

Uniqueness holds because J is zero at these negative diagonal degrees.
Use x,y also for their unique positive diagonal lifts, with coordinates
(x,h^-1 x) and (y,h^-1 y). They generate an actual polynomial
subalgebra: pi is multiplicative and J vanishes at every positive
diagonal degree. In particular xy=yx.

Contraction and the matching characters in (8) force

\[
 x b_{2,0}=b_{2,0}x=b_{1,0},\qquad
 y b_{0,2}=b_{0,2}y=b_{0,1},                              \tag{9}
\]
\[
 x b_{1,1}=b_{1,1}x=b_{0,1},\qquad
 y b_{1,1}=b_{1,1}y=b_{1,0}.                             \tag{10}
\]

Their targets have degree minus four and are unique lifts.
The symbols b_(2,0), b_(1,1), b_(0,2) are lifts of dual monomials,
not Yoneda squares of the degree-minus-four classes.

Define eta=x b_(1,0). Associativity and (9) give

\[
 x b_{1,0}=x(b_{2,0}x)=(x b_{2,0})x=b_{1,0}x.
                                                               \tag{11}
\]

Similarly y b_(0,1)=b_(0,1)y. Equations (10) and xy=yx give

\[
 x b_{1,0}=x(y b_{1,1})
          =y(x b_{1,1})=y b_{0,1}.                        \tag{12}
\]

Thus all four bottom contractions agree with eta. Its diagonal
image is (m_(0,0),h^2 m_(0,0)), so eta and omega are independent.

The four zero bottom contractions do not acquire an omega term.
For example b_(0,1)=y b_(0,2), while x b_(0,2)=0: its diagonal
contraction is zero and its degree-minus-four target has no J.
Therefore

\[
 x b_{0,1}=y(x b_{0,2})=0,\qquad
 b_{0,1}x=(b_{0,2}x)y=0.                                \tag{13}
\]

The two products y b_(1,0) and b_(1,0)y vanish by the symmetric
argument using b_(2,0).

Send m_(0,0) to eta and every m_(a,b) of positive total index to
b_(a,b). For total index at least two, the generator contractions
on both sides follow from unique lifting. At index one they are
(11)-(13). At index zero x eta, eta x, y eta and eta y have
degree two, whose E group is zero. Hence this gives one and the
same two-sided S-linear lift s:M -> E. No independent choice of
left and right splittings is being assumed.

Products of two lifted M classes have negative degree congruent to
one modulo three, where E is zero. Thus s(M)^2=0, and the actual
stable identity, polynomial lifts and s form a multiplicative
copy of S plus M. This closes the formerly ambiguous diagonal seam
without assuming a DG diagonal splitting.

## 4. All cross products, including the degree-zero cross

Use the branch sum w=w_1+w_2 as the raw cokernel coordinate in (6).
Normalize it by

\[
 J^{3n+1}\to\epsilon S_n,\quad w\mapsto\epsilon h^n w
       \quad(n\ge1),\qquad
 J^{-3m}\to\epsilon D S_m,\quad
       w\mapsto\epsilon h^{-(m+2)}w\quad(m\ge0).           \tag{14}
\]

The m=0 normalization defines rho as the class corresponding to
epsilon m_(0,0). The class eta chosen above has exactly the
diagonal coordinates required by this identification.

Actual block multiplication and naturality of the two kernel
projections give raw left and right factors h^-n a for a positive
diagonal a in S_n, and h^(m+2) beta for a negative diagonal beta
in D S_m. The second diagonal coordinate gives the same factor
on the other side. An off-diagonal component of a lift contributes
nothing because I^2=0.

Positive diagonal times positive cross is ordinary polynomial
multiplication after (14). For positive diagonal a in S_n acting
on a negative raw cross w in D S_m, if m>=n its output has
dual index m-n and

\[
 h^{-(m-n+2)}h^{-n}a w=h^{-(m+2)}a w.                    \tag{15}
\]

This is exactly the normalized dual contraction, including m=n
and its output rho in degree zero. For negative diagonal beta
of dual index m acting on a positive raw cross w in S_n,

\[
 h^{-(m-n+2)}h^{m+2}\beta w=h^n\beta w\quad(m\ge n).
                                                               \tag{16}
\]

It gives the other mixed contraction in either order.

If n>m, either of these mixed products has degree 3(n-m).
There is a positive diagonal E group there, so degree support
alone does not prove vanishing. Instead the product belongs to
the ideal J, and J^(3(n-m))=0. Hence it vanishes.
All products of two cross classes, including rho and omega,
are zero by J^2=0.

It remains to check a negative diagonal of index m times a negative
cross of index l. The product is in J and has degree
-3(m+l)-1. Unless m=l=0, that J group is zero, even though E
has a negative diagonal group there. At m=l=0 the two products
eta rho and rho eta may land in the omega line and require more.
Since rho is in J^0 and x is diagonal of degree three,

\[
 \rho x=x\rho=0\quad\text{in }J^3=0.
\]

Using the actual equalities eta=x b_(1,0)=b_(1,0)x,

\[
 \rho\eta=(\rho x)b_{1,0}=0,\qquad
 \eta\rho=b_{1,0}(x\rho)=0.                              \tag{17}
\]

Thus the exceptional secondary products vanish by actual
associativity and the DG ideal, rather than an unsupported
assumption about the branch projections.

## 5. Omega, completeness, and provenance

Omega lies in J, so it annihilates every cross class by J^2=0.
Its products with positive diagonals have positive degree 3n-1,
outside E support. Its products with M have negative degree
-3m-2, also outside support. Omega^2 is zero and the scalar
identity acts normally. All products between the summands of (2)
have now been determined, proving (3) and (4).

No giant matrix enumeration, new cochain search or numerical
calculation is used. The additional argument is the explicit
height-two lift (9)-(13), its two-sided consistency from
associativity, and the seam product (17). The complete-resolution
comparison, actual DG ideal, same finite object, ambient duality
and both twist weights are the prior inputs already proved and
attributed in [the finite construction](finite-resonant-realization.md)
and [the Tate note](finite-resonant-tate-algebra.md).
In particular the weight m+2 is the characteristic-two case of
Qiyue Tang's [Lemma 4.3](https://hexagonmath.org/pdf/2610.00143v1).
The equal-twist theorem does not transfer a map from Tang's
different finite target into the OpenAI target.

The degree-zero ring computed here is stable. Its ordinary
projective-factorization ideal is not computed. The finite-ratio
module has positive self-extensions and is not an ARC counterexample.
The whole finite construction and the full Tate family are still
unformalized in Lean. Independent written agent readings do not
amount to a machine certificate, journal peer review or a global
literature-priority determination.
