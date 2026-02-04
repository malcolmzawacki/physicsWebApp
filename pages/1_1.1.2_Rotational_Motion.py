import streamlit as st

from tools.loading import lazy_tabs
from utils.ui import interface


def rotational_kinematics():
    from utils.generators.rotational_motion_generator import RotationalMotionGenerator
    title = "Rotational Kinematics"
    prefix = "rotational_kinematics"
    difficulties = ["Easy", "Medium", "Hard"]
    generator = RotationalMotionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def main():
    tab_specs = [
        ("Rotational Kinematics", rotational_kinematics),
    ]

    lazy_tabs(tab_specs, state_key="rotational_motion_tabs", auto_load_first=True)


if __name__ == "__main__":
    main()
