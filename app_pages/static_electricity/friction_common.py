from __future__ import annotations

import streamlit as st

from utils.generators.static_electricity import (
    TRIBOELECTRIC_MODEL_NOTES,
    compare_materials,
    describe_charge_outcome,
    get_material,
    get_reference_series,
)


def render_symbol_legend() -> None:
    st.caption("Legend: `+` = becomes positive, `-` = becomes negative, `e-` = electron flow")


def format_rank_gap(first_key: str, second_key: str) -> str:
    first = get_material(first_key)
    second = get_material(second_key)
    gap = abs(first.rank - second.rank)
    if gap == 0:
        return "same position"
    if gap == 1:
        return "adjacent positions"
    return f"{gap} positions apart"


def render_reference_series(material_keys: tuple[str, ...] | None = None) -> None:
    series = get_reference_series(material_keys)
    st.markdown("#### Classroom Triboelectric Reference")
    st.caption(TRIBOELECTRIC_MODEL_NOTES["rule"])
    st.caption("Top of the list tends to lose electrons. Bottom of the list tends to gain electrons.")

    if not series:
        return

    st.markdown("`+` More likely to become positive")
    for material in series:
        st.markdown(f"`{material.rank + 1:>2}`  {material.label}")
    st.markdown("`-` More likely to become negative")


def render_charge_flow_strip(first_key: str, second_key: str) -> None:
    first = get_material(first_key)
    second = get_material(second_key)
    comparison = compare_materials(first_key, second_key)

    if comparison == 0:
        st.caption(f"`{first.label}`  |  no clear net transfer  |  `{second.label}`")
        return

    positive = first if comparison > 0 else second
    negative = second if comparison > 0 else first
    st.markdown(f"`+ {positive.label}`  `e- ->`  `- {negative.label}`")


def render_outcome_card(first_key: str, second_key: str) -> None:
    first = get_material(first_key)
    second = get_material(second_key)
    outcome_text = describe_charge_outcome(first_key, second_key)
    comparison = compare_materials(first_key, second_key)

    st.markdown("#### Predicted Outcome")
    render_charge_flow_strip(first_key, second_key)
    st.info(outcome_text["summary"])
    st.write(outcome_text["electron_flow"])

    if comparison == 0:
        st.caption("These are the same material in the simplified model, so no reliable net charging is predicted.")
        return

    stronger = first.label if comparison > 0 else second.label
    weaker = second.label if comparison > 0 else first.label
    st.caption(
        f"{stronger} is higher on the reference list than {weaker}, so it is modeled as losing electrons. "
        f"The two materials are {format_rank_gap(first_key, second_key)}."
    )
