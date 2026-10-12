# Completed routes and the next structural question

This is a mathematical chronology. The latest bound is the interval in
`README.md`; older proof files and their reviews remain frozen.

## Results retained with their original scope

The seven/nine cyclic-moment argument proves an asymptotic upper coefficient
`(9-sqrt(33))/12`, and its collision refinement gives a useful finite bound
with a degree-two error. The repair and rotation arguments subsequently
proved a quarter upper bound, and the reciprocal-pair argument then proved
`182/729`. Their old displayed intervals are historical stages.

The ternary eighteen-word template has weighted optimum `2/9`. This is only
an optimum within that template. The fixed classical Jiggs 57-word template
has the strictly larger weighted optimum beta proved in revision 2. Thus
the earlier project conjecture `lambda_4=2/9` is false. The old C4 note's
statement that its *matrix counterexample* does not refute that conjecture
remains literally correct, but that conjecture has now been refuted by a
separate actual GP construction.

The final fourteen-state representation and its count-preserving completion
have independent all-parameter written review. It is an exact representation
on three-letter states; fourteen is not an alphabet-block bound.

## Mechanisms that have reached a mathematical obstruction

1. **Assuming independence after a negligible deletion.** The explicit
   binary block construction in
   `global_upper/ENDPOINT_SUPPORT_AND_INDEPENDENT_CODES.md` contains disjoint
   complete bipartite selected-adjacency graphs. Removing all selected
   adjacency can require order `m^4` deletions. No independent-set upper
   bound may be applied to arbitrary strict codes using this shortcut.

2. **The unrestricted three-color defect bound `E>=1/9`.** The rational
   matrix calculation and probabilistic finite construction in
   `global_upper/C4_DEFECT_AND_COLOR_COUNTEREXAMPLE.md` disprove it. These
   arbitrary colorings are not asserted to arise from canonical levels of
   strict codes. The valid `1/729` bound is the one used in the main theorem.

3. **Order types alone.** `order_codes/probe_rank_types.py` is a completed
   exploratory finite calculation on the 24 orders of four distinct
   letters and 40320 orders of eight distinct letters. Its candidate class
   has at most four selected order patterns, hence leading density at most
   `1/6`. This restricted class cannot improve the exhibited lower bound.
   It is not an upper bound for arbitrary original GP sets or strict codes.

4. **Stationary or cyclic relaxations without full overlap compatibility.**
   The files `global_upper/probe_dependence.py` and `probe_cycle_gluing.py`
   are discovery tools, not universal optimality certificates. Pairwise
   stationarity and the tested local gluing restrictions did not supply the
   missing global implication. No solver timeout or missing example is
   promoted to a theorem.

No old frozen B support enumeration or five-letter template search is a
dependency of these improvements. No enlargement of those enumerations is
needed to reproduce the bounds.

## Continuing question

For a strict code, pair levels must increase on selected two-pair arcs, and
the fourteen triple profiles must be compatible on **every** shift/append
arc. A useful stronger upper bound must couple these constraints rather
than optimize arbitrary three-color matrices in isolation. The fixed target
graph now permits an exact study of which sets of incoming and outgoing
profiles can coexist at each two-letter state. This is the current structural
route; no unproved finite alphabet cutoff or density value is assumed.
