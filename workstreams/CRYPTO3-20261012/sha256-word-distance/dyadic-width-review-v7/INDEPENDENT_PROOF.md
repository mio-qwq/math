# Independently reconstructed dyadic width reduction

This argument and its checker were written before inspecting the author's
`dyadic-width-v7/` files. The statements concern the actual three-pair
necessary core, not a complete schedule or a feasible-core witness.

Let N=2^32, f=sigma0, g=sigma1, and suppose three actual ordered word
pairs X,Y,R have nonzero modular input differences D,D,-D and satisfy
the core's two sigma1 gaps GY-GX=2D and GY-GR=D. Their sigma0 equality
may be retained but is not needed for this necessary width restriction.
Fix k=v2(D). For every k from 10 through18 the conclusion is

```
D = +/-q*2^k + h*2^(k+14) modulo2^32,
q odd, 1 <= q <= 2^(22-k)-1,
0 <= h <= 2^(18-k)-1.
```

Put M=2^(k+14), J=M/2=2^(k+13), and L=2^22. Since k<=18, M divides
N. The output row of g at j is {(j+17) mod32,(j+19) mod32}, with
input j+10 also present if j<22. For j=22,...,k+12 both inputs j-15
and j-13 lie below k, so these output bits agree in each pair. Row
k+13 is exactly {k-2,k}; the SHR10 term is absent. The input bit k
flips because D/2^k is odd, and it flips for -D as well. Input k-2
is fixed. Thus output bit k+13 flips in each of the three pairs.
Output bits above k+13 are discarded only by passing modulo M.

For each actual pair let q_i be the ordinary difference of the low22
sigma1 output residues. Then |q_i|<L. Its bits22,...,k+12 cancel
in ordinary subtraction, and the next output bit contributes +J or
-J, the same residue J modulo M. Hence

```
G_i = J + q_i modulo M,  i in {X,Y,R}.
```

The input wrap, output wrap and signs of the top-bit changes are all
retained. There is no ordinary ordering assumption about complete
32-bit sigma outputs.

Set A=q_Y-q_R and B=q_Y-q_X. Both shared J terms cancel. Therefore
A=D modulo M and B=2D modulo M, with |A|,|B|<2L. Importantly,

```
B-2A = 2q_R-q_Y-q_X,
|B-2A| < 4L = 2^24.
```

This uses their shared q_Y. The cruder bound |B|+2|A|<6L is
insufficient at k=10 and must not be used to claim that endpoint.
For k>=10, M>=2^24. Since B-2A is a multiple of M in the displayed
strict interval, it must be0. Thus B=2A as ordinary integers, and
|A|<L follows from |B|<2L.

Because A=D modulo M and M is a multiple of2^(k+1), A has exact
valuation k and is nonzero. Consequently A=+/-q*2^k with positive
odd q strictly below2^(22-k). Lifting this congruence from M to N
gives every and only the h residues0,...,N/M-1. This proves the
stated full lift coverage with N/M=2^(18-k); no wrap or high-word
class is dropped.

Reversing every ordered pair negates all actual input and output
derivatives and preserves the core. For a negative representative
D=-q*2^k+hM, reversal gives -D=q*2^k+(-h mod N/M)*M. Thus positive
q representatives suffice under that proved reversal symmetry.

## Exact boundary at k=9

The common-J row argument still works at k=9: row22 is {7,9},
there are no intermediate fixed rows, and M=2^23=2L. But the joint
bound |B-2A|<4L now allows the nonzero multiples +M and -M.
For instance the ordinary integers

```
q_X=0, q_Y=-1024, q_R=2^22-512
```

all lie strictly between -L and L. They give A=-L-512, B=-1024,
B-2A=M, D=A mod M=L-512, with exact v2(D)=9. Both gap congruences
hold modulo M, but B=2A fails and |A| exceeds L. This is only an
integer-representative counterexample to that inference; it is not
asserted to come from real word pairs or satisfy the sigma0 core.

The same final q/h formula at k=9 is nevertheless not a false
statement: signed odd q up to8191 and h from0 to511 cover the entire
v2(D)=9 residue stratum. Its 2^22 residues equal the number of all
32-bit residues with that valuation. At k=9 the formula is therefore
vacuous arithmetic and gives no width reduction. The nontrivial
joint cancellation proof applies exactly to k=10,...,18 here.

At k=8 the parity row would be21, with inputs6,8,31. The changing
input31 can cancel the change in bit8, so there is no shared top
change forced by D. Actual pairs (0,256) and (2^32-256,0), both
with difference256, exhibit different changes in output bit21.
They are boundary examples only, not complete-core witnesses.

For k=10,...,18 the retained fraction of each original exact-valuation
stratum is2^(9-k). Distinct signed q/h representatives do not collide:
their signed q differences have magnitude less than2^14, so equality
modulo M forces identical signed q, then identical h modulo N/M.
These are case-budget counts, not probabilities or feasibility claims.
