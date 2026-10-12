# Existence of the Ka(m,4) density and a sharper 2/7 upper bound

The scope is arXiv:2604.15909v1 Problem5.2, fixed word length four and arbitrary alphabet size. This is a partial universal bound and limiting-density theorem.

## Statement

The limit

    lambda_4 = lim_{m -> infinity} gp(Ka(m,4))/m^4

exists. Combining the constructive lower bound in LOWER_BOUND.md with the proof below yields

    26/125 <= lambda_4 <= 2/7.

For every integer m>=7, a finite upper bound is

    gp(Ka(m,4)) <= floor(2(m)_4/7) + m(m-1)(3m-5),

where (m)_4=m(m-1)(m-2)(m-3). This bound is not claimed sharp at small m. The new ingredients are a cyclic seven-window constraint and standard subalphabet averaging. No numerical optimization supports either assertion.

## 1. Original distances and isometric alphabet restriction

Vertices abcd have unequal adjacent symbols; an arc shifts one position and appends any symbol unequal to d. Between distinct vertices the directed distance is four minus the longest proper suffix/prefix overlap (zero overlap allowed). Every shorter walk would force such an overlap. Conversely, appending the target suffix realizes the overlap; if there is no overlap, the first append is legal because the last source symbol differs from the first target symbol.

This formula does not depend on unused alphabet symbols. Thus restricting to any subalphabet is isometric, even though we always measure distances in the entire original digraph. A GP set excludes three distinct selected vertices x,y,z with d(x,y)+d(y,z)=d(x,z).

## 2. Seven distinct symbols supply at most two selected windows

Take any ordered seven distinct symbols a_0,...,a_6 and read indices modulo7. Let

    W_i = a_i a_{i+1} a_{i+2} a_{i+3},  0<=i<7.

For forward offsets j=1,2,3,4, the original distance d(W_i,W_{i+j}) is exactly j. For j<=3 this follows from its overlap of length4-j, with no longer overlap because all seven symbols are distinct. For j=4 there is no nonempty overlap. Importantly, the entire seven-cycle is NOT claimed isometric: offsets5and6 have shortcuts.

Among any three distinct positions on a seven-cycle, their three positive cyclic gaps sum to7, so the largest gap is at least3. The complementary directed arc spans at most4 edges and contains all three positions. Its window sequence is a geodesic by the preceding distance assertion. Consequently a GP set contains at most two of W_0,...,W_6.

## 3. Double counting all seven-symbol cycles

Let S_4 be any GP set of four-distinct-letter words. Choose a uniformly random ordered seven-tuple of distinct alphabet symbols. A specified word abcd occurs as one of the seven windows with probability

    7/(m)_4.

For each chosen starting position, fix its four entries and freely fill the remaining three with distinct unused symbols: there are (m-4)_3 choices out of (m)_7 total. Occurrence at two different positions is impossible because all symbols are distinct. Thus the probabilities add.

Every sampled seven-tuple contains at most two selected windows, so taking expectations gives |S_4|<=2(m)_4/7. Every arbitrary GP set consists of such words plus at most m(m-1)^3-(m)_4=m(m-1)(3m-5) words with repeated symbols. This proves the finite bound and limsup<=2/7.

## 4. Monotone normalized extremal function and existence of the limit

For m>=4 let f(m) be the maximum size of a GP set consisting solely of four-distinct-letter words, with original Ka(m,4) distances. For m>=n>=4, choose an n-symbol subset uniformly at random and intersect an optimal f(m)-set with the words over that subset. Isometric restriction makes this a feasible f(n)-set. Each selected word survives with probability

    binom(m-4,n-4)/binom(m,n) = (n)_4/(m)_4.

Therefore

    f(m)/(m)_4 <= f(n)/(n)_4.

These normalized numbers are nonincreasing and nonnegative, hence converge. On the other hand,

    0 <= gp(Ka(m,4))-f(m) <= m(m-1)(3m-5)=O(m^3).

Since (m)_4/m^4 tends to1, gp(Ka(m,4))/m^4 has the same limit. Section3 bounds it above by2/7.

Finally, the lower bound in LOWER_BOUND.md is gp(Ka(5q,4))>=130q^4-74q^3+8q^2. For arbitrary m use q=floor(m/5) and the isometric subalphabet inclusion. Division by m^4 gives lambda_4>=130/625=26/125.
