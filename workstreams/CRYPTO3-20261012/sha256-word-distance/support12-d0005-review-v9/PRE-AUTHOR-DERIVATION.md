# Pre-author sign and orientation freeze

This note was written before opening the contents of
`support12-d0005-v9`.  The constants and the two known forward pairs are
reconstructed from the accepted v9 q=5 fixture and evaluated directly with
the standard SHA-256 small-sigma formulas.

All arithmetic is modulo `2^32`.  Write

```
f(x) = ROTR7(x) xor ROTR18(x) xor SHR3(x)
g(x) = ROTR17(x) xor ROTR19(x) xor SHR10(x)
F_h(x) = f(x+h)-f(x)
G_h(x) = g(x+h)-g(x).
```

The fixed data are

```
D = 00050000
A = 40406e02
T = 1ffd913e
X = (0ffb000a, 1000000a)
Y = (0ffb0002, 10000002)
```

Direct evaluation gives

```
(d,F,G)(X) = ( D, A, 1ff8913e) = (D,A,T-D)
(d,F,G)(Y) = ( D, A, 2002913e) = (D,A,T+D).
```

The selected three-pair equations use a third pair `R` with orientation
`d(R)=-D`, `F(R)=A`, `G(R)=T`.  Reversing it produces a forward-`D`
pair `Z`, and reversal negates every modular derivative.  Therefore the
exact third-image query is

```
(d,F,G)(Z) = (+D,-A,-T)
            = (00050000,bfbf91fe,e0026ec2).
```

In particular, neither `(+D,+A,+T)` nor `(-D,-A,-T)` is the required
orientation.

For the fourth-pair coupling, the original orientation is
`(d,F)(P)=(-A,-D)`.  Reversing `P` to `Q` negates both coordinates, so

```
(d,F)(Q)=(+A,+D).
```

Writing `Q=(u,u+A)`, its exact reciprocal condition is consequently
`F_A(u)=D`, not a one-sign-flipped variant.

The independent finite questions frozen for review are thus:

1. Is there a 32-bit `z` with `F_D(z)=-A` and `G_D(z)=-T`?
2. Is there a 32-bit `u` with `F_A(u)=D`?

The scope is only this fixed candidate and these two selected local image
questions.  It says nothing about other q=5 values of `A`, full support,
message completion, or distance 14.
