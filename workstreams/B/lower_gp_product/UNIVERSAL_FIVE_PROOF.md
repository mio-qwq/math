# Universal lower general-position product bound through five

B, 2026-10-10. **Complete computer-assisted all-orders partial theorem, pending independent review.**

## Statement, original source, and scope

For every two nonempty finite simple undirected graphs G,H,

    gp^-(G square H) >= min{5,gp^-(G),gp^-(H)}.             (T)

Here a general-position (GP) set contains no three distinct vertices on any shortest path. A maximal GP set is inclusion-maximal, not necessarily maximum. Its smallest possible size is gp^-.

Original question: Eartha Kruft Welton, Sharif Khudairi and James Tuite, *Lower General Position in Cartesian Products*, arXiv2404.19451v1 Conjecture2.10; final Communications in Combinatorics and Optimization10(1)(2025),110–125, Conjecture3, printedp117, DOI10.22049/cco.2024.29171.1879. Primary final https://oro.open.ac.uk/98050/9/98050final.pdf . The original bound omits5 from the minimum. Thus(T) proves the ORIGINAL conjecture whenever at least one factor has lowerGP at most5. Both orders AND diameters are arbitrary. The case with both factor parameters>=6 remains unresolved here.

This supersedes B's truncation-at4 and its diameter-two truncation-at5 as a bound, preserving those frozen proofs. It is not a full conjecture resolution, an original counterexample, or an exact formula for every product. The certificate below checks sizes1,2,3,4 directly; it does not depend on either earlier partial theorem.

## 1. Metric reduction

First suppose G,H connected. If(T) fails, choose a maximal product GP set S of size k<min{5,gp^-G,gp^-H}. Since the product is nonempty,1<=k<=4. Write its distinct vertices as (a_i,b_i),0<=i<k. Coordinate repetitions are allowed.

Let A_ij=d_G(a_i,a_j),B_ij=d_H(b_i,b_j). These are pseudometrics on k labels: symmetry, nonnegativity, zero diagonal, triangle inequalities; zero distance identifies the same actual vertex. Every product distance is A_ij+B_ij. Indeed every product path makes at least the shortest required number of steps in each coordinate, and concatenating factor geodesics attains that sum.

For any three labels, each triangle slack d(i,j)+d(j,l)-d(i,l) is nonnegative. It vanishes in the product exactly when it vanishes in BOTH coordinates, with the SAME middle label. Likewise two product labels coincide exactly when their coordinate distances both vanish. These tests depend only on zeros of distances and triangle slacks, not on the sizes of nonzero distances.

For an outside factor vertex x, its distances to the k landmarks together with A form a pseudometric on k+1labels. An outside profile records, for each unordered pair of landmark labels i,j, the three truth values

    d(i,x)+d(x,j)=d(i,j);          x is the middle
    d(x,i)+d(i,j)=d(x,j);          i is the middle
    d(x,j)+d(j,i)=d(x,i).          j is the middle          (1)

It also records which landmark distances are zero. For a vertex outside all landmarks this last mask is empty. Known landmark vertices have their exact profile and zero mask. Repeated landmark labels can make more than one equality in(1) hold, so profiles use separate bits, not one exclusive case label.

Two factor profiles describe a new GP product extension of S if and only if:
- their zero masks are disjoint, so the new point is not in S;
- their equality bits(1) are disjoint, so no pair of S and the new point has a common middle in both coordinates.

We call this pair compatible. Maximality of S forbids every compatible pair of ACTUAL profiles.

## 2. Complete finite cover of unbounded metric data

Let C be the cone in R^10 whose coordinates d_ij,0<=i<j<5, are nonnegative and satisfy all30triangle inequalities on five labels. These are precisely all five-label pseudometrics. No distance bound, graph order bound, or integer coordinate bound is imposed.

Any pseudometric on k+1<=5labels extends to one in C by duplicating an existing landmark to fill unused labels. We always use label4 for the new point and labels0,...,k-1 for the selected landmarks. Thus C covers every factor projection and every possible outside profile needed above.

The exact program `verify_metric_rays.py` derives the extreme rays of C from its DEFINING INEQUALITIES, with integer arithmetic only. It does not read a supplied ray list. Start with the nonnegative orthant's10unit rays. Add each triangle inequality h>=0 in turn. Retain rays with h>=0. For each positive/negative adjacent ray pair r,s add the primitive integer ray

    h(r)s - h(s)r

on h=0. Divide coordinates by their positive gcd. Old active-inequality masks identify adjacency exactly: r,s are adjacent if their common zero constraints contain no third old extreme ray.

Why this algorithm is complete: all intermediate cones are pointed, full-dimensional and inside the nonnegative orthant; the all-one vector satisfies every added triangle inequality strictly. Normalize by sum(d_ij)=1 to get a compact polytope. Clipping this polytope by one halfspace retains old feasible vertices and creates new vertices only at crossings of old edges. Two vertices span an edge exactly when their minimal common face has no other vertex. That face is the intersection of their common active inequalities, including any redundant inequalities. Hence the update lists every new ray and no missing ones. This establishes completeness inductively from the orthant.

The actual computation ends with25rays. This matches the classical MET5 description (15cuts and10K2,3graph metrics), which motivated discovery, but the proof's checker derives them independently. The generic polyhedral theory is prior, not B's invention; see David Avis's primary exposition https://cgm.cs.mcgill.ca/~avis/epc/epc.html , section3. No correctness claim rests on a floating-point LP or an unchecked ray count.

For each ray record zeros of all10coordinate forms and30triangle-slack forms. All40forms are nonnegative on C. Every cone point is a nonnegative combination of its extreme rays; a form vanishes on that point exactly when it vanishes on each ray used with positive coefficient. Consequently all possible zero patterns are precisely the intersections of subsets of the25ray zero masks, including the empty intersection for the cone origin.

The verifier computes the full intersection closure by a queue, beginning with the all-zero point, and repeatedly intersecting with EVERY ray mask. For each newly reached pattern it stores an integer metric representative obtained by adding the corresponding ray to the previous representative, and checks all40zero tests exactly. There are9484patterns. Queue exhaustion is a closure certificate; it is not a sample of bounded distances. Any real metric has one of these patterns.

## 3. Necessary factor-extension demands

Group these patterns by the k-landmark zero distances and triangle equalities. Within each group retain all possible outside profiles, using only patterns with positive distances from the new point to every landmark. For k=1,2,3,4 the numbers of landmark groups are respectively1,2,8,106, and the total outside-profile counts are1,5,87,9101.

This grouping may allow outside profiles that individually arise with different numeric landmark distances inside the same equality group. Allowing them all is a RELAXATION. Every actual graph profile is included, which is the only direction required for nonexistence. We do not assume that an arbitrary collection of profiles has a simultaneous graph realization.

Take any inclusion-maximal GP subset T of the DISTINCT landmark vertices in a factor. Its size is at most k<gp^- of that factor. It is therefore not maximal in the whole factor graph. A vertex extending T cannot be another landmark, by landmark maximality. At least one outside profile has NONE of the equality bits(1) belonging to pairs of T. This gives the demand

    actual outside-profile set intersects E_T,

where E_T is the explicitly computed set of profiles extending T. These demands are necessary even if T uses fewer than klandmarks. Existence suffices; multiplicity of vertices with the same outside profile is irrelevant. Known landmark vertices remain separately mandatory.

If S were maximal, actual outside-profile sets X,Y would simultaneously hit every respective demand and avoid ALL compatible pairs, including pairs involving mandatory known profiles.

## 4. Exhaustive nonexistence certificate

`verify_arbitrary_four.py k` implements the following finite exact check, for EACH k=1,2,3,4. It imports only the new inequality-to-ray verifier; it reads no discovery script, discovery JSON or supplied ray table.

- Iterate every unordered pair of landmark groups; factor exchange is harmless because both factors use the identical complete list. Exclude pairs with a coinciding product label or a common tight triangle. Respectively1,2,14,2381GP product groups remain.
- A compatible known-known profile pair would itself refute maximality. Otherwise discard every outside profile compatible with an unavoidable known profile in the other factor.
- Search exhaustively for a set Y of remaining second-factor profiles hitting its demands while leaving first-factor profiles able to hit ALL first-factor demands. A state consists of unmet second-factor demands and still-allowed first-factor profiles. If any first demand has become empty, reject the state. Otherwise choose an unmet second demand and branch over EVERY profile in it. Choosing a profile satisfies every demand containing it and deletes from the first side all profiles compatible with it. Identical states may be merged.
- If all second demands were met while all first demands remained nonempty, taking all remaining first profiles would exhibit a feasible relaxed local system. No such state is reached, in any of the four set sizes.

This search is complete: any hypothetical actual Y must contain a profile from the selected unmet demand and so follows at least one branch; every deletion is forced by product maximality. Each branch meets a new demand, so it terminates. Exhaustion proves there are no possible actual X,Y.

Discovery independently used the classical25ray description, positive-support unions and first-factor recursive branching. Verification uses inequality-derived rays, zero-mask intersection closure, numeric representatives, and second-factor iterative branching. They agree on the four-point obstruction. The smaller sizes are additionally checked directly. This is algorithmic cross-checking by B, NOT an independent person's acceptance.

Thus no maximal GP set of size k<min{5,gp^-G,gp^-H} exists for connected factors, proving(T) there.

## 5. Disconnected graphs

For a disjoint union of nonempty components G_i, maximality is componentwise and gp^-(G)=sum_i gp^-(G_i): paths never connect different components, so a union of componentwise GP sets is GP and is maximal exactly when every component restriction is maximal. Components of G square H are G_i square H_j. Applying the connected result and putting x_i=gp^-(G_i),y_j=gp^-(H_j),

    gp^-(G square H) >= sum_ij min(5,x_i,y_j)
                       >= min(5,sum_i x_i,sum_j y_j).

For the last inequality use sum_j min(t,y_j)>=min(t,sum_j y_j), first with t=min(5,x_i), then sum over i and apply the same elementary inequality again with t=min(5,sum_j y_j). This proves(T) for all stated graphs. QED.

## Verification, sources and limits

One-command replay:

    python workstreams/B/lower_gp_product/verify_universal_five.py

Environment: Python3.12.14, standard library only. The harness checks all four values of k, not just k=4. Detailed actual counts/digests and source hashes appear in UNIVERSAL_FIVE_REVIEW.md and verify_universal_five.log. All33semantic fixtures (25rays and8face representatives) are realized as original unweighted graphs by identifying zero-distance labels and subdividing weighted complete-graph edges;6022BFS entries check the intended original distances. These fixture graphs are not asserted to have any particular lowerGP number.

Negative controls remove the crucial factor-extension demands and confirm that the finite system becomes feasible, reject a corrupted triangle metric, and reject a collinear claimed GP triple. An additional ray-module control also rejects a triangle-violating vector. No floating-point search, added axiom, solver timeout, Lean claim, global firstness claim or independent-review claim appears in this proof.

The primary original statement and later-result/author searches were refreshed on2026-10-10. No matching universal bound through5 was found; absence from bounded searches does not establish priority. Original conjecture cases with both factor lowerGP>=6 remain outside this theorem. A hypothetical original counterexample must now have product lowerGP>=5. Extending this computation to larger sets is not automatic: it needs a complete larger metric cone and a new nonexistence calculation, not just more random graph checks.
