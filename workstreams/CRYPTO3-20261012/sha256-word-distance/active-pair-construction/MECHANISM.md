# Constructing a full active-pair assignment for support 0

This is a bounded examination of a new construction mechanism for the
actual SHA-256 message schedule. It concerns the full 48 modular
difference equations, with every active position assigned its own actual
32-bit word pair. A solution of these equations would still require the
ten exact base-lift residual equations before it could be called a pair
of actual schedules. No distance-13 witness is presently claimed.

## Mathematical question recorded before computation

For the support

    S0 = {2,9,10,16,23,24,30,37,38,44,51,52,58},

write the exact interface of a word pair `(x,x+d)` as

    (d, F, G) = (d, sigma0(x+d)-sigma0(x),
                   sigma1(x+d)-sigma1(x))  modulo 2^32.

First derive all 48 difference equations from the original lag set. Then
eliminate only explicit signed equalities, with no division by a
nonunit, and determine whether the equations factor into adjacent
modules on these actual-pair interfaces. The initial and terminal
interfaces must remain distinct. In particular, the word pairs at
indices congruent modulo 14 are not identified.

The prospective constructive mechanism is exact XOR translation inside
a fibre of a known local `G=-d` collision. For a fixed pair `(x,y)` and
translation mask `z`, determine the linear conditions under which
`(x xor z,y xor z)` preserves its modular difference and its sigma1
modular difference. The remaining freedom in sigma0 may enable adjacent
interfaces to join. Unlike a free assignment to `(d,F,G)`, this mechanism
always evaluates both sigmas on the same actual word pair.

Any bounded calculation will answer whether such a fibre supplies the
specific module interfaces derived from all 48 equations. A failed
restricted fibre construction will be reported only as a failure of that
construction. There will be no unrestricted tail rerun, periodic-pair
ansatz rerun, zero-base schedule search, or extended timeout.

## Inputs and scope

The only schedule operations are 32-bit modular addition,
`sigma0 = ROTR7 xor ROTR18 xor SHR3`, and
`sigma1 = ROTR17 xor ROTR19 xor SHR10`, with least-significant bit 0.
The support is the frozen CRYPTO2 support 0 at commit
`80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51`.
All coordinates not in S0 have zero word and sigma differences.
Every active pair must be unequal. Base words remain arbitrary.

## First fibre result and the single bounded construction test

Direct derivation gives 24 nonzero equations and 24 identities. The
root-supplied coupled seed is

    q  = 00305680, q' = 88abc2db,
    p  = 96e4e732, p' = 1f60538d.

Its directly recomputed interfaces are

    D = 887b6c5b,
    F(q) = 410c6383, G(q) = -D,
    F(p) = bef39c7d = -F(q).

The complete fixed-XOR fibre preserving `(d,G)` at q has dimension 5,
32 pairs and 16 sigma0 differences. Preserving `(d,F)` at p gives
dimension 2 and four sigma1 differences. Thus the seed has a specific
finite amount of interface freedom; that freedom is not an arbitrary
choice of both sigma differences.

Before the next calculation: examine one exact, finite construction
family. Each Q position independently takes a member of the fixed-XOR
q fibre with `(d,G)=(D,-D)`. Each P position independently takes a pair
with the fixed input XOR mask of p and modular difference D. Each R
position independently takes a pair with input XOR mask
`sigma0(q xor q')`. This last mask is natural because reversing the
sigma0 images of a Q pair gives a pair with word difference `-F(Q)`.
R pairs are then allowed their entire fixed-mask fibre; they are not
required to equal those sigma0 images.

For a fixed XOR mask, prescribing each modular difference amounts to
linear constraints on the corresponding changed-bit signs, apart from
the harmless top-bit sign. Solve these exact binary systems for every
interface needed by the adjacent modules, retaining each independent
pair and all initial/terminal equations. A finite path search will then
decide this one fixed-mask construction family completely. Failure will
exclude only these three seed masks and D, and stops this mechanism.
