from __future__ import annotations

import time

import streamlit as st

from utils.ui_components import (
    build_performance_table,
    init_performance,
    performance_expander,
    record_performance,
)
from utils.ui_state import State
from utils.generators.current_electricity import (
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
    for equation in case.get("equations", ()):
        st.markdown(equation)


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


def _render_series_schematic(drawing, elm, diagram: dict) -> None:
    battery_cls = getattr(elm, "BatteryCell", getattr(elm, "Battery", None))
    if battery_cls is None:
        raise RuntimeError("schemdraw battery element was not available")
    battery = drawing.add(battery_cls().up().label(diagram["source_label"], loc="left"))
    top_wire = elm.Line().right().length(0.9)
    if diagram["wire_label"]:
        top_wire = top_wire.label(diagram["wire_label"], loc="top")
    drawing.add(top_wire)
    for resistor_label in diagram["resistor_labels"]:
        drawing.add(elm.Resistor().right().label(resistor_label))
        drawing.add(elm.Line().right().length(0.9))
    drawing.add(elm.Line().down().length(2.0))
    drawing.add(elm.Line().tox(battery.start))
    drawing.add(elm.Line().toy(battery.start))


def _render_parallel_schematic(drawing, elm, diagram: dict) -> None:
    battery_cls = getattr(elm, "BatteryCell", getattr(elm, "Battery", None))
    if battery_cls is None:
        raise RuntimeError("schemdraw battery element was not available")
    battery = drawing.add(battery_cls().up().label(diagram["source_label"], loc="left"))
    left_node = drawing.add(elm.Line().right().length(1.0))

    drawing.push()
    drawing.add(elm.Line().right().length(1.2))
    drawing.add(elm.Resistor().down().label(diagram["resistor_labels"][0]))
    drawing.add(elm.Line().toy(battery.start))
    drawing.pop()

    drawing.add(elm.Line().right().length(3.0))
    drawing.push()
    drawing.add(elm.Resistor().down().label(diagram["resistor_labels"][1]))
    drawing.add(elm.Line().toy(battery.start))
    drawing.pop()

    drawing.add(elm.Line().down().length(2.0))
    drawing.add(elm.Line().tox(left_node.start))
    drawing.add(elm.Line().toy(battery.start))


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
        with schemdraw.Drawing() as drawing:
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
    tolerance = max(abs(answer) * 0.05, 0.05)
    return abs(user_value - answer) <= tolerance


def current_electricity_series_parallel_page() -> None:
    state = State("current_electricity_series_parallel")
    state.ensure("problem_type", SERIES_PARALLEL_PROBLEM_TYPES[0])
    state.ensure("difficulty", "Easy")
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(list(SERIES_PARALLEL_PROBLEM_TYPES), list(DIFFICULTIES)),
    )

    top_col1, top_col2 = st.columns((2, 1), gap="large")
    with top_col1:
        problem_type = st.radio(
            "Mode",
            options=SERIES_PARALLEL_PROBLEM_TYPES,
            horizontal=True,
            index=SERIES_PARALLEL_PROBLEM_TYPES.index(state.get("problem_type", SERIES_PARALLEL_PROBLEM_TYPES[0])),
            key=state.key("problem_type_select"),
        )
    with top_col2:
        difficulty = st.radio(
            "Difficulty",
            options=DIFFICULTIES,
            horizontal=True,
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
            check_clicked = st.form_submit_button("Check Answer", type="primary", use_container_width=True)

        if check_clicked:
            try:
                user_value = float(answer_text.strip())
            except ValueError:
                st.error("Enter a numeric value before checking the answer.")
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
                st.caption("Loading the next circuit...")
                time.sleep(AUTO_ADVANCE_DELAY_SECONDS)
                _reset_question(state, problem_type, difficulty)
                st.rerun()

    _render_performance(state)
