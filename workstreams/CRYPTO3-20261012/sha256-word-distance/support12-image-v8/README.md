# Support-12 fixed-residue joint-image obstruction

For the exact numerical difference `D=0x00010000`, the selected twin core
has no solution even after the `sigma1` gap equation is weakened modulo
`2^31`.  Reversing both pairs also excludes `D=0xffff0000`.

The standard-library replay covers all 256 input-XOR class pairs.  Full
`sigma0` equality leaves 414 affine branches; the `sigma1` gap modulo
`2^30` leaves 20; output bit 30 eliminates all of them by an odd-carry
parity contradiction.  A real four-word boundary fixture proves that the
last bit is essential.

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-image-v8/check.py --negative
```

Scope is deliberately narrow: this is a complete fixed-residue selected-
core obstruction, not an exclusion of every exact-valuation-16 difference,
not a full support proof, and not a SHA-256 message-pair result.  See
`PROOF.md` and `CERTIFICATE.json`.

