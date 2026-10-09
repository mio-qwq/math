# Six-point midpoint covers of the six-cube and a twelve-center obstruction

This note gives a complete written classification
of six same-parity Hamming words whose distance-four pairs supply every
midpoint of that parity. It then excludes all feasible twelve-center sets in
\(Q_6\boxtimes Q_6\), strengthening the necessary size window to
\(13\le |C|\le21\). The classification and product exclusion are written
proofs, not Lean theorems. The formalization boundary is stated in Section 11.
Historical originality of the exact classification and product consequence
has not been established.

The result does not resolve the general strong-product packing-domination
conjecture. It excludes one boundary size in one particular product; no
feasible nonlinear set of size 13 through 21 is constructed or excluded here.

## 1. Definitions and statements

Let \(V=\mathbb F_2^6\), with coordinatewise XOR as addition. Write
\(\operatorname{wt}(x)\) for Hamming weight,
\(d(x,y)=\operatorname{wt}(x+y)\),
\(\pi(x)=\operatorname{wt}(x)\bmod2\), and
\(\mathbf1=(1,1,1,1,1,1)\). The antipode of \(x\) is
\(\bar x=x+\mathbf1\). Thus

\[
 d(\bar x,y)=6-d(x,y),\qquad \pi(\bar x)=\pi(x).
\]

For two words at distance four, a **midpoint** is a word at distance two
from each. A midpoint agrees with its two endpoints on every common
coordinate: otherwise the Hamming triangle inequality could not be an
equality. In the four differing coordinates, it agrees with each endpoint
on exactly two.

For \(P\subseteq V\) consisting of words of one parity \(\varepsilon\),
consider the condition

\[
 \tag{M}
 \forall x\in V\text{ with }\pi(x)=\varepsilon\quad
 \exists a,b\in P:
 d(a,b)=4,\quad d(x,a)=d(x,b)=2.
\]

Define

\[
 P_*=
 \{(t_1,t_1,t_2,t_2,t_3,t_3):
          t\in\mathbb F_2^3\setminus\{000,111\}\}.
\]

**Theorem 1 (six-point classification).** A set of six distinct words of one
parity satisfies (M) if and only if it is obtained from \(P_*\) by an ambient
XOR translation and a coordinate permutation. Consequently every such set
is closed under antipodes, and its graph of distance-two pairs is a
triangle-free six-cycle.

A set \(C\subseteq V\times V\) is **feasible** if

\[
 \begin{split}
 &\max\{d(a,a'),d(b,b')\}\ge4
       &&\text{for distinct }(a,b),(a',b')\in C,\\
 &\forall(x,y)\in V\times V\ \exists(a,b)\in C:
       d(x,a)\le2\text{ and }d(y,b)\le2.
 \end{split}
\]

The second line uses the same center for both coordinates. The metric is
the maximum of the two block distances, not their sum.

**Theorem 2 (twelve-center exclusion).** No feasible set has exactly twelve
centers. Together with the earlier bounds, every feasible set satisfies
\(13\le |C|\le21\).

The earlier
[affine obstruction and nonlinear necessary conditions](q6-strong-product-affine-obstruction.md)
give the single-factor obstruction, the window \(12\le |C|\le21\), and
the following projection implication: each block projection has at least
six distinct words of each parity, and each parity projection satisfies
(M). Thus a feasible twelve-center set would have injective projections,
with exactly six words of each parity in each block. Section 10 recalls why
this implication follows from the original packing and covering quantifiers.

## 2. Local consequences of midpoint coverage

Let \(P\) have six distinct words of one parity and satisfy (M). Let
\(G_P\) be the simple graph on \(P\) joining pairs at Hamming distance two.

For any \(p\in P\), apply (M) first to \(x=p\). This gives two distinct
distance-two neighbors of \(p\) that are distance four from each other.
Apply it next to \(x=\bar p\). Its parity is unchanged, and the two
resulting centers are at distance four from \(p\). Therefore

\[
 2\le\deg_{G_P}(p)\le3,
 \qquad
 |\{q\in P:d(p,q)=4\}|\ge2.
\]

The upper bound follows because at least two of the other five words are
already at distance four. A degree-two vertex cannot lie in a triangle:
its only two distance-two neighbors must be distance four apart. Hence
every vertex of a triangle in \(G_P\) has degree three.

No coordinate is constant on \(P\). If coordinate \(j\) were constant,
all midpoints of its distance-four pairs would have that value at \(j\).
But exactly 16 of the 32 words of the relevant parity have the opposite
value there, contradicting (M).

Translation and coordinate permutation preserve distances and (M). When
convenient we translate a selected word to zero; then every word of the
translated set has even parity.

## 3. The distance-two graph has a Hamiltonian six-cycle

We first give the graph reduction without assuming Hamiltonicity.

The graph \(G_P\) is connected. Otherwise its minimum degree two forces
each component to contain at least three vertices; with six vertices it
would consist of two triangles. Their degree-two vertices violate Section 2.

It is also 2-connected. If a vertex \(v\) were a cut vertex, its degree
at most three would force some component of \(G_P-v\) to attach to \(v\)
by just one edge. That edge is a bridge. Each side of any bridge has at
least three vertices: a side of size one or two would contain a vertex of
degree at most one. Thus the two sides have exactly three vertices each.
The two vertices on a side other than the bridge endpoint must both have
degree at least two, forcing that side to be a triangle. This gives two
triangles joined by a bridge, again with degree-two triangle vertices.

Choose a longest cycle. Its length is at least four. If it were only a
triangle, a component outside it would, by 2-connectivity, attach at two
distinct triangle vertices. A path through that component together with
the longer triangle arc would make a cycle of length at least four.

A longest cycle cannot have length four. Write it as
\(a-b-c-d-a\), with outside vertices \(r,s\).

- If \(rs\) is an edge, each outside vertex has a cycle neighbor. Their
  attachments cannot both be confined to one cycle vertex, by
  2-connectivity. Choose distinct cycle vertices \(a',b'\) giving the
  path \(a'-r-s-b'\). If \(a',b'\) are adjacent on the four-cycle, combine
  this path with its three-edge arc to obtain a six-cycle. If they are
  opposite, combine it with a two-edge arc to obtain a five-cycle.
- If \(rs\) is not an edge, each outside vertex has at least two cycle
  neighbors. Adjacent cycle neighbors would allow insertion of that
  outside vertex to make a five-cycle. Thus each attaches to a pair of
  opposite cycle vertices. They cannot attach to the same pair, as those
  cycle vertices would have degree four. If \(r\) attaches to \(a,c\)
  and \(s\) to \(b,d\), the cycle
  \(a-r-c-b-s-d-a\) has length six.

Suppose there is still no six-cycle. There is then a five-cycle and one
outside vertex. The outside vertex has at least two cycle neighbors; an
adjacent pair would yield a six-cycle. A five-cycle has no independent set
of size three, so there are exactly two nonadjacent neighbors. This gives
a spanning theta graph with three internally disjoint paths of lengths
two, two and three. Write the paths as

\[
 u-a-v,\qquad u-b-v,\qquad u-c-d-v.
\]

The endpoints \(u,v\) already have degree three. Any extra edge must be
one of \(ab,ac,ad,bc,bd\); each would yield a six-cycle, respectively

\[
 \begin{array}{c|l}
 ab&u-a-b-v-d-c-u\\
 ac&u-b-v-d-c-a-u\\
 ad&u-b-v-a-d-c-u\\
 bc&u-a-v-d-c-b-u\\
 bd&u-a-v-b-d-c-u.
 \end{array}
\]

Hence the only possible non-Hamiltonian graph under these conditions is
exactly this theta graph.

It cannot be the Hamming distance-two graph of \(P\). Translate \(u\)
to zero. The two-step paths through \(a,b\), and the fact that \(u,v\)
are not adjacent, give \(d(u,v)=4\). Permute coordinates so that
\(v=111100\). Since \(a,b\) are each distance two from both \(u,v\),
their supports are two-element subsets of the support of \(v\).
They are not adjacent to each other, so these supports are disjoint.
Take \(a=110000\) and \(b=001100\).

The word \(c\) has weight two and is not adjacent to \(a\) or \(b\).
Two weight-two words have distance at least four only when their supports
are disjoint. Thus \(c\) avoids both supports and must be \(000011\),
at distance six from \(v\). But \(c-d-v\) consists of two
distance-two steps and would give \(d(c,v)\le4\), a contradiction.

Therefore \(G_P\) has a Hamiltonian six-cycle.

## 4. Exactly twelve coordinate changes

Order the Hamiltonian cycle as \(p_0,\ldots,p_5,p_6=p_0\). Let
\(F_i\subseteq\{1,\ldots,6\}\) be the coordinates flipped between
\(p_i\) and \(p_{i+1}\). Every \(F_i\) has size two, so the traversal
makes twelve coordinate changes in total.

Every coordinate is nonconstant on \(P\), so it changes on this traversal.
A coordinate changes an even positive number of times around a closed
cycle. All six coordinates therefore change **exactly twice**.

Represent their occurrences by a loopless multigraph \(T\) on the six
cycle-edge positions \(0,\ldots,5\): each coordinate gives one edge
joining the two positions where it changes. Every vertex of \(T\) has
degree two. Parallel edges are allowed at this stage; loops are not.

In three consecutive flip sets, six coordinate changes occur. If \(k\)
coordinates each occur twice within those sets, the endpoints of the
three-edge path have Hamming distance \(6-2k\). For two consecutive
sets the corresponding distance is
\(4-2|F_i\cap F_{i+1}|\). These identities follow by cancelling repeated
flips; no coordinate can occur three times.

## 5. No chord at cyclic distance two

Suppose a cyclic distance-two chord exists. Rotate labels so that
\(p_0,p_1,p_2\) form a triangle. Then \(F_0,F_1\) share exactly one
coordinate \(\alpha\), which has now used both its occurrences.
The three triangle vertices have degree three. In particular \(p_0\)
is adjacent to \(p_1,p_5,p_2\), so its remaining vertices \(p_3,p_4\)
are both distance four from it. Similarly \(p_2\) is distance four from
\(p_4,p_5\).

The vertex \(p_1\) needs a third neighbor, among \(p_3,p_4,p_5\).
Each possibility is impossible.

- If \(d(p_1,p_3)=2\), the sets \(F_1,F_2\) share a coordinate
  \(\beta\ne\alpha\). In \(F_0,F_1,F_2\), both \(\alpha\) and
  \(\beta\) cancel, giving \(d(p_0,p_3)\le2\), contrary to distance four.
- If \(d(p_1,p_5)=2\), the symmetric argument in
  \(F_5,F_0,F_1\) gives \(d(p_5,p_2)\le2\), again a contradiction.
- If \(d(p_1,p_4)=2\), the three sets \(F_1,F_2,F_3\) require two
  cancelling coordinates. But \(d(p_2,p_4)=4\) says that \(F_2,F_3\)
  are disjoint. One of the two coordinates of \(F_1\), namely
  \(\alpha\), is already paired with \(F_0\); the other can give at
  most one cancellation. Two are impossible.

Thus there is no cyclic distance-two chord. The only possible remaining
chords join opposite cycle vertices. These chords form a matching and,
together with cycle edges alone, cannot make a triangle. Hence \(G_P\)
is triangle-free.

In particular \(T\) has no edge joining consecutive cycle positions:
one common coordinate would give a forbidden distance-two chord, and two
would give \(p_i=p_{i+2}\), violating distinctness.

## 6. No opposite chord

Suppose \(d(p_0,p_3)=2\). The three sets \(F_0,F_1,F_2\) require two
cancelling coordinates. Consecutive flip sets are disjoint, so both
cancellations occur between \(F_0,F_2\), forcing \(F_0=F_2\).
Call this two-coordinate set \(A\).

The coordinates at positions 0 and 2 have been used twice. Position 4
cannot share coordinates with its consecutive positions 3 and 5, or with
0 and 2. It can only pair with position 1. Thus \(F_1=F_4=B\), and the
remaining two-coordinate set gives \(F_3=F_5=D\). These three blocks
partition all six coordinates.

After translating \(p_0\) to zero, the six words are

\[
 0,\ A,\ A+B,\ B,\ B+D,\ D,
\]

where a block denotes its indicator word. This is a pair-coordinate cube
with the two adjacent messages \(A+D\) and \(A+B+D\) omitted.

Choose \(x\) with the coordinate pairs \(01\) in \(A\), \(01\) in
\(B\), and \(11\) in \(D\). Its parity is even, as is the normalized
set. The first two blocks contribute one to its distance from every
listed center. Consequently the centers at distance two from \(x\)
are exactly those with their \(D\) block equal to \(11\): only \(B+D\)
and \(D\). Those two centers are distance two apart, not four. This
violates (M).

There is therefore no opposite chord, and \(G_P\) is exactly a six-cycle.

## 7. The four occurrence structures and their missing midpoints

The edges of \(T\) now join positions at cyclic distance two or three.
Distance-two edges cannot be parallel: two common coordinates of
\(F_i,F_{i+2}\) would produce the opposite chord just excluded.
Such edges form simple subgraphs of the two triangles on positions
\(\{0,2,4\}\) and \(\{1,3,5\}\). The distance-three edges join the
opposite pairs \((0,3),(1,4),(2,5)\), each with multiplicity
\(\lambda\in\{0,1,2\}\).

An endpoint with opposite-pair multiplicity \(\lambda\) has degree
\(2-\lambda\) within its triangle. The two endpoints of an opposite
pair have the same internal degree. A simple graph on three vertices is
empty, a single edge, a two-edge path, or a triangle, with degree sequences

\[
 (0,0,0),\ (0,1,1),\ (1,1,2),\ (2,2,2).
\]

Therefore, up to ordering the opposite pairs, the only multiplicity types
are \(222,211,110,000\). Once these degrees are specified, each of the
two internal triangle subgraphs is uniquely determined. Rotations and
reflections of the cycle induce every permutation of its three opposite
pairs, so the following representatives exhaust the possibilities.

Here \(a,b,c,d,e,f\) are the six distinct coordinate names. A string such
as \(ab\) denotes the indicator word of those coordinates, and \(0\)
denotes the all-zero word. The displayed words are successive XORs of
the flip sets, with \(p_0=0\).

| Type | \(F_0,F_1,F_2,F_3,F_4,F_5\) | The six words | Missing midpoint |
|---|---|---|---|
| 222 | \(ab,cd,ef,ab,cd,ef\) | \(0,ab,abcd,abcdef,cdef,ef\) | none |
| 211 | \(ab,cf,de,ab,ce,df\) | \(0,ab,abcf,abcdef,cdef,df\) | \(ae\) |
| 110 | \(ab,ce,af,cd,be,df\) | \(0,ab,abce,bcef,bdef,df\) | \(cd\) |
| 000 | \(ac,df,ab,de,bc,ef\) | \(0,ac,acdf,bcdf,bcef,ef\) | \(ab\) |

Each listed flip set has two coordinates, and each coordinate appears
exactly twice. The exclusions are direct distance calculations:

- In type 211, the only centers at distance two from \(ae\) are \(0,ab\).
- In type 110, the only centers at distance two from \(cd\) are \(0,df\).
- In type 000, the only centers at distance two from \(ab\) are \(0,ac\).

In each case every other center is distance four from the indicated word,
and the two available centers are distance two apart. Each missing word
has even parity, so (M) fails.

Type 222 gives three paired coordinate blocks \(A=ab,B=cd,D=ef\).
Its messages are \(000,100,110,111,011,001\), omitting the opposite
messages \(010,101\). Translation by the whole block \(B\) changes
the omitted messages to \(000,111\), giving exactly \(P_*\).
This proves the necessary direction of Theorem 1.

## 8. Converse and antipodal structure

The set \(P_*\) is closed under complements: a message of weight one is
sent to one of weight two, and conversely. We verify (M) for all even
words, without assuming that the word itself has paired coordinates.

- A word of weight zero is a midpoint of any two distinct weight-two
  full-pair centers.
- For a word of weight two whose ones fill one coordinate pair, use the
  two weight-four centers containing that pair and respectively one of
  the other two pairs. Each is distance two from the word, and the
  centers are distance four apart.
- For a word of weight two whose ones lie in two different pairs, use
  the two full-pair centers corresponding to those pairs. Each mixed
  pair contributes one to the relevant distance, so both distances are
  two and the centers are distance four apart.
- Complementation reduces weights four and six to the preceding cases.

These are all even weights. Translation and coordinate permutation
preserve (M), proving the converse. In the message cube, the distance-two
graph of \(P_*\) is the three-cube with the opposite vertices \(000,111\)
deleted, which is a six-cycle. Complementation commutes with translation
and coordinate permutation, so every classified set remains antipodally
closed and has the same triangle-free distance-two graph.

## 9. An opposite-parity degree consequence

Let \(P\) be a classified six-point set of parity \(\varepsilon\), and
let \(q\) have the opposite parity. Distinct words at distance one from
\(q\) differ by flipping different coordinates; they are pairwise at
distance two. Thus three such words in \(P\) would form a triangle in
its distance-two graph. There are at most two.

The antipodal bijection of \(P\) sends a word at distance one from \(q\)
to one at distance five from \(q\), and vice versa. Consequently

\[
 |\{p\in P:d(q,p)=5\}|
   =|\{p\in P:d(q,p)=1\}|\le2.
\]

All these distances are odd and hence belong to \(\{1,3,5\}\).
At least four of the six words therefore satisfy \(d(q,p)\le3\).
This consequence uses the actual antipodal and triangle-free geometry;
it is not obtained from a numerical count assumption alone.

## 10. Excluding every twelve-center feasible set

Recall the projection argument from the earlier
[nonlinear constraints](q6-strong-product-affine-obstruction.md#3-constraints-on-arbitrary-product-center-sets).
For every \(x\in V\), the second projection of

\[
 C_x=\{(a,b)\in C:d(x,a)\le2\}
\]

must radius-two cover \(V\). The single-factor obstruction says that
this projected set cannot be a distance-four packing. Choose two distinct
projected words at distance at most three and lift them to centers in
\(C_x\). Product packing forces their first coordinates to be distance
at least four, while their two distances from \(x\) have sum at most four.
Equality gives two first-coordinate words at distance four with \(x\)
as their midpoint. They have the same parity as \(x\). This proves (M)
for each parity projection; exchanging blocks gives the other two cases.

The earlier projection lower bound gives at least six distinct words in
each of these four parity projections. For \(|C|=12\), each block thus
has exactly twelve distinct projected words, so both projections are
injective and every parity class has exactly six words. Theorem 1 applies
to all four classes.

For a block projection \(R\), define its **short graph** by distances
at most three between distinct words, and its **long graph** by distances
at least four. These two simple graphs partition the edges of the complete
graph on its twelve words.

Fix \(q\in R\). Within its own parity class, it has exactly two
distance-two neighbors, since that graph is a six-cycle. The opposite
parity class supplies at least four short neighbors by Section 9.
Hence every vertex of the short graph has degree at least six, and every
vertex of the long graph has degree at most

\[
 11-6=5.
\]

The two injective projections of \(C\) define a bijection \(f\) from
the first block projection to the second, using the common center index.
Every short edge \(aa'\) in the first projection must map to a long
edge \(f(a)f(a')\) in the second: otherwise both block distances would
be at most three, violating packing.

A first-block vertex has at least six distinct short neighbors. Their
images under the bijection would be six distinct long neighbors of its
second-block image, whose long degree is at most five. This contradiction
excludes every twelve-center feasible set.

The previous layer bound excluded sizes below twelve, and its diameter-three
anticode bound gives \(|C|\le21\). Thus every feasible set must have
\(13\le|C|\le21\), proving Theorem 2. These bounds are necessary; they
do not assert that any size in this interval is attainable.

## 11. Formalization boundary

The earlier
[single-factor Lean source](proof/Q6PackingDomination.lean) and its
[verification receipt](results/q6-packing-domination-verification.json)
establish the factor obstruction over arbitrary sets of actual six-bit
words. They do not formalize Theorem 1 or Theorem 2 of this note.

The additional [Lean geometry source](proof/Q6AntipodalCompatibility.lean)
proves `antipodal_trianglefree_opposite_has_four_near`: for a six-point
same-parity set assumed antipodally closed with a triangle-free distance-two
graph, an opposite-parity vertex has at least four words at Hamming distance
at most three. It uses actual `BitVec 6` words and a natural-number count of
their six coordinate differences. It proves the distance-one-neighbor
triangle relation and the complementary-distance bijection, rather than
assuming neighborhood counts. The structural hypotheses remain explicit.
This does not formalize the classification or the twelve-center theorem.

Its three closed geometric certificates each have at most \(64^2\) cases
and use ordinary `decide`; translating a common neighbor to zero avoids a
\(64^3\) certificate. No six-subset enumeration is used. Actual runs and
all fifteen axiom outputs are recorded separately in the
[geometry verification receipt](results/q6-antipodal-compatibility-verification.json).
From the pinned `002-weighted-rectangular-pruning/proof/mathlib` package, run
`lake env lean ../../../notes/proof/Q6AntipodalCompatibility.lean`.

The classification, its graph reductions, the projection interpretation and
the final degree coupling remain complete written proofs. Neither the old
factor audits nor the new conditional geometry audits remove this boundary.

## 12. Classical background and scope of the contribution

Coordinate labels of cube and half-cube embeddings are classical.
Deza and Shpectorov's *Recognition of the \(\ell_1\)-graphs with Complexity
\(O(nm)\), or Football in a Hypercube*, LIENS-95-11 (1995), Section 4,
Lemma 4.2(2), treats an isometric even cycle of length \(2t\) under an
\(s\)-isometric embedding into a halved cube, with \(t\le s\).
It identifies equal coordinate labels on opposite cycle edges and disjoint
labels on non-opposite edges; an edge label is the two-coordinate
symmetric difference of its endpoints.
[Original research report](https://www.di.ens.fr/reports/1995/liens-95-11.pdf).
For the final classified six-cycle the relevant scale is \(s=t=3\).
The repeated coordinate labels and paired-coordinate cycle structure are
therefore not claimed as new embedding theory.

The proof here starts from full parity-midpoint coverage, rather than
assuming that the distance-two graph is an isometrically embedded cycle.
Sections 2–7 force the cycle structure, and the three failed occurrence
types in Section 7 show why cycle adjacency alone would not suffice for
the full midpoint condition. The coordinate argument is included in full
so the classification does not depend on importing a cycle-embedding
theorem with unchecked hypotheses. Whether the exact midpoint-forcing
classification or its particular product consequence already occurs in
the literature remains unconfirmed. No first-proof or priority claim is made.

Bujtás, Iršič Chenoweth, Klavžar and Zhang's Conjecture 3.1 in *On d-distance
p-packing domination number in strong products* asks whether

\[
 \gamma_d^p(G)=\infty
 \quad\Longrightarrow\quad
 \gamma_d^p(G\boxtimes H)=\infty\text{ for every }H.
\]

We use finite nonempty factors, as in the preceding note.
[Original preprint, Section 3](https://arxiv.org/html/2510.02749v1),
[published article](https://link.springer.com/article/10.1007/s00026-026-00814-0).
A counterexample would need only **one** infeasible factor \(G\) and a
feasible product for some \(H\); it need not have two infeasible factors.
Our choice \(G=H=Q_6\) is one test case, not a restriction justified by
the original quantifiers. The factor obstruction is known here, but the
product's nonlinear sizes 13 through 21 remain unresolved. No resolution
or counterexample to the original public conjecture is asserted.
