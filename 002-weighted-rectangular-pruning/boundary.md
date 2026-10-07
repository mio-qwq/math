# A positive-weight obstruction to convexifying the product hypothesis

This supplement to [paper.md](paper.md) proves that Theorems 1 and 2 do not extend to pair costs formed by summing just two strictly positive product systems. It is a boundary example for the hypotheses, not an input supported by the product-weighted solver.

Use one element in each of the four coordinate sets, and include the unique possible pair in each relation and each original family. There is one conflict, one corner in \(H\), and one corner in \(Z\). Its augmented graph is the path
\[
 z_L\;--\;c\;--\;r\;--\;z_R.
\]

Consider the following two positive systems of coordinate weights:

| System | \(a\) | \(b\) | \(c\) | \(d\) |
| --- | --- | --- | --- | --- |
| 1 | \(1/10\) | \(1\) | \(1\) | \(1/10\) |
| 2 | \(1\) | \(1/10\) | \(1/10\) | \(1\) |

Sum the pair costs produced by these systems, rather than sum the coordinates before taking products. Thus
\[
 w_R=\sum a d=101/100,\qquad
 w_C=\sum b c=101/100,\qquad
 w_H=\sum a c=1/5,\qquad
 w_Z=\sum b d=1/5.
\]
Both graph copies of the \(Z\)-corner have cost \(w_Z\).

**Proposition.** With these pair costs, the minimum cover cost is \(121/100\), exceeding \(w_H+w_Z=2/5\). Moreover no conflict-free pruning satisfies the corresponding deletion bound.

**Proof of the cover obstruction.** Every inclusion-minimal cover of a four-vertex path is one of
\[
 \{r,c\},\qquad\{r,z_L\},\qquad\{c,z_R\}.
\]
Their costs are \(202/100\), \(121/100\), and \(121/100\), respectively. Since all costs are positive, any other cover contains an inclusion-minimal cover and cannot cost less. This proves the minimum. The proposed right-hand side is \(40/100\), leaving a gap of \(81/100\).

For an independent lower-bound certificate, use the usual cover network. Send \(101/100\) from the source to \(r\), and \(1/5\) from the source to \(z_L\). Route \(81/100\) from \(r\) to \(c\), \(1/5\) from \(r\) to \(z_R\), and \(1/5\) from \(z_L\) to \(c\). Send \(101/100\) from \(c\) to the sink and \(1/5\) from \(z_R\) to the sink. These rational flows obey capacity bounds and conservation, and have value \(121/100\), equal to the cost of \(\{r,z_L\}\). Summing conservation over a cut proves that no cover has smaller cost.

**Proof of the pruning obstruction.** Both original members cannot be retained. The complete list of feasible deletion choices is:

| Deleted originals | Deletion cost | Uncovered \(Z\)-corners | Proposed bound \(w_H+w(U)\) |
| --- | --- | --- | --- |
| \(r\) alone | \(101/100\) | none | \(1/5\) |
| \(c\) alone | \(101/100\) | none | \(1/5\) |
| \(r,c\) | \(202/100\) | the unique corner | \(2/5\) |

If exactly one member survives, it covers the corner. If both are deleted, the corner is uncovered. In all three cases the cost exceeds the proposed bound. There is no initially conflict-free original member to consider. This proves the proposition. \(\square\)

Each of the two component systems individually satisfies the product-weighted theorem. In the first system, the cover \(\{r,z_L\}\) costs \(11/100\), below its bound \(1/5\). In the second, \(\{c,z_R\}\) has the same cost and bound. Different cheap covers are needed for the two systems; summing their pair costs need not preserve the existence of a sufficiently cheap common cover. The weighted-cover statement is therefore not closed under this convexification.

## The exact single-conflict criterion

For any four nonnegative pair costs \(x=w_R\), \(y=w_C\), \(h=w_H\), and \(z=w_Z\), the single-conflict pruning conclusion holds if and only if
\[
 h\geq \min\{x,y,x+y-z\}.
\]
Indeed, the three feasible deletion choices have costs \(x\), \(y\), and \(x+y\), and bounds \(h\), \(h\), and \(h+z\), respectively. At least one choice succeeds exactly under the displayed condition. The cover conclusion has precisely the same criterion: its minimum cost is \(\min\{x+y,x+z,y+z\}\), and subtracting \(z\) from its comparison with \(h+z\) gives the same minimum. This argument also covers zero costs: every cover contains one of the three listed covers, and nonnegative extra costs cannot decrease its value. Thus the example is part of an exact classification of arbitrary costs in the one-conflict case.

## Exact reproduction

The separate [examples/nonproduct.json](examples/nonproduct.json) explicitly uses its own format. It is not accepted by `code/solve.py`. Verify this supplement with:

```text
python code/check_nonproduct.py examples/nonproduct.json
```

The program uses exact rational arithmetic and explicit `require` checks, enumerates all 16 vertex subsets and all four original-deletion choices, verifies the feasible flow, and checks that all feasible prunings fail the proposed bound. It remains active under Python's optimization flag. The actually run finite stress ranges for the main theorem are recorded separately in [validation.json](validation.json).
