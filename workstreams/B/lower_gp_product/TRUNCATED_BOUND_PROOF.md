# A universal truncation at four for the lower general-position product bound

Agent B,2026-10-10. **Partial affirmative result for the original conjecture; pending independent review.** No full resolution, Lean compilation, or historical-firstness claim.

## Statement and source

The conjecture of Eartha Kruft Welton, Sharif Khudairi and James Tuite asserts

    gp^-(G □ H) >= min{gp^-(G), gp^-(H)}.

Here gp^- is the smallest size of an inclusion-maximal general-position set. The original is arXiv:2404.19451v1, Conjecture2.10; final Communications in Combinatorics and Optimization10(1)(2025),110–125, Conjecture3, printedpage117, DOI10.22049/cco.2024.29171.1879. [Original preprint](https://arxiv.org/html/2404.19451v1); [final primary PDF](https://oro.open.ac.uk/98050/9/98050final.pdf). Definitions and status gate appear in SOURCE_GATE.md.

**Theorem. For all finite nonempty simple undirected graphs G,H,**

    gp^-(G □ H) >= min{4, gp^-(G), gp^-(H)}.

**In particular the original conjecture holds whenever at least one factor has lower general-position number at most four. Any counterexample to the original conjecture must have both factor parameters at least five and product parameter at least four.**

This is an all-orders statement, not an inference from the finite searches. The cases involving maximal sets of size at most two also follow from known universal-line results; the substantive step here is the general three-point extension argument.

## 1. Metric facts and extension convention

In a connected graph, three distinct vertices x,y,z fail general position exactly when one triangle inequality is an equality. Write [x,z] for the metric interval {y:d(x,y)+d(y,z)=d(x,z)}. A set is in general position if every triple of its distinct vertices has all three triangle inequalities strict.

If |A|<gp^-(G) and A is a general-position set, then A is not maximal, so there is a vertex u outside A for which A union {u} remains in general position. Call u an extension of A. In particular an extension of a two-point set lies on none of the three possible lines determined by that pair: all three inequalities are strict.

Distances in a Cartesian product add:

    d((a,b),(a',b')) = d_G(a,a') + d_H(b,b').

Therefore an equality expressing that one of three product vertices is between the other two holds if and only if the corresponding equality holds in BOTH coordinates with the SAME designated middle vertex. This follows because both coordinate triangle deficits are nonnegative and their sum vanishes exactly when each vanishes. The statement remains valid with coincident coordinate values, even though the product vertices must be distinct.

We first prove the theorem for connected factors. Factors with one vertex give an isomorphic copy of the other factor and cause no difficulty.

## 2. One- and two-point product sets

A singleton in a graph with at least two vertices is extendable. Suppose both factors have gp^->2, and let S consist of two distinct product vertices. At least one coordinate projection consists of two distinct points. Extend that pair in its factor and choose any value in the other coordinate. Since all three triangle inequalities in the first coordinate are strict, the resulting new product point extends S. Thus there is no maximal product GP-set of size two when both factor parameters exceed two.

## 3. Three-point extension: projections that are already GP or repeat

Assume gp^-(G)>=4 and gp^-(H)>=4. Let

    S={(a_i,b_i):i=0,1,2}

be a general-position set of three distinct product vertices. We show that S is extendable.

If a coordinate projection contains three distinct points in general position, extend that triple in its factor. Pair the extension with any value in the other factor. Each potential new product triple has three distinct first-coordinate points in general position, so cannot be collinear. This extends S.

If one projection has exactly two distinct values, interchange factors if necessary and suppose a_i=a_j=a, while a_k=c differs from a. Distinctness of product vertices implies b_i!=b_j. Choose u extending {a,c} in G, and v extending {b_i,b_j} in H. The point (u,v) extends S: the pair of old vertices indexed i,j is protected by strict triangle inequalities in H; each other pair is protected by strict inequalities for {u,a,c} in G.

If one projection is a singleton, the other consists of three distinct points in general position (because S is GP), so the first case applies. Hence only the case of two three-element collinear projections remains.

## 4. The two collinear projections must bend in opposite orders

Three distinct collinear points in a metric have a unique middle. The middles in the two projections must have different indices, or else the product triple S would itself be collinear. Relabel the common endpoint index as0, the middle in G as1, and the middle in H as2. Thus

    d_G(a0,a2)=x+y,  x=d_G(a0,a1)>0, y=d_G(a1,a2)>0;
    d_H(b0,b1)=p+q,  p=d_H(b0,b2)>0, q=d_H(b2,b1)>0.

Choose u extending {a0,a2} in G, and v extending {b0,b1} in H. These extensions exist because each two-point set has size less than the corresponding lower GP-number. All coordinate values u,a0,a1,a2 are distinct, since a1 is already between a0,a2; likewise v differs from b0,b1,b2.

We claim that at least one of the following three new product vertices extends S:

    z1=(u,b0), z2=(a0,v), z3=(u,v).

If z1 or z2 works we are done, so suppose neither works. Put alpha_i=d_G(u,a_i).

Consider the failure at z1. The old pair indexed0,2 cannot cause it, since {u,a0,a2} is GP. For the pair0,1, the second-coordinate values are b0,b0,b1. Their possible equalities allow only u or a0 to be the middle in G. But u cannot lie between a0,a1: since a1 lies between a0,a2, this would put u between a0,a2, contrary to its choice. Therefore this pair can obstruct only if

    alpha_1 = alpha_0 + x.                                      (A)

For the old pair1,2, the second-coordinate triple b0,b1,b2 has b2 as its unique middle. Hence this pair can obstruct only if

    alpha_1 = alpha_2 + y.                                      (B)

Thus failure of z1 implies (A) or (B). Either possibility excludes a1 from being between u and a2: that equality would be alpha_2=alpha_1+y. Under(B) it contradicts y>0; under(A) it would give alpha_2=alpha_0+x+y and make a0 a middle vertex of {u,a0,a2}, again a contradiction. Also u cannot be between a1,a2, since that would place u between a0,a2. Consequently, if {u,a1,a2} is collinear at all, its middle MUST be a2.

Apply the same argument to failure of z2 with G,H interchanged and indices1,2 interchanged. It shows that if {v,b1,b2} is collinear, its middle MUST be b1.

Now consider z3. The old pair0,2 is protected by {u,a0,a2} being GP; the old pair0,1 is protected by {v,b0,b1} being GP. For the remaining old pair1,2, any equality in G requires index2 as middle, whereas any equality in H requires index1 as middle. These cannot be the same product vertex. The metric fact in Section1 therefore excludes every equality. Hence S union {z3} is GP. This proves the three-point extension claim in all cases.

Sections2–4 imply the stated truncated bound for connected graphs: if the desired minimum is3 no maximal pair is possible, and if it is4 no maximal triple is possible. Smaller desired minima are immediate.

## 5. Disconnected and boundary cases

A GP-set in a disjoint union is maximal exactly when its intersection with EACH component is maximal there; shortest paths stay inside one component. Thus lower GP-numbers add over components. Write G_i,H_j for the components and a_i=gp^-(G_i),b_j=gp^-(H_j), all positive integers. Product components are G_i □ H_j, and the connected result gives

    gp^-(G □ H) >= sum_{i,j} min{4,a_i,b_j}.

This sum is at least min{4,sum_i a_i,sum_j b_j}. Indeed, with at least four component pairs there are at least four positive summands. With at most three pairs, at least one factor is connected, and the assertion follows from sum_j min{c,b_j} >= min{c,sum_j b_j}, with c=min{4,a_1} (or its symmetric version). This proves the theorem for all nonempty finite graphs. If empty graphs are allowed and gp^-(empty)=0, their case is immediate as well. QED.

## Verification and scope

`extend_triple.py` implements the proof's extension map, using only factor distance tables. `verify_extension.py` reconstructs factor and Cartesian-product adjacency and computes BFS distances independently, checks the extension hypotheses in the factors, and tests the constructed new point directly in the actual product graph. It also exercises the opposite-middle metric argument on exact integer distance tables, includes deliberate negative controls, and verifies disconnected boundary fixtures. Actual counts/environment/hashes are recorded in the adjacent logs and SELF_REVIEW.md.

The earlier dense-factor and true-twin-blow-up experiments found no counterexample and are retained as discovery history; they are NOT the justification for the universal theorem. Once the three-point extension proof is available, further searches for product triples are mathematically superseded. The case when both factors have lower GP-number at least five and a putative product witness has size at least four remains open here. Independent review, historical novelty and any formalization are pending.
