"""Check prompt metadata, per-quantity grading, and independent setup submissions."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest
from utils.generators.kinematics.linear_motion_generator import LinearMotionGenerator
from utils.setup_workspace import check_entry
from utils.setup_feedback import evaluate_entry


def main():
    generator = LinearMotionGenerator()
    values = {"x": -12, "t": 3, "vi": 0, "vf": -8, "a": -2}
    for missing in ("t", "x", "a", "vf"):
        given = [key for key in values if key != missing]
        for target in given:
            payload = generator._build_question(values, target, "cart", given)
            expected = payload["extras"]["setup_expected"]
            assert expected[target] == "?"
            assert expected[missing] == "x"
            for key in set(given) - {target}:
                assert expected[key] == values[key]
    for value, expected in [(" X ", "x"), ("?", "?"), ("0", 0), ("-8.0", -8)]:
        assert check_entry(value, expected)[0] == "correct"
    for value, expected in [("8", -8), ("8.1", 8), ("x", 0), ("?", 8), ("nan", 8), ("inf", 8), ("hello", 8)]:
        assert check_entry(value, expected)[0] == "incorrect"
    assert check_entry("", 0)[0] == "empty"
    expected = {"x": "x", "t": 3, "vi": 0, "vf": "?", "a": -8}
    assert evaluate_entry("-8", "t", expected).code == "matches_other_given"
    assert evaluate_entry("-8", "vf", expected).code == "matches_other_given"
    assert evaluate_entry("0", "vi", expected).code == "correct"
    assert evaluate_entry("8", "a", expected).code == "unclassified"
    for value in ("64", "hello", "nan", "inf", "?"):
        assert evaluate_entry(value, "t", expected).code == "unclassified"
    # Equal values must never cause a correct entry to be diagnosed as a mix-up.
    equal = {**expected, "a": 3}
    assert evaluate_entry("3", "t", equal).code == "correct"
    assert evaluate_entry("3", "vi", equal).code == "matches_other_given"
    # A requested answer's internal numeric value is not among the givens.
    assert evaluate_entry("24", "t", expected).code == "unclassified"

    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25).run()
    next(b for b in at.sidebar.button if b.label == "Kinematics").click().run()
    next(b for b in at.sidebar.button if b.label == "Accelerated Motion").click().run()
    assert not at.exception
    qid = at.session_state["accelerated_motion_question_id"]
    expected = at.session_state["accelerated_motion_payload"].extras["setup_expected"]
    for key, value in expected.items():
        at.text_input(key=f"accelerated_motion_setup_input_{qid}_{key}").set_value(str(value).upper())
    next(b for b in at.button if b.label == "Check setup").click().run()
    assert not at.exception
    assert len(at.success) == 5
    assert at.session_state["accelerated_motion_question_id"] == qid
    assert not at.session_state["accelerated_motion_submitted"]
    at.text_input(key=f"accelerated_motion_setup_input_{qid}_a").set_value("nonsense").run()
    assert len(at.success) == 4
    assert any("changed" in c.value for c in at.caption)
    next(b for b in at.button if b.label == "Check setup").click().run()
    assert len(at.error) == 1
    assert "Acceleration" in at.error[0].value
    assert any("Recheck the value" in m.value for m in at.markdown)
    next(b for b in at.button if b.label == "New Question").click().run()
    assert not at.exception
    assert at.session_state["accelerated_motion_setup_submission"] is None
    assert all(not value for value in at.session_state["accelerated_motion_setup_draft"].values())
    print("Organizing help: metadata, checking, stale results, isolated submission, and reset passed.")


if __name__ == "__main__":
    main()
