"""Generic layout for matching a primary diagram to one of several options."""

from __future__ import annotations

import time
from typing import Callable, Dict, Optional

import streamlit as st

from utils.ui_components import render_header
from utils.ui_state import State
from utils.word_lists import random_correct_message, random_error_message


def render_diagram_match_layout(
    title: str,
    prefix: str,
    payload_factory: Callable[[Dict[str, object]], Dict[str, object]],
    controls: Optional[Callable[[State], Dict[str, object]]] = None,
    generate_label: str = "Generate New Matching Set",
    auto_advance_timer: float = 3.0,
) -> None:
    state = State(prefix)
    state.ensure("payload", None)
    state.ensure("stars", 0)

    render_header(title, state.get("stars", 0) or None)

    control_state: Dict[str, object] = {}
    if controls is not None:
        control_state = controls(state) or {}

    if state.get("payload") is None:
        state.set("payload", payload_factory(control_state))

    if st.button(generate_label, key=state.key("generate")):
        payload = payload_factory(control_state)
        state.set("payload", payload)

    payload = state.get("payload")
    if payload is None:
        st.info(f"Click '{generate_label}' to start.")
        return

    prompt = payload.get("prompt", "Select the matching diagram:")
    primary_diagram = payload.get("primary_diagram")
    option_diagrams = payload.get("option_diagrams", [])
    correct_index = payload.get("correct_index")
    choice_labels = payload.get("choice_labels")

    if choice_labels is None:
        choice_labels = [chr(ord("A") + i) for i in range(len(option_diagrams))]

    st.write(prompt)
    if primary_diagram is not None:
        st.pyplot(primary_diagram)

    if option_diagrams:
        cols = st.columns(len(option_diagrams))
        for fig_opt, col, label in zip(option_diagrams, cols, choice_labels):
            with col:
                st.write(f"Option {label}")
                st.pyplot(fig_opt)

        user_choice = st.radio(
            "Which graph matches?",
            choice_labels,
            horizontal=True,
            key=state.key("choice"),
        )

        if st.button("Check Match", key=state.key("check")):
            chosen_index = choice_labels.index(user_choice)
            if chosen_index == correct_index:
                st.success(random_correct_message())
                state.inc("stars", 1)
                _auto_advance(
                    payload_factory,
                    control_state,
                    state,
                    auto_advance_timer,
                    generate_label,
                )
            else:
                st.error(random_error_message())
    else:
        st.info(f"Click '{generate_label}' to see the options.")


def _auto_advance(
    payload_factory: Callable[[Dict[str, object]], Dict[str, object]],
    control_state: Dict[str, object],
    state: State,
    timer: float,
    generate_label: str,
) -> None:
    total_ticks = int(timer * 100)
    col1, col2 = st.columns([5, 2])
    with col1:
        progress = st.progress(0, "Next Question")
    with col2:
        cancel = st.checkbox("Cancel Next Question", key=state.key("cancel_next"))
    for i in range(total_ticks):
        if cancel:
            return
        time.sleep(0.01)
        progress.progress((i + 1) / total_ticks, "Next Question")
    payload = payload_factory(control_state)
    state.set("payload", payload)
    st.rerun()
