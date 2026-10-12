# Coupled seven- and nine-window moments for Ka(m,4)

## Scope and statements

This is a new partial upper bound for the original directed general-position
problem in Chandran et al., [arXiv:2604.15909v1, Problem 5.2](https://arxiv.org/html/2604.15909v1#S5).
The alphabet has **m letters**, the word length is four, and general position
excludes a third selected vertex on **any** shortest directed path. Digons and
nonadjacent repeated letters are retained. Historical priority is unconfirmed.
The source question for all word lengths is not solved here.

Put

    alpha = (9 - sqrt(33))/12 = 0.271286446121830945...

**Theorem A (universal asymptotic bound).**

    limsup_(m -> infinity) gp(Ka(m,4))/m^4 <= alpha.

The inherited existence theorem and lower construction therefore give

    26/125 <= lambda_4 <= (9-sqrt(33))/12 < 377/1320.

Theorem A has an elementary proof without an enumeration or solver dependency.

**Theorem B (finite refinement).** Define falling factorials in the usual
integer sense, so `(m)_j=0` when `m` is a nonnegative integer less than `j`, and put

    P_m = 8(m)_2 + 12(m)_3 + 15(m)_4 + 3(m)_5
        = 3m^5 - 15m^4 + 27m^3 - 13m^2 - 2m.

For every integer `m >= 2`,

    gp(Ka(m,4))
      <= floor( m^4 [9-sqrt(33-72P_m/m^7)]/12 ).

In particular, the upper expression is

    alpha m^4 + (9/sqrt(33))m^2 + O(m).

The finite refinement uses a complete, small equality-pattern certificate:
877 partitions of seven positions, with every relevant original distance
rebuilt by BFS. It does not use a numerical optimum on Ka(m,4), the old
five-letter search, or an inference from finite samples to arbitrary m.
The finite-to-universal bridge is given explicitly below.

## 1. Original directed distances

The vertices are words `abcd` with `a!=b`, `b!=c`, and `c!=d`.
There is an arc from `abcd` to `bcde` exactly when `d!=e`.

For different vertices `u,v`, the distance is the smallest `s` in `{1,2,3}`
such that `suffix_(4-s)(u)=prefix_(4-s)(v)`, if one exists, and four otherwise.
Indeed, after fewer than four left shifts a walk still retains the indicated
suffix of its initial vertex, proving necessity. The target suffix realizes
each possible overlap by successive valid appends. If no positive overlap
exists, the last source letter differs from the first target letter, so all
four target letters can be appended legally. Thus the diameter is at most four.

Consequently, three distinct selected vertices `u,v,w` violate general position
exactly when `d(u,v)+d(v,w)=d(u,w)` for some ordering. A shortest path has no
repeated vertex, so the metric condition is equivalent to the original
all-shortest-path quantifier. The distance formula is unchanged on an enlarged
alphabet, proving isometric alphabet restriction.

## 2. The three local pair probabilities

Fix any original GP set `S`, including its permitted repeated-letter words.
Extend its indicator `f` by zero to all of `[m]^4` outside `S`, and let

    p = E f(U_0,U_1,U_2,U_3) = |S|/m^4,

where all the letters are independent and uniform. For `d=1,2,3` define

    q_d = E[f(U_0,U_1,U_2,U_3)
            f(U_d,U_(d+1),U_(d+2),U_(d+3))],
    Q = q_1+q_2+q_3.

For `n=7` or `9`, independently sample `n` letters and read their indices
cyclically. Let `N_n` be the **number of occurrences** of selected four-windows
among the `n` starting positions. Occurrences are counted separately even if
two resulting words agree. Every individual window has the same four-letter
product distribution, so

    E N_7 = 7p,          E N_9 = 9p.

Each unordered pair of positions in a seven-cycle has a unique shorter cyclic
separation `d in {1,2,3}`. There are seven pairs of each separation. After
rotating the starting index, the two windows use `d+4 <= 7` independent input
coordinates in exactly the arrangement defining `q_d`. Therefore

    E binom(N_7,2) = 7Q.                                      (1)

For nine positions there are nine pairs at each shorter separation
`d in {1,2,3,4}`. The first three have the same distributions as above. At
separation four, the two length-four windows use **disjoint** sets of input
coordinates. Their indicators are independent, with joint expectation `p^2`.
Thus

    E binom(N_9,2) = 9Q + 9p^2.                               (2)

These are exact identities for every finite m and every indicator f. No
independence of overlapping windows is asserted. Independence is used only
for the disjoint pairs in the nine-cycle.

## 3. Elementary proof of Theorem A

When the seven cyclic letters are all distinct, any three starting positions
have three positive cyclic gaps summing to seven. A largest gap is at least
three, so its complementary directed arc spans at most four edges and
contains all three positions. For offsets one through four along this arc,
the original distance equals the offset by Section 1: the natural overlap
exists and a longer one would identify distinct letters. Thus three selected
windows would lie on an original geodesic. In particular `N_7 <= 2` on the
all-distinct event. This does not claim that the whole seven-cycle is isometric.

Let `delta_m = 1-(m)_7/m^7`. Pointwise `0 <= N_7 <= 7`, and

    binom(N_7,2)-N_7/2 <= 0

on the all-distinct event, while its value is at most `35/2` elsewhere.
Using (1) gives

    Q <= p/2 + (5/2)delta_m.                                  (3)

For every nonnegative integer N,

    binom(N,2) >= 2N-3,                                       (4)

because the difference is `(N-2)(N-3)/2`, a nonnegative number at every
integer. Apply (4) to `N_9` and use (2) and (3):

    18p-3 <= 9Q+9p^2 <= (9/2)p + 9p^2 + (45/2)delta_m.

Equivalently,

    6p^2 - 9p + 2 + 15delta_m >= 0.                           (5)

Since `delta_m -> 0` and `0 <= p <= 1`, every limit point x of the normalized
maximum satisfies `6x^2-9x+2 >= 0`. The roots are
`(9-sqrt(33))/12` and `(9+sqrt(33))/12`. The larger root exceeds one, so
every such limit point is at most alpha. This proves Theorem A directly as a
limsup statement. The inherited density-limit theorem supplies existence;
its three-block family supplies the unchanged lower endpoint `26/125`.

The upper endpoint decreases by approximately `0.01431961448423`. The gap
to the inherited lower endpoint decreases from approximately `0.07760606060606`
to `0.06328644612183`, a reduction of about 18.45 percent. This is a new
joint-moment constraint, not a rounding of the old seven-window count.

## 4. Why the finite correction has degree two

There is already a short non-computational improvement to the collision
argument: seven cyclic letters with **at least six distinct values** still
force `N_7 <= 2`.

Here is a detailed justification. Assume three windows are selected, and
rotate the largest-gap complement so their positions are `0<s<t<=4`.
Successive selected positions differ by at most three. Their three valid
windows therefore cover every adjacent pair of letters in the concatenated
word, making the natural length-t walk legal. The windows are distinct:
equality of two different four-windows forces at least two distinct position
identifications, whereas the seven inputs have at most one repeated pair.

The possible shorter distances are also excluded. Along a legal walk of
length two, a one-step shortcut forces adjacent letters to agree. Along
length three, a two-step shortcut does the same; a one-step shortcut requires
the alternating identities `b=d=f` and `c=e`. Along length four, a three-step
shortcut forces `d=e`; a two-step shortcut requires both `c=e` and `d=f`;
a one-step shortcut requires `b=e,c=f,d=g`. The non-adjacent alternatives
all require at least two independent position identifications among the
seven cyclic inputs. Thus the walk is geodesic, a contradiction.

Failure consequently needs at most five distinct input values. Its probability
is `O(m^-2)`: it implies either an equal triple among seven positions (35
choices), or two disjoint equal pairs (105 choices); each event has probability
`m^-2`. This alone would yield an explicit but coarser `O(m^2)` finite bound.
The exact small certificate below gives a much smaller correction without
changing the asymptotic argument.

## 5. Complete equality-pattern certificate

Canonicalize each seven-letter tuple by numbering its distinct values in order
of first appearance. These are exactly the 877 set partitions of seven
labelled positions (restricted-growth words). A pattern with k distinct values
has exactly `(m)_k` realizations over `[m]`: choose the distinct actual letters
in their first-appearance order.

For each pattern, form its seven cyclic four-windows. Invalid Kautz words have
indicator zero. For every valid word retain its occurrence multiplicity.
There are at most seven distinct valid words. Compute their original distances
in `Ka(k,4)` by adjacency and BFS, enumerate their GP subsets, and maximize the
sum of their occurrence multiplicities. Isometric alphabet restriction makes
this the correct capacity in every original `Ka(m,4)` realizing the pattern.
There is no replacement of original graph distances by distances in the
induced graph of windows.

The complete capacity counts are:

| Number k of distinct letters | Capacity 0 | Capacity 1 | Capacity 2 | Capacity 3 | Capacity 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 35 | 14 | 7 | 0 | 7 |
| 3 | 56 | 70 | 147 | 28 | 0 |
| 4 | 14 | 49 | 252 | 35 | 0 |
| 5 | 0 | 7 | 126 | 7 | 0 |
| 6 | 0 | 0 | 21 | 0 | 0 |
| 7 | 0 | 0 | 1 | 0 | 0 |

For capacity B the maximum of `N(N-2)` over permitted nonnegative occurrence
counts is `max(0,B(B-2))`. The sums of these twice-excess values, by k, are

    k:                 1   2   3    4   5   6   7
    twice-excess sum:  0  56  84  105  21   0   0.

Every local subset attaining a listed capacity has an explicit witness;
every subset exceeding it is rejected by a shortest-path triple. The
independent checker reconstructs both the equality partitions and all original
adjacency/BFS data, verifies every capacity, and tests deliberately damaged
inputs. The discovery file uses the overlap formula for exploration and is
not imported by the independent checker.

Summing over the `(m)_k` realizations of each equality pattern gives

    E[N_7(N_7-2)] <= [56(m)_2+84(m)_3+105(m)_4+21(m)_5]/m^7
                  = 7P_m/m^7.

Equations (1) and `E N_7=7p` now yield the exact refinement

    Q <= p/2 + P_m/(2m^7).                                   (6)

This proves an inequality for every original GP set, not a claim that a
single global set attains all the local capacities simultaneously.

## 6. Solving the finite quadratic

Combine (2), (4), and (6) as in Section 3. The result is

    6p^2-9p+2+epsilon_m >= 0,   epsilon_m = 3P_m/m^7.           (7)

For every m>=2, `0 <= epsilon_m < 1`. At m=2 it is `3/8`. For m>=3,
the expansion of P gives `P_m < 3m^5`, since

    15m^3-27m^2+13m+2 > 0

(already `15m-27>0` for m>=2). Thus `epsilon_m<9/m^2<=1` for m>=3.
The quadratic in (7) has positive discriminant `33-24epsilon_m>9`, and
its larger root exceeds one. Since `p<=1`, (7) forces

    p <= [9-sqrt(33-24epsilon_m)]/12.

Substitution of epsilon and the integrality of `|S|` prove Theorem B.
Finally `epsilon_m=9/m^2+O(m^-3)` and the derivative of the smaller-root
expression at epsilon=0 is `1/sqrt(33)`, which gives the stated expansion.

An exact integer implementation can avoid all square-root rounding: for
each integer candidate size s in `[0,m^4]`, inequality (7) is equivalent to

    6s^2 - 9sm^4 + 2m^8 + 3mP_m >= 0.                       (8)

The valid sizes below `m^4` form the initial interval ending at the asserted
floor. Binary search using integers therefore returns the exact finite upper
bound. A floating-point approximation is never used to certify a size.

## 7. Dependencies and verification boundary

- The asymptotic proof uses only the original distance bridge, independent
  input letters, finite expectation identities, and the integer inequality (4).
- The stronger finite correction additionally uses the complete 877-pattern
  certificate, with an independent original-adjacency replay.
- The existence of lambda_4 and the lower construction are inherited from
  `workstreams/ROOT/distributed-written-proofs/B/kautz_length4/` at
  main `61488e05c9fe41984f483853f99e79f5715dc893`; those files are unchanged.
- The separate `../construction/STRICT_WINDOW_REPAIR.md` is a new structural
  bridge, but is **not required** for either upper-bound proof above.
- Internal independent review, finite computation, formalization, main
  integration, and historical novelty are separate statuses. No complete
  all-parameter Lean proof or external human peer review is asserted here.

The exact finite values and the exact limit remain undetermined.
