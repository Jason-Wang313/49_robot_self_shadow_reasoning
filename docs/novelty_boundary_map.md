# Novelty Boundary Map

- Already covered: shadow detection/removal, cast-shadow localization, self-modeling, mirror self-recognition support, occlusion-aware perception.
- Not yet covered together: a robot-centric latent state for self-generated shadows/reflections that is updated online and used by planning/control.
- Boundary: if the method only segments shadows before perception, it is not novel enough. The central mechanism must explain and predict self-caused illumination artifacts as state variables.
- Weak variants: better shadow masks, better detectors, or a larger multimodal model.
- Strong variant: a causal self-shadow field coupled to body pose and scene geometry, with evidence that the field reduces egocentric self-model and localization errors.
