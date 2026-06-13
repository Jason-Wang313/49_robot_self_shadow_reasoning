# Robot Self-Shadow Reasoning

Paper 49 for the robotics 60-paper batch.

Decision: kill/archive.

The v2 hardening stress collapses the central evidence. The original simulator claimed a shadow-state controller reduced contact-force latency sensitivity. A non-shadow kinematic latency-advance baseline reproduces the shadow-state controller exactly at every tested latency. At 150 ms latency, delayed feedback peaks at 48.539 N, while both shadow-state and non-shadow kinematic advance peak at 48.155 N; the shadow-minus-non-shadow gap is 0.000 N.

Canonical PDF:

- `C:/Users/wangz/Downloads/49.pdf`

Important files:

- `main.tex`: manuscript source.
- `scripts/sim_contact_shadow.py`: original synthetic simulator.
- `scripts/v2_nonshadow_advance_baseline.py`: v2 collapse baseline.
- `docs/v2_nonshadow_advance_baseline.json`: v2 baseline summary.
- `docs/v2_nonshadow_advance_baseline.csv`: v2 baseline table data.
- `v2_nonshadow_advance_table.tex`: manuscript table generated from v2 stress.
- `docs/final_audit.md`: final hardening audit.

Rebuild commands:

- `python scripts/v2_nonshadow_advance_baseline.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/49.pdf` and removes root `main.pdf`.
