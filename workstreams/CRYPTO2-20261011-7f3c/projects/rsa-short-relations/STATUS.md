# RSA short-relation recovery: v1 research checkpoint

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

Evidence at reservation was source-only, with no lattice experiment or new
theorem. The reservation was published as remote commit
3b651069e690bc237faa6c608de895f532160736 before computation.

Current phase: restricted proof candidates and exact evidence frozen for
review. Major-result objective remains unmet. Core derivations were done
by this researcher; no independent reviewer has examined this RSA v1.

Actual mathematical evidence:
* PROOF-v1.md Proposition A: factor inheritance in I^m at the x-degree
  limit, for all integer e>=2; quantitative content-defect corollary.
* A proof that one precisely specified count/full-volume sufficient
  criterion cannot certify delta>=1/4. It is not an attack lower bound.
* PROOF-v1.md Proposition B: recovery from one certified quadratic
  relation under explicit size conditions, without an independence
  assumption. Finding that relation is not guaranteed.
* GENERAL-PROOF-v1.md: for any degree m in S(m,0), a primitive-at-e
  relation in I^m with 3^m M(H)<e^m and X^2Y>=e yields a short linear
  relation and exact key recovery. This covers t=0 only and retains its
  finite norm margin. It establishes no improved RSA exponent.

Actual checks: a separate standard-library integer checker validates
three finite BD basis certificates, exact RSA equations and primality,
synthetic quadratic and degree-3/12 recovery controls, 12 algebra cases,
3,660 count regressions and 12 rejected damaged/invalid inputs. Five
certificate files regenerate byte for byte. The general extractor reads
only public inputs and the supplied relation, not the expected secret or
the witness field. Synthetic inputs were built using disclosed test keys;
they are not relation-discovery or attack results. See RUN-RESULTS.json.

Blockers: positive y shifts create a leading-degree/ideal-order deficit;
the general proof does not handle it. Originality is unconfirmed, with
important full-text optimality literature gaps. No independent RSA review
or formalization has occurred. An interrupted 256-bit probe has no result.

Next: analyze that positive-y deficit with retained weighted discriminant
bounds, and require a usable recovery theorem with actual relation
existence before claiming progress on the attack exponent. HANDOFF.md
states the concrete step and stop condition. Do not repeat the t=0 proof
or expand the LLL sample count as a substitute.

Stop conditions: no new generic small-root identity counts as a major result;
failure of a finite LLL run does not refute an asymptotic attack; successful
toy keys do not establish a new exponent. Several substantively failed
routes must be logged and trigger a new decision, not sample growth.
