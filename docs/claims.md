# Claims

Primary claim:

- Robot-caused shadows and reflections can be represented as a causal robot self-shadow state for hidden pose and clearance reasoning under self-occlusion.

Supported result:

- Across 302400 compact condition rows, the robot self-shadow state is the only non-oracle policy with positive aggregate utility.
- Proposed policy: 1.91 cm hidden-pose error, 2.24 cm clearance error, 0.078 unsafe-clearance rate, 0.734 self-occlusion F1, 0.776 safe-action success, and 0.461 utility.
- Strongest non-shadow baselines remain near 4.42 cm pose error, 4.90 cm clearance error, 0.36 to 0.40 unsafe-clearance rate, and negative utility.

Bounded interpretation:

- The evidence is a deterministic simulated mechanism benchmark.
- The claim is strongest under local self-occlusion, gripper/tool/fingertip shadows, contact-line shadows, and informative reflections.
- The claim weakens under cable-shadow confusion, broad mobile-base shadows, transparent materials, and moving lights.
