# PDF artifact QA

This is a document gate, not a browser actuator. It must never upload a file,
click Submit, or infer application confirmation.

Require machine checks for every artifact:

- readable PDF with a text layer;
- A4 MediaBox and expected page count;
- no replacement glyphs or empty extraction;
- visible URLs and preserved URI annotations when links are supplied;
- text bounds, margins, overflow, and reading order;
- exact SHA-256 match between generated, manifest, and staged bytes.

Render every page at 100 DPI and record an explicit per-page visual result for
spacing, clipping, alignment, density, legibility, and balance. `PASS_MACHINE`
with pending visual review is incomplete; package work ends at `PASS_FINAL`.

The public core defaults to `submission_allowed: false`. Browser upload and
submission remain separate, explicitly authorized operations.
