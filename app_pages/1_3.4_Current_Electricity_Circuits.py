from __future__ import annotations

from utils.grading import parse_number, answer_matches, CIRCUIT_POLICY
from utils.solve_for import select_target, generate_selected, MIXED
from utils.solve_for_custom import OhmsLawTargets
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
    CIRCUIT_EQUATION_METADATA,
    PROBLEM_TYPES,
    build_circuit_case,
    format_answer_value,
)

AUTO_ADVANCE_DELAY_SECONDS = 2
DIFFICULTIES: tuple[str, ...] = ("Easy", "Medium", "Hard")


def _render_givens(case: dict) -> None:
    st.markdown("#### Givens")
    for label, value in case["givens"]:
        st.markdown(f"- **{label}:** `{value}`")


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
            battery_cls = getattr(elm, "BatteryCell", getattr(elm, "Battery", None))
            if battery_cls is None:
                raise RuntimeError("schemdraw battery element was not available")
            battery = drawing.add(battery_cls().up().label(diagram["source_label"], loc="left"))
            drawing.add(elm.Line().right().length(0.9).label(diagram["wire_label"], loc="top"))
            for resistor_label in diagram["resistor_labels"]:
                drawing.add(elm.Resistor().right().label(resistor_label))
                drawing.add(elm.Line().right().length(0.9))
            drawing.add(elm.Line().down().length(2.0))
            drawing.add(elm.Line().tox(battery.start))
            drawing.add(elm.Line().toy(battery.start))
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

    st.markdown(svg_bytes.decode("utf-8"), unsafe_allow_html=True)


def _render_diagram_panel(case: dict) -> None:
    st.markdown("#### Circuit Diagram")
    _render_schematic(case)
    _render_givens(case)


def _reset_question(state: State, problem_type: str, difficulty: str) -> None:
    payload = generate_selected(OhmsLawTargets(), problem_type, difficulty, state.get("solve_for", MIXED))
    state.set("case", payload["extras"]["case"])
    state.inc("question_number")
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


    top_col1, top_col2, top_col3 = question_columns()
    with top_col1:
        problem_type = st.selectbox(
            "Problem Type",
            options=PROBLEM_TYPES,
            index=PROBLEM_TYPES.index(state.get("problem_type", PROBLEM_TYPES[0])),
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
    previous_target = state.get("solve_for", MIXED)
    with top_col3:
        target = select_target(OhmsLawTargets(), problem_type, difficulty, state)
    state.set("solve_for", target)
    previous_difficulty = state.get("difficulty")
    state.set("problem_type", problem_type)
    state.set("difficulty", difficulty)

    if not state.has("case"):
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
