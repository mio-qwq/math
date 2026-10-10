# Independent audit of proof sketch

Scope: supplied proof sketch for n=qd+a>d, q>=1 and 2<=a<=d. This is not yet an audit of a frozen manuscript and makes no novelty claim.

## Verdict

The proposed formula gp(Circ(n,{1,...,d}))=max(a,floor(d/a)+1) follows from the sketch after correcting one overly strong statement. No substantive obstruction found.

## Required correction

The claim “the triple {0,xi,xj} violates general position iff ri>=rj” is false if “triple” means any ordering. For n=8,d=3,a=2, the triple {0,1,3} has increasing remainders but D(1,3)+D(3,0)=1+2=3=D(1,0).

Replace it with: “D(0,xi)+D(xi,xj)=D(0,xj) iff ri>=rj.” This is enough to prove strictly increasing remainders for every GP set containing 0.

## Checked algebra

Use xi=ki*d+ri, with 1<=ri<=d for i>0, and k0=r0=0. Under increasing remainders, for i<j, letting h=rj-ri:

- D(xi,xj)=kj-ki+1=D(ri,rj)+kj-ki.
- D(xj,xi)=q+ki-kj+ceil((a-h)/d)=D(rj,ri)+ki-kj.

Thus the potential identity holds for all ordered distinct pairs. Every geodesic equality is preserved in both directions. The compressed set is injective, lies in [0,d], and is GP.

For compressed x<y<z, put u=y-x, v=z-y, s=u+v. Forward distances are all 1. Backward distances are q+1{gap<a}. For the two potentially geodesic ordered triples:

- D(y,z)+D(z,x)-D(y,x)=1+1{s<a}-1{u<a}.
- D(z,x)+D(x,y)-D(z,y)=1+1{s<a}-1{v<a}.

The other four orderings have positive defect. In particular the reverse-chain defect is q+1{u<a}+1{v<a}-1{s<a}, positive because if s<a both u,v<a, and otherwise q>=1.

Consequently a compressed triple is GP iff s<a or (u>=a and v>=a). Equality boundaries s=a, u=a and v=a are covered by the strict indicators.

If the compressed set has span<a, its cardinality is at most a. Otherwise, with at least three vertices, the first, second and last force the first gap>=a. Each triple of the first vertex and two successive later vertices then has span>=a and forces their successive gap>=a. Every gap is at least a, giving cardinality at most floor(d/a)+1. Two-element sets satisfy the bound automatically.

Both claimed lower examples obey the triple criterion: {0,...,a-1} has every triple span<a, and {0,a,...,floor(d/a)*a} has every gap>=a.

The convention a=d, used when n is divisible by d, is consistent throughout. No use of a nonzero standard remainder is needed.

## Independent computation

The accompanying stdlib script constructs directed distances by BFS, generates forbidden triples by all six permutations, and enumerates all GP subsets containing 0 by exact backtracking. Translation invariance makes this enough for the maximum. It also verifies the distance formula, increasing-remainder property, projection identity and GP preservation for every enumerated set, and the triple criterion for every triple in [0,d]. Results are recorded separately when complete.
