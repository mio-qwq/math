# One unrestricted probe of the actual three-pair core

The object is six actual 32-bit words x,x',y,y',r,r'. Let
D=x'-x modulo2^32 be nonzero. Impose exactly

```
y'-y=D, r'-r=-D,
f(x')-f(x)=f(y')-f(y)=f(r')-f(r),
[g(y')-g(y)]-[g(x')-g(x)]=2D,
[g(y')-g(y)]-[g(r')-g(r)]=D.
```

Here f=ROTR7 xor ROTR18 xor SHR3 and g=ROTR17 xor ROTR19 xor SHR10.
All displayed subtraction and multiplication occur modulo2^32. This is
the support-12 necessary local core, not thirteen active pairs, an actual
base schedule, a sixteen-word input block or a compression differential.
There is no valuation restriction on D, selected XOR mask, fixed base,
linearized addition, free derivative variable or independent-carry
assumption. High-divisibility exclusions do not resolve this question.

The six input words give192 raw Boolean parameters. D is derived, not
an additional free word. Two 32-bit input-difference equalities determine
y' and r' from x,x',y,r, leaving128 effective free input bits before the
four remaining 32-bit derivative equalities and D!=0. These equation
counts are a representation budget, not rank, independence or a claimed
solution probability. All derivatives retain the same actual word bits.

The mathematical reversal symmetry is exact: exchanging primed and
unprimed members of all three pairs negates D and every derivative,
preserving all equations. The probe does not use that symmetry to prune
the domain.

Protocol: one Z3 QF_BV query, timeout15000ms, no seed sweep or retry.
SAT requires a separate standard-library verifier rebuilding each sigma
one output bit at a time and checking the six actual words, nonzero D,
all equations and full reversal. UNKNOWN ends this probe. A solver UNSAT
answer without an independently checked certificate is recorded only as
unverified solver output and supplies no impossibility theorem.
