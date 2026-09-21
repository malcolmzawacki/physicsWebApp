"""Diagram matching with per-question scoring and shared advancement."""
from typing import Callable, Dict, Optional
import streamlit as st
from utils.activity_flow import next_question_countdown
from utils.ui_components import render_header, init_performance, record_performance, build_performance_table, performance_expander
from utils.ui_state import State
from utils.word_lists import random_correct_message, random_error_message
from utils.graph_cards import graph_cards, prepare_images, selected_index


def render_diagram_match_layout(title: str, prefix: str,
        payload_factory: Callable[[Dict[str, object]], Dict[str, object]],
        controls: Optional[Callable[[State], Dict[str, object]]] = None,
        generate_label: str = "Generate New Matching Set", auto_advance_timer: float = 3.0) -> None:
    state = State(prefix)
    state.ensure("stars", 0)
    state.ensure("question_id", 0)
    state.ensure_lazy("performance", lambda: init_performance([title], ["Easy"]))
    render_header(title, state.get("stars") or None)
    control_col, layout_col, new_col = st.columns([3, 2, 2], vertical_alignment="bottom")
    with control_col:
        settings = (controls(state) or {}) if controls else {}
    with layout_col:
        layout = st.selectbox("Graph layout", ["Options in a column", "Compact grid"], key=state.key("layout"))
    with new_col:
        new_requested = st.button(generate_label, key=state.key("generate"))

    def generate():
        state.set("payload", payload_factory(settings))
        state.set("settings", dict(settings))
        state.inc("question_id")
        state.set("submitted", False)
        state.set("selection", None)
        state.pop("card_images")
        state.pop("last_result")
        state.pop("feedback")

    def advance():
        generate()
        st.rerun()

    if state.get("payload") is None or state.get("settings") != settings:
        generate()
    if new_requested:
        advance()
    payload = state.get("payload")
    options = payload.get("option_diagrams", [])
    labels = payload.get("choice_labels") or [chr(65 + i) for i in range(len(options))]
    st.write(payload.get("prompt", "Select the matching diagram:"))
    if not options:
        st.info(f"Click '{generate_label}' to see the options.")
        return
    if state.get("card_images") is None:
        state.set("card_images", prepare_images(payload))
    event = graph_cards(state.get("card_images"), labels, state.get("question_id"),
                        state.get("selection"), state.get("submitted"), layout,
                        key=state.key("cards"), correct_index=payload["correct_index"])
    index = selected_index(event, state.get("question_id"), len(options))
    if not state.get("submitted") and index is not None and index != state.get("selection"):
        state.set("selection", index)
        st.rerun()
    choice = state.get("selection")
    if st.button("Check Match", key=state.key("check"), disabled=state.get("submitted")):
        if choice is None:
            st.error("Choose a graph before checking.")
        else:
            correct = choice == payload["correct_index"]
            state.set("submitted", True)
            state.set("last_result", correct)
            state.set("feedback", random_correct_message() if correct else random_error_message())
            state.set("performance", record_performance(state.get("performance"), title, "Easy", correct))
            if correct:
                state.inc("stars", 1)
            st.rerun()
    if state.get("submitted"):
        if state.get("last_result"):
            st.success(state.get("feedback"))
        else:
            st.error(f"{state.get('feedback')} The correct option is {labels[payload['correct_index']]}.")
    performance_expander(build_performance_table(state.get("performance"), ["Easy"]))
    if state.get("submitted") and state.get("last_result"):
        next_question_countdown(state, state.get("question_id"), advance, auto_advance_timer)
