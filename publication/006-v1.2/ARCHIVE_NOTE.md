# Archive contents and boundaries

The archive preserves exact repository-relative payload bytes: the standalone manuscript and PDF, companion bibliography, three mathematical Lean modules, pinned Git dependency configuration, graph and certificate, exact checkers, replay tools and recorded source-specific evidence. No private instructions, credentials, cached dependencies, machine junctions or third-party paper PDFs are included.

Existing repository navigation links in copied documentation can lead to project pages outside this 006 supplement. Those pages remain available in GitHub. The ZIP, external SHA256SUMS, integrity-check.json, archive-replay.json and final package-validation.json are provided alongside the archive, avoiding circular file hashes. The included manifest omits its own self-hash; external SHA256SUMS covers it.

Historical Lean compilations retain their original dates; this paper revision binds their unchanged mathematical source hashes. New exact graph checks and environment-only queries have separate receipts. The extracted supplement's graph reconstruction and certificate comparison were rerun as documented in archive-replay.json. Empty-cache Lean bootstrapping on a new machine has not been performed.

The compiler-output log is normalized to UTF-8/LF, with two absolute local output-directory paths replaced by an explicit placeholder. Diagnostics and filenames are preserved. The source log remains local; original and published hashes and the transformation are recorded in evidence/compile-output-serialization.json.

Draft author information is supplied; accountability examination, paper deposit license and external-publication approval remain pending. The repository LICENSE does not choose that deposit license. No Zenodo record or DOI has been created or reserved by this preparation work. No historical priority or external human peer review is claimed.
