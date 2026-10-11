# Ordinary source review of the streaming-prefix implementation

Date: 2026-10-11. Verdict: **pass; no mathematical or implementation defect found in the reviewed evaluator**. No source change is requested.

## 1. Reviewed versions and disclosure boundary

| File | Reviewed SHA-256 |
|---|---|
| `../../proofs/streaming_prefix_baseline.md` | `738f5b5fb3a9ef2414f75d1406d43af455acab99cb660ea04eed90e9f7b71315` |
| `../../experiments/streaming_prefix.py` | `225348096f0e4bddbd13a117840ea45ea5976c32b6a4ec65e2d0ee4476d905b7` |
| `../../experiments/STREAMING_PREFIX_RUN.md` | `4390656f4c62163159798a146f1f7aef377cf41169ce5c1eb755bef278bc2a69` |
| `../../experiments/results/streaming_prefix_run.json` | `501a20071b5215adfa61a5de8dd51ed580ef98f585d46c80484daacdb3db2b1c` |

The relative paths in this table refer to the parent project from this nested review directory. The exact absolute paths are also captured in `ordinary_code_review_run.json`.

The preceding phase reconstructed the kernels and tested the supplied mathematical specification before reading these implementation files. That phase is documented in `MATRIX_SPEC_REVIEW.md` and `matrix_spec_run.json`.

This phase explicitly read the four files above and imported the reviewed Python module for 18 targeted executions. It is **ordinary post-disclosure code review**, not a blind third implementation. The discovery implementation's full 1,650-case harness was not rerun. The previous independent word data and small mathematical checks were already sufficient; the targeted calls reused precisely the same 18 cases.

## 2. Transition and insertion implementation

`build_transition` correctly enumerates eight bit triples in the uniform model and four bit pairs in the fixed-word model. In the latter, the output bit of `B=S-A` and the outgoing subtraction borrow both use the fixed input bit and current borrow. The signs for `B`, `Y`, and `BY` apply to the appropriate bits of that same transition.

`constant_tables` constructs only three kernel types and four boundary-phase types. These are independent of `n`. It inverts only the unmasked kernels, obtains determinant `1/16`, and checks exact inverse identities. The constant signed insertion is built as

`D P^-1 P^mask D = T^-1 K^mask`.

`scale_columns` implements the incoming phase in `T=P D`; `scale_rows` implements the inverse phase in `T^-1=D P^-1`. The actual phase code uses the XOR of the two borrow-boundary indicators, so coincident borrow observations cancel correctly.

The ordinary code check compared all 36 combinations of mode, phase, and marked insertion against the independently reconstructed matrices. All agree, including the joint `BY` transitions. The six base/inverse matrices also agree with the preceding independent reconstruction.

## 3. Prefix orientation and mask placement

The terminal row is computed in descending bit order, giving `f T_(n-1) ... T_0` as required. There is no reversal of the intended transition order.

`advance` correctly left-multiplies a forward prefix and right-multiplies its inverse:

`prefix_next=T_p prefix`, `inverse_next=inverse T_p^-1`.

`conjugated_insertion` implements `G_p^-1 (T_p^-1 K_p) G_p`. For distinct positions the evaluator first multiplies the terminal row by the high insertion and then takes its product with the first column of the low insertion. This is precisely `fG_n H_high H_low e0`.

The two interval branches exchange mask roles correctly when the rotation wraps: the lower position is a `Y` mask and the higher a `B` mask in the `i<q` branch. The coefficient exponent is then the higher `B` position, `n-q+t`. In the nonwrapping branch it is `t`.

When `q=0`, the code uses one joint `BY` insertion at the shared position and maintains only one active prefix pair. Empty intervals return the unmasked moment times `2^-j`. All terminal states are summed. The result retains the sign and the correlation normalization; it is not an absolute value or a probability bias.

The public function checks that `r,q` are already in `[0,n)` and rejects values outside this declared interface domain. This is consistent with the accompanying proof. A caller wanting rotation aliases must reduce them before calling this particular API.

## 4. Actual arithmetic and storage behavior

There is no list, dictionary, decorator cache, or memoized recursion retaining a prefix for every position in `streaming_correlation`. The global tables have fixed size. The local state consists of one terminal row, two prefix/inverse pairs, a fixed number of temporary matrices or rows, one weighted sum, and fixed-size statistics. Each tuple/list in a matrix operation has fixed dimension four. Replacing a prefix does not retain its predecessor.

For nonzero distance `d` and nonempty interval length `L`, the actual dynamic count is `2d+8L` four-by-four matrix products and `n+L` row products. For a shared position it is `4L` matrix products and `n` row products. For an empty interval it is zero matrix products and `n` row products. The final unnecessary prefix advancement is included in these counts. They satisfy the stated upper bounds of `8n` matrix products and `2n` row products.

The ordinary executions checked these **exact** operation-count formulas for all 18 reused cases, rather than only checking the looser upper bound. All passed.

The proof's representation-length argument applies to the actual operations: the constant inverse kernels are dyadic with denominator at most two and induced one-norm at most ten; prefix and inverse-prefix entries have `O(n)`-bit representations. Only a constant number remain live. Current `Fraction` multiplication temporaries also involve only products or sums of a fixed number of `O(n)`-bit operands. Thus the core's `O(n)` live auxiliary-bit bound is justified in the usual mathematical storage model.

This does not assert linear bit time. The proof correctly charges multiplication and `Fraction` normalization/GCD costs separately. Its dyadic-arithmetic alternative and the schoolbook cubic bit-operation upper bound are distinguished from the `O(n)` rational-operation count. The documentation does not infer a smaller elementary bit-time exponent over the project's earlier addition-based evaluator, a measured speedup, or a stronger published algorithmic bound.

## 5. Core space versus harness and instrumentation

The `main` test harness reads complete JSON/JSONL inputs, retains all 1,650 result records, and serializes them. Those collections are outside the single-correlation core evaluator. Their storage grows with the number and size of test records, and must not be included in an assertion that the entire process uses only a constant number of matrices.

The supplied proof, receipt, and result JSON make this distinction explicitly. They also state that process RSS includes interpreter state, constant tables, parsed inputs and retained reports. Consequently the observed RSS is not presented as an asymptotic proof of the core's space usage.

The scalar-product counter counts nonzero products inside the matrix and row routines. It excludes some dot products, coefficient multiplications, initialization and harness work. The receipt explicitly says it is not a count of every scalar operation.

Likewise the reported 79-bit maxima are the largest **observed reduced** numerators and denominators at the instrumented matrices, rows, moments and accumulators. They are not an exhaustive measurement of every temporary integer allocated inside `Fraction`. The written growth proof supports the general bound. The receipt accurately describes the observation points.

The reported 1.480809-second timing starts after constant-table construction and ends before JSON serialization; it includes input parsing and retained-result construction. That scope matches the code and is stated in the receipt. It is not used to infer a speedup against a different workload.

## 6. Evidence executed or inspected in this review

The supplied result file records 216 uniform-word comparisons, 1,274 fixed-word comparisons, and 160 standard-width comparisons, with no failures and completion code zero. Its source hash matches the reviewed source and the provided expected hash. Its three input hashes match the frozen independent data. These are the implementing agent's recorded self-checks; this review does not relabel them as a new blind verifier execution.

The additional ordinary-code check executed here was:

```sh
python /workspace/scratch/5f0455e66649/math-crypto/workstreams/CRYPTO/projects/chacha-three-add/verification/streaming_review/ordinary_code_review_checks.py
```

It exited zero and checked:

- 36 constant phase/mask insertion matrices against the earlier independent kernel reconstruction;
- the same 18 selected original-word cases already used in the mathematical phase;
- the exact dynamic matrix/row operation counts on those cases;
- unchanged hashes for the reviewed source, all 22 earlier verification files, and their old manifest.

No original-word search was added, and the full 1,650-case harness was not repeated. Exact results, source hashes, command, and timestamps are in `ordinary_code_review_run.json`. Bytecode generation was disabled during imports, avoiding generated cache files in the reviewed implementation directory.

## 7. Final assessment

The source implements the supplied mathematical construction with the correct phase orientation, inverse update direction, same-position joint kernel, wrapped pair ordering and correlation normalization. Its core genuinely avoids storing all prefixes, and its proof distinguishes arithmetic-operation count, operand length, auxiliary bits and test-report storage. No blocking or nonblocking source correction was identified.

The conclusion is implementation correctness and an appropriate same-target computational baseline. This review makes no novelty claim for the matrix construction, the project-specific optimization, or any cryptanalytic improvement. It is ordinary source review following a separate independent mathematical-specification check, not formal verification or human peer review.
