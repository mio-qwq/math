# A sigma difference two-cycle alone is always feasible

Status: elementary written proof; not a full schedule result. This is a
methodological boundary using the classical finite-sum obstruction to
complete mappings of even cyclic groups. No originality is asserted.

Let N be a positive even integer, R = Z/N, and f:R→R any permutation.
For every c∈R there exist x≠x' and y≠y' such that

```
y' - y = f(x') - f(x),
f(y') - f(y) = -(x' - x),
y = c + f(x), y' = c + f(x').
```

Indeed, define h_c(x)=x+f(c+f(x)). As x ranges over R, both x and
f(c+f(x)) separately run through all residues. Thus

    sum_x h_c(x) = 2 sum_x x = 0 in R.

But the sum of every residue exactly once is N/2 in R, which is
nonzero. Therefore h_c is not injective on the finite set R. Choose
x≠x' with h_c(x)=h_c(x') and set y=c+f(x), y'=c+f(x').
Injectivity of f implies y≠y'. Subtracting these definitions and the
h_c equality proves the claimed two equations.

The real SHA-256 sigma0 is a permutation of Z/(2^32) as a set, by the
frozen complete inverse-basis certificate. Hence the theorem applies.
In support 5, equations at t=26,34,42,49 require
`d34=F19` and `F34=-d19`. Those two relations alone therefore cannot
exclude support 5. The theorem imposes neither the other difference
equations nor the actual base-schedule equations, and does not supply
a pair at distance 13. The statement is independent of padding or IV.
