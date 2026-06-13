# Child Status 49

Status: kill_archive
Attempt: 3
Stage: v2_submission_hardening

Current facts:
- Original manuscript and synthetic contact-shadow simulator are present.
- Original evidence is in `docs/sim_results.txt`.
- V2 non-shadow latency-advance baseline artifacts are present at `docs/v2_nonshadow_advance_baseline.json`, `docs/v2_nonshadow_advance_baseline.csv`, and `v2_nonshadow_advance_table.tex`.
- At 150 ms latency, delayed force feedback peaks at 48.539 N.
- At 150 ms latency, shadow-state control peaks at 48.155 N.
- At 150 ms latency, non-shadow kinematic advance also peaks at 48.155 N.
- The shadow-minus-non-shadow gap is 0.000 N at every tested latency.
- Canonical PDF target: `C:/Users/wangz/Downloads/49.pdf`.
- Canonical PDF size: 178297 bytes.
- Local generated root PDF is removed after build.
- Desktop PDF copy is absent.

Decision:
- Kill/archive. The central toy evidence is not shadow-specific; it is exactly reproduced by a non-shadow latency-compensation baseline.

End time: 2026-06-13 10:33:38 +01:00
