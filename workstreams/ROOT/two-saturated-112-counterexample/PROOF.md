# Exact construction and complete contradiction

Use seven distinct vertices a,b,c,z,x_a,x_b,x_c and exactly the edges

    ab, ac, bc, a x_a, b x_b, c x_c, z x_a, z x_b, z x_c.

The labels in `candidate.json` and the Lean graph are

    a=0, b=1, z=2, c=3, x_b=4, x_c=5, x_a=6.

Thus the numerical edge list is

    01, 03, 06, 13, 14, 24, 25, 26, 35.

The triangle is 0,1,3. The three spokes through z have length two.
There are no loops or repeated edges. The graph is connected, and the
vertex degrees in numerical order are [3,3,3,3,2,2,2].

A graph is subcubic if every degree is at most three. It is 2-saturated
if every degree-three vertex has at most two degree-three neighbors.
Here a,b,c each have two such neighbors and z has zero. These are the
hypotheses of [the printed Conjecture 3](https://arxiv.org/html/2603.25113v1#S5).

A (1,1,2)-packing coloring uses three distinct labels A,B,C. Equal A
labels and equal B labels must have original-graph distance greater than
one; equal C labels must have distance greater than two. In particular,
every pair of adjacent vertices has different labels.

Assume such a coloring. The three mutually adjacent vertices a,b,c
cannot use only A,B, so one has label C. Permute their names to call it a.
Every other vertex is within distance two of a: b,c,x_a are adjacent;
z is reached by a–x_a–z; x_b by a–b–x_b; x_c by a–c–x_c.
No other vertex can therefore have label C. However,

    b–c–x_c–z–x_b–b

is an actual five-cycle avoiding a. It must use only A,B. Alternating two
colors around five edges cannot close, a contradiction. If b or c rather
than a has label C, the corresponding cycles are a–c–x_c–z–x_a–a and
a–b–x_b–z–x_a–a. This covers all cases. Consequently the graph satisfies
all original assumptions and violates the conclusion.

The Lean proof quantifies the three cases using `Fin 3`. Its finite
kernel checks establish real adjacency, degree bounds, short walks,
the three five-cycle edge lists, and the elementary odd-cycle obstruction.
It then derives nonexistence for an arbitrary coloring using actual
`G.edist`, defined from lengths of actual walks. No Boolean search result
is assumed to represent the original metric.

For scope comparison, a,b,c have local girth three. Any cycle through z
uses two length-two spokes and at least one triangle edge, so its shortest
length is five. The maximum local girth among degree-three vertices is
therefore five. The source's local-girth-three Theorem 3 is not contradicted.
Local girth, planarity and bridgelessness are not asserted as additional
Lean declarations in this packet; they are unnecessary for the original
counterexample.

The construction is a classical pyramid configuration; see, for example,
[Chudnovsky–Thomassé–Trotignon–Vušković (2019)](https://arxiv.org/abs/1912.11246)
for the graph shape. This reference does not certify the historical
non-(1,1,2) result. We make no firstness or minimality claim.
