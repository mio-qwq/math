# Exact finite-certificate transfer by independent alphabet sampling

GP2-20261012, 2026-10-13. This note proves an all-alphabet bridge for
finite strict-code certificates. It does not certify the unresolved
six-index optimization or improve the current lambda_4 interval.

## 1. A quantitative convergent hierarchy

For each integer n>=4, let I_n be the ordered four-tuples of distinct
elements of [n]={0,...,n-1}. Write (n)_k=n(n-1)...(n-k+1). Let M_n be
the maximum size of a strict code D contained in I_n. Strictness is tested
on **all** words in [n]^8, including repeated indices, not only on
injective eight-letter words. This distinction is essential.

**Theorem 1.** For every finite alphabet A, every probability distribution
mu on A, and every strict C subset A^4 of density p,

    p <= M_n/(n)_4,                 for every n>=4.     (1)

Consequently, using the accepted equality between lambda_4 and the
supremum of weighted strict-code densities,

    M_n/n^4 <= lambda_4 <= rho_n := M_n/(n)_4,
    rho_N <= rho_n                  for N>=n>=4,
    0 <= rho_n-lambda_4
       <= [1-(n)_4/n^4]/4 <= 3/(2n).                   (2)

In particular lambda_4=inf_(n>=4) rho_n. This is an exact convergent
certificate target, not an assertion that a fixed n determines lambda_4.

**Proof.** Choose independent letters X_0,...,X_(n-1) with law mu and
form the index code

    D_X={ (i,j,k,l) in I_n : (X_i,X_j,X_k,X_l) in C }.

The full inverse image of C under the alphabet map i->X_i is strict:
any forbidden index word would map to a forbidden word of C with the
same three selected **positions**. Deleting all noninjective index
four-tuples preserves strictness. Hence |D_X|<=M_n pointwise.
For each fixed tuple in I_n, its four images are independent with law mu,
even though their actual values may coincide. Thus

    E |D_X|=(n)_4 p.

Taking expectations proves (1), with no collision correction. Zero letter
weights and noninjective sampled alphabet maps are included.

A maximizing D on n letters has uniform product density M_n/n^4, so it
is a legitimate weighted strict template and gives the left inequality
in (2). The known strict-to-Kautz lift and repair identify the common
supremum with the original lambda_4; the finite GP number is not identified
with M_n. For monotonicity, restrict an optimal N-index code to a uniform
n-element subset. Each of its words survives with probability (n)_4/(N)_4.
Taking expectations yields rho_N<=rho_n.

Each orbit of I_n under cyclic rotation has exactly four elements, and
strictness permits at most one of them. Thus rho_n<=1/4. The two bounds
on lambda_4 give

    rho_n-lambda_4 <= rho_n[1-(n)_4/n^4]
                  <= [1-(n)_4/n^4]/4.

Finally 1-(n)_4/n^4 is the collision probability of four independent
uniform n-valued draws, at most 6/n by the six-pair union bound. QED.

For example, a proved M_6<=89 would imply lambda_4<=89/360, a substantive
improvement. **No such certificate has been obtained.** A timeout in the
discovery scripts says nothing about whether M_6 is 90, 89 or smaller.

More generally an accepted certificate M_n<=U_n gives, by the original
strict-window repair, for every m>=3,

    gp(Ka(m,4)) <= floor[U_n m^4/(n)_4]+73m^3.

U_n must bound **all** strict index codes, including every compatible
labelling. The fixed six-letter 41/216 model does not have this scope.

## 2. Transfer of joint motif inequalities

A finite motif on k labelled indices is any Boolean function of selected
word indicators for specified ordered four-tuples of **distinct indices**
among those k indices. The k indices can be shared between different
words. Let Phi(C,mu) be its probability under k independent mu-letters.
Actual letters are allowed to repeat. For D subset I_n, let N_Phi(D)
count injections of the k labelled indices into [n] for which that
Boolean function is true.

**Theorem 2.** For every such motif with k<=n,

    E N_Phi(D_X) = (n)_k Phi(C,mu).                     (3)

Therefore every pointwise inequality on all strict D subset I_n of the
form

    sum_j c_j N_(Phi_j)(D)/(n)_(k_j) <= B              (4)

transfers to the all-alphabet product-weight inequality

    sum_j c_j Phi_j(C,mu) <= B.                        (5)

The coefficients c_j can be arbitrary real numbers. Proof: for a fixed
injection the sampled letters on its k indices are independent, and
every queried four-tuple remains in I_n. Its truth value agrees exactly
with the corresponding query to C. Sum over injections and use linearity
of expectation; (4) holds for every sampled D_X. QED.

The selected-word motif has k=4 and expectation p. The adjacent-pair
motif has k=5, querying positions 0123 and 1234, and expectation a(C).
The empty-rotation motif has k=4 and expectation 1-4p. Thus a certificate
can retain bridge adjacency and rotation information at the same time.
Overlapping words cause no independence assumption between their truth
values; only the underlying indexed letters are independent.

Limitations: a queried word with a repeated **index** is always deleted
from D_X, so (3) is not valid for that query without changing the model.
The nonlinear deletion functional d(C), support-existence predicates, and
canonical levels recomputed from D_X also do not automatically satisfy
(3). Label functions may be sampled as extra data, but any resulting
certificate must explicitly quantify over their compatible assignments.

## 3. A complete five-index certificate and a real limitation

The certificate accompanying this note contains the following strict code
on five letters (every word uses four distinct letters):

    0123 0124 0132 0134 0213 0214 0231 0234 0241 0243
    0312 0314 0321 0324 0412 0413 0431 0432 1034 1042
    1234 1324 1423 1432 2014 2034 2134 3014 3042 3124

Its 30 words occupy all 30 injective rotation orbits. The checker verifies
strictness both by all 5^8 literal words and by the independent five-step
triple-state dynamic program. The rotation upper bound then proves

    M_5=30, rho_5=1/4.

Restriction to any four letters retains the six rotation representatives,
so M_4=6 and rho_4=1/4 as well. This code contains 0123 and 1234, an
adjacent selected pair using five distinct indices. Hence for every c>0
the proposed pointwise five-index inequality

    |D|/120 + c N_adj(D)/120 <= 1/4

is false. This rules out that particular order-five certificate form;
it does **not** disprove an all-alphabet inequality p+c a<=1/4 obtained
by a different argument or larger/augmented certificate.

The code was found by a solver, but its feasibility and exact optimality
here depend only on the literal strictness checker and the orbit proof.
No floating solver bound is an accepted proof. A six-index MILP attempt
and a separate integer search for full rotation completion both timed out.
They are recorded only as bounded discovery attempts, with no inference
of impossibility and no claim of an exact six-index extremum.

## 4. Original graph checks and provenance

The checker reconstructs the original directed Ka(5,4) from its 320 valid
words and its shift-and-append arcs. BFS distances test every ordered
triple of distinct vertices from the 30-word certificate. It checks distance
additivity, not mutual visibility. This is a finite definition check; the
all-m bridge in (2) uses the already accepted strict lift and O(m^3) repair.

Induced-subalphabet averaging, alphabet blow-ups and injective sampling
are standard extremal arguments. This workstream already used
subalphabet monotonicity for the original GP density limit, and classical
comma-free work already uses rotation counts and alphabet blow-ups; see
[Golomb--Gordon--Welch (1958)](https://doi.org/10.4153/CJM-1958-023-9) and
the inherited source review. These ideas are not claimed newly invented.
The present deliverable makes the strict injective model, exact weighted
motif transfer, quantitative error and five-index obstruction explicit.
Historical priority of the particular formulation or finite witness is
unconfirmed. No Lean proof or complete finite optimization is claimed.

The next useful step is a structural or exactly checkable inequality on
the six-index compatibility model, retaining mixed pair classes or triple
interfaces. Increasing a floating solver's timeout or accepting its dual
bound would not supply the required certificate.
