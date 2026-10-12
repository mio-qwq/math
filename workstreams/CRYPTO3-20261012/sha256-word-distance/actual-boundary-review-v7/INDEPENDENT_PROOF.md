# Independent high-power obstruction for the actual sigma0 anti-cycle

This proof and its checker are reconstructed before reading the new
author boundary proof or certificate. The reviewer retains distinct
notation: **a=d26=d42**, **b=d18=d34=d11** on support12. The parent
reports that the author's a,b names are reversed; a later comparison
will state that mapping explicitly.

## Original actual-pair bridge

With the exact frozen support12 zero pattern, original recurrence rows
18 and34 give d18=d11=d34. Row42 gives d42=d26. Row33 is
`0=d26+F18`, and row41 is `0=d34+F26`. Thus the actual pairs at
18 and26 obey

    (dP,FP)=(b,-a), (dQ,FQ)=(a,-b).

These are constraints on the same actual word members in each pair,
not independent choices of additive derivatives. All arithmetic is
modulo N=2^32. The two members a,b are nonzero on that support.

## A signed power in either member is impossible at bits22..31

It is enough to treat b=D=+2^k for 22<=k<=31. Swapping the members
of **both** pairs negates a,b and every derivative, preserving the
anti-cycle. Interchanging the two actual pairs also preserves its form,
so this one positive case covers both signs and either a or b.

Adding 2^k modulo 2^32 changes a contiguous input XOR interval

    alpha_e = sum(2^j : k<=j<=e), k<=e<=31.

The e=31 mask includes both stopping at bit31 and overflowing it;
bit31 is not assumed to be zero. Lower k input bits stay arbitrary
but do not change. These are all possible masks.

For f=ROTR7 XOR ROTR18 XOR SHR3, and an input mask confined to
positions k..31 with k>=22, every changed output position is at least
k-18. In detail the output positions from the three terms lie in
`k-7..24`, `k-18..13`, and `k-3..28`. Therefore the actual F_P is
divisible by 2^(k-18). Since F_P=-a, a has the same divisibility.
The actual Q input members must therefore share their low k-18 bits.

But F_Q=-D. Reversing its two output words shows that their XOR mask
is one of the same contiguous intervals alpha_e. The original binary
linear map f is invertible: the checker reconstructs its full32 rows
and a two-sided inverse, verifying both compositions on all32 basis
vectors. Thus the Q **input** XOR mask is exactly f^{-1}(alpha_e).

For every k=22..31 and every e=k..31, that inverse mask has a nonzero
bit strictly below k-18. All55 cases are evaluated from the exact
inverse rows in `check_independent.py`. This contradicts the common
low k-18 input bits forced by a. Hence b cannot be the given signed
power. The two symmetries prove the claim for either member.

No ordinary addition linearity of f is used. The only linearity is over
XOR masks, and actual additive divisibility is turned into equality of
low input/output bits. Both inverse maps act on complete original
32-bit words. No solver or enumeration of arbitrary messages is needed.

This theorem is a necessary local restriction. It excludes neither the
whole anti-cycle at other differences nor an entire SHA-256 support,
and says nothing about existence of a complete 13-word message pair.
