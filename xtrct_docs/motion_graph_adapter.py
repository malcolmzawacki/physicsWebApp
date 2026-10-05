"""Stable graph specifications for worksheets, independent of practice state."""
import random
import threading
from matplotlib.figure import Figure
from utils.generators.kinematics.motion_graph_generator import MotionGraphGenerator

_render_lock = threading.Lock()


class WorksheetMotionGraphs(MotionGraphGenerator):
    """Always sample all six motion shapes; Hard is an internal compatibility value.

    Worksheet interpretation has no pedagogical difficulty tiers. Even legacy
    Easy/Medium requests use the full pool so slowing-down cases are never omitted.
    """
    def __init__(self):
        super().__init__()
        self._remaining = {}
        self._last = {}

    def choose_problem_dict(self, problem_type, difficulty="Hard"):
        if problem_type not in self.get_problem_types():
            raise ValueError("Unsupported graph family")
        difficulty = self.FIXED_DIFFICULTY
        candidates = self.graph_types
        key = (problem_type, difficulty)
        remaining = self._remaining.setdefault(key, [])
        if not remaining:
            remaining.extend(candidates)
        choices = [shape for shape in remaining if shape != self._last.get(key)] or remaining
        graph_type = random.choice(choices)
        remaining.remove(graph_type)
        self._last[key] = graph_type
        direction = "Positive" if graph_type.endswith("positive") else "Negative"
        motion = "Constant Velocity" if graph_type.startswith("linear") else "Slowing Down" if graph_type.startswith("decelerating") else "Speeding Up"
        units = ["Direction", "Motion State"]
        return {"question": "Circle one choice in each row for the graph below.",
                "answers": [direction, motion], "units": units,
                "diagram_data": {"graph_type": graph_type},
                "button_options": self.get_answer_options(units),
                "side_by_side": True, "graph_doc_width": 2.8}

    def generate_diagram(self, diagram_data, problem_type, difficulty):
        # Explicit Figure construction avoids pyplot managers and practice session writes.
        with _render_lock:
            method = self.generate_position_time_graph if problem_type == "Position-Time Graph" else self.generate_velocity_time_graph
            figure, _, _ = method(diagram_data["graph_type"], rowsize=3.2, colsize=2.4,
                                  figure_factory=lambda size: Figure(figsize=size))
            return figure
