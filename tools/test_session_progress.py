"""Routed regression checks for temporary history and the shared pacing setting."""
import logging
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.session_progress import AUTO_LOAD_KEY, HISTORY_KEY


def page(section, activity, group=None):
    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    for key, value in {"router_section": section, "router_activity": activity,
                       "router_group": group, "nav_level": "advanced", AUTO_LOAD_KEY: False}.items():
        app.session_state[key] = value
    app.run()
    assert not app.exception
    return app


def click(app, label):
    next(b for b in app.button if b.label == label).click().run()
    assert not app.exception


class SessionProgressTests(unittest.TestCase):
    def test_standard_navigation_reruns_manual_next_and_new_session(self):
        app = page("Kinematics", "Constant Motion")
        qid = app.session_state["const_motion__question_id"]
        inputs = [f for f in app.text_input if "setup_input" not in f.key]
        inputs[0].set_value("nan")
        click(app, "Submit")
        self.assertNotIn(HISTORY_KEY, app.session_state)
        expected = app.session_state["const_motion__correct_answers"]
        inputs = [f for f in app.text_input if "setup_input" not in f.key]
        for field, answer in zip(inputs, expected):
            field.set_value(str(answer))
        click(app, "Submit")
        self.assertEqual(app.session_state["const_motion__question_id"], qid)
        self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)
        self.assertEqual(app.session_state[HISTORY_KEY][0]["Result"], "Correct")
        click(app, "My Current Session Progress")
        self.assertEqual(app.title[0].value, "My Current Session Progress")
        self.assertEqual(len(app.expander), 1)
        click(app, "Back to practice")
        self.assertFalse(app.checkbox(key=AUTO_LOAD_KEY).value)
        self.assertEqual(app.session_state["const_motion__question_id"], qid)
        click(app, "New Question")
        self.assertEqual(app.session_state["const_motion__question_id"], qid + 1)
        self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)
        # A second WebSocket session (also what a browser refresh creates) has no history.
        fresh = AppTest.from_file(str(ROOT / "Home.py")).run()
        self.assertTrue(fresh.checkbox(key=AUTO_LOAD_KEY).value)
        self.assertNotIn(HISTORY_KEY, fresh.session_state)

    def test_toggle_back_on_advances_without_duplicate_history(self):
        app = page("Kinematics", "Constant Motion")
        qid = app.session_state["const_motion__question_id"]
        for field, answer in zip([f for f in app.text_input if "setup_input" not in f.key],
                                 app.session_state["const_motion__correct_answers"]):
            field.set_value(str(answer))
        click(app, "Submit")
        app.checkbox(key=AUTO_LOAD_KEY).check().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["const_motion__question_id"], qid + 1)
        self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)

    def test_circuit_history_has_givens_and_persists(self):
        for activity, prefix in [("Circuit Fundamentals", "current_electricity"),
                                 ("Series and Parallel Circuits", "current_electricity_series_parallel")]:
            with self.subTest(activity=activity):
                app = page("⚡Electricity⚡", activity, "Current Electricity")
                case = app.session_state[prefix + "_case"]
                qid = app.session_state[prefix + "_question_number"]
                answers = case.get("answers", [case.get("answer")])
                fields = [f for f in app.text_input if f.key.startswith(prefix + "_answer_")]
                for field, answer in zip(fields, answers):
                    field.set_value(str(answer))
                click(app, "Check Answer")
                self.assertEqual(app.session_state[prefix + "_question_number"], qid)
                self.assertEqual(app.session_state[HISTORY_KEY][0]["Question"]["Givens"], dict(case["givens"]))
                app.run()
                self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)

    def test_conduction_and_induction_hold_feedback(self):
        for activity, prefix in [("Charging by Conduction", "conduction_practice"),
                                 ("Charging by Induction", "induction_practice")]:
            with self.subTest(activity=activity):
                app = page("⚡Electricity⚡", activity, "Static Electricity")
                app.radio(key=prefix + "_difficulty_select").set_value("Easy").run()
                case = app.session_state[prefix + "_case"]
                qid = app.session_state[prefix + "_question_number"]
                if "Conduction" in activity:
                    from utils.generators.static_electricity import sign_label
                    for box in ("a", "b"):
                        app.radio(key=f"{prefix}_final_{box}_{qid}").set_value(sign_label(case["final_sign"]))
                else:
                    for obj in case["asked_objects"]:
                        next(r for r in app.radio if r.key.startswith(prefix + "_sign_") and obj in r.key).set_value(case["expected_signs"][obj])
                click(app, "Check Answer")
                self.assertTrue(app.success)
                self.assertEqual(app.session_state[prefix + "_question_number"], qid)
                self.assertTrue(next(b for b in app.button if b.label == "Check Answer").disabled)
                app.run()
                self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)
                click(app, "New Scenario")
                self.assertEqual(app.session_state[prefix + "_question_number"], qid + 1)

    def test_friction_puzzle_and_comparison(self):
        app = page("⚡Electricity⚡", "Charging by Friction", "Static Electricity")
        app.radio(key="static_electricity_mode_select").set_value("Comparison Practice").run()
        case = app.session_state["friction_compare_case"]
        from utils.generators.static_electricity import compare_materials, get_material
        left, right = case["left_key"], case["right_key"]
        positive, negative = (left, right) if compare_materials(left, right) > 0 else (right, left)
        app.radio(key=f"friction_compare_positive_choice_{left}_{right}").set_value(get_material(positive).label)
        app.radio(key=f"friction_compare_negative_choice_{left}_{right}").set_value(get_material(negative).label)
        click(app, "Check Answer")
        self.assertTrue(app.success)
        self.assertEqual(app.session_state["friction_compare_case"], case)
        app.radio(key="static_electricity_mode_select").set_value("Ranking Logic Puzzle").run()
        qid = app.session_state["friction_puzzle_question_number"]
        for i, label in enumerate(app.session_state["friction_puzzle_case"]["hidden_order"]):
            app.selectbox(key=f"friction_puzzle_rank_{i}_{qid}").select(label)
        click(app, "Check Puzzle")
        self.assertTrue(app.success)
        self.assertEqual(app.session_state["friction_puzzle_question_number"], qid)
        self.assertEqual(len(app.session_state[HISTORY_KEY]), 2)
        click(app, "My Current Session Progress")
        self.assertEqual(len(app.expander), 2)

    def test_matching_history_preserves_graphs(self):
        app = page("Kinematics", "Matching Motion Graphs")
        qid = app.session_state["motion_graph_matching_question_id"]
        payload = app.session_state["motion_graph_matching_payload"]
        app.session_state["motion_graph_matching_cards"] = {"question_id": qid, "index": payload["correct_index"]}
        app.run()
        click(app, "Check Match")
        self.assertEqual(app.session_state["motion_graph_matching_question_id"], qid)
        record = app.session_state[HISTORY_KEY][0]
        self.assertEqual(len(record["Diagrams"]), 1 + len(payload["option_diagrams"]))
        click(app, "My Current Session Progress")
        self.assertFalse(app.exception)

    def test_other_practice_pages_record_results(self):
        app = page("Foundations", "Scientific Notation")
        for field, value in zip(app.number_input, [app.session_state["sci_notate_ans1"], app.session_state["sci_notate_ans2"]]):
            field.set_value(float(value))
        click(app, "Submit")
        self.assertEqual(app.session_state[HISTORY_KEY][0]["Result"], "Correct")
        app = page("Chemistry", "Compound Names Practice")
        app.text_input[0].set_value(app.session_state["compound_names_correct_name"])
        click(app, "Check Answer")
        self.assertEqual(app.session_state[HISTORY_KEY][0]["Result"], "Correct")
        app = page("Chemistry", "Stoichiometry Practice")
        app.number_input[0].set_value(0.0)
        click(app, "Submit Answer")
        self.assertEqual(app.session_state[HISTORY_KEY][0]["Result"], "Incorrect")
        click(app, "My Current Session Progress")
        self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
