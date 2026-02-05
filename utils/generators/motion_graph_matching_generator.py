"""Payload generator for matching position-time and velocity-time graphs."""

from __future__ import annotations

import random

from utils.generators.motion_graph_generator import MotionGraphGenerator


def generate_motion_graph_match_payload(primary_order: str) -> dict:
    graph_types = [
        "linear_positive",
        "linear_negative",
        "accelerating_positive",
        "accelerating_negative",
        "decelerating_positive",
        "decelerating_negative",
    ]

    graph_type = random.choice(graph_types)
    generator = MotionGraphGenerator()

    if primary_order == "Position-Time First":
        primary_diagram, _, _ = generator.generate_position_time_graph(
            graph_type, rowsize=5, colsize=2
        )
        option_diagrams, correct_index = _build_option_diagrams(
            generator.generate_velocity_time_graph, graph_type, graph_types
        )
        prompt = "Match this Position-Time Graph to the correct Velocity-Time Graph:"
    else:
        primary_diagram, _, _ = generator.generate_velocity_time_graph(
            graph_type, rowsize=5, colsize=2
        )
        option_diagrams, correct_index = _build_option_diagrams(
            generator.generate_position_time_graph, graph_type, graph_types
        )
        prompt = "Match this Velocity-Time Graph to the correct Position-Time Graph:"

    return {
        "prompt": prompt,
        "primary_diagram": primary_diagram,
        "option_diagrams": option_diagrams,
        "correct_index": correct_index,
    }


def _build_option_diagrams(generator_fn, correct_type: str, graph_types: list[str]) -> tuple:
    wrong_answers = graph_types.copy()
    wrong_answers.remove(correct_type)
    wrong_1 = random.choice(wrong_answers)
    wrong_answers.remove(wrong_1)
    wrong_2 = random.choice(wrong_answers)
    choice_list = [correct_type, wrong_1, wrong_2]
    random.shuffle(choice_list)
    option_diagrams = [
        generator_fn(entry, rowsize=5, colsize=3)[0] for entry in choice_list
    ]
    return option_diagrams, choice_list.index(correct_type)
