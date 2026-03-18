import streamlit as st

from utils.ui_state import State
from app_pages.static_electricity.friction_common import render_reference_series, render_symbol_legend


def charging_by_friction_page() -> None:
    state = State("static_electricity")
    state.ensure("mode", "Explorer")

    st.write(
        "Use the triboelectric reference to predict how materials charge when rubbed together. "
        "This first version includes the shared reference display and a material sandbox."
    )

    mode = st.radio(
        "Mode",
        options=("Explorer", "Comparison Practice", "Ranking Logic Puzzle"),
        horizontal=True,
        key=state.key("mode_select"),
    )
    state.set("mode", mode)

    if mode == "Ranking Logic Puzzle":
        from app_pages.static_electricity.friction_puzzle import render as render_puzzle

        render_puzzle()
        return

    content_col, guide_col = st.columns((3, 2), gap="large")
    with guide_col:
        render_reference_series()
        render_symbol_legend()

    with content_col:
        if mode == "Explorer":
            from app_pages.static_electricity.friction_explorer import render as render_explorer

            render_explorer()
        else:
            from app_pages.static_electricity.friction_comparison import render as render_comparison

            render_comparison()
