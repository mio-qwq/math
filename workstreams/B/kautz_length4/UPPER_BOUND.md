# An arbitrary-set upper bound for length-four Kautz digraphs

Agent B, 2026-10-10. A partial affirmative bound toward Chandran et al., arXiv:2604.15909v1, Problem5.2; not an exact formula or conjecture counterexample. Pending independent review and source/novelty gate. This uses cross-support constraints and applies to **every** general-position set, not a fixed lower-bound template.

For m>=6, put t=floor(m/2) and (m)_4=m(m-1)(m-2)(m-3). Then

    gp(Ka(m,4)) <= m(m-1)(3m-5)
                  + floor((m)_4 floor(t²/3) / (t(t-1))).

In particular, limsup as m tends to infinity of gp(Ka(m,4))/m^4 <=1/3.

## Definitions and block embedding

A vertex of Ka(m,4) is a word abcd with unequal consecutive symbols; shifting left and appending any symbol unequal to d gives an arc. A GP set contains no three distinct vertices x,y,z with d(x,y)+d(y,z)=d(x,z).

For distinct length-four words, distance is four minus the length of their longest proper suffix/prefix overlap. A zero overlap permits appending all four target symbols: failure of length-one overlap ensures the first append is legal. This proves the formula directly from the original arcs.

Choose t pairwise symbol-disjoint ordered pairs P_1,...,P_t from the alphabet. Associate each two-letter word ij, i!=j, with the length-four word P_i P_j. For any two distinct such words, the original distance is 2 if the second block of the first equals the first block of the second, and is 4 otherwise.

Indeed, overlaps of length one or three would identify an even-position symbol of one ordered pair with an odd-position symbol of another. All 2t symbols are distinct, so this is impossible. A length-two overlap occurs precisely on equal whole blocks. Consequently this map multiplies all distances of Ka(t,2) by two. Restricting any GP set to these block words therefore gives a GP set of Ka(t,2).

## Elementary two-letter bound, including digons

The source paper's Theorem3.4 gives gp(Ka(t,2))=floor(t²/3) for t>=3. Here is a self-contained upper-bound argument, so no computational base case from that theorem is needed.

For a GP collection of words ij, create a loopless auxiliary digraph H with arc i->j for each selected word. A directed three-edge walk gives three selected words. Unless its first and last arcs coincide, these are distinct and form a forbidden two-step geodesic in Ka(t,2): the middle arc is j->k with j!=k, so the first word's last symbol differs from the third word's first symbol.

Every digon in H is therefore an isolated component. For if a<->b has any extra incident arc, traverse the digon and that arc in the appropriate order to obtain a three-edge walk whose first and last arcs differ. After removing q isolated digons, H has no directed cycle and no directed path of length three. Assign each remaining vertex its longest incoming-path length, in {0,1,2}. Arcs go strictly from a lower to a higher level. If level sizes are a,b,c, the arc count is at most ab+ac+bc <=floor((a+b+c)²/3).

For r=t-2q remaining vertices, the total is at most 2q+floor(r²/3). If q=0 this is the claimed bound. If q>=1 and t>=3, then r+q=t-q>=2 (the sole exception r=0,q=1 has t=2). Hence t²-r²=4q(r+q)>=8q>=6q. Thus 2q+floor(r²/3)<=floor(t²/3). This establishes the needed upper bound for all t>=3. The alternating digon exception at t=2 explains the parameter restriction m>=6.

## Double counting over symbol-disjoint block systems

Let S_4 be the selected words having four distinct symbols. Sample a uniformly random permutation of all m alphabet symbols and use its first 2t positions as consecutive ordered pairs. For a fixed word abcd in S_4, the event that (a,b) and (c,d) both occur as ordered pairs has probability

    t(t-1)/(m)_4.

There are t(t-1) choices of their distinct pair slots; each placement fixes four permutation positions and has probability 1/(m)_4. These events are disjoint. Every sampled block system contains at most floor(t²/3) selected block words by the previous sections. Taking expectations gives

    |S_4| <= floor((m)_4 floor(t²/3)/(t(t-1))).

There are exactly m(m-1)^3 proper length-four words, of which (m)_4 have four distinct symbols. Bounding all other selected words by their total number adds m(m-1)(3m-5), proving the displayed upper bound. The added term is O(m³), and floor(t²/3)/(t(t-1)) tends to1/3. Thus the asymptotic assertion follows.

## Limits and next step

This does not match B's frozen lower coefficient26/125, so the exact original problem remains open. The finite bound is deliberately coarse on words with repeated symbols and may be inferior to other elementary bounds at small m. No optimized template, numerical MILP bound or exhaustive graph count is used in the proof. Check the scaled-distance bridge and inclusion probability independently before acceptance. Historical novelty has not been established.

## Relation to the frozen lower bound and actual checks

The frozen0202144 lower packet gives gp(Ka(5q,4))>=130q^4-74q^3+8q^2. For general m take q=floor(m/5); the subalphabet embedding is isometric by the same overlap-distance formula, so this lower bound also applies in Ka(m,4). Therefore the two packets together imply

    26/125 <= liminf gp(Ka(m,4))/m^4
           <= limsup gp(Ka(m,4))/m^4 <= 1/3.

Existence of a limiting density is not asserted.

Actual Python3.12.14 stdlib run of verify_upper_bound.py: PASS. It builds the full original digraphs for m=6,7,8,9, runs BFS from every encoded block word (101796 distance entries total), checks360 scaled-distance identities, exhausts64+4096 two-letter subsets, and counts all720 permutations of six symbols to recover the exact12-fold inclusion of each of360 four-distinct-letter words. It also checks95 finite algebra cases and eight deliberately invalid conclusions/triples. The universal argument is the written proof above; finite validation is not its replacement and this self-check is not independent review. Source/checker/log hashes are in ../SHA256SUMS.
