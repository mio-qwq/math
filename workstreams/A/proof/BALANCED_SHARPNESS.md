# Sharp scope of simultaneous partition balancing

This is a scope/limitation note for the two-partition discrepancy-one theorem in workstreams/A/proof/BALANCED_TWO_PARTITIONS.md. It is not a new original open-problem solution.

## Three partitions can fail even with blocks of size two

Let X={0,1,2,3} and define three perfect-matching partitions

    P={{0,1},{2,3}}
    S={{0,2},{1,3}}
    T={{0,3},{1,2}}.

For a two-element block, discrepancy at most one means its two elements must receive different colours (otherwise the discrepancy would be two). The six blocks above are precisely the six edges of K4. A red/blue assignment splitting *all three* partitions would therefore be a proper two-vertex-colouring of K4, impossible because K4 contains a triangle.

Any pair of the partitions DOES admit a balanced 2-colouring by the Eulerian orientation theorem. Thus two partitions are not an arbitrary number of partitions. The script workstreams/A/code/verify_balanced_sharpness.py independently checks all 16 colour assignments and the existence of a solution for each pair.

## Optimality with singleton blocks

A singleton's red/blue count difference is necessarily one; hence the uniform discrepancy-one upper bound cannot be reduced to zero when singleton blocks are allowed.

For the original component-avoiding transversal application, both families have blocks of size at least two. The stronger balanced statement allows singleton blocks but then does NOT promise both colours appear in those singleton blocks.

The theorem is a standard Eulerian graph-balancing consequence, not a claim of historical novelty. This scope note does not replace the frozen original complete Conjecture 10 mathematical proof, nor constitute compiled Lean or independent ROOT acceptance.
