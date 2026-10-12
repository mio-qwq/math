# Independent reconstruction of support S0 active-pair interfaces

This review concerns 13 independently supplied, genuinely unequal 32-bit word pairs at S0 = {2,9,10,16,23,24,30,37,38,44,51,52,58}. Inactive positions contribute d = F = G = 0. A pair X=(x,x') contributes d(X)=x'-x, F(X)=sigma0(x')-sigma0(x), and G(X)=sigma1(x')-sigma1(x), all in Z/(2^32). The two small sigmas are the original FIPS 180-4 maps, bit 0 least significant.

The finite mathematical purpose is to reconstruct all 48 necessary difference equations directly from d_t = G_(t-2) + d_(t-7) + F_(t-15) + d_(t-16), for 16 <= t < 64, and decide whether the proposed module description preserves exactly these equations and every unequal-pair boundary. The fixed locations are Q_j = 2+14j (j=0..4), P_j=9+14j (j=0..3), and R_j=10+14j (j=0..3).

Before reading any author active-pair-construction file, the review will freeze the complete raw equation list and a direct symbolic derivation of its chain interfaces. It will then compare the author's claimed equivalence. No base schedule is imposed in this independent-pair relaxation, so a successful equivalence does not establish a genuine SHA-256 input pair. No SAT or additional search is part of this review.

Definition source: NIST FIPS 180-4 sections 4.1.2 and 6.2.2, https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf .
