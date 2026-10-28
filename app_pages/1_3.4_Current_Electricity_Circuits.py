from __future__ import annotations

from utils.activity_flow import next_question_countdown
from utils.session_progress import record_answer, format_answers
from utils.word_lists import random_correct_message, random_error_message

from utils.grading import parse_number, answer_matches, CIRCUIT_POLICY
from utils.solve_for import select_target, generate_selected, MIXED
from utils.solve_for_custom import OhmsLawTargets
from utils.problem_payload import payload_from_dict
from utils.setup_workspace import render_setup_workspace
from utils.circuit_workspace import render_circuit_workspace

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
    CIRCUIT_EQUATION_METADATA,
    PROBLEM_TYPES,
    build_circuit_case,
    format_answer_value,
)

AUTO_ADVANCE_DELAY_SECONDS = 5

DIFFICULTIES: tuple[str, ...] = ("Easy", "Medium", "Hard")


def _render_schematic(case: dict) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import schemdraw
        import schemdraw.elements as elm
    except ImportError:
        st.warning("`schemdraw` is not installed yet. Install the updated requirements to see the schematic diagrams.")
        st.code(
            "\n".join(
                [
                    f"Source: {case['diagram']['source_label']}",
                    *[f"Element: {label}" for label in case["diagram"]["resistor_labels"]],
                    f"Top wire: {case['diagram']['wire_label']}",
                ]
            )
        )
        return

    diagram = case["diagram"]
    try:
        with schemdraw.Drawing(show=False, color="black", bgcolor="white") as drawing:
            if hasattr(elm, "STYLE_IEEE") and hasattr(elm, "style"):
                elm.style(elm.STYLE_IEEE)
            from utils.circuit_diagrams import draw_series, draw_parallel
            draw = draw_parallel if diagram["kind"] == "parallel" else draw_series
            draw(drawing, elm, diagram)
            drawing.draw(show=False)
            svg_bytes = drawing.get_imagedata("svg")
    except Exception as exc:
        st.warning(f"Schematic rendering fell back to text: {exc}")
        st.code(
            "\n".join(
                [
                    f"Source: {case['diagram']['source_label']}",
                    *[f"Element: {label}" for label in case["diagram"]["resistor_labels"]],
                    f"Top wire: {case['diagram']['wire_label']}",
                ]
            )
        )
        return

    st.image(svg_bytes.decode("utf-8"), width="stretch")


def _render_diagram_panel(case: dict) -> None:
    st.markdown("#### Circuit Diagram")
    _render_schematic(case)


def _reset_question(state: State, problem_type: str, difficulty: str) -> None:
    payload = generate_selected(OhmsLawTargets(), problem_type, difficulty, state.get("solve_for", MIXED))
    state.set("case", payload["extras"]["case"])
    state.set("payload", payload_from_dict(payload))
    state.set("question_id", state.inc("question_number"))
    state.set("submitted", False)
    state.set("last_result", None)


def _render_performance(state: State) -> None:
    df = build_performance_table(state.get("performance"), list(DIFFICULTIES))
    performance_expander(df)


def _answer_is_correct(user_value: float, answer: float) -> bool:
    return answer_matches(user_value, answer, CIRCUIT_POLICY)


def current_electricity_circuits_page() -> None:
    state = State("current_electricity")
    state.ensure("problem_type", PROBLEM_TYPES[0])
    state.ensure("difficulty", "Easy")
    state.ensure("level", False)
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(list(PROBLEM_TYPES), list(DIFFICULTIES)),
    )


    # Retired task selections must not leave an old case under a new label.
    if state.get("problem_type") not in PROBLEM_TYPES:
        state.set("problem_type", PROBLEM_TYPES[0])
        state.pop("problem_type_select")
        state.pop("fundamentals_task_select")
        state.pop("fundamentals_practice_select")
        _reset_question(state, PROBLEM_TYPES[0], state.get("difficulty"))

    st.caption("Circuit Fundamentals · Apply current and voltage relationships to individual components. "
               "For equivalent resistance and calculations that combine several steps, choose Series and Parallel Circuits.")
    top_col1, top_col2, top_col3 = question_columns()
    with top_col1:
        problem_type = st.selectbox(
            "Problem Type",
            options=PROBLEM_TYPES,
            index=PROBLEM_TYPES.index(state.get("problem_type", PROBLEM_TYPES[0])),
            key=state.key("fundamentals_practice_select"),
        )
    with top_col2:
        difficulty = st.selectbox(
            "Difficulty",
            options=DIFFICULTIES,
            index=DIFFICULTIES.index(state.get("difficulty", "Easy")),
            key=state.key("difficulty_select"),
        )

    previous_type = state.get("problem_type")
    previous_target = state.get("solve_for", MIXED)
    with top_col3:
        target = select_target(OhmsLawTargets(), problem_type, difficulty, state)
    state.set("solve_for", target)
    previous_difficulty = state.get("difficulty")
    state.set("problem_type", problem_type)
    state.set("difficulty", difficulty)

    if not state.has("case") or not state.has("payload"):
        _reset_question(state, problem_type, difficulty)
        st.rerun()
    elif previous_type != problem_type or previous_difficulty != difficulty or previous_target != target:
        _reset_question(state, problem_type, difficulty)
        st.rerun()

    case = state.get("case")
    question_number = state.get("question_number", 0)
    result = state.get("last_result")

    equation_controls(object(), case["problem_type"], state,
                      state.key("equation_level"), CIRCUIT_EQUATION_METADATA)
    diagram_col, content_col = st.columns((1, 1), gap="large")
    with diagram_col:
        _render_diagram_panel(case)

    with content_col:
        st.subheader(case["problem_type"], help=case.get("relationship"))
        st.write(case["prompt"])

        render_setup_workspace(state)
        render_circuit_workspace(state, case)

        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        st.caption("Score: 0/0" if attempts == 0 else f"Score: {correct}/{attempts}")

        answers = case["answers"] if "answers" in case else [case["answer"]]
        labels = case["answer_labels"] if "answer_labels" in case else [case["answer_label"]]
        with diagram_col, st.form(state.key(f"answer_form_{question_number}"), clear_on_submit=False):
            answer_texts = []
            answer_columns = st.columns(len(labels))
            for index, (column, label) in enumerate(zip(answer_columns, labels)):
                # Keep the original single-resistor widget identity.
                key = f"answer_{question_number}" if len(answers) == 1 else f"answer_{question_number}_{index}"
                answer_texts.append(column.text_input(f"{label} ({case['unit']})", key=state.key(key), disabled=state.get("submitted")))
            check_clicked = st.form_submit_button("Check Answer", type="primary", width="stretch",
                disabled=state.get("submitted"))

        if check_clicked and not state.get("submitted"):
            try:
                user_values = [parse_number(text) for text in answer_texts]
            except ValueError:
                st.error("Enter a finite numeric value in every answer field before checking.")
            else:
                field_results = [_answer_is_correct(value, expected) for value, expected in zip(user_values, answers)]
                is_correct = all(field_results)
                record_answer("Circuit Fundamentals", {"Question": case["prompt"], "Givens": dict(case["givens"])},
                              format_answers(user_values, [case["unit"]] * len(answers)),
                              format_answers(answers, [case["unit"]] * len(answers)),
                              is_correct, difficulty=difficulty, problem_type=problem_type, explanation=case["explanation"])
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
                        "expected_answer": format_answer_value(answers[0]) if len(answers) == 1 else "; ".join(
                            f"{label}: {format_answer_value(answer)} {case['unit']}"
                            for label, answer in zip(labels, answers)),
                        "field_results": field_results,
                    },
                )
                st.rerun()

        if state.get("submitted") and result:
            render_calculation_feedback(case["explanation"], result["expected_answer"],
                                        case["unit"] if len(answers) == 1 else "", is_correct=result["is_correct"],
                                        message=result.get("message"))
            if len(answers) > 1:
                for label, correct in zip(labels, result["field_results"]):
                    st.caption(f"{'✓' if correct else '✗'} {label}: {'Correct' if correct else 'Not quite'}")
            if result["is_correct"]:
                def advance() -> None:
                    _reset_question(state, problem_type, difficulty)
                    st.rerun()

                next_question_countdown(state, question_number, advance, seconds=AUTO_ADVANCE_DELAY_SECONDS)

    new_col, performance_col = st.columns((1.4, 4), vertical_alignment="center")
    with new_col:
        st.button("New Question (Circuit)", key=state.key(f"new_circuit_{question_number}"),
                  on_click=_reset_question, args=(state, problem_type, difficulty),
                  width="stretch")
    with performance_col:
        _render_performance(state)
