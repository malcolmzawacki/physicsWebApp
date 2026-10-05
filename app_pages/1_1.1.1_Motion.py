import matplotlib.pyplot as plt
import streamlit as st

from utils.layouts import render_diagram_match_layout
from utils.generators.kinematics.motion_graph_matching_generator import (
    generate_motion_graph_match_payload,
)
from utils.ui import interface

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")


def constant_motion():
    # Lazy import - only load when this section is accessed
    from utils.generators.kinematics.const_motion_generator import ConstantMotionGenerator

    from utils.worksheet_ui import worksheet_shortcut
    worksheet_shortcut("Constant Motion")

    generator = ConstantMotionGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy", "Medium", "Hard"]
    title = "Constant Motion"
    prefix = "const_motion_"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(setup_workspace=True)


def accelerated_motion():
    # Lazy import - only load when this section is accessed
    from utils.generators.kinematics.linear_motion_generator import LinearMotionGenerator
    from utils.worksheet_ui import worksheet_shortcut

    worksheet_shortcut("Accelerated Motion")

    generator = LinearMotionGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy", "Medium", "Hard"]
    title = "Accelerated Motion"
    prefix = "accelerated_motion"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(setup_workspace=True)


def motion_graph_types():
    from utils.worksheet_ui import worksheet_shortcut
    worksheet_shortcut("Types of Motion Graphs")
    # Lazy import - only load when this section is accessed
    from utils.generators.kinematics.motion_graph_generator import MotionGraphGenerator

    difficulties = ["Easy", "Medium", "Hard"]
    generator = MotionGraphGenerator()
    metadata = generator.stored_metadata()
    prefix = "motion_graph"
    title = "Analyzing Motion Graphs"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(side_by_side=True, equations=False, expanded=True)


def motion_graph_matching():
    from utils.worksheet_ui import worksheet_shortcut
    worksheet_shortcut("Matching Motion Graphs")
    def controls(state):
        return {
            "primary_order": st.radio(
                "Select primary graph type:",
                ["Position-Time First", "Velocity-Time First"],
                horizontal=True,
                key=state.key("primary_select"),
            )
        }

    render_diagram_match_layout(
        title="Matching Motion Graphs",
        prefix="motion_graph_matching",
        payload_factory=lambda control_state: generate_motion_graph_match_payload(
            control_state.get("primary_order", "Position-Time First")
        ),
        controls=controls,
        generate_label="Generate New Matching Set",
    )


def projectiles():
    from utils.worksheet_ui import worksheet_shortcut
    worksheet_shortcut("Projectiles")
    # Lazy import - only load when this section is accessed
    from utils.generators.kinematics.projectile_generator import ProjectileGenerator

    generator = ProjectileGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy", "Medium", "Hard"]
    title = "Projectiles"
    prefix = "projectiles"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()
