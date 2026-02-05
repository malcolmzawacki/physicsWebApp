import streamlit as st

from tools.loading import lazy_tabs
from utils.ui import interface


def momentum():
    from utils.generators.momentum_generators.momentum import MomentumGenerator
    title = "Momentum"
    prefix = "momentum"
    difficulties = ["Easy"]
    generator = MomentumGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()    

def impulse():
    from utils.generators.momentum_generators.impulse_generator import ImpulseGenerator
    title = "Impulse"
    prefix = "impulse"
    difficulties = ["Easy","Medium","Hard"]
    generator = ImpulseGenerator()
    metadata = generator.stored_metadata()
    if isinstance(metadata, dict):
        metadata = {k: v for k, v in metadata.items() if k == "Change in Momentum"}
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(diagram_title="Diagram", expanded=True)

def matching_impulses():
    from utils.generators.momentum_generators.impulse_generator import ImpulseGenerator
    title = "Matching Impulses"
    prefix = "impulse_mc"
    difficulties = ["Easy","Medium","Hard"]
    generator = ImpulseGenerator()
    metadata = generator.stored_metadata()
    if isinstance(metadata, dict):
        metadata = {k: v for k, v in metadata.items() if k == "Change in Momentum (Multiple Choice)"}
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout(diagram_title="Diagram", expanded=True)


def collisions():
    from utils.generators.momentum_generators.collision_generator import CollisionGenerator
    title = "Collisions"
    prefix = "collisions"
    difficulties = ["Easy"]
    generator = CollisionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def main():
    tab_specs = [
        ("Momentum", momentum),
        ("Matching Impulses", matching_impulses),\
        ("Impulse", impulse),
        ("Collisions", collisions),
    ]

    lazy_tabs(tab_specs, state_key="momentum_tabs", auto_load_first=True)


if __name__ == "__main__":
    main()
