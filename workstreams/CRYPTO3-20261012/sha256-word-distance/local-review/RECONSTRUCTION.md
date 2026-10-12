# Independent reconstruction of two local sigma1 claims

This review began from the SHA-256 definition, before inspecting the
discoverer's proof or mechanism files. It is an independent AI review,
not external human peer review. The object is

```
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x),
h(x) = x + g(x) (mod 2^32).
```

## Mechanism 1: XOR masks and necessary carry conditions

For a putative collision put `d=x xor y` and `e=g(d)`. Linearity of `g`
over F2 gives `e=g(x) xor g(y)`. Equality of the two sums implies that the
signed bit differences in the two summands add to zero modulo `2^32`.
At bit `i` each signed summand is zero or +/-1 according to `d_i,e_i`.
The incoming signed carry belongs to `{-1,0,1}`. If the preceding bit has
`d=e=0`, its outgoing carry must be zero. A bit with exactly one active
mask would then be odd and impossible. Bit zero also starts with carry
zero. Therefore

```
((d xor e) & ~((d | e) << 1)) & 0xffffffff == 0
```

is necessary. This discards correlations between summand bits, so a
surviving mask alone would not construct an actual collision.

If `x=y mod 2^b`, both `d` and `e` have their bottom `b` bits zero. The
linear kernel of `d -> (low_b(d), low_b(g(d)))` can be reconstructed
without a SAT solver. Preliminary independent row elimination for `b=13`
gave dimension six, and all 63 nonzero masks failed the carry condition.
The deliverable checker will reconstruct the kernel by a separate
full-column elimination and record one exact obstructing bit per mask.

## Mechanism 2: an additive power of two has an interval XOR mask

If `y-x=2^k mod 2^32`, then `x xor y` is a contiguous nonempty run of ones
starting at bit `k`. The compensating difference `g(y)-g(x)=-2^k` forces
`g(d)` to be another such run starting at `k`. Testing the 528 possible
input runs from the standard definition leaves only

```
k=0, d=0xffffffff, g(d)=0x003fffff.
```

For this last case the actual ordered input pairs can only be
`(0x7fffffff,0x80000000)` or `(0xffffffff,0)`, because adding one must
toggle all 32 bits. Both pairs can be checked directly. A negative
power-of-two difference reduces to a positive one by swapping the pair.

## Mechanism 3: locate an actual boundary example

The `b=12` kernel has dimension eight in preliminary elimination. A new
small computation will first screen its 255 nonzero masks by the same
necessary carry condition, and then retain the exact `g` relation in an
SMT equation `h(x)=h(x xor d)` for surviving masks. The sole purpose is
to find a real 32-bit pair testing the claimed sharp modulus threshold.
Any candidate will be reconstructed by a separate per-output-bit
implementation of `g`; SMT SAT alone is not the delivered verification.
Timeout or unknown will not imply nonexistence.

Source definition: NIST FIPS 180-4, Section 4.1.2,
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.

## Completed independent reconstruction

The planned classifications have now been completed. Full-column
elimination reproduced the rank-26 and rank-24 maps and the respective
6- and 8-dimensional kernels. All 63 nonzero low-13 masks were rejected;
among all 255 nonzero low-12 masks exactly `fbca7000` survived the
necessary carry relaxation. The exact pair
`x=cd027f2a, y=36c80f2a` has common low bits `f2a` and common
`h` value `3d45fee8`. It was obtained before receiving or inspecting
the discoverer's different witness. All 528 power-of-two input intervals
were also checked, with the unique interval exception rejected by the
two actual word pairs described above.

The complete certificate, separate verifier, actual run record, and
mathematical derivation are in `independent_certificate.json`,
`check_independent.py`, `INDEPENDENT_RUN.json`, and
`INDEPENDENT_PROOF.md`. The first run exited zero and rejected all eight
damaged controls. At this checkpoint no discoverer proof or code has
been read. Subsequent precise-version comparison is recorded separately
and does not retroactively form part of this blind reconstruction.

