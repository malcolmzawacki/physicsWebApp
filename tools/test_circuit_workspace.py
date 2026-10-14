"""Reviewed circuit organizer facts, isolated checks, and question transitions."""
import logging
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.current_electricity.ohms_law_model import build_circuit_case
from utils.generators.current_electricity.series_parallel_model import build_series_parallel_case


def main():
    kinds = ("Series Current and Voltage", "Parallel Current and Voltage", "Series Voltage Drop",
             "Series Equivalent Resistance", "Parallel Equivalent Resistance", "Series Total Current", "Parallel Branch Current")
    count = 0
    for kind in kinds:
        builder = build_circuit_case if kind in kinds[:2] else build_series_parallel_case
        for difficulty in ("Easy", "Medium", "Hard"):
            for seed in range(80):
                random.seed(seed)
                case = builder(kind, difficulty)
                plan = case["organizer"]
                fields = [group["fields"][0] for group in plan["groups"]]
                supplied = [float(value.split()[0]) for _, value in case["givens"]]
                assert [field["value"] for field in fields] == supplied
                shared, r1, r2 = (None, *supplied) if "Equivalent Resistance" in kind else supplied
                assert float(case['diagram']['resistor_labels'][0].split('=')[1].split()[0]) == r1
                if kind == kinds[0]:
                    assert case["answers"] == [shared * r1, shared * r2]
                elif kind == kinds[1]:
                    assert case["answers"] == [shared / r1, shared / r2]
                elif kind == "Series Voltage Drop":
                    steps = plan["steps"]
                    assert steps[0]["value"] == r1 + r2
                    assert math.isclose(steps[1]["value"], shared / (r1 + r2))
                elif kind == "Series Total Current":
                    assert plan["steps"][0]["value"] == r1 + r2
                    assert math.isclose(case["answer"], shared / (r1 + r2))
                elif kind == "Series Equivalent Resistance":
                    assert case["answer"] == r1 + r2
                elif kind == "Parallel Equivalent Resistance":
                    assert math.isclose(case["answer"], r1 * r2 / (r1 + r2))
                else:
                    resistance = r1 if case["answer_label"].endswith("R1") else r2
                    assert math.isclose(case["answer"], shared / resistance)
                assert len(plan["steps"]) == (2 if kind == kinds[2] else 1 if kind == "Series Total Current" else 0)
                count += 1
    for route, prefix, selector, activities in (
        ("Circuit Fundamentals", "current_electricity", "fundamentals_practice_select", kinds[:2]),
        ("Series and Parallel Circuits", "current_electricity_series_parallel", "problem_type_select", kinds[2:]),
    ):
        app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
        app.session_state["router_section"] = "⚡Electricity⚡"
        app.session_state["router_group"] = "Current Electricity"
        app.session_state["router_activity"] = route
        app.run()
        for kind in activities:
            app.selectbox(key=f"{prefix}_{selector}").select(kind).run()
            for difficulty in ("Easy", "Medium", "Hard"):
                app.selectbox(key=f"{prefix}_difficulty_select").select(difficulty).run()
                assert not app.exception
                assert not any(message.value == app.session_state[prefix + "_case"].get("relationship") for message in app.info)
                case = app.session_state[prefix + "_case"]
                plan = case["organizer"]
                qid = app.session_state[prefix + "_question_number"]
                assert app.session_state[prefix + "_circuit_setup_submission"] is None
                fields = [field for group in plan["groups"] for field in group["fields"]] + plan["steps"]
                attempts = app.session_state[prefix + "_attempt_count"]
                for field in fields:
                    app.text_input(key=f"{prefix}_circuit_setup_input_{qid}_{field['id']}").set_value(str(field["value"]))
                app.run()
                assert not app.success
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert not app.exception and len(app.success) == len(fields)
                assert app.session_state[prefix + "_attempt_count"] == attempts
                assert not app.session_state[prefix + "_submitted"]
                app.text_input(key=f"{prefix}_circuit_setup_input_{qid}_R1").set_value("-100").run()
                assert any("Changed" in c.value for c in app.caption)
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert len(app.error) == 1
                next(b for b in app.button if b.label == "New Question (Circuit)").click().run()
                assert not app.exception
                assert app.session_state[prefix + "_circuit_setup_submission"] is None
                assert all(i.value == "" for i in app.text_input if "circuit_setup" in i.key)
        if route == "Series and Parallel Circuits":
            case = dict(app.session_state[prefix + "_case"])
            case.pop("organizer")
            app.session_state[prefix + "_case"] = case
            qid = app.session_state[prefix + "_question_number"]
            app.run()
            assert not app.exception and any(e.label == "Organizing help" for e in app.expander)
            assert app.session_state[prefix + "_question_number"] == qid
            assert len([i for i in app.text_input if "circuit_setup_input" in i.key]) == 3
            app.selectbox(key=f"{prefix}_{selector}").select("Series Equivalent Resistance").run()
            assert not app.exception and any(e.label == "Organizing help" for e in app.expander)
    print(f"Circuit organizers: {count} displayed-value cases and all 21 routed type/difficulty branches passed; checks, feedback, isolation, resets, and live-session recovery passed.")


if __name__ == "__main__":
    main()
