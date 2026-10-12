# Independent review: common top-bit cancellation at divisibility 2^18

**Decision: accepted.** The parent candidate `../width-reduction-v5/PROOF.md`
is a complete written necessary-condition lemma for actual word pairs.
This review is independent mathematical examination and independently
written definition-based code after reading the author's proof. The
author's checker was neither read, imported nor executed by the reviewer.
This is not blind discovery, external human peer review or Lean.

Let N=2^32, H=2^31, K=2^18 and L=2^22. Three ordered pairs X,Y,R
have nonzero modular input differences D,D,-D. Their actual sigma1
derivatives satisfy G(Y)-G(X)=2D and G(Y)-G(R)=D. The conclusion is
that K|D implies D=+/-qK modulo N, for 1<=q<=15.

For the actual FIPS sigma1 g=ROTR17 xor ROTR19 xor SHR10, output bit j
uses input bits (j+17) mod32 and (j+19) mod32, and also j+10 if that
index is below32. Independent reconstruction from all 32 basis inputs
verifies every row. For j=22,...,30 the rows are exactly {j-15,j-13},
strictly below18; row31 is {16,18}. Output bit21 is a genuine boundary:
its row includes input31 and cannot be included among fixed output bits.

If a pair's modular input difference is a multiple of K, its lower18
bits agree. Write the word as its common lower residue plus K times a
14-bit quotient. The quotient changes by D/K modulo2^14. Its lowest
bit, input bit18, toggles precisely when e=(D/K) mod2 is1. Negating
D preserves that parity. Thus all three pairs have fixed output bits
22..30 and identical XOR change e in output bit31, since input16 is
fixed. This argument includes input wrap and either pair orientation.

For each pair take q to be the ordinary difference of the low22-bit
output residues. Then |q|<L. In ordinary subtraction the common bits
22..30 cancel; the top bit contributes0 if e=0 or either +H or -H if
e=1. Both signs represent H modulo N. Hence, without dropping modular
wrap or asserting anything about ordinary full output ordering,

```
G(X)=eH+q_X, G(Y)=eH+q_Y, G(R)=eH+q_R modulo N.
```

Define the ordinary integers A=q_Y-q_R and B=q_Y-q_X. The common
eH cancels in the two required gaps, so A=D modulo N and B=2D
modulo N, with |A|,|B|<2L=2^23. Therefore B-2A is a multiple of N
whose absolute value is below3*2^23<N. The only possible multiple is0.
This establishes B=2A as an integer equality, not just a congruence.
It follows from the strict bound on B that |A|<L. Since K divides both
D and N, K divides A. A cannot be0 because D is a nonzero residue.
The only possibilities are exactly the thirty signed integers
+/-K,...,+/-15K; +/-16K violates the strict bound. This proves the
candidate for arbitrary actual pairs.

The independently written read-only checker verifies all output rows,
the high-row boundaries, the top parity row and the integer constants.
It constructs actual three-pair tuples with differences D,D,-D, with
positive and negative orientations, odd and even D/K, modular wrap,
and values both within and outside the resulting necessary range.
It directly checks the three decompositions and both H cancellations.
Reversing every pair gives differences -D,-D,D, preserves e, negates
each ordinary q and reverses both integer gaps. These are implementation
checks of actual-pair identities; the samples are not a quantified proof
or a claim that any sample satisfies the two additional gap hypotheses.
The number of full-hypothesis hits is explicitly reported in the result.

Four malformed controls are rejected: treating output21 as fixed,
treating output31 as fixed, moving its dependency from input18 to17,
and accepting quotient16 despite the strict integer range.

Acceptance concerns this necessary condition only. Applying it to a
specific support still requires its original recurrence bridges. It
does not establish joint sigma0 feasibility, full schedule interpolation,
distance13 attainment, distance at least14, a cryptanalytic attack,
historical originality or any formal proof-assistant compilation.
