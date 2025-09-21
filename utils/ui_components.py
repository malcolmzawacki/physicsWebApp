from __future__ import annotations

import pandas as pd
import streamlit as st
from typing import Dict


def render_header(title: str, stars: int | None = None) -> None:
    col1, col2 = st.columns([10, 4], vertical_alignment='top')
    with col1:
        st.title(title)
    with col2:
        if stars:
            st.title(f"⭐ x {stars}")
        else:
            st.write("")


def build_performance_table(performance: Dict[str, Dict[str, Dict[str, int]]], ordered_difficulties: list[str]) -> pd.DataFrame:
    rows = []
    for problem_type, difficulties in performance.items():
        for difficulty, stats in difficulties.items():
            attempts = stats.get('attempts', 0)
            correct = stats.get('correct', 0)
            if attempts > 0:
                percentage = f"{(correct / attempts * 100):.1f}%"
                display = f"{correct}/{attempts} ({percentage})"
            else:
                display = "0/0 (0.0%)"
            rows.append({
                "Problem Type": problem_type,
                "Difficulty": difficulty,
                "Performance": display
            })
    df = pd.DataFrame(rows)
    pivot_df = df.pivot(index="Problem Type", columns="Difficulty", values="Performance")
    for col in ordered_difficulties:
        if col not in pivot_df.columns:
            pivot_df[col] = "0/0 (0.0%)"
    pivot_df = pivot_df[ordered_difficulties]
    return pivot_df


def performance_expander(df: pd.DataFrame) -> None:
    with st.expander("Your Performance", expanded=False):
        st.dataframe(df)


def draw_answer_inputs(prefix: str, units: list[str], correct_answers: list, question_id: int) -> list[str]:
    """Render text inputs for each answer part and return raw user inputs as strings."""
    user_answers: list[str] = []
    num_inputs = len(correct_answers)

    if num_inputs > 1:
        cols = st.columns(num_inputs)
        for i, col in enumerate(cols):
            unit = units[i]
            with col:
                key = f"{prefix}_input_{i}_{question_id}"
                placeholder = "Enter a number..." if not isinstance(correct_answers[i], str) else "Type text..."
                label = f"{i+1}: {unit}"
                input_value = st.text_input(label, placeholder=placeholder, key=key)
                user_answers.append(input_value)
    else:
        unit = units[0]
        key = f"{prefix}_input_0_{question_id}"
        input_value = st.text_input(f"{unit}:", placeholder="Type a number ...", key=key)
        user_answers.append(input_value)

    return user_answers


def render_button_options(prefix: str, units: list[str], answer_options: Dict[int, list[str]], question_id: int) -> None:
    """Render multiple-choice buttons per answer index and store selection in session state."""
    if f"{prefix}_user_answers_selected" not in st.session_state:
        st.session_state[f"{prefix}_user_answers_selected"] = [None] * len(units)

    for i, unit in enumerate(units):
        st.write(f"**{unit}:**")
        options = answer_options.get(i, [])
        if not options:
            st.text_input(f"Enter {unit}:", key=f"{prefix}_text_input_{i}")
            continue

        cols = st.columns(len(options))
        for j, (col, option) in enumerate(zip(cols, options)):
            with col:
                is_selected = st.session_state[f"{prefix}_user_answers_selected"][i] == option
                button_type = "primary" if is_selected else "secondary"
                if st.button(option, key=f"{prefix}_option_{i}_{j}_{question_id}", type=button_type, use_container_width=True):
                    user_answers = st.session_state[f"{prefix}_user_answers_selected"]
                    user_answers[i] = option
                    st.session_state[f"{prefix}_user_answers_selected"] = user_answers
                    st.rerun()


def render_hints(hints: list[str]) -> None:
    if hints:
        with st.expander("Hints"):
            for i, hint in enumerate(hints, 1):
                st.write(f"{i}. {hint}")
