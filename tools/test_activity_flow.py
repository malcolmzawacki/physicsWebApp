"""Regression coverage for shared countdowns and the legacy Interface adapter."""
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    at = AppTest.from_string('''
import streamlit as st
from utils.activity_flow import next_question_countdown
from utils.ui_state import State
for prefix in ("first", "second"):
    state = State(prefix)
    state.ensure("question_id", 1)
    next_question_countdown(state, state.get("question_id"), lambda state=state: state.inc("calls"), seconds=.015)
''')
    at.session_state["first_cancel_next_1"] = True
    at.run()
    assert not at.exception
    assert "first_calls" not in at.session_state
    assert at.session_state["second_calls"] == 1
    at.run()
    assert at.session_state["second_calls"] == 1
    at.checkbox(key="first_cancel_next_1").uncheck().run()
    assert at.session_state["first_calls"] == 1
    at.session_state["first_question_id"] = 2
    at.run()
    assert at.session_state["first_calls"] == 2
    assert at.session_state["second_calls"] == 1

    # Existing standard pages keep their default generation callback and scoring.
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=20).run()
    next(b for b in at.sidebar.button if b.label == "Kinematics").click().run()
    next(b for b in at.sidebar.button if b.label == "Constant Motion").click().run()
    assert not at.exception
    question_id = at.session_state["const_motion__question_id"]
    for field, answer in zip(at.text_input, at.session_state["const_motion__correct_answers"]):
        field.set_value(str(answer))
    next(b for b in at.button if b.label == "Submit").click().run()
    assert not at.exception
    assert at.session_state["const_motion__question_id"] == question_id + 1
    assert at.session_state["const_motion__stars"] == 1
    print("Shared countdown passed: cancellation isolation, reruns, fractional duration, and standard-page advancement.")


if __name__ == "__main__":
    main()
