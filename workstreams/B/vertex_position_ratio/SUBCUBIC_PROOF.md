# Unbounded vertex-position ratio even in bipartite subcubic graphs

B,2026-10-10 12:31UTC. Extension AFTER freezing the general-family answerd1d82779f60c522dd2fa689d27c7c839d1115012. **Complete elementary restricted-family proof; independent review pending.** The original Problem4/preprint2.4, authors, definitions and source gates are in PROOF.md and SOURCE_GATE.md. Subcubic means maximum degree at most3, not exactly3regular.

## Theorem

There are connected finite simple BIPARTITE graphs of maximum degree3for which vp(G)/vp^-(G) tends to infinity. Specifically, for each k=2^h with h>=2, the graph below has roots v,u satisfying

    p_v=2k,        p_u >= (k-1)(k-2)/2+k.

Thus

    vp/vp^- >= (k^2-k+2)/(4k) = k/4-1/4+1/(2k) -> infinity.

This strengthens the negative answer to the SAME original question; it is not an additional conjecture count. No exact global root extrema are claimed.

## Construction

Take a complete rooted binary tree of depthh, rootv, with leaves l_0,...,l_(k-1). Put a=2k, N=(k-1)(k-2)/2 and L=a+3N+3. Attach to each leaf a track

    l_j=(j,0),(j,1),...,(j,L).

Add backbone vertices H_0,...,H_(k-1) and midpoint vertices M_0,...,M_(k-2). Add edges (j,a)–H_j, and replace each backbone link by the two-edge path H_j–M_j–H_(j+1). Set u=(0,a).

Finally process targets j=k-1,k-2,...,2 in descending order. For each target process sources i=j-1,j-2,...,1 in descending order. Number these pairs globally by s=0,...,N-1, set p=a+2+3s, and add the shortcut

    (i,p)–(j,p+1).                                      (E)

Equivalently the closed index is

    s=sum_{t=j+1}^{k-1}(t-1)+(j-1-i).

There are no other edges. In particular source0is NOT used. The graph order is kL+4k-2, and its size is kL+5k-4+N.

The graph is simple and connected. Internal tree vertices have degree3except the root of degree2; each tree leaf has degree2after track attachment. Track bases(j,a) have degree3; ordinary track vertices have degree2, shortcut endpoints degree3and terminal vertices degree1. Shortcut levels are3apart, so a track vertex cannot be endpoint of two shortcuts. Internal Hvertices have degree3and endpoint Hvertices degree2; Mvertices have degree2. Thus maximum degree is3.

For bipartiteness assign heights: tree depth to tree vertices; h+t to(j,t); h+a+1to H_j; h+a+2to M_j. EVERY edge joins heights differing by exactly1. Their parities give an explicit bipartition.

## The v-root position number

All assigned heights are actual distances from v: no edge increases height by more than1, and the tree/track paths reach every track vertex at its height. A shortest branch to H_j goes through(j,a), and one to M_j then goes through H_j. Therefore2krooted geodesics cover all vertices:

- kfull tree–track paths ending at(j,L);
- for j<k-1, the path ending at M_j through H_j, and the final path ending at H_(k-1).

Each v-position set meets each geodesic in at most one vertex, with the usual singleton-root exception harmless. Hence p_v<=2k.

Take all H_j and all track terminals(j,L), a set of size2k. The Hvertices share one height; the terminals share another. An ascending continuation from H_j can only go to an adjacent Mvertex, and that Mvertex has NO neighbor of larger height. Thus a v-geodesic passing through H_j cannot subsequently reach any selected terminal, whose height is larger. Terminals themselves have no farther neighbor. This proves the selected2kvertices form a v-position set. Hence p_v=2k.

## Distances from u and shortcut induction

Before adding shortcuts, a shortest u–(j,a) path for j>=1 follows the backbone and has length2j+2. A path using the binary tree must travel down at leastatrack edges before entering the tree and back up at leastatrack edges before reaching any base again, hence has length at least2a=4k>2j+2. A path avoiding the tree can change tracks only through their base attachments, so the backbone route is optimal. For j>=1and t>=a, therefore,

    d_initial(u,(j,t)) = t-a+2j+2,                       (I)

whereas d_initial(u,(0,t))=t-a for t>=a. The rest of the initial distance function may simply be the actual metric of the explicitly defined initial graph; no formula for its tree values is needed.

Add shortcuts in the listed order. When(E) is added, subtract2from the current distance potential on trackj at ALL levels>=p+1, changing no other vertices. Sourcei<j has never been a target. If there have already been q=j-1-i shortcuts intoj, equation(I) and prior updates give

    f(i,p)=p-a+2i+2,
    f(j,p)=p-a+2i+4,
    f(j,p+1)=p-a+2i+5.

After subtracting2on the target suffix, the new shortcut has potential difference1, and the vertical edge(j,p)–(j,p+1) has potential difference-1. All other vertical-edge differences are unchanged. Every earlier shortcut ends at a level<=p-2; tree and backbone edges are below the changed suffix. Thus the potential remains1-Lipschitz on ALL edges and0at u.

Affected vertices(j,t),t>=p+1, have paths of exactly their new potential: take an old shortest u–(i,p) path, use the new shortcut, and go upward on trackj. Its length is

    (p-a+2i+2)+1+(t-p-1)=t-a+2i+2.

Unaffected vertices retain old shortest paths of unchanged length. The1-Lipschitz lower bound and these attaining walks prove that the new potential is the exact distance function. Induction handles ALL shortcuts and ALL alternative undirected paths; no assumption about a shortest path's shape is omitted.

## Large u-position set

For each shortcut(E), select its preceding target vertex(j,p). It has only its two vertical neighbors; both are exactly one closer to u after the update. No later shortcut/update reaches these levels. Each terminal(j,L) also has only one neighbor, exactly one closer. Therefore the N+kselected vertices are all strict distance-boundary vertices of u.

The original paper's generic boundary lemma (finalProposition12) says such a set is an u-position set; directly, a u-geodesic cannot pass through one of these vertices internally because it has no possible next vertex farther from u. Hence p_u>=N+k. Together with p_v=2k this proves the theorem and unboundedness on the bipartite subcubic class. QED.

## Actual verification and limits

    python workstreams/B/vertex_position_ratio/verify_bipartite_subcubic.py

The standalone verifier reconstructs original edges via CLOSED shortcut indices, with no discovery imports. It checks degree<=3, parity bipartition, connected BFS, the actual root-distance levels, all2kgeodesic-cover paths, the2kposition witness, the N+kstrict-boundary witness, and a1-Lipschitz/descending-predecessor distance certificate. Small graphs additionally check all selected pairs against original BFS distances. Deliberately wrong ascending targets, a corrupted potential, a parity-violating extra backbone edge, and an impossible claimed root bound are rejected. Actual logs/hashes are in SUBCUBIC_REVIEW.md.

Only finite semantic regressions are computed; the infinite conclusion is established by the all-parameter proof above. The intermediate nonsubdivided-base degree3experiment is preserved as discovery history in probe_subcubic.py/log/json but is superseded by this bipartite family. Neither a cubic-regular, planar,2connected, minimal-order, exactglobalextrema, Lean, independently accepted nor historical-first result is claimed. The earlier simple family remains frozen and independently reviewable.
