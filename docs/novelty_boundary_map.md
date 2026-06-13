# Novelty Boundary Map

## Claimed boundary

- Shadow removal treats artifacts as image corruption.
- Cast-shadow reasoning uses shadows as external scene evidence.
- Visual self-modeling estimates robot body state but does not explicitly use self-caused shadows or reflections as latent state.

## V2 boundary failure

The runnable experiment does not cross that boundary. The shadow-state controller uses a correction that can be computed from current penetration and velocity without any shadow measurement. A non-shadow kinematic advance baseline therefore matches the result exactly.

## Future requirement

A recoverable version would need a visual artifact variable whose removal degrades performance and whose non-shadow proxy cannot reproduce the same downstream behavior.
