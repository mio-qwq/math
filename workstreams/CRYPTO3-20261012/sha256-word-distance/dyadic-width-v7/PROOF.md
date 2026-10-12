# A shared-term width screen for the actual irregular core

**Complete written lemma; independent acceptance is separate.** This
screen concerns the actual three-pair necessary core of supports
12,6,7,13. It excludes no whole support and changes neither the global
distance bound 13 nor the need for genuine base completion.

Let N=2^32. For actual ordered word pairs X,Y,R, write d for the input
difference and G for the difference of

    g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).

Assume, modulo N,

    d(X)=d(Y)=D!=0, d(R)=-D,
    G(Y)-G(X)=2D, G(Y)-G(R)=D.                         (1)

The usual common sigma0 derivative is not needed for this lemma.
Let k=v2(D), and suppose 10<=k<=18. Then necessarily

    D = epsilon*q*2^k + h*2^(k+14) (mod N),            (2)
    epsilon in {-1,+1},
    q odd, 1<=q<=2^(22-k)-1,
    0<=h<2^(18-k).

Global reversal of all three ordered pairs preserves (1). Thus every
negative representative reduces to a positive one, with the lift h
changed to (-h) modulo 2^(18-k). This lift permutation matters: h is
not generally preserved by reversal.

## Proof from original bit rows

Number bits from zero. For each output bit j>=22, the shift term is
absent and the two rotation arguments are input bits j-15 and j-13.
The pairs in (1) agree in their low k input bits. Adding either D or
-D flips input bit k, since the quotient by 2^k is odd.

Hence g output bits 22 through k+12 agree within every pair, while
output bit k+13, whose row is {k-2,k}, flips. Put

    M=2^(k+14), C=2^(k+13), L=2^22-1.

The flipping output bit contributes either +C or -C to the ordinary
integer output difference; both equal C modulo M. All output bits
above it contribute multiples of M. The ordinary difference q_i of
the low 22 output bits lies in [-L,L]. Thus

    G_i = C+q_i (mod M), q_i in [-L,L], i=X,Y,R.      (3)

For k=18 there are no higher output bits and M=N; the same argument
still applies. Equation (3) is a universal bit identity for these
actual pairs, not an assumption that the q_i are independent.

Set A=q_Y-q_R and B=q_Y-q_X. Reducing (1) modulo M gives
A=D and B=2D modulo M, so B-2A is an integer multiple of M. The
shared occurrence of q_Y gives the sharper bound

    B-2A = -q_Y-q_X+2q_R,
    |B-2A| <= 4L = 2^24-4 < M.                       (4)

The final strict inequality holds already at k=10. Consequently
B=2A as integers. Also |B|<=2L, whence |A|<=L. The residue A has
valuation k because A=D modulo M and k<log2(M). In particular A
is nonzero. Therefore A=epsilon*q*2^k for the odd q in (2).
As M divides N, all possible lifts are exactly h=0,...,N/M-1,
which is the stated range. This proves (2).

The two signed intervals in a single M-period are disjoint: the
positive interval is contained in (0,2^22) and the negative one in
(M-2^22,M), with M>=2^24. Their q-values and M-period lifts are
unique. Reversing all pairs negates d and G, so changes epsilon to
-epsilon and h to (-h) mod (N/M), proving the representative reduction.

## Exact domains, without new mask enumeration

There are 2^(21-k) positive odd q values and 2^(18-k) lifts. The table
counts positive representatives after reversal; both signs must be
included when listing the full residue domain.

| k | Maximum odd q | Lifts | Positive representatives |
|---:|---:|---:|---:|
| 10 | 4095 | 256 | 524288 |
| 11 | 2047 | 128 | 131072 |
| 12 | 1023 | 64 | 32768 |
| 13 | 511 | 32 | 8192 |
| 14 | 255 | 16 | 2048 |
| 15 | 127 | 8 | 512 |
| 16 | 63 | 4 | 128 |
| 17 | 31 | 2 | 32 |
| 18 | 15 | 1 | 8 |

These are necessary screens, not claims of feasibility. The already
accepted complete finite exclusions at k>=17 are separate proof
objects; this note creates no exclusion certificate for k<=16.

## Exact limit of this width argument

At k=9, M=2^23, and (4) does not force its multiple to vanish.
For example, the following free integers lie within [-L,L]:

    q_X=-4194303, q_Y=-4193279, q_R=513.

They give A=-4193792, B=1024, and B-2A=M. Taking
D=A mod M=4194816 gives valuation 9 and both reduced gap congruences.
Thus the integer-width premises alone do not force B=2A at k=9.
In fact the formula (2) extended to k=9 would cover the entire exact
valuation-9 domain: every such residue modulo M has a signed odd
multiple representative of magnitude below M/2=2^22. It is then a
vacuous screen, not a false statement. These free integers are not
supplied by actual word pairs and are not a counterexample to an
actual SHA-256 theorem. At k=8, output bit k+13=21 also has the
SHR10 argument input31, so the common-bit argument itself fails.

The former separate estimate |B|+2|A| used 6L and supported the
threshold k>=11. The shared-term bound 4L is the precise improvement
made here. No SMT/SAT output, stochastic model, free-interface
countermodel or finite sample is a premise of the universal proof.

## Reproduction and status

`check.py` rebuilds g rows from original bit definitions, checks every
unchanged and flipping row for all nine k, verifies the strict integer
bound, the complete signed lift formula and reversal permutation,
and rejects four damaged certificates. Actual endpoint samples check
the decomposition identity and both pair orientations; they are not
core witnesses and do not replace the quantified row argument.
Only the Python standard library is needed. The theorem remains an
author result until a separate exact-byte independent receipt exists.
No message pair, global bound 14, Lean result, historical priority,
paper, DOI, Release or main integration is claimed.
