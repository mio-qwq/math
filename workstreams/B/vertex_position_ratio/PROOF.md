# The vertex-position ratio is unbounded

B,2026-10-10. **Negative answer to the original open boundedness question; complete elementary family proof, pending independent review.**

## 1. Original question and definitions

Maya G.S. Thankachy, Ullas Chandran S.V., James Tuite, Elias John Thomas, Gabriele Di Stefano and Grahame Erskine, *On the vertex position number of graphs*, Discussiones Mathematicae Graph Theory44(2024),1169–1188, DOI10.7151/dmgt.2491, **Problem4**. Author-hosted early-access source https://oro.open.ac.uk/87516/8/87516_EA.pdf , printedearly-accessp6. The corresponding preprint is arXiv2209.00359v2, **Problem2.4**. The question asks whether vp(G)/vp^-(G) is bounded for connected graphs. The2026survey https://arxiv.org/html/2501.19385v5 Section3.3 and final open-problem list repeats it.

For a vertex x of a finite simple connected undirected graph, an x-position set S satisfies: for each y in S, NO other vertex of S lies on ANY shortest x–y path. Let p_x(G) be the maximum size of such a set. Then

    vp(G)=max_x p_x(G),       vp^-(G)=min_x p_x(G).

This vp^- is NOT the minimum size of a maximal general-position set. Also the observation root x cannot belong to an x-position set of size>=2.

**Theorem.** For every integer r>=2 there is a finite simple connected graph F_r with two vertices v,u such that

    p_v(F_r)=2r,          p_u(F_r)>=r(r+1).

Consequently

    vp(F_r)/vp^-(F_r) >= (r+1)/2 -> infinity.

This answers the ORIGINAL boundedness question negatively. A single finite ratio above6 would not suffice; the all-r construction and proof are essential. No exact global maximum or minimum of the root parameters is needed.

## 2. Explicit graph family

Put k=2r, a=k, N=r(r-1), and L=a+3N+2. The vertices are a common root v and

    (j,t),       0<=j<k, 1<=t<=L.

For notation only identify every(j,0) with v. Add the following undirected edges, and no others.

1. **Track edges:** (j,t)–(j,t+1), for0<=j<k and0<=t<L.
2. **Base crossedges:** (j,a)–(j+1,a), for0<=j<k-1.
3. **Descending-target shortcuts:** list pairs(j,q) in descending order j=k-1,k-2,...,2, and within each j in ascending order q=1,...,floor(j/2). Let s be the zero-based position of(j,q) in this list, so

       s = sum_{h=j+1}^{k-1} floor(h/2) + q-1.

   Put i=j-2q and p=a+2+3s, and add the edge

       (i,p)–(j,p+1).                                    (E)

There are N=sum_{j=0}^{k-1}floor(j/2)=r(r-1) shortcuts. Their level p increases by3each time. Set u=(0,a). The vertices(j,p) associated to the shortcuts will be called the selected peaks; a peak is NOT an endpoint of its own shortcut.

The largest shortcut level is a+3N-1=L-3, so every defined vertex and edge is within the tracks. This is a simple connected graph: tracks meet at v, and every added edge joins two distinct existing vertices. Track, base and shortcut edges are distinct. The exact counts are

    |V(F_r)| = 1+kL = 6r^3-2r^2+4r+1,
    |E(F_r)| = kL+(k-1)+N = |V(F_r)|+r^2+r-2.

No weighted edges or omitted subdivision vertices occur.

## 3. The first root has p_v=k exactly

Give vertex(j,t) level t and v level0. Every graph edge changes level by at most1. Hence every v–(j,t) path has length at least t, while the track path has length exactly t. Thus each full track is a v-geodesic.

The ktrack geodesics cover all vertices. An x-position set for x=v can meet a fixed track in at most one vertex: of two selected track vertices, the earlier lies on the track geodesic from v to the later. A set containing v can have only one vertex, which is also at most k. Therefore p_v<=k.

All kterminal vertices(j,L) have the same distance L from v. No one can occur on a shortest v-path to another, since a proper internal vertex of a shortest path has smaller distance from its initial root. They are a v-position set. Therefore p_v=k=2r.

## 4. Exact distances from u by a monotone potential induction

First omit all shortcuts but keep track and base edges. Its distance function from u is

    f(v)=a;
    f(j,t)=min(a+t,a-t+j),             1<=t<=a;
    f(j,t)=t-a+j,                      a<=t<=L.             (P0)

For t<=a, the two displayed candidates are attained via v or via the base crossedge path at levela and then downward on trackj. For t>=a, the base route has length t-a+j. These candidates are exact: the displayed function is0at u, is1-Lipschitz on every track/base edge, and is attained by the stated paths. The two definitions agree at t=a because0<=j<k=a. The 1-Lipschitz property gives a lower bound on every path length.

Now add shortcuts in the stated order. Maintain the following exact update rule:

    when (i,p)–(j,p+1) is added,
    subtract2from f(j,t) for ALL t>=p+1,
    and leave every other value unchanged.                (U)

We prove inductively that f remains the actual distance from u.

For the current shortcut let q be its index within targetj, so i=j-2q. All earlier targets are larger than j, and the q-1earlier shortcuts into trackj have already subtracted2(q-1)from its current high-level suffix. The source track i<j has not yet been a target. Therefore, just before the new edge,

    f(i,p)=p-a+i,
    f(j,p)=p-a+i+2,
    f(j,p+1)=p-a+i+3.                                  (D)

After(U), the new edge has endpoint values differing by1. The vertical edge(j,p)–(j,p+1) now has values p-a+i+2 and p-a+i+1, also differing by1. Every other track-edge difference is unchanged. All OLD crossedges have endpoints at levels at most p-2, because shortcut levels are3apart, and base edges are at levela. Their endpoint values are therefore unchanged by(U). The new function is still1-Lipschitz on EVERY edge and remains0at u.

Every affected vertex(j,t),t>=p+1, is reachable with exactly its new assigned value: take a previously shortest path to(i,p), use the new edge, then go upward on trackj. This walk has length

    (p-a+i)+1+(t-p-1)=t-a+i,

which is precisely the old value minus2. Every unaffected vertex retains an old shortest path of its unchanged assigned length. Because the 1-Lipschitz function bounds all u-path lengths below, these upper bounds establish exactness. This completes the induction.

In particular this proof accounts for ALL possible undirected routes through multiple shortcuts, including backward traversals; it does not assume shortest paths use only one shortcut. An arbitrary extra shortcut cannot defeat the lower bound provided by the globally1-Lipschitz potential.

For direct reproduction the final potential is

    f(j,t)=f_initial(j,t)-2 #{shortcuts with targetj and levelp<t},
    f(v)=a.                                             (PF)

## 5. Quadratically many vertices visible from u

For each shortcut(E), select the vertex z=(j,p) immediately BEFORE its target endpoint, and also select every terminal vertex(j,L). Let S be this set of N+kdistinct vertices.

At a selected peak(j,p), equation(D) and update(U) give

    f(j,p-1)=f(j,p)-1=f(j,p+1).

The peak has exactly its two vertical neighbors. It is above the base level; its own shortcut ends at(j,p+1), not at(j,p); earlier crossedges are below p-1and later ones above p+1. Future updates begin still farther up the tracks, so these values remain unchanged. Thus every neighbor of this peak is strictly closer to u.

A terminal vertex(j,L) has only its previous track vertex as neighbor. Every shortcut ends at level<=L-2, and the final potential increases by1along the last track edge. Hence every terminal vertex also has every neighbor strictly closer to u.

If a vertex z has no neighbor farther from u, it cannot be an INTERNAL vertex of a u-geodesic: distances from u strictly increase by1along such a path. Therefore any collection of such boundary vertices is an u-position set. This elementary boundary fact is already Proposition12of the original paper (preprintProposition2.12), not a new lemma claimed here; the argument above restates it for completeness.

All selected peaks and terminal vertices satisfy the stronger strict-boundary condition. Consequently

    p_u(F_r) >= |S| = N+k = r(r-1)+2r = r(r+1).

Combining with p_v=2r,

    vp(F_r)/vp^-(F_r) >= p_u(F_r)/p_v(F_r) >= (r+1)/2.

Here we use vp>=p_u and vp^-<=p_v; we do NOT assume either root is a global extremizer. Letting r increase proves the theorem and gives a negative answer to Problem4. QED.

## 6. Reproduction and evidence limits

    python workstreams/B/vertex_position_ratio/verify_unbounded_ratio.py

The standalone checker imports no discovery program, recorded distances or matching solver. It constructs shortcuts using the CLOSED index formula in Section2, then reconstructs original adjacency and BFS distances. It checks a distance certificate independently using1-Lipschitz edge inequalities and descending predecessors, verifies the kroot-geodesic covers/equal-level witness, and verifies every selected peak/terminal vertex is strictly boundary. For the smaller tested graphs it also computes original BFS from EVERY selected witness vertex and checks all selected pairs directly against the x-position definition.

Actual tested r=2,3,5,12,20; orders49,157,721,10129,47281. The r=12example certifies a ratio at least13/2, and r=20at least21/2. These finite facts alone would not settle boundedness; the exact all-parameter potential induction does. Four negative controls reject a corrupted potential, a false rootwise upper bound, adding the observation root to a nontrivial position set, and the deliberately wrong ascending-target order.

Source gate and actual hashes/run counts are in SOURCE_GATE.md and REVIEW.md. The generic boundary/poset/shortest-path facts are prior theory. The descending-target construction and its distance induction were derived independently; the earlier paper's specific6-limit construction was not adopted. A post-candidate query later displayed its formula, after this family had already been constructed and checked. No Lean, full global parameter classification, order-minimality, independent acceptance or historical-firstness claim. Bounded later-result searches found no same-scope resolution but cannot rule out a missed publication.
