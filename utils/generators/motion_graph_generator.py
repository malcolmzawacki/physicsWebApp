# utils/generators/motion_graph_generator.py
import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from utils.generators.base_generator import BaseGenerator
from utils.ui_state import State
from typing import Optional, Any, Tuple

class MotionGraphGenerator(BaseGenerator):
    def __init__(self):
        super().__init__(state_prefix="motion_graph_")
        self.graph_types = ["linear_positive", "linear_negative", 
                           "accelerating_positive", "accelerating_negative",
                           "decelerating_positive", "decelerating_negative"]
        self.doc_graph_width = 2.4
        self.doc_figsize = (2.6, 1.9)
    
    def get_difficulty_range(self, difficulty):
        # Required by BaseGenerator
        if difficulty == "Easy":
            return 5
        elif difficulty == "Hard":
            return 20
        return 10

    def set_doc_graph_dimensions(self, width_inches: float, figsize: Tuple[float, float]):
        """Update the preferred DOCX graph width and Matplotlib figure size."""
        self.doc_graph_width = width_inches
        self.doc_figsize = figsize

    def _apply_print_style(self, ax, title, y_label):
        ax.set_title(title, color="black")
        ax.set_xlabel("Time (s)", color="black")
        ax.set_ylabel(y_label, color="black")
        ax.tick_params(axis='both', colors="black")
        ax.grid(True, color="#BFBFBF", linewidth=0.5)
        ax.set_facecolor("white")
        ax.figure.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_color("black")
        ax.figure.tight_layout()

    def generate_position_time_graph(self, graph_type=None, rowsize=3, colsize=2.5):
        """Generate a position-time graph optimized for print output"""
        if graph_type is None:
            graph_type = random.choice(self.graph_types)

        fig, ax = plt.subplots(figsize=(rowsize, colsize))
        ax.set_xlim(0, 5)
        t = np.linspace(0, 5, 100)

        if graph_type == "linear_positive":
            position = 2 * t + 1
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            position = -1.5 * t + 5
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            position = t**2
            correct_direction = "Positive"
            correct_motion_state = "Speeding Up"
        elif graph_type == "decelerating_positive":
            position = -t * (t - 10) + 5
            correct_direction = "Positive"
            correct_motion_state = "Slowing Down"
        elif graph_type == "decelerating_negative":
            position = t * (t - 10) - 5
            correct_direction = "Negative"
            correct_motion_state = "Slowing Down"
        else:
            position = -t**2 + 5
            correct_direction = "Negative"
            correct_motion_state = "Speeding Up"

        ax.plot(t, position, color="black", linewidth=2)
        self._apply_print_style(ax, "Position-Time Graph", "Position (m)")

        return fig, correct_direction, correct_motion_state

    def generate_velocity_time_graph(self, graph_type=None, rowsize=3, colsize=2.5):
        """Generate a velocity-time graph optimized for print output"""
        if graph_type is None:
            graph_type = random.choice(self.graph_types)

        fig, ax = plt.subplots(figsize=(rowsize, colsize))
        t = np.linspace(0, 5, 100)
        ax.set_xlim(0, 5)

        if graph_type == "linear_positive":
            velocity = np.ones_like(t) * 2
            correct_direction = "Positive"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "linear_negative":
            velocity = np.ones_like(t) * -2
            correct_direction = "Negative"
            correct_motion_state = "Constant Velocity"
        elif graph_type == "accelerating_positive":
            velocity = t
            correct_direction = "Positive"
            correct_motion_state = "Speeding Up"
        elif graph_type == "decelerating_positive":
            velocity = -t + 5
            correct_direction = "Positive"
            correct_motion_state = "Slowing Down"
        elif graph_type == "decelerating_negative":
            velocity = t - 5
            correct_direction = "Negative"
            correct_motion_state = "Slowing Down"
        else:
            velocity = -t
            correct_direction = "Negative"
            correct_motion_state = "Speeding Up"

        ax.plot(t, velocity, color="black", linewidth=2)
        self._apply_print_style(ax, "Velocity-Time Graph", "Velocity (m/s)")

        return fig, correct_direction, correct_motion_state

    def generate_diagram(
            self, 
            diagram_data: Any, 
            problem_type: str, 
            difficulty: str
            ) -> Optional['matplotlib.figure.Figure']:
        
        return diagram_data  # Just return the figure that was passed in
    
    
    def display_current_graph(self):
        state = State(self.state_prefix.rstrip("_"))
        current_graph = state.get("current_graph")
        if current_graph is not None:
            st.pyplot(current_graph)


    def get_answer_options(
            self, 
            units: list[str]
            ) -> dict[int, list[str]]:
        
        options = {}

        for i, unit in enumerate(units):
            if unit == "Direction":
                options[i] = ["Positive", "Negative"]
            elif unit == "Motion State":
                options[i] = ["Constant Velocity", "Speeding Up", "Slowing Down"]

        return options
    
    def choose_problem_dict(self, problem_type, difficulty, graph_type=None):
        chosen_type = graph_type or random.choice(self.graph_types)
        units = ["Direction", "Motion State"]
        options = self.get_answer_options(units)

        if problem_type == "Position-Time Graph":
            fig, direction, motion_state = self.generate_position_time_graph(
                chosen_type, rowsize=self.doc_figsize[0], colsize=self.doc_figsize[1]
            )
            State(self.state_prefix.rstrip("_")).set("current_graph", fig)
            question = "Analyze the position-time graph shown to the left. What is the direction and state of motion?"
            answers = [direction, motion_state]

        elif problem_type == "Velocity-Time Graph":
            fig, direction, motion_state = self.generate_velocity_time_graph(
                chosen_type, rowsize=self.doc_figsize[0], colsize=self.doc_figsize[1]
            )
            State(self.state_prefix.rstrip("_")).set("current_graph", fig)
            question = "Analyze the velocity-time graph shown to the left. What is the direction and state of motion?"
            answers = [direction, motion_state]

        else:
            raise ValueError(f"Unsupported problem_type: {problem_type}")

        return {"question": question,
                    "answers": answers,
                    "units": units,
                    "graph": fig,
                    "graph_type": chosen_type,
                    "diagram_data": fig,
                    "button_options": options,
                    "side_by_side": True,
                    "graph_doc_width": self.doc_graph_width}


    def unique_graph_problems_for_doc(
        self,
        problem_type: str,
        difficulty: str = "Medium",
        *,
        graph_doc_width: Optional[float] = None,
        figsize: Optional[Tuple[float, float]] = None,
        suppress_question_text: bool = True,
    ) -> list[dict[str, Any]]:
        """Return one problem per graph type for DOCX export while keeping UI untouched."""
        original_width = self.doc_graph_width
        original_figsize = self.doc_figsize

        try:
            if graph_doc_width is not None:
                self.doc_graph_width = graph_doc_width
            if figsize is not None:
                self.doc_figsize = figsize

            problems: list[dict[str, Any]] = []
            types = self.graph_types.copy()
            random.shuffle(types)
            for graph_type in types:
                payload = self.choose_problem_dict(problem_type, difficulty, graph_type=graph_type)
                if suppress_question_text:
                    payload["suppress_question_text"] = True
                payload.setdefault("graph_doc_width", self.doc_graph_width)
                problems.append(payload)
            return problems
        finally:
            self.doc_graph_width = original_width
            self.doc_figsize = original_figsize

    def stored_metadata(self) -> dict[str, dict]:
        """Return metadata mapping for this generator."""
        return {
            "Position-Time Graph": {
            "honors": r"\text{Direction and motion from position-time graphs}",
            "conceptual": r"""
            \text{Positive slope: moving in positive direction} \\
            \text{Negative slope: moving in negative direction} \\
            \text{Straight line: constant velocity} \\
            \text{Curved (increasing): speeding up} \\
            \text{Curved (decreasing): slowing down}
            """
        },
        "Velocity-Time Graph": {
            "honors": r"\text{Direction and motion from velocity-time graphs}",
            "conceptual": r"""
            \text{Above x-axis: moving in positive direction} \\
            \text{Below x-axis: moving in negative direction} \\
            \text{Horizontal line: constant velocity} \\
            \text{Sloped line (increasing): speeding up} \\
            \text{Sloped line (decreasing): slowing down}
            """
        },
    }




