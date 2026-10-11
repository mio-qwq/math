# Failed routes and actual limits

1. **Direct modular projection after factoring.** The original hope was
   that a common integer component of several short relations might yield
   a useful univariate equation after substituting y=N+1/x modulo e.
   Proposition A shows the projection is identically zero for every
   positive-x-degree factor of a primitive-at-e relation at the degree
   limit. Corollary A2 quantifies the content needed to escape. Stop this
   version of the route; do not simply try more such factorizations.
2. **Number of vectors plus Newton support.** The exact sufficient
   criterion based on full determinant and prefix covolume >=1 cannot
   cross delta=1/4 for any m>=1,t>=0. The proof is the nonnegative
   polynomial case split in PROOF-v1.md, not the finite regression grid.
   Stronger prefix-volume or arithmetic arguments were not ruled out.
3. **Bare discriminant/height estimate, subsequently improved.** A crude
   estimate discarded the x-weights and left a positive exponent in the
   target range. Keeping those weights fixed this loss: Proposition B
   settles the quadratic case, and GENERAL-PROOF-v1.md handles arbitrary
   degree for t=0 with a 3^m norm margin. The failed estimate is retained
   to explain the change of mechanism; it is not a no-go theorem for
   discriminant methods. The positive-y-shift case remains unresolved.
4. **Finite LLL diagnostics.** The 25- and 35-dimensional saved bases,
   using d near N^(13/50), have respectively 6 and 15 relations that
   actually vanish, but zero relations passing the prescribed HG norm
   test. These are isolated, small keys. They prove neither an attack
   exponent nor failure of the lattice or of root recovery. A dimension-6
   control in the Wiener range has three certified relations and a common
   bilinear curve from which k,d are exactly recovered. A zero resultant
   cannot be counted as a counterexample to the attack.
5. **Interrupted larger diagnostic.** A nominal 256-bit m=8,t=2 run was
   manually interrupted, exit 130, before it saved a certificate. That
   version had no progress checkpoints, so we cannot attribute the delay
   to lattice reduction versus symbolic factorization. It supplies no
   mathematical evidence. Progress logging, a 45-second replay timeout,
   and a skip-factor option were added. Do not restart it by default.

No SHA-256/AES claim follows from any of these results. No standard RSA
modulus was attacked. All keys used in diagnostics are generated locally
and are disclosed test inputs. No asymptotic or practical attack improvement
is currently established.
