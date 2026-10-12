# The coupled local valuation bound is sharp

This object is four 32-bit words, not two input blocks. It resolves the
sharpness of the local four-word theorem only. All arithmetic below is
modulo 2^32 and uses the original SHA-256 small sigmas, f=sigma0 and
g=sigma1, with bit 0 least significant.

Consider arbitrary ordered pairs P=(p,p') and Q=(q,q') satisfying

    p'-p = q'-q = D != 0,
    g(q')-g(q) = -D,
    f(p')-f(p) = -(f(q')-f(q)).

The reviewed coupled theorem proves v2(D)<=11. The following explicit
object proves that 11 is attained by this local system:

| word | value | f(value) | g(value) |
|---|---|---|---|
| p | 0019f0ed | a6384dfa | c66b2673 |
| p' | 973448ed | dbf38441 | ad4eb46e |
| q | dff7f75f | 5996e6f8 | 0573e9f8 |
| q' | 77124f5f | 23dbb0b1 | 6e5991f8 |

Indeed, both input differences equal `971a5800`; its low twelve bits
are `800`, so it is divisible by 2^11 but not 2^12. The two f differences
are `35bb3647` and `ca44c9b9`, which sum to zero. The q g difference is
`68e5a800`, whose sum with `971a5800` is zero.

Thus the largest possible v2(D) in this exact local system is 11. Any
proof of a stronger restriction on the seven support applications must
use information outside these three local equations. No lower bound on
the distance of full expansions is improved by this witness.

The one discovery query returned SAT within the recorded 15-second
budget. Its bit-vector encoding is in `probe.py`; its execution is in
`RUN.json`. The witness's correctness does not depend on that solver.
`check.py` separately reconstructs each output bit directly from its
three input positions, verifies all displayed values and differences,
and rejects eight damaged words, constants or claimed outputs. This is
the discoverer's separate checker. A distinct AI agent's reconstruction
and exact-version receipt, when available, are in
`../coupled-sharpness-review/`; that is not external human peer review.

The local conditions come from the separately proved support bridges.
This object has not been assigned to all active positions, and neither
base interpolation nor the full 48 difference equations is asserted.
The mathematical stopping decision is to retain this sharp bound and
use additional original recurrences before further universal exclusion
attempts. No timeout extension or seed sweep is part of this test.
