from __future__ import annotations

import pandas as pd
import streamlit as st
from typing import Dict, Optional

from utils.ui_state import State
from utils.progress_ids import custom_progress_id, migrate_custom_progress, progress_label


def _ensure_selection_state_length(state: State, units: list[str]) -> None:
    """Ensure selection state always matches the current number of answer parts."""
    current = state.get("user_answers_selected")
    target_len = len(units)
    if not isinstance(current, list) or len(current) != target_len:
        state.set("user_answers_selected", [None] * target_len)


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
    performance = migrate_custom_progress(performance)
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
                "Problem Type": progress_label(problem_type),
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


def init_performance(problem_types: list[str], difficulties: list[str]) -> Dict[str, Dict[str, Dict[str, int]]]:
    """Create a fresh performance tracking dict structure.

    Returns: { problem_type: { difficulty: { 'attempts': int, 'correct': int } } }
    """
    perf: Dict[str, Dict[str, Dict[str, int]]] = {}
    for p in problem_types:
        p = custom_progress_id(p)
        perf[p] = {}
        for d in difficulties:
            perf[p][d] = {"attempts": 0, "correct": 0}
    return perf


def record_performance(perf: Dict[str, Dict[str, Dict[str, int]]], problem_type: str, difficulty: str, is_correct: bool) -> Dict[str, Dict[str, Dict[str, int]]]:
    """Update an existing performance dict for a submission.

    Mutates the provided dict and returns it for convenience.
    """
    migrate_custom_progress(perf)
    problem_type = custom_progress_id(problem_type)
    if problem_type not in perf:
        perf[problem_type] = {}
    if difficulty not in perf[problem_type]:
        perf[problem_type][difficulty] = {"attempts": 0, "correct": 0}
    perf[problem_type][difficulty]["attempts"] += 1
    if is_correct:
        perf[problem_type][difficulty]["correct"] += 1
    return perf


def equation_controls(generator, problem_type, state, checkbox_key, fallback_dict=None, expanded=True):
    """Keep the equation expander and its detail switch together on one row."""
    from utils import layout_config
    equation_col, toggle_col = st.columns(
        [layout_config.EQUATION_EXPANDER_WIDTH, layout_config.EQUATION_TOGGLE_WIDTH],
        gap=layout_config.CONTROL_GAP, vertical_alignment="top")
    # Evaluate the switch first so this rerun renders the requested equation set.
    with toggle_col:
        level = st.checkbox("More Equations", value=state.get("level", False), key=checkbox_key)
    state.set("level", level)
    with equation_col:
        show_equations_expander(generator, problem_type, level, fallback_dict, expanded)


def show_equations_expander(
    generator: object,
    problem_type: str,
    level: bool,
    fallback_dict: Optional[dict] = None,
    expanded: bool = True,
) -> None:
    """Render the equations expander using generator metadata with optional fallback.

    - generator: expects optional get_problem_metadata(problem_type) -> dict
    - level: False = honors_equation, True = conceptual_equation
    - fallback_dict: optional { problem_type: { 'honors': str, 'conceptual': str } }
    """
    candidates = []
    if hasattr(generator, "get_problem_metadata"):
        candidates.append(generator.get_problem_metadata(problem_type))
    if fallback_dict is not None:
        candidates.append(fallback_dict.get(problem_type, {}))
    name = "conceptual" if level else "honors"
    for metadata in candidates:
        equation = metadata.get(name + "_equation") or metadata.get(name)
        if isinstance(equation, (list, tuple)):
            equation = r"\begin{gathered}" + r" \\ ".join(equation) + r"\end{gathered}"
        if equation:
            with st.expander("equation(s)", expanded=expanded):
                st.latex(equation)
            break


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
    state = State(prefix)
    _ensure_selection_state_length(state, units)

    for i, unit in enumerate(units):
        st.write(f"**{unit}:**")
        options = answer_options.get(i, [])
        if not options:
            value = st.text_input(f"Enter {unit}:", key=f"{prefix}_text_input_{i}_{question_id}")
            selections = state.get("user_answers_selected")
            selections[i] = value if value.strip() else None
            state.set("user_answers_selected", selections)
            continue

        cols = st.columns(len(options))
        for j, (col, option) in enumerate(zip(cols, options)):
            with col:
                user_answers = state.get("user_answers_selected")
                is_selected = user_answers[i] == option
                button_type = "primary" if is_selected else "secondary"
                if st.button(option, key=f"{prefix}_option_{i}_{j}_{question_id}", type=button_type, use_container_width=True):
                    user_answers[i] = option
                    state.set("user_answers_selected", user_answers)
                    st.rerun()


def render_dropdown_options(prefix: str, units: list[str], answer_options: Dict[int, list[str]], question_id: int) -> None:
    """Render dropdowns in columns and store selections in session state."""
    state = State(prefix)
    _ensure_selection_state_length(state, units)
    cols = st.columns(len(units)) if units else []

    for i, unit in enumerate(units):
        with cols[i]:
            options = answer_options.get(i, [])
            if not options:
                value = st.text_input(f"{unit}", key=f"{prefix}_dropdown_fallback_{i}_{question_id}")
                selections = state.get("user_answers_selected")
                selections[i] = value if value.strip() else None
                state.set("user_answers_selected", selections)
                continue

            key = f"{prefix}_dropdown_{i}_{question_id}"
            current = state.get("user_answers_selected")[i]
            if current not in options:
                current = None
            selected = st.selectbox(
                unit,
                options=["Select..."] + options,
                index=0 if current is None else options.index(current) + 1,
                key=key,
            )

            user_answers = state.get("user_answers_selected")
            user_answers[i] = None if selected == "Select..." else selected
            state.set("user_answers_selected", user_answers)


def render_hints(hints: list[str]) -> None:
    if hints:
        with st.expander("Hints"):
            for i, hint in enumerate(hints, 1):
                st.write(f"{i}. {hint}")
