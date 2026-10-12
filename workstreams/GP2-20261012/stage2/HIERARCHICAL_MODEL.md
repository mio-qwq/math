# A marked-objective-preserving hierarchy: 14 triple profiles, 9 pair types, 5 letter types

GP2-20261012, stage 2. Complete written argument; **new candidate awaiting independent review**. No all-parameter Lean compilation or claim of historical priority.

## 1. Object, dependency, and attribution

For a finite nonempty alphabet A, a strict code C contained in A^4 has at most two selected occurrences among the five four-letter windows of **every** word in A^8. Repetitions count as separate occurrences. This is not the definition of directed general position at finite alphabet size. The stage-one repair theorem places a strict subset inside every original Ka(m,4) GP set after deletion of at most 73m^3 points. Its separate blow-up/averaging argument equates the limiting GP density with the supremum of weighted strict-code densities over finite alphabets.

The fourteen-profile representation below is inherited from `../construction/FOURTEEN_STATE_REDUCTION.md`. The present increment is the explicit threshold hierarchy, objective-preserving domain reduction, and localization of the adjacency branch. The generic incoming/outgoing-rectangle mechanism is **classical**, not a new general theorem: Foniok and Tardif, *Digraph functors which admit both left and right adjoints*, arXiv:1304.2204v2, Definition 3.1 and Proposition 3.2, describe the right adjoint of the arc-graph construction using complete directed rectangles. We specialize it and give elementary formulas and proofs; objective domination for the designated marked arcs must additionally be verified.

## 2. The inherited marked target, restated

Set

    P = {(a,b): 1 <= a <= 4, a+1 <= b <= 6}.

For p=(a,b), put h_t(p)=1_{a<=t}+1_{b<=t}, 0<=t<=5. An arc p -> q=(c,d) is allowed when

    c <= a+1, and (b >= 5 or d <= b+1).                     (2.1)

It is marked when, additionally,

    c=1, b>=5, d<=a+1.                                    (2.2)

These are respectively equivalent to h_t(q)>=h_(t-1)(p) and h_t(q)>=h_(t-1)(p)+1 for every t=1,...,5. Hence an allowed five-arc walk has at most two marked arcs.

An admissible assignment gamma:A^3 -> P sends every shift xyz -> yzt to an allowed arc. The resulting marked code C_gamma is strict. Conversely every strict code C is contained in such a code. For nonempty C, let F_t(s) be the maximum selected count on a t-arc full-shift walk ending at triple s. Then F_0=0; each increment is 0 or 1; F_5<=2; and F_4>=1, since one selected arc can be followed by the three letters of any target triple. The two hitting times of levels one and two (six if the second is not reached) give gamma(s) in P. Appending one arc proves (2.1) and, for a selected arc, (2.2). For empty C use constant gamma=(4,6). This proves the representation needed here, without assuming independence of the code.

## 3. Nine exact pair rectangles

Define

    Q = {(alpha,beta): 1<=alpha<=3, alpha+1<=beta<=5}.
    I_q = {(a,b) in P: a>=alpha, b>=beta},
    O_q = {(a,b) in P: a<=alpha+1, b<=beta+1}.

Every I_q x O_q is a nonempty complete allowed rectangle. Conversely let I x O be a nonempty complete allowed rectangle. With

    alpha = min(3, min_{(a,b) in I} a),
    beta  = min(5, min_{(a,b) in I} b),

we have q=(alpha,beta) in Q, I contained in I_q, and O contained in O_q. Indeed the strongest first-hit constraint is at the minimum a; clamping 4 to 3 changes no destination constraint because destination first coordinates are at most 4. The strongest second-hit constraint is at the minimum b if it is at most 4, while b>=5 imposes no second-hit restriction; clamping to 5 expresses both cases. Also beta>=alpha+1.

All nine displayed rectangles are maximal: the common allowed successors of I_q are exactly O_q, and the common allowed predecessors of O_q are exactly I_q. These equalities follow by testing the extreme threshold profiles and are also exhaustively checked against the 138 allowed target arcs. Thus they are exactly the maximal nonempty complete rectangles; arbitrary subsets need not be retained as new types.

The derived graph on Q is

    q -> q' iff O_q intersect I_q' is nonempty
             iff alpha'<=alpha+1 and beta'<=beta+1.        (3.1)

For sufficiency, q' itself is a profile in the intersection; necessity is coordinatewise.

Given admissible gamma, apply the envelope above to the nonempty set of incoming images {gamma(xbc):x in A} at each pair bc. It gives kappa:A^2 -> Q with

    gamma(abc) in D(kappa(ab),kappa(bc)),
    D(q,q') = O_q intersect I_q'.                         (3.2)

Conversely any such pair/triple choices yield an admissible gamma: the images gamma(abc) and gamma(bcd) lie respectively in I_kappa(bc) and O_kappa(bc), a complete rectangle. This retains the actual chosen gamma, not merely existence of some homomorphism.

## 4. Five exact letter rectangles

For the derived nine-state graph define

    R = {(s,t): 1<=s<=2, s+1<=t<=4},
    J_r = {(alpha,beta) in Q: alpha>=s, beta>=t},
    N_r = {(alpha,beta) in Q: alpha<=s+1, beta<=t+1}.

Exactly the same envelope proof, now with clamps 2 and 4, gives precisely these five maximal nonempty rectangles. Its derived graph has

    r -> r' iff s'<=s+1 and t'<=t+1.                     (4.1)

In particular kappa has a representation by eta:A -> R with independent pair choices

    kappa(ab) in N_eta(a) intersect J_eta(b).             (4.2)

Here “independent choices” means that, after eta is fixed, any choices in the specified pair domains are feasible together. Once kappa is fixed, any gamma choices in (3.2) are also feasible together. The marked **objective** still couples consecutive triples; this is not a decoupled optimization problem.

List R as

    r0=(1,2), r1=(1,3), r2=(1,4), r3=(2,3), r4=(2,4).

Only the arcs r0->r2 and r0->r4 are absent among its 25 ordered pairs, including loops. Since every ordered pair of alphabet letters occurs, eta(A) must be contained in one of

    {r0,r1,r3},                {r1,r2,r3,r4}.              (4.3)

It is incorrect to conclude that an optimal code is a three- or four-block substitution: kappa can distinguish letters of the same eta type, and gamma can still distinguish triples with identical eta patterns. The alphabet remains unrestricted.

## 5. At most three active profiles, with the marked objective preserved

Fix a nonempty D(q,q'), with q=(alpha,beta), q'=(alpha',beta'). Retain the following applicable profiles:

    S=(alpha+1,beta+1),  if beta>=4;                       source
    T=(1,beta'),        if alpha'=1 and beta'<=4;         terminal
    B=(1,5),            if alpha'=1 and beta>=4.          bridge

If none is applicable, retain the lexicographically first element of D. All displayed profiles lie in D: this follows from (3.1), alpha<beta, and alpha'<beta'. There are at most three of them.

For profiles p,q, say q dominates p when every marked arc out of p is also a marked arc out of q, and every marked arc into p is also a marked arc into q (tested against **all** fourteen other profiles). Every p in D is dominated by one of the retained profiles:

* If p is a pure source (second coordinate >=5, but p is not (1,5)), it has no incoming marked arc, and its outgoing marked destinations have first coordinate one and second coordinate at most p_first+1. S has at least that first coordinate and dominates p. This includes (1,6), whose only possible outgoing marked destination is (1,2).
* A pure terminal is (1,b) with 2<=b<=4. It has no outgoing marked arc; decreasing b to the minimum permitted beta' enlarges its set of incoming marked sources. T dominates it.
* The only profile with both incoming and outgoing marked arcs is (1,5). It is retained as B whenever present in D.
* All remaining profiles have no marked incidence. Any retained element dominates them; if there is no active profile, the retained inert element does so.

Replace each gamma(abc) by such a dominating retained profile in its **own** unchanged domain. Feasibility is automatic by (3.2). Every previously marked arc remains marked: first use row domination at its source and then column domination at its destination. Therefore the new marked code contains the old one, and **every nonnegative product-weight objective is nondecreasing**.

**Theorem.** For every finite alphabet and every nonnegative letter-weight distribution, the maximum strict-code density equals the maximum marked density over the hierarchical choices eta, kappa, gamma above, with at most three retained choices at each triple. Taking the supremum over all finite weighted alphabets gives exactly the stage-one variational problem for lambda_4.

Proof: every hierarchical code is strict by Section 2. Every strict code first embeds into an admissible marked code, then obtains the hierarchy, then enlarges by the domination step. Apply this to an optimum (which exists for each fixed finite alphabet). An inclusion-maximal strict code is represented exactly, since none of these strict enlargements can be proper. No assertion of a globally bounded optimizing alphabet or of attainment of the supremum is made.

## 6. Where adjacency can occur

If p->q->r are two consecutive marked arcs, the target rules force

    p in {(4,5),(4,6)}, q=(1,5), r=(1,2).                 (6.1)

Indeed q has incoming and outgoing marked incidence, hence q=(1,5); the first arc forces p_first>=4, and the second forces r=(1,2).

Suppose abcd and bcde are both in a hierarchical marked code. The first coordinate four of gamma(abc) forces the first coordinate of kappa(ab) to be three, which in turn forces eta(a) to have first coordinate two. The profile gamma(cde)=(1,2) forces kappa(de)=(1,2), and hence eta(e)=r0. The existence of r0 excludes r2,r4 everywhere by (4.3). Consequently

    eta(A) contained in {r0,r1,r3}, eta(a)=r3, eta(e)=r0. (6.2)

Thus all adjacency lies in the three-type branch and has this directed endpoint pattern. The result does **not** discard that branch and does not prove independent codes are extremal. The strict binary code {0001,0011} is an explicit retained adjacency example.

## 7. Verification scope

`verify_stage2.py` independently rebuilds allowed/marked arcs from the five height inequalities, enumerates all nonempty-subset rectangle closures (14 then 9 vertices), checks every one of the 64 pair domains and every marked row/column domination, and checks the letter-branch implication on all compatible length-five configurations. It also checks finite full-shift codes and actual Kautz adjacency/BFS instances. These are finite semantic checks supporting the all-alphabet proof, not a numerical solution or a new independent-agent review.
