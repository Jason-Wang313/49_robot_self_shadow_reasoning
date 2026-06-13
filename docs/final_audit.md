# Final Audit

Paper: 49_robot_self_shadow_reasoning

Decision: kill/archive

Submission-hardening version: v2

## Original evidence

- 0 ms latency: delayed 47.899 N, shadow-state 47.899 N.
- 50 ms latency: delayed 48.032 N, shadow-state 47.714 N.
- 100 ms latency: delayed 48.281 N, shadow-state 47.910 N.
- 150 ms latency: delayed 48.539 N, shadow-state 48.155 N.

## V2 non-shadow baseline

- A non-shadow kinematic latency-advance baseline matches the shadow-state controller exactly.
- At 50 ms latency: shadow-state 47.714 N, non-shadow advance 47.714 N.
- At 100 ms latency: shadow-state 47.910 N, non-shadow advance 47.910 N.
- At 150 ms latency: shadow-state 48.155 N, non-shadow advance 48.155 N.
- Shadow minus non-shadow: 0.000 N at every tested latency.

## Main blocker

The central toy evidence is not shadow-specific. It demonstrates latency compensation from kinematic/contact state, not robot self-shadow reasoning.

## Submission decision

Kill/archive. Do not submit this paper in its current form. A future version needs an actual self-shadow/reflection measurement and a downstream task where the shadow state beats non-shadow kinematic and self-modeling baselines.

## Artifact audit

- Canonical PDF: `C:/Users/wangz/Downloads/49.pdf`
- Local generated PDF: removed after build
- Desktop copy: absent
- Build script: `scripts/build_pdf.ps1`
- V2 stress script: `scripts/v2_nonshadow_advance_baseline.py`
