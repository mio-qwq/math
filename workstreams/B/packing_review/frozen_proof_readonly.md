# Candidate all-length packing 4-coloring proof

This proof addresses exactly the hypotheses supplied in the task: a finite simple graph of maximum degree at most 3, whose degree-3 vertices form an independent set, and every degree-3 vertex lies on a cycle of length at most 4. The independent source gate confirmed these are the hypotheses of Conjecture 1 in arXiv:2603.25113v1. This is a candidate proof awaiting independent mathematical review. No frozen SAT instances were rerun or enlarged.

## 1. Structural classification

Work in a connected component. Any triangle contains at most one degree-3 vertex, and any square at most two; in the latter case they are opposite. A square cannot have a chord, because its endpoints would be adjacent degree-3 vertices.

Suppose two distinct cycles of length at most 4 intersect. At any common vertex their two pairs of incident cycle edges overlap, since the vertex has degree at most 3. Thus they have a common edge. Take a maximal common-edge path P. Its distinct endpoints have degree 3: the two cycles diverge there. (The intersection cannot contain an entire cycle unless the cycles are identical.) Since these endpoints cannot be adjacent, P has at least two edges, and each complementary path in either cycle has at least two edges. Hence both cycles are squares and all three paths have length exactly two. Their two complementary middle vertices are distinct, or the cycles would be identical. Their union is K2,3. The two degree-3 vertices are saturated, and each of their three common neighbors has degree exactly 2: it cannot have degree 3 adjacent to them. Therefore this is the whole component.

Outside this exception, all short cycles are vertex-disjoint. Every vertex outside them has degree at most 2. Contract each short cycle. Its degree is the number of exits, at most 2; two exits require an opposite-terminal square. The connected quotient multigraph has maximum degree 2, so is a path, cycle, or isolated vertex (loops and parallel edges allowed). Consequently components with degree-3 vertices are square necklaces, or chains of opposite-terminal squares whose ends are a one-terminal triangle, a one-terminal square, or a leaf. Joining paths between cycle terminals have length at least 2 by independence. Leaf-end paths have length at least 1. Components with no degree-3 vertices are paths or cycles.

## 2. Universal tiles

A word assigns colors to consecutive vertices of a path. The following four tiles start and end in color 1; their lengths refer to edges:

| Edge length | Word | Positions of color 2 | Positions of color 3 | Positions of color 4 |
|---|---|---|---|---|
| 4 | 1 3 1 2 1 | 3 | 1 | none |
| 5 | 1 3 1 4 2 1 | 4 | 1 | 3 |
| 6 | 1 3 1 4 1 2 1 | 5 | 1 | 3 |
| 7 | 1 3 1 2 1 4 2 1 | 3, 6 | 1 | 5 |

Positions start at 0. Concatenate tiles by identifying their endpoint 1s, not by retaining two consecutive 1s.

Any linear or circular concatenation is a packing coloring. There are no adjacent 1s. Within one tile, repeated 2s occur only at positions 3 and 6 in the length-7 tile, distance 3. Across a join, the last 2 is at position -1 and the next 2 at position at least 3, distance at least 4. Consecutive 3s are separated by a whole tile, hence at least 4. A tile containing 4 has its 4 at least two edges before its final endpoint (two for lengths 5 and 7, three for length 6); the next tile containing 4 places it at least three edges after its initial endpoint. Thus distinct consecutive 4s have separation at least 5; intervening length-4 tiles only increase this. The cyclic version has exactly the same consecutive-occurrence checks. A color that occurs only once has no self-conflict.

Every integer d >= 4 is a sum of numbers from {4,5,6,7}: use one tile 4+r, where r is the residue modulo 4, and otherwise length-4 tiles. Therefore arbitrary prescribed color-1 marks whose successive backbone gaps are at least 4 can be accommodated.

## 3. Square necklaces and square-ended chains

Replace each opposite-terminal square by the two-edge path through one of its degree-2 vertices, retaining that middle vertex as a marked vertex. A connector of length L between degree-3 terminals now gives a gap d=L+2 >= 4 between marks. Color each gap by the tiles above. At every marked vertex, its preceding terminal has color 2 and its succeeding terminal color 3.

Restore each square by adding the second middle vertex, also colored 1. This vertex is a false twin of the retained middle vertex: both have exactly the same two neighbors. They are distance 2, so their equal color 1 is permitted; adding the twin never shortens distances among old vertices. Its distances to every other color-1 vertex equal those from the retained middle vertex. Hence restoration preserves the packing coloring.

For a square-ended chain, use the same construction, retaining the terminal color 2 before the first marked vertex and terminal color 3 after the last marked vertex. These additional end vertices do not cause conflicts: the first later 2 is at least four edges from the initial 2, and the final 3 is at least four edges from the previous 3. Restore the square twins as above.

## 4. Triangle caps

The direction of the chain is fixed throughout.

Left cap: replace an endpoint square by a triangle whose exit terminal is color 3, and whose other vertices are colors 1 and 2. Retain the color-1 vertex as the initial marked vertex. Compared to the square-ended construction, only distances from the left cap's color-2 vertex to the rest may decrease, by one. The first subsequent 2 is at position at least 3 relative to the initial mark, while the exit terminal is at position 1. Its distance from the cap's 2 is therefore at least 1+(3-1)=3, as required. The left cap has no 4. All other relevant distances are unchanged.

Right cap: its exit terminal has color 2, and its other vertices receive 1 and h. Retain the 1 as the final marked vertex. Let d in {4,5,6,7} be the length of the final elementary tile (not necessarily the entire final connector gap).

- If d=4, set h=4. The final tile has no 4. Any preceding 4 is at least two edges before this tile's initial mark. Since the cap's h vertex is reached through the final terminal at position 3 plus one edge, its distance from that preceding 4 is at least 2+3+1=6.
- If d>=5, set h=3. The nearest earlier 3 is at position 1 in this tile; the final exit terminal is at position d-1. Their distance to the cap's h vertex is (d-1-1)+1=d-1>=4.

The cap's 1 causes no adjacency conflict. Its terminal 2 retains all previously checked distances. The cap may be used with either a left triangle or a left square: the left cap introduces no 4, and its terminal 3 fits the same position-1 calculation. Thus all triangle/square endpoint combinations are covered, including chains with no interior square and only one connector.

## 5. Leaf caps and elementary components

If a chain ends in a leaf, attach a fresh one-terminal square by one edge from that leaf to the square's terminal. A leaf-to-first-cycle path of length L>=1 becomes a square-to-first-cycle connector of length L+1>=2. The enlarged chain is covered above; restricting its coloring to the original graph preserves every packing condition. Apply at both ends when necessary.

Paths use the repeating word 1,2,1,3 and its restrictions. A cycle of length 3 uses distinct colors 1,2,3. Every cycle of length n>=4 is a circular concatenation of the tiles. K2,3 has its degree-3 vertices colored 2 and 3 and its three other vertices colored 1. Isolated vertices are immediate.

Consequently every graph satisfying the stated hypotheses has a packing coloring with colors 1,2,3,4. This conclusion is a candidate theorem pending independent mathematical review, not a claim of publication or priority.

## 6. Source gate and overlap with existing results

Target: El Zein–Mortada, arXiv:2603.25113v1, Section 5 Conjecture 1, https://arxiv.org/html/2603.25113v1 . The separate read-only source gate is `../packing_gate/literature_gate_2026-10-10.md`. It found no primary resolution in its scoped pass; this is not an exhaustive novelty certificate.

Credit for the already known all-even connector subclass: Lemdani, Abbas, Ferme, *Packing Chromatic Numbers of Finite Super Subdivisions of Graphs*, Filomat 34(10) (2020), 3275–3286, Proposition 2.8 and subgraph monotonicity (Proposition 2.1), DOI 10.2298/FIL2010275L, publisher PDF https://web1.pmf.ni.ac.rs/filomat-content/2020/34-10/34-10-9-12153.pdf . An all-even square necklace embeds in a super subdivision of a cycle. The present candidate mechanism additionally covers odd and mixed connector lengths, all endpoint types, and the complete structural reduction. No novelty claim should precede further literature and independent proof review.
