"""Single Resistor: displayed facts, diagram agreement, and custom-page lifecycle."""
import io
import logging
import math
import random
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from docx import Document
from streamlit.testing.v1 import AppTest
from utils.generators.current_electricity.ohms_law_model import build_circuit_case, CIRCUIT_EQUATION_METADATA
from utils.problem_adapters import circuit_payload
from utils.problem_payload import payload_from_dict
from utils.quantities import PROFILES
from utils.setup_feedback import evaluate_entry
from utils.setup_schema import expected_entries
from utils.solve_for import generate_selected, target_options
from utils.solve_for_custom import OhmsLawTargets
from xtrct_docs.document_creator import create_doc
from xtrct_docs.payload_adapter import DocumentGenerator

TARGETS = {"Voltage": "V", "Current": "I", "Resistance": "R"}
LABELS = {"Battery voltage": "V", "Current": "I", "Resistance": "R"}
UNITS = {"V": "V", "I": "A", "R": "ohms"}
# Independently enumerate all original sampling choices, including decimal cases.
RANGES = {
    "Easy": (range(2, 13), range(1, 7)),
    "Medium": ((3, 4, 5, 6, 8, 10, 12, 15, 18), (0.5, 1, 1.5, 2, 2.5, 3)),
    "Hard": ((2.5, 4, 6, 7.5, 12, 15, 18), (0.4, 0.6, 0.8, 1.2, 1.5, 2.4, 3.2)),
}


def verify_case(case, payload):
    target = TARGETS[case["answer_label"]]
    setup = payload_from_dict(payload).extras["setup"]
    expected = expected_entries(setup)
    assert setup["profile"] == "single_resistor" and setup["target_roles"] == [target]
    facts = {}
    for label, text in case["givens"]:
        key = LABELS[label]
        number, unit = text.split()
        assert unit == UNITS[key]
        facts[key] = float(number)
        assert expected[key] == float(number)
        assert f"- {label}: {text}" in payload["question"]
    assert set(facts) == set(UNITS) - {target}
    assert expected[target] == "?" and "value" not in setup["fields"][target]
    expected_answer = {"V": lambda: facts["I"] * facts["R"],
                       "I": lambda: facts["V"] / facts["R"],
                       "R": lambda: facts["V"] / facts["I"]}[target]()
    assert math.isclose(case["answer"], expected_answer, rel_tol=1e-12)
    assert payload["answers"] == [case["answer"]]
    assert case["unit"] == UNITS[target]
    diagram = case["diagram"]
    labels = {"V": diagram["source_label"], "I": diagram["wire_label"].removeprefix("I = "),
              "R": diagram["resistor_labels"][0]}
    for key, text in labels.items():
        if key == target:
            assert text == "? " + UNITS[key]
        else:
            number, unit = text.split()
            assert float(number) == facts[key] and unit == UNITS[key]
    assert payload_from_dict(payload).extras.get("grading", payload.get("grading")) == {
        "rel_tol": 0.05, "abs_tol": 0.05}


def verify_content():
    count = 0
    for difficulty, (resistances, currents) in RANGES.items():
        for resistance in resistances:
            for current in currents:
                for target in TARGETS:
                    sampler = "randint" if difficulty == "Easy" else "choice"
                    with patch("utils.generators.current_electricity.ohms_law_model.random." + sampler,
                               side_effect=[resistance, current]):
                        case = build_circuit_case("Single Resistor", difficulty, target)
                    verify_case(case, circuit_payload(case))
                    verify_case(case, OhmsLawTargets._payload(case))
                    count += 1
        # Force every Mixed target without assuming random seeds reach each branch.
        for target in TARGETS:
            calls = [target] if difficulty == "Easy" else [resistances[0], currents[0], target]
            with patch("utils.generators.current_electricity.ohms_law_model.random.choice", side_effect=calls):
                payload = generate_selected(OhmsLawTargets(), "Single Resistor", difficulty)
            verify_case(payload["extras"]["case"], payload)
        for option in target_options(OhmsLawTargets(), "Single Resistor", difficulty):
            for seed in range(10):
                random.seed(seed)
                payload = generate_selected(OhmsLawTargets(), "Single Resistor", difficulty, option["id"])
                verify_case(payload["extras"]["case"], payload)
            random.seed(71)
            exported = DocumentGenerator(OhmsLawTargets()).question("Single Resistor", difficulty, option["id"])
            random.seed(71)
            direct = generate_selected(OhmsLawTargets(), "Single Resistor", difficulty, option["id"])
            assert exported["extras"]["setup"] == direct["extras"]["setup"]
            assert exported["answers"] == direct["answers"]
    assert count == 507
    for kind in ("Series Current and Voltage", "Parallel Current and Voltage"):
        for difficulty in RANGES:
            payload = generate_selected(OhmsLawTargets(), kind, difficulty)
            assert "setup" not in payload["extras"]
    roles = PROFILES["single_resistor"]
    expected = {"V": "?", "I": 2, "R": 2}
    assert evaluate_entry("2", "I", expected, roles).status == "correct"
    feedback = evaluate_entry("2", "V", expected, roles)
    assert feedback.code == "matches_other_given" and "start or the end" not in feedback.message
    assert evaluate_entry("x", "V", expected, roles).code == "unclassified"
    assert evaluate_entry("nan", "R", expected, roles).status == "incorrect"
    assert CIRCUIT_EQUATION_METADATA["Single Resistor"]["honors"] == "V = IR"
    # Serialize a shared export with diagram; practice metadata alone does not
    # opt printed worksheets into organizing help or add a student circuit route.
    buffer = io.BytesIO()
    create_doc("Single Resistor", lambda: [{"heading": "Ohm's law", "gap": 0, "problems": [exported]}],
               1, output_path=buffer, open_document=False)
    buffer.seek(0)
    assert Document(buffer).inline_shapes
    print(f"Single Resistor: all {count} curated cases match givens, diagram, units, setup, and answers; export passed.")


def verify_page():
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    at.session_state["router_section"] = "⚡Electricity⚡"
    at.session_state["router_group"] = "Current Electricity"
    at.session_state["router_activity"] = "Circuit Fundamentals"
    at.run()
    prefix = "current_electricity"
    assert not at.exception
    # Upgrade a live session created before the page retained shared payloads.
    previous = at.session_state[prefix + "_question_number"]
    del at.session_state[prefix + "_payload"]
    del at.session_state[prefix + "_question_id"]
    at.run()
    assert not at.exception and at.session_state[prefix + "_question_number"] == previous + 1
    assert at.session_state[prefix + "_payload"].extras["setup"]["profile"] == "single_resistor"
    for difficulty in RANGES:
        at.selectbox(key=prefix + "_difficulty_select").select(difficulty).run()
        for target in ("voltage", "current", "resistance", "mixed"):
            at.selectbox(key=prefix + "_solve_for_select").select(target).run()
            assert not at.exception
            qid = at.session_state[prefix + "_question_number"]
            assert at.session_state[prefix + "_question_id"] == qid
            assert at.session_state[prefix + "_setup_submission"] is None
            assert not any(at.session_state[prefix + "_setup_draft"].values())
            forms = [n.proto.form for n in at.get("form")]
            form = next(f for f in forms if f.form_id == f"{prefix}_setup_form_{qid}")
            assert form.enter_to_submit and not form.clear_on_submit
            assert any(f.form_id == f"{prefix}_answer_form_{qid}" for f in forms)
            assert [i.label for i in at.text_input if "setup_input" in i.key] == [
                "Battery voltage", "Current", "Resistance"]
            before = at.session_state[prefix + "_attempt_count"]
            expected = expected_entries(at.session_state[prefix + "_payload"].extras["setup"])
            for key, value in expected.items():
                at.text_input(key=f"{prefix}_setup_input_{qid}_{key}").set_value(str(value))
            # Form edits are sent by the submit button, without an intervening rerun.
            assert not at.success
            next(b for b in at.button if b.label == "Check setup").click().run()
            assert not at.exception and len(at.success) == 3
            assert at.session_state[prefix + "_question_number"] == qid
            assert at.session_state[prefix + "_attempt_count"] == before
            assert not at.session_state[prefix + "_submitted"]
            requested = next(k for k, v in expected.items() if v == "?")
            given = next(v for v in expected.values() if not isinstance(v, str))
            # Model an external rerun with a changed saved form value.
            at.session_state[f"{prefix}_setup_input_{qid}_{requested}"] = str(given)
            at.run()
            assert any("changed" in c.value for c in at.caption)
            next(b for b in at.button if b.label == "Check setup").click().run()
            assert len(at.error) == 1
            assert any("matches another given" in m.value for m in at.markdown)
    next(b for b in at.button if b.label == "New Question (Circuit)").click().run()
    assert not at.exception
    assert at.session_state[prefix + "_setup_submission"] is None
    assert not any(at.session_state[prefix + "_setup_draft"].values())
    qid = at.session_state[prefix + "_question_number"]
    at.text_input(key=f"{prefix}_answer_{qid}").set_value("inf")
    next(b for b in at.button if b.label == "Check Answer").click().run()
    assert at.session_state[prefix + "_attempt_count"] == 0
    at.session_state[f"{prefix}_cancel_next_{qid}"] = True
    at.text_input(key=f"{prefix}_answer_{qid}").set_value(str(at.session_state[prefix + "_case"]["answer"]))
    next(b for b in at.button if b.label == "Check Answer").click().run()
    at.run()
    assert not at.exception and at.session_state[prefix + "_attempt_count"] == 1
    assert at.session_state[prefix + "_correct_count"] == 1
    assert at.session_state[prefix + "_question_number"] == qid
    assert at.session_state[prefix + "_setup_submission"] is None
    calculation = next(e for e in at.expander if e.label == "View calculation")
    assert not calculation.proto.expanded
    next(b for b in at.button if b.label == "New Question (Circuit)").click().run()
    assert at.session_state[prefix + "_question_number"] == qid + 1
    assert at.session_state[prefix + "_setup_submission"] is None
    assert at.session_state[prefix + "_solve_for"] == "mixed"
    # Incorrect final answers retain the existing single-attempt policy.
    qid = at.session_state[prefix + "_question_number"]
    at.text_input(key=f"{prefix}_answer_{qid}").set_value("-1")
    next(b for b in at.button if b.label == "Check Answer").click().run()
    assert at.session_state[prefix + "_submitted"]
    assert at.session_state[prefix + "_attempt_count"] == 2
    at.run()
    assert at.session_state[prefix + "_attempt_count"] == 2
    for kind in ("Series Current and Voltage", "Parallel Current and Voltage"):
        at.selectbox(key=prefix + "_fundamentals_practice_select").select(kind).run()
        assert not at.exception
        assert "setup" not in at.session_state[prefix + "_payload"].extras
        assert any(e.label == "Organizing help" for e in at.expander)
        assert not any(b.label == "Check setup" for b in at.button)
    at.selectbox(key=prefix + "_fundamentals_practice_select").select("Single Resistor").run()
    assert not at.exception and any(e.label == "Organizing help" for e in at.expander)
    assert at.session_state[prefix + "_setup_submission"] is None
    assert not any(at.session_state[prefix + "_setup_draft"].values())
    print("Single Resistor page passed: nine explicit requests plus Mixed, isolated forms/scoring, feedback, reset, explicit progression, and exclusions.")


if __name__ == "__main__":
    verify_content()
    verify_page()
