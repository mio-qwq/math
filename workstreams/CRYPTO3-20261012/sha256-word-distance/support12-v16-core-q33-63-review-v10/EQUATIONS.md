# Frozen equations for the q=33..63 selected-core review

This review uses arithmetic modulo `2^32`.  For a fixed word difference `D`,
define

```
F_D(w) = sigma0(w+D) - sigma0(w)
G_D(w) = sigma1(w+D) - sigma1(w)
```

where `sigma0=ROTR7 xor ROTR18 xor SHR3` and
`sigma1=ROTR17 xor ROTR19 xor SHR10` are the SHA-256 message-schedule
functions.  The independently encoded selected three-pair core is

```
A = F_D(x)
T = G_D(x) + D
F_D(y) = A
G_D(y) = T + D
F_D(z) = -A
G_D(z) = -T
```

for `D=q*2^16` and odd `q` from 33 through 63.  Additions, subtractions and
negations are modulo `2^32`.

The Boolean encoding below uses little-endian word bits, explicit ripple
carries, truth-table XOR gates, and two binary clauses per equality bit.  It
is written without importing the author generator.  Only after construction
is its DIMACS byte string compared with the author file.

For sign reversal, put `D'=-D` and replace each base word `w` by `w+D`.
Directly from the definition,

```
F_{D'}(w+D) = -F_D(w),  G_{D'}(w+D) = -G_D(w).
```

Consequently the selected-core equation vector is preserved, with `A` and
`T` negated.  This supplies the negative-`D` counterpart only for the same
local core.

The intended conclusion is strictly finite and local: no SHA-256 message
pair, no distance-13 construction, no distance-at-least-14 theorem, and no
Lean formalization is asserted.
