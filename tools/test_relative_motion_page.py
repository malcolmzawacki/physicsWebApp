"""Run with python tools/test_relative_motion_page.py (requires Streamlit)."""
import sys
from pathlib import Path
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.word_lists import correct_messages, error_messages


def main():
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=20).run()
    assert not at.exception
    at.sidebar.button[1].click().run()  # Kinematics
    assert "Relative Motion" not in [b.label for b in at.sidebar.button]
    at.selectbox(key="nav_level").select("advanced").run()
    next(b for b in at.sidebar.button if b.label == "Relative Motion").click().run()
    assert not at.exception
    for kind in ("Independent motion", "Nested reference frames", "Combined"):
        at.selectbox(key="relative_motion_type_select").select(kind).run()
        for difficulty in ("Easy", "Medium", "Hard"):
            at.selectbox(key="relative_motion_difficulty_select").select(difficulty).run()
            for target in ("Result", "Missing velocity", "Mixed practice"):
                at.selectbox(key="relative_motion_target_select").select(target).run()
                assert not at.exception
                assert at.session_state["relative_motion_payload"]["question"]
    at.checkbox(key="relative_motion_more_equations").check().run()
    assert "begin{gathered}" in at.latex[0].value
    at.selectbox(key="relative_motion_target_select").select("Missing velocity").run()
    question_id = at.session_state["relative_motion_question_id"]
    at.text_input[0].set_value("nan")
    next(b for b in at.button if b.label == "Submit").click().run()
    assert at.error and not at.session_state["relative_motion_submitted"]
    answer = at.session_state["relative_motion_payload"]["answers"][0]
    # Pause this question so feedback and the worked solution can be inspected.
    at.session_state[f"relative_motion_cancel_next_{question_id}"] = True
    at.text_input[0].set_value(str(answer))
    next(b for b in at.button if b.label == "Submit").click().run()
    assert at.success and at.session_state["relative_motion_stars"] == 3
    assert at.success[0].value in correct_messages
    message = at.success[0].value
    assert at.session_state["relative_motion_question_id"] == question_id
    at.run()
    assert at.session_state["relative_motion_stars"] == 3
    assert at.success[0].value == message
    at.checkbox(key=f"relative_motion_cancel_next_{question_id}").uncheck().run()
    assert not at.session_state["relative_motion_submitted"]
    assert at.session_state["relative_motion_question_id"] > question_id
    assert at.session_state["relative_motion_selection"] == ("Combined", "Hard", "Missing velocity")
    assert at.session_state["relative_motion_payload"]["extras"]["solve_for"] != "result"
    # A fresh correct submission advances by default, with no second click.
    question_id = at.session_state["relative_motion_question_id"]
    at.text_input[0].set_value(str(at.session_state["relative_motion_payload"]["answers"][0]))
    next(b for b in at.button if b.label == "Submit").click().run()
    assert at.session_state["relative_motion_question_id"] == question_id + 1
    assert at.session_state["relative_motion_stars"] == 6
    question_id = at.session_state["relative_motion_question_id"]
    at.text_input[0].set_value("9999")
    next(b for b in at.button if b.label == "Submit").click().run()
    assert at.error and at.session_state["relative_motion_stars"] == 6
    assert any(at.error[0].value.startswith(message) for message in error_messages)
    at.run()
    assert at.session_state["relative_motion_question_id"] == question_id
    at.button(key="relative_motion_new_question").click().run()
    assert not at.session_state["relative_motion_submitted"]
    at.selectbox(key="nav_level").select("high").run()
    assert not at.text_input and "Relative Motion" not in [b.label for b in at.sidebar.button]
    assert not at.exception
    print("Relative motion UI passed: 27 selections, feedback, auto-advance, cancellation, single scoring, and access gate.")


if __name__ == "__main__":
    main()
