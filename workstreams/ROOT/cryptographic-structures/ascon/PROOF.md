# Exact two-round Ascon propagation for at most two active input columns

Complete written theorem with a finite binary-rank certificate, integrated from the frozen proof. It concerns the actual 320-bit permutation under uniform full-state inputs. Current replay and the independently reviewed frozen source versions are identified in ../VERIFICATION.json. Historical originality is unconfirmed; no Lean proof or AEAD attack is claimed.

## Definitions and standard convention

Let S be the 5-bit Ascon S-box of NIST SP 800-232, Section 3.3, acting
independently at the 64 bit positions of the five 64-bit words. In our
column integers, lane l has weight 2^l; this reverses the five bits relative
to NIST Table 6's display convention. The actual Boolean mapping is unchanged.
Word position j means integer bit 2^j. Let L be the standard linear layer
with right rotations (19,28), (61,39), (1,6), (10,17), (7,41), by lane.
Thus (LY)_(l,j)=Y_(l,j)+Y_(l,j+a_l)+Y_(l,j+b_l), indices modulo 64.

Fix arbitrary constants c0,c1, XORed in their proper positions before each
S layer. X is uniform on all 2^320 states; its paired state is X+A. For
fixed 320-bit differences A,B,C, let E(A,B,C) be the joint event

    S(X+c0)+S(X+A+c0)=B,
    S(L S(X+c0)+c1)+S(L S(X+A+c0)+c1)=C.

Here vector S means the parallel layer. The two full-round differences
are LB and LC; the final L is deterministic. Write

    D(a,b) = #{x in F2^5 : S(x)+S(x+a)=b},
    M(A,B,C) = product_j D(A_j,B_j)/32
               times product_j D((LB)_j,C_j)/32.

M is the local-DDT product, not a probability asserted a priori. An active
column is one nonzero 5-bit A_j, regardless of its bit weight.

## Theorem 1 (uniform validity and sharp column-count boundary)

For EVERY A supported on at most two columns, EVERY B,C and EVERY c0,c1,

    Pr[E(A,B,C)] = M(A,B,C).

This universal statement is false with three active columns. For constants
f0,e1 in lane 2, the explicit certificates below have respectively

    actual probability 2^-54, DDT product 2^-55;
    actual probability 0,     DDT product 2^-55.

Thus two is the largest input-column-count threshold for a universal
two-round product theorem. The theorem does not say that all triples fail,
that arbitrary multi-round Markov approximations are exact, or that the
zero-probability trail makes the full endpoint differential impossible.

## 1. Conditioning on the first layer

Put U=X+c0 and Y=S(U). Both U and Y are uniform, with independent columns,
because S is a permutation. Let I be the support of A. If some first local
transition has D(A_j,B_j)=0, then both sides of the theorem are zero.
Otherwise B vanishes outside I. Conditional on the first event:

- the Y_j, j outside I, remain independent uniform 5-bit words;
- they are independent of the active-column values Y_I;
- each active Y_j is uniform on the exact set
  F_j={S(x): S(x)+S(x+A_j)=B_j}.

No assertion that F_j is an affine space is needed. Indeed some size-eight
Ascon output fibers are not affine. The first-event probability is exactly
the first DDT product by independence before conditioning.

## 2. A sufficient surjectivity criterion (general fact)

Let J contain all active columns of LB. Restrict the map Y -> (LY)_J to
inputs with all columns in I set to zero; call it Q_(I,J). If Q_(I,J) is
onto all 5|J| output bits, then conditional on ANY fixed value of Y_I,
(LY)_J is jointly uniform. This follows because every image of an onto
linear map on uniform bits has equally many preimages. Adding the fixed
contribution of Y_I and the constant c1 preserves uniformity.

Consequently the columns at the input of the second S layer that carry
nonzero differences are independent and uniform after the first event.
Their specified transitions have the second DDT product as probability.
Inactive columns contribute either one or zero according as C_j=0 or not.
Multiplying by the first-event probability proves equality whenever Q is
onto. This uses actual conditional randomness, not a Markov assumption.

## 3. Exhaustive finite certificate for all supports of size at most two

Define

    T={0,45,36,3,25,63,58,54,47,57,23} subset Z/64Z,
    J=I+T.

Every possible LB with B supported on I is supported on J. Since L acts
independently by lane, Q is the direct sum of five binary maps. In lane l,
its matrix has rows indexed by J and columns by k outside I, with entry
one exactly when k is j, j+a_l, or j+b_l modulo 64.

Translation of I simultaneously permutes input and output positions and
preserves ranks. Every nonempty I of size at most two is a translate of
{0,d} for some d=0,...,63, where d=0 is the singleton case. The empty case
has only zero differences and is immediate. The certificate lists these
64 cases, J for each, and all five ranks. In each of the 320 binary blocks
the rank equals |J|. This establishes surjectivity for every support covered
by the theorem, without enumerating A, B, C or 320-bit states.

Reproduction: `python check.py` in this directory. The checker constructs
images of individual free input bits using physical right rotations and
performs column elimination with lowest-bit pivots. Discovery instead
constructs output equation rows and eliminates highest-bit pivots. All
support sets are regenerated; merely trusting listed ranks is insufficient.
The source and certificate hashes are recorded in ../provenance.json.
No corresponding cryptographic GitHub Release is claimed. This is a
finite, exact component of the proof, not a claim of an all-word-size theorem.

## 4. Three-column examples, and their exact probabilities

Use c0=f0 and c1=e1 in lane 2, the first two rounds of Ascon-p[12].
These are not the constants of Ascon-p[2], which uses the last two rounds.
In our lane-0-as-bit-0 column encoding set

    A_0=9, A_1=8, A_6=9;
    B_0=11, B_1=25, B_6=1;

all other A,B columns zero. The three first-layer output fibers are

    F_0={27,16}, F_1={27,11,2,18}, F_6={13,12}.

Their lane-2 bits are respectively 0,0,1. Therefore the lane-2 value at
position zero before the second S layer is forced:

    (LY+c1)_(2,0) = Y_(2,0)+Y_(2,1)+Y_(2,6)+1 = 0.

Let alpha=LB, and choose C_j=S(alpha_j)+S(0). All local transitions are
possible since zero is a witness. At j=0, alpha_0=11 and C_0=20. The entire
set of second-box inputs realizing this transition is {0,11}; both have
lane-2 bit zero. The first transition probability is (2*4*2)/32^3=2^-11.
The product of second-layer local probabilities is 2^-44.

For completeness, no uncounted dependency is hidden here. The active
second-column set is

    J={0,1,3,6,24,25,36,37,42,45,46,47,48,51,54,55,58}.

The five free-input projection ranks are 17,17,16,17,17. The only missing
coordinate is precisely lane 2 at position 0, whose free-input row is zero.
Hence all remaining 84 bits are jointly uniform independently of Y_I.
The restricted second-box transition at j=0 now has probability 2/16,
instead of 2/32, and all other factors are unchanged. The exact probability
is therefore 2^-11 * 2 * 2^-44 = 2^-54.

For the second example change only C_0 to

    S(4)+S(4+alpha_0)=21.

Its second-box preimages have lane-2 bit one, contrary to the forced zero.
This joint trail has probability zero. Its local DDT product is still
2^-55. The two JSON certificates store all 64 columns explicitly.

The checker obtains the fibers and second-box sets directly from NIST's
lookup table with explicit bit reversal; it does not use derivative
linearization or import discovery code. Its projection-rank calculation
then proves these counts over the full 320-bit domain, with no sampling.

## 5. General exact conditioning reduction (algorithmic scope only)

The Ascon S-box is quadratic, so for each alpha, D_alpha S(z) is affine.
For arbitrary A,B,C with nonempty first fibers, the second event is a
binary linear system H L Y = q, with the constant correctly evaluated as
q=C+D_alpha S(c1). Split the Y coordinates into active I and free Z.
Gaussian elimination on free-variable coefficients has rank r_Z and leaves
some consistency constraints K Y_I=t. For every active-fiber tuple
satisfying these constraints, exactly a fraction 2^-r_Z of the uniform
free variables solve the system. Thus exactly

    Pr[E] = 2^(-5|I|-r_Z) * #{y_I in product F_j : K y_I=t}.

This is a general elementary conditioning identity and is not advertised
as a new Gaussian elimination or counting algorithm. The supplied implementation applies
it only to bounded three-column cases. It can be exponential in |I| and
is not an efficient solution for arbitrary-round Ascon. Sections 2–4,
especially the full-width universal two-column boundary, are the concrete
result rather than a generic formula renamed as a cryptanalytic advance.

## Consequences and limits

Summing Theorem 1 over B gives exact equality of the entire two-round
differential distribution and its DDT-product composition for inputs with
at most two active columns. Therefore any linear functional of that
distribution, including any two-round DL correlation, is also exact under
that composition. This does not automatically validate the further
columnwise factorization used by a particular approximation program.

The original HNW 2026 Section 7.4 asks broadly for error measurement. Our
result is a precise bounded validity/failure certificate, not a solution
to that general future-work problem and not a refutation of its clearly
stated heuristic assumptions. No claim is made about their 5/6-round
distinguishers. Their paper also uses older Ascon initialization models;
we instead use NIST's fixed permutation and unconstrained uniform inputs.

No keys, chosen-plaintext attack, success probability, attack data/memory
cost or reduced security level is inferred. Mathematical correctness,
historical originality and practical cryptanalytic usefulness remain
separate assessments. See ../VERIFICATION.json for the current replay scope and a frozen link to
the independent AI review; see EXTENSION.md for the three-column result.
