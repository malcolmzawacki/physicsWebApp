import streamlit as st

from tools.loading import lazy_tabs
from utils.ui import interface





def newtons_2nd():
    from utils.generators.force_generator import ForceGenerator
    title = "Newton's Second Law"
    prefix = "newtons_2nd"
    difficulties = ["Easy","Medium","Hard"]
    generator = ForceGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def tension():
    from utils.generators.forces.tension_generator import TensionGenerator
    title = "Tension Problems"
    prefix = "tension"
    difficulties = ["Easy","Medium","Hard"]
    generator = TensionGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

def atwood():
    from utils.generators.forces.atwood_generator import AtwoodGenerator
    title = "Atwood Machines"
    prefix = "atwood"
    difficulties = ["Medium"]
    generator = AtwoodGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def inclines():
    from utils.generators.forces.incline_generator import InclineGenerator
    title = "Inclined Planes"
    prefix = "incline"
    difficulties = ["Medium"]
    generator = InclineGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

def center_of_mass():
    from utils.generators.forces.center_of_mass_generator import CenterOfMassGenerator
    title = "Center of Mass"
    prefix = "com"
    difficulties = ["Easy", "Medium", "Hard"]
    generator = CenterOfMassGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()

def _under_construction_tab():
    st.write("Currently Under Construction")


def main():
    tab_specs = [
        ("Newton's Second Law", newtons_2nd),
        ("Center of Mass", center_of_mass),
        ("Tension", tension),
        ("Atwood Machines", atwood),
        ("Inclined Planes", inclines),
   
    ]

    lazy_tabs(tab_specs, state_key="forces_tabs", auto_load_first=True)


if __name__ == "__main__":
    main()
