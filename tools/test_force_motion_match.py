"""C2 force/motion consistency, multi-answer sets, and routed interaction tests."""
import itertools
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.force_motion_match import (
    CASES, CASE_BY_ID, MOTIONS, PRACTICE_SETS, available_cases,
    check_motion_set, compatible, make_options, new_attempt, render_motion, submit_attempt,
)
from utils.graph_cards import selected_indices


def model_checks():
    expected_signs = {"cart_balance": 0, "cart_right": 1, "cart_left": -1,
                      "load_balance": 0, "load_up": 1, "load_down": -1, "ball_gravity": -1}
    count = 0
    for case in CASES:
        assert case.acceleration_sign == expected_signs[case.id]
        correct_ids = {m.id for m in MOTIONS if compatible(case, m)}
        expected_ids = ({"rest", "coast_positive", "coast_negative"} if expected_signs[case.id] == 0 else
                        {"speed_positive", "slow_negative", "start_positive"} if expected_signs[case.id] == 1 else
                        {"speed_negative", "slow_positive", "start_negative"})
        assert correct_ids == expected_ids
        for seed in range(20):
            options = make_options(case, random.Random(seed))
            assert len({m.id for m in options}) == 4
            assert {m.id for m in options} >= expected_ids
            for flags in itertools.product((False, True), repeat=4):
                selected = tuple(i for i, flag in enumerate(flags) if flag)
                expected = {i for i, m in enumerate(options) if m.id in expected_ids}
                result = check_motion_set(case, options, selected)
                assert result["correct"] == (set(selected) == expected)
                assert set(result["missing"]) == expected - set(selected)
                assert set(result["extra"]) == set(selected) - expected
                count += 1
    for motion in MOTIONS:
        x = motion.positions
        assert x[2] - 2*x[1] + x[0] == motion.acceleration
        assert x[3] - 2*x[2] + x[1] == motion.acceleration
        velocities = [motion.v0 + motion.acceleration*t for t in range(4)]
        if motion.id.startswith("slow_"):
            assert abs(velocities[-1]) < abs(velocities[0])
            assert velocities[0] * velocities[-1] > 0  # no reversal in the interval
        for axis in ("horizontal", "vertical"):
            assert render_motion(motion, axis).startswith(b"\x89PNG")
    assert selected_indices({"question_id": 2, "indices": []}, 2, 6) == ()
    assert selected_indices({"question_id": 2, "indices": [4, 1]}, 2, 6) == (1, 4)
    for event in (None, {}, {"question_id": 1, "indices": [0]},
                  {"question_id": 2, "indices": [True]}, {"question_id": 2, "indices": [1, 1]},
                  {"question_id": 2, "indices": [6]}, {"question_id": 2, "indices": "0"}):
        assert selected_indices(event, 2, 6) is None
    for context in PRACTICE_SETS:
        assert len(available_cases(context)) >= 2
    attempt = new_attempt("cart_right")
    assert submit_attempt(attempt)
    assert not submit_attempt(attempt)
    attempt["selection"] = tuple(i for i,m in enumerate(attempt["options"]) if m.id in {"speed_positive", "slow_negative", "start_positive"})
    assert submit_attempt(attempt) and attempt["completed"]
    assert attempt["outcome"] == "Corrected after feedback"
    assert not submit_attempt(attempt)
    print(f"C2 model passed: seven cases, {count} answer sets, nine synchronized motion histories, and 18 rendered diagrams.")


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=30)
    at.session_state["practice_auto_load"] = False
    at.run()

    def click(label):
        next(b for b in at.button if b.label == label).click().run()
        assert not at.exception

    def select(indices, question_id=None):
        qid = at.session_state["force_motion_match_question_id"]
        at.session_state[f"force_motion_match_cards_{qid}"] = {"question_id": qid if question_id is None else question_id, "indices": list(indices)}
        at.run()
        assert not at.exception

    def expected():
        attempt = at.session_state["force_motion_match_attempt"]
        return tuple(i for i,m in enumerate(attempt["options"]) if compatible(CASE_BY_ID[attempt["case_id"]], m))

    click("Dynamics")
    click("Force and Motion Matching")
    click("Check motions")
    assert at.warning and not at.session_state["force_motion_match_attempt"]["checks"]
    select([0, 1])
    select([])
    assert at.session_state["force_motion_match_attempt"]["selection"] == ()
    select([0], question_id=-1)
    assert at.session_state["force_motion_match_attempt"]["selection"] == ()
    good = expected()
    select([good[0]])
    assert not at.session_state["force_motion_match_attempt"]["checks"]
    click("Check motions")
    assert at.warning and not at.session_state["force_motion_match_attempt"]["completed"]
    click("Check motions")
    assert len(at.session_state["practice_answer_history"]) == 1
    click("Show interaction hint")
    click("Free-Body Diagram Builder")
    click("Force and Motion Matching")
    assert at.session_state["force_motion_match_attempt"]["selection"] == (good[0],)
    select(good)
    click("Check motions")
    assert at.success and any(t.value == "⭐ x 1" for t in at.title)
    assert at.session_state["force_motion_match_attempt"]["outcome"] == "Completed with help"
    select([])
    assert at.session_state["force_motion_match_attempt"]["selection"] == good
    assert len(at.session_state["practice_answer_history"]) == 2
    for context in PRACTICE_SETS:
        at.selectbox(key="force_motion_match_context").set_value(context).run()
        assert not at.exception
        assert CASE_BY_ID[at.session_state["force_motion_match_attempt"]["case_id"]] in available_cases(context)
    click("Try a related case")
    click("Skip question")
    click("Reset practice")
    assert at.session_state["force_motion_match_records"] == []
    for case in CASES:
        at.session_state["force_motion_match_attempt"] = new_attempt(case.id)
        at.session_state["force_motion_match_question_id"] += 1
        at.run()
        select(expected())
        click("Check motions")
        assert at.success
        at.run()
        assert len(at.session_state["force_motion_match_attempt"]["checks"]) == 1
    click("Next question")
    qid = at.session_state["force_motion_match_question_id"]
    at.session_state["practice_auto_load"] = True
    at.session_state[f"force_motion_match_cancel_next_{qid}"] = True
    select(expected())
    click("Check motions")
    assert at.session_state["force_motion_match_question_id"] == qid
    at.checkbox(key=f"force_motion_match_cancel_next_{qid}").uncheck().run()
    assert at.session_state["force_motion_match_question_id"] == qid + 1
    count = len(at.session_state["force_motion_match_records"])
    at.run()
    assert len(at.session_state["force_motion_match_records"]) == count
    print("C2 UI passed: multi-selection/deselection, no scoring on edits, exact-set revisions, hints, stale events, navigation, history, stars, contexts/reset, and countdown.")


if __name__ == "__main__":
    model_checks()
    ui_checks()
