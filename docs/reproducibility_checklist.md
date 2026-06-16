# Reproducibility Checklist

Commands:

- `python scripts/run_full_scale_self_shadow_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

Expected experiment validation:

- `expected_condition_rows`: 302400.
- `actual_condition_rows`: 302400.
- `represented_trajectory_evaluations`: 37013760000.
- `represented_frame_decisions`: 2664990720000.

Expected PDF artifact:

- Path: `C:/Users/wangz/Downloads/49.pdf`.
- Pages: 25.
- SHA256: `72BF9B8880BB56F73A00538B19883AE37A7C5CEB676C7AAD26A9EE9DB91D2AEF`.
- Local `main.pdf`: absent after build.

Visual QA:

- Render PDF pages with `pdftoppm -png -r 144`.
- Inspect title page, main result figure page, dense table page, appendix page, and final page.
- Confirm generated figures are nonblank and table text fits.
