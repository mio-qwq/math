# The standard-equivalence moduli space is a finite graph

Fix \(m\ge2\). Let \(X_m\) be the labelled, dephased unit-entry matrices
of order \(2m\) whose entrywise powers \(1,\ldots,m-1\) are all complex
Hadamard. The classification in [general-patterns.md](general-patterns.md)
and the graph construction in [phase-geometry.md](phase-geometry.md)
are the mathematical antecedents of this note.

Here *standard equivalence* means independent unit row and column phases
and row and column permutations. Transposition and complex conjugation
are not added to this equivalence relation. We determine the quotient
topology, the exact action on each phase circle, and its local valencies.
These are written consequences of the exhaustive classification, not
a complete Lean formalization, a new seed-existence theorem, or a
historical-priority claim.

## 1. Dephasing reduces equivalence to a finite action

Let \(N=2m\), with initial index \(0\), and put
\(\Gamma=\mathfrak S_N\times\mathfrak S_N\).
For a row permutation \(\sigma\) and column permutation \(\tau\), define
\[
T_{\sigma,\tau}(K)_{ij}
 =\frac{K_{\sigma(i),\tau(j)}K_{\sigma(0),\tau(0)}}
        {K_{\sigma(i),\tau(0)}K_{\sigma(0),\tau(j)}}. \tag{1}
\]
All entries in the denominator are unit. This is permutation followed
by the unique dephasing, so it preserves the required Hadamard powers
and maps \(X_m\) continuously to itself.

Multiplying an input matrix by arbitrary unit row and column factors
does not change (1), since those factors cancel. Applying (1) twice
therefore composes as applying the corresponding permutations twice
and dephasing once. With the induced right-action convention, these
maps give a finite group action. Its orbits are exactly standard
equivalence classes of dephased matrices: phases disappear under
dephasing, and every standard equivalence is phases and permutations.

The same description holds topologically. The full unit-entry
all-power solution set is a compact subset of the finite torus.
The continuous dephasing map identifies its quotient by unit row and
column phases with \(X_m\): its fibers are exactly those phase orbits,
and every fiber has exactly one dephased representative.
A continuous bijection from a compact space to the Hausdorff \(X_m\)
is a homeomorphism. Quotienting afterwards by the finite permutations
gives precisely \(X_m/\Gamma\), with its quotient topology.

## 2. The forced action on phase circles

For a root seed \(G\in B_m\) and compatible rectangle \(Q=R\times S\),
write
\[
\Phi_{G,Q}(\alpha)_{ij}
 =G_{ij}\alpha^{r_i s_j},\quad |\alpha|=1,\qquad
r_i=\mathbf1_R(i),\quad s_j=\mathbf1_S(j).
\]
Each of \(R,S\) has size \(m\) and avoids index \(0\).
The exponent of \(\alpha\) after (1) is exactly
\[
\begin{aligned}
&r_{\sigma(i)}s_{\tau(j)}
 +r_{\sigma(0)}s_{\tau(0)}
 -r_{\sigma(i)}s_{\tau(0)}
 -r_{\sigma(0)}s_{\tau(j)}\\
&\hspace{2em}=(r_{\sigma(i)}-r_{\sigma(0)})
             (s_{\tau(j)}-s_{\tau(0)}). \tag{2}
\end{aligned}
\]
Define
\[
R'=\{i:r_{\sigma(i)}\ne r_{\sigma(0)}\},\quad
S'=\{j:s_{\tau(j)}\ne s_{\tau(0)}\},\quad
e=(-1)^{r_{\sigma(0)}+s_{\tau(0)}}.
\]
Both new sets have size \(m\) and avoid index \(0\).
Equation (2) is \(e\mathbf1_{R'\times S'}(i,j)\).
The matrix \(G'=T_{\sigma,\tau}(G)\) is again a root seed, and hence
\[
T_{\sigma,\tau}\bigl(\Phi_{G,Q}(\alpha)\bigr)
 =\Phi_{G',R'\times S'}(\alpha^e). \tag{3}
\]
The new rectangle is compatible. Indeed, this entire transformed family
satisfies all powers; choose any nonroot parameter and use the
exhaustive classification and uniqueness of its nonconstant
\(m\)-th-power rectangle to obtain that compatibility.
Thus \(\Gamma\) permutes the actual circle images and root points.

Suppose an element of \(\Gamma\) stabilizes one circle image, using
\(\Phi_{G,Q}\) as its chosen parametrization. Its transformed root
\(G'\) is on that circle. The circle has exactly the \(m\) root points
\(\Phi_{G,Q}(\zeta)\), \(\zeta\in\mu_m\), so
\(G'=\Phi_{G,Q}(\zeta)\) for a unique \(\zeta\in\mu_m\).
Uniqueness of the nonroot rectangle gives \(R'\times S'=Q\).
On this circle the induced action is therefore precisely
\[
\alpha\longmapsto\zeta\alpha
\quad\text{or}\quad
\alpha\longmapsto\zeta\alpha^{-1},
\qquad \zeta\in\mu_m. \tag{4}
\]
Its effective stabilizer is a subgroup of this finite dihedral action.
Elements acting trivially on the whole circle remain allowed; no
faithfulness assumption on the permutation group is made.

## 3. The quotient is a finite graph

Start with the finite graph of [phase-geometry.md](phase-geometry.md),
whose root vertices are \(B_m\) and whose edges are the arcs between
successive roots on each distinct circle image.
Subdivide each circle at the fixed points of every effective reflection
in its circle stabilizer, adding them to the root vertex set.
There are finitely many circles and group elements, and each effective
reflection has exactly two fixed points. The resulting finite vertex
set is \(\Gamma\)-invariant: group elements carry a circle stabilizer
and its reflection fixed points to the conjugate stabilizer on the
image circle.

The action on this finite subdivision has no edge inversion. To see
this, an element preserving an edge must preserve its unique circle.
By (4) its restriction is a rotation or a reflection. A nontrivial
rotation cannot map a proper arc to itself. A reflection mapping an
arc to itself and reversing its endpoints has a fixed point inside
that arc, which was included among the subdivision vertices; such
an arc is no longer an edge. The remaining edge-preserving action
fixes the entire edge pointwise.

Consequently the quotient has the finite graph construction obtained
by taking vertex and edge orbits and their endpoint incidences.
Each edge interior maps homeomorphically to its image interior:
distinct edges can be identified, but the stabilizer of an edge acts
pointwise. Attach each quotient interval to the corresponding vertex
orbits; loops, parallel edges and isolated vertices are allowed.
This finite compact graph maps continuously and bijectively to
\(X_m/\Gamma\). The latter is Hausdorff because it is the quotient of
a compact Hausdorff space by a finite group. The map is therefore a
homeomorphism.

**Theorem.** The standard-equivalence moduli space of the all-power
unit-entry matrices is a finite compact graph. It is obtained by
subdividing the labelled graph at effective reflection fixed points
and then taking the finite permutation orbits. At odd \(m\), it is
a finite discrete set of root equivalence classes, possibly empty.

This is a finite mathematical construction given the root seeds,
compatible rectangles and their permutation stabilizers. It does
not assert that their enumeration is efficient or that seeds exist
at any new order.

## 4. Local valencies and the location of folding

For a nonroot point \(K=\Phi_{G,Q}(\alpha)\), only one actual circle
is incident. Its stabilizer in \(\Gamma\) preserves that circle.
Choose a small invariant arc neighborhood of \(K\), disjoint from
neighborhoods of the other points in its finite orbit and from the
other circles and root points. Formula (4) shows that an effective
circle action fixing \(\alpha\) is either the identity or a reflection:
a rotation \(\zeta\alpha=\alpha\) requires \(\zeta=1\).

If no effective reflection fixes \(\alpha\), the two local half-arcs
remain distinct in the quotient and the valency is two.
If such a reflection exists, it interchanges the half-arcs and the
valency is one. Thus a nonroot orbit is an endpoint exactly when an
effective circle-stabilizing reflection fixes it. No new nonroot
branch point of valency greater than two can occur.

The fixed-point equation is
\[
\alpha^2=\zeta,\qquad \zeta\in\mu_m.
\]
An actual circle can occur only when \(m\) is even, by the existing
rank obstruction. Hence
\[
\alpha^m=\zeta^{m/2}\in\{1,-1\}.
\]
The value \(1\) is a root point already in \(B_m\). Therefore every
endpoint created away from root orbits has
\[
\alpha^m=-1. \tag{5}
\]
The phase condition (5) is necessary, not sufficient: the corresponding
effective reflection must actually occur in the circle stabilizer.
It is unchanged by replacing the chosen seed by another root on the
circle, since that change multiplies \(\alpha\) by an \(m\)-th root.

At a root \(G\), let \(r(G)\) be its number of compatible rectangles,
and let \(\Gamma_G\) be its dephased permutation stabilizer.
The labelled graph has \(2r(G)\) incident local half-branches.
Take a small \(\Gamma_G\)-invariant star neighborhood, disjoint from
neighborhoods of the other roots in the finite orbit of \(G\).
Quotient half-branches correspond exactly to \(\Gamma_G\)-orbits:
within such a small star, an element identifying two branches must
fix the central root. It follows that
\[
\operatorname{valency}([G])
=\#\bigl(\Gamma_G\backslash
        \{\text{the }2r(G)\text{ local half-branches at }G\}\bigr). \tag{6}
\]
In particular \(r(G)=0\) gives an isolated quotient point. A root
with incident circles can become an endpoint, a regular point, or a
branch vertex. Formula (6) uses the actual action on branches, not
just the order of the stabilizer.

## 5. Provenance and remaining questions

The exhaustive all-power classification and labelled graph are the
specific antecedents. The facts that a finite action without inversions
has a graph quotient, and that a circle's dihedral reflections fold
local arcs, are classical elementary topology. The contribution
recorded here is their explicit application using the exact matrix
dephasing formula (2), which forces (4), (5) and (6) for this solution
space.

Hadamard switching, the order-four affine family, and general phase
deformations are established methods; the original references and
comparison limits in [general-patterns.md](general-patterns.md) apply.
The full original-text comparison with Craigen and Woodford,
*Power Hadamard matrices*, Discrete Mathematics 308 (2008), 2868–2884,
DOI [10.1016/j.disc.2006.06.050](https://doi.org/10.1016/j.disc.2006.06.050),
remains pending. In particular, failing to obtain that original article
does not establish originality or absence of overlap.

Realizing compatible cyclic root seeds at new even half-orders,
counting seed orbits, computing their effective stabilizers in
general, and formalizing the whole matrix classification and topology
in Lean remain separate questions. This note does not infer
existence, nonexistence or new priority from its finite description.
