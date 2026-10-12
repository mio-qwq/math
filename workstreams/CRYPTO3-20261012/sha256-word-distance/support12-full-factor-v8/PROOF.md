# Exact factorisation of all support-12 difference rows

**Complete written proof for the independent-active-pair layer.**  This
does not construct a pair of sixteen-word messages, exclude support 12, or
raise the global distance lower bound.  It retains the joint origin of the
`F` and `G` derivatives at every one of the thirteen active positions.

All arithmetic below is in `R=Z/(2^32)`.  Put

```
f(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x),
g(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

For an oriented unequal word pair `(u,v)`, define its actual joint triple

```
(d,F,G)=(v-u, f(v)-f(u), g(v)-g(u)).
```

Let `J` be the set of all such triples.  Membership in `J` is a single
word-pair obligation: its `F` and `G` coordinates may not be chosen from
different preimages.

## 1. All 48 original rows

Support 12 is

```
S={10,11,15,18,20,26,27,28,29,34,42,43,57}.
```

For every `t=16,...,63`, the original SHA-256 message-schedule difference
row is

```
E_t = d_t-G_(t-2)-d_(t-7)-F_(t-15)-d_(t-16)=0,       (1)
```

where a coordinate whose index is not in `S` is zero.  Exactly 25 rows are
nonzero:

| t | `E_t` after the support substitution |
|---:|---|
| 17 | `-G15-d10` |
| 18 | `d18-d11` |
| 20 | `d20-G18` |
| 22 | `-G20-d15` |
| 25 | `-d18-F10` |
| 26 | `d26-F11-d10` |
| 27 | `d27-d20-d11` |
| 28 | `d28-G26` |
| 29 | `d29-G27` |
| 30 | `-G28-F15` |
| 31 | `-G29-d15` |
| 33 | `-d26-F18` |
| 34 | `d34-d27-d18` |
| 35 | `-d28-F20` |
| 36 | `-G34-d29-d20` |
| 41 | `-d34-F26` |
| 42 | `d42-F27-d26` |
| 43 | `d43-F28-d27` |
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

are identically zero.  Thus no boundary row is silently removed.

## 2. Fourteen-scalar normal form

Choose the fourteen free coordinates

```
a=d10, b=d11, c=d15, p=F11, x=G10, y=G11,
q=F15, r=G18, s=G26, u=F27, v=G27,
w=F29, z=F42, j=F57.                              (2)
```

Then all 39 interface coordinates satisfy all 48 rows if and only if their
thirteen triples are exactly the following table.

| i | `d_i` | `F_i` | `G_i` |
|---:|---|---|---|
| 10 | `a` | `-b` | `x` |
| 11 | `b` | `p` | `y` |
| 15 | `c` | `q` | `-a` |
| 18 | `b` | `-p-a` | `r` |
| 20 | `r` | `-s` | `-c` |
| 26 | `p+a` | `-r-2b` | `s` |
| 27 | `r+b` | `u` | `v` |
| 28 | `s` | `-2r-3b` | `-q` |
| 29 | `v` | `w` | `-c` |
| 34 | `r+2b` | `-u-p-a` | `-v-r` |
| 42 | `u+p+a` | `z` | `-w-s` |
| 43 | `-r-2b` | `-u-p-a` | `-v` |
| 57 | `z` | `j` | `r+2b` |

Here is a direct reverse derivation.  Equations 25,17,18,20,22 give
`F10=-b`, `G15=-a`, `d18=b`, `d20=r`, `G20=-c`.
Equations 26--31 give

```
d26=p+a, d27=r+b, d28=s, d29=v, G28=-q, G29=-c.
```

Equations 33--36 give

```
F18=-p-a, d34=r+2b, F20=-s, G34=-v-r.
```

Equations 41,42,44,45 give

```
F26=-r-2b, d42=u+p+a, G42=-w-s, G43=-v.
```

Equations 49,50,57--59 give

```
F34=-u-p-a, d43=-r-2b, d57=z,
F43=-u-p-a, G57=r+2b.
```

Finally equation 43 gives
`F28=d43-d27=-2r-3b`.  These are all 25 nonzero equations, each used
without division.  Conversely, direct substitution of the table makes
each displayed row zero; the other 23 rows already are zero.  This proves
both directions over `R`.

The machine certificate strengthens the bookkeeping statement: 57
explicit integer unit row operations transform the original 25 rows into
the 25 pivot equations in the table, and the checker reverses all 57
operations.  Hence the two equation modules agree integrally, not merely
after a rank computation over a field.  The pivots have coefficient one,
so the solution module is exactly `R^14`; there is no hidden 2-power
torsion.  In particular, fourteen is the minimum number of cyclic scalar
coordinates in a bijective linear parametrisation of this solution module.

## 3. Exact thirteen-factor theorem

The independent-active-pair support-12 system is feasible if and only if
there exist `a,b,c,p,x,y,q,r,s,u,v,w,z,j in R` such that **all thirteen
rows of the table belong to `J`**.

Necessity: take the actual pair at each active index.  Its three
coordinates are in `J`; Section 2 extracts (2) and forces the table.

Sufficiency: for each table row choose one actual preimage pair promised
by its membership in `J`.  At every inactive index choose an equal pair,
whose three differences are zero.  Section 2 then makes all 48 difference
rows (1) hold.  Pair choices at different indices remain independent in
this theorem.  In particular, it does not assert that the chosen word
values satisfy either undifferenced SHA-256 recurrence or arise from two
common sixteen-word bases.

Because both `f` and `g` are binary-linear bijections, every member of `J`
has three nonzero coordinates.  Thus the factor theorem includes, without
a solver, the necessary conditions

```
a,b,c,p,x,y,q,r,s,u,v,w,z,j != 0,
p+a, r+2b, r+b, 2r+3b, u+p+a, v+r, w+s != 0.        (3)
```

These seven affine hyperplane exclusions are structural obstacles, not a
support exclusion.

## 4. Smallest local/global split of this normal form

The exact factor graph has one factor for each table row and one scalar
node for each free parameter, with an edge when that scalar occurs in the
factor's joint triple.  Three parameters have degree one:

```
x at factor 10, y at factor 11, j at factor 57.
```

They can be existentially eliminated inside their own actual joint-image
membership.  The remaining eleven shared scalar nodes have incidences

```
a:{10,15,18,26,34,42,43}       b:{10,11,18,26,27,28,34,43,57}
c:{15,20,29}                    p:{11,18,26,34,42,43}
q:{15,28}                       r:{18,20,26,27,28,34,43,57}
s:{20,26,28,42}                 u:{27,34,42,43}
v:{27,29,34,43}                 w:{29,42}
z:{42,57}.
```

This eleven-scalar incidence graph is connected and is the minimal
local/global split **for the displayed normal form**: all degree-one
coordinates have been made local, while every remaining coordinate joins
at least two pair factors.  No claim of uniqueness or absolute graph
minimality under arbitrary nonlinear reparametrisation is made.

## 5. Scope

The reduction is exact and solver-free at the independent-active-pair
level.  It gives a concrete next target: either realize all thirteen
coupled memberships, then solve the common-base completion, or derive a
joint-image obstruction to one of them.  It provides neither such a
realization nor such an obstruction today.  In particular it contains no
distance-13 message pair, support-12 exclusion, distance-at-least-14
proof, Lean formalisation, historical-priority claim, or cryptographic
attack.

