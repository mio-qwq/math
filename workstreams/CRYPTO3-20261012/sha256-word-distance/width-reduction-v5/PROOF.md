# A half-word cancellation in the support-12 divisibility reduction

**Complete written lemma; independent review pending.** This is a new
necessary-condition reduction, not a whole-support exclusion or a message
pair. All arithmetic in word differences is modulo N=2^32; H=2^31.

Let three arbitrary actual ordered pairs X,Y,R have input differences
D,D,-D, with D nonzero, and let G denote their actual sigma1 derivatives.
Suppose

    G(Y)-G(X)=2D,  G(Y)-G(R)=D.

Then, if 2^18 divides D, its residue is one of

    D = +/-q*2^18 (mod N),  1 <= q <= 15.                 (1)

The previously used width argument directly worked at 2^19 divisibility.
At 2^18, the top output bit can change. It nevertheless contributes the
same half-word to all three modular derivatives, which cancels in both
required gaps. No inequality of ordinary full sigma outputs is assumed.

## 1. The exact high output bits

The original map is

    g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).

For every output bit j from 22 through 30, its only input indices are
j-15 and j-13, both below 18. Thus those output bits agree in any pair
whose input difference is divisible by 2^18. At j=31 the only inputs
are 16 and 18. Its change is exactly the change in input bit 18, because
bit 16 agrees.

Put e=(D/2^18) mod 2. For an input difference D or -D, the lower 18
bits agree and the XOR change in bit 18 is e: adding an even quotient
leaves it unchanged, and adding an odd quotient changes it. The negative
quotient has the same parity. Therefore the bit-31 sigma1 contribution
to its ordinary additive derivative is zero if e=0, or +/-H if e=1.
In the latter case either sign is H modulo N.

For each of the three pairs let q_X,q_Y,q_R be the ordinary integer
difference between the **low 22 bits** of its sigma1 outputs. The common
bits 22..30 cancel in ordinary subtraction, so

    G(X)=eH+q_X, G(Y)=eH+q_Y, G(R)=eH+q_R (mod N),
    |q_X|, |q_Y|, |q_R| < 2^22.                           (2)

This step retains every modular wrap: the top-bit sign is discarded only
modulo N, where its two possible signs are equal.

## 2. Integer representatives of the two gaps

Set A=q_Y-q_R and B=q_Y-q_X. The shared eH contribution cancels, giving

    A=D (mod N), B=2D (mod N), |A|,|B|<2^23.

The integer B-2A is a multiple of N with absolute value below
3*2^23<N, so it is zero. Hence B=2A, and |A|<2^22. The congruence
A=D and N's divisibility show that 2^18 divides A. Also A is nonzero
since D is a nonzero residue. The possible signed integers A are
precisely +/-q*2^18 for 1<=q<=15, proving (1).

## 3. Scope and verification

The hypothesis uses only three actual word pairs, their input differences
and the two actual sigma1 gaps. Its support application still needs the
original recurrence bridges in `support12-v4/`; it does not follow from a
support mask alone. Adding the sigma0 equalities gives a further finite
case problem, which (1) does not solve.

`check.py` reconstructs the original output rows, checks the stated high
bit dependency identities and the integer range constants, and rejects
four damaged bit-boundary controls. XOR linearity makes the row identities
universal. The proof above supplies the modular and integer arguments;
finite input samples are not substituted for their quantifiers.

The definition is NIST FIPS 180-4, Section 4.1.2. Bit-output locality and
integer representative arguments are elementary. No historical priority,
Lean compilation, SHA collision, new global distance, or human review is
claimed.
