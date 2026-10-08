# The positive Yoneda algebra at a finite twist resonance

Research note, 8 October 2026.

This note determines multiplication, rather than only dimensions, under
explicit polynomial and bimodule action hypotheses in the triangular
conversion setup of [paper.md](paper.md). Its application to the concrete
ARC construction remains conditional on that setup being realized. This
is a written proof, not a Lean theorem or a verification of the complete
ARC construction. Historical novelty has not been established.

## 1. Setup and the additional multiplicative hypotheses

Use the characteristic-two field k, symmetric finite-dimensional algebra
A, side-projective bimodule F, module X, stable map v and actual finite
triangular module Z of Lemma 2 in [paper.md](paper.md). Let P_Z be its
complete cone resolution constructed there, and put

\[
 E^a=H^a\operatorname{End}^{\bullet}(P_Z),\quad
 H^a=\underline{\operatorname{Hom}}_A(X,X[a]),\quad
 V^a=\underline{\operatorname{Hom}}_A(X,FX[a]).
\]

The comparison in that lemma respects multiplication and identifies
E^a with actual Ext_Lambda^a(Z,Z) for a>0. Its block sequence gives

\[
 0\longrightarrow\operatorname{coker}\delta^{a-1}
 \longrightarrow E^a\xrightarrow{\pi}\ker\delta^a
 \longrightarrow0,\qquad
 \delta^a(g,j)=F(g)v+v[a]j. \tag{1}
\]

Assume all the following, beyond merely the dimension hypotheses of
Theorem 3 in that note:

1. The nonnegative algebra H is S=k[x,y], with |x|=|y|=3.
   Write S_m for the homogeneous polynomials of ordinary degree m,
   so H^(3m)=S_m. All other positive H degrees vanish.
2. V^0=kv and delta^0(c,d)=(c+d)v. In positive degrees V vanishes
   outside multiples of three. For every m>=1 there are specified
   branch coordinates V^(3m) -> S_m plus S_m, which form an isomorphism.
   For nonzero h_1,h_2 in k, these coordinates give

\[
 \delta^{3m}(g,j)=(h_1^{-m}g+j,h_2^{-m}g+j). \tag{2}
\]

3. The coordinates respect both graded actions, not just (2).
   For a in S_n, w in V^(3m), n,m>=1, left postcomposition by F(a)
   acts on branch i by multiplication by h_i^(-n)*a.
   Right precomposition by b in S_n acts on each branch by multiplication
   by b. These are the actions induced by the actual diagonal blocks of
   End(P_Z); they are not additional actions chosen after taking dimensions.

In particular, hypothesis 3 must be proved by naturality in an intended
application. The scalar matrix (2) alone does not establish it.

Let r=h_1/h_2 and let d be its multiplicative order. If d is finite,
define the Veronese subalgebra, with its actual cohomological grading,

\[
 R=S^{(d)}=\bigoplus_{j\ge0}S_{jd},\qquad
 R_+=\bigoplus_{j\ge1}S_{jd},\qquad |S_{jd}|=3jd.
\]

Here R_+ is the positive-degree ideal. Introduce a formal symbol epsilon
of degree one with epsilon^2=0. The algebra

\[
 R\oplus\epsilon R_+\ \subseteq\ R[\epsilon]/(\epsilon^2) \tag{3}
\]

consists of a+epsilon*b with a in R and b in R_+. Its multiplication is
(a+epsilon*b)(c+epsilon*e)=ac+epsilon*(ae+bc). It does not contain
epsilon by itself: there is no constant term in its epsilon summand.

## 2. The multiplicative conclusion

**Theorem.** Under hypotheses 1-3, if d is finite, there is an isomorphism
of graded nonunital k-algebras

\[
 \bigoplus_{a>0}\operatorname{Ext}^a_\Lambda(Z,Z)
 \ \cong\ R_+\oplus\epsilon R_+. \tag{4}
\]

On adjoining the actual scalar identity of Z, it extends to an
isomorphism of unital graded k-algebras

\[
 k\,1_Z\oplus\bigoplus_{a>0}\operatorname{Ext}^a_\Lambda(Z,Z)
 \ \cong\ R\oplus\epsilon R_+. \tag{5}
\]

The degree-zero part on the left of (5) is specifically the scalar
endomorphisms, not the entire ordinary or stable endomorphism ring of Z.
If d is infinite, every positive self-Ext vanishes, so the algebra in
(5) is just k. For finite d, the ideal epsilon R_+ is square-zero and
the quotient in (5) is exactly R.

**Proof.** Work first in the cohomology algebra E of the complete cone.
Let I be the single off-diagonal block in its endomorphism DG algebra.
The opposite off-diagonal block is zero as an ordinary Hom complex.
Consequently I is a DG ideal with I^2=0, and the quotient DG algebra is
the product of the two diagonal endomorphism DG algebras. Thus pi in
(1) is multiplicative. Its kernel J consists of classes represented by
closed elements of I, and J^2=0. This proves the ideal assertion using
actual block multiplication, rather than guessing it from dimensions.

For m>=1 with r^m!=1, the matrix in (2) is invertible. Its kernel and
cokernel are zero. If r^m=1, write chi_m=h_1^(-m)=h_2^(-m).
The kernel is

\[
 Q_m=\{(a,\chi_m a):a\in S_m\},
\]

and the cokernel is identified with S_m by
(w_1,w_2) -> w_1+w_2. This is well-defined and bijective on the
cokernel because the image of (2) is exactly {(b,b):b in S_m}.

Surjectivity of delta^0 gives E^1=0. Equation (1) and the degree support
of H,V show that in positive degrees E has only the following terms:

\[
 E^{3m}\xrightarrow[\ \pi\ ]{\sim}Q_m,\qquad
 E^{3m+1}=J^{3m+1}\cong S_m\quad(d\mid m), \tag{6}
\]

and all other terms vanish. In particular J^(3m)=0. These statements
include d=1: the first off-diagonal group is in degree four, not one.

Let s_m(a) be the unique lift of (a,chi_m*a) to E^(3m). For resonant
positive m,n, multiplicativity of pi gives

\[
 \pi(s_m(a)s_n(b))=(ab,\chi_m\chi_n ab)
                  =(ab,\chi_{m+n}ab).
\]

There is no J in degree 3(m+n), so uniqueness forces
s_m(a)s_n(b)=s_(m+n)(ab). Hence these sections give a graded algebra
copy of R_+ in E. This splitting is forced by the degree support;
it is not obtained by assuming the original DG splitting is a chain map.

It remains to determine multiplication with J. Represent a class in
J^(3m+1) by a closed off-diagonal element with coordinates (w_1,w_2).
Multiplying on the left by a diagonal lift with coordinates
(a,chi_n*a) gives (chi_n*a*w_1,chi_n*a*w_2), by hypothesis 3 and
resonance. Multiplying on the right gives the same two coordinates.
Off-diagonal parts of the chosen lifts make no contribution, since
I^2=0. Both actions descend to the cokernel: adding a pair (b,b)
changes either product by another such pair. Under w=w_1+w_2 the
common action is chi_n*a*w.

Use the following normalization in each resonant positive degree:

\[
 J^{3m+1}\longrightarrow\epsilon S_m,
 \qquad w\longmapsto\epsilon h_1^m w. \tag{7}
\]

It is invertible because h_1 is nonzero. For either action, its value
on a product is

\[
 \epsilon h_1^{m+n}\chi_n a w
 =\epsilon a(h_1^m w).
\]

Thus (7) turns both actions into ordinary multiplication in R.
Products inside J are zero. Together with the unique diagonal sections,
this proves (4), including its grading and its multiplication formula.
Comparison with actual positive Ext respects composition, giving the
stated Yoneda interpretation.

The stable identity maps to (1,1) in ker delta^0, so it is nonzero;
in particular Z is not zero. The actual scalar identity acts as the
unit on all positive Ext classes. Including this scalar copy of k
extends (4) to (5). No assertion about other degree-zero endomorphisms
is needed. If r has infinite order, the same invertibility argument
and delta^0 surjectivity give the final vanishing assertion. ∎

## 3. Explicit products and the missing degree-one generator

The algebra R is generated by the d+1 monomials
u_i=x^(d-i)*y^i, 0<=i<=d, all in cohomological degree 3d.
Its positive ideal is generated by these monomials. Therefore the
algebra (5) is generated by the u_i and v_i=epsilon*u_i, with
|v_i|=3d+1. Within the polynomial-dual-number model, all products
are specified by

\[
 u_i u_j=x^{2d-i-j}y^{i+j},\qquad
 u_i v_j=\epsilon x^{2d-i-j}y^{i+j}=v_i u_j,\qquad
 v_i v_j=0.
\]

These identities are product formulas, not a claim that a displayed
short list is a complete defining presentation. In particular a
generator epsilon in degree one would incorrectly introduce an Ext^1
class. Formula (3) excludes it. The dimension series agrees with the
previous spectrum, but the multiplication proof used the DG ideal,
the unique sections and the actual bimodule actions in addition.

## 4. Provenance, scope and the remaining realization problem

The cone block sequence and composition-compatible complete-resolution
comparison are prior machinery in the pinned OpenAI source
`02-conversion.tex`. The natural branch maps and positive scalar twist
action are in `07-branches.tex` (including `branch:twist`);
`06-lift.tex` supplies the preceding finite lift and evaluation input.
See [ATTRIBUTION.md](ATTRIBUTION.md) for the pinned commit and manuscripts.
This note extracts the positive multiplicative structure in the resonant
case from that setup. It does not present the cone construction or
square-zero matrix multiplication as new methods, and it does not
claim that no equivalent calculation exists in prior literature.

The theorem is stronger than a dimension classification under the
stated multiplicative hypotheses. The application to the explicit
ARC family still requires the actual side-projective F, finite Z,
complete-resolution comparison and branch naturality over the chosen
parameter field. The current Lean sources do not construct those
objects or prove these added hypotheses. This note cannot be used
as an unconditional complete ARC certificate. It treats positive
Yoneda multiplication and its scalar degree-zero subalgebra; it does
not compute the entire degree-zero endomorphism ring or the full
Tate algebra in negative degrees. Signs and skew-polynomial issues
outside characteristic two require a separate proof.
