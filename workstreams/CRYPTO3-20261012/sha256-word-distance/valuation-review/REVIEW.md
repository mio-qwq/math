# Independent review of the four-support valuation restriction

## Decision

The reviewed written theorem is correct, with the stated conditional
scope. For an actual pair of SHA-256 expanded messages whose exact
support is one of frozen indices `6,7,12,13`, the indicated differences
satisfy

```
d_x=d_y=D != 0, d_r=-D,
F_x=F_y,
G_y-G_x=2D, G_y-G_r=D,
v2(D)<=20.
```

The support coordinates are respectively `(19,35,44)`, `(21,37,46)`,
`(18,34,43)`, and `(20,36,45)`. No assumption on the actual base-message
words is needed. This review found no mathematical gap in the precise
written version below.

This is an independent AI review, not external human peer review.
No Lean compilation or historical novelty clearance is claimed. The
theorem excludes a divisibility stratum in four supports, not an entire
support. It does not raise the global schedule distance bound from 13,
construct an actual distance-13 message pair, or establish a hash attack.

## Exact reviewed version

| Author artifact | SHA256 |
|---|---|
| `mechanism/VALUATION_BOUND.md` | `1edca147825bae48618e56d65730b5cf62ab7ebf50faf085f9226f5f1d95c574` |
| `mechanism/STRUCTURAL-CERTIFICATE.json` | `6fb30742ea7a520e0ce61d57c1ccb1f443ddb51dead591c46728804a701bef1d` |
| `mechanism/check_structural.py` | `e1659b38a9b2f1e4949a53239e5a8de289128f8f969953e6ab316bb09c962077` |
| `supports-v2.json` | `02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf` |

`REVIEW_RECEIPT.json` binds the remaining checked boundary objects and
actual run evidence as well. The review covers those exact bytes;
changed versions require a corresponding updated receipt.

## Reconstruction before reading the author proof

The independent work began from the FIPS definitions and the specified
support coordinates. Before either author proof or structural certificate
was read, it produced:

- the eleven restricted recurrence rows for each support;
- exact integer linear combinations giving the five shared identities;
- the integer size argument reducing a high-divisibility `D` to
  `+/-2^21` using the third pair;
- ten sigma0 carry obstructions for the mixed input-interval cases;
- a parity identity giving a contradiction in the final interval case;
- a solver-free independent checker and complete finite certificate.

`RECONSTRUCTION.md` contains that complete mathematical argument and
the pre-comparison checkpoint. `INDEPENDENT_RUN.json` records its actual
successful execution before the author files were read. The subsequent
comparison did not replace that reconstruction.

There is a useful implementation distinction in the middle of the proof.
The independent reconstruction uses `F_x=F_y` and ten sigma0 gap
obstructions to force both input carries to reach bit 31. The author
uses the sigma1 derivative gap and ten sigma1 gap obstructions. After
reading the author version, the latter ten gaps were also independently
checked from the per-output-bit sigma definition. Both arguments work.
The resulting parity identity was independently found with exactly the
same coefficients as the author's displayed identity.

## Mathematical audit

### Original recurrence and modular algebra

All 44 concrete recurrence substitutions are correct when generated
from lags `2,7,15,16` and the exact support bytes. The independent
certificate also verifies 20 integer linear-combination identities,
not just the restricted row labels. Those combinations use coefficients
`0,+/-1,+/-2`; they require no division in `Z/(2^32)`.

All times remain in `[16,63]`, including the shift to support 12. The
positions `x,y,r` are active, giving the claimed nonzero differences.
Setting differences outside the support to zero is legitimate for the
nonlinear sigma differences too: the underlying words are then equal.
It does not set the base words themselves to zero.

### Ordinary integer representatives and the indispensable third pair

When input differences are divisible by `2^21`, all sigma1 output
differences have an ordinary integer representative strictly between
`-2^22` and `2^22`. This follows directly from the unchanged output
bits 22 through 31, and is valid for every base word.

Writing `A=G_y-G_r` and `B=G_y-G_x` for those ordinary representatives,
the identities give `A=D mod 2^32` and `B=2D mod 2^32`. The strict
bound `|B-2A|<3*2^23<2^32` makes the congruence `B=2A` an integer
equality. It follows that `0<|A|<2^22`, so its divisibility by `2^21`
leaves only `A=+/-2^21`.

This step uses both `G` identities. It does not infer the fixed
difference from the two-pair subsystem alone. Priming swap covers the
negative case and preserves all the original equations.

### Input carry intervals and wraparound

Adding `2^21` produces exactly one interval of toggled bits `[21,e]`.
For `e=31`, bits 21 through 30 of the unprimed input are one, while
bit 31 is unrestricted. This explicitly covers a carry ending at the
top bit and a carry wrapping out of the word.

If neither interval reaches bit 31, the sigma1 derivative magnitudes
cannot give a gap of `2^22`. In a mixed case, every author gap has both
preceding mask bits zero, one current mask bit active, and index below
22. The lower signed contributions have magnitude strictly less than
the current bit's weight. Their required divisibility forces them to
sum to zero, after which the singleton bit contradicts the next output
bit. No final zero carry is imposed in this modular argument.

### Equal-mask signed sums and the final identity

When both intervals reach bit 31, their common masks are
`alpha=ffe00000`, `f(alpha)=1e03fff8`, `g(alpha)=003f980c`.
For `z` the XOR of the two unprimed inputs, bits 21 through 30 vanish.
The equality of sigma0 derivatives gives
`f(z)&1e03fff8=0`. The sigma1 derivative gap gives
`g(z)&003f980c=00200000`.

The conversions from signed sums to those bit equations are valid:
the relevant sums have magnitudes below the modulus, and a nonzero
sum of distinct powers of two with coefficients in `{-1,0,1}` cannot
vanish because its highest nonzero term dominates every lower term.
The claimed top-bit coefficient in the sigma1 equation must be one;
all lower coefficients must then vanish.

The universal identity has parity masks

```
f: 0600ffa8, g: 0020000c, raw z: 4ea00000.
```

Independent evaluation on all 32 single-bit inputs confirms the identity.
Linearity makes this a complete check on every word, not a sample.
The three forced parities are `0,1,0`, which contradict their XOR being
zero. All bit-set inclusions used to force those parities were checked.

## Boundary evidence when the third equation is omitted

The author's explicit two-pair example was independently reconstructed:

| Quantity | Hexadecimal value |
|---|---|
| `x, x'` | `80000000`, `00200000` |
| `y, y'` | `29904000`, `a9b04000` |
| Common input difference `D` | `80200000` |
| Common sigma0 difference | `ef042008` |
| `G_x` | `ffdfb814` |
| `G_y` | `001fb814` |
| `G_y-G_x=2D mod 2^32` | `00400000` |

Thus `2^21` does divide a valid nonzero difference in the two-pair
subsystem. A third pair with difference `-D` could not also satisfy
`G_y-G_r=D`, by the strict ordinary-integer bound above. The example
therefore confirms the stated limitation of the reduced subsystem.

All twelve supplied positive half-stratum word pairs and the generic
pair in `TWIN-RUN.json` were directly evaluated using the independent
bit implementation. This verifies the stored witnesses only. Null
traversal entries and completeness of those exploratory cases are not
asserted or needed in this review.

## Actual checks and reproduction

The independent verification used Python 3.12.14 and exited zero.
All 14 controls were rejected, covering wrong sigma constants, damaged
support or recurrence data, omission of the third relation, wrong
integer-combination coefficients, zero difference, missing interval,
incorrect carry bit, altered output mask, parity tampering, corrupted
source bytes, and a false whole-support claim.

The precise-version comparison also exited zero. As an additional
check, it ran the pinned author structural checker with `--negative`;
that run exited zero and rejected all six controls. Actual commands,
stdout, stderr, timings, and hashes are retained in
`INDEPENDENT_RUN.json`, `COMPARISON_RUN.json`, and `REVIEW_RECEIPT.json`.

From this directory:

```
python -B check_valuation_independent.py --negative
python -B compare_valuation.py
```

The first verifies the frozen independent certificate. The second pins
and compares the author bytes, rechecks stored positive word pairs,
and writes a fresh comparison receipt with actual run timing. It does
not edit author files. The independent proof needs neither the
121-case search nor a SAT solver, and neither was rerun for this review.
`SHA256.json` lists the complete review package except itself.

Definition source: NIST FIPS 180-4, Sections 4.1.2 and 6.2.2,
<https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>.
