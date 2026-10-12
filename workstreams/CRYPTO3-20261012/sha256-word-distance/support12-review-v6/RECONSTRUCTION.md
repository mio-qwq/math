# Independent reconstruction of the valuation-17 boundary

The reviewer uses a parameterized copy of their own frozen v5 engine.
Before reading any author v6 file, its complete output-mask constants
were restored and a full 32-representative run was started. The parent
quarter-width observation is disclosed in `PRE_AUTHOR_FREEZE.json`;
the modular derivation below was reconstructed independently. No author
checker, generator, or discovery program is imported.

## Width reduction applies to the new valuation-17 layer

Use the already accepted actual three-pair core, in the original
orientation:

    dX=dY=D!=0, dR=-D,
    FX=FY=FR, GY-GX=2D, GY-GR=D mod N=2^32.

The frozen v5 result has already excluded v2(D)>=18. It is enough to
consider **v2(D)=17**; the following finite representative argument does
not silently assume that D merely nonzero implies D nonzero modulo
P=2^31.

At valuation 17, the two members of each actual input pair share their
low seventeen bits. Sigma1 output rows at bits22..29 depend only on
input coordinates below17. The exact row at bit30 is input15 XOR17,
and the row at bit31 is input16 XOR18. Input bit17 always changes for
differences D or -D. Put Q=2^30 and P=2^31. Its bit30 derivative is
either +Q or -Q, which are equal **modulo P**. Bit31 contributes a
multiple of P and also vanishes in that quotient. Consequently

    G_i = Q + q_i mod P, |q_i|<2^22,

where q_i is the ordinary difference of the low twenty-two output
bits. This is a statement in the quotient. It does not give G_i=Q+q_i
modulo N, and it does not assert an ordinary full-output bound.

Set A=qY-qR and B=qY-qX. The two gaps give A=D and B=2D modulo P,
and |A|,|B|<2^23. Hence B-2A is a multiple of P with absolute value
below 3*2^23<P, so B=2A and |A|<2^22. Since v2(D)=17, A is a
nonzero odd multiple of 2^17. Thus

    D = +/- q*2^17 + h*2^31 mod N,
    q in {1,3,...,31}, h in {0,1}.

A simultaneous priming swap negates every actual derivative and keeps
the original core in its original form. The negative-q lift maps to
positive q and the same h because -2^31=2^31 modulo N. Exactly the
32 positive-q/h representatives remain.

## The finite core remains modulo 2^32

Reverse the third actual pair, obtaining three plus-D pairs on actual
bases a,b,c. The required equations are exactly

    Fa=Fb=-Fc, Gb-Ga=2D, Gb+Gc=D mod N.

Every input XOR-mask class is enumerated from all 32768 high-input
quotients, under addition of q+h*2^14 modulo 2^15. Its fibre is checked
against its entire binary cube. Low seventeen bits and input bit31
remain free. Input carry overflow is included.

For each original sigma map, let beta be its **complete 32-bit**
output XOR mask and U be the actual unprimed sigma output masked by
beta. Its derivative is beta-2U modulo N. Thus each equality becomes
an exact masked equation X=T modulo 2^31, by the equivalence

    2X=2T mod 2^32  iff  X=T mod 2^31.

This is a different use of modulus 2^31 from the width quotient above.
It does not weaken any original core equation: the complete beta
constants enter T, including sigma1 beta31, and the complete D enters
the last G target, including h*2^31. The actual output variable at
bit30 enters the masked X term and its original input-bit XOR row is
retained. Only the output variable at bit31 has coefficient 2^32 in
the original derivative and is irrelevant modulo N. Sigma1 beta31's
constant coefficient 2^31 is **retained**, not discarded.

Sigma0 masks have bit31 set in this layer. Their complete constants
are likewise retained. All sigma0 and sigma1 rows of one word use the
same 32 actual input variables, for 96 variables overall. No ordinary
addition linearity of either sigma is assumed.

The independent engine interleaves all four masked equations across
31 output bits, branching on complete local Boolean carry truth tables
and rejecting only exact binary contradictions. The final carry is
unrestricted, as required by the exact half-carry congruence. It uses
the same audited signed-carry/GF2 implementation as the accepted v4/v5
reviews, restored to full output masks in this stage.

An inexpensive width cut uses only the lower22 output XOR masks. In
the weaker width quotient, G differences have the required ordinary
low-output values 2*q*2^17 and q*2^17, because their absolute ranges
are far below P. Thus their necessary mask magnitude bounds are valid
for both h values. The comment naming an ordinary output-mask bound
in the source refers here only to these low-output parts; it is not
an ordinary bound on the full sigma1 derivative.

The complete execution and author comparison will be bound by the
separate frozen review receipt. Until that receipt is supplied, this
file describes an independent model, not an accepted new ceiling.

## Completed execution and comparison

The initial complete run finished before the first author-file contact.
All 32 fullmod-N cases are unsatisfiable. They cover 7,538,454 triple
mask cases, visiting 2,819,229 carry/GF2 nodes and detecting 94,446
binary contradictions. The initial uncached execution took 192.9
seconds. Both lifts are separate cases even though their mask counts
coincide.

| q | Masks per pair, each h | Triple cases per h |
|---:|---:|---:|
| 1 | 15 | 3375 |
| 3 | 27 | 19683 |
| 5 | 38 | 54872 |
| 7 | 37 | 50653 |
| 9 | 47 | 103823 |
| 11 | 58 | 195112 |
| 13 | 57 | 185193 |
| 15 | 45 | 91125 |
| 17 | 54 | 157464 |
| 19 | 75 | 421875 |
| 21 | 85 | 614125 |
| 23 | 74 | 405224 |
| 25 | 73 | 389017 |
| 27 | 83 | 571787 |
| 29 | 72 | 373248 |
| 31 | 51 | 132651 |

After source contact, `controls_and_compare.py` independently checks
all 32 compressed cases against their original raw SHA256 values,
all positive/negative cubes, all 111,718 twin-mask indices, every one
of the 7,068 third-mask tests, and 10,914 per-case stored XOR receipt
identities. It does not import the author's kernel. Their raw JSON
totals 20,167,680 bytes and the XZ data totals 360,716 bytes; each
individual recovered raw byte string is bound in the comparison run.

The controls independently classify the twin mask pairs and recover
actual word witnesses for all 32 feasible mask pairs. Each such witness
is evaluated with the original sigmas and the full native modulus N,
including its complete D lift. These are twin witnesses, not three-pair
or actual message witnesses. The author's 142 surviving affine twin
branches are a different count and are kept separate.

Negative controls detect deletion of the h=1 lift, using the quotient
quarter identity at the full modulus, an invalid ordinary full-output
width bound, removal of the sigma1 beta31 constant, and corruption of
a receipt RHS. The accepted v5 receipt and frozen author dependencies
are checked byte for byte.

The accompanying `REVIEW.md` and `REVIEW_RECEIPT.json` provide the final
acceptance disposition and supersede the earlier pending-review scope
sentence. Old v4/v5 files are unchanged.
