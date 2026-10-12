# Independent reconstruction of the valuation-18 extension

The new independent checker is a parameter change to the reviewer's own
frozen v4 engine, not to the author's kernel. Its source and all eight
odd-value runs were frozen/completed before the first author v5 byte
read. The parent agent supplied the bit18 cancellation observation;
the reviewer reconstructed and checked its exact modular interpretation.
That contact is explicit in `PRE_AUTHOR_FREEZE.json`. No author function
is imported or executed.

## Width lemma, including the half-word

Use the same actual three-pair core as in the accepted v4 review:

    dX=dY=D!=0, dR=-D,
    FX=FY=FR, GY-GX=2D, GY-GR=D mod 2^32.

If 2^18 divides D, both input members of every pair share their low
eighteen bits. The sigma1 output rows at 22..30 depend only on input
positions below 18. The exact row at 31 is input16 XOR input18. Let
e=(D/2^18) mod2 and H=2^31. The input18 XOR change is e in a pair of
difference D or -D. Thus the modular sigma1 derivative is always

    G_i = eH + q_i mod 2^32, |q_i|<2^22,

where q_i is the ordinary low-22-output difference. The ordinary top
contribution may be +H or -H; those signs are equal modulo 2^32.
The common eH cancels in both differences. Consequently

    A=qY-qR = D mod 2^32, B=qY-qX = 2D mod 2^32,
    |A|,|B|<2^23, |B-2A|<3*2^23<2^32.

Hence B=2A and |A|<2^22. Nonzero A is divisible by 2^18, so
D is +/-k*2^18 for k=1..15. The already accepted v4 excludes every
even k. The new finite task is exactly k=1,3,5,7,9,11,13,15.
Global priming swap covers their negative orientations.

The width proof `../width-reduction-v5/PROOF.md` was read after this
reconstruction. Its proof agrees, and its exact universal row identities
are independently checked by `controls_and_compare.py`. The width
checker hash is bound as an author dependency; its program is not
executed or used as an independent proof premise.

## Exact new finite model

Reverse the third actual pair and parameterize the three plus-D bases
as `(a,a+D),(b,b+D),(c,c+D)`. The exact equations become

    Fa=Fb=-Fc, Gb-Ga=2D, Gb+Gc=D mod 2^32.

For each odd k enumerate all 16384 high-input quotients under addition
by k modulo 16384. Each input XOR mask fibre is checked by exhaustive
set equality against its full binary cube. Lower eighteen bits and the
final input bit31 remain free. There is no no-overflow assumption.

Sigma0 output XOR masks lie below bit29. Every new sigma1 XOR mask
has bit31 set, bits22..30 zero, and its remaining bits below22. Remove
bit31 from that mask: its derivative's modular offset H cancels in
Gb-Ga and contributes 2H=0 in Gb+Gc. The remaining scalar derivative
is beta_low-2U_low, using actual sigma1 output bits from the same 32
base variables as sigma0. The discarded output31 sign has coefficient
2H=2^32 in that expression, so it is irrelevant modulo 2^32; the
actual input bit31 is still retained in all original sigma output rows.

The same independently written 31-bit masked-add/subtract carry engine
then excludes each complete three-mask product:

| k | Masks per pair | Triple cases | Satisfiable final systems |
|---:|---:|---:|---:|
| 1 | 14 | 2744 | 0 |
| 3 | 25 | 15625 | 0 |
| 5 | 35 | 42875 | 0 |
| 7 | 34 | 39304 | 0 |
| 9 | 43 | 79507 | 0 |
| 11 | 53 | 148877 | 0 |
| 13 | 52 | 140608 | 0 |
| 15 | 41 | 68921 | 0 |

All 538461 triples are processed. The execution visits 338778 exact
carry/GF2 nodes and detects 17101 binary contradictions, as recorded
in `INDEPENDENT_RUN.json`. Arithmetic width and parity cuts precede
the linear model; every cut is a necessary condition, not a sampled
feasibility approximation.

## Independent controls and author comparison

The controls rebuild both positive and negative input cubes, independently
classify all 12245 twin-mask pairs, and construct/directly check an
actual word witness for every feasible twin-mask pair. There are two
feasible mask pairs for k=5, one for k=13, and two for k=15. Their
stored author branch counts differ from mask-pair counts and are kept
distinct. These actual twin examples show why a two-pair exclusion
would be false; the complete three-pair engine excludes each extension.

The author certificate's complete 612 third-mask tests and all 1253
direct XOR row receipts pass. All twenty manifest artifacts, frozen v4
author dependencies, the accepted v4 review, and width proof/checker
hashes are checked. A receipt RHS mutation is rejected in memory.

A direct width control uses x=0, x'=2^18. Its ordinary sigma1 difference
is H+0x102, which exceeds the old ordinary bound; its low-output
difference is 0x102. Both orientations have the same modular H offset,
and their sum is zero modulo 2^32. Thus silently dropping H is detected.

The independent checker/source scope is the eight new odd cases. The
combined theorem <=17 additionally uses the accepted frozen v4
exclusion and original support bridges. No global support classification
is rerun, and no actual pair of SHA-256 message schedules is constructed.
