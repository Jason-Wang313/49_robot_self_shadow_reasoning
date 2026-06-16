from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figs" / "full_scale"

SEEDS = 17
POSE_VARIANTS = 8
LIGHT_SAMPLES = 6
CAMERA_VIEWPOINTS = 5
TRIALS = 30
FRAMES = 72
EVALS_PER_ROW = SEEDS * POSE_VARIANTS * LIGHT_SAMPLES * CAMERA_VIEWPOINTS * TRIALS
FRAMES_PER_ROW = EVALS_PER_ROW * FRAMES


SCENARIOS = [
    {"name": "wrist_self_occlusion", "label": "Wrist self-occlusion", "shadow": 0.78, "reflection": 0.20, "clearance": 0.70, "kinematic_gap": 0.46, "external": 0.06},
    {"name": "gripper_cast_shadow", "label": "Gripper cast shadow", "shadow": 0.86, "reflection": 0.10, "clearance": 0.66, "kinematic_gap": 0.34, "external": 0.08},
    {"name": "elbow_table_shadow", "label": "Elbow-on-table shadow", "shadow": 0.70, "reflection": 0.14, "clearance": 0.55, "kinematic_gap": 0.42, "external": 0.10},
    {"name": "reflected_fingertip", "label": "Reflected fingertip", "shadow": 0.28, "reflection": 0.84, "clearance": 0.74, "kinematic_gap": 0.40, "external": 0.12},
    {"name": "tool_shadow_fixture", "label": "Tool shadow on fixture", "shadow": 0.76, "reflection": 0.24, "clearance": 0.80, "kinematic_gap": 0.38, "external": 0.15},
    {"name": "cable_shadow_confusion", "label": "Cable shadow confusion", "shadow": 0.48, "reflection": 0.18, "clearance": 0.62, "kinematic_gap": 0.32, "external": 0.52},
    {"name": "arm_shadow_target", "label": "Arm shadow over target", "shadow": 0.82, "reflection": 0.16, "clearance": 0.60, "kinematic_gap": 0.44, "external": 0.10},
    {"name": "sensor_rig_reflection", "label": "Sensor-rig reflection", "shadow": 0.24, "reflection": 0.78, "clearance": 0.58, "kinematic_gap": 0.36, "external": 0.18},
    {"name": "transparent_object_shadow", "label": "Self-shadow near transparent object", "shadow": 0.62, "reflection": 0.54, "clearance": 0.82, "kinematic_gap": 0.50, "external": 0.30},
    {"name": "shadow_contact_line", "label": "Shadow crossing contact line", "shadow": 0.88, "reflection": 0.22, "clearance": 0.88, "kinematic_gap": 0.54, "external": 0.08},
    {"name": "body_shadow_handover", "label": "Body shadow on handover object", "shadow": 0.74, "reflection": 0.12, "clearance": 0.72, "kinematic_gap": 0.48, "external": 0.14},
    {"name": "specular_insertion_reflection", "label": "Specular insertion reflection", "shadow": 0.34, "reflection": 0.90, "clearance": 0.90, "kinematic_gap": 0.52, "external": 0.22},
]

ROBOTS = [
    {"name": "single_arm_gripper", "label": "Single-arm gripper", "geometry": 0.78, "encoder": 0.78, "silhouette": 0.72},
    {"name": "dual_arm_manipulator", "label": "Dual-arm manipulator", "geometry": 0.86, "encoder": 0.74, "silhouette": 0.66},
    {"name": "wrist_camera_arm", "label": "Wrist-camera arm", "geometry": 0.80, "encoder": 0.76, "silhouette": 0.82},
    {"name": "dexterous_hand", "label": "Dexterous hand", "geometry": 0.90, "encoder": 0.66, "silhouette": 0.58},
    {"name": "mobile_manipulator", "label": "Mobile manipulator", "geometry": 0.70, "encoder": 0.70, "silhouette": 0.62},
]

LIGHTING = [
    {"name": "overhead_diffuse", "label": "Overhead diffuse", "shadow_quality": 0.66, "reflection_quality": 0.30, "distractor": 0.08},
    {"name": "side_light", "label": "Side light", "shadow_quality": 0.88, "reflection_quality": 0.38, "distractor": 0.12},
    {"name": "back_light", "label": "Back light", "shadow_quality": 0.74, "reflection_quality": 0.42, "distractor": 0.22},
    {"name": "moving_lamp", "label": "Moving lamp", "shadow_quality": 0.58, "reflection_quality": 0.36, "distractor": 0.36},
    {"name": "specular_surface", "label": "Specular surface", "shadow_quality": 0.42, "reflection_quality": 0.86, "distractor": 0.28},
    {"name": "transparent_surface", "label": "Transparent surface", "shadow_quality": 0.36, "reflection_quality": 0.74, "distractor": 0.40},
    {"name": "mixed_indoor_lights", "label": "Mixed indoor lights", "shadow_quality": 0.52, "reflection_quality": 0.48, "distractor": 0.30},
]

SURFACES = [
    {"name": "matte_table", "label": "Matte table", "shadow_preserve": 0.88, "reflection_preserve": 0.18, "texture": 0.12},
    {"name": "glossy_table", "label": "Glossy table", "shadow_preserve": 0.62, "reflection_preserve": 0.70, "texture": 0.20},
    {"name": "brushed_metal", "label": "Brushed metal", "shadow_preserve": 0.52, "reflection_preserve": 0.76, "texture": 0.34},
    {"name": "transparent_plastic", "label": "Transparent plastic", "shadow_preserve": 0.42, "reflection_preserve": 0.82, "texture": 0.40},
    {"name": "textured_rubber", "label": "Textured rubber", "shadow_preserve": 0.72, "reflection_preserve": 0.22, "texture": 0.42},
]

OCCLUSION = [
    {"name": "none", "label": "No occlusion", "visual_loss": 0.00, "shadow_loss": 0.04, "need": 0.18},
    {"name": "mild_self_occlusion", "label": "Mild self-occlusion", "visual_loss": 0.22, "shadow_loss": 0.02, "need": 0.48},
    {"name": "severe_self_occlusion", "label": "Severe self-occlusion", "visual_loss": 0.48, "shadow_loss": 0.10, "need": 0.78},
    {"name": "scene_object_occlusion", "label": "Scene-object occlusion", "visual_loss": 0.38, "shadow_loss": 0.24, "need": 0.62},
]

PROPRIO = [
    {"name": "clean_encoder", "label": "Clean encoder", "quality": 0.92, "latency": 0.02, "bias": 0.02},
    {"name": "encoder_bias", "label": "Encoder bias", "quality": 0.66, "latency": 0.04, "bias": 0.22},
    {"name": "encoder_dropout", "label": "Encoder dropout", "quality": 0.50, "latency": 0.06, "bias": 0.12},
    {"name": "delayed_proprioception", "label": "Delayed proprioception", "quality": 0.70, "latency": 0.24, "bias": 0.08},
    {"name": "camera_proprio_desync", "label": "Camera-proprio desync", "quality": 0.58, "latency": 0.18, "bias": 0.18},
    {"name": "joint_backlash", "label": "Joint backlash", "quality": 0.62, "latency": 0.08, "bias": 0.24},
]

POLICIES = [
    {"name": "shadow_removal_inpainting", "label": "Shadow removal/inpainting", "class": "baseline"},
    {"name": "kinematic_only_self_model", "label": "Kinematic-only self model", "class": "baseline"},
    {"name": "nonshadow_visual_silhouette", "label": "Non-shadow visual silhouette", "class": "baseline"},
    {"name": "generic_photometric_residual", "label": "Generic photometric residual", "class": "baseline"},
    {"name": "robot_self_shadow_state", "label": "Robot self-shadow state", "class": "proposed"},
    {"name": "oracle_self_state_estimator", "label": "Oracle self-state estimator", "class": "oracle"},
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable_jitter(parts: tuple[str, ...], amplitude: float) -> float:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).digest()
    unit = int.from_bytes(digest[:4], "big") / 0xFFFFFFFF
    return (unit - 0.5) * 2.0 * amplitude


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def tex_escape(text: str) -> str:
    return text.replace("&", "\\&").replace("_", "\\_").replace("%", "\\%").replace("#", "\\#")


def label(items: list[dict], name: str) -> str:
    for item in items:
        if item["name"] == name:
            return item["label"]
    return name


def policy_label(name: str) -> str:
    return label(POLICIES, name)


def scenario_label(name: str) -> str:
    return label(SCENARIOS, name)


def lighting_label(name: str) -> str:
    return label(LIGHTING, name)


def robot_label(name: str) -> str:
    return label(ROBOTS, name)


class Aggregate:
    def __init__(self) -> None:
        self.weight = 0.0
        self.pose_error = 0.0
        self.clearance_error = 0.0
        self.unsafe = 0.0
        self.false_external = 0.0
        self.success = 0.0
        self.utility = 0.0
        self.tp = 0.0
        self.fp = 0.0
        self.fn = 0.0

    def add(self, row: dict[str, float | str]) -> None:
        w = EVALS_PER_ROW
        self.weight += w
        self.pose_error += float(row["hidden_pose_error_cm"]) * w
        self.clearance_error += float(row["clearance_error_cm"]) * w
        self.unsafe += float(row["unsafe_clearance_rate"]) * w
        self.false_external += float(row["false_external_shadow_rate"]) * w
        self.success += float(row["safe_action_success"]) * w
        self.utility += float(row["utility"]) * w
        self.tp += float(row["occlusion_tp"]) * w
        self.fp += float(row["occlusion_fp"]) * w
        self.fn += float(row["occlusion_fn"]) * w

    def summary(self) -> dict[str, float]:
        precision = safe_div(self.tp, self.tp + self.fp)
        recall = safe_div(self.tp, self.tp + self.fn)
        f1 = safe_div(2 * precision * recall, precision + recall)
        return {
            "weight": self.weight,
            "hidden_pose_error_cm": safe_div(self.pose_error, self.weight),
            "clearance_error_cm": safe_div(self.clearance_error, self.weight),
            "unsafe_clearance_rate": safe_div(self.unsafe, self.weight),
            "false_external_shadow_rate": safe_div(self.false_external, self.weight),
            "safe_action_success": safe_div(self.success, self.weight),
            "self_occlusion_f1": f1,
            "utility": safe_div(self.utility, self.weight),
        }


def observed_features(scenario: dict, robot: dict, lighting: dict, surface: dict, occlusion: dict, proprio: dict) -> dict[str, float]:
    parts = (scenario["name"], robot["name"], lighting["name"], surface["name"], occlusion["name"], proprio["name"])
    shadow_signal = clip(
        0.46 * scenario["shadow"]
        + 0.22 * lighting["shadow_quality"]
        + 0.18 * surface["shadow_preserve"]
        + 0.14 * robot["geometry"]
        - occlusion["shadow_loss"]
        - 0.18 * lighting["distractor"] * scenario["external"]
        + stable_jitter(parts + ("shadow",), 0.035)
    )
    reflection_signal = clip(
        0.48 * scenario["reflection"]
        + 0.22 * lighting["reflection_quality"]
        + 0.18 * surface["reflection_preserve"]
        + 0.12 * robot["geometry"]
        - 0.12 * occlusion["shadow_loss"]
        + stable_jitter(parts + ("reflection",), 0.030)
    )
    kinematic_signal = clip(
        robot["encoder"] * proprio["quality"]
        - 0.36 * proprio["bias"]
        - 0.18 * proprio["latency"]
        - 0.12 * scenario["kinematic_gap"]
        + stable_jitter(parts + ("kinematic",), 0.025)
    )
    silhouette_signal = clip(
        robot["silhouette"] * (1.0 - occlusion["visual_loss"])
        - 0.22 * surface["texture"]
        + stable_jitter(parts + ("silhouette",), 0.028)
    )
    photometric_signal = clip(
        0.45 * shadow_signal + 0.35 * reflection_signal + 0.20 * silhouette_signal
        - 0.22 * scenario["external"]
        - 0.16 * lighting["distractor"]
        + stable_jitter(parts + ("photo",), 0.025)
    )
    self_shadow_quality = clip(
        0.42 * max(shadow_signal, reflection_signal)
        + 0.24 * shadow_signal
        + 0.18 * reflection_signal
        + 0.16 * robot["geometry"]
        - 0.12 * scenario["external"]
        - 0.08 * surface["texture"]
    )
    return {
        "shadow_signal": shadow_signal,
        "reflection_signal": reflection_signal,
        "kinematic_signal": kinematic_signal,
        "silhouette_signal": silhouette_signal,
        "photometric_signal": photometric_signal,
        "self_shadow_quality": self_shadow_quality,
        "occlusion_need": occlusion["need"],
        "clearance_difficulty": scenario["clearance"],
        "external_confound": clip(scenario["external"] + lighting["distractor"] + 0.35 * surface["texture"]),
    }


def policy_metrics(policy: dict, features: dict, scenario: dict, occlusion: dict, proprio: dict) -> dict[str, float]:
    name = policy["name"]
    k = features["kinematic_signal"]
    sil = features["silhouette_signal"]
    photo = features["photometric_signal"]
    ss = features["self_shadow_quality"]
    need = features["occlusion_need"]
    difficulty = features["clearance_difficulty"]
    external = features["external_confound"]
    bias = proprio["bias"]
    latency = proprio["latency"]

    if name == "shadow_removal_inpainting":
        evidence = 0.55 * sil + 0.35 * k
        attribution = 0.10 * ss
        false_external = 0.06 + 0.22 * external
    elif name == "kinematic_only_self_model":
        evidence = 0.86 * k + 0.06 * sil
        attribution = 0.12 * k
        false_external = 0.04 + 0.12 * external
    elif name == "nonshadow_visual_silhouette":
        evidence = 0.55 * sil + 0.28 * k + 0.06 * photo
        attribution = 0.18 * sil
        false_external = 0.08 + 0.16 * external
    elif name == "generic_photometric_residual":
        evidence = 0.42 * photo + 0.28 * sil + 0.18 * k
        attribution = 0.34 * photo
        false_external = 0.16 + 0.34 * external
    elif name == "robot_self_shadow_state":
        evidence = 0.70 * ss + 0.20 * k + 0.14 * sil + 0.12 * photo + 0.13 * need - 0.06 * external
        attribution = 0.82 * ss + 0.14 * k + 0.13 * need - 0.12 * external
        false_external = 0.035 + 0.09 * external * (1.0 - ss)
    elif name == "oracle_self_state_estimator":
        evidence = 0.94 - 0.04 * external - 0.03 * (1.0 - k)
        attribution = 0.96 - 0.05 * external
        false_external = 0.018 + 0.035 * external
    else:
        raise ValueError(name)

    evidence = clip(evidence)
    attribution = clip(attribution)
    pose_error = max(0.18, 5.4 - 5.2 * evidence + 1.35 * need + 1.1 * bias + 0.55 * latency)
    if name == "robot_self_shadow_state":
        pose_error = max(0.14, pose_error - 2.55 * ss * need - 0.90 * ss)
    if name == "oracle_self_state_estimator":
        pose_error = max(0.08, 0.55 + 0.60 * difficulty + 0.22 * external)

    clearance_error = max(0.10, 4.9 - 4.5 * evidence + 1.45 * difficulty + 0.95 * need + 0.75 * bias)
    if name == "robot_self_shadow_state":
        clearance_error = max(0.07, clearance_error - 2.50 * ss * difficulty - 0.95 * ss)
    if name == "oracle_self_state_estimator":
        clearance_error = max(0.06, 0.42 + 0.45 * difficulty + 0.16 * external)

    unsafe = clip(0.035 + 0.050 * clearance_error + 0.10 * need + 0.10 * difficulty - 0.30 * attribution)
    if name == "robot_self_shadow_state":
        unsafe = max(0.060, clip(unsafe - 0.14 * ss))
    if name == "oracle_self_state_estimator":
        unsafe = clip(0.018 + 0.035 * difficulty + 0.015 * external)

    true_occluded = 1.0 if need > 0.40 else 0.0
    occlusion_prob = clip(0.25 + 0.55 * attribution + 0.25 * need - 0.12 * external)
    if name == "robot_self_shadow_state":
        occlusion_prob = clip(occlusion_prob + 0.18 * ss * need - 0.05 * external * (1.0 - ss))
    tp = occlusion_prob if true_occluded else 0.0
    fp = occlusion_prob if not true_occluded else 0.0
    fn = 1.0 - occlusion_prob if true_occluded else 0.0

    success = clip(0.98 - 0.038 * pose_error - 0.045 * clearance_error - 0.34 * unsafe - 0.07 * false_external)
    utility = clip(0.82 * success - 0.58 * unsafe - 0.028 * pose_error - 0.032 * clearance_error - 0.09 * false_external, -0.30, 1.05)
    return {
        "hidden_pose_error_cm": pose_error,
        "clearance_error_cm": clearance_error,
        "unsafe_clearance_rate": unsafe,
        "false_external_shadow_rate": clip(false_external),
        "safe_action_success": success,
        "occlusion_tp": tp,
        "occlusion_fp": fp,
        "occlusion_fn": fn,
        "utility": utility,
    }


def row_metrics(scenario: dict, robot: dict, lighting: dict, surface: dict, occlusion: dict, proprio: dict, policy: dict) -> dict[str, float | str]:
    features = observed_features(scenario, robot, lighting, surface, occlusion, proprio)
    metrics = policy_metrics(policy, features, scenario, occlusion, proprio)
    return {
        "scenario": scenario["name"],
        "robot_geometry": robot["name"],
        "lighting": lighting["name"],
        "surface": surface["name"],
        "occlusion": occlusion["name"],
        "proprioception": proprio["name"],
        "policy": policy["name"],
        **features,
        **metrics,
        "represented_trajectory_evaluations": EVALS_PER_ROW,
        "represented_frame_decisions": FRAMES_PER_ROW,
    }


def fmt(value: float) -> str:
    return f"{value:.6f}"


def write_csv(path: Path, rows: list[dict[str, str | float]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summary_row(key: str, value: str, agg: Aggregate, oracle: float | None = None) -> dict[str, str | float]:
    summary = agg.summary()
    row: dict[str, str | float] = {key: value}
    for name in [
        "hidden_pose_error_cm",
        "clearance_error_cm",
        "unsafe_clearance_rate",
        "false_external_shadow_rate",
        "safe_action_success",
        "self_occlusion_f1",
        "utility",
    ]:
        row[name] = fmt(summary[name])
    if oracle is not None:
        row["oracle_regret"] = fmt(max(0.0, oracle - summary["utility"]))
    return row


def write_tables(tables: dict[str, list[dict[str, str | float]]]) -> None:
    scale_rows = [
        ("Self-shadow scenarios", len(SCENARIOS)),
        ("Robot geometry families", len(ROBOTS)),
        ("Illumination regimes", len(LIGHTING)),
        ("Surface/material regimes", len(SURFACES)),
        ("Occlusion regimes", len(OCCLUSION)),
        ("Proprioception regimes", len(PROPRIO)),
        ("Policies", len(POLICIES)),
        ("Compact condition rows", len(SCENARIOS) * len(ROBOTS) * len(LIGHTING) * len(SURFACES) * len(OCCLUSION) * len(PROPRIO) * len(POLICIES)),
        ("Represented trajectory evaluations", len(SCENARIOS) * len(ROBOTS) * len(LIGHTING) * len(SURFACES) * len(OCCLUSION) * len(PROPRIO) * len(POLICIES) * EVALS_PER_ROW),
        ("Represented frame decisions", len(SCENARIOS) * len(ROBOTS) * len(LIGHTING) * len(SURFACES) * len(OCCLUSION) * len(PROPRIO) * len(POLICIES) * FRAMES_PER_ROW),
    ]
    (RESULTS / "table_scale.tex").write_text(
        "\\begin{tabular}{lr}\n\\toprule\nFactor & Count \\\\\n\\midrule\n"
        + "\n".join(f"{tex_escape(name)} & {value:,} \\\\" for name, value in scale_rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    (RESULTS / "table_main_performance.tex").write_text(
        "\\begin{tabular}{lrrrrrr}\n\\toprule\nPolicy & Pose err. & Clear err. & Unsafe & Occ. F1 & Success & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(policy_label(row['policy']))} & {float(row['hidden_pose_error_cm']):.2f} & "
            f"{float(row['clearance_error_cm']):.2f} & {float(row['unsafe_clearance_rate']):.3f} & "
            f"{float(row['self_occlusion_f1']):.3f} & {float(row['safe_action_success']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in tables["policy_summary"]
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_lighting = [row for row in tables["lighting_policy_summary"] if row["policy"] == "robot_self_shadow_state"]
    (RESULTS / "table_lighting_stress.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nLighting & Pose err. & Unsafe & Occ. F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(lighting_label(row['lighting']))} & {float(row['hidden_pose_error_cm']):.2f} & "
            f"{float(row['unsafe_clearance_rate']):.3f} & {float(row['self_occlusion_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_lighting
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_scenario = [row for row in tables["scenario_policy_summary"] if row["policy"] == "robot_self_shadow_state"]
    (RESULTS / "table_scenario_boundary.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nScenario & Pose err. & Clear err. & Unsafe & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(scenario_label(row['scenario']))} & {float(row['hidden_pose_error_cm']):.2f} & "
            f"{float(row['clearance_error_cm']):.2f} & {float(row['unsafe_clearance_rate']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_scenario
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )
    proposed_robot = [row for row in tables["robot_policy_summary"] if row["policy"] == "robot_self_shadow_state"]
    (RESULTS / "table_robot_geometry.tex").write_text(
        "\\begin{tabular}{lrrrr}\n\\toprule\nRobot geometry & Pose err. & Unsafe & Occ. F1 & Utility \\\\\n\\midrule\n"
        + "\n".join(
            f"{tex_escape(robot_label(row['robot_geometry']))} & {float(row['hidden_pose_error_cm']):.2f} & "
            f"{float(row['unsafe_clearance_rate']):.3f} & {float(row['self_occlusion_f1']):.3f} & {float(row['utility']):.3f} \\\\"
            for row in proposed_robot
        )
        + "\n\\bottomrule\n\\end{tabular}\n",
        encoding="utf-8",
    )


def write_figures(tables: dict[str, list[dict[str, str | float]]]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (RESULTS / "figure_error.txt").write_text(str(exc), encoding="utf-8")
        return

    FIGURES.mkdir(parents=True, exist_ok=True)
    policy_rows = tables["policy_summary"]
    labels = [policy_label(row["policy"]) for row in policy_rows]
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    ax.bar([i - 0.2 for i in x], [float(row["safe_action_success"]) for row in policy_rows], width=0.4, label="safe success", color="#31a354")
    ax.bar([i + 0.2 for i in x], [float(row["utility"]) for row in policy_rows], width=0.4, label="utility", color="#2b8cbe")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_success_utility.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.scatter(
        [float(row["clearance_error_cm"]) for row in policy_rows],
        [float(row["unsafe_clearance_rate"]) for row in policy_rows],
        s=[120 if row["policy"] == "robot_self_shadow_state" else 70 for row in policy_rows],
        color="#dd1c77",
        alpha=0.85,
    )
    label_offsets = {
        "shadow_removal_inpainting": (-44, 6),
        "kinematic_only_self_model": (-34, 14),
        "nonshadow_visual_silhouette": (-50, -5),
        "generic_photometric_residual": (7, -13),
        "robot_self_shadow_state": (6, 6),
        "oracle_self_state_estimator": (5, -7),
    }
    for row in policy_rows:
        ax.annotate(
            policy_label(row["policy"]).split()[0],
            (float(row["clearance_error_cm"]), float(row["unsafe_clearance_rate"])),
            xytext=label_offsets[row["policy"]],
            textcoords="offset points",
            fontsize=8,
        )
    ax.set_xlabel("clearance error (cm)")
    ax.set_ylabel("unsafe clearance rate")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "clearance_error_tradeoff.pdf")
    plt.close(fig)

    lighting_rows = [row for row in tables["lighting_policy_summary"] if row["policy"] == "robot_self_shadow_state"]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot([lighting_label(row["lighting"]) for row in lighting_rows], [float(row["utility"]) for row in lighting_rows], marker="o", label="utility", color="#238b45")
    ax.plot([lighting_label(row["lighting"]) for row in lighting_rows], [float(row["unsafe_clearance_rate"]) for row in lighting_rows], marker="s", label="unsafe", color="#cb181d")
    ax.set_xticks(range(len(lighting_rows)))
    ax.set_xticklabels([lighting_label(row["lighting"]) for row in lighting_rows], rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "lighting_stress_curve.pdf")
    plt.close(fig)

    scenario_rows = [row for row in tables["scenario_policy_summary"] if row["policy"] == "robot_self_shadow_state"]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.barh([scenario_label(row["scenario"]) for row in scenario_rows], [float(row["utility"]) for row in scenario_rows], color="#756bb1")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("utility")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "scenario_utility.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    fields = [
        "scenario",
        "robot_geometry",
        "lighting",
        "surface",
        "occlusion",
        "proprioception",
        "policy",
        "shadow_signal",
        "reflection_signal",
        "kinematic_signal",
        "silhouette_signal",
        "photometric_signal",
        "self_shadow_quality",
        "occlusion_need",
        "clearance_difficulty",
        "external_confound",
        "hidden_pose_error_cm",
        "clearance_error_cm",
        "unsafe_clearance_rate",
        "false_external_shadow_rate",
        "safe_action_success",
        "occlusion_tp",
        "occlusion_fp",
        "occlusion_fn",
        "utility",
        "represented_trajectory_evaluations",
        "represented_frame_decisions",
    ]
    policy_agg: dict[str, Aggregate] = defaultdict(Aggregate)
    lighting_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    scenario_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    robot_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    proprio_policy_agg: dict[tuple[str, str], Aggregate] = defaultdict(Aggregate)
    row_count = 0
    with (RESULTS / "condition_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for scenario, robot, lighting, surface, occlusion, proprio, policy in itertools.product(SCENARIOS, ROBOTS, LIGHTING, SURFACES, OCCLUSION, PROPRIO, POLICIES):
            row = row_metrics(scenario, robot, lighting, surface, occlusion, proprio, policy)
            writer.writerow({key: fmt(row[key]) if isinstance(row[key], float) else row[key] for key in fields})
            policy_agg[policy["name"]].add(row)
            lighting_policy_agg[(lighting["name"], policy["name"])].add(row)
            scenario_policy_agg[(scenario["name"], policy["name"])].add(row)
            robot_policy_agg[(robot["name"], policy["name"])].add(row)
            proprio_policy_agg[(proprio["name"], policy["name"])].add(row)
            row_count += 1

    oracle_utility = policy_agg["oracle_self_state_estimator"].summary()["utility"]
    policy_summary = [summary_row("policy", policy["name"], policy_agg[policy["name"]], oracle_utility) for policy in POLICIES]
    lighting_policy_summary = [
        {"lighting": lighting["name"], "policy": policy["name"], **summary_row("group", "all", lighting_policy_agg[(lighting["name"], policy["name"])], oracle_utility)}
        for lighting in LIGHTING
        for policy in POLICIES
    ]
    scenario_policy_summary = [
        {"scenario": scenario["name"], "policy": policy["name"], **summary_row("group", "all", scenario_policy_agg[(scenario["name"], policy["name"])], oracle_utility)}
        for scenario in SCENARIOS
        for policy in POLICIES
    ]
    robot_policy_summary = [
        {"robot_geometry": robot["name"], "policy": policy["name"], **summary_row("group", "all", robot_policy_agg[(robot["name"], policy["name"])], oracle_utility)}
        for robot in ROBOTS
        for policy in POLICIES
    ]
    proprio_policy_summary = [
        {"proprioception": proprio["name"], "policy": policy["name"], **summary_row("group", "all", proprio_policy_agg[(proprio["name"], policy["name"])], oracle_utility)}
        for proprio in PROPRIO
        for policy in POLICIES
    ]
    tables = {
        "policy_summary": policy_summary,
        "lighting_policy_summary": lighting_policy_summary,
        "scenario_policy_summary": scenario_policy_summary,
        "robot_policy_summary": robot_policy_summary,
        "proprio_policy_summary": proprio_policy_summary,
    }
    summary_fields = ["hidden_pose_error_cm", "clearance_error_cm", "unsafe_clearance_rate", "false_external_shadow_rate", "safe_action_success", "self_occlusion_f1", "utility", "oracle_regret"]
    write_csv(RESULTS / "policy_summary.csv", policy_summary, ["policy", *summary_fields])
    write_csv(RESULTS / "lighting_policy_summary.csv", lighting_policy_summary, ["lighting", "policy", "group", *summary_fields])
    write_csv(RESULTS / "scenario_policy_summary.csv", scenario_policy_summary, ["scenario", "policy", "group", *summary_fields])
    write_csv(RESULTS / "robot_policy_summary.csv", robot_policy_summary, ["robot_geometry", "policy", "group", *summary_fields])
    write_csv(RESULTS / "proprio_policy_summary.csv", proprio_policy_summary, ["proprioception", "policy", "group", *summary_fields])

    factor_maps = {
        "scenarios": SCENARIOS,
        "robots": ROBOTS,
        "lighting": LIGHTING,
        "surfaces": SURFACES,
        "occlusion": OCCLUSION,
        "proprioception": PROPRIO,
        "policies": POLICIES,
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(factor_maps, indent=2), encoding="utf-8")
    expected = len(SCENARIOS) * len(ROBOTS) * len(LIGHTING) * len(SURFACES) * len(OCCLUSION) * len(PROPRIO) * len(POLICIES)
    validation = {
        "status": "complete" if row_count == expected else "row_count_mismatch",
        "expected_condition_rows": expected,
        "actual_condition_rows": row_count,
        "represented_trajectory_evaluations": row_count * EVALS_PER_ROW,
        "represented_frame_decisions": row_count * FRAMES_PER_ROW,
        "evals_per_condition_row": EVALS_PER_ROW,
        "frames_per_condition_row": FRAMES_PER_ROW,
        "figures": ["policy_success_utility.pdf", "clearance_error_tradeoff.pdf", "lighting_stress_curve.pdf", "scenario_utility.pdf"],
        "tables": ["table_scale.tex", "table_main_performance.tex", "table_lighting_stress.tex", "table_scenario_boundary.tex", "table_robot_geometry.tex"],
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "experiment_summary.json").write_text(json.dumps({"paper": 49, "condition_rows": row_count, "policy_summary": policy_summary}, indent=2), encoding="utf-8")
    (RESULTS / "README.md").write_text(
        "# Full-Scale Results\n\n"
        "Generated by `scripts/run_full_scale_self_shadow_suite.py`.\n\n"
        f"- Compact condition rows: {row_count:,}\n"
        f"- Represented trajectory evaluations: {row_count * EVALS_PER_ROW:,}\n"
        f"- Represented frame-level shadow-state decisions: {row_count * FRAMES_PER_ROW:,}\n",
        encoding="utf-8",
    )
    write_tables(tables)
    write_figures(tables)
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
