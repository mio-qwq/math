# Complete structural proof

The original question is Section 6 Problem 1 of
[Mortada, El Zein and Al Hajjar, arXiv:2608.02566v1](https://arxiv.org/html/2608.02566v1#S6).
The hypothesis is a connected claw-free subcubic simple graph other than H;
there is no three-connectivity, girth or diamond-free-core hypothesis.
The palette has five distinct labels 1a,1b,3a,3b,4, with equal-label
vertices at distance strictly greater than the indicated radius.

For an odd integer k>=3, define D_k on a_i,b_i,p_i,q_i (i modulo k).
Its edges are a_i b_i, a_i p_i, a_i q_i, b_i p_i, b_i q_i,
and q_i p_(i+1). Thus D_k is a connected simple cubic graph on 4k
vertices. Replace each vertex v by the triangle T_v of incidences (v,w),
w in N_D(v). Add the three edges in T_v and the edge (v,w)(w,v) for
each core edge vw. Call the resulting triangle expansion G_k.

G_k has 12k vertices and 18k edges. It is connected and simple; each
point has two adjacent neighbours in its own triangle and one reciprocal
port neighbour. Thus it is cubic and claw-free. Since H has 12 vertices
(source Figure 1 and Proposition 1), G_k is not isomorphic to H.

Suppose an original coloring exists. Each T_v contains a high-colored
point, since three pairwise adjacent vertices cannot use only the two
radius-one labels. Choose one such point x_v, with no normalization and
no assumption that it is the only high point in T_v. Its label, renamed
A=3a,B=3b,C=4, defines f(v).

For every core edge uv, any two points of T_u,T_v are connected by a
walk of length at most three: an internal triangle edge, the reciprocal
port edge, and an internal triangle edge, omitting steps when endpoints
already are the appropriate ports. Hence f is a proper three-coloring
of D_k, for both radius-three labels and the radius-four label.

Let I=f^{-1}(C). For v in I, write its actual selected point as
x_v=(v,w). If u!=v is another I-vertex adjacent to w, then

(v,w) -> (w,v) -> (w,u) -> (u,w) -> x_u

is a walk of at most four edges in G_k. Therefore the original distance
between the two distinct points x_v,x_u is at most four, contradicting
their common label C. Consequently N_D(w) intersect I = {v}.
Every C-vertex has an external private neighbour. This is necessary for
every original coloring and every choice of its high representatives.

In a properly three-colored diamond, a_i and b_i have different colors;
p_i and q_i must have the same third color t_i. The joining edge gives
t_i!=t_(i+1). If t_i=C, both p_i and q_i belong to I. Neither a_i nor
b_i is a private neighbour of p_i, since each also neighbours q_i.
The third neighbour of p_i is q_(i-1). Its color is not C, so one of
a_(i-1),b_(i-1) has color C and also neighbours q_(i-1). Therefore
this third neighbour is not private either, a contradiction.

Thus no t_i equals C. But the t_i form a proper two-coloring of an odd
cycle, which is impossible. This proves the infinite written family.
For k=3, the three tips are pairwise different; the final finite
contradiction is just a triangle with only two allowed labels.

The k=3 certificate uses core labels a_i=4i,b_i=4i+1,p_i=4i+2,q_i=4i+3.
The original 36 vertices are the lexicographically sorted (v,w)
incidences in `counterexample.json`. In Lean, `vertex v i` has number
3*v+i; `partner` is reciprocal incidence. `graph_matches_edges` checks
all 36-by-36 pairs against the exact certificate's directed edge list.
The color function is universally quantified over Fin36 -> Fin5.
No assumed distance table, no assumed non-colorability and no restriction
to a special family of original colorings enters the final theorem.

Lean formalizes all original hypotheses and this whole contradiction
for k=3. It does not yet formalize the entire odd-k family. The original
problem is refuted by this fixed witness alone.
