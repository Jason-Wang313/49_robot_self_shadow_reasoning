import math
import os

import matplotlib.pyplot as plt
import numpy as np


def simulate(latency_s: float, use_shadow_state: bool, seed: int = 0):
    rng = np.random.default_rng(seed)
    dt = 0.002
    t = np.arange(0.0, 2.0, dt)
    target = np.where(t < 0.6, 0.0, 1.0)
    x = 0.0
    v = 0.0
    v_hist = []
    f_contact_hist = []
    f_obs_hist = []
    contact_started = False
    contact_t = None
    buffer_len = max(1, int(round(latency_s / dt)))
    obs_buf = [0.0] * (buffer_len + 1)
    peak = 0.0
    for ti, des in zip(t, target):
        # Simple wall contact at x >= 0.9.
        pen = max(0.0, x - 0.9)
        f_contact = 500.0 * pen + 4.0 * max(0.0, v)
        if f_contact > 1e-6 and not contact_started:
            contact_started = True
            contact_t = ti
        obs_buf.append(f_contact)
        f_obs = obs_buf.pop(0)
        if use_shadow_state and contact_started:
            # Advance delayed evidence with current penetration rate proxy.
            f_use = f_obs + 500.0 * max(0.0, x - 0.9) - 500.0 * max(0.0, x - 0.9 - v * latency_s)
            f_use = max(0.0, f_use)
        else:
            f_use = f_obs
        # PD-ish control with force correction.
        u = 12.0 * (des - x) - 1.2 * v - 0.02 * f_use
        # Saturation and plant
        u = float(np.clip(u, -18.0, 18.0))
        a = u - 0.15 * v - (f_contact if pen > 0 else 0.0)
        v += dt * a
        x += dt * v
        x = float(np.clip(x, -0.2, 1.2))
        v_hist.append(v)
        f_contact_hist.append(f_contact)
        f_obs_hist.append(f_use)
        peak = max(peak, f_contact)
    return t, np.array(f_contact_hist), np.array(v_hist), peak


def main():
    os.makedirs("figs", exist_ok=True)
    latencies = np.array([0.0, 0.05, 0.10, 0.15])
    peaks_naive = []
    peaks_shadow = []
    for L in latencies:
        _, _, _, p0 = simulate(L, False)
        _, _, _, p1 = simulate(L, True)
        peaks_naive.append(p0)
        peaks_shadow.append(p1)

    plt.figure(figsize=(5.2, 3.4))
    plt.plot(latencies * 1000, peaks_naive, "o-", label="delayed force feedback")
    plt.plot(latencies * 1000, peaks_shadow, "s-", label="shadow-state controller")
    plt.xlabel("observation latency (ms)")
    plt.ylabel("peak contact force (N)")
    plt.title("Synthetic first-contact sensitivity to delayed evidence")
    plt.grid(True, alpha=0.3)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig("figs/contact_latency_plot.png", dpi=200)

    # One representative trajectory for the paper.
    t, f0, _, _ = simulate(0.15, False)
    _, f1, _, _ = simulate(0.15, True)
    plt.figure(figsize=(5.2, 3.4))
    plt.plot(t, f0, label="delayed force feedback")
    plt.plot(t, f1, label="shadow-state controller")
    plt.xlabel("time (s)")
    plt.ylabel("control force proxy (N)")
    plt.title("Representative run at 150 ms latency")
    plt.grid(True, alpha=0.3)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig("figs/contact_latency_trace.png", dpi=200)

    with open("docs/sim_results.txt", "w", encoding="utf-8") as f:
        for L, p0, p1 in zip(latencies, peaks_naive, peaks_shadow):
            f.write(f"{L:.3f},{p0:.4f},{p1:.4f}\n")


if __name__ == "__main__":
    main()
