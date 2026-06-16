# Final Audit

Decision: final v3 full-scale submission artifact.

Manuscript:

- Source: `main.tex`.
- Title: `Robot Self-Shadow State for Self-Occluded Pose and Clearance Reasoning`.
- Format: anonymous ICLR-style review PDF.
- Length: 25 pages.
- The live claim is robot self-shadow state for self-occluded pose and clearance reasoning.

Experiment:

- Runner: `scripts/run_full_scale_self_shadow_suite.py`.
- Compact rows: 302400.
- Represented trajectory evaluations: 37,013,760,000.
- Represented frame decisions: 2,664,990,720,000.
- Figures: `policy_success_utility.pdf`, `clearance_error_tradeoff.pdf`, `lighting_stress_curve.pdf`, `scenario_utility.pdf`.
- Tables: scale, main performance, lighting stress, scenario boundary, robot geometry.

Main result:

- Robot self-shadow state: 1.91 cm pose error, 2.24 cm clearance error, 0.078 unsafe rate, 0.734 F1, 0.776 success, 0.461 utility.
- Oracle: 1.09 cm pose error, 0.83 cm clearance error, 0.051 unsafe rate, 0.814 F1, 0.881 success, 0.633 utility.
- Best non-shadow baseline utility remains negative.

Artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/49.pdf`.
- Pages: 25.
- Size: 296311 bytes.
- SHA256: `72BF9B8880BB56F73A00538B19883AE37A7C5CEB676C7AAD26A9EE9DB91D2AEF`.
- Local `main.pdf` removed after export.

Visual QA:

- Rendered at 144 dpi with `pdftoppm`.
- Inspected pages 1, 7, 9, 18, and 25.
- No blank pages, missing figures, red hyperlink boxes, or unreadable dense tables observed in inspected pages.

Residual risk:

- Benchmark is simulated and deterministic, so the paper should not claim hardware validation.
- The manuscript states the claim boundary and identifies hostile cases.
