# Claims

Original claim:

- Robot-caused shadows/reflections can encode pose, body, and lighting interactions that should be treated as robot state.
- A shadow-state controller improves downstream contact behavior under delayed evidence.

V2 result:

The runnable evidence does not support the shadow-specific claim. A non-shadow kinematic latency-advance controller exactly matches the shadow-state controller at every tested latency. At 150 ms, both peak at 48.155 N, while delayed force feedback peaks at 48.539 N.

Unsupported claim:

The repository does not demonstrate that self-shadow state, reflection state, or illumination geometry adds information beyond ordinary kinematic latency compensation.
