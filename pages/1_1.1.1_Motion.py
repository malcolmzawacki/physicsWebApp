import streamlit as st
import matplotlib.pyplot as plt

# Use a dark background for matplotlib so it fits a "dark mode" style
plt.style.use("dark_background")

from utils.ui import interface
from utils.layouts import render_diagram_match_layout
from utils.generators.motion_graph_matching_generator import generate_motion_graph_match_payload
from tools.loading import lazy_tabs

def linear_fns():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.linear_motion_generator import LinearMotionGenerator
    generator = LinearMotionGenerator()
    metadata = generator.stored_metadata()


    difficulties = ["Easy","Medium","Hard"]

    title = "Accelerated Motion"
    prefix = "accelerated_motion"

    ui = interface(prefix,title,
                    generator,metadata,difficulties)
    ui.unified_smart_layout()


def projectile_fns():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.projectile_generator import ProjectileGenerator

    generator = ProjectileGenerator()
    metadata = generator.stored_metadata()
    
    difficulties = ["Easy","Medium","Hard"]

    title = "Projectiles"
    prefix = "projectiles"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def position_and_velocity_graph_analysis():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.motion_graph_generator import MotionGraphGenerator

    difficulties = ["Easy", "Medium", "Hard"]
    generator = MotionGraphGenerator()
    metadata = generator.stored_metadata()
    prefix = "motion_graph"
    title = "Analyzing Motion Graphs"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(side_by_side=True, equations=False, expanded=True)


def PvT_and_VvT_graph_matching():
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


def constant_motion():
    # Lazy import - only load when this tab is actually accessed
    from utils.generators.const_motion_generator import ConstantMotionGenerator

    generator = ConstantMotionGenerator()
    metadata = generator.stored_metadata()
    difficulties = ["Easy","Medium","Hard"]
    title = "Constant Motion"
    prefix = "const_motion_"
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

    
def main():
    tab_specs = [
        ("Constant Motion", constant_motion),
        ("Accelerated Motion", linear_fns),
        ("Types of Motion Graphs", position_and_velocity_graph_analysis),
        ("Matching Motion Graphs", PvT_and_VvT_graph_matching),
        ("Projectiles", projectile_fns),
    ]

    lazy_tabs(tab_specs, state_key="motion_tabs", auto_load_first=True)

if __name__ == "__main__":
    main()

