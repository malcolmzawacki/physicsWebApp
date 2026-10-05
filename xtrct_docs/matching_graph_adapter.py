"""Printable matching sets with stable curves and shuffled, distinct choices."""
import io
import random
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from utils.generators.base_generator import BaseGenerator
from utils.generators.kinematics.motion_graph_generator import MotionGraphGenerator
from xtrct_docs.motion_graph_adapter import _render_lock


class WorksheetMatchingGraphs(BaseGenerator):
    DIFFICULTIES = ("Standard",)

    def __init__(self):
        super().__init__("worksheet_matching")
        self._remaining = {}
        self._last = {}

    def stored_metadata(self):
        return {"Position-Time First": {}, "Velocity-Time First": {}}

    def choose_problem_dict(self, problem_type, difficulty):
        if problem_type not in self.get_problem_types() or difficulty not in self.DIFFICULTIES:
            raise ValueError("Unsupported matching graph request")
        shapes = MotionGraphGenerator().graph_types
        remaining = self._remaining.setdefault(problem_type, [])
        if not remaining:
            remaining.extend(shapes)
        correct = random.choice([s for s in remaining if s != self._last.get(problem_type)] or remaining)
        remaining.remove(correct)
        self._last[problem_type] = correct
        choices = [correct] + random.sample([s for s in shapes if s != correct], 2)
        random.shuffle(choices)
        source, target = ("position–time", "velocity–time") if problem_type == "Position-Time First" else ("velocity–time", "position–time")
        return {"question": f"Match the given {source} graph to the {target} graph A, B, or C. Write your answer: ______.",
                "answers": ["ABC"[choices.index(correct)]], "units": ["Option"],
                "diagram_data": {"primary": correct, "choices": choices}}

    def generate_diagram(self, diagram_data, problem_type, difficulty):
        with _render_lock:
            generator = MotionGraphGenerator()
            primary = generator.generate_position_time_graph if problem_type == "Position-Time First" else generator.generate_velocity_time_graph
            option = generator.generate_velocity_time_graph if problem_type == "Position-Time First" else generator.generate_position_time_graph
            figure = Figure(figsize=(6.4, 4.8), facecolor="white")
            for index, (method, shape, label) in enumerate([(primary, diagram_data["primary"], "Given graph")] +
                    [(option, shape, f"Option {letter}") for letter, shape in zip("ABC", diagram_data["choices"])]):
                source, _, _ = method(shape, rowsize=3.2, colsize=2.2, figure_factory=lambda size: Figure(figsize=size))
                if method == generator.generate_velocity_time_graph:
                    # Match the derivative of the existing position curve exactly.
                    ax = source.axes[0]
                    line = ax.lines[0]
                    scale = 0.75 if shape == "linear_negative" else 1 if shape == "linear_positive" else 2
                    line.set_ydata(line.get_ydata() * scale)
                    ax.relim()
                    ax.autoscale_view(scalex=False)
                source.axes[0].set_title(label, color="black")
                buffer = io.BytesIO()
                source.savefig(buffer, format="png", dpi=180, bbox_inches="tight", facecolor="white")
                buffer.seek(0)
                ax = figure.add_subplot(2, 2, index + 1)
                ax.imshow(mpimg.imread(buffer))
                ax.axis("off")
                source.clear()
            figure.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=.08, wspace=.06)
            return figure
