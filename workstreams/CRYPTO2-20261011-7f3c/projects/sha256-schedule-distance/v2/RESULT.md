# SHA-256 v2 result

For the actual 32-bit, 64-word SHA-256 message expansion, the frozen
necessary support constraints have exactly **15 supports of weight 13**.
Two cannot occur for **any pair of actual input blocks**, by the universal
sigma-chain contradiction in PROOF.md. Thirteen remain undecided.

The central arithmetic obstruction is:

    delta_x=2^31, delta_a=-delta_sigma0(x),
    delta_b=delta_sigma0(a), delta_sigma1(b)=2^31

is impossible. The first three force delta_b !=2 mod 4, whereas the last
forces delta_b=2 mod 4. This uses actual SHA-256 shift constants, not an
independence assumption or a zero-base approximation.

The bound is still **at least 13 unequal words**, not 14. No pair attaining
13 is known here. There is no collision/preimage construction, attack
complexity improvement, or security theorem for the compression function.

The same tail without the forced half-word delta is feasible: TAIL.json
and the direct checker prove this. Extending the exclusion therefore
requires additional global equations.

Verification: `python reproduce.py` (from this directory) regenerates the
support file exactly and checks finite proof dependencies plus seven
negative controls, using only Python's standard library. See RUNS.json,
SHA256.json, ATTEMPTS.md, SOURCE-GATE.md and HANDOFF.md.

**Awaiting independent review.** No SHA Lean verification. Generic methods
are prior art; exact-result originality and practical importance remain
unconfirmed. This does not yet reach the user's major-result objective.
