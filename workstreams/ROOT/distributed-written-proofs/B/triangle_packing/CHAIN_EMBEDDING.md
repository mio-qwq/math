# Chain-to-necklace embedding

Any triangle chain other than the component consisting of two triangles
joined directly by one edge can be embedded as a subgraph in a necklace:
use an unused non-port vertex on a cap triangle as a second port; extend
leaf tails by new vertices and new triangles as necessary; then join the
two ends with a sufficiently long connector. Original connectors incident
to internal triangles already have length>=2. Leaf extensions make their
old last vertices degree two, and the added joining path can have length
at least two. This creates an admissible necklace. Restriction of a packing
coloring to the original subgraph is valid, since deleting vertices/edges
cannot shorten original-graph distances. An isolated triangle is immediate.
