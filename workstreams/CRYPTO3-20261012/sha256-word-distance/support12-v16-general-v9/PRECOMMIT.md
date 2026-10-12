# Precommitted bounded extension at exact valuation 16

## Question and scope

For `D=q*2^16`, with positive odd `q`, test the selected twin condition

```text
F_D(x)=F_D(y)                    (mod 2^32),
G_D(y)-G_D(x)=2D                (mod 2^32),
```

using the actual SHA-256 small-sigma derivatives on the same directed
word pair.  The fixed domain for the certificate run is every odd
`q` in `1..31`.  Negative `D` is obtained only by the exact pair-reversal
argument.  This is a selected local condition, not the third joint-image
membership, reciprocal edge, remaining support rows, or base completion.

## Facts known before this bounded run

The accepted v8 package proves exclusion for `q=1`.  During mechanism
development, non-certificate exploratory calls tested
`q=1,3,5,7,9,15,17,31`.  They already showed full 32-bit twin survivors
for `q=5` and `q=15`; therefore a uniform all-valuation-16 obstruction is
false.  These exploratory calls are disclosed rather than presented as
preregistered evidence.

The complete odd interval `1..31`, the certificate schema, and the
controls below are fixed before the certificate-generating run.  The
remaining values `11,13,19,21,23,25,27,29` have not been tested here.

## Exact finite mechanism

Addition by `D` changes only the upper half.  Enumerate every upper-half
word `u=0..65535`, group it by
`alpha=(u xor (u+q mod 2^16))<<16`, and independently verify that each
group equals the affine cube encoded by its fixed coordinates.  Thus the
Cartesian square of the classes, with two free lower halves, covers every
ordered pair `(x,y)` exactly.

For every class pair, expand every bit of the modular derivative equations
from independently constructed rotation/shift rows and the exact incoming
integer carry.  Enumerate the at-most-two toggled row bits, verify any
affine compression by its full truth table, and use GF(2) insertion.
Every pruned branch must carry an XOR of original affine equations equal
to `0=1`.  Every surviving leaf must be reconstructed as actual words and
checked directly against the standard small-sigma definitions.

## Fixed outcomes and controls

For each q record the input-class count, sigma0 leaves, full twin leaves,
and either all surviving actual word fixtures or the empty result.  The
checker must reject mutations of `x+D`, `y+D`, the common sigma0
derivative, and the sigma1 gap for every stored witness.  It must also
check that dropping sigma1 bit 31 does not accidentally get reported as
the full theorem for any excluded q having a low-31 survivor.

One certificate run only, no SMT/SAT solver, no timeout retry, no extension
of the q range after seeing results.  Runtime target is 180 seconds.

