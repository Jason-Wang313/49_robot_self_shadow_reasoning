# Reviewer Attacks

Attack: The paper is only measuring access to more visual pixels.

Response: The generic photometric residual baseline has access to photometric change, but its utility remains negative because it lacks robot-centered attribution.

Attack: The method should be compared with shadow removal.

Response: Shadow removal/inpainting is included. It reaches 4.42 cm pose error, 4.90 cm clearance error, 0.386 unsafe rate, and negative utility.

Attack: Kinematics and a better self model are enough.

Response: The kinematic-only self model is included under six proprioception regimes. It is the weakest baseline on aggregate pose and clearance.

Attack: The method is too lighting-dependent.

Response: Lighting stress is reported. Side light is strongest; moving lamps and transparent surfaces are weaker but remain positive. The limitation is stated.

Attack: The benchmark is synthetic.

Response: The manuscript presents a deterministic mechanism benchmark and avoids hardware claims. A hardware translation plan is included in the appendix.
