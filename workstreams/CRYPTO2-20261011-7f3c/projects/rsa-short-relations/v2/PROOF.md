# Exact RSA recovery and a classical-scope obstruction

Classification: conditional arithmetic theorem and significance audit.
No new RSA attack; awaiting independent review.

For integers e,N,k,s,d,r,t,u,X,Y,T assume e>0, 0<k<=X, r>0,
Y>=1, -Y<=s<=Y, rY<=T, |t|<=T, 3XT<e,
1+k(N-s)=ed, eu=rN+t and gcd(k,d)=1.
Then, writing g=gcd(r,u)>0, r/g=k and u/g=d.
If also s>=1, then 3k^2Y<e, 0<=Nk-ed, and 2k(Nk-ed)<e.
These are the integer conclusions in RSAScopeAudit.short_relation_scope;
signed-s lifting is separately exposed by short_lift_recovers.

Proof. Direct cancellation gives
    k(rs+t)-r = e(uk-rd).
Since r<=rY<=T and X>=1, the absolute value on the left is at most
2kT+r<=2XT+T<=3XT<e. It is an integer multiple of e, hence zero.
Thus uk=rd. Coprimality gives k|r, so r=ak for a>0; cancelling k yields
u=ad. Therefore gcd(r,u)=a and the quotient formulas follow.
In particular r>=k and 3k^2Y<=3XrY<=3XT<e.
For s>=1, Nk-ed=ks-1>=0 and
    2k(Nk-ed)=2k(ks-1)<2k^2Y<3k^2Y<e.
Every operation is exact. Lean checks this integer argument.

For ordinary RSA, N=pq, s=p+q-1 and ed=1+k phi(N).
Dividing the last strict inequality by positive 2e k^2 yields
    |N/e-d/k| < 1/(2k^2).
The classical Legendre theorem puts reduced d/k among the convergents
of N/e. Enumerate them by the Euclidean algorithm. For each d,k with
k>0 and k|(ed-1), put phi=(ed-1)/k and test whether
z^2-(N-phi+1)z+N has positive integral roots multiplying to N.
The true key passes. This takes polynomial time in the input bit length
and does not require H or a short relation as input.

The classical mechanism is described in Boneh, Twenty Years of Attacks
on the RSA Cryptosystem (1999), Section 3, Theorem 2:
https://crypto.stanford.edu/~dabo/pubs/papers/RSA-survey.pdf .
That source uses k/d against e/N; we use the reciprocal approximation.
We do not claim every parameter here meets the exact sufficient
d<N^(1/4)/3 inequality in Wiener's printed theorem.

Formalization boundary: Legendre's theorem, polynomial-factor existence,
Mahler measure and the discriminant estimates in GENERAL-PROOF-v1.md
are NOT formalized by this artifact. That full theorem remains a written
proof candidate. The short linear witness is an explicit Lean hypothesis,
not an added axiom. Do not call this a Lean proof of the high-degree theorem.

Decision: the t=0 theorem's conclusion lies within classical
continued-fraction key recovery. It cannot expand that attack's reach.
This meets the earlier RSA stopping condition. Keep the structural proof
and checked scope audit, defer expensive remaining formalization, and
shift effort to SHA-256. Nothing here proves the positive-y-shift case.
