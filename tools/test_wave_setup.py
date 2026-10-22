"""Wave Properties: every given/target form, displayed precision, and page flow."""
import io
import logging
import math
import re
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from docx import Document
from streamlit.testing.v1 import AppTest
from utils.generators.waves_generator import WaveGenerator
from utils.problem_payload import payload_from_dict
from utils.quantities import PROFILES
from utils.setup_feedback import evaluate_entry
from utils.setup_schema import expected_entries
from utils.solve_for import _catalog, generate_selected, target_options
from xtrct_docs.document_creator import create_doc


# Independent expectations: branch, prompt givens, target, calculation from text.
CASES = [
    (("f", "wavelength"), "v", lambda d: d["wavelength"] * d["f"]),
    (("v", "f"), "wavelength", lambda d: d["v"] / d["f"]),
    (("v", "wavelength"), "f", lambda d: d["v"] / d["wavelength"]),
    (("T", "wavelength"), "v", lambda d: d["wavelength"] / d["T"]),
    (("v", "T"), "wavelength", lambda d: d["v"] * d["T"]),
    (("v", "wavelength"), "T", lambda d: d["wavelength"] / d["v"]),
    (("f",), "T", lambda d: 1 / d["f"]),
    (("T",), "f", lambda d: 1 / d["T"]),
]
WORDS = {"v": "wave speed", "wavelength": "wavelength", "f": "frequency", "T": "period"}
UNITS = {"v": "m/s", "wavelength": "m", "f": "Hz", "T": "s"}


def verify_content():
    generator = WaveGenerator()
    problems = []
    for variant, (given, target, calculate) in enumerate(CASES):
        # Include nonterminating reciprocals, boundaries, and coincident givens.
        for frequency in range(2, 101):
            for wavelength in (2, frequency, 100):
                with patch("utils.generators.waves_generator.ri", side_effect=[frequency, wavelength]):
                    raw = generator.properties_of_waves("Easy", variant=variant)
                payload = payload_from_dict(raw)
                setup = payload.extras["setup"]
                entries = expected_entries(setup)
                text_values = {}
                for role in WORDS:
                    match = re.search(rf"a {WORDS[role]} of ([\d.]+) {re.escape(UNITS[role])}(?= and |\.)", payload.question)
                    assert bool(match) == (role in given), (variant, payload.question, role)
                    if match:
                        number = float(match.group(1))
                        text_values[role] = number
                        assert entries[role] == number
                        if role == "T":
                            assert len(match.group(1).partition(".")[2]) <= 3
                    else:
                        assert entries[role] == ("?" if role == target else "x")
                        assert "value" not in setup["fields"][role]
                assert setup["target_roles"] == [target]
                assert payload.question.endswith(f"What is its {WORDS[target]}?")
                assert payload.units == [f"{PROFILES['wave_properties'][target].name} ({UNITS[target]})"]
                assert math.isclose(payload.answers[0], calculate(text_values), rel_tol=1e-12)
                if frequency == 7 and wavelength == 100:
                    problems.append(raw)
        # Exercise every branch through Mixed practice as well as direct calls.
        with patch("utils.generators.waves_generator.ri", side_effect=[7, 9, variant]):
            assert generate_selected(generator, "Wave Properties", "Easy")["extras"]["wave_variant"] == variant

    entries = _catalog()["WaveGenerator"]["Wave Properties"]
    assert {o["label"] for o in target_options(generator, "Wave Properties", "Easy")} == {
        "Wave Speed", "Wavelength", "Frequency", "Period"}
    assert sorted(c["kwargs"]["variant"] for e in entries for c in e["calls"]) == list(range(8))
    for entry in entries:
        assert len(entry["calls"]) == 2
        for call in entry["calls"]:
            for difficulty in ("Easy", "Medium", "Hard"):
                with patch("utils.solve_for.random.choice", return_value=call):
                    raw = generate_selected(generator, "Wave Properties", difficulty, entry["id"])
                assert raw["extras"]["setup"]["target_roles"] == entry["quantity_roles"]
                assert raw["extras"]["wave_variant"] == call["kwargs"]["variant"]
    for bad in (-1, 8, True, 1.5, "3"):
        try:
            generator.properties_of_waves("Easy", variant=bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid wave variant accepted: {bad!r}")
    roles = PROFILES["wave_properties"]
    expected = {"v": "?", "wavelength": 7, "f": 7, "T": "x"}
    assert evaluate_entry("7", "f", expected, roles).status == "correct"
    feedback = evaluate_entry("7", "T", expected, roles)
    assert feedback.code == "matches_other_given" and "start or the end" not in feedback.message
    assert evaluate_entry("0.143", "T", {**expected, "T": "?"}, roles).code == "unclassified"
    assert evaluate_entry("X", "T", expected, roles).status == "correct"
    assert evaluate_entry("nan", "v", expected, roles).status == "incorrect"
    # Exercise serialization of all eight forms; this does not enable a Waves
    # student worksheet route or add organizing help to printed worksheets.
    output = io.BytesIO()
    create_doc("Wave Properties", lambda: [{"heading": "Eight forms", "gap": 0, "problems": problems}],
               1, output_path=output, open_document=False, include_graphs=False)
    output.seek(0)
    assert Document(output).tables


def verify_page():
    at = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    at.session_state["router_section"] = "Waves"
    at.session_state["router_activity"] = "Wave Properties"
    at.run()
    assert not at.exception
    prefix = "wave_properties"
    for call_index in (0, 1):
        for option in target_options(WaveGenerator(), "Wave Properties", "Easy"):
            with patch("utils.solve_for.random.choice", side_effect=lambda calls: calls[call_index]):
                at.selectbox(key=prefix + "_solve_for_select").select(option["id"]).run()
            assert not at.exception
            qid = at.session_state[prefix + "_question_id"]
            assert at.session_state[prefix + "_setup_submission"] is None
            payload = at.session_state[prefix + "_payload"]
            expected = expected_entries(payload.extras["setup"])
            form = next(n.proto.form for n in at.get("form")
                        if n.proto.form.form_id == f"{prefix}_setup_form_{qid}")
            assert form.enter_to_submit and not form.clear_on_submit
            assert [i.label for i in at.text_input if "setup_input" in i.key] == [
                "Wave speed", "Wavelength", "Frequency", "Period"]
            for key, value in expected.items():
                at.text_input(key=f"{prefix}_setup_input_{qid}_{key}").set_value(str(value))
            # Form edits are sent by the submit button, without an intervening rerun.
            assert not at.success
            next(b for b in at.button if b.label == "Check setup").click().run()
            assert not at.exception and len(at.success) == 4
            assert at.session_state[prefix + "_question_id"] == qid
            assert not at.session_state[prefix + "_submitted"]
            target = payload.extras["setup"]["target_roles"][0]
            given = next(v for v in expected.values() if not isinstance(v, str))
            # Model an external rerun with a changed saved form value.
            at.session_state[f"{prefix}_setup_input_{qid}_{target}"] = str(given)
            at.run()
            assert any("changed" in c.value for c in at.caption)
            next(b for b in at.button if b.label == "Check setup").click().run()
            assert len(at.error) == 1
            assert any("matches another given" in m.value for m in at.markdown)
    next(b for b in at.button if b.label == "New Question").click().run()
    assert not at.exception
    assert at.session_state[prefix + "_setup_submission"] is None
    assert not any(at.session_state[prefix + "_setup_draft"].values())
    # A wrong final answer is independent of an unchecked organizer.
    final = next(i for i in at.text_input if "setup_input" not in i.key)
    final.set_value("-1")
    qid = at.session_state[prefix + "_question_id"]
    next(b for b in at.button if b.label == "Submit").click().run()
    assert not at.exception and at.session_state[prefix + "_setup_submission"] is None
    assert at.session_state[prefix + "_question_id"] == qid
    assert at.session_state[prefix + "_submitted"]  # Existing one-attempt final-answer policy.
    next(b for b in at.button if b.label == "New Question").click().run()
    final = next(i for i in at.text_input if "setup_input" not in i.key)
    final.set_value(str(at.session_state[prefix + "_correct_answers"][0]))
    qid = at.session_state[prefix + "_question_id"]
    next(b for b in at.button if b.label == "Submit").click().run()
    assert not at.exception and at.session_state[prefix + "_question_id"] == qid + 1
    next(b for b in at.sidebar.button if b.label == "Harmonics").click().run()
    assert not at.exception and not any(e.label == "Organizing help" for e in at.expander)


if __name__ == "__main__":
    verify_content()
    verify_page()
    print("Wave Properties passed: 2,376 displayed-value cases, eight forms, targets, DOCX, feedback, and independent form flow.")
