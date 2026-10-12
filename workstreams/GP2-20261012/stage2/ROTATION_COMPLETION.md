# Exact 2-SAT completion at a fixed pair-level rotation bound

GP2-20261012, stage 2. Candidate complete written theorem, no new independent review or Lean certificate.

## 1. Necessary pair levels and rotation counting

For any strict four-window code C, form a directed graph on ordered pairs with ab->cd whenever abcd is selected. It has no three-edge walk, since such a walk concatenates four pairs to a word whose windows at starts 0,2,4 are selected. The maximum incoming walk length therefore defines a level function ell:A^2->{0,1,2} strictly increasing on every selected edge.

Fix any such three-level function (not necessarily derived from a code). Define

    V_ell = {abcd: ell(ab)<ell(cd)},
    E_ell = Pr[ell(ab)=ell(cd) and ell(bc)=ell(da)]

for independent letters drawn from a probability distribution mu. Every primitive cyclic rotation orbit has zero, one, or two words in V_ell: opposite rotations reverse the same strict comparison, so each opposite pair contributes at most one. Orbits of period one or two contribute none. The nonviable orbits are exactly those described by E_ell. The total product weight of **one representative from every viable orbit** is therefore

    T_ell = (1-E_ell)/4.

Every strict code contains at most one member of a rotation orbit. Otherwise repeating the four-letter word supplies selected occurrences at starts 0,j,4 for 1<=j<=3. The same repetition excludes short-period words individually. Thus every strict C contained in V_ell has density at most T_ell.

## 2. Independence gives an exact binary completion problem

Here independence means there are no selected u,v (including u=v) with suffix_3(u)=prefix_3(v), i.e. no selected consecutive shift vertices.

An independent subset of V_ell is automatically strict. If three selected windows had positive gaps a,b with a+b<=4, independence would force a,b>=2, hence a=b=2. The corresponding ordered-pair walk would have three selected edges, whose strictly increasing levels require four distinct values in {0,1,2}, a contradiction.

Now ask whether an independent strict code can select one member of **every** viable rotation orbit. Put one Boolean variable at each two-candidate orbit; its two literals mean selecting the respective candidate. A singleton orbit is represented by a variable with candidate-0 unit clause. For each pair of adjacent candidate words u,v, impose

    not(select(u)) OR not(select(v)).

This is an exact 2-CNF formula. A satisfying assignment selects one word per orbit, excludes adjacency, and is strict by the preceding paragraph. Conversely any such independent completion gives a satisfying assignment. A repeated candidate in an adjacency constraint simply produces a unit prohibition.

**Theorem.** Independent rotation saturation at a fixed ell is decidable by 2-SAT. For a strictly positive finite letter distribution, it is also equivalent to attaining the weighted bound T_ell in the independent subclass. With zero weights, first restrict the alphabet to its positive-weight support for the weighted-attainment question; imposing zero-weight orbits unnecessarily can change feasibility.

The formula has O(|A|^4) variables and at most O(|A|^5) indexed adjacency conflicts. This is a decision theorem **for fixed ell**, not an algorithm optimizing ell over all alphabets. UNSAT does not, by itself, exclude a nonindependent strict saturation. The separate forced-overlap theorem can sometimes do so.

## 3. Exact, replayable certificates

`model.py` uses the implication graph: for each clause not(u) OR not(v), add u -> not(v) and v -> not(u); for a forced singleton u, add not(u)->u. Opposite literals in one strongly connected component prove infeasibility. The output certificate contains paths in both directions between one literal and its negation, each arc justified by original candidate words or a singleton orbit. A verifier need only validate these paths against original rotations and suffix/prefix equality; it need not trust an SCC implementation.

For a SAT instance the selected words are a direct certificate. Check one candidate from each viable orbit, no adjacency, the pair-level inequalities, and strictness. No floating-point solver is involved.

## 4. Two fixed examples and their limits

Use letter order A,B,C,D and the fixed level array

    1 1 0 2
    0 1 0 1
    1 2 0 2
    0 0 0 1.

The **classical** 57-word Jiggs dictionary frozen in stage one selects exactly one member of every viable orbit and has disjoint triple-prefix and triple-suffix supports. Therefore it attains T_ell for every distribution on these four letters. For integer weights (5,5,3,3), normalized by 16, the exact equality is

    E_ell = 1651/16384,
    T_ell = 14733/65536.

This reinterprets an inherited lower-bound construction; it does not improve its density or claim the dictionary as new.

The six-letter level array in `certificate.json` has 310 viable orbits, 189 singleton orbits, and 809 ordered candidate-adjacency conflicts. Its independent saturation formula is UNSAT, with a three-arc implication path in each direction between one literal and its negation. Separately, it has an explicit triple of forced overlapping windows, so even a nonindependent strict code cannot attain its rotation bound. See `FORCED_OVERLAP_BOUND.md` for that stronger but differently justified conclusion.

## 5. Source relationship

Cyclic rotation counting is classical in comma-free coding, and 2-SAT implication graphs are a standard algorithm. The stated contribution is the precise fixed-pair-level equivalence for independent strict-window completion, its original-word certificate semantics, and its use to reject candidate level structures that look favorable only under rotation counting. It is not an unrestricted comma-free-code algorithm or a proof that all extremizers are independent. Historical novelty remains unverified.
