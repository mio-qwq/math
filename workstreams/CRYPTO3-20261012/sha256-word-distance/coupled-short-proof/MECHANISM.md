# Short-proof attempt for the fixed-mask coupled boundary

This is a proof-compression attempt, not a review of the CNF or its RUP
certificate. It does not assume the unreviewed affine-fibre enumeration.
The exact local question is whether arbitrary 32-bit words can satisfy

```
K = fbca7000, q' = q xor K,
q + g(q) = q' + g(q'),
p' + q = p + q',
f(p') + f(q') = f(p) + f(q),
```

where all additions are modulo `2^32`,
`f=ROTR7 xor ROTR18 xor SHR3`, and
`g=ROTR17 xor ROTR19 xor SHR10`. Their fixed-mask images are
`f(K)=828ee412` and `g(K)=763e9000`.

## First mechanism: necessary input/output mask synchronization

Let `A=p xor p'` and `D=q'-q=p'-p`. Since the least active bit of `K`
is 12, `v2(D)=12`. Hence `A` has low 12 bits zero and bit 12 one.
The third equation makes the two sigma0 differences opposite, and the
least active bit of `f(K)` is 1. Therefore the least active bit of
`f(A)` is also 1. With `A[0..11]=0`, the standard output-bit equations
give `f(A)[0]=A[18]` and `f(A)[1]=A[19]`. Thus

```
A[0..11]=0, A[12]=1, A[18]=0, A[19]=1.
```

Only 17 mask bits remain free. A bounded screening of these `2^17`
possibilities can test a new mechanism: whether the shared arithmetic
difference and opposite sigma0 derivatives force `A` into a very small
set, possibly `A=K` or a few affine classes. It is not a search over
actual base words and not a rerun of any support, tail, SAT, or RUP task.

For any two signed bit-mask sums that are equal modulo `2^32`, a bit
with exactly one active mask cannot immediately follow a bit where
both masks are inactive. At bit zero the incoming carry is also zero.
Consequently the two necessary tests are

```
((A xor K) & ~((A | K) << 1)) & ffffffff == 0,
((f(A) xor f(K)) & ~((f(A) | f(K)) << 1)) & ffffffff == 0.
```

The first comes from equality of the input additive differences; the
second comes from the sum of the output differences being zero. These
tests discard signs and the dependence between base sigma bits, so a
surviving mask is only necessary evidence, not a solution.

If only a small set remains, the next step is to derive its shared
linear constraints and inspect the exact carry equations together with
the fixed `q` sigma1 collision. If the screening leaves a large,
unstructured set, the mask-only route will be recorded as insufficient
rather than expanded into a full pair search.

## A possible final linear contradiction

When `A=K`, equal input derivatives force `p_i=q_i` on changed input
bits below 31. Opposite sigma0 derivatives force the sigma0 base bits
to be complementary on changed output bits below 31. Thus for
`z=p xor q`, this special case reduces to

```
z & (K & 7fffffff) = 0,
f(z) & (f(K) & 7fffffff) = f(K) & 7fffffff.
```

A 32-column binary linear consistency check can decide whether this
particular mask is already impossible. The top bit is intentionally
omitted: changing both signs at weight `2^31` changes an integer sum
by a multiple of `2^32`. No argument may force that bit without an
additional carry constraint.

## Second mechanism: adjacent carry parity gives linear equations

The first screen leaves 132 masks. Their affine hull still has dimension
17, so no new universal linear condition on `A` follows merely by taking
that hull. The special case `A=K` is inconsistent by the very short
identity `f(z)[10]=z[17] xor z[28] xor z[13]`: the input constraints
force the right side zero while the output condition forces the left
side one.

Before using any fixed-mask `h` fibres, a sharper necessary condition
can be extracted from adjacent carry parity for each surviving mask.
For equality of the input derivatives, the signed carry entering bit
`i` has parity `A_i xor K_i`. If both masks are active at that bit,
the carry is therefore zero. Its outgoing value is `q_i-p_i`, whose
parity is `z_i` for `z=p xor q`. The next bit then forces

```
z_i = A_(i+1) xor K_(i+1)  whenever A_i=K_i=1 and i<31.
```

For the opposite sigma0 derivatives, put `B=f(A)` and `L=f(K)`.
When `B_i=L_i=1`, the outgoing carry is
`1-f(p)_i-f(q)_i`. Its parity is `1 xor f(z)_i`, giving

```
f(z)_i = 1 xor B_(i+1) xor L_(i+1)
          whenever B_i=L_i=1 and i<31.
```

These are binary linear constraints on `z` for each fixed `A`. A bounded
check of the 132 small linear systems will test whether the mixed-mask
possibilities already contradict sigma0 linearity. The mask `A=K`
reduces to the previous three-input-bit contradiction. Surviving linear
systems would again be necessary relaxations, not actual coupled words.

## Third mechanism: fixed masks make the full zero-sum carry system affine

The adjacent-bit screen rejects 58 masks, all using the same sigma0
output-bit-10 identity, and leaves 74. To avoid promoting necessary
linear conditions into an equivalence, the next mechanism retains the
entire signed-carry recurrence.

Consider two fixed XOR masks `a,b` and the exact modular equation

```
sum_i [a_i(1-2u_i) + b_i(1-2v_i)] 2^i = 0 mod 2^32.
```

The `u_i,v_i` may themselves be affine binary expressions in arbitrary
base words. Every signed carry `c_i` is in `{-1,0,1}`, and its parity
is fixed by `w_i=a_i xor b_i`. Thus `c_i=0` when `w_i=0`, and
`c_i=1-2t_i` when `w_i=1`. For bits below 31 put
`w'=a_(i+1) xor b_(i+1)`. The complete local transitions are:

| Active masks at bit i | Required binary equation | Next carry sign when w'=1 |
|---|---|---|
| none | `w'=0` | impossible if `w'=1` |
| both, with base bits u,v | `u xor v = 1 xor w'` | `t_(i+1)=u=v` |
| one, with base bit u | `t_i xor u = 1 xor w'` | `t_(i+1)=t_i=u` |

The initial condition requires `w_0=0`. At bit31 there is no restriction
on the final carry; the current carry parity already makes the bit sum
even. Consequently all the conditions are affine binary equations.
There is no hidden sign branch in this description: a nonzero next
carry's sign can be substituted by the displayed base bit.

The table follows from the integer equation
`c_i + a_i(1-2u_i)+b_i(1-2v_i) = 2c_(i+1)`.
For one active mask the next carry is `1-t_i-u_i`; for two it is
`1-u_i-v_i`. Its parity fixes whether the two binary arguments are
equal or different, and its sign in the equal case is explicit.
Both directions follow, giving an exact equivalence, not only necessity.

Apply this to the fixed `A` cases as follows:

- Input derivative equality: masks `A,K`, base forms `p_i,q_i xor 1`.
- Opposite sigma0 derivatives: masks `f(A),f(K)`, base forms
  `f(p)_i,f(q)_i`.
- The fixed-mask h collision: masks `K,g(K)`, base forms `q_i,g(q)_i`.

For each of the 132 previously screened masks, these are three affine
systems on the 64 actual base bits of `p,q`. A single bounded matrix
check can therefore produce short XOR contradictions, or reconstruct
an actual pair if a system survives. This is a different proof
representation from the existing CNF/RUP proof. The 64-fibre exploration
is neither read nor assumed. Tiny complete transition truth tables
will check the carry table itself before using the 32-bit systems.

## Completed compression

All 132 exact fixed-mask affine systems were inconsistent. Their row
contradictions compress to ten templates using 26 different binary rows,
with only 36 template-row occurrences. The final 13,098-byte certificate
and separately written direct-bit checker require no solver or Gaussian
elimination to verify. The final checker passed, including all 14 damaged
controls. Complete mathematics, the 132-mask partition, and actual run
evidence are in `PROOF.md`, `CERTIFICATE.json`, `check.py`, and `RUNS.json`.
No CNF/RUP or affine-fibre file was read or imported in this reconstruction.
Independent-agent review is recorded separately; the same-author checker
is not presented as that review.
