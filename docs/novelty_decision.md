# Novelty Decision

Chosen thesis: robot-generated shadows and reflections should be modeled as first-class perceptual state, not as preprocessing noise.

Why this survives the hostile set: existing work either removes shadows, reasons about external cast shadows, or learns self-models without explicit illumination state. The gap is an online, robot-centric state that predicts self-caused illumination artifacts and feeds back into planning/control.

Decision: proceed with a compact theory-and-evidence paper built around a causal latent shadow/reflection state and a synthetic demonstration of why ignoring it breaks self-localization and self-model consistency.
