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
- SHA256: `41D52D6E629156AD7C22D0706DBA2A618E95225936C5A016E94D9C34FC41D120`.
- Local `main.pdf`: absent after build.

Visual QA:

- Render affected highlight pages with `pdftoppm -png -r 160`.
- Inspect pages 3, 4, 6, 7, 8, and 9.
- Confirm VLA-style green citation boxes and red internal-reference boxes are thin, aligned, readable, and do not collide with text, figures, tables, or captions.
