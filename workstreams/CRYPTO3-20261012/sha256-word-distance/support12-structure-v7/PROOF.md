# Exact joint-image structure and sigma0 reciprocal restrictions

**Complete written analytic results with small author dependency checks;
independent-agent acceptance is separate.** No complete support is
excluded, no new bound on the valuation of D beyond the accepted v6
ceiling16 is claimed, and the global distance lower bound remains13.

All word arithmetic is modulo N=2^32. Let

    f=ROTR7 xor ROTR18 xor SHR3,
    g=ROTR17 xor ROTR19 xor SHR10.

Both maps are binary linear permutations. The checker verifies each
claim by supplying32 inverse basis columns and applying the original
output-bit rows to each column. Every standard basis vector has a
preimage; linearity and finite equal dimensions give bijectivity.

## 1. An exact criterion with two external target parameters

For a fixed nonzero D, define actual joint derivatives

    F_D(x)=f(x+D)-f(x), G_D(x)=g(x+D)-g(x),
    I_D={(F_D(x),G_D(x)): x ranges over all32bit words}.

The actual three-pair core is

    d(X)=d(Y)=D, d(R)=-D,
    F(X)=F(Y)=F(R),
    G(Y)-G(X)=2D, G(Y)-G(R)=D.                    (1)

**Exact joint-image criterion.** Core (1) is feasible if and only if
there are scalars A,T such that all three points

    (A,T-D), (A,T+D), (-A,-T)                         (2)

belong to I_D.

Proof. Given (1), define **A=F(X) and T=G(X)+D**, without division by2.
Then G(Y)=T+D and G(R)=T. The pairs X,Y supply the first two points
of (2). Reverse R to obtain Z with d(Z)=D,F(Z)=-A,G(Z)=-T; it
supplies the third point. Conversely choose actual preimages x,y,z
of the three points, take X=(x,x+D),Y=(y,y+D), and R=(z+D,z).
All equations (1) then follow by direct subtraction. The two constructions
are inverse when the preimages are retained. There is no average or
division by2 in the even cyclic ring.

For an equivalent fibre formulation define

    B_(D,A)={G_D(x): F_D(x)=A}.

Then (1) is feasible exactly when there exist A,c satisfying

    c in B_(D,A), c+2D in B_(D,A),
    -c-D in B_(D,-A).                                (3)

Here c=G(X), not an independently assigned derivative. The twin core
asks only for the first two memberships. The third pair asks for a
specified reflected value in the *different* sigma0 fibre B_(D,-A).
It is not an automatic completion of a twin solution.

This reduces the **external interface** at fixed D to two targets A,T
(or A,c). It does not reduce the hidden preimage obligations or claim a
computational speedup: each image has up to2^32 elements, and its exact
membership still evaluates both sigmas on the same actual word pair.
The original three base-word choices remain in those image preimages.
No distribution, independence or random-image assumption is introduced.

Bijectivity implies automatically A!=0 and T notin{0,D,-D}, since the
three actual sigma1 derivatives T-D,T+D,T must all be nonzero.

## 2. The fourth original pair supplies a reciprocal derivative edge

For support12, put D=d18=d34 and A=F18=F34=F43. The original
difference equations at t33 and t41, together with t34, give

    d26=-A, F26=-D.                                   (4)

In terms of original row E_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16),
`-E33=d26+F18` and `-E41-E34=F26+d18`. The direct checker
reconstructs these signed combinations for support12 and their shifts
+1,+3,+2 for supports6,7,13. No boundary row is omitted.

For actual pairs X,P, condition (4) is the selected two-pair coupling

    d(X)=D,F(X)=A,d(P)=-A,F(P)=-D.                     (5)

Reverse P to Q. Then d(Q)=A,F(Q)=D. In the directed derivative graph
whose nonzero vertices are additive differences and whose edge U->V
means `V=F_U(x)` for some actual x, (5) means the reciprocal edges
D->A and A->D. The negative signs in (5) cannot be replaced by a
single negative edge; both disappear when reversing the actual pair.

Define R_A={F_A(u):u ranges over all32bit words}. The selected four-pair
system consisting of (1) and (4) is therefore exactly equivalent to
the three memberships (2) together with

    D in R_A.                                         (6)

Necessity follows from Q; sufficiency chooses a preimage Q of (6) and
sets P to its reverse. This is equivalence for these **selected local
equations**, not for all48 original support equations or genuine base
completion. The sigma1 derivative of P and every omitted original row
remain obligations for a full support assignment.

## 3. An exact small valuation-signature filter

For unequal words u,v, let alpha=u xor v. The lowest set bit of alpha
is also the2-adic valuation of v-u: lower bits agree and at that bit
the difference is +/-2^k, which is2^k modulo2^(k+1). Thus

    v2(v-u)=v2(alpha),
    v2(f(v)-f(u))=v2(f(alpha)).                         (7)

The second identity uses the binary linearity of f and the first
identity applied to its unequal image words.

Let M_(a,b) mean that a nonzero mask alpha exists with
v2(alpha)=a,v2(f(alpha))=b. It is equivalent to exactly the following
binary equations on32 input bits:

    alpha_j=0 (j<a), alpha_a=1,
    f(alpha)_j=0 (j<b), f(alpha)_b=1.                  (8)

`CERTIFICATE.json` covers all1024 pairs (a,b). Each of the417 possible
single-pair signatures has an actual mask witness checked by the bit
definitions. Each of the607 impossible signatures has an explicit XOR
of original rows in (8) yielding0=1. The final checker does **no Gaussian
elimination** and imports no generator: it only evaluates witnesses
and directly XORs the specified original rows. Positive signatures are
actual pairs, for example (0,alpha), so this is an exact one-pair
classification, not a sufficient-mask ansatz.

Coupling (5) necessarily has signatures (a,b) and (b,a), where
a=v2(D),b=v2(A). Therefore both M_(a,b) and M_(b,a) are true.
The checked transpose filter has309 entries. It yields the global
necessary restrictions

    a<=23, b<=23, a+b<=30,                             (9)
    b>=18 implies a=b-18<=5.                          (10)

By symmetry the analogous statement holds when a>=18. A particularly
useful boundary is a=16: the exact necessary b list is

    b in {0,1,2,3,4,5,6,7,8,9,10,12}.                 (11)

These are **necessary** transposed valuation signatures. The309 entries
are not claimed to be all feasible exact numerical reciprocal pairs:
two separate mask witnesses do not establish the same actual numerical
D,A in both pairs. Equation (6) retains that stronger compatibility.
The table is a32-row binary dependency check, not an enumeration of
messages or an extension of the valuation16 SMT case list.

For each of supports12,6,7,13, A=-d_(26+shift)=-d_(42+shift).
Thus these two other nonzero word differences have valuation<=23, and
their valuation together with that of D satisfies (9)-(11).

## 4. A short half-word obstruction without any table traversal

Let H=2^31. The original bit equations give

    f(H)=11002000 hex, v2(f(H))=13,
    f^(-1)(H)=94857ee6 hex, v2(f^(-1)(H))=1.          (12)

The checker evaluates both identities directly; f's permutation
property makes the inverse identity unique.

If D=H in (5), X has input XOR mask H, so (7) forces v2(A)=13.
But F(P)=-D=H gives output XOR mask H and hence input XOR mask
f^(-1)(H). Since d(P)=-A, (7) also forces v2(A)=1: contradiction.

If A=H, apply the same reasoning with X and reversed P interchanged.
It forces simultaneously v2(D)=1 and13. Consequently neither D nor
A can equal H in any reciprocal pair coupling (5). This global
analytic obstruction does not need the older three-pair high-valuation
certificate, a solver, or enumeration of32bit word values.

## 5. Shared endpoints are excluded by the fourth-pair coupling

Consider R versus either X or Y in (1), writing X=(x,x+D) and
R=(r,r-D) with common f derivative A.

If r=x, equality of F gives f(x-D)=f(x+D), so injectivity of f
implies2D=0. Active D would be H, excluded by Section4. If the second
endpoints agree, equal F similarly forces the first endpoints to agree
and leads to the same contradiction.

If r=x+D, the opposite input difference makes R exactly the reverse
of X. Then F(R)=-A=A, so2A=0, and active A would be H, again excluded.
The other crossed endpoint equality gives the same reversal.

Thus in the selected four-pair system **neither endpoint of R can
equal any endpoint of X or Y**. Also X and Y cannot have an aligned
endpoint in common: their equal input differences would make them
the same pair, contradicting G(Y)-G(X)=2D with D!=H. Crossed endpoint
overlaps between X and Y are not excluded here. In particular the
three-pair core within the four-pair system uses at least five distinct
actual word values. This rules out natural constructions reusing an
X or Y endpoint as the R anchor; it does not exclude arbitrary pairs.

## 6. Why the reciprocal sigma0 condition alone cannot solve the support

For **every permutation** f of an even cyclic group, the map
h(x)=f(x)-x is not a permutation. Indeed sum h(x)=0 because f merely
permutes all elements, whereas the sum of all elements is H modulo N.
If h were a permutation its sum would be H, a contradiction.
Thus some distinct x,y satisfy h(x)=h(y), giving

    D=y-x!=0, f(y)-f(x)=D.

Set X=(x,y),A=D and P=(y,x). They satisfy (5) exactly. Therefore a
search attempting to exclude the reciprocal two-pair system **alone**
would be mathematically misguided. The sigma1 joint-image memberships,
the other original support rows, and genuine base completion are
substantive remaining conditions. This elementary finite-sum argument
and the binary linear method are not claimed as new techniques or
historical priority.

## Replay and final scope

```sh
python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-structure-v7/check.py --negative
```

Only the Python standard library is required. The author checker
passes all1024 witness/row cases,64 inverse basis identities, the
exact necessary transpose filter and all four support bridges; six
damaged controls are rejected. `CHECK-RUN.json` records the actual
result and source hashes. The image equivalences, half-word logic,
endpoint restrictions and finite-sum boundary are written proofs;
sample word fixtures are not substituted for their quantifiers.

`manifest.json` freezes this stage. The small author checks are not
an independent-agent acceptance receipt, formal assistant proof, or
external human review. Local image preimages do not guarantee the
simultaneous original base completion, and the fourth-pair condition
does not supply the remaining original difference rows. No full
support exclusion, real13-word witness, distance>=14, hash collision,
preimage attack, historical-priority, DOI, Release, or main integration
is claimed.
