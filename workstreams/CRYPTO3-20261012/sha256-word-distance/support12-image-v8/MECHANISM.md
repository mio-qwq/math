# Budget and mechanism fixed before computation

This stage asks whether the already accepted joint-image criterion plus the
reciprocal `sigma0` edge has a small obstruction at exact `v2(D)=16`, or
instead admits a concrete selected-local-system witness.

The first finite probe is exactly the canonical residue `D=0x00010000`.
It enumerates the actual input-XOR carry classes for three directed pairs of
differences `D,D,-D`, then imposes the two `sigma0` equalities and two
`sigma1` gap equalities modulo `2^32`.  If a three-pair survivor is found,
its resulting numerical `A` is tested for the reciprocal edge by an exact
one-pair carry search for input difference `A` and `sigma0` derivative `D`.
All output relations use the original bit rows and integer carries.

Budget fixed before the run: one canonical `D`, at most 300 seconds wall
time, no SMT/SAT call, no retry with another `D`, and no extension of an
UNKNOWN result.  A survivor must be reconstructed as actual 32-bit words
and independently checked directly from the SHA-256 small-sigma definitions.
An empty search is only a proof for this one numerical `D`, not for the
other exact-valuation-16 residues.  A survivor is only a local selected-core
witness, never a 16-word message pair or a distance-13 witness.

