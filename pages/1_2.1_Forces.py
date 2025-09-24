import streamlit as st

from tools.loading import lazy_tabs
from utils.ui import interface
from utils.generators.force_generator import ForceGenerator


def newtons_2nd():
    title = "Newton's Second Law"
    prefix = "newtons_2nd"
    difficulties = ["Easy","Medium","Hard"]
    generator = ForceGenerator()
    metadata = generator.stored_metadata()
    ui = interface(prefix, title, generator, metadata, difficulties)
    ui.unified_smart_layout()


def _under_construction_tab():
    st.write("Currently Under Construction")


def main():
    tab_specs = [
        ("Newton's Second Law", newtons_2nd),
        ("TBD", _under_construction_tab),
    ]

    lazy_tabs(tab_specs, state_key="forces_tabs", auto_load_first=True)


if __name__ == "__main__":
    main()
