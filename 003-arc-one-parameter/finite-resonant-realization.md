# A finite triangular realization of the resonant positive Yoneda algebra

Research note, 8 October 2026. This is a written construction and proof;
the complete construction in this note has not been formalized in Lean.
The construction machinery is attributed below. Historical novelty of
the finite-resonant multiplication calculation remains unestablished.

## 1. Statement and scope

Let k be a characteristic-two field, let q in k have infinite
multiplicative order, and let h_1,h_2 be nonzero elements of k. Use the
ten-dimensional algebra C(q) in Section1 of [paper.md](paper.md), its
trivial extension T=C(q) plus DC(q), the symmetric algebra A=T tensor_k T,
and its one-dimensional module X=s tensor_k s. Here s is the f-simple
inflated from C(q) to T. Put r=h_1/h_2.

**Theorem.** There exist an actual finite A-bimodule F, projective on both
sides, and an actual finite module Z over

\[
 \Lambda=\begin{pmatrix}A&0\\F&A\end{pmatrix}
\]

with a complete totally acyclic resolution such that Z is nonprojective
and Ext_Lambda^a(Z,Lambda)=0 for every a>0. If r has finite order d, its
positive Yoneda algebra is

\[
 \bigoplus_{a>0}\operatorname{Ext}_\Lambda^a(Z,Z)
 \cong R_+\oplus\epsilon R_+,
 \qquad R=k[\tau_1,\tau_2]^{(d)},\quad |\tau_i|=3,
 \quad |\epsilon|=1,\quad\epsilon^2=0. \tag{1}
\]

Here R is the dth Veronese subalgebra with its cohomological grading,
and R_+ its positive ideal. Adjoining only the actual scalar identity
of Z gives R plus epsilon R_+. The epsilon summand has no constant
term. If r has infinite order, every positive self-Ext of Z vanishes.

This theorem establishes the explicit multiplicative hypotheses of
[resonant-yoneda-algebra.md](resonant-yoneda-algebra.md) for a finite
construction. It does not compute the entire ordinary degree-zero
endomorphism ring or negative Tate multiplication. For finite d, the
module has nonzero positive self-extensions and is not an ARC
counterexample. No complete Lean verification is asserted here.

## 2. The base calculation over the chosen field

The lower resolution calculation in the pinned OpenAI source
`04-resolution.tex` uses q nonzero and 1+q^m nonzero for every m>0.
Both follow from infinite order. Its coordinate kernels and images
therefore apply over k, without assuming that q,h_1,h_2 are algebraically
independent. They give

\[
 \operatorname{Ext}_C^i(s,s)=
 \begin{cases}k&i=0,\\0&i>0,\end{cases}\qquad
 \operatorname{Ext}_C^i(s,C)=
 \begin{cases}s^{\mathrm r}&i=2,\\0&i\ne2,\end{cases} \tag{2}
\]

where the latter identification respects the right C-action.

For each finite projective left C-module P, the natural identification
DC tensor_C P = D Hom_C(P,C) turns (2) into
DC tensor_C^L s = s[2]. Tensoring 0 -> DC -> T -> C ->0 with that
resolution gives the T-derived triangle

\[
 s[2]\longrightarrow T\otimes_C^{\mathbf L}s\longrightarrow s
 \xrightarrow{\delta}s[3].
\]

Induction/restriction adjunction computes Hom of the middle term into
s[i] as k at i=0 and zero at all other i. Its exact sequence gives
Ext_T^1=Ext_T^2=0 and, for i>=2, identifies Ext_T^(i-3) with Ext_T^i
by composition with delta. Thus Ext_T^*(s,s)=k[tau], |tau|=3.
The specified cochain p(s) is a nonzero generator, since its value on
the stated bar cycle is q^3. This is the prior polynomial calculation,
not a new all-power assertion.

Tensoring two projective resolutions over k and their comparison maps
identifies the actual nonnegative stable algebra of X with

\[
 H^{\ge0}=k[\tau_1,\tau_2],\qquad |\tau_1|=|\tau_2|=3. \tag{3}
\]

Characteristic two removes the interchange sign. The nonzero Ext3
classes show X is nonprojective; its ordinary and stable endomorphism
spaces are k. In particular its stable identity is nonzero.

The algebra and cochain coefficients are universal polynomials over
F_2[q]. The closure and twisted-boundary recurrences in
`09-cochain.tex` require no parameter independence. These existing
identities justify using the same cochain and comparison maps over k;
they do not substitute for the following finite bimodule construction.

## 3. One fixed finite target and maps for every nonzero twist

Use the two-cone complex K of `05-cones.tex` and the side-projective
finite bimodule C_1=coker(K_2 -> K_1). Put

\[
 Y=\Sigma_{A^e}^{4}C_1.
\]

The finite cosyzygies are taken using
M -> Hom_k(A^e,M), m -> (t -> tm), with action by right multiplication
on the input. These are injective embeddings into finite projectives
because A^e is symmetric. When M is projective on both A-sides, each
sequence splits on both sides, so its cokernel has the same property.
Consequently Y is finite and side-projective. It represents
the stable two-cone object Ccal[3] in that source.

The source's full filtration computation, including the top connecting
map, proves

\[
 W_Y^a=\underline{\operatorname{Hom}}_A(X,YX[a])=
 \begin{cases}k&a=-3,0,\\0&\text{otherwise}.
 \end{cases} \tag{4}
\]

It also identifies W_Y^0 with H^-1 by the top-cell projection. This
construction and profile involve q, and are independent of h_1,h_2.

For H in k nonzero, let h_H fix C and scale DC by H, and set
U_H=A_(h_H tensor h_H), with its regular left and twisted right action.
It is free on both sides. Since the twist fixes the simple character,
U_H tensor_A X is canonically X.

`06-lift.tex` constructs a stable map U_H -> Ccal[3] for every nonzero H.
It uses the twisted trace tensor, the bar homotopy B and the homotopy G
supplied by the universal twisted-boundary identity. The last homotopy
is lifted successively through projective terms; no denominator
h_1^m+h_2^m occurs. The evaluated top-cell map has value
H^2(f^* tensor f^*) and is nonzero stably, by the radical/socle
annihilation argument. The formulas and proof use only the field
conditions in Section2 and H nonzero, so they apply to the present k.

Taking the corresponding four cosyzygies gives a stable map into the
fixed Y. Choose actual representatives g_i:U_(h_i) -> Y after rescaling
by h_i^-2. Because the top projection in (4) is an isomorphism, their
evaluated stable maps equal one common nonzero w in W_Y^0.
These are choices in finite bimodule Hom spaces over k, rather than
specializations of rational matrices from a three-variable field.

## 4. The finite kernel and its whole positive profile

Let Q=A^e tensor_k Y with surjection pi(a tensor y)=ay, and define

\[
 F=\ker\bigl((g_1,g_2,\pi):U_{h_1}\oplus U_{h_2}\oplus Q\to Y\bigr).
 \tag{5}
\]

The sequence is onto because pi is. It splits separately on both
A-sides, since Y is projective on each side. Hence F is finite and
side-projective. Let rho_i:F -> U_(h_i) be the actual projections.

Evaluation on X preserves exactness, and QX is A-projective.
Its stable triangle is

\[
 FX\longrightarrow X\oplus X\xrightarrow{(w,w)}YX
 \longrightarrow FX[1].
\]

Set V^a=stable Hom_A(X,FX[a]). Its exact sequence contains

\[
 (H^{a-1})^2\longrightarrow W_Y^{a-1}\longrightarrow V^a
 \xrightarrow{(\rho_1[a],\rho_2[a])}(H^a)^2\longrightarrow W_Y^a.
 \tag{6}
\]

At a=0, W_Y^-1=0 and the last map k^2 -> W_Y^0 sends(c,e) to(c+e)w.
Thus V^0 is the diagonal line and contains a unique v with projections
(id_X,id_X). At a=1, surjectivity of k^2 -> W_Y^0 kills the potential
connecting contribution, and the projection in (6) is an isomorphism.
For a>=2 both W groups in (6) are zero, giving the same isomorphism.
This proves the entire positive branch profile for arbitrary h_1,h_2;
no ratio-order condition was used.

## 5. Both actions and the actual comparison matrix

The bimodule maps rho_i give natural transformations of exact tensor
functors that preserve projectives, with compatible stable shifts.
Write p_i^a:V^a -> H^a for the branch coordinates in (6).
For arbitrary alpha in H^n, beta in H^n and u in V^m, naturality gives

\[
 p_i^{m+n}\bigl(F(\alpha)[m]\circ u\bigr)
   =U_{h_i}(\alpha)[m]\circ p_i^m(u),\qquad
 p_i^{m+n}\bigl(u[n]\circ\beta\bigr)
   =p_i^m(u)[n]\circ\beta. \tag{7}
\]

These formulas hold for arbitrary u, not only v. The exact tensor
functors and their stable comparison maps supply the shifts, so the
formulas agree with composition on the complete resolutions.

The right-twist convention gives
A_sigma tensor_A M = inverse restriction of M. Applying sigma^-1
to all bar letters multiplies the specified simple-valued degree-three
cocycle by H^-1: every nonzero component has exactly one dual input.
The tensor functor preserves Yoneda products. It therefore acts on
the whole polynomial piece H^(3n)=S_n by H^-n, since both generators
have that weight. Thus (7) gives left multiplication by h_i^-n alpha
on branch i and ordinary right multiplication by beta. This proves
both action hypotheses of the positive multiplication theorem.

Since p_i(v)=id_X, the actual map delta^a(g,j)=F(g)v+v[a]j has

\[
 \delta^0(c,e)=(c+e)v,\qquad
 \delta^{3m}(g,j)=(h_1^{-m}g+j,h_2^{-m}g+j). \tag{8}
\]

Its determinant need not be nonzero. Finite-order resonance is
retained, rather than importing the source's final independence
argument to eliminate it.

## 6. The actual finite module and its Yoneda multiplication

Choose an ordinary representative v_0:X -> FX and embed X into a finite
A-projective P by i. Set

\[
 N=(FX\oplus P)/\{(v_0(x),i(x)):x\in X\},\qquad
 Z=(X,N,\iota),
\]

where iota:FX -> N is induced by inclusion. It is injective because i
is. These are actual finite modules. The complete column resolution
construction of Lemma2 in [paper.md](paper.md) applies: the cone
cokernel is Z and the cone is totally acyclic, giving
Ext_Lambda^a(Z,Lambda)=0 for every a>0. Total acyclicity uses the
projective-injective left A-modules A,F and does not use invertibility
of (8). The upper-component functor takes Lambda-projectives to
A-projectives. Its value X on Z is nonprojective, so Z is nonprojective.

The cone has one strict square-zero off-diagonal DG ideal. Its full
endomorphism cohomology computes positive Yoneda Ext with composition
preserved. Sections2–5 have established all three hypotheses in
[resonant-yoneda-algebra.md](resonant-yoneda-algebra.md). Applying that
theorem proves (1), including the actual mixed products and scalar
degree-zero subalgebra. In particular the conclusion is an algebra
isomorphism, not merely a matching dimension series. This completes
the construction proof.

## 7. An exact field example and provenance

Take k=F_4(t), with F_4=F_2[zeta]/(zeta^2+zeta+1), q=t, h_1=zeta and
h_2=1. The element zeta has order three, while t has infinite order.
The first positive self-Ext groups of the constructed Z are Ext9 and
Ext10, each of dimension four; Ext18 and Ext19 each have dimension
seven. Its positive generators are the four degree-nine monomials
tau1^3,tau1^2 tau2,tau1 tau2^2,tau2^3 and their degree-ten epsilon
multiples. Products of two epsilon multiples are zero. These are
exact consequences of the construction proof, not finite or Lean
computations. Every odd finite order can likewise be obtained by
using suitable finite-field constants and adjoining an indeterminate.

The base polynomial calculation, two cones, finite cosyzygies, arbitrary
twist lift, finite fiber and triangular conversion are prior OpenAI
machinery at the pinned commit in [ATTRIBUTION.md](ATTRIBUTION.md),
specifically `02-conversion.tex`, `04-resolution.tex`, `05-cones.tex`,
`06-lift.tex`, `07-branches.tex` and `09-cochain.tex`. The point here is
to keep finite twist-ratio resonance and determine its actual positive
multiplication using that machinery; the Veronese algebra itself and
square-zero matrix multiplication are classical constructions.

Qiyue Tang's [Hexagon preprint2610.00143v1](https://hexagonmath.org/pdf/2610.00143v1)
also supplies maps for every nonzero H into one common finite target in
Proposition5.4, via a different derived-induction construction. That
target has not been identified with the fixed Y used above. Using
Tang's route requires taking its target, profile and maps together,
rather than transferring its maps into the OpenAI Y. Tang's field
extension and base-parameter results remain prior mathematics; no
new ARC field extension or global originality claim is made here.
