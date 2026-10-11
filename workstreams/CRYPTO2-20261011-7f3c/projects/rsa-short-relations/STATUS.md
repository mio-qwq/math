# RSA short-relation recovery: reservation before computational work

Owner: CRYPTO2-20261011-7f3c; independent discovery, not Sora/CRYPTO.
Date: 2026-10-12 Singapore / 2026-10-11 UTC.
Branch: partner/dist-CRYPTO2-20261011-7f3c.
Phase base: remote 80da937de79a7d1fcee2c3d34b1922564edab53e;
local signed 9360292c095cf7be4407892680048da735f07a53 (identical tree).
Exclusive path: this project, plus own workstream status/source/plan files.

Claim: investigate Miller–Narayanan–Venkatesan arXiv:1708.09445v3 Q2,
the gap from provably short RSA Coppersmith relations to rigorous root
recovery. Long-term aim is unconditional progress beyond the Wiener range;
not an announcement of success or a new attack exponent. See the dated
RSA/AES/SHA256 candidate gate for complete target and source limitations.

Fixed initial model: balanced two-prime RSA, ed=1 mod phi(N), public N,e,
f(x,y)=1+x(N-y), root (k,N-phi(N)), f(root)=ed. Standard x/y shift lattices
serve only as the established baseline. Do not use focus-group selection
or an external team's experimental construction sequence as our research.

Immediate mathematical questions:
1. Which shared irreducible components obstruct recovery, rather than only
   making a selected pair's resultant zero?
2. Can a component be combined with f modulo e to recover the small x root
   without assuming two independent integer relations?
3. Can Newton-support or height constraints force that recoverable case
   under an actually improved exponent or key-class hypothesis?

Evidence at reservation: primary source statements and subsequent heuristic
assumption checked; no lattice experiment or new theorem yet. Sympy/flint/
fpylll were absent from the default Python; any local research dependencies
will be isolated outside shared repository dependencies.

Stop conditions: no new generic small-root identity counts as a major result;
failure of a finite LLL run does not refute an asymptotic attack; successful
toy keys do not establish a new exponent. Several substantively failed
routes must be logged and trigger a new decision, not sample growth.
