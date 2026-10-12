# Independent reconstruction of the local four-word witness

This calculation concerns four arbitrary 32-bit words, not a 64-word SHA-256 schedule. Let R = Z/(2^32), bit 0 be the least significant bit, f(x) = ROTR7(x) XOR ROTR18(x) XOR SHR3(x), and g(x) = ROTR17(x) XOR ROTR19(x) XOR SHR10(x).

The supplied words are p = 0x0019f0ed, p' = 0x973448ed, q = 0xdff7f75f, and q' = 0x77124f5f. The mathematical purpose of the finite calculation is to check directly whether the same nonzero additive difference D occurs in both pairs, with g(q') - g(q) = -D and f(p') - f(p) = -(f(q') - f(q)), and whether the residue D has 2-adic valuation exactly 11. A successful result would show that the previously proved local bound v2(D) <= 11 cannot be improved under these four-word conditions alone. It would give neither a schedule extension nor a word-distance equality example.

The implementation will reconstruct each output bit from its three source bits. Rotations use source indices (i+r) mod 32; the logical shift contributes source i+s only when i+s < 32. All differences and sums are reduced modulo 2^32, so an overflowing addition is permitted. The four input words remain unrestricted except for the supplied values. No SAT solver, author checker, certificate table, or author proof is used for this reconstruction.

The initial numerical result and code are to be frozen before comparison with the author's sharpness package. Negative controls will alter a word, a sigma parameter, and a claimed difference. The scope of this receipt is direct finite witness verification.

Definition source: NIST FIPS 180-4, section 4.1.2, equations (4.6) and (4.7), https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf .
