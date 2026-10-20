from __future__ import annotations

from utils.activity_flow import next_question_countdown
from utils.session_progress import record_answer, format_answers
from utils.circuit_workspace import render_circuit_workspace
from utils.word_lists import random_correct_message, random_error_message

from utils.grading import parse_number, answer_matches, CIRCUIT_POLICY

import streamlit as st

from utils.ui_components import (
    build_performance_table,
    init_performance,
    performance_expander,
    record_performance,
    equation_controls,
    render_calculation_feedback,
)
from utils.ui_state import State
from utils.layout_config import question_columns
from utils.generators.current_electricity import (
    SERIES_PARALLEL_EQUATION_METADATA,
    SERIES_PARALLEL_PROBLEM_TYPES,
    build_series_parallel_case,
    format_answer_value,
)

AUTO_ADVANCE_DELAY_SECONDS = 5

DIFFICULTIES: tuple[str, ...] = ("Easy", "Medium", "Hard")


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

    st.image(svg_bytes.decode("utf-8"), width="stretch")


def _render_diagram_panel(case: dict) -> None:
    st.markdown("#### Circuit Diagram")
    _render_schematic(case)


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

    st.caption("Series and Parallel Circuits · Combine circuit relationships to find equivalent resistance, "
               "circuit current, or component voltage. For focused relationship practice, choose Circuit Fundamentals.")
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
    diagram_col, content_col = st.columns((1, 1), gap="large")
    with diagram_col:
        _render_diagram_panel(case)

    with content_col:
        st.subheader(case["problem_type"])
        st.write(case["prompt"])
        render_circuit_workspace(state, case)

        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        st.caption("Score: 0/0" if attempts == 0 else f"Score: {correct}/{attempts}")

        with diagram_col, st.form(state.key(f"answer_form_{question_number}"), clear_on_submit=False):
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
                record_answer("Series and Parallel Circuits", {"Question": case["prompt"], "Givens": dict(case["givens"])},
                              format_answers([user_value], [case["unit"]]),
                              format_answers([case["answer"]], [case["unit"]]),
                              is_correct, difficulty=difficulty, explanation=case["explanation"])
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
                        "message": random_correct_message() if is_correct else random_error_message(),
                        "expected_answer": format_answer_value(case["answer"]),
                    },
                )
                st.rerun()

        if state.get("submitted") and result:
            render_calculation_feedback(case["explanation"], result["expected_answer"],
                                        case["unit"], is_correct=result["is_correct"],
                                        message=result.get("message"))
            if result["is_correct"]:
                def advance() -> None:
                    _reset_question(state, problem_type, difficulty)
                    st.rerun()

                next_question_countdown(state, question_number, advance, seconds=AUTO_ADVANCE_DELAY_SECONDS)

    new_col, performance_col = st.columns((1.4, 4), vertical_alignment="center")
    with new_col:
        st.button("New Question (Circuit)", key=state.key(f"new_circuit_{question_number}"),
                  on_click=_reset_question, args=(state, problem_type, difficulty),
                  use_container_width=True)
    with performance_col:
        _render_performance(state)
