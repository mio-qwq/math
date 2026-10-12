# Structural classification for the five-color theorem

## Structural classification

A triangle contains at most two degree-three vertices, because otherwise
each would have two degree-three neighbors. Two intersecting triangles
cannot share just one vertex, since that vertex would have degree at least
four. If they share an edge uw with other vertices z,t, then u,w have degree
three. Since u,w are adjacent, z,t must have degree two; otherwise u would
have a second degree-three neighbor. The component is the diamond K4-e.
The edge zt is excluded by 1-saturation. Its square is K4, already four-colorable.

Excluding these isolated diamonds, all triangles involving degree-three
vertices are disjoint. Every other vertex has degree at most two. Each
triangle has at most two external edges; its external-edge endpoints are
its ports. Contract the triangles. The resulting connected multigraph
has maximum degree two, so each component has a path or cycle arrangement.
Thus the possibilities are a plain path/cycle, a triangle, a chain of
triangles with leaf or triangle ends, or a necklace of triangles. In a
two-port triangle its ports are adjacent degree-three vertices, so each
external neighbor has degree at most two. Every connector incident to
such a triangle therefore has at least two edges before another triangle.
A direct edge between two one-port triangles and direct leaf tails are
allowed and will be handled below. No minimum-degree assumption is added.
