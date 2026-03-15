import math
import random

from utils.generators.base_generator import BaseGenerator
from utils.object_library import pick_rotation_object, sample_lever_arm


class TorqueGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="torque_")
        # Keep visual scaling subtle so diagrams stay legible.
        self.RADIUS_SCALE_MIN = 1.00
        self.RADIUS_SCALE_MAX = 1.35
        self.FORCE_SCALE_MIN = 0.90
        self.FORCE_SCALE_MAX = 1.25

    def _value_range(self, difficulty: str) -> int:
        base = self.get_difficulty_range(difficulty)
        if difficulty == "Easy":
            return max(6, base)
        if difficulty == "Hard":
            return max(20, base)
        return max(12, base)

    def _pick_angle(self, difficulty: str) -> int:
        if difficulty == "Easy":
            return 90
        if difficulty == "Hard":
            return random.choice([15, 30, 45, 60, 75])
        return random.choice([30, 45, 60, 90])

    def _torque(self, force: float, radius: float, angle_deg: float) -> float:
        return force * radius * math.sin(math.radians(angle_deg))

    def _pick_object(self) -> dict:
        return pick_rotation_object()

    def _format_find_unknown_prompt(
        self, noun: str, context: str, force: float, radius: float, angle_deg: int
    ) -> str:
        if angle_deg == 90:
            angle_phrase = "perpendicular to the lever arm"
        else:
            angle_phrase = f"at an angle of {angle_deg} degrees relative to the lever arm"
        return (
            f"{context} A {noun} is pushed with a {force:.1f} N force applied {radius:.2f} m from the pivot, "
            f"{angle_phrase}. What torque is produced?"
        )

    def _new_interaction(
        self,
        difficulty: str,
        *,
        force_min: float = 5.0,
        force_pad: float = 5.0,
        angle: int | None = None,
        direction: str | None = None,
    ) -> dict:
        max_val = self._value_range(difficulty)
        force = random.uniform(force_min, max_val + force_pad)
        radius = sample_lever_arm(self._pick_object(), difficulty)
        picked_angle = self._pick_angle(difficulty) if angle is None else angle
        picked_direction = direction or random.choice(["CCW", "CW"])
        sign = 1 if picked_direction == "CCW" else -1
        torque_signed = round(sign * self._torque(force, radius, picked_angle), 2)
        return {
            "force": round(force, 2),
            "radius": round(radius, 3),
            "angle": int(picked_angle),
            "direction": picked_direction,
            "torque_signed": torque_signed,
            "torque_mag": round(abs(torque_signed), 2),
        }

    def _build_case(self, problem_type: str, difficulty: str) -> dict:
        obj = self._pick_object()

        if problem_type == "Perpendicular Force":
            interaction = self._new_interaction(
                difficulty, force_min=5.0, force_pad=5.0, angle=90
            )
            return {"kind": "single_torque", "object": obj, "interactions": [interaction]}

        if problem_type == "Angled Force":
            interaction = self._new_interaction(
                difficulty, force_min=6.0, force_pad=8.0
            )
            return {"kind": "single_torque", "object": obj, "interactions": [interaction]}

        if problem_type == "Net Torque":
            first = self._new_interaction(
                difficulty, force_min=5.0, force_pad=5.0, angle=90, direction="CW"
            )
            second = self._new_interaction(
                difficulty, force_min=5.0, force_pad=5.0, angle=90, direction="CCW"
            )
            return {
                "kind": "net_torque",
                "object": obj,
                "interactions": [first, second],
                "net_torque": round(first["torque_signed"] + second["torque_signed"], 2),
            }

        if problem_type == "Torque Comparison (More/Less/Same)":
            left = self._new_interaction(difficulty)
            right = self._new_interaction(difficulty)
            comparison = "Same"
            if left["torque_mag"] > right["torque_mag"]:
                comparison = "More"
            elif left["torque_mag"] < right["torque_mag"]:
                comparison = "Less"
            return {
                "kind": "comparison",
                "object": obj,
                "left": left,
                "right": right,
                "comparison_answer": comparison,
            }

        if problem_type == "Torque Ranking (Least to Greatest)":
            labels = self._ranking_labels_for_difficulty(difficulty)
            options = [self._new_interaction(difficulty) for _ in labels]
            labeled = list(zip(labels, options))
            sorted_labels = [
                name for name, _ in sorted(labeled, key=lambda item: item[1]["torque_mag"])
            ]

            return {
                "kind": "ranking",
                "object": obj,
                "labeled_interactions": labeled,
                "ranking_order": sorted_labels,
            }

        raise ValueError(f"Unknown problem type '{problem_type}'")

    def _render_find_unknown(self, case: dict) -> dict:
        obj = case["object"]

        if case["kind"] == "single_torque":
            interaction = case["interactions"][0]
            question = (
                f"{self._format_find_unknown_prompt(obj['name'], obj['context'], interaction['force'], interaction['radius'], interaction['angle'])} "
                "Use the sign convention + = CCW, - = CW."
            )
            return {
                "question": question,
                "answers": [interaction["torque_signed"]],
                "units": ["Torque (N*m)"],
                "diagram_data": interaction,
                "extras": {"layout": "find_unknown", "case": case},
            }

        if case["kind"] == "net_torque":
            first, second = case["interactions"]
            question = (
                f"{obj['context']} A {obj['name']} has two perpendicular forces applied. "
                f"Force A is {first['force']:.1f} N at {first['radius']:.2f} m (clockwise). "
                f"Force B is {second['force']:.1f} N at {second['radius']:.2f} m (counterclockwise). "
                "What is the net torque? Use + = CCW, - = CW."
            )
            return {
                "question": question,
                "answers": [case["net_torque"]],
                "units": ["Net Torque (N*m)"],
                "diagram_data": {
                    "force": first["force"],
                    "radius": first["radius"],
                    "angle": 90,
                    "direction": "CW",
                    "force2": second["force"],
                    "radius2": second["radius"],
                    "direction2": "CCW",
                },
                "extras": {"layout": "find_unknown", "case": case},
            }

        raise ValueError(f"Unsupported case kind for find_unknown layout: {case['kind']}")

    def _render_more_less_same(self, case: dict) -> dict:
        obj = case["object"]
        left = case["left"]
        right = case["right"]
        question = (
            f"{obj['context']} Compare torque magnitudes for two pushes on a {obj['name']}. "
            f"Case A: F = {left['force']:.1f} N, r = {left['radius']:.2f} m, angle = {left['angle']} degrees. "
            f"Case B: F = {right['force']:.1f} N, r = {right['radius']:.2f} m, angle = {right['angle']} degrees. "
            "Relative to Case B, does Case A produce more, less, or the same torque magnitude?"
        )
        return {
            "question": question,
            "answers": [case["comparison_answer"]],
            "units": ["Torque Magnitude Comparison"],
            "button_options": {0: ["More", "Less", "Same"]},
            "diagram_data": {
                "mode": "multi",
                "panels": [
                    {"label": "A", "interaction": left},
                    {"label": "B", "interaction": right},
                ],
            },
            "extras": {"layout": "more_less_same", "case": case},
        }

    def _render_rank(self, case: dict) -> dict:
        obj = case["object"]
        ranking_order = case["ranking_order"]
        segments = []
        for label, interaction in case["labeled_interactions"]:
            segments.append(
                f"{label}: F = {interaction['force']:.1f} N, r = {interaction['radius']:.2f} m, angle = {interaction['angle']} degrees"
            )
        listing = "; ".join(segments)
        slot_labels = self._rank_slot_labels(len(ranking_order))
        option_labels = [label for label, _ in case["labeled_interactions"]]
        question = (
            f"{obj['context']} Rank the torque magnitudes for a {obj['name']} from least to greatest. "
            f"{listing}."
        )
        return {
            "question": question,
            "answers": ranking_order,
            "units": slot_labels,
            "button_options": {idx: option_labels for idx, _ in enumerate(slot_labels)},
            "answer_input_mode": "dropdown",
            "diagram_data": {
                "mode": "multi",
                "panels": [
                    {"label": label, "interaction": interaction}
                    for label, interaction in case["labeled_interactions"]
                ],
            },
            "extras": {"layout": "rank", "case": case},
        }

    def _ranking_labels_for_difficulty(self, difficulty: str) -> list[str]:
        if difficulty == "Easy":
            count = 3
        elif difficulty == "Hard":
            count = 5
        else:
            count = 4
        return [chr(ord("A") + idx) for idx in range(count)]

    def _rank_slot_labels(self, count: int) -> list[str]:
        if count <= 1:
            return ["Only Option"]
        if count == 2:
            return ["Least", "Most"]
        if count == 3:
            return ["Least", "Middle", "Most"]

        labels = []
        for idx in range(count):
            if idx == 0:
                labels.append("Least")
            elif idx == count - 1:
                labels.append("Most")
            elif idx == 1:
                labels.append("Second Least")
            elif idx == count - 2:
                labels.append("Second Most")
            elif count % 2 == 1 and idx == count // 2:
                labels.append("Middle")
            else:
                labels.append(f"Position {idx + 1}")
        return labels

    def perpendicular_force(self, difficulty: str) -> dict:
        return self._render_find_unknown(self._build_case("Perpendicular Force", difficulty))

    def angled_force(self, difficulty: str) -> dict:
        return self._render_find_unknown(self._build_case("Angled Force", difficulty))

    def net_torque(self, difficulty: str) -> dict:
        return self._render_find_unknown(self._build_case("Net Torque", difficulty))

    def compare_torque_magnitudes(self, difficulty: str) -> dict:
        return self._render_more_less_same(
            self._build_case("Torque Comparison (More/Less/Same)", difficulty)
        )

    def rank_torque_magnitudes(self, difficulty: str) -> dict:
        return self._render_rank(
            self._build_case("Torque Ranking (Least to Greatest)", difficulty)
        )

    def choose_problem_dict(self, problem_type: str, difficulty: str) -> dict:
        if problem_type == "Perpendicular Force":
            return self.perpendicular_force(difficulty)
        if problem_type == "Angled Force":
            return self.angled_force(difficulty)
        if problem_type == "Net Torque":
            return self.net_torque(difficulty)
        if problem_type == "Torque Comparison (More/Less/Same)":
            return self.compare_torque_magnitudes(difficulty)
        if problem_type == "Torque Ranking (Least to Greatest)":
            return self.rank_torque_magnitudes(difficulty)
        raise ValueError(f"Unknown problem type '{problem_type}'")

    def stored_metadata(self) -> dict[str, dict]:
        return {
            "Perpendicular Force": {
                "honors_equation": r"\tau = rF",
                "conceptual_equation": r"\tau = rF \quad (\theta = 90^\circ)",
                "tags": ["rotation", "torque", "perpendicular"],
            },
            "Angled Force": {
                "honors_equation": r"\tau = rF\sin\theta",
                "conceptual_equation": r"\tau = rF\sin\theta",
                "tags": ["rotation", "torque", "angle"],
            },
            "Net Torque": {
                "honors_equation": r"\tau_{net} = \tau_{ccw} - \tau_{cw}",
                "conceptual_equation": r"\tau_{net} = \tau_{ccw} - \tau_{cw}",
                "tags": ["rotation", "torque", "net"],
            },
            "Torque Comparison (More/Less/Same)": {
                "honors_equation": r"|\tau| = rF\sin\theta",
                "conceptual_equation": r"\text{Compare } |\tau_A| \text{ and } |\tau_B| \text{ using } rF\sin\theta",
                "tags": ["rotation", "torque", "conceptual", "comparison"],
            },
            "Torque Ranking (Least to Greatest)": {
                "honors_equation": r"|\tau| = rF\sin\theta",
                "conceptual_equation": r"\text{Rank multiple } |\tau| \text{ values using } rF\sin\theta",
                "tags": ["rotation", "torque", "conceptual", "ranking"],
            },
        }

    def generate_diagram(self, diagram_data, problem_type: str, difficulty: str):
        if not isinstance(diagram_data, dict):
            return None

        import matplotlib.pyplot as plt
        if diagram_data.get("mode") == "multi" and isinstance(diagram_data.get("panels"), list):
            panels = diagram_data["panels"]
            count = len(panels)
            if count == 0:
                return None

            interactions = [panel.get("interaction", {}) for panel in panels]
            max_force = max(float(item.get("force", 1.0)) for item in interactions)
            max_radius = max(float(item.get("radius", 1.0)) for item in interactions)

            # Keep all comparison/ranking cases in one row for side-by-side scanning.
            fig, axes = plt.subplots(1, count, figsize=(count * 3.6, 4.0))
            axes_flat = list(axes) if isinstance(axes, (list, tuple)) else [axes]
            if hasattr(axes, "flatten"):
                axes_flat = list(axes.flatten())
            fig.patch.set_facecolor("#121417")
            fixed_limits = self._multi_panel_limits(max_force=max_force, max_radius=max_radius)
            panel_labels = []

            for i, panel in enumerate(panels):
                ax = axes_flat[i]
                label = panel.get("label", f"Case {i + 1}")
                panel_labels.append(str(label))
                interaction = panel.get("interaction", {})
                angle_style = "external" if i % 2 == 1 else "internal"
                self._draw_single_interaction_diagram(
                    ax,
                    interaction,
                    max_force=max_force,
                    max_radius=max_radius,
                    angle_style=angle_style,
                    show_values=True,
                    fixed_limits=fixed_limits,
                )

            fig.tight_layout(rect=(0.0, 0.11, 1.0, 0.88))
            # Figure-level labels stay aligned at the top of each subplot column.
            for i, ax in enumerate(axes_flat[:count]):
                pos = ax.get_position()
                fig.text(
                    (pos.x0 + pos.x1) * 0.5,
                    0.92,
                    f"Case {panel_labels[i]}",
                    ha="center",
                    va="center",
                    fontsize=10.5,
                    color="#E8EDF3",
                )
            return fig

        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        fig.patch.set_facecolor("#121417")
        max_force = max(
            float(diagram_data.get("force", 1.0)),
            float(diagram_data.get("force2", 0.0) or 0.0),
        )
        max_radius = max(
            float(diagram_data.get("radius", 1.0)),
            float(diagram_data.get("radius2", 0.0) or 0.0),
        )
        self._draw_single_interaction_diagram(
            ax,
            diagram_data,
            max_force=max_force,
            max_radius=max_radius,
            angle_style="internal",
            show_values=True,
        )

        force2 = diagram_data.get("force2")
        radius2 = diagram_data.get("radius2")
        direction2 = diagram_data.get("direction2", "CCW")
        if force2 is not None and radius2 is not None:
            self._draw_secondary_force(
                ax,
                force2,
                radius2,
                direction2,
                max_force=max_force,
                max_radius=max_radius,
            )
            r2_vis = self._scaled_length(
                float(radius2),
                max_radius,
                minimum=self.RADIUS_SCALE_MIN,
                maximum=self.RADIUS_SCALE_MAX,
            )
            f2_vis = self._scaled_length(
                float(force2),
                max_force,
                minimum=self.FORCE_SCALE_MIN,
                maximum=self.FORCE_SCALE_MAX,
            )
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            ax.set_xlim(min(xmin, -r2_vis - 0.6), xmax)
            ax.set_ylim(min(ymin, -abs(f2_vis) - 0.6), max(ymax, abs(f2_vis) + 0.6))

        fig.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
        return fig

    def _draw_single_interaction_diagram(
        self,
        ax,
        interaction: dict,
        title: str | None = None,
        *,
        max_force: float = 1.0,
        max_radius: float = 1.0,
        angle_style: str = "internal",
        show_values: bool = True,
        fixed_limits: tuple[float, float, float, float] | None = None,
    ) -> None:
        force = float(interaction.get("force", 1.0))
        radius = float(interaction.get("radius", 1.0))
        angle = float(interaction.get("angle", 90.0))
        direction = interaction.get("direction", "CCW")

        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_facecolor("#1A1E24")

        radius_vis = self._scaled_length(
            radius,
            max_radius,
            minimum=self.RADIUS_SCALE_MIN,
            maximum=self.RADIUS_SCALE_MAX,
        )
        force_vis = self._scaled_length(
            force,
            max_force,
            minimum=self.FORCE_SCALE_MIN,
            maximum=self.FORCE_SCALE_MAX,
        )
        ref_len = max(radius_vis, force_vis)
        r_arrow_thickness = 0.08
        f_arrow_thickness = 0.08
        pivot_x = 0.0
        pivot_y = 0.0
        tip_x = radius_vis
        tip_y = 0.0

        # Radius vector as an arrow.
        ax.arrow(
            pivot_x,
            pivot_y,
            tip_x,
            tip_y,
            head_width=0.08,
            head_length=0.12,
            length_includes_head=True,
            color="#6EC1E4",
            linewidth=2.6,
        )
        ax.scatter([pivot_x], [pivot_y], s=70, color="#F2C14E", zorder=3)

        angle_rad = math.radians(angle)
        fx = math.cos(angle_rad)
        fy = math.sin(angle_rad)
        if direction == "CW":
            fy *= -1

        # Force vector with length scaled to force magnitude.
        ax.arrow(
            tip_x,
            tip_y,
            fx * force_vis,
            fy * force_vis,
            head_width=0.08,
            head_length=0.12,
            length_includes_head=True,
            color="#E76F51",
            linewidth=2,
        )

        self._draw_angle_annotation(
            ax,
            tip_x=tip_x,
            tip_y=tip_y,
            angle_deg=angle,
            direction=direction,
            style=angle_style,
            ref_len=max(radius_vis, force_vis),
        )

        # Label rules:
        # - r label: always below the radius arrow by > arrow thickness.
        # - F label: always to the side of the force-arrow tip by > arrow thickness.
        r_label_offset = r_arrow_thickness + 0.06
        ax.text(
            tip_x * 0.52,
            -(r_label_offset + 0.01),
            "r",
            color="#9ADAF0",
            fontsize=11,
            ha="center",
            va="top",
        )
        fx_tip = tip_x + fx * force_vis
        fy_tip = tip_y + fy * force_vis
        normal_x = -fy
        normal_y = fx
        normal_mag = max((normal_x**2 + normal_y**2) ** 0.5, 1e-6)
        normal_x /= normal_mag
        normal_y /= normal_mag
        force_label_offset = f_arrow_thickness + 0.07
        ax.text(
            fx_tip + normal_x * force_label_offset,
            fy_tip + normal_y * force_label_offset,
            "F",
            color="#FFB4A6",
            fontsize=11,
            ha="center",
            va="center",
        )

        if show_values:
            ax.text(
                0.5,
                -0.23,
                f"r = {radius:.2f} m\nF = {force:.1f} N\ntheta = {int(angle)} deg",
                transform=ax.transAxes,
                ha="center",
                va="top",
                fontsize=9.4,
                color="#E8EDF3",
                bbox={"facecolor": "#2A3038", "edgecolor": "#475463", "boxstyle": "round,pad=0.38"},
                clip_on=False,
            )

        right_extent = tip_x + abs(fx * force_vis) + 0.5
        top_extent = abs(fy * force_vis) + 0.55
        left_extent = 0.65
        if fixed_limits is not None:
            ax.set_xlim(fixed_limits[0], fixed_limits[1])
            ax.set_ylim(fixed_limits[2], fixed_limits[3])
        else:
            ax.set_xlim(-left_extent, right_extent)
            ax.set_ylim(-top_extent, top_extent)

    def _draw_secondary_force(
        self,
        ax,
        force2: float,
        radius2: float,
        direction2: str,
        *,
        max_force: float,
        max_radius: float,
    ) -> None:
        r2_val = float(radius2)
        f2_val = float(force2)
        r2 = self._scaled_length(
            r2_val,
            max_radius,
            minimum=self.RADIUS_SCALE_MIN,
            maximum=self.RADIUS_SCALE_MAX,
        )
        force_vis = self._scaled_length(
            f2_val,
            max_force,
            minimum=self.FORCE_SCALE_MIN,
            maximum=self.FORCE_SCALE_MAX,
        )

        # Second radius also as an arrow.
        ax.arrow(
            0,
            0,
            -r2,
            0,
            head_width=0.08,
            head_length=0.12,
            length_includes_head=True,
            color="#6EC1E4",
            linewidth=2.2,
            alpha=0.8,
        )
        dir_sign = 1 if direction2 == "CCW" else -1
        ax.arrow(
            -r2,
            0,
            0,
            force_vis * dir_sign,
            head_width=0.08,
            head_length=0.12,
            length_includes_head=True,
            color="#2A9D8F",
            linewidth=2,
        )
        r2_label_offset = 0.10 + 0.05 * max(r2, force_vis)
        ax.text(-r2 * 0.5, -r2_label_offset, "r2", color="#9ADAF0", fontsize=10, ha="center")
        ax.text(
            -r2 - 0.10,
            force_vis * dir_sign * 0.58,
            "F2",
            color="#7EE0BF",
            fontsize=10,
            ha="center",
        )
        ax.text(
            0.03,
            0.03,
            f"r2 = {r2_val:.2f} m\nF2 = {f2_val:.1f} N",
            transform=ax.transAxes,
            va="bottom",
            fontsize=8.4,
            color="#E8EDF3",
            bbox={"facecolor": "#2A3038", "edgecolor": "#475463", "boxstyle": "round,pad=0.25"},
        )

    def _draw_angle_annotation(
        self,
        ax,
        *,
        tip_x: float,
        tip_y: float,
        angle_deg: float,
        direction: str,
        style: str,
        ref_len: float,
    ) -> None:
        sweep = angle_deg if direction == "CCW" else -angle_deg
        base_radius = max(0.18, ref_len * 0.18)
        arc_radius = base_radius if style == "internal" else base_radius * 1.35
        step = 3 if sweep >= 0 else -3
        if abs(step) > abs(sweep) and sweep != 0:
            step = int(sweep)

        if style == "external":
            ext = max(0.35, ref_len * 0.40)
            ax.plot(
                [tip_x, tip_x + ext],
                [tip_y, tip_y],
                color="#8D99AE",
                linestyle="--",
                linewidth=1.1,
                alpha=0.95,
            )

        samples = [math.radians(t) for t in range(0, int(sweep) + step, step)] if sweep != 0 else [0.0]
        arc_x = [tip_x + arc_radius * math.cos(t) for t in samples]
        arc_y = [tip_y + arc_radius * math.sin(t) for t in samples]
        ax.plot(arc_x, arc_y, color="#8D99AE", linewidth=1.4)

        # Place the degree label along the bisector of the exterior angle
        # between r-hat (positive x) and F-hat to reduce overlap with the force arrow.
        sweep_rad = math.radians(sweep)
        u_r_x, u_r_y = 1.0, 0.0
        u_f_x, u_f_y = math.cos(sweep_rad), math.sin(sweep_rad)
        b_ext_x = u_r_x - u_f_x
        b_ext_y = u_r_y - u_f_y
        b_norm = math.hypot(b_ext_x, b_ext_y)
        if b_norm < 1e-6:
            # Degenerate near-zero angle fallback.
            b_ext_x, b_ext_y = 0.0, -1.0 if direction == "CCW" else 1.0
            b_norm = 1.0
        b_ext_x /= b_norm
        b_ext_y /= b_norm

        label_radius = arc_radius + max(0.26, ref_len * 0.18)
        ax.text(
            tip_x + b_ext_x * label_radius,
            tip_y + b_ext_y * label_radius,
            f"{int(abs(angle_deg))} deg",
            color="#CBD5E1",
            fontsize=8.4,
            ha="center",
            va="center",
        )

    def _scaled_length(self, value: float, max_value: float, *, minimum: float, maximum: float) -> float:
        if max_value <= 0:
            return (minimum + maximum) * 0.5
        ratio = max(0.0, min(1.0, value / max_value))
        return minimum + ratio * (maximum - minimum)

    def _multi_panel_limits(self, *, max_force: float, max_radius: float) -> tuple[float, float, float, float]:
        r_vis = self._scaled_length(
            max_radius,
            max_radius,
            minimum=self.RADIUS_SCALE_MIN,
            maximum=self.RADIUS_SCALE_MAX,
        )
        f_vis = self._scaled_length(
            max_force,
            max_force,
            minimum=self.FORCE_SCALE_MIN,
            maximum=self.FORCE_SCALE_MAX,
        )
        x_min = -0.85
        x_max = r_vis + f_vis + 0.70
        y_bound = f_vis + 0.80
        return (x_min, x_max, -y_bound, y_bound)
