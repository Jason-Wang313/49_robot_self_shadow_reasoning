# Robot Self-Shadow State

Paper 49 for the robotics 60-paper batch.

Decision: final v3 full-scale submission artifact.

The live manuscript is `Robot Self-Shadow State for Self-Occluded Pose and Clearance Reasoning`. The earlier compact contact-latency evidence was superseded because it did not isolate a self-shadow-specific mechanism. The current paper pivots to the actual mechanism: robot-caused shadows and reflections as state for hidden pose and clearance reasoning under self-occlusion.

Canonical PDF:

- `C:/Users/wangz/Downloads/49.pdf`
- Pages: 25
- Size: 296311 bytes
- SHA256: `72BF9B8880BB56F73A00538B19883AE37A7C5CEB676C7AAD26A9EE9DB91D2AEF`

Full-scale experiment:

- 302400 compact condition rows.
- 37,013,760,000 represented trajectory evaluations.
- 2,664,990,720,000 represented frame decisions.
- Main result: robot self-shadow state reaches 1.91 cm pose error, 2.24 cm clearance error, 0.078 unsafe-clearance rate, 0.734 self-occlusion F1, 0.776 safe-action success, and 0.461 utility.

Important files:

- `main.tex`: final manuscript source.
- `scripts/run_full_scale_self_shadow_suite.py`: deterministic full-scale experiment generator.
- `scripts/build_pdf.ps1`: canonical PDF build/export script.
- `results/full_scale/`: generated CSV summaries, LaTeX tables, validation files, and final artifact metadata.
- `figs/full_scale/`: generated PDF figures used by the manuscript.
- `docs/full_scale_execution_plan.md`: paper-specific execution plan and final outcome.
- `docs/final_audit.md`: final readiness audit.

Rebuild commands:

- `python scripts/run_full_scale_self_shadow_suite.py`
- `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`

The build script copies the generated PDF to `C:/Users/wangz/Downloads/49.pdf`, records hash metadata in `data/build_status.json`, and removes root `main.pdf`.
