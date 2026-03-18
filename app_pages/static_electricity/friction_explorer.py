from __future__ import annotations

import streamlit as st

from utils.ui_state import State
from utils.generators.static_electricity import (
    TRIBOELECTRIC_MODEL_NOTES,
    get_material,
    get_triboelectric_materials,
)
from app_pages.static_electricity.friction_common import render_outcome_card


def render() -> None:
    state = State("friction_explorer")
    materials = get_triboelectric_materials()
    labels = {material.key: material.label for material in materials}
    keys = [material.key for material in materials]

    state.ensure("left_material", "glass")
    state.ensure("right_material", "teflon")

    st.subheader("Explorer")
    st.write("Choose two materials and inspect the predicted charging outcome after rubbing them together.")

    left_col, right_col = st.columns(2)
    with left_col:
        left_key = st.selectbox(
            "Material 1",
            options=keys,
            format_func=lambda key: labels[key],
            index=keys.index(state.get("left_material", "glass")),
            key=state.key("left_select"),
        )
    with right_col:
        right_key = st.selectbox(
            "Material 2",
            options=keys,
            format_func=lambda key: labels[key],
            index=keys.index(state.get("right_material", "teflon")),
            key=state.key("right_select"),
        )

    state.set("left_material", left_key)
    state.set("right_material", right_key)

    render_outcome_card(left_key, right_key)

    with st.expander("Why this model works for the page", expanded=False):
        st.write(TRIBOELECTRIC_MODEL_NOTES["scope"])
        st.write(TRIBOELECTRIC_MODEL_NOTES["tie_behavior"])

    with st.expander("Material notes", expanded=False):
        first = get_material(left_key)
        second = get_material(right_key)
        st.markdown(f"**{first.label}:** {first.description}")
        st.markdown(f"**{second.label}:** {second.description}")
