"""Bounded Newton's Second Law rollout: all Easy cases, targets, and page flow."""
import logging
import re
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.force_generator import ForceGenerator
from utils.problem_payload import payload_from_dict
from utils.quantities import PROFILES
from utils.setup_feedback import evaluate_entry
from utils.setup_schema import expected_entries
from utils.solve_for import generate_selected, target_options
from xtrct_docs.payload_adapter import DocumentGenerator


def main():
    generator = ForceGenerator()
    options = target_options(generator, "Newton's Second Law", "Easy")
    targets = ("a", "Fnet", "m")
    patterns = {"Fnet": r"(\d+\.\d+) N", "m": r"(\d+\.\d+) kg", "a": r"(\d+\.\d+) m/s\^2"}
    count = 0
    for mass in range(1, 11):
        for acceleration in range(1, 11):
            for option, target in zip(options, targets):
                with patch("utils.generators.force_generator.random.randint", side_effect=[17, mass, acceleration]), patch("utils.generators.force_generator.random_noun", return_value="cart"):
                    payload = payload_from_dict(generate_selected(generator, "Newton's Second Law", "Easy", option["id"]))
                setup = payload.extras["setup"]
                facts = {key: float(re.search(pattern, payload.question).group(1)) for key, pattern in patterns.items() if key != target}
                assert not re.search(patterns[target], payload.question)
                expected = {key: "?" if key == target else value for key, value in {"Fnet": mass * acceleration, "m": mass, "a": acceleration}.items()}
                assert expected_entries(setup) == expected
                assert setup["target_roles"] == [target] and "value" not in setup["fields"][target]
                calculated = facts["Fnet"] / facts["m"] if target == "a" else facts["m"] * facts["a"] if target == "Fnet" else facts["Fnet"] / facts["a"]
                assert payload.answers == [calculated]
                assert "net force" in payload.question.lower()
                count += 1
    for variant, target in enumerate(targets, 1):
        with patch("utils.generators.force_generator.random.randint", side_effect=[17, 3, 8, variant]):
            mixed = generate_selected(generator, "Newton's Second Law", "Easy", "mixed")
        assert mixed["extras"]["setup"]["target_roles"] == [target]
    for option, target in zip(options, targets):
        exported = DocumentGenerator(generator).question("Newton's Second Law", "Easy", option["id"])
        assert exported["extras"]["setup"]["target_roles"] == [target]
    for difficulty in ("Medium", "Hard"):
        for option in target_options(generator, "Newton's Second Law", difficulty):
            result = generate_selected(generator, "Newton's Second Law", difficulty, option["id"])
            assert "force_plan" in result["extras"] and len(result["answers"]) == 2
            plan = result["extras"]["force_plan"]
            assert plan["steps"][0]["answer"] == plan["given"]["Mass (kg)"] * 10
    roles = PROFILES["newtons_second_law"]
    assert evaluate_entry("4", "m", {"Fnet": 4, "m": 4, "a": "?"}, roles).status == "correct"
    feedback = evaluate_entry("2", "Fnet", {"Fnet": 6, "m": 2, "a": "?"}, roles)
    assert feedback.code == "matches_other_given" and "start or the end" not in feedback.message

    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    app.session_state["router_section"] = "Dynamics"
    app.session_state["router_activity"] = "Newton's Second Law"
    app.run()
    prefix = "newtons_2nd"
    assert not app.exception
    for target_id in [o["id"] for o in options] + ["mixed"]:
        app.selectbox(key=prefix + "_solve_for_select").select(target_id).run()
        assert not app.exception
        qid = app.session_state[prefix + "_question_id"]
        forms = [node.proto.form for node in app.get("form")]
        setup_form = next(f for f in forms if f.form_id == f"{prefix}_setup_form_{qid}")
        assert setup_form.enter_to_submit and not setup_form.clear_on_submit
        assert any(f.form_id == prefix + "_form" for f in forms)
        assert [i.label for i in app.text_input if "setup_input" in i.key] == ["Net force", "Mass", "Acceleration"]
        expected = expected_entries(app.session_state[prefix + "_payload"].extras["setup"])
        for key, value in expected.items():
            app.text_input(key=f"{prefix}_setup_input_{qid}_{key}").set_value(str(value))
        # Form edits are sent by the submit button, without an intervening rerun.
        assert not app.success
        next(b for b in app.button if b.label == "Check setup").click().run()
        assert not app.exception and len(app.success) == 3
        assert not app.session_state[prefix + "_submitted"]
        assert app.session_state[prefix + "_question_id"] == qid
    next(b for b in app.button if b.label == "New Question").click().run()
    assert app.session_state[prefix + "_setup_submission"] is None
    assert not any(app.session_state[prefix + "_setup_draft"].values())
    qid = app.session_state[prefix + "_question_id"]
    app.session_state[f"{prefix}_cancel_next_{qid}"] = True
    next(i for i in app.text_input if "setup_input" not in i.key).set_value(str(app.session_state[prefix + "_correct_answers"][0]))
    next(b for b in app.button if b.label == "Submit").click().run()
    assert not app.exception and app.success
    assert app.session_state[prefix + "_stars"] == 1
    app.run()
    assert app.session_state[prefix + "_stars"] == 1
    app.checkbox(key=f"{prefix}_cancel_next_{qid}").uncheck().run()
    assert app.session_state[prefix + "_question_id"] == qid + 1
    for difficulty in ("Medium", "Hard"):
        app.selectbox(key=prefix + "_difficulty_select_unified").select(difficulty).run()
        assert not app.exception
        assert any(e.label == "Organizing help" for e in app.expander)
        plan = app.session_state[prefix + "_payload"].extras["force_plan"]
        qid = app.session_state[prefix + "_question_id"]
        assert app.session_state[prefix + "_setup_submission"] is None
        for index, value in enumerate(plan["given"].values()):
            app.text_input(key=f"{prefix}_force_plan_{qid}_given_{index}").set_value(str(value))
        for index, step in enumerate(plan["steps"]):
            app.text_input(key=f"{prefix}_force_plan_{qid}_step_{index}").set_value(str(step["answer"]))
        next(b for b in app.button if b.label == "Check organized work").click().run()
        assert not app.exception and len(app.success) == len(plan["given"]) + len(plan["steps"])
        assert not app.session_state[prefix + "_submitted"]
    app.selectbox(key=prefix + "_difficulty_select_unified").select("Easy").run()
    assert not app.exception and any(e.label == "Organizing help" for e in app.expander)
    assert app.session_state[prefix + "_setup_submission"] is None
    print(f"Newton's Second Law: {count} Easy cases, all targets/Mixed, feedback, export, independent forms, scoring, progression, and Medium/Hard prototype transitions passed.")


if __name__ == "__main__":
    main()

