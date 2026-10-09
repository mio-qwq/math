# An asymmetric cubic-character witness from an actual MUB triplet

The concrete matrix construction and its normalized three-basis Gram/overlap
conditions are now proved in [Lean](proof/FourierAsymmetricTriplet.lean).
The closed endpoint constructs the specified raw data; it does not assume
the matrix Gram, companion or character assertions. Source-specific
[compiler and axiom evidence](proof/FourierAsymmetricTriplet.verification.json)
records the actual checks.

The cubic-character product condition in Conjecture 2 of
[Matolcsi, Matszangosz, Varga and Weiner](https://arxiv.org/html/2503.14752v2)
allows one factor to be nonzero. The following exact example shows that
replacing the product condition by the vanishing of both factors, even at a
single prescribed balanced partition, would be false. The Fourier companion
construction is classical: see
[Szollosi, Section 4 and Proposition 4.2](https://arxiv.org/pdf/0811.3930v2).
Historical novelty of this particular numerical example is not established.

## Actual matrices and normalization

Let omega be a primitive cube root of unity and let
F[r,k]=omega^(-rk), with r,k in Z/3. Thus F*F=FF*=3I.
Write C(a)[r,s]=a[r-s] and set

    a=(1,i,1), b=(1,-1,-1),
    A=C(a), B=C(b), Hc=[A B; B* -A*].

The Fourier modes of A and B are respectively

    alpha=(2+i,(i-1)omega,(i-1)omega^2), beta=(-1,2,2).

Their squared moduli are (5,2,2) and (1,4,4). Their coordinatewise sum is
6, and the circulant blocks and their adjoints commute. Expanding both Gram
products therefore gives Hc*Hc=Hc Hc*=6I. Every entry has modulus one.

Define the three unit phases and a second actual matrix by

    x0=(1-2i)/sqrt(5),
    x1=(-1-i)omega/sqrt(2), x2=(-1-i)omega^2/sqrt(2),
    X=diag(x), K=[F F; F X* -F X*].

Block multiplication gives K*K=KK*=6I and all its entries have modulus
one. To check the complete companion condition, put r_k=|alpha_k| and
t_k=|beta_k|. Then x_k=i alpha_k beta_k/(r_k t_k), with r_k,t_k>0.
The four blocks of Hc*K are Fourier matrices multiplied columnwise by

    star(alpha)+beta star(x), star(alpha)-beta star(x),
    star(beta)-alpha star(x), star(beta)+alpha star(x).

The two types of scalar factor have squared moduli
r_k^2+t_k^2=6, since

    star(alpha_k) +/- beta_k star(x_k)
      =star(alpha_k)(1 -/+ i t_k/r_k),
    star(beta_k) +/- alpha_k star(x_k)
      =star(beta_k)(1 -/+ i r_k/t_k).

Consequently all 36 entries of Hc*K have squared modulus 6. This checks
all six mutually orthogonal companion columns, rather than only individual
unbiased vectors.

Use the six labels (inl0,inl1,inl2,inr0,inr1,inr2). Let Q be the column
permutation taking the columns of K in the order

    (inl0,inr0,inl1,inr1,inl2,inr2),

and set H=KQ. It follows that (I,H/sqrt(6),Hc/sqrt(6)) is an actual MUB
triplet: all three basis Gram matrices are I, and every entry of each
transition between distinct bases has squared modulus 1/6.

## The same displayed partition on H and H*

For eta=(1,1,1,-1,-1,-1), define

    g_M(n eta)=sum_j ((product_top_rows M[r,j]) /
                     (product_bottom_rows M[r,j]))^n.

The entries in the paired columns (inl k,inr k) of K differ by a minus
sign on its three bottom rows. Their balanced ratios are therefore
negatives. Their odd powers cancel, and a column permutation does not
change the sum. Thus g_H(eta)=g_H(3eta)=0.

In H*, the same displayed first three rows correspond to the original K
columns T={inl0,inr0,inl1}. Their sign sums by Fourier column index are
(2,0,-2). Set s=(x0/x2)^2. The six balanced ratios of H* are

    omega^(-4r), -s omega^(-4r)  (r=0,1,2).

The first powers sum to zero because the three Fourier phases sum to
zero. The cubes sum to 3(1-s^3). Direct exact arithmetic gives

    x0^6=(117-44i)/125, x2^6=-i,
    (x0/x2)^6=(44+117i)/125,
    g_H*(3eta)=(243-351i)/125,
    |g_H*(3eta)|^2=1458/125>0.

The partition on each side is the same displayed eta. It is not a
comparison of two unrelated labels disguised as that statement. The
original conjectured cubic product is still zero in this example.

## Consequence and boundary

The already proved displayed four-circulant theorem forces both fixed
cubic characters to vanish. Transformations by monomial matrices that
preserve the two row triples and the two column triples preserve their
zero/nonzero status. Hence this H cannot be transformed into four
circulant blocks while preserving these fixed triples. With the written
fixed-partition witness equivalence, it also excludes a spectral companion
whose observable satisfies both prescribed anticommutation equations at
these triples, regardless of which companion is chosen.

This conclusion is restricted to the specified partition. It does not
exclude witnesses at other partitions, classify all triplets, or disprove
the published cubic-product conjecture. Any published formalization record
must say which actual matrix, companion and character implications were
compiled; the written witness equivalence does not automatically become a
Lean theorem by importing a scalar calculation.

## Exact formal scope and replay

The main source has fifteen audited interfaces. The concrete root helper
has four and the generic normalization bridge two. These are interface
counts, not counts of independent mathematical discoveries. The final
three new sources were compiled at the recorded hashes with Lean 4.34.1
and Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612, with zero errors,
warnings or internal PANIC diagnostics, and only propext, Classical.choice
and Quot.sound. No added axiom, sorry or native_decide is used.

An independent mathematical reviewer reconstructed the actual matrices,
both Gram directions and all 36 overlaps in an exact rational extension
field. Separately, ROOT rebuilt CirculantCharacter, UnitTripleZeroSum and
all three new sources in a new empty project-object directory and replayed
the complete endpoint. This separate compiler process reused the pinned
Mathlib cache; it did not reuse any earlier project olean. It was run by
ROOT, and is not described as a second Lean reviewer.

`ActualNormalizedTriplet` records the actual three normalized matrix Grams
and all three pairwise transition norms. These are the complete matrix
conditions for the three bases in finite dimension six. The source does
not construct Mathlib `OrthonormalBasis` objects. The generic bridge has
raw-data hypotheses; the concrete endpoint proves and supplies them all.
The fixed-partition witness equivalence and its resulting nonexistence
claim in the previous section remain written mathematics, not a Lean
nonexistence theorem. General companion selection and the published
cubic-product conjecture remain unproved here.

The pinned generic vector simproc printed internal diagnostics on concrete
third entries during earlier proof attempts. The final source replaces
that simproc with the proved third-entry rewrite, and represents Hc by its
actual entries with a proved equality to the original circulant blocks.
All linters remain enabled; no dependency or system configuration was
changed. Earlier failed attempts were retained locally and are not
presented as passing verification.

To replay from the repository, use the pinned package's environment and
build the five project modules in this order:

```sh
taskMubSources=$(realpath 004-mub-triplets/proof)
taskMubBuild=$(mktemp -d)
export LEAN_PATH="$taskMubBuild${LEAN_PATH:+:$LEAN_PATH}"
cd 002-weighted-rectangular-pruning/proof/mathlib
for taskModule in CirculantCharacter UnitTripleZeroSum PrimitiveCubicRoot NormalizedRawMUBBridge FourierAsymmetricTriplet; do
  lake env lean --root="$taskMubSources" -o "$taskMubBuild/$taskModule.olean" "$taskMubSources/$taskModule.lean" || exit 1
done
```
