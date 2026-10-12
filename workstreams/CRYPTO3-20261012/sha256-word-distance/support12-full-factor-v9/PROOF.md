# Correct full factorisation for support identifier 12

**Complete author-written proof candidate for the independent-active-pair
layer.**  This v9 object corrects the target-binding failure preserved in
`support12-full-factor-v8/`.  It does not construct two messages, exclude
the support, or prove distance at least 14.

All arithmetic is in `R=Z/(2^32)`.  Define the FIPS small sigmas

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For one oriented unequal word pair `(u,v)`, put

```
(d,F,G)=(v-u, f(v)-f(u), g(v)-g(u)).
```

Let `J` be the set of all such actual joint triples.  In particular, one
membership in `J` keeps `F` and `G` attached to the same pair.

## 1. Correct object binding and all original rows

The name “support 12” is the zero-based identifier used by the frozen
support list.  Thus the object is `supports[12]`, not the twelfth list entry
`supports[11]`.  Its exact active set is

```
S={10,11,13,15,18,20,26,28,29,34,42,43,57}.         (1)
```

This same set is recorded by the accepted actual-boundary proof and by the
base-lift structural certificate.  The checker binds all three sources by
hash and content.

For every `t=16,...,63`, subtraction of the two SHA-256 schedule rows gives

```
E_t=d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)=0,        (2)
```

where every interface outside `S` is zero.  Exactly 25 rows are nonzero:

| t | `E_t` after substituting (1) |
|---:|---|
| 17 | `-G15-d10` |
| 18 | `d18-d11` |
| 20 | `d20-G18-d13` |
| 22 | `-G20-d15` |
| 25 | `-d18-F10` |
| 26 | `d26-F11-d10` |
| 27 | `-d20-d11` |
| 28 | `d28-G26-F13` |
| 29 | `d29-d13` |
| 30 | `-G28-F15` |
| 31 | `-G29-d15` |
| 33 | `-d26-F18` |
| 34 | `d34-d18` |
| 35 | `-d28-F20` |
| 36 | `-G34-d29-d20` |
| 41 | `-d34-F26` |
| 42 | `d42-d26` |
| 43 | `d43-F28` |
| 44 | `-G42-F29-d28` |
| 45 | `-G43-d29` |
| 49 | `-d42-F34` |
| 50 | `-d43-d34` |
| 57 | `d57-F42` |
| 58 | `-F43-d42` |
| 59 | `-G57-d43` |

The other 23 rows, at

```
16,19,21,23,24,32,37,38,39,40,46,47,48,51,52,53,54,
55,56,60,61,62,63,
```

are identically zero.

## 2. Exact fourteen-coordinate normal form

Choose

```
a=d10, b=d11, c=d13, k=d15, p=F11, q=F13,
x=G10, y=G11, h=G13, l=F15, s=G26,
w=F29, z=F42, j=F57.                                (3)
```

The 39 interface coordinates satisfy all 48 rows (2) if and only if their
thirteen triples are the following.

| i | `d_i` | `F_i` | `G_i` |
|---:|---|---|---|
| 10 | `a` | `-b` | `x` |
| 11 | `b` | `p` | `y` |
| 13 | `c` | `q` | `h` |
| 15 | `k` | `l` | `-a` |
| 18 | `b` | `-p-a` | `-b-c` |
| 20 | `-b` | `-q-s` | `-k` |
| 26 | `p+a` | `-b` | `s` |
| 28 | `q+s` | `-b` | `-l` |
| 29 | `c` | `w` | `-k` |
| 34 | `b` | `-p-a` | `b-c` |
| 42 | `p+a` | `z` | `-w-q-s` |
| 43 | `-b` | `-p-a` | `-c` |
| 57 | `z` | `j` | `b` |

For completeness, the reverse derivation uses every nonzero row.  Rows
17,18,22,25 and 26 give

```
G15=-a, d18=b, G20=-k, F10=-b, d26=p+a.
```

Rows 20 and 27 give `d20=-b` and then `G18=-b-c`.  Rows 28--31 give

```
d28=q+s, d29=c, G28=-l, G29=-k.
```

Rows 33--36 give

```
F18=-p-a, d34=b, F20=-q-s, G34=b-c.
```

Rows 41,42,44,45 give

```
F26=-b, d42=p+a, G42=-w-q-s, G43=-c.
```

Rows 49,50,57--59 give

```
F34=-p-a, d43=-b, d57=z, F43=-p-a, G57=b.
```

Finally row 43 gives `F28=d43=-b`.  Conversely, substitution of the table
zeros all 25 displayed rows, and the remaining 23 are already zero.  No
division is used.

The certificate separately records 53 integer unit row operations taking
the original 25 rows to these 25 pivot equations.  The checker executes and
then reverses every operation.  Therefore the equation modules agree over
the integers, so also over `R`; the solution module is exactly `R^14` and
has no hidden two-power torsion.

## 3. Exact actual-pair factor theorem

At the fourteen-coordinate level, independent-active-pair feasibility is
equivalent to requiring every row of the table in Section 2 to belong to
`J`.  Necessity extracts (3) from the thirteen actual pairs.  Sufficiency
chooses an actual preimage pair for each of the thirteen memberships and
uses equal pairs off the support; Section 2 then gives every difference row.

There is a smaller exact local/global presentation.  Define

```
PF(d,F) iff some G has (d,F,G) in J,
PG(d,G) iff some F has (d,F,G) in J.
```

The private coordinates `x,y,h,j` can be existentially absorbed into their
single factors.  Thus feasibility is equivalent to the existence of ten
shared scalars `a,b,c,k,p,q,l,s,w,z` satisfying

```
a,b,c,k,p+a,q+s,z != 0,                              (4)
```

and the thirteen actual-pair conditions

```
10: PF(a,    -b)
11: PF(b,     p)
13: PF(c,     q)
15: J (k,     l,          -a)
18: J (b,    -p-a,        -b-c)
20: J (-b,   -q-s,        -k)
26: J (p+a,  -b,           s)
28: J (q+s,  -b,          -l)
29: J (c,     w,          -k)
34: J (b,    -p-a,         b-c)
42: J (p+a,   z,          -w-q-s)
43: J (-b,   -p-a,        -c)
57: PG(z,     b).                                      (5)
```

Conditions (4) are precisely the distinct nonzero `d_i` requirements for
the exact support.  The two implications of (5) are just the two
implications of the fourteen-coordinate theorem, with the four private
preimages forgotten or restored.  This retains, rather than relaxes, the
same-pair `F/G` coupling at all nine full `J` factors and through exact
projections at the other four.

The ten-scalar incidence graph is connected.  Its scalar occurrences are

```
a:{10,15,18,26,34,42,43}        b:{10,11,18,20,26,28,34,43,57}
c:{13,18,29,34,43}              k:{15,20,29}
p:{11,18,26,34,42,43}           q:{13,20,28,42}
l:{15,28}                        s:{20,26,28,42}
w:{29,42}                        z:{42,57}.
```

This is the minimal local/global split for this normal form: all four
degree-one parameters are local and each remaining parameter joins at least
two factors.  No uniqueness under arbitrary nonlinear reparametrisation is
claimed.

## 4. Failure boundary

The theorem exactly solves the additive-row bookkeeping while preserving
actual local word-pair semantics.  It does not decide whether (4)--(5) has
a solution.  Even a solution would comprise thirteen independently chosen
pairs and would still require the accepted base-completion residual system
to obtain two common SHA-256 schedules.  Hence this package contains no
message pair, no support exclusion, no distance-14 lower bound, and no Lean
or external human verification.

