# An affine-code obstruction in the strong product of two six-cubes

We prove that no binary affine subspace of
\(\mathbb F_2^6\times\mathbb F_2^6\) is simultaneously a distance-three
packing and a distance-two dominating set of \(Q_6\boxtimes Q_6\).
The packing distance is at least **four**, and covering requires distance at
most **two in each block from the same center**. We also prove the complete
single-factor obstruction and necessary conditions for arbitrary nonlinear
product center sets.

The product theorem has a complete written proof below. The accompanying
[Lean source](proof/Q6PackingDomination.lean) proves the nonexistence of a
radius-two covering distance-four packing for every subset of the six-bit
Hamming space. The packing size bound, product theorem and shortest-path
interpretation in a `SimpleGraph` are not formalized. Actual
compilation and axiom-audit results are recorded in the
[verification receipt](results/q6-packing-domination-verification.json).
Historical originality of the particular product obstructions in this note has not been
established. The general strong-product conjecture remains unresolved here.

## 1. Problem, metric and statements

For a finite simple undirected graph \(G\), a set \(S\subseteq V(G)\) is
\(d\)-dominating if its closed radius-\(d\) balls cover \(V(G)\), and is a
\(p\)-packing if distinct centers have graph distance at least \(p+1\).
Here \(d,p\) are nonnegative integers; distances between different connected
components are \(\infty\). Write \(\gamma_d^p(G)=\infty\) when no set satisfies
both conditions.

Bujtás, Iršič Chenoweth, Klavžar and Zhang formulate the following as
Conjecture 3.1 in *On d-distance p-packing domination number in strong products*:

\[
 \gamma_d^p(G)=\infty
 \quad\Longrightarrow\quad
 \gamma_d^p(G\boxtimes H)=\infty\text{ for every }H.
\]

We use finite **nonempty** factors. Allowing an empty second factor makes the
product empty and removes the intended obstruction. The published article
still presents the conjecture as open; its remaining parameter range is
\(d<p<2d\), whose smallest instance is \((d,p)=(2,3)\).
[Original preprint, §3](https://arxiv.org/html/2510.02749v1),
[published article, DOI 10.1007/s00026-026-00814-0](https://link.springer.com/article/10.1007/s00026-026-00814-0).
The literature check of 2026-10-09 did not obtain a subsequent complete
resolution; this does not exclude unindexed or inaccessible developments.

Let \(V=\mathbb F_2^6\). Addition is coordinatewise XOR,
\(\operatorname{wt}(x)\) is Hamming weight, and
\(d_H(x,y)=\operatorname{wt}(x+y)\). The graph \(Q_6\) has vertex set \(V\)
and joins vertices differing in one coordinate. Its shortest-path distance is
\(d_H\): every differing coordinate must be flipped, and flipping precisely
those coordinates gives a path of that length.

The strong product joins distinct pairs when each coordinate is either equal
or adjacent in its factor. Consequently its distance is

\[
 d_\infty((x,y),(a,b))=\max\{d_H(x,a),d_H(y,b)\}.
\]

Each product step changes at most one bit in each block, giving the lower
bound. Paths in the two factors can be followed simultaneously, with the
shorter one waiting after it ends, giving the matching upper bound.
Thus its closed radius-two ball is \(B_2(a)\times B_2(b)\), where
\(B_2(a)=\{x:d_H(x,a)\le2\}\).

Call \(C\subseteq V\times V\) **feasible** when

\[
 \begin{split}
 &\max\{d_H(a,a'),d_H(b,b')\}\ge4
       &&\text{for all distinct }(a,b),(a',b')\in C,\\
 &\forall(x,y)\in V\times V\ \exists(a,b)\in C:
       d_H(x,a)\le2\ \text{and}\ d_H(y,b)\le2.
 \end{split}
\]

This is a maximum of two Hamming distances, not the ordinary length-twelve
Hamming distance, which is their sum.

**Theorem 1 (single factor).** Every subset of \(V\) with pairwise Hamming
distance at least four has at most four elements and fails to cover \(V\) by
closed radius-two balls. In particular, \(\gamma_2^3(Q_6)=\infty\).

**Theorem 2 (nonlinear necessary conditions).** Every feasible
\(C\subseteq V\times V\) satisfies \(12\le |C|\le21\). For either block
and either parity \(\varepsilon\), let \(P_\varepsilon\) be the set of
distinct projected words of that parity. Then \(|P_\varepsilon|\ge6\), every
coordinate is nonconstant on \(P_\varepsilon\), and every member has at least
two neighbors at distance two and at least two neighbors at distance four
within \(P_\varepsilon\). If \(|C|=12\), both block projections are injective
and each has exactly six words of each parity.

The subsequent [six-point midpoint classification](q6-six-point-midpoint-classification.md)
excludes this twelve-center boundary, strengthening the necessary window
to \(13\le |C|\le21\). Its full classification and product consequence
are written proofs; the separate Lean geometry retains explicit antipodal
and triangle-free hypotheses.

**Theorem 3 (affine obstruction).** No affine subspace of \(V\times V\) is
feasible. More specifically, a four-dimensional linear packing subspace has
a projection with constant weight parity.

Theorem 3 excludes one entire construction family. It neither constructs a
counterexample to Conjecture 3.1 nor excludes general nonlinear center sets
in this product, or center sets in \(Q_6\boxtimes H\) for arbitrary \(H\).

## 2. Complete single-factor proof

Consider \(M\) distinct binary words of length six. If coordinate \(j\) has
\(t_j\) ones, the sum of all unordered pair distances is

\[
 \sum_{u<v}d_H(u,v)=\sum_{j=1}^6 t_j(M-t_j).
\]

If a distance-four packing contained five words, those five would have total
pair distance at least \(4\binom52=40\), whereas every coordinate contributes
at most \(2\cdot3=6\), giving at most 36. Thus every such packing has size
at most four. This is the standard Plotkin counting mechanism.

Every radius-two ball has size \(1+6+\binom62=22\). Zero, one or two centers
therefore cover at most 44 of the 64 vertices. Three and four centers require
the equality structures of the same distance count.

### Three centers

For three centers the total distance is at least 12 and at most
\(6\cdot2=12\). All three pair distances are consequently four.
Translation and coordinate permutation preserve distances and ball unions.
Translate the first center to zero and write the other two as \(u,v\).
Their supports have size four and intersect in two coordinates. Their
intersection and their two support differences partition the six coordinates
into three pairs. Hence every three-center packing is equivalent to

\[
 0=(00,00,00),\qquad u=(11,11,00),\qquad v=(11,00,11).
\]

For two centers at distance four, a point in their two radius-two balls must
agree with their common coordinates and choose exactly two of the four
differing coordinates. The ball intersection thus has \(\binom42=6\) points.

A point in \(B_2(0)\cap B_2(u)\cap B_2(v)\) must have weight two with both
its support coordinates in \(\operatorname{supp}(u)\cap\operatorname{supp}(v)\).
Indeed, if its weight is \(w\le2\), distance at most two from a weight-four
word requires \(4+w-2|\operatorname{supp}(z)\cap\operatorname{supp}(u)|\le2\),
forcing \(w=2\) and support containment; the same applies to \(v\).
The triple intersection is therefore the single point \((11,00,00)\).
Inclusion-exclusion gives

\[
 \left|B_2(0)\cup B_2(u)\cup B_2(v)\right|
   =3\cdot22-3\cdot6+1=49<64.
\]

### Four centers

For four centers the total distance is at least \(6\cdot4=24\) and at most
\(6\cdot4=24\). Every pair distance is four and every coordinate splits the
four words two against two. After translating the first word to zero, each
column has two ones among the remaining three words. Let the multiplicities
of the three possible column types be \(a,b,c\). The three distances from
zero give \(a+b=a+c=b+c=4\), so \(a=b=c=2\).
Every four-center packing is therefore equivalent to the doubled simplex

\[
 \{(00,00,00),(11,11,00),(11,00,11),(00,11,11)\}.
\]

Its six pairwise ball intersections have size six. Each of its four
three-center subsets has the structure just proved, so each triple
intersection has size one. The intersection of all four balls is empty:
the sole intersection point \((11,00,00)\) for the first three centers has
distance six from the fourth. Thus the ball union has size

\[
 4\cdot22-6\cdot6+4\cdot1=56<64.
\]

The eight omitted points are explicit: choose either \(01\) or \(10\) in
each coordinate pair. Each chosen pair is distance one from both \(00\) and
\(11\), so every such point has distance three from every center.
All possible packing sizes have now been handled, proving Theorem 1.
No linearity assumption was used.

## 3. Constraints on arbitrary product center sets

### Constant parity prevents covering

Suppose all first coordinates of a product packing \(C\) have parity
\(\varepsilon\). Choose \(x\in V\) of the opposite parity and consider

\[
 C_x=\{(a,b)\in C:d_H(x,a)\le2\}.
\]

Parity forces \(d_H(x,a)=1\) for every member of \(C_x\). Any two of its
first coordinates are therefore at distance at most two. Product packing
forces their second coordinates to be distinct and at distance at least four.
If \(C\) covered the layer \(\{x\}\times V\), these second coordinates would
radius-two cover \(V\), contradicting Theorem 1. An empty \(C_x\) also fails
to cover that layer. Interchanging the blocks proves the parity assertion
of Theorem 2 for all center sets, including nonlinear ones.

### Size bounds

Product radius-two balls have size \(22^2=484\). As
\(8\cdot484=3872<4096=|V\times V|\), covering requires at least nine centers.
This elementary volume bound can be strengthened by counting fixed layers.

First, every radius-two cover of \(V\), without any packing assumption,
needs at least four distinct centers. At most two centers cover at most 44
vertices. For three distinct centers, their three pair distances have sum at
most \(6\cdot2=12\), by the coordinate count in Section 2. They cannot all
be at least five, so some pair has distance \(t\) with \(1\le t\le4\).

The sizes of intersections of two radius-two balls at these distances are

| Center distance \(t\) | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| \(\lvert B_2(a)\cap B_2(b)\rvert\) | 12 | 12 | 6 | 6 |

To obtain the table, translate \(a\) to zero and let \(b\) be one on its
\(t\) differing coordinates. An intersection point with \(i\) ones in
these coordinates and \(j\) in the others has distances \(i+j\) and
\(t-i+j\) from the two centers. Thus the exact count is

\[
 \sum_{i=0}^{t}\binom ti
       \sum_{j=0}^{\min(2-i,\,2-t+i)}\binom{6-t}{j},
\]

where an inner sum with negative upper limit is zero. For \(t=1\) the two
contributions are 6 and 6; for \(t=2\) they are 1, 10 and 1; for \(t=3\)
the nonzero contributions are 3 and 3; for \(t=4\) the only contribution is
\(\binom42=6\). The identified pair therefore overlaps in at least six
vertices, so the union of all three balls has size at most
\(3\cdot22-6=60<64\). This proves the four-center lower bound.

Now suppose \(C\) covers \(V\times V\). For every fixed \(x\in V\),
the second-coordinate projection of
\(C_x=\{(a,b)\in C:d_H(x,a)\le2\}\) must radius-two cover \(V\).
That projection has at least four distinct words, hence \(|C_x|\ge4\),
even if several centers in \(C_x\) have the same second coordinate.
Each center belongs to exactly 22 of these 64 slices, giving

\[
 22|C|=\sum_{x\in V}|C_x|\ge64\cdot4=256,
 \qquad |C|\ge\left\lceil\frac{256}{22}\right\rceil=12.
\]

This lower bound requires only covering.

For the upper bound use the diameter-three set

\[
 A=\{(\eta,z):\eta\in\mathbb F_2,\ z\in\mathbb F_2^5,
                                  \operatorname{wt}(z)\le1\}.
\]

It has \(2(1+5)=12\) points; two of its points differ in at most one first
coordinate and two remaining coordinates. For each \(t\in V\), restrict
product centers to those whose first coordinate lies in \(t+A\). Their
second coordinates form a distance-four packing, without repetitions, so
Theorem 1 bounds their number by four. Each fixed first coordinate lies in
exactly 12 of the 64 translates: the corresponding translations are
\(t=a+u\) for \(u\in A\). Counting center-translation incidences gives

\[
 12|C|\le64\cdot4,\qquad |C|\le\lfloor256/12\rfloor=21.
\]

This upper bound uses only packing, and permits repeated first coordinates.
Together with the layer lower bound it proves Theorem 2. Neither bound is
asserted to be sharp for feasible sets.

### A midpoint condition in every layer

There is also a necessary pair structure. For every \(x\in V\), a feasible
set has centers \((a,b),(a',b')\) such that

\[
 d_H(a,a')=4,\qquad d_H(x,a)=d_H(x,a')=2,
 \qquad b\ne b',\quad d_H(b,b')\le3.
\]

Indeed, the second projection of \(C_x\) covers \(V\). By Theorem 1 it
cannot be a distance-four packing, so it has two distinct words \(b,b'\)
at distance at most three. Lift them to centers in \(C_x\); product packing
forces \(d_H(a,a')\ge4\), while the triangle inequality gives
\(d_H(a,a')\le d_H(a,x)+d_H(x,a')\le4\). All inequalities are equalities,
including both distances from \(x\). Thus every \(x\) is a Hamming midpoint
of a distance-four first-coordinate pair whose second coordinates are close.
Equivalently, \(x\) agrees with the pair on their common coordinates and
matches one endpoint on two of their four differing coordinates and the other
endpoint on the remaining two.
Repeated second coordinates in \(C_x\) do not affect the argument: it uses
the set of distinct projected words. Interchanging the blocks gives the
corresponding condition for every second-coordinate layer.

### Parity projections and their local structure

Fix one parity \(\varepsilon\), and let \(P_\varepsilon\) be the set of
distinct first-coordinate words of this parity. The midpoint condition means
that every one of the 32 words \(x\) of parity \(\varepsilon\) is distance
two from two members of \(P_\varepsilon\) at distance four from each other.
The endpoints have the same parity as \(x\), since their distances from it
are two. In particular \(P_\varepsilon\) is nonempty.

No coordinate can be constant on \(P_\varepsilon\). A Hamming midpoint
agrees with its two endpoints on every coordinate where they agree, as shown
above. If coordinate \(j\) had one fixed value on \(P_\varepsilon\), every
midpoint of its pairs would have that value too. But 16 of the 32 words of
parity \(\varepsilon\) have the opposite value at \(j\), contradicting
midpoint coverage.

Take any \(p\in P_\varepsilon\). Applying the midpoint condition to \(x=p\)
gives two distinct other members at distance two from \(p\). Apply it next
to \(x=p+\mathbf1\). Complementing all six bits preserves parity, and
\(d_H(p,q)=6-d_H(p+\mathbf1,q)\); the two resulting members are distance
four from \(p\). These distance-two and distance-four neighbor sets are
disjoint and exclude \(p\), so \(|P_\varepsilon|\ge5\). This also proves
the two asserted minimum neighbor counts for every member.

Suppose \(|P_\varepsilon|=5\). Each word then has exactly two distance-two
and two distance-four neighbors. The simple graph on these five words with
distance-two pairs as edges is 2-regular, hence a five-cycle: each component
of a finite simple 2-regular graph is a cycle of length at least three, and
five cannot split into two such component sizes. Traverse the cycle once.
Its five edges each flip exactly two coordinates, for ten flips in total.
Each coordinate flips an even number of times on this closed traversal; a
nonconstant coordinate flips at least twice. Six nonconstant coordinates
would require at least twelve flips. Thus some coordinate is constant on
all five words, contradicting the preceding midpoint argument.
Consequently \(|P_\varepsilon|\ge6\).

The reasoning applies to both parities and, after exchanging the blocks, to
the second projection. These are counts of distinct projected words, so
repeated coordinates of centers cannot repair a five-word projection.
If \(|C|=12\), each block projection has at least \(6+6=12\) distinct words
and at most \(|C|=12\); it is therefore injective, and both parity classes
have exactly six words. This completes the stronger projection assertions
in Theorem 2. The twelve-center boundary is a necessary structure, not an
existence assertion or a contradiction.

## 4. Linear reduction and character count

Let \(C\le V\times V\) be a linear packing subspace, of dimension \(m\).
The preceding upper bound gives \(2^m\le21\), so \(m\le4\). If \(m\le3\),
the volume bound excludes covering. It remains to analyze \(m=4\).

Choose a linear isomorphism \(W=\mathbb F_2^4\to C\), written
\(s\mapsto(L_1s,L_2s)\), and define

\[
 H_i=\{s\in W:\operatorname{wt}(L_is)\ge4\},\qquad
 E=W\setminus\{0\}.
\]

Linearity makes packing equivalent to \(H_1\cup H_2=E\): every nonzero
center difference is a nonzero codeword, and the parameter map is injective.
Both \(H_i\) exclude zero. We will show that this equality is impossible
if parity is nonconstant in both block images. The previous section then
excludes covering.

For one block map \(L\), let \(U=\operatorname{im}L\),
\(r=\dim U\le4\), and \(D=U^\perp\) under the binary dot product.
The image has nonconstant parity exactly when the all-one vector
\(\mathbf1\) does not belong to \(D\). The standard finite orthogonality
identity is

\[
 1_U(z)=\frac1{|D|}\sum_{a\in D}(-1)^{a\cdot z}.
\]

For \(z\in U\) all summands are one. Otherwise there is an
\(a_0\in D\) with \(a_0\cdot z=1\), by \((U^\perp)^\perp=U\);
translation by \(a_0\) pairs opposite summands and gives zero.

For \(\operatorname{wt}(a)=j\), define
\(T(j)=\sum_{\operatorname{wt}(z)\ge4}(-1)^{a\cdot z}\).
Complementing \(z\) turns the weight range into zero, one and two. Their
character sums give

\[
 T(j)=(-1)^j\left(1+(6-2j)+\frac{(6-2j)^2-6}{2}\right).
\]

The weight-two term follows directly from
\(\binom{6-j}{2}+\binom j2-j(6-j)\). The exact table is

| \(j\) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| \(T(j)\) | 22 | −10 | 2 | 2 | −2 | −2 | 10 |

Orthogonality yields the number of high-weight words in the image:

\[
 h(U)=|\{z\in U:\operatorname{wt}(z)\ge4\}|
     =\frac1{|D|}\sum_{a\in D}T(\operatorname{wt}(a)).
\]

Assume nonconstant parity. Then every nonzero dual word has weight from one
through five, hence contributes at most two to this sum.

* If \(r=4\), then \(|D|=4\), so \(h(U)\le(22+6)/4=7\).
  The map \(L\) is injective and consequently \(|H|\le7\).
* If \(r=3\), then \(|D|=8\), so \(h(U)\le36/8\). Integer-valuedness
  gives \(h(U)\le4\). Each image word has two preimages, giving \(|H|\le8\).
* If \(r=2\), parity on \(U\) is a nonzero linear functional. Among its
  three nonzero words, two are odd and one is even. An odd high-weight word
  must have weight five. If both odd words have weight five, their sum has
  weight two, since they omit distinct coordinates from \(\mathbf1\);
  the nonzero even word is then not high. If at most one odd word is high,
  adding the possible even high word still gives at most two.
  Hence \(h(U)\le2\), and the four preimages of each word give \(|H|\le8\).
* If \(r=1\), at most the single nonzero image word is high. Its eight
  preimages give \(|H|\le8\). Rank zero has constant parity and is excluded
  by the assumption.

The separate rank-two argument is necessary: the character upper bound alone
would only give \(h(U)\le3\).

## 5. Extremal high sets and XOR

For a finite set \(S\) of binary vectors write
\(\sigma(S)=\sum_{s\in S}s\), its coordinatewise XOR.

### Low-rank sets

When \(r\le3\), choose \(0\ne k\in\ker L\). Translation by \(k\)
preserves \(H\) and partitions it into pairs \(\{s,s+k\}\), with no fixed
points. In particular \(|H|\) is even. If \(|H|=8\), the four pairs each
have XOR \(k\), so \(\sigma(H)=4k=0\). This does not require \(H\) itself
to be a subspace.

### Rank four with seven high words

Suppose \(r=4\) and \(|H|=7\). Equality in the character bound forces all
three nonzero words of \(D\) to have \(T=2\), so their weights lie in
\(\{2,3\}\). Their sum is zero, so an even number have odd weight.
The only possible weight multisets are \((2,2,2)\) and \((2,3,3)\).

In the first case two independent weight-two dual words must have supports
intersecting in one coordinate, since their sum also has weight two.
After a coordinate permutation they are \(e_1+e_2\) and \(e_1+e_3\).
Thus

\[
 U=\{(t,t,t,b,c,d):t,b,c,d\in\mathbb F_2\}.
\]

Its seven high words have \(t=1\) and \((b,c,d)\ne(0,0,0)\).
Their XOR is \((1,1,1,0,0,0)\ne0\): each last coordinate occurs four times.

In the second case the two weight-three dual words have support intersection
of size two, because their sum has weight two. They can be placed at
\(e_1+e_2+e_3\) and \(e_1+e_2+e_4\), giving

\[
 U=\{(u,v,u+v,u+v,e,f):u,v,e,f\in\mathbb F_2\}.
\]

The choices \((u,v)=(1,0)\) and \((0,1)\) each give three high words,
with \((e,f)\ne(0,0)\). The choice \((u,v)=(1,1)\) gives only
\((e,f)=(1,1)\), and \((u,v)=(0,0)\) gives none. In parameters
\((u,v,e,f)\), the two groups have XOR \((1,0,0,0)\) and \((0,1,0,0)\);
the last word is \((1,1,1,1)\). The total parameter XOR is \((0,0,1,1)\),
whose image is \((0,0,0,0,1,1)\ne0\).

These classifications exhaust the equality cases. Since \(L:W\to U\) is
an isomorphism, the nonzero image XOR implies \(\sigma(H)\ne0\).
Different block maps may use different coordinates or parameters in this
classification; nonzero XOR is invariant under linear isomorphism, so the
conclusion holds in their common original message space \(W\).

## 6. Completing the affine obstruction

Each coordinate occurs as one in exactly eight members of
\(E=\mathbb F_2^4\setminus\{0\}\), so \(\sigma(E)=0\).
Assume both block images have nonconstant parity and the code is packed.
The equality \(H_1\cup H_2=E\), with \(|E|=15\) and each \(|H_i|\le8\),
leaves only two cases, up to swapping blocks.

1. The sizes are eight and seven, with empty intersection. The eight-element
   set has low rank and XOR zero. The seven-element set cannot have low rank,
   since such sets have even size; it has rank four and nonzero XOR. Their
   union consequently has nonzero XOR, contradicting \(\sigma(E)=0\).
2. Both sizes are eight and their intersection is exactly \(\{z\}\) with
   \(z\in E\), hence \(z\ne0\). Both individual XORs are zero. Over
   \(\mathbb F_2\),

   \[
    \sigma(H_1\cup H_2)
      =\sigma(H_1)+\sigma(H_2)+\sigma(H_1\cap H_2)=z\ne0,
   \]

   again a contradiction.

Thus every four-dimensional linear packing subspace has a constant-parity
block projection. Section 3 excludes covering for any such code.
The volume bound already handled lower dimensions, and the packing size
bound excluded higher dimensions. No linear subspace is feasible.

Finally an affine subspace is \(c_0+C_0\) for a linear subspace \(C_0\).
Translation by \(c_0\) preserves all distances and is a bijection of the
ambient space, preserving covering as well. A feasible affine subspace would
therefore yield a feasible linear subspace. This proves Theorem 3.

The projection constraints also give a shorter exclusion of feasible linear
codes. Each block projection of such a code has at least 12 distinct words,
so its linear rank is at least four. The packing size bound gives
\(\dim C\le4\), hence \(\dim C=4\) and both block ranks are four. Both
images have nonconstant parity, so Section 4 gives \(|H_1|,|H_2|\le7\).
They cannot cover the 15 nonzero messages required by packing. This argument
uses constraints derived from covering; the XOR proof above proves the
stronger constant-parity conclusion for every four-dimensional linear
packing, whether or not it covers.

## 7. Formalization and relation to prior work

The Lean theorem `Q6PackingDomination.no_packing_cover` quantifies over every
`S : Set (BitVec 6)`. Its hypothesis `Packing S` requires Hamming distance
at least four between distinct members; `Covers2 S` would cover every actual
six-bit vertex at distance at most two. The stronger theorem
`packing_has_uncovered` constructs a vertex at distance greater than two
from every center, including when the center set is empty. `distance_bits`
identifies the metric with the sum of six coordinate differences, using
natural-number counts rather than a bit-vector count that could wrap around.

The formal proof translates one center to zero and uses closed finite
certificates on the 22 words of weight at least four. Its largest certificate
has \(22^3\) index cases; these are kernel-checked with `decide`. The proof
then applies them to an arbitrary set, rather than enumerating the powerset
of the 64 vertices. This certificate proof and the Plotkin/equality proof in
Section 2 establish the same complete finite-code obstruction by different
arguments. The graph shortest-path interpretation, nonlinear product
constraints and affine product theorem are written mathematics in this note.

The counting, diameter-three anticode, binary character orthogonality and
weight-enumerator sums are classical coding tools; the doubled simplex is a
classical code structure. We do not claim these tools, the factor bound or
the block-maximum metric as new.

Miyamoto and Firer study the maximum of component metrics and prove that
products of equal-radius balls are balls in that metric. Their tiling results
concern perfect codes, with disjoint covering balls.
[Metrics which turn tilings into binary perfect codes, 1903.05951v2](https://arxiv.org/html/1903.05951v2),
[Obtaining binary perfect codes out of tilings, 1904.10789v2](https://arxiv.org/html/1904.10789v2).
For the present parameters, radius-two balls around centers at distance four
may overlap. Moreover \(484\nmid4096\), which excludes a disjoint tiling by
these balls but does not exclude an overlapping covering. A perfect-code
factor theorem therefore cannot simply replace the proof above.

The checked literature did not supply an exact prior theorem for this
six-plus-six affine obstruction; that is not evidence of historical priority.
No historical priority is claimed for the nonlinear projection constraints
either.
The subsequent [midpoint classification and coupling proof](q6-six-point-midpoint-classification.md)
excludes all twelve-center sets. The outstanding case is an arbitrary
nonlinear center set of size between 13 and 21 satisfying the projection and
coupled midpoint conditions. No such set is constructed or excluded here,
and no resolution of the original conjecture is asserted.
