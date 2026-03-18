from __future__ import annotations

import random
import time

import streamlit as st

from utils.ui_components import build_performance_table, init_performance, performance_expander, record_performance
from utils.ui_state import State
from utils.generators.static_electricity import compare_materials, describe_charge_outcome, get_material, get_triboelectric_materials
from app_pages.static_electricity.friction_common import format_rank_gap, render_charge_flow_strip


def _build_comparison_case() -> dict[str, str]:
    materials = get_triboelectric_materials()
    first, second = random.sample(materials, 2)
    return {"left_key": first.key, "right_key": second.key}


def _comparison_difficulty(first_key: str, second_key: str) -> str:
    gap = abs(get_material(first_key).rank - get_material(second_key).rank)
    if gap >= 6:
        return "Easy"
    if gap >= 3:
        return "Medium"
    return "Hard"


def _comparison_answer_options(left_key: str, right_key: str) -> tuple[str, ...]:
    left = get_material(left_key)
    right = get_material(right_key)
    return (left.label, right.label, "Neither / no reliable net charge difference")


def _reset_comparison_question(state: State) -> None:
    state.set("case", _build_comparison_case())
    state.set("submitted", False)
    state.set("last_result", None)


def render() -> None:
    state = State("friction_compare")
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure_lazy("case", _build_comparison_case)
    state.ensure_lazy("performance", lambda: init_performance(["Comparison Practice"], ["Easy", "Medium", "Hard"]))
    state.ensure("submitted", False)
    state.ensure("last_result", None)

    case = state.get("case")
    left_key = case["left_key"]
    right_key = case["right_key"]
    left = get_material(left_key)
    right = get_material(right_key)
    difficulty = _comparison_difficulty(left_key, right_key)
    outcome = describe_charge_outcome(left_key, right_key)
    answer_options = _comparison_answer_options(left_key, right_key)

    st.subheader("Comparison Practice")
    st.write("Use the reference series to decide which material becomes positive and which becomes negative after rubbing.")
    st.caption(f"Difficulty: {difficulty}")
    st.markdown(
        f"When **{left.label}** is rubbed with **{right.label}**, which material becomes positive and which becomes negative?"
    )
    render_charge_flow_strip(left_key, right_key)

    positive_choice = st.radio("Becomes positive", options=answer_options, key=state.key(f"positive_choice_{left_key}_{right_key}"))
    negative_choice = st.radio("Becomes negative", options=answer_options, key=state.key(f"negative_choice_{left_key}_{right_key}"))

    score_col, spacer_col, next_col = st.columns((2, 3, 1))
    with score_col:
        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        st.caption("Score: 0/0" if attempts == 0 else f"Score: {correct}/{attempts}")
    with next_col:
        if st.button("New Pair", key=state.key("new_pair"), type="secondary", use_container_width=True):
            _reset_comparison_question(state)
            st.rerun()

    if st.button("Check Answer", key=state.key("check_answer"), type="primary", use_container_width=True):
        expected_positive = get_material(left_key if compare_materials(left_key, right_key) > 0 else right_key).label
        expected_negative = get_material(right_key if compare_materials(left_key, right_key) > 0 else left_key).label
        if compare_materials(left_key, right_key) == 0:
            expected_positive = "Neither / no reliable net charge difference"
            expected_negative = "Neither / no reliable net charge difference"

        is_valid = positive_choice != negative_choice or positive_choice == "Neither / no reliable net charge difference"
        is_correct = is_valid and positive_choice == expected_positive and negative_choice == expected_negative

        state.inc("attempt_count")
        if is_correct:
            state.inc("correct_count")
        performance = state.get("performance")
        state.set("performance", record_performance(performance, "Comparison Practice", difficulty, is_correct))
        state.set("submitted", True)
        state.set(
            "last_result",
            {
                "is_correct": is_correct,
                "is_valid": is_valid,
                "expected_positive": expected_positive,
                "expected_negative": expected_negative,
            },
        )

    result = state.get("last_result")
    if state.get("submitted") and result:
        if not result["is_valid"]:
            st.warning("A material cannot be both positive and negative in the same rubbing interaction.")
        elif result["is_correct"]:
            st.success("Correct.")
        else:
            st.error("Not quite.")

        st.write(outcome["summary"])
        st.write(outcome["electron_flow"])
        st.caption(f"Correct response: positive = {result['expected_positive']}; negative = {result['expected_negative']}.")
        st.caption(f"The two materials are {format_rank_gap(left_key, right_key)} on the simplified triboelectric list.")
        if result["is_correct"]:
            st.caption("Loading the next comparison...")
            time.sleep(0.8)
            _reset_comparison_question(state)
            st.rerun()

    performance_expander(build_performance_table(state.get("performance"), ["Easy", "Medium", "Hard"]))
