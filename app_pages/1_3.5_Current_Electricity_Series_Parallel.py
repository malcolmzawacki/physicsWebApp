from __future__ import annotations

from utils.grading import parse_number, answer_matches, CIRCUIT_POLICY
from utils.activity_flow import next_question_countdown

import streamlit as st

from utils.ui_components import (
    build_performance_table,
    init_performance,
    performance_expander,
    record_performance,
    equation_controls,
)
from utils.ui_state import State
from utils.layout_config import question_columns
from utils.generators.current_electricity import (
    SERIES_PARALLEL_EQUATION_METADATA,
    SERIES_PARALLEL_PROBLEM_TYPES,
    build_series_parallel_case,
    format_answer_value,
)

AUTO_ADVANCE_DELAY_SECONDS = 2
DIFFICULTIES: tuple[str, ...] = ("Easy", "Medium", "Hard")


def _render_givens(case: dict) -> None:
    st.markdown("#### Givens")
    for label, value in case["givens"]:
        st.markdown(f"- **{label}:** `{value}`")


def _render_fallback_text(case: dict) -> None:
    st.code(
        "\n".join(
            [
                f"Type: {case['diagram']['kind']}",
                f"Source: {case['diagram']['source_label']}",
                *[f"Element: {label}" for label in case["diagram"]["resistor_labels"]],
            ]
        )
    )


from utils.circuit_diagrams import draw_series as _render_series_schematic, draw_parallel as _render_parallel_schematic


def _render_schematic(case: dict) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import schemdraw
        import schemdraw.elements as elm
    except ImportError:
        st.warning("`schemdraw` is not installed yet. Install the updated requirements to see the schematic diagrams.")
        _render_fallback_text(case)
        return

    diagram = case["diagram"]
    try:
        with schemdraw.Drawing(show=False, color="black", bgcolor="white") as drawing:
            if hasattr(elm, "STYLE_IEEE") and hasattr(elm, "style"):
                elm.style(elm.STYLE_IEEE)
            if diagram["kind"] == "parallel":
                _render_parallel_schematic(drawing, elm, diagram)
            else:
                _render_series_schematic(drawing, elm, diagram)
            drawing.draw(show=False)
            svg_bytes = drawing.get_imagedata("svg")
    except Exception as exc:
        st.warning(f"Schematic rendering fell back to text: {exc}")
        _render_fallback_text(case)
        return

    st.markdown(svg_bytes.decode("utf-8"), unsafe_allow_html=True)


def _render_diagram_panel(case: dict) -> None:
    st.markdown("#### Circuit Diagram")
    _render_schematic(case)
    _render_givens(case)


def _reset_question(state: State, problem_type: str, difficulty: str) -> None:
    state.set("case", build_series_parallel_case(problem_type, difficulty))
    state.inc("question_number")
    state.set("submitted", False)
    state.set("last_result", None)


def _render_performance(state: State) -> None:
    df = build_performance_table(state.get("performance"), list(DIFFICULTIES))
    performance_expander(df)


def _answer_is_correct(user_value: float, answer: float) -> bool:
    return answer_matches(user_value, answer, CIRCUIT_POLICY)


def current_electricity_series_parallel_page() -> None:
    state = State("current_electricity_series_parallel")
    state.ensure("problem_type", SERIES_PARALLEL_PROBLEM_TYPES[0])
    state.ensure("difficulty", "Easy")
    state.ensure("level", False)
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(list(SERIES_PARALLEL_PROBLEM_TYPES), list(DIFFICULTIES)),
    )

    top_col1, top_col2, top_col3 = question_columns()
    with top_col1:
        problem_type = st.selectbox(
            "Problem Type",
            options=SERIES_PARALLEL_PROBLEM_TYPES,
            index=SERIES_PARALLEL_PROBLEM_TYPES.index(state.get("problem_type", SERIES_PARALLEL_PROBLEM_TYPES[0])),
            key=state.key("problem_type_select"),
        )
    with top_col2:
        difficulty = st.selectbox(
            "Difficulty",
            options=DIFFICULTIES,
            index=DIFFICULTIES.index(state.get("difficulty", "Easy")),
            key=state.key("difficulty_select"),
        )

    previous_type = state.get("problem_type")
    previous_difficulty = state.get("difficulty")
    state.set("problem_type", problem_type)
    state.set("difficulty", difficulty)

    if not state.has("case"):
        _reset_question(state, problem_type, difficulty)
        st.rerun()
    elif previous_type != problem_type or previous_difficulty != difficulty:
        _reset_question(state, problem_type, difficulty)
        st.rerun()

    case = state.get("case")
    question_number = state.get("question_number", 0)
    result = state.get("last_result")

    equation_controls(object(), case["problem_type"], state,
                      state.key("equation_level"), SERIES_PARALLEL_EQUATION_METADATA)
    diagram_col, content_col = st.columns((2, 3), gap="large")
    with diagram_col:
        _render_diagram_panel(case)

    with content_col:
        st.subheader(case["problem_type"])
        st.caption(f"Difficulty: {difficulty}")
        st.write(case["prompt"])

        score_col, action_col, spacer_col = st.columns((2, 1.2, 4.0))
        with score_col:
            attempts = state.get("attempt_count", 0)
            correct = state.get("correct_count", 0)
            st.caption("Score: 0/0" if attempts == 0 else f"Score: {correct}/{attempts}")
        with action_col:
            if st.button("New Circuit", key=state.key("new_circuit"), type="secondary", use_container_width=True):
                _reset_question(state, problem_type, difficulty)
                st.rerun()

        with st.form(state.key(f"answer_form_{question_number}"), clear_on_submit=False):
            answer_text = st.text_input(
                f"{case['answer_label']} ({case['unit']})",
                key=state.key(f"answer_{question_number}"),
            )
            check_clicked = st.form_submit_button("Check Answer", type="primary", use_container_width=True,
                disabled=state.get("submitted"))

        if check_clicked and not state.get("submitted"):
            try:
                user_value = parse_number(answer_text)
            except ValueError:
                st.error("Enter a finite numeric value before checking the answer.")
            else:
                is_correct = _answer_is_correct(user_value, case["answer"])
                state.inc("attempt_count")
                if is_correct:
                    state.inc("correct_count")
                updated = record_performance(
                    state.get("performance"),
                    problem_type,
                    difficulty,
                    is_correct,
                )
                state.set("performance", updated)
                state.set("submitted", True)
                state.set(
                    "last_result",
                    {
                        "is_correct": is_correct,
                        "expected_answer": format_answer_value(case["answer"]),
                    },
                )
                st.rerun()

        if state.get("submitted") and result:
            if result["is_correct"]:
                st.success("Correct.")
            else:
                st.error("Not quite.")
            st.info(case["explanation"])
            st.caption(f"Expected answer: {result['expected_answer']} {case['unit']}")
            if result["is_correct"]:
                def advance():
                    _reset_question(state, problem_type, difficulty)
                    st.rerun()
                next_question_countdown(state, question_number, advance, AUTO_ADVANCE_DELAY_SECONDS)

    _render_performance(state)
