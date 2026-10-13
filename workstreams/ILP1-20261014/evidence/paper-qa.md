# Research draft visual verification

Actual final PDF:17 pages. Source SHA256 `2ba4ec3531787f4dbf0739df834a571661b02622b4247271703cc567ca3c808d`; PDF SHA256 `d657f325e88943ce3ce464ce37bfa3c1ad902514ce30c3851db330816148b924`. Both hashes match the final build receipt.

Two actual pdflatex passes completed. The build rejects overfull horizontal/vertical boxes and undefined references; none occurred. All17 final pages were rendered with pdftoppm at1350px maximum dimension and fully decoded by PIL without truncated-image acceptance. The17-page contact sheet was visually inspected, as were full-resolution pages1,7,14,15,16 during integration and the corrected final pages14,16. Mathematical displays, tables, footers and references fit their pages without clipping or overlap. The last bibliography page is partial but intentional.

The first rendering produced truncated PNGs on pages5 and13; these were detected by decoding, rerendered individually, then successfully decoded. The final corrected PDF was independently rendered again; all17 pages decoded on that pass. Compilation is not being substituted for visual inspection.

The hidden-final-operand proof's two nonstandard A-first actions were checked during visual reading and spelled out separately so no already-completed job is reissued. Other theorem and proof-status limits are unchanged. Temporary rendered images: `/workspace/scratch/6a1539b44ef3/ilp1-paper-qa/phase5final-*.png` (not repository artifacts). No authorship, new license, formal version or DOI is assigned.
