"""Question-flow components that do not own generation, scoring, or page layout."""
import math
import time
from collections.abc import Callable

import streamlit as st
from utils.ui_state import State


def next_question_countdown(
    state: State, question_id: int, on_next: Callable[[], None], seconds: float = 3,
) -> None:
    """Show a cancellable countdown, then invoke the page's next-question action.

    Call after rendering correct feedback. The caller owns scoring and decides
    when this component appears. `on_next` must replace the question and rerun.
    A stable question ID preserves the deadline across Streamlit reruns; a new
    ID resets both the timer and cancellation. State must be activity-specific.
    """
    if not math.isfinite(seconds) or seconds < 0:
        raise ValueError("Countdown seconds must be finite and nonnegative")
    if state.get("advance_question_id") != question_id:
        state.set("advance_question_id", question_id)
        state.set("advance_deadline", time.monotonic() + seconds)
        state.set("advance_fired", False)
    countdown = st.empty()
    with countdown.container():
        progress_col, cancel_col = st.columns([5, 2])
        with cancel_col:
            canceled = st.checkbox("Cancel Next Question", key=state.key(f"cancel_next_{question_id}"))
        with progress_col:
            progress = st.progress(0.0, "Next Question")
    if canceled or state.get("advance_fired"):
        return
    deadline = state.get("advance_deadline")
    while True:
        remaining = max(0.0, deadline - time.monotonic())
        progress.progress(1.0 if seconds == 0 else min(1.0, max(0.0, 1 - remaining / seconds)), "Next Question")
        if remaining == 0:
            break
        time.sleep(min(.05, remaining))
    state.set("advance_fired", True)
    countdown.empty()
    on_next()
