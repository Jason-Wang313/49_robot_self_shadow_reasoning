# Novelty Boundary Map

Inside the claim:

- Robot-caused cast shadows from grippers, tools, wrists, arms, sensor rigs, and body components.
- Robot-caused reflections from fingertips, tools, and sensor hardware on glossy or transparent surfaces.
- Hidden pose and clearance reasoning under self-occlusion.
- Cases where proprioception is biased, delayed, dropped, desynchronized, or mechanically uncertain.
- Causal attribution of photometric evidence through robot geometry.

Outside the claim:

- Generic image shadow removal.
- External cast-shadow scene localization where the shadow is not caused by the robot.
- Pure visual self-modeling that ignores illumination artifacts.
- Hardware deployment claims without a physical robot study.

Hard boundary cases:

- Cable-shadow confusion.
- Moving independent light sources.
- Broad mobile-base shadows with weak local geometry.
- Transparent surfaces that shift apparent reflection geometry.

Novel contribution:

- Treat robot-caused shadows and reflections as first-class self-state evidence before deciding whether to remove, ignore, or use the artifact.
