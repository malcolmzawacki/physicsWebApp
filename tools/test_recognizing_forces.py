"""Run with python tools/test_recognizing_forces.py."""
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.recognizing_forces import (
    FORCE_LABELS, PRACTICE_SETS, SCENARIOS, SCENARIO_BY_ID,
    available_scenarios, check_forces, new_attempt, submit_attempt,
)

# Independent reviewed force sets for every original scenario.
EXPECTED = {
    "book_rest": {"gravity", "normal"},
    "book_push": {"gravity", "normal", "applied", "friction"},
    "puck_coast": {"gravity", "normal"},
    "crate_slide": {"gravity", "normal", "friction"},
    "lamp_hang": {"gravity", "tension"},
    "bucket_lift": {"gravity", "tension"},
    "spring_hang": {"gravity", "spring"},
    "spring_cart": {"gravity", "normal", "spring"},
    "ball_rise": {"gravity"},
    "ball_drag": {"gravity", "drag"},
    "skydiver": {"gravity", "drag"},
    "probe_coast": set(),
}


def content_checks():
    assert set(EXPECTED) == set(SCENARIO_BY_ID)
    assert len(SCENARIOS) == len(SCENARIO_BY_ID)
    assert set.union(*EXPECTED.values()) == set(FORCE_LABELS)
    for scenario in SCENARIOS:
        assert scenario.forces == EXPECTED[scenario.id]
        assert scenario.target and scenario.situation and scenario.hint
        assert SCENARIO_BY_ID[scenario.related].context == scenario.context
        assert len(scenario.interactions) == len(scenario.forces)
        for flags in itertools.product((False, True), repeat=len(FORCE_LABELS)):
            selected = {force for force, flag in zip(FORCE_LABELS, flags) if flag}
            result = check_forces(scenario, selected)
            assert result["correct"] == (selected == EXPECTED[scenario.id])
            assert set(result["missing"]) == EXPECTED[scenario.id] - selected
            assert set(result["extra"]) == selected - EXPECTED[scenario.id]
            assert len(result["feedback"]) == len(selected ^ EXPECTED[scenario.id])
    for context in PRACTICE_SETS:
        assert len(available_scenarios(context)) >= 2
    attempt = new_attempt("ball_rise")
    submit_attempt(attempt, {"applied"})
    submit_attempt(attempt, {"applied"})
    assert len(attempt["checks"]) == 1
    submit_attempt(attempt, {"gravity"})
    assert attempt["outcome"] == "Corrected after feedback"
    submit_attempt(attempt, {"normal"})
    assert len(attempt["checks"]) == 2
    attempt = new_attempt("ball_rise")
    attempt["hint_used"] = True
    submit_attempt(attempt, {"gravity"})
    assert attempt["outcome"] == "Completed with help"
    attempt = new_attempt("probe_coast")
    submit_attempt(attempt, [])
    assert attempt["outcome"] == "First try"
    try:
        check_forces(SCENARIOS[0], ["motion"])
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown force accepted")


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25).run()

    def click(label):
        next(b for b in at.button if b.label == label).click().run()
        assert not at.exception

    click("Dynamics")
    click("Recognizing Forces")
    assert at.selectbox(key="nav_level").value == "high"
    for context in PRACTICE_SETS:
        at.selectbox(key="recognizing_forces_context").select(context).run()
        assert not at.exception
        assert SCENARIO_BY_ID[at.session_state["recognizing_forces_attempt"]["scenario_id"]] in available_scenarios(context)
    at.selectbox(key="recognizing_forces_context").select("All contexts").run()
    for scenario in SCENARIOS:
        at.session_state["recognizing_forces_attempt"] = new_attempt(scenario.id)
        at.session_state["recognizing_forces_question_id"] += 1
        at.run()
        question_id = at.session_state["recognizing_forces_question_id"]
        at.session_state[f"recognizing_forces_cancel_next_{question_id}"] = True
        for force in EXPECTED[scenario.id]:
            at.checkbox(key=f"recognizing_forces_answer_{question_id}_{force}").check()
        click("Check forces")
        assert at.success
        assert at.session_state["recognizing_forces_attempt"]["completed"]
        assert next(b for b in at.button if b.label == "Check forces").disabled
        at.run()
        assert len(at.session_state["recognizing_forces_attempt"]["checks"]) == 1
    at.session_state["recognizing_forces_attempt"] = new_attempt("ball_rise")
    at.session_state["recognizing_forces_question_id"] += 1
    at.run()
    qid = at.session_state["recognizing_forces_question_id"]
    click("Check forces")
    assert at.warning
    click("Check forces")
    assert len(at.session_state["recognizing_forces_attempt"]["checks"]) == 1
    at.checkbox(key=f"recognizing_forces_answer_{qid}_gravity").check()
    click("Show interaction hint")
    assert at.checkbox(key=f"recognizing_forces_answer_{qid}_gravity").value
    assert len(at.session_state["recognizing_forces_attempt"]["checks"]) == 1
    click("Newton's Second Law")
    click("Recognizing Forces")
    assert at.checkbox(key=f"recognizing_forces_answer_{qid}_gravity").value
    at.session_state[f"recognizing_forces_cancel_next_{qid}"] = True
    click("Check forces")
    assert at.session_state["recognizing_forces_attempt"]["outcome"] == "Completed with help"
    click("Try a related case")
    assert at.session_state["recognizing_forces_attempt"]["scenario_id"] == "ball_drag"
    assert not at.success and not at.warning
    assert all(not box.value for box in at.checkbox if box.key.startswith("recognizing_forces_answer_"))
    qid = at.session_state["recognizing_forces_question_id"]
    click("Newton's Second Law")
    click("Recognizing Forces")
    assert at.session_state["recognizing_forces_question_id"] == qid
    at.selectbox(key="recognizing_forces_context").select("Springs").run()
    assert not at.exception
    assert at.session_state["recognizing_forces_attempt"]["last_result"] is None
    seen = {at.session_state["recognizing_forces_attempt"]["scenario_id"]}
    click("Skip question")
    assert at.session_state["recognizing_forces_attempt"]["scenario_id"] not in seen
    click("Reset practice")
    assert at.session_state["recognizing_forces_records"] == []
    assert at.session_state["recognizing_forces_attempt"]["checks"] == []
    assert not at.exception
    # Default success advances once, retaining one completed record and star.
    scenario_id = at.session_state["recognizing_forces_attempt"]["scenario_id"]
    qid = at.session_state["recognizing_forces_question_id"]
    assert next(b for b in at.button if b.label == "Check forces").proto.type == "primary"
    for force in EXPECTED[scenario_id]:
        at.checkbox(key=f"recognizing_forces_answer_{qid}_{force}").check()
    click("Check forces")
    assert at.session_state["recognizing_forces_question_id"] == qid + 1
    assert len(at.session_state["recognizing_forces_records"]) == 1
    assert at.session_state["recognizing_forces_records"][0]["completed"]
    assert not at.session_state["recognizing_forces_attempt"]["completed"]
    assert at.session_state["recognizing_forces_attempt"]["scenario_id"] != scenario_id
    at.run()
    assert len(at.session_state["recognizing_forces_records"]) == 1


if __name__ == "__main__":
    content_checks()
    ui_checks()
    print("Recognizing Forces passed: 12 cases, 1,536 answer sets, routed forms, revisions, hints, related cases, navigation, filters, reset, and single scoring.")
