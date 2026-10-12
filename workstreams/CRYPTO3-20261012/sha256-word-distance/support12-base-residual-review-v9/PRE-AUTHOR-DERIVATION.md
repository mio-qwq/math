# Blind derivation: composing base row 57 with the position-57 factor

Status: frozen before any file in `support12-base-residual-v9` was read.
This is an exact coordinate derivation, not residual solvability, a factor
witness, or a message pair.

Let `u_i` be the prescribed first endpoint at active position `i` in the
accepted base chart, and let `p_9,p_12,p_14,p_19,p_22` be its inactive
anchors.  Trace the accepted 46 `(row,target)` solves solely by original-row
incidence.  The prescribed coordinate `u_57` reaches exactly

```
C57, C59, C61, C63.
```

Indeed no solve before row 59 reads coordinate 57.  Row 59 creates
`C59=g(u57)+C52+f(C44)+C43`; row 61 then reads `C59`, and row 63 reads
`C61`.  No other solved coordinate reads one of this chain.  Consequently
`R33` is independent of `u57`.  In row 57, all four right-side coordinates
are already independent of `u57`, so exactly

```
R57 = u57 - B,
B = g(C55) + C50 + f(C42) + C41             (mod 2^32).
```

Thus row 57 is not an irreducible residual once `u57` is allowed to be
chosen.  Remove 57 from the prescribed coordinates and insert solve
`(row 57,target 57)` after row 56 and before row 59.  Starting from the
twelve active coordinates other than 57 and the same five anchors, this
uses 47 distinct original rows to solve 47 distinct coordinates.  The only
remaining row is 33.  The exact base criterion becomes `R33=0`, and the
first endpoint at position 57 is forced to be `u57=B`.

In the accepted factor normal form, position 57 is

```
d57=z, G57=b, with projected factor PG(z,b).
```

For an oriented pair whose first endpoint is `u57`, its actual condition is

```
g(u57+z)-g(u57)=b.
```

After the rewritten base chart, exact composition therefore requires

```
g(B+z)-g(B)=b.                              (pointwise condition)
```

The existential projection `PG(z,b)` remains a necessary consequence but
is not sufficient: its witness may be a base word different from `B`.
Definitionally, for the actual SHA-256 `g`, `z=1,b=0x0000a000` has the PG
witness `x=0`, whereas at `B=4` the derivative is `0xffffa000`.  The private
coordinate `F57` is simply the actual value `f(B+z)-f(B)` and is not used by
any original row through 63.

The checker independently validates the dependency trace, the 47-step
rewritten chart, twelve genuine schedule roundtrips, the identity
`R57=u57-B`, exact changed-coordinate controls, and the PG/pointwise
separation example.

Scope: this derivation never asserts that `R33=0` is soluble together with
the other twelve pointwise active-pair conditions, and never infers an
actual message pair.
