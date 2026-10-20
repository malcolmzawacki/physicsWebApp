"""Independent C5 physics, distractor uniqueness, artwork, and routed lifecycle."""
from dataclasses import replace
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.force_diagram_match import (
    CASES, CASE_BY_ID, DIRECTIONS, available_cases, diagram_matches,
    diagram_signature, make_options, render_force_diagram,
)
from utils.recognizing_forces import PRACTICE_SETS

EXPECTED = {
    "book_rest": {"gravity": ("down", 1), "normal": ("up", 1)},
    "puck_coast": {"gravity": ("down", 1), "normal": ("up", 1)},
    "book_push": {"gravity": ("down", 1), "normal": ("up", 1), "applied": ("right", 1), "friction": ("left", 1)},
    "crate_slide": {"gravity": ("down", 1), "normal": ("up", 1), "friction": ("left", 1)},
    "lamp_hang": {"gravity": ("down", 1), "tension": ("up", 1)},
    "bucket_lift": {"gravity": ("down", 1), "tension": ("up", 2)},
    "spring_hang": {"gravity": ("down", 1), "spring": ("up", 1)},
    "spring_cart": {"gravity": ("down", 1), "normal": ("up", 1), "spring": ("left", 1)},
    "ball_rise": {"gravity": ("down", 1)},
    "skydiver": {"gravity": ("down", 1), "drag": ("up", 1)},
}


def model_checks():
    assert set(EXPECTED) == set(CASE_BY_ID)
    for case in CASES:
        assert {a.force: (a.direction, a.size) for a in case.arrows} == EXPECTED[case.id]
        assert {a.force for a in case.arrows} == case.scenario.forces
        net = [sum(DIRECTIONS[d][i] * size for d, size in EXPECTED[case.id].values()) for i in (0, 1)]
        expected_net = {"crate_slide": [-1, 0], "bucket_lift": [0, 1],
                        "spring_cart": [-1, 0], "ball_rise": [0, -1]}.get(case.id, [0, 0])
        assert net == expected_net
        assert diagram_matches(case, tuple(replace(a, size=a.size * 3) for a in case.arrows))
        positions = set()
        for seed in range(50):
            options = make_options(case, random.Random(seed))
            matches = [i for i, option in enumerate(options) if diagram_matches(case, option["arrows"])]
            assert len(matches) == 1
            positions.update(matches)
            assert len({diagram_signature(o["arrows"]) for o in options}) == 4
            assert all(o["feedback"] for o in options)
        assert positions == set(range(4))
        for option in options:
            assert render_force_diagram(option["arrows"]).startswith(b"\x89PNG")
    # Cross-axis comparisons are not promised by the text and must not grade answers.
    case = CASE_BY_ID["book_push"]
    assert diagram_matches(case, tuple(replace(a, size=3) if a.direction in ("left", "right") else a for a in case.arrows))
    for context in PRACTICE_SETS:
        assert len(available_cases(context)) >= 2


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=30)
    at.session_state["practice_auto_load"] = False
    at.run()

    def click(label):
        next(b for b in at.button if b.label == label).click().run()
        assert not at.exception

    def choice(correct):
        attempt = at.session_state["force_diagram_match_attempt"]
        case = CASE_BY_ID[attempt["case_id"]]
        index = next(i for i, o in enumerate(attempt["options"]) if diagram_matches(case, o["arrows"]) == correct)
        qid = at.session_state["force_diagram_match_question_id"]
        checks = len(attempt["checks"])
        at.session_state[f"force_diagram_match_cards_{qid}"] = {"question_id": qid, "index": index}
        at.run()
        assert not at.exception
        assert len(at.session_state["force_diagram_match_attempt"]["checks"]) == checks
        return index

    click("Dynamics")
    click("Match the Free-Body Diagram")
    assert not at.radio
    assert next(b for b in at.button if b.label == "Check diagram").proto.type == "primary"
    click("Check diagram")
    assert at.warning and not at.session_state["force_diagram_match_attempt"]["checks"]
    wrong = choice(False)
    click("Check diagram")
    assert at.warning and len(at.session_state["force_diagram_match_attempt"]["checks"]) == 1
    click("Check diagram")
    assert len(at.session_state["force_diagram_match_attempt"]["checks"]) == 1
    assert len(at.session_state["practice_answer_history"]) == 1
    assert set(at.session_state["practice_answer_history"][0]["Diagrams"]) == {"Your diagram", "Correct diagram"}
    choice(True)
    click("Show interaction hint")
    assert at.session_state["force_diagram_match_attempt"]["hint_used"]
    selected = at.session_state["force_diagram_match_attempt"]["selection"]
    click("Recognizing Forces")
    click("Match the Free-Body Diagram")
    assert at.session_state["force_diagram_match_attempt"]["selection"] == selected
    click("Check diagram")
    assert at.success and at.session_state["force_diagram_match_attempt"]["completed"]
    assert any(t.value == "⭐ x 1" for t in at.title)
    assert at.session_state["force_diagram_match_attempt"]["outcome"] == "Completed with help"
    at.run()
    assert len(at.session_state["practice_answer_history"]) == 2
    click("Try a related case")
    assert not at.success and at.session_state["force_diagram_match_attempt"]["selection"] is None
    qid = at.session_state["force_diagram_match_question_id"]
    at.session_state[f"force_diagram_match_cards_{qid}"] = {"question_id": qid - 1, "index": 0}
    at.run()
    assert at.session_state["force_diagram_match_attempt"]["selection"] is None
    for context in PRACTICE_SETS:
        at.selectbox(key="force_diagram_match_context").select(context).run()
        assert not at.exception
        attempt = at.session_state["force_diagram_match_attempt"]
        assert CASE_BY_ID[attempt["case_id"]] in available_cases(context)
        assert at.session_state["force_diagram_match_attempt"]["selection"] is None
    click("Skip question")
    click("Reset practice")
    assert at.session_state["force_diagram_match_records"] == []
    # All original cases render, select, score once, and remain inspectable.
    for case in CASES:
        at.selectbox(key="force_diagram_match_context").select("All contexts").run()
        at.session_state["force_diagram_match_attempt"] = {
            "case_id": case.id, "options": make_options(case, random.Random(5)), "checks": [],
            "selection": None, "hint_used": False, "completed": False, "outcome": None}
        at.session_state["force_diagram_match_question_id"] += 1
        at.run()
        choice(True)
        click("Check diagram")
        assert at.success
        assert next(b for b in at.button if b.label == "Check diagram").disabled
    click("Next question")
    qid = at.session_state["force_diagram_match_question_id"]
    at.session_state["practice_auto_load"] = True
    at.session_state[f"force_diagram_match_cancel_next_{qid}"] = True
    choice(True)
    click("Check diagram")
    assert at.session_state["force_diagram_match_question_id"] == qid
    at.checkbox(key=f"force_diagram_match_cancel_next_{qid}").uncheck().run()
    assert not at.exception
    assert at.session_state["force_diagram_match_question_id"] == qid + 1
    count = len(at.session_state["force_diagram_match_records"])
    at.run()
    assert len(at.session_state["force_diagram_match_records"]) == count


if __name__ == "__main__":
    model_checks()
    ui_checks()
    print("C5 passed: 10 physical cases, 500 shuffled boards, 40 rendered diagrams, revision/hints, stars, history, filters, navigation, reset, and cancellable progression.")
