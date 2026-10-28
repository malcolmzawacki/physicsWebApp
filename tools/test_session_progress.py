"""Routed regression checks for temporary history and the shared pacing setting."""
import logging
from datetime import date, datetime, timezone
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.session_progress import AUTO_LOAD_KEY, HISTORY_KEY, SESSION_CODE_KEY, activity_summary, daily_history, progress_date


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
        code = app.session_state[SESSION_CODE_KEY]
        self.assertRegex(code, r"^\d{4}-\d{4}-\d{4}-\d{4}$")
        click(app, "My Current Session Progress")
        self.assertTrue(any(code in caption.value for caption in app.caption))
        self.assertTrue(app.title[0].value.startswith("Progress for "))
        self.assertEqual(next(m.value for m in app.metric if m.label == "Total stars in saved progress"), "⭐ 1")
        app.run()
        self.assertEqual(next(m.value for m in app.metric if m.label == "Total stars in saved progress"), "⭐ 1")
        self.assertEqual(len(app.table), 1)
        self.assertEqual([e.label for e in app.expander if e.label != "Functions & history"], [])
        click(app, "Back to practice")
        self.assertFalse(app.checkbox(key=AUTO_LOAD_KEY).value)
        self.assertEqual(app.session_state["const_motion__question_id"], qid)
        click(app, "New Question")
        self.assertEqual(app.session_state["const_motion__question_id"], qid + 1)
        self.assertEqual(len(app.session_state[HISTORY_KEY]), 1)
        self.assertEqual(app.session_state[SESSION_CODE_KEY], code)
        # AppTest has no browser storage; a new simulated connection starts empty.
        fresh = AppTest.from_file(str(ROOT / "Home.py")).run()
        self.assertTrue(fresh.checkbox(key=AUTO_LOAD_KEY).value)
        self.assertNotIn(HISTORY_KEY, fresh.session_state)
        self.assertNotIn(SESSION_CODE_KEY, fresh.session_state)

    def test_session_code_stays_stable_and_new_session_gets_another(self):
        from unittest.mock import patch
        with patch("utils.session_progress.secrets.randbelow", side_effect=[1234567890123456, 9876543210987654]) as random_number:
            app = AppTest.from_file(str(ROOT / "Home.py")).run()
            click(app, "My Current Session Progress")
            self.assertEqual(app.session_state[SESSION_CODE_KEY], "1234-5678-9012-3456")
            app.run()
            click(app, "Back to practice")
            click(app, "My Current Session Progress")
            self.assertEqual(app.session_state[SESSION_CODE_KEY], "1234-5678-9012-3456")
            fresh = AppTest.from_file(str(ROOT / "Home.py")).run()
            click(fresh, "My Current Session Progress")
            self.assertEqual(fresh.session_state[SESSION_CODE_KEY], "9876-5432-1098-7654")
            self.assertEqual(random_number.call_count, 2)

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
                self.assertEqual(app.session_state[HISTORY_KEY][0]["Problem type"], case["problem_type"])
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
        self.assertEqual(len(app.table[0].value), 2)

    def test_matching_history_preserves_graphs(self):
        app = page("Kinematics", "Matching Motion Graphs")
        qid = app.session_state["motion_graph_matching_question_id"]
        payload = app.session_state["motion_graph_matching_payload"]
        app.session_state["motion_graph_matching_cards"] = {"question_id": qid, "index": payload["correct_index"]}
        app.run()
        click(app, "Check Match")
        self.assertEqual(app.session_state["motion_graph_matching_question_id"], qid)
        record = app.session_state[HISTORY_KEY][0]
        self.assertEqual(record["Problem type"], "Position-Time First")
        self.assertEqual(len(record["Diagrams"]), 1 + len(payload["option_diagrams"]))
        click(app, "My Current Session Progress")
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("imgs")), 0)
        app.radio(key="progress_view").set_value("Review answers").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.selectbox(key="progress_answer_selection").options), 1)

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

    def test_summary_counts_checks_and_uses_school_date(self):
        day = date(2026, 10, 21)
        history = [
            {"Activity": "Motion", "Result": "Incorrect", "Date": "2026-10-21"},
            {"Activity": "Motion", "Result": "Correct", "Date": "2026-10-21"},
            {"Activity": "Forces", "Result": "Correct", "Date": "2026-10-21"},
            {"Activity": "Motion", "Result": "Correct", "Date": "2026-10-20"},
        ]
        self.assertEqual(activity_summary(daily_history(history, day)), [
            {"Activity": "Motion", "Problem type": "Unspecified", "Checks": 2, "Correct": 1, "Incorrect": 1, "Stars": 1},
            {"Activity": "Forces", "Problem type": "Unspecified", "Checks": 1, "Correct": 1, "Incorrect": 0, "Stars": 1},
        ])
        # The daily table is filtered, but the running total spans this session.
        from unittest.mock import patch
        app = AppTest.from_string("from utils.session_progress import render_session_progress\nrender_session_progress()")
        app.session_state[HISTORY_KEY] = history
        with patch("utils.session_progress.progress_date", return_value=day):
            app.run()
        self.assertFalse(app.exception)
        self.assertEqual(next(m.value for m in app.metric if m.label == "Total stars in saved progress"), "⭐ 3")
        with patch("utils.session_progress.progress_date", return_value=day):
            app.selectbox(key="progress_day").select("2026-10-20").run()
        self.assertEqual(app.title[0].value, "Progress for October 20, 2026")
        self.assertEqual(len(app.table[0].value), 1)
        # Midnight in UTC is still the previous school day in New York.
        self.assertEqual(progress_date(datetime(2026, 10, 22, 1, tzinfo=timezone.utc)), day)

    def test_many_answers_stay_compact_and_review_shows_one_record(self):
        app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
        from unittest.mock import patch
        records = []
        for i in range(180):
            records.append({"Activity": f"Activity {i % 12 + 1}", "Date": "2026-10-21",
                            "Result": "Correct", "Question": f"Question {i}",
                            "Your answer": "5 m/s", "Correct answer": "5 m/s",
                            "Difficulty": "Easy", "Explanation": "Divide distance by time.",
                            "Equations": [], "Diagrams": {}})
        app.session_state[HISTORY_KEY] = records
        app.session_state["show_session_progress"] = True
        with patch("utils.session_progress.progress_date", return_value=date(2026, 10, 21)):
            app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.title[0].value, "Progress for October 21, 2026")
            self.assertEqual(len(app.table), 2)
            self.assertEqual(sum(len(table.value) for table in app.table), 12)
            self.assertEqual([e.label for e in app.expander if e.label != "Functions & history"], [])
            app.radio(key="progress_view").set_value("Review answers").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.selectbox(key="progress_answer_selection").options), 180)
            app.selectbox(key="progress_activity_filter").select("Activity 1").run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.selectbox(key="progress_answer_selection").options), 15)
            self.assertEqual([e.label for e in app.expander if e.label != "Functions & history"], [])

    def test_summary_separates_types_and_preserves_old_records(self):
        history = [
            {"Activity": "Projectiles", "Problem type": "Type 1", "Result": "Correct", "Difficulty": "Easy"},
            {"Activity": "Projectiles", "Problem type": "Type 1", "Result": "Incorrect", "Difficulty": "Hard"},
            {"Activity": "Projectiles", "Problem type": "Type 2", "Result": "Correct"},
            {"Activity": "Another activity", "Problem type": "Type 1", "Result": "Correct"},
            {"Activity": "Projectiles", "Result": "Correct"},
            {"Activity": "Projectiles", "Problem type": "", "Result": "Incorrect"},
        ]
        rows = activity_summary(history)
        self.assertEqual([(r["Activity"], r["Problem type"], r["Checks"]) for r in rows], [
            ("Projectiles", "Type 1", 2), ("Projectiles", "Type 2", 1),
            ("Another activity", "Type 1", 1), ("Projectiles", "Unspecified", 2)])
        self.assertEqual(sum(r["Checks"] for r in rows), 6)
        self.assertEqual(sum(r["Correct"] for r in rows), 4)
        self.assertEqual(sum(r["Incorrect"] for r in rows), 2)
        self.assertEqual(sum(r["Stars"] for r in rows), 4)

    def test_projectile_types_are_captured_at_submission_and_grouped(self):
        app = page("Kinematics", "Projectiles")
        for kind, difficulty in [("Type 1", "Easy"), ("Type 2", "Easy"), ("Type 3", "Easy"), ("Type 1", "Medium")]:
            app.selectbox(key="projectiles_problem_type_select_unified").select(kind).run()
            app.selectbox(key="projectiles_difficulty_select_unified").select(difficulty).run()
            fields = [f for f in app.text_input if f.key.startswith("projectiles_input_")]
            self.assertTrue(fields)
            for field, answer in zip(fields, app.session_state["projectiles_correct_answers"]):
                field.set_value(str(answer))
            click(app, "Submit")
            self.assertEqual(app.session_state[HISTORY_KEY][-1]["Problem type"], kind)
        click(app, "My Current Session Progress")
        table = app.table[0].value
        self.assertEqual(table["Problem type"].tolist(), ["Type 1", "Type 2", "Type 3"])
        self.assertEqual(table["Checks"].tolist(), [2, 1, 1])
        app.radio(key="progress_view").set_value("Review answers").run()
        self.assertTrue(any("Type 3" in label for label in app.selectbox(key="progress_answer_selection").options))


if __name__ == "__main__":
    unittest.main()
