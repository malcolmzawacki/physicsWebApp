"""I2 independent physics, qualitative alternatives, rendering, and page lifecycle."""
from dataclasses import replace
import itertools
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.force_diagram_match import CASES, CASE_BY_ID, DIRECTIONS, ForceArrow
from utils.force_diagram_builder import check_builder, new_builder_attempt, render_builder_diagram, submit_builder
from utils.recognizing_forces import FORCE_LABELS, PRACTICE_SETS
from tools.test_force_diagram_match import EXPECTED


def model_checks():
    combinations = 0
    for case in CASES:
        expected = EXPECTED[case.id]
        names = list(expected)
        for specs in itertools.product(itertools.product(DIRECTIONS, (1, 2, 3)), repeat=len(names)):
            arrows = tuple(ForceArrow(f, d, size) for f, (d, size) in zip(names, specs))
            directions_ok = all(d == expected[f][0] for f, (d, _) in zip(names, specs))
            net = [sum(DIRECTIONS[d][axis] * size for d, size in specs) for axis in (0, 1)]
            net_ok = (net[0] == 0 and net[1] > 0) if case.id == "bucket_lift" else (
                net[0] < 0 and net[1] == 0 if case.id in ("crate_slide", "spring_cart") else
                net[0] == 0 and net[1] < 0 if case.id == "ball_rise" else net == [0, 0])
            assert check_builder(case, arrows)["correct"] == (directions_ok and net_ok), (case.id, specs)
            combinations += 1
        for flags in itertools.product((False, True), repeat=len(FORCE_LABELS)):
            arrows = tuple(ForceArrow(f, expected[f][0] if f in expected else "right")
                           for f, flag in zip(FORCE_LABELS, flags) if flag)
            assert check_builder(case, arrows)["forces_ok"] == ({a.force for a in arrows} == set(expected))
        assert render_builder_diagram(case.arrows).startswith(b"\x89PNG")
    bucket = CASE_BY_ID["bucket_lift"]
    assert check_builder(bucket, (ForceArrow("gravity", "down", 2), ForceArrow("tension", "up", 3)))["correct"]
    book = CASE_BY_ID["book_push"]
    assert check_builder(book, tuple(replace(a, size=3 if a.direction in ("left", "right") else 2) for a in book.arrows))["correct"]
    result = check_builder(CASE_BY_ID["book_rest"], (ForceArrow("gravity", "up"),))
    assert result["force_feedback"] and result["direction_feedback"] and result["size_deferred"]
    result = check_builder(CASE_BY_ID["book_rest"], (ForceArrow("gravity", "down"), ForceArrow("normal", "up", 2)))
    assert result["forces_ok"] and not result["direction_feedback"] and result["size_feedback"]
    attempt = new_builder_attempt("book_rest")
    assert submit_builder(attempt, ())
    assert not submit_builder(attempt, ())
    assert submit_builder(attempt, CASE_BY_ID["book_rest"].arrows)
    assert attempt["outcome"] == "Corrected after feedback"
    assert not submit_builder(attempt, ()) and len(attempt["checks"]) == 2
    for direction in DIRECTIONS:
        for size in (1, 2, 3):
            assert render_builder_diagram(tuple(ForceArrow(f, direction, size) for f in FORCE_LABELS)).startswith(b"\x89PNG")
    assert render_builder_diagram(()).startswith(b"\x89PNG")
    for arrows in ((ForceArrow("motion", "up"),), (ForceArrow("gravity", "up", 0),),
                   (ForceArrow("gravity", "up", True),), (ForceArrow("gravity", "diagonal"),),
                   (ForceArrow("gravity", "up"), ForceArrow("gravity", "down"))):
        try:
            check_builder(book, arrows)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid construction accepted")
    print(f"Builder physics passed: {combinations} complete constructions, 1,280 force sets, alternative sizes, category feedback, and rendering stress cases.")


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=30)
    at.session_state["practice_auto_load"] = False
    at.run()

    def click(label):
        next(b for b in at.button if b.label == label).click().run()
        assert not at.exception

    def build(case):
        qid = at.session_state["force_diagram_builder_question_id"]
        at.multiselect(key=f"force_diagram_builder_forces_{qid}").set_value([a.force for a in case.arrows]).run()
        for a in case.arrows:
            at.selectbox(key=f"force_diagram_builder_direction_{qid}_{a.force}").set_value(a.direction)
            at.select_slider(key=f"force_diagram_builder_size_{qid}_{a.force}").set_value(a.size)
        at.run()
        assert not at.exception

    click("Dynamics")
    click("Free-Body Diagram Builder")
    assert next(b for b in at.button if b.label == "Check diagram").proto.type == "primary"
    qid = at.session_state["force_diagram_builder_question_id"]
    at.multiselect(key=f"force_diagram_builder_forces_{qid}").set_value(["gravity"]).run()
    click("Check diagram")
    assert at.warning and not at.session_state["force_diagram_builder_attempt"]["checks"]
    at.selectbox(key=f"force_diagram_builder_direction_{qid}_gravity").set_value("up").run()
    assert not at.session_state["force_diagram_builder_attempt"]["checks"]
    click("Check diagram")
    assert len(at.session_state["force_diagram_builder_attempt"]["checks"]) == 1
    click("Check diagram")
    assert len(at.session_state["practice_answer_history"]) == 1
    click("Show interaction hint")
    assert at.session_state["force_diagram_builder_attempt"]["hint_used"]
    click("Recognizing Forces")
    click("Free-Body Diagram Builder")
    assert at.selectbox(key=f"force_diagram_builder_direction_{qid}_gravity").value == "up"
    for case in CASES:
        at.session_state["force_diagram_builder_attempt"] = new_builder_attempt(case.id)
        at.session_state["force_diagram_builder_question_id"] += 1
        at.run()
        build(case)
        assert not at.session_state["force_diagram_builder_attempt"]["checks"]
        click("Check diagram")
        assert at.success and at.session_state["force_diagram_builder_attempt"]["completed"]
        assert any(t.value.startswith("⭐ x ") for t in at.title)
        assert at.multiselect[0].disabled
        assert next(b for b in at.button if b.label == "Check diagram").disabled
        before = len(at.session_state["practice_answer_history"])
        at.run()
        assert len(at.session_state["practice_answer_history"]) == before
    assert set(at.session_state["practice_answer_history"][-1]["Diagrams"]) == {"Your diagram", "One valid diagram"}
    click("Try a related case")
    assert not at.session_state["force_diagram_builder_attempt"]["draft"]
    for context in PRACTICE_SETS:
        at.selectbox(key="force_diagram_builder_context").set_value(context).run()
        assert not at.exception
        assert not at.session_state["force_diagram_builder_attempt"]["draft"]
    click("Skip question")
    click("Reset practice")
    assert not at.session_state["force_diagram_builder_records"]
    assert not at.session_state["force_diagram_builder_attempt"]["checks"]
    case = CASE_BY_ID[at.session_state["force_diagram_builder_attempt"]["case_id"]]
    build(case)
    qid = at.session_state["force_diagram_builder_question_id"]
    at.session_state["practice_auto_load"] = True
    at.session_state[f"force_diagram_builder_cancel_next_{qid}"] = True
    click("Check diagram")
    assert at.session_state["force_diagram_builder_question_id"] == qid
    at.checkbox(key=f"force_diagram_builder_cancel_next_{qid}").uncheck().run()
    assert at.session_state["force_diagram_builder_question_id"] == qid + 1
    assert len(at.session_state["force_diagram_builder_records"]) == 1
    print("Builder UI passed: live drafts, incomplete direction, explicit checking, retries, hints, navigation, all cases, stars, session images, contexts, reset, and countdown.")


if __name__ == "__main__":
    model_checks()
    ui_checks()
