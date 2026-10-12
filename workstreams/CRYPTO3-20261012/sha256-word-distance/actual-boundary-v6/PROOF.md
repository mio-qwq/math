# Actual-word restrictions at the unresolved support-12 inverse boundary

**New exact local candidate, independently written direct-bit checker;
independent-agent acceptance pending.** This stage provides a necessary
signed-power exclusion and a four-pair real-word fixture delimiting one
weaker nonlinear mechanism. The real `12 -> 6` inverse shift, full
distance-13 attainability, and a global lower bound 14 remain unresolved.

The original support bytes are pinned to SHA256
`02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf`.
The operator is the actual [FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
sigma0 `f=ROTR7 XOR ROTR18 XOR SHR3` and sigma1
`g=ROTR17 XOR ROTR19 XOR SHR10`, with additions in R=Z/(2^32).
No frozen earlier result is modified.

## 1. Every original difference recurrence retained

For two actual expansions write

    d_i=W'_i-W_i,
    F_i=f(W'_i)-f(W_i),
    G_i=g(W'_i)-g(W_i).

For all t=16,...,63 subtracting the original schedules gives

    E_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)=0.                 (1)

Support 12 is exactly

    {10,11,13,15,18,20,26,28,29,34,42,43,57}.

Outside it all three interfaces vanish. The following twenty-five
nonzero rows exhaust the original forty-eight rows; the other twenty-three
reduce identically to zero. The direct checker independently substitutes
the original lag list and compares the entire row table.

| t | Necessary equation |
|---:|---|
| 17 | G15=-d10 |
| 18 | d18=d11 |
| 20 | d20=G18+d13 |
| 22 | G20=-d15 |
| 25 | F10=-d18 |
| 26 | d26=F11+d10 |
| 27 | d20=-d11 |
| 28 | d28=G26+F13 |
| 29 | d29=d13 |
| 30 | F15=-G28 |
| 31 | G29=-d15 |
| 33 | F18=-d26 |
| 34 | d34=d18 |
| 35 | F20=-d28 |
| 36 | G34=-d29-d20 |
| 41 | F26=-d34 |
| 42 | d42=d26 |
| 43 | d43=F28 |
| 44 | F29=-G42-d28 |
| 45 | G43=-d29 |
| 49 | F34=-d42 |
| 50 | d43=-d34 |
| 57 | d57=F42 |
| 58 | F43=-d42 |
| 59 | G57=-d43 |

In particular set

    a=d11=d18=d34,   b=d26=d42,   c=d13=d29,
    e=d28,           k=d15,       z=d57.

Every one of these differences is nonzero. Among the necessary actual
word-pair constraints are

    F26=-a, F18=F34=F43=-b,
    G18=-a-c, G34=a-c, G43=-c, G57=a,
    F13+F29+G26+G42=0,  e=F13+G26,
    G29=-k.                                                    (2)

The inverse recurrence at old t=15 gives

    d_-1=d15-G13=-(G13+G29).                                    (3)

Thus completing a common prefix requires opposed g derivatives on the
two actual pairs at indices 13 and 29, whose additive input differences
are equal to c. The additive row module alone does not force this, as
the separate frozen v5 note proves. Here the original word-pair
semantics is explicitly retained in the two local statements below.

## 2. A new actual sigma0 negative two-cycle restriction

**Local theorem.** Let (p,p') and (q,q') be actual 32-bit word pairs.
Put b=p'-p and a=q'-q. Suppose

    f(p')-f(p)=-a,    f(q')-f(q)=-b.

Then b cannot equal +2^k or -2^k for any 22<=k<=31. By interchanging
the pairs, the same statement holds for a. This is a restriction on a
specified parameter stratum; no entire support is excluded.

**Actual schedule consequence.** Apply the theorem to p=W26,p'=W'26
and q=W18,q'=W'18, using (2). Therefore, for an actual support-12 pair,

    d26=d42 is not +/-2^k for 22<=k<=31.                       (4)

The earlier bound `v2(a)<=20` is stronger on high valuations of a,
whereas (4) restricts the different parameter b. No general valuation
ceiling on b is asserted here.

### 2.1. Reduction to two exact interval-mask valuations

For a nonzero modular difference, its 2-adic valuation equals the least
set bit of the input XOR mask. This follows because below the first
differing bit the unsigned words agree, and at that bit their difference
is odd after division by its weight.

If two words differ additively by +/-2^k, their XOR mask is a consecutive
run of bits k,...,u for some k<=u<=31. Carry/borrow wraparound at the
most significant bit is included by u=31. Denote that mask I(k,u).

Assume b is a signed 2^k. For the pair p,p', its input XOR mask is
I(k,u). XOR-linearity of f makes its output XOR mask f(I(k,u)). Since
its additive output difference is -a,

    v2(a)=v2(f(I(k,u))).                                       (5)

For the pair q,q', its additive f-output difference is -b, so its output
XOR mask is I(k,v). The original f is XOR-linear and invertible; the
thirty-two inverse columns in the finite certificate each satisfy
f(column_j)=2^j, proving its inverse on every word by binary linearity.
Consequently the input XOR mask is f^-1(I(k,v)), giving

    v2(a)=v2(f^-1(I(k,v))).                                    (6)

Both (5) and (6) are necessary for actual pairs. Nothing assumes the
two input masks or derivative signs can be independently realized.

### 2.2. Complete obstruction for k>=22

For every k>=22 and u>=k, the least output bit of f(I(k,u)) is exactly
k-18. It comes from ROTR18 of input bit k. All ROTR7 contributions have
indices at least k-7, and all SHR3 contributions at least k-3; there is
no rotation wraparound for these high input positions. Hence no term can
cancel bit k-18, and no smaller bit is present.

The inverse-mask side has the following strict bounds, obtained by direct
XOR sums of the original verified inverse columns for every v=k,...,31.
There are only fifty-five inverse masks in these ten high strata; all
their exact words appear in `CHECK_RUN.json`.

| k | v2(f(I(k,u))) | Maximum v2(f^-1(I(k,v))) |
|---:|---:|---:|
| 22 | 4 | 3 |
| 23 | 5 | 2 |
| 24 | 6 | 1 |
| 25 | 7 | 2 |
| 26 | 8 | 3 |
| 27 | 9 | 4 |
| 28 | 10 | 2 |
| 29 | 11 | 3 |
| 30 | 12 | 0 |
| 31 | 13 | 1 |

Every row contradicts (5)-(6). This proves the local theorem, including
both signs and all wraparound endpoints.

The pre-budgeted experiment checked the necessary endpoint equality for
all 32 values of k, for exactly 11,440 comparisons. It retained 3,675
endpoint triples below k=22. Those triples are necessary-mask candidates
only; the experiment does not prove their actual-pair feasibility and
does not continue their search. The empty ten high strata have the
complete proof above and an exact independently reconstructed bit check.

## 3. A real-word fixture for the conservation submechanism

The equality in (2) involving four sigma derivatives does not, even with
actual word pairs and matching input differences, force (3) to vanish.
Here is an explicit fixture. It supplies four real pairs, not all thirteen
active pairs and not two initial message blocks.

| Index | W | W' | d | F | G |
|---:|---|---|---|---|---|
| 13 | 00000000 | 290afdcd | 290afdcd | 20000000 | 2155731b |
| 29 | d6f50232 | ffffffff | 290afdcd | e0000000 | ded5731b |
| 26 | 00000000 | 8ddd55ad | 8ddd55ad | 1fcb7369 | 00400000 |
| 42 | 7222aa52 | ffffffff | 8ddd55ad | 1fcb7369 | ffc00000 |

All entries are hexadecimal unsigned words. Direct original bit equations
verify

    d13=d29=c!=0, d26=d42=b!=0,
    F13+F29=0, G26+G42=0,
    F13+F29+G26+G42=0,
    -(G13+G29)=ffd519ca!=0.

Define the local auxiliary values

    a=-F26=e0348c97,   e=F13+G26=20400000,
    k=-G29=212a8ce5,   z=F42=1fcb7369.

These are all nonzero. In particular e is not silently set to zero and
the fixture's b is an odd, nonsigned-power residue, so the fixture does
not violate (4).

### 3.1. Analytic complement-and-reverse construction

Let U=ffffffff. XOR-linearity gives

    f(U)=1fffffff,   g(U)=003fffff.

For an actual pair (0,x), the complement-and-reverse pair (U XOR x,U)
has the same additive input difference x. Its derivative for an XOR-linear
operator L is L(U)-(L(U) XOR L(x)).

Take x=f^-1(20000000)=290afdcd. The f image lies above the set bits
of f(U), so the second f derivative is -20000000, opposite the first.
Write g(x)=H+ell where ell=g(x) AND 003fffff and H contains its higher
bits. The complement-and-reverse g derivative is ell-H, whereas the
first is H+ell. Their sum is 2ell. Here ell=0015731b, so the sum is
002ae636!=0.

For the b pairs choose y=8ddd55ad, whose original g image is 00400000.
This lies above the set bits of g(U), so complement-and-reverse produces
opposite g derivatives. The original f image of y is 1fcb7369, entirely
inside f(U); therefore both f derivatives equal 1fcb7369. These exact
constants complete the table without a solver or random search.

### 3.2. Scope of the fixture and the remaining gap

The fixture establishes failure of the single conservation submechanism
to force a common inverse prefix. It is stronger than a freely assigned
d/F/G interface at these four indices: every displayed triple is computed
from two actual words. It remains weaker than all twenty-five equations
with all thirteen actual pairs. In particular the required pairs at
18,34,43 must also obey the same f derivative -b, their specified +/-a
input differences, and the coupled g relations in (2). None is supplied
here. Nor are pairs at 10,11,15,20,28,57 or the original base recurrences
realized. The checker explicitly rejects promoting this four-pair fixture
to a complete support model.

No incompatibility of those missing actual pairs is asserted. The actual
reverse implication may still follow from these missing constraints and
base-message equations; this stage does not decide it.

## 4. Finite budget, direct verification and freeze scope

`EXPERIMENT_PLAN.md` was created before executing the finite experiment
and has not been changed. It fixes the exact 11,440 comparisons and stops
after the cover. No SAT/SMT query, previous timeout/unknown model replay,
seed sweep, extended timeout, previous row-module elimination or safe
shift enumeration was run.

Read-only deterministic commands from the repository root:

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/actual-boundary-v6/finite_mask_experiment.py
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/actual-boundary-v6/check_actual_boundary.py
```

The generator prints `MASK_EXPERIMENT.json`; the checker prints the
corresponding `CHECK_RUN.json`. Neither writes files without `--output`.
The generator uses rotate expressions, whereas the checker independently
computes every output bit and imports no generator code. It verifies the
entire original row substitution, all inverse columns, endpoint cover,
the ten high-power contradictions, all eight actual words and their
derivatives, plus six damaged or scope-negative controls. Execution
records and the SHA256 manifest bind this exact version.

Specific historical originality is unconfirmed. The result is a complete
written local proof with exact finite checking, pending independent-agent
mathematical acceptance. It is neither a full distance theorem nor a
research-paper publication, formal proof-assistant theorem, attack on
SHA-256, signed integration commit or release.
