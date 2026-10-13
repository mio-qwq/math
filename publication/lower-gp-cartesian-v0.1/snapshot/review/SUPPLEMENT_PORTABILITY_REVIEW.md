# Independent AI portability addendum

Date: 12 October 2026. Scope: only the new package-local adapter and the added reproduction paragraph. This is an independent AI code/document review, not human peer review or a new mathematical audit. No original report, manuscript, mathematical source, or historical control output was modified by this reviewer.

**No blocking portability or scope-reporting defect was found.** The adapter preserves the bounded controls and redirects their paths to the extracted package. ROOT remains responsible for the actual extracted-package execution and output verification; this addendum does not claim that execution has already succeeded.

## Exact bindings and relation to the earlier report

Directly computed SHA256 values:

| File | SHA256 |
| --- | --- |
| `replay_independent_controls.py` | `e896d774d4548c4fabd29cd8719a916a3608d77afd053c430b5210fd8347e4d5` |
| Current `REPRODUCE.md` | `679a06da3084f42a3dd9ae2ce6ce3e4f9424c1caa754e4ce688a4caf13843766` |
| Preserved `review/scratch/independent_small_controls.py` | `7431ad02908c06cf8624ff710d235653f0052575a39d3beb320778eabfd1d1d6` |
| Preserved `review/scratch/independent_small_controls.json` | `a4f0afd76e54363e3abb0ce7a182d5a7058cd5e0f7e46310713d334b0a4af6e2` |
| Unmodified `review/FINAL_MANUSCRIPT_REVIEW.md` | `a6bac8e7dd35602488aaa97f0de206b1f3f32139609f679e7ae406edf816edd1` |

`FINAL_MANUSCRIPT_REVIEW.md` binds the **earlier** reproduction document, SHA256 `213c84f34c048b96d0d7f9adb8d9d70609c98788fc73371ef35b1ef80423e338`. It was intentionally retained unchanged. This addendum covers the current reproduction document and newly added adapter. Deleting exactly the new optional-replay paragraph from the current document reproduces the earlier document's byte hash; no other reproduction instruction changed.

The actual TeX, BibTeX and PDF still match their earlier reviewed hashes (`81104eac829996435ed5076a56745c4b5ef2494db33fd9321b76bebfdd97b815`, `012b8a5a1ec7e03b44b44f5e2361bd7b792d07b5217da40543956e0195683ac6`, and `fe923b7017dd04c03126aa07a48c3538a48a31855e4bb2ec973d4f5397392cb4`, respectively). All seventeen mathematical-source bindings were also rechecked against actual file bytes and still match.

## Review performed and reasons

I read the complete adapter, current reproduction document, and preserved control source. I executed only a read-only AST-prefix check: it parsed the preserved source and performed the adapter's four-assignment removal, stopping before directory creation or control execution. A separate comparison, including AST attributes, confirmed that the removed names are exactly `REPO`, `WRITTEN`, `FIXED`, and `OUT`, each once, and that every remaining top-level node is unchanged. All thirteen original functions and the original main execution body are preserved. The adapter has no additional transformation of proof or control code.

`ROOT` derives from the adapter's resolved file location, so running the command does not depend on the caller's working directory or the former machine's absolute repository path. The injected `REPO` is `ROOT/supplement`, with `WRITTEN` and `FIXED` at its `universal` and `fixed319` subdirectories. All files used by the controls exist under those package paths. New control output and the adapter receipt go to `verification/replayed-independent-controls/`; the preserved source and historical JSON are not output targets.

The new paragraph correctly calls this an optional bounded replay, describes the path-only adaptation and separate output, and excludes a second full MET5 or Lean verification. The existing instruction against Python `-O` remains applicable, since assertions are essential to both adapter and controls.

The replay's JSON is expected to differ from the historical JSON in UTC and in the source-hash map's relative path keys (`fixed319/...` and `universal/...` instead of the old repository layout). Its mathematical control statistics and corresponding source-hash values are the appropriate comparison targets; raw JSON byte identity is not expected. ROOT should record the actual extracted-package result separately. No Lean compilation, full MET5 enumeration, or repeated mathematical-source review was performed in this addendum.
