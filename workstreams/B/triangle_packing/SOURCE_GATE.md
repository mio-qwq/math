# Gate and new reservation, 2026-10-10 06:21 UTC

B reserves arXiv:2603.25113v1 Section 5, Problem 1 and Conjecture 2,
by Ayman El Zein and Maidoun Mortada, submitted 26 March 2026.
This is a different exact class/question from the accepted 0-saturated
local-girth-at-most-four packing-4 theorem. No new root project number.

Original: https://arxiv.org/html/2603.25113v1#S5
Version record: https://arxiv.org/abs/2603.25113

Class: finite simple undirected subcubic graphs, each degree-three vertex
adjacent to at most one degree-three vertex, and every degree-three vertex
on a triangle (g3=3, maximum of local girths). No minimum degree or
connectedness assumption added. Problem 1 asks whether every such graph
has each of the packing sequences (1,2,3,3), (1,2,2,4), (2,2,2,2,4).
Conjecture 2 asks whether packing chromatic number is at most five, i.e.
the sequence (1,2,3,4,5). Equal labels i must have graph distance strictly
greater than the corresponding sequence entry. Repeated entries still
denote DIFFERENT colors. A graph failing any asked sequence gives a
negative answer to that part, not automatically to the other parts.

Sources were read in the original. Search rounds used exact paper ID,
Conjecture 2, proof/erratum/counterexample, and 1-saturated with the exact
(1,2,3,3) sequence and both authors. No later same-scope resolution was
located. Other results on (1,1,3,3) or (1,2,2,2,2) do not settle this task.
Prior author-page gate for this shared paper is retained in packing_gate/;
new searches alone do not establish historical novelty. Before final
claim refresh author pages and later versions again. Current status:
bounded source gate, not a certified assertion of global openness.

Visible coord/distributed d8f2994 and all branch heads checked. A's matching
powers, C's asymmetric covers and ROOT's orientation-spectrum Conjecture
4.30 are distinct. No conflicting claim seen; concurrency remains possible.

Mechanism: each triangle has at most two degree-three vertices. Apart from
small overlapping-triangle exceptions, contracting the disjoint triangles
should leave path/cycle components. Search exact triangle necklaces and
capped chains, with connector length >=2 to preserve 1-saturation. First
experiment is bounded, aimed at a small UNSAT witness or an explicit
transition constraint. No blind enlargement of the old 95165-case search.
A negative claim must have a complete exact unsatisfiability check, separate
from the discovery solver, plus original-hypothesis verification. If tests
only find colorings, do not infer the universal statement. Derive new
structure or stop rather than repeating a larger unchanged window.

06:22 UTC author-page refresh: both laboratory publication pages were opened:
https://kalma-lu.com/authors/15/Maydoun-MORTADA and
https://kalma-lu.com/authors/11/Ayman-EL-ZEIN . No resolving item was listed.
Search also located the August 2026 claw-free follow-on arXiv:2608.02566,
whose stated palettes concern different questions. Author lists may lag.

06:29 UTC post-proof searches: exact "1-saturated" with "2,2,2,2,4",
the exact arXiv ID with "Problem 1", and local girth / degeneracy / square
coloring / triangle-necklace combinations located no prior same-scope proof.
This does not certify novelty. The new result is affirmative for Problem 1's
THIRD palette only, strengthened to (2,2,2,2,r) for arbitrary positive r.
The other two palettes and Conjecture 2 remain unresolved by this packet.

06:39 UTC second-palette result: SECOND_PROOF.md and a 139-state finite
invariant give a computer-assisted affirmative answer to (1,2,2,4).
Exact-palette and local-girth follow-up searches found only the original
question and different palettes, not a prior same-scope resolution. The
normal restricted transfer model has five zero-trace matrix states and
an infinite family of failures; it is explicitly NOT a proof by itself.
Allowing one special length4 connector resolves the obstruction, with a
closed 139-state invariant. Original graph checks are separate. This is
still B self-review, not independent acceptance. Problem1's first palette
and Conjecture2 remain unresolved by the two proofs.

06:49 UTC first-palette result: FIRST_PROOF.md supplies a complete reduction
and71-matrix invariant for (1,2,3,3). Its42-state interface has a proved
long-connector cutoff from a27-state path automaton, not a guessed cutoff.
An exact-palette and Problem1 follow-up search located no earlier answer.
All three parts of Problem1 now have B self-verified positive candidates;
Conjecture2 is still open in this stream. Independent review is pending.

06:56 UTC original Conjecture2 result: FIVE_PROOF.md gives a full semantic
reduction and a139-matrix,90-state certificate for the ORIGINAL five-color
claim. This is separate from the second palette's coincidentally139-state
six-by-six certificate. Color5 is restricted only in the construction,
not as an extra graph hypothesis. A fresh exact-ID, Conjecture2 and
triangle-local 1-saturated five-color search found no same-scope prior
resolution. Authors' lab pages were checked earlier this same run. This
remains a bounded literature gate, not a firstness certification.
All three parts of Problem1 and Conjecture2 now have B self-verified
positive proof candidates; none of these new packets has an independent
acceptance recorded here. The earlier permutation counterexample remains
a distinct accepted result. No new counterexample is claimed in this run.
