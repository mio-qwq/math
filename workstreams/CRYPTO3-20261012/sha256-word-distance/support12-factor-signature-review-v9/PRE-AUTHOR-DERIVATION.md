# Blind reconstruction and resource-boundary freeze

From the accepted corrected `support12-full-factor-v9` table, the projected
graph over `Z/(2^26)` is

```
10 PF(a,-b)                 11 PF(b,p)
13 PF(c,q)                  15 J(k,l,-a)
18 J(b,-p-a,-b-c)           20 J(-b,-q-s,-k)
26 J(p+a,-b,s)              28 J(q+s,-b,-l)
29 J(c,w,-k)                34 J(b,-p-a,b-c)
42 J(p+a,z,-w-q-s)          43 J(-b,-p-a,-c)
57 PG(z,b)
```

with `b=2^16` and nonzero forms `a,b,c,k,p+a,q+s,z`.

The independent encoding uses two actual 32-bit words for each factor and
evaluates the FIPS functions

```
sigma0(x)=ROTR7(x) xor ROTR18(x) xor SHR3(x)
sigma1(x)=ROTR17(x) xor ROTR19(x) xor SHR10(x).
```

Only bits 0 through 25 of `y-x`, `sigma0(y)-sigma0(x)`, and
`sigma1(y)-sigma1(x)` are equated to the factor graph.  Bits 26 through 31
are absent from all graph equalities.  `PF` omits the sigma1 equality and
`PG` omits the sigma0 equality; every `J` keeps F and G attached to the same
word pair.

The resulting CNF has 13,997 variables and 57,032 clauses, digest
`f94f9f26cba2d20ef88e7a52ff735ba3a9a5a8c9507484c398dbf862fb7545d3`.
Generic HiGHS MILP and independent WalkSAT searches were stopped at the
resource boundary without a model.  This is `UNKNOWN`, not `UNSAT`.

No author witness is frozen here.  The post-freeze audit may establish SAT
by direct witness checking even though the blind discovery search did not.

Procedural caveat: an over-broad repository `rg` printed author certificate
pair lines before this freeze was written.  The reconstructed table and CNF
did not use those lines, and neither blind backend found a model, but the
search should not be described as pristine blind discovery.  The acceptance
decision rests on the independent arithmetic audit below, not on this search.
