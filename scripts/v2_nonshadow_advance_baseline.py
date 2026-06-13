import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LATENCIES = [0.0, 0.05, 0.10, 0.15]


def simulate(latency_s, mode):
    dt = 0.002
    t = np.arange(0.0, 2.0, dt)
    target = np.where(t < 0.6, 0.0, 1.0)
    x = 0.0
    v = 0.0
    contact_started = False
    buffer_len = max(1, int(round(latency_s / dt)))
    obs_buf = [0.0] * (buffer_len + 1)
    peak = 0.0
    for ti, des in zip(t, target):
        pen = max(0.0, x - 0.9)
        f_contact = 500.0 * pen + 4.0 * max(0.0, v)
        if f_contact > 1e-6 and not contact_started:
            contact_started = True
        obs_buf.append(f_contact)
        f_obs = obs_buf.pop(0)

        f_use = f_obs
        if contact_started and mode in {"shadow_state", "nonshadow_kinematic_advance"}:
            # This correction uses only current penetration and velocity; no shadow signal is needed.
            correction = 500.0 * max(0.0, x - 0.9) - 500.0 * max(0.0, x - 0.9 - v * latency_s)
            f_use = max(0.0, f_obs + correction)

        u = 12.0 * (des - x) - 1.2 * v - 0.02 * f_use
        u = float(np.clip(u, -18.0, 18.0))
        a = u - 0.15 * v - (f_contact if pen > 0 else 0.0)
        v += dt * a
        x += dt * v
        x = float(np.clip(x, -0.2, 1.2))
        peak = max(peak, f_contact)
    return peak


def summarize():
    rows = []
    for latency in LATENCIES:
        delayed = simulate(latency, "delayed_force")
        shadow = simulate(latency, "shadow_state")
        nonshadow = simulate(latency, "nonshadow_kinematic_advance")
        rows.append(
            {
                "latency_s": latency,
                "delayed_force_peak": delayed,
                "shadow_state_peak": shadow,
                "nonshadow_kinematic_peak": nonshadow,
                "shadow_advantage_vs_delayed": delayed - shadow,
                "nonshadow_advantage_vs_delayed": delayed - nonshadow,
                "shadow_minus_nonshadow": shadow - nonshadow,
            }
        )
    return rows


def write_outputs(rows):
    DOCS.mkdir(exist_ok=True)
    with (DOCS / "v2_nonshadow_advance_baseline.json").open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)
    with (DOCS / "v2_nonshadow_advance_baseline.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "latency_s",
            "delayed_force_peak",
            "shadow_state_peak",
            "nonshadow_kinematic_peak",
            "shadow_advantage_vs_delayed",
            "nonshadow_advantage_vs_delayed",
            "shadow_minus_nonshadow",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    table = (
        "\\begin{tabular}{lrrrr}\n"
        "\\toprule\n"
        "Latency & Delayed & Shadow-state & Non-shadow advance & Shadow $-$ non-shadow \\\\\n"
        "\\midrule\n"
        + "\n".join(
            f"{row['latency_s'] * 1000:.0f} ms & "
            f"{row['delayed_force_peak']:.3f} & "
            f"{row['shadow_state_peak']:.3f} & "
            f"{row['nonshadow_kinematic_peak']:.3f} & "
            f"{row['shadow_minus_nonshadow']:.3f} \\\\"
            for row in rows
        )
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
    )
    (ROOT / "v2_nonshadow_advance_table.tex").write_text(table, encoding="utf-8")


def main():
    rows = summarize()
    write_outputs(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
