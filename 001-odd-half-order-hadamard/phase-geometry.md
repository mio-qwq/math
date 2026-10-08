# The labelled dephased solution space is a finite graph

Fix m>=2. Let X_m be the set of **labelled, dephased** complex matrices
K of order 2m for which every entrywise power 1,...,m-1 is Hadamard.
Rows and columns retain their labels, the initial row and column are
all ones, and no quotient by matrix equivalence is taken. Give X_m the
subspace topology of the finite-dimensional complex matrix space.

Let B_m be its finite set of cyclic GH(m,2) root matrices. The exact
classification and exhaustive construction in
[general-patterns.md](general-patterns.md) express X_m as B_m together
with finitely many compatible phase-circle images. The following are
analytical consequences of those written theorems; they are not a
complete Lean formalization or a historical novelty claim.

## 1. Distinct phase circles intersect only at root matrices

For a root seed G and compatible rectangle Q=R×S, write

\[
 \Phi_{G,Q}(\alpha)_{ij}=
 \begin{cases}\alpha G_{ij},&(i,j)\in Q,\\G_{ij},&(i,j)\notin Q,
 \end{cases}\qquad |\alpha|=1.
\]

Remove duplicate circle images. If a nonroot matrix K lies on such a
circle, its mth entrywise power equals one off Q and a common value
x=alpha^m!=1 on Q. Thus K itself uniquely determines R and S as the
nonconstant rows and columns of this power.

Suppose K=Phi_(G,Q)(alpha)=Phi_(G',Q')(beta) is nonroot. This uniqueness
gives Q=Q'. Outside Q the seeds agree; on Q, G'=(alpha/beta)G. Since
both seeds have entries in mu_m and Q is nonempty, zeta=alpha/beta lies
in mu_m. For every unit t,

\[
 \Phi_{G',Q}(t)=\Phi_{G,Q}(\zeta t).
\]

The two entire circle images therefore coincide. Distinct images can
intersect only in B_m.

Each phase map is injective: any fixed entry in Q recovers alpha by
division by its nonzero seed entry. It has exactly m root matrices,
corresponding to alpha^m=1. These are m distinct matrices.

## 2. A complete finite graph model

Use B_m as the vertex set. The m root points cut each distinct circle
into m open arcs; add one edge for each arc and identify its endpoints
with their actual root matrices. Since m>=2, each closed arc is an
embedded interval with distinct endpoints. Parallel edges are allowed:
at m=2 one circle contributes two edges between the same pair of roots.
Roots on no circle are isolated vertices. The empty solution set is
also allowed.

The resulting finite compact graph maps continuously onto X_m by the
phase parametrizations. Exhaustiveness gives surjectivity. Different
open arcs have no common point, and all root intersections were
identified by their actual matrix labels, giving injectivity. A
continuous bijection from a compact space to a Hausdorff space is a
homeomorphism. Thus **X_m is homeomorphic to this finite graph**.

For odd m there are no compatible circles, so X_m=B_m is finite and
discrete. This is not an existence theorem at any specified order.

## 3. Actual local dimension and branches

The phase map has the explicit affine form

\[
 \Phi_{G,Q}(\alpha)=G+(\alpha-1)(G\circ\mathbf1_Q).
\]

The vector G∘1_Q is nonzero. Hence its image is a smooth circle in an
affine real two-plane, with nonzero derivative
i exp(it)(G∘1_Q). A nonroot point lies on exactly one image. The other
finitely many compact images and the finite root set have positive
distance from it. A sufficiently small neighborhood therefore meets
X_m in a single smooth arc. Its **actual local real dimension is one**.

If a root G belongs to d(G) different circles, its local graph has
2d(G) branches. When d(G)=0 it is isolated. Every incident circle can
use G itself as seed. Its tangent line is

\[
 \mathbb R\,(iG\circ\mathbf1_Q).
\]

Distinct incident circles have distinct rectangles and hence distinct
tangent lines. These describe the actual curve branches; they do not
assert that the kernel of the linearized Hadamard equations has the
same dimension or equals their union.

## 4. Finite construction and limits

Given the finite root seeds and their compatible rectangles, duplicate
circle images are identified exactly by multiplying the seed on the
same rectangle by one element of mu_m. Each distinct circle has m such
seed-rectangle representations, one at each root point. Consequently,
if c_m is the number of distinct circles and r(G) is the number of
compatible rectangles at G, then

\[
 \sum_{G\in B_m}r(G)=m c_m,
 \qquad \deg(G)=2r(G).
\]

The connected components are those of the resulting finite incidence
graph. This is a finite mathematical construction, without a new
parameter enumeration or an efficiency claim. Realization of seeds
and compatible rectangles at new even orders remains a separate
problem. Taking a quotient by row or column equivalence would require
separate stabilizer and local-geometry analysis. The full literature
comparison with power-Hadamard classifications and classical complex
Hadamard deformations remains pending.
