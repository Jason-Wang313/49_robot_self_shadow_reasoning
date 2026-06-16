# Hostile Reviewer Response

Reviewer attack: This is just shadow detection.

Response: The benchmark separates generic photometric residuals from robot self-shadow state. The generic residual baseline sees brightness changes but has high false external-shadow rate and negative utility. The proposed policy gains because it attributes robot-caused image structure through robot geometry and uses it for hidden pose and clearance.

Reviewer attack: Kinematics already solves robot self-state.

Response: Kinematics is included as a baseline under clean encoders, bias, dropout, latency, camera-proprioception desynchronization, and backlash. It reaches 4.56 cm pose error, 5.02 cm clearance error, 0.396 unsafe-clearance rate, and negative utility.

Reviewer attack: The evidence is simulated.

Response: Correct. The paper is framed as a deterministic mechanism benchmark and does not claim hardware validation. The value is isolating a self-shadow-specific state variable across a large stress grid.

Reviewer attack: Shadows are unreliable.

Response: The paper agrees under cable-shadow confusion, moving lamps, broad mobile-manipulator shadows, and transparent materials. Those cases are reported as boundaries. The claim is that attributed robot-caused shadows and reflections are useful when their causal assumptions hold.
