# The full Tate algebra of the finite resonant triangular module

Research note, 8 October 2026. This is a written mathematical proof.
It is not a Lean formalization. The construction and base calculations
used below are attributed in Section 8; historical novelty is unresolved.

## 1. The actual module and the statement

Use exactly the finite objects constructed in
[finite-resonant-realization.md](finite-resonant-realization.md):
a characteristic-two field k, an infinite-order element q, nonzero
h_1,h_2, the algebra A=(C(q) plus DC(q)) tensor_k (C(q) plus DC(q)),
its simple X, the fixed OpenAI target Y, its kernel bimodule F, and
the finite module Z over Lambda=[[A,0],[F,A]]. In particular, the target
is the fourfold cosyzygy of the specified two-cone cokernel. It is not
replaced by another bimodule having the same evaluated Hom dimensions.

Let r=h_1/h_2 have finite order d>1. In characteristic two d is odd:
an element of even minimal order would satisfy
(r^(d/2)-1)^2=r^d-1=0, contradicting minimality. Thus d>=3.
Let P_Z be the complete totally acyclic column cone from that construction.
Define the graded Tate algebra by its composition-compatible comparison

\[
 E^a=\widehat{\operatorname{Ext}}_\Lambda^a(Z,Z)
     =H^a\operatorname{End}^{\bullet}_\Lambda(P_Z),
 \qquad a\in\mathbb Z.                                      \tag{1}
\]

Equivalently the groups are computed by Hom(P_Z,Z). In positive degrees
they are ordinary Yoneda Ext. In degree zero they are stable
endomorphisms, modulo maps through projectives, rather than ordinary
endomorphisms.

Put S=k[x,y], with |x|=|y|=3, and write S_m for ordinary polynomial
degree m. Set

\[
 R=\bigoplus_{n\ge0}S_{nd},\qquad R_+=\bigoplus_{n\ge1}S_{nd},
 \qquad
 M=\bigoplus_{j\ge1}D S_{jd-2},\quad
 |D S_{jd-2}|=5-3jd,                                      \tag{2}
\]

where D denotes k-linear duality. Give M its two identical R-actions
by dual polynomial contraction. For a monomial a=x^alpha y^beta
in S_{nd}, and a dual basis element m_(u,v) of D S_(jd-2), this means

\[
 a\,m_{u,v}=m_{u,v}\,a=
 \begin{cases}
 m_{u-\alpha,v-\beta}&u\ge\alpha,\ v\ge\beta,\\
 0&\text{otherwise}.
 \end{cases}                                               \tag{3}
\]

A nonzero result has index j-n>=1. Scalars act as usual.
Let B=R plus M be the square-zero extension with M^2=0, and
let B_0=R_+ plus M be its augmentation ideal. Introduce a formal
symbol epsilon of degree one, and a vector omega of degree minus one.
Define

\[
 \mathcal B=(R\oplus M)\oplus\epsilon(R_+\oplus M)\oplus k\omega.
                                                               \tag{4}
\]

Multiplication on the first two summands is the subalgebra
B plus epsilon B_0 of B[epsilon]/(epsilon^2). Multiplication on
k omega is given by the scalar augmentation: omega^2=0, and omega
annihilates R_+, M, epsilon R_+, and epsilon M on both sides.
This defines an associative unital graded algebra. There is no
standalone epsilon: it is absent because B_0 has no scalar term.

**Theorem.** For the actual finite module Z above and d>1, there is
an isomorphism of unital graded k-algebras

\[
 \widehat{\operatorname{Ext}}_\Lambda^*(Z,Z)\cong\mathcal B. \tag{5}
\]

In particular E^0=k is the stable scalar identity and E^-1=k omega.
The theorem determines every integer degree and every product. It
does not determine the entire ordinary End_Lambda(Z), does not
treat d=1, and does not assert a complete Lean certificate.

## 2. The ambient stable algebra and both contraction actions

Write H^a=stable Hom_A(X,X[a]). The base calculation and symmetric
stable duality give

\[
 H^{3m}=S_m,\qquad H^{-3m-1}=D S_m\quad(m\ge0),              \tag{6}
\]

with all other groups zero. Choose a nonzero trace functional
lambda:H^-1 -> k, and identify beta in H^(-3m-1) with
the functional a -> lambda(a beta) on S_m. The perfect composition
pairing makes this an isomorphism. Its naturality and associativity
identify left multiplication by a positive polynomial with contraction.
If its polynomial degree exceeds m, the target has no support and the
product is zero. Negative times negative is zero by (6).

The right contraction agrees with the left contraction here; this
does not follow merely from the dimension profile. The selected
classes x,y are evaluations of the actual bimodule comparison maps
p_1,p_2 in the pinned OpenAI construction. Each such bimodule class
is a bimodule derived morphism A -> A[3]. Derived tensor evaluation
therefore induces a natural transformation Id -> [3].
It descends to the stable A-category: on projective modules the
evaluated positive extension class is zero stably, and the exact
projective-cover and cosyzygy sequences give its shift comparisons.
Tensor evaluation and its shift comparisons commute with stable maps:
for u:L -> N[a], naturality says

\[
 p_i(N)[a]\,u=u[3]\,p_i(L).                                \tag{7}
\]

These identities can be checked on projective resolutions; choices
of the lifts differ by homotopy. Naturality with the connecting
map N -> Omega N[1] identifies the action on Omega N with the
shifted action on N. Iterating projective covers and cosyzygies
therefore gives compatibility with every integer shift. The usual
shift sign is one in characteristic two.
Taking L=N=X proves that x,y commute with every class of H,
including its negative degrees. Their polynomial products do so
as well. Hence (3) describes both actions, rather than one chosen
action on a vector space of the right dimension.

## 3. The negative twist weight

For any h!=0, the tensor functor U_h=A_(h_h tensor h_h) fixes X.
The right-twist convention gives inverse restriction, so its action
on H^(3m) is h^-m, as in the positive realization note. In negative
degrees its action is

\[
 U_h|_{H^{-3m-1}}=h^{m+2}.                                \tag{8}
\]

For completeness, the extra two in (8) has an actual stable origin.
Let p=f tensor f and zeta=f^* tensor f^* in the projective cover Ap
of X. The socle map X -> rad(A)p=Omega X, 1 -> zeta, represents a
nonzero H^-1 class. Every map X -> A lands in the left socle. By
symmetry that socle is also annihilated on the right by rad(A).
Every map A -> rad(A)p is right multiplication by a radical element
and kills this socle. The same holds for finite sums and summands,
so the displayed map cannot factor through a projective.

Comparison of the twisted projective cover by h_h tensor h_h
sends zeta to h^2 zeta. It therefore acts on H^-1 by h^2.
For a in S_m and beta in D S_m, preservation of composition gives

\[
 h^{-m}\lambda\bigl(a\,U_h(\beta)\bigr)
   =\lambda\bigl(U_h(a\beta)\bigr)
   =h^2\lambda(a\beta).
\]

Nondegeneracy of the pairing forces (8) on the entire dual piece.
This is the characteristic-two case of Tang's Lemma 4.3; its fixed
involution is the identity in this characteristic. Only this base
weight calculation is used from that lemma, not a change of target Y.

## 4. All branch groups, including the exceptional degrees

Let V^a=stable Hom_A(X,FX[a]) and W^a=stable Hom_A(X,YX[a]).
The fixed target has W^-3=W^0=k and all other W groups zero.
The actual finite kernel projections rho_i:F -> U_(h_i) give
the exact sequence

\[
 (H^{a-1})^2\longrightarrow W^{a-1}\longrightarrow V^a
 \xrightarrow{(p_1^a,p_2^a)}(H^a)^2\longrightarrow W^a.     \tag{9}
\]

The positive profile and V^0=kv have already been proved in the
realization note. At a=-3, W^-4=0 and H^-3=0, so V^-3=0;
the nonzero preceding group (H^-4)^2 maps into W^-4=0.
At a=-2, the preceding H^-3 and following H^-2 vanish, giving
V^-2=W^-3=k. At a=-1, both adjoining W groups vanish, and
V^-1=(H^-1)^2. For a<=-4 both adjoining W groups vanish as well.
Altogether

\[
 V^{-3}=0,\quad V^{-2}=k,\quad V^{-1}=(H^{-1})^2,\quad
 V^0=kv,\quad V^1=0,\qquad
 V^a=(H^a)^2\ (a\le-4\text{ or }a\ge1).                    \tag{10}
\]

In the last expression the a=1 isomorphism is between zero spaces.

The projections are induced by actual bimodule maps between exact
tensor functors preserving projectives. Their naturality and shift
compatibility give, for every integer degree and arbitrary u in V,

\[
 p_i\bigl(F(a)u\bigr)=U_{h_i}(a)p_i(u),\qquad
 p_i(ub)=p_i(u)b.                                         \tag{11}
\]

Thus the negative actions have the weights in (8), on every class,
and the other action is ordinary composition in H. This is the
same complete-resolution comparison as in positive degrees.

Since p_i(v)=1, the cone connecting map
delta^a(g,j)=F(g)v+v[a]j has matrices

\[
 \delta^{3m}(g,j)=(h_1^{-m}g+j,h_2^{-m}g+j)\quad(m\ge1),
 \qquad
 \delta^{-3m-1}(g,j)=(h_1^{m+2}g+j,h_2^{m+2}g+j)\quad(m\ge0).
                                                               \tag{12}
\]

Also delta^0(c,e)=(c+e)v. At a=-2 its source is zero and its
target is k; at a=-3 both source and target are zero. In particular
delta^-1 is invertible because r^2!=1 when d>=3.

## 5. The full support and the unique diagonal sections

The actual cone endomorphism DG algebra has one off-diagonal DG
ideal I, with I^2=0; the opposite block vanishes as an ordinary
Hom complex. Its diagonal quotient gives, in every integer degree,

\[
 0\longrightarrow\operatorname{coker}\delta^{a-1}
 \longrightarrow E^a\xrightarrow{\pi}\ker\delta^a
 \longrightarrow0.                                      \tag{13}
\]

The map pi is multiplicative. Its kernel J consists of classes
represented by closed elements of I, so J^2=0 strictly by block
multiplication.

Put L=3d. Positive matrices resonate exactly at polynomial degree
nd. Negative matrices resonate exactly when d divides m+2,
that is m=jd-2 for j>=1. Equations (10)-(13) therefore give

| Degree | Space |
| --- | --- |
| 0 | k, the stable identity |
| -1 | k omega, from coker delta^-2 |
| Ln, n>=1 | S_(nd) |
| Ln+1, n>=1 | S_(nd), an off-diagonal class |
| 5-Lj, j>=1 | D S_(jd-2) |
| 6-Lj, j>=1 | D S_(jd-2), an off-diagonal class |
| Every other integer | 0 |

In particular E^-2=0. At degree zero coker delta^-1=0 and
ker delta^0 is the scalar diagonal, so there is no additional
stable degree-zero summand.

For a in S_(nd), let D_n(a) be the unique lift under pi of
(a,h_1^(-nd)a). For beta in D S_(jd-2), let N_j(beta) be the
unique lift of (beta,h_1^(jd)beta). Uniqueness follows because
J is zero in each of their degrees. The stable identity is the
unique lift of (1,1).

Multiplicativity of pi forces the positive products to be those
of R. For a positive and a negative diagonal lift, (3), (8) and
the character identity
h_1^(-nd)h_1^(jd)=h_1^((j-n)d)
give the contraction coordinates whenever j>n. The target lift
is again unique. When j<=n the total degree is 5+L(n-j)>0,
which is not a positive support degree, and the product is zero.
This proves both mixed diagonal actions.

Products of two negative diagonal lifts are zero in E, including
possible terms invisible under pi. Their total degree is
10-L(j+l)<=-8. It cannot equal 5-Lt or 6-Lt, since the differences
are respectively 5 and 4, smaller than L. It cannot be -1 since
L(j+l)>=18. There is no supported target. These facts prove that
the unique diagonal lifts give an actual algebra copy of R plus M.

## 6. The off-diagonal normalization and every remaining product

At each resonant degree, (12) has diagonal image, so its cokernel
is identified with the corresponding polynomial or dual piece by
(w_1,w_2) -> w_1+w_2. Write w for this raw cokernel coordinate.
Use the following normalizations:

\[
 J^{Ln+1}\longrightarrow\epsilon S_{nd},
       \quad w\longmapsto\epsilon h_1^{nd}w,
 \qquad
 J^{6-Lj}\longrightarrow\epsilon D S_{jd-2},
       \quad w\longmapsto\epsilon h_1^{-jd}w.               \tag{14}
\]

Both are invertible. There is no rescaling of the negative diagonal
coordinates N_j(beta) in Section 5.

Actual block multiplication, followed by (11), gives the following
raw actions on either side. A positive diagonal D_n(a) acts by
h_1^(-nd)a; a negative diagonal N_j(beta) acts by h_1^(jd)beta.
The second diagonal block has exactly the same character as the
twisted first block at resonance. Consequently both left and right
actions agree, using the centrality and contraction proved in
Section 2. Off-diagonal corrections in the diagonal lifts do not
contribute, because I^2=0.

For two positive indices, (14) changes the raw factor h_1^(-nd)
into ordinary polynomial multiplication, just as in the positive
Yoneda theorem. For a positive diagonal and a negative raw cross
class with j>n, the output negative index is j-n, and

\[
 h_1^{-(j-n)d}h_1^{-nd}a w=h_1^{-jd}a w.
                                                               \tag{15}
\]

This is precisely a times the normalized epsilon M_j class.
For a negative diagonal and a positive cross class, the raw
positive coordinate for epsilon a is h_1^(-nd)a. Therefore

\[
 h_1^{-(j-n)d}h_1^{jd}\beta\,h_1^{-nd}a=\beta a.            \tag{16}
\]

This gives epsilon times the same contraction, in either order.
When j<=n these mixed products have degree 6+L(n-j), outside
positive support, and vanish. All products involving two
off-diagonal classes vanish by J^2=0.

A negative diagonal times a negative cross class has degree
11-L(j+l)<=-7. It cannot be 5-Lt or 6-Lt, because the differences
are 6 and 5, less than L, and cannot be -1 because L(j+l)>=18.
Hence it is zero. Notice the necessary sign restriction: for d=3
the residue of a product of two negative diagonals equals a
positive cross residue, but its degree is negative.

There are no hidden mixed products into degrees -1 or zero.
The three types of positive-negative products have residues
5,6,7 modulo L. Since L>=9, none is 0 or -1 modulo L.
This also explains why the exceptional seam cannot be ignored
when d=1.

Finally omega is in J, as the image of V^-2 under the cross
connecting map. Products omega times epsilon R_+ or epsilon M
are therefore zero by J^2=0, in both orders. Their degrees can
have supported targets; degree support alone would not prove
these vanishings. Products of omega with positive diagonals
have degree Ln-1, outside positive support. Products with
negative diagonals have degree 4-Lj, outside negative support.
Also omega^2 lies in E^-2=0. Scalars act identically.

We have determined all products between the summands of (4),
with the actual stable identity as unit. This proves (5).

## 7. Local cohomology interpretation and an exact example

The negative diagonal module M has the usual local cohomology
description for the Veronese ring, with an explicit grading change.
Let f=x^d and g=y^d in R. Their ideal has radical R_+:
each monomial of degree d has a power in (f,g). The Cech quotient is

\[
 H^2_{R_+}(R)=R_{fg}/(R_f+R_g).                            \tag{17}
\]

It has basis [x^-a y^-b] for a,b>=1 with a+b divisible by d.
Indeed localization gives Laurent monomials with total exponent
divisible by d. The two submodules remove exactly those with
at least one nonnegative exponent. Each monomial with both
exponents negative can be obtained by taking sufficiently large
powers of f,g as denominator. Thus the explicit identification

\[
 (x^u y^v)^*\longmapsto[x^{-u-1}y^{-v-1}]
 \quad(u+v=jd-2)                                        \tag{18}
\]

is a bijection onto the ordinary polynomial degree -jd part
of (17). Multiplication is exactly (3). Multiplying that grading
by three and adding five gives the grading of M in (2).
This is the classical local cohomology model, not a new duality method.

Take k=F_4(t), q=t, h_1=zeta, h_2=1 with zeta^2+zeta+1=0.
Then d=3. The first negative diagonal and cross groups are
E^-4 and E^-3, each of dimension two. There are also E^-1=k
and E^0=k. The first positive groups are E^9 and E^10, each
of dimension four. Generally
dim M_j=jd-1 and dim S_(nd)=nd+1.
These are exact consequences of the theorem, not computed certificates.

## 8. Provenance and the omitted order-one seam

The finite Y,F,Lambda,Z and its totally acyclic cone are the same
OpenAI construction at commit
adc7f1241b42e322a6451854ab7e4b4c146bf78a, reconstructed over the
chosen field in the [finite realization note](finite-resonant-realization.md).
The full cone comparison and DG block sequence are in
[the pinned conversion source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-counterexample-to-the-Auslander-Reiten-conjecture-September-23-2026/build/02-conversion.tex).
The bimodule comparison representatives are in 03-algebra.tex,
label coc:comparison. The ambient polynomial algebra, symmetric
stable duality and negative contraction are in its 04-resolution.tex
and 05-cones.tex.
The branch maps are those of 07-branches.tex.

Qiyue Tang, [A note on counterexamples to homological conjectures,
Hexagon 2610.00143v1](https://hexagonmath.org/pdf/2610.00143v1),
Proposition 4.2 and Lemma 4.3, gives the ambient stable profile and
the negative weight m+2 used here. These are prior results.
Its different derived-induction target is not used as the fixed Y.

Square-zero negative Tate extensions under symmetric duality and a
central regular sequence are classical; see Bergh, Jorgensen and
Oppermann, [The negative side of cohomology for Calabi-Yau categories](https://arxiv.org/abs/1208.5785),
Theorem 3.5. The final triangular Lambda here is not assumed symmetric,
so that theorem is not being applied to it. Veronese and trivial-extension
patterns also occur in the general Auslander-Yoneda constructions
described in Changchang Xi,
[Derived equivalences of algebras](https://www.wemath.cn/~ccxi/Papers/Articles/Xi-2018-BLMS.pdf),
Section 4.3. This note computes the actual resonant triangular module's
full algebra; it does not claim those general constructions are new,
or that a global literature search has established originality.

If d=1, delta^-1 is no longer invertible. The seam then has an
additional diagonal degree-minus-one class and a cross degree-zero
class. Their products can land in the exceptional omega line.
The branch projections and ordinary degree support do not determine
those secondary products. They require further actual cone
representatives or nullhomotopies. Formula (5) is not asserted in
that case. The whole construction and this full Tate theorem also
remain unformalized in Lean; the previously compiled lower-algebra
and low-degree Yoneda proofs retain their separate stated scope.
