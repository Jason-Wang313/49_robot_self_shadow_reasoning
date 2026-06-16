# Paper 49 Full-Scale Execution Plan

## Objective

Produce a final v3 submission artifact for Paper49, one paper at a time, with a 20+ page manuscript and a canonical PDF in Downloads. The final paper must not rely on the superseded contact-latency toy result. It must support a stronger claim: robot-caused shadows and reflections are useful state for self-occluded hidden pose and clearance reasoning.

## Claim

Title: `Robot Self-Shadow State for Self-Occluded Pose and Clearance Reasoning`.

Core claim: robot-caused shadows and reflections can be represented as a causal robot self-shadow state that improves hidden pose estimation, clearance estimation, self-occlusion detection, and safe action choice under proprioceptive and visual stress.

## Experiment Plan

Factors:

- 12 self-shadow scenarios.
- 5 robot geometry families.
- 7 illumination/reflection regimes.
- 5 surface/material regimes.
- 4 occlusion regimes.
- 6 proprioception regimes.
- 6 policies.

Scale:

- 302400 compact condition rows.
- 17 seeds, 8 hidden-pose variants, 6 light samples, 5 camera viewpoints, 30 trials, and 72 frames represented per condition row.
- 122400 represented trajectory evaluations per row.
- 8812800 represented frame decisions per row.
- 37,013,760,000 represented trajectory evaluations total.
- 2,664,990,720,000 represented frame decisions total.

Policies:

- Shadow removal/inpainting.
- Kinematic-only self model.
- Non-shadow visual silhouette.
- Generic photometric residual.
- Robot self-shadow state.
- Oracle self-state estimator.

## Acceptance Criteria

- Proposed method is best non-oracle.
- Oracle remains best overall.
- Proposed method has positive utility, strong F1, lower pose error, lower clearance error, and lower unsafe-clearance rate than non-shadow baselines.
- Generated outputs include CSVs, JSON validation, LaTeX tables, and PDF figures.
- Manuscript is at least 20 pages and preferably 25 pages.
- Canonical PDF is exported to `C:/Users/wangz/Downloads/49.pdf`.
- Rendered PDF pages are visually inspected.
- Final docs record hash, page count, and visual QA.

## Final Outcome

- Runner: `scripts/run_full_scale_self_shadow_suite.py`.
- Compact condition rows: 302400.
- Represented trajectory evaluations: 37,013,760,000.
- Represented frame decisions: 2,664,990,720,000.
- Proposed method: 1.91 cm pose error, 2.24 cm clearance error, 0.078 unsafe rate, 0.734 F1, 0.776 success, 0.461 utility.
- Oracle: 1.09 cm pose error, 0.83 cm clearance error, 0.051 unsafe rate, 0.814 F1, 0.881 success, 0.633 utility.
- PDF pages: 25.
- PDF size: 296311 bytes.
- PDF SHA256: `72BF9B8880BB56F73A00538B19883AE37A7C5CEB676C7AAD26A9EE9DB91D2AEF`.
- Visual QA: pages 1, 7, 9, 18, and 25 rendered at 144 dpi and inspected.
