"""Friction/distance: displayed facts, multi-answer targets, balances and page flow."""
import logging
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.energy.frict_and_dist import ThermalWithFrictionGenerator
from utils.thermal_organizer import STATES
from utils.solve_for import generate_selected, target_options
from xtrct_docs.payload_adapter import DocumentGenerator

BRANCHES = [
    ("grav_to_kinetic", ["v", "h", "m"], ["v", "h", "m", "d", "F"]),
    ("kinetic_to_grav", ["v", "h", "m"], ["v", "h", "m", "d", "F"]),
    ("grav_to_elastic", ["x", "k", "h", "m"], ["x", "k", "m", "d", "h", "F"]),
    ("elastic_to_grav", ["h", "x", "k", "m"], ["h", "x", "m", "d", "k", "F"]),
    ("kinetic_to_elastic", ["x", "k", "v", "m"], ["x", "k", "m", "d", "v", "F"]),
    ("elastic_to_kinetic", ["v", "x", "k", "m"], ["v", "x", "m", "d", "k", "F"]),
]


def verify(result, targets=None):
    plan = result["extras"]["energy_plan"]
    if targets is not None:
        assert plan["targets"] == targets, (plan["direction"], plan["targets"], targets, result["units"])
    given = plan["givens"]
    patterns = {"m": r"([\d.]+) kg", "v": r"([\d.]+) m/s", "h": r"([\d.]+) meter", "x": r"([\d.]+) (?:m\b|meter)", "k": r"([\d.]+) N/m", "F": r"([\d.]+) N(?!/)", "d": r"([\d.]+) (?:m\b|meter)"}
    for key, value in given.items():
        assert value in [float(n) for n in re.findall(patterns[key], result["question"])], (key, value, result["question"])
    assert "T" not in given
    assert not set(plan["targets"]) & set(given)
    assert plan["targets"][-1] not in [s["id"] for s in plan["steps"]]
    values = {**given, **dict(zip(plan["targets"], result["answers"]))}
    thermal = next(s["value"] for s in plan["steps"] if s["id"] == "T")
    assert all(math.isfinite(v) and v > 0 for v in values.values())
    assert math.isclose(thermal, values["F"] * values["d"], rel_tol=1e-9)
    initial, final, *_ = STATES[plan["direction"]]
    def energy(kind):
        return values["m"]*10*values["h"] if kind == "gravity" else .5*values["m"]*values["v"]**2 if kind == "kinetic" else .5*values["k"]*values["x"]**2
    ei, ef = energy(initial), energy(final)
    assert math.isclose(ei - ef, thermal, rel_tol=1e-8, abs_tol=1e-8)
    if "h" in values:
        assert values["d"] >= values["h"]
    for key, expected in (("Ei", ei), ("Ef", ef)):
        assert math.isclose(next(s["value"] for s in plan["steps"] if s["id"] == key), expected)


def main():
    generator = ThermalWithFrictionGenerator()
    count = 0
    for method, easy, advanced in BRANCHES:
        for difficulty in ("Easy", "Medium", "Hard"):
            for variant, target in enumerate(easy if difficulty == "Easy" else advanced):
                for seed in range(40):
                    random.seed(seed)
                    result = getattr(generator, method + "_friction_distance_q")(difficulty, variant=variant)
                    verify(result, ["T", target] if difficulty == "Easy" else [target])
                    count += 1
    for kind in generator.stored_metadata():
        for difficulty in ("Easy", "Medium", "Hard"):
            for option in target_options(generator, kind, difficulty):
                verify(generate_selected(generator, kind, difficulty, option["id"]))
                verify(DocumentGenerator(generator).question(kind, difficulty, option["id"]))
    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    app.session_state["router_section"] = "Energy"
    app.session_state["router_activity"] = "Friction and Distance"
    app.run()
    prefix = "frict_dist"
    for kind in generator.stored_metadata():
        app.selectbox(key=prefix + "_problem_type_select_unified").select(kind).run()
        for difficulty in ("Easy", "Medium", "Hard"):
            app.selectbox(key=prefix + "_difficulty_select_unified").select(difficulty).run()
            for target in [o["id"] for o in target_options(generator, kind, difficulty)] + ["mixed"]:
                app.selectbox(key=prefix + "_solve_for_select").select(target).run()
                assert not app.exception
                qid = app.session_state[prefix + "_question_id"]
                plan = app.session_state[prefix + "_payload"].extras["energy_plan"]
                assert app.session_state[prefix + "_setup_submission"] is None
                fields = [f for group in plan["groups"] for f in group["fields"]] + plan["steps"]
                for field in fields:
                    app.text_input(key=f"{prefix}_energy_setup_input_{qid}_{field['id']}").set_value(str(field["value"]))
                # Form edits are sent by the submit button, without an intervening rerun.
                assert not app.success
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert not app.exception and len(app.success) == len(fields)
                assert not app.session_state[prefix + "_submitted"]
                # Model an external rerun with a changed saved form value.
                app.session_state[f"{prefix}_energy_setup_input_{qid}_T"] = "-1"
                app.run()
                assert any("changed" in c.value for c in app.caption)
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert len(app.error) == 1
    qid = app.session_state[prefix + "_question_id"]
    app.session_state[f"{prefix}_cancel_next_{qid}"] = True
    for widget, answer in zip([i for i in app.text_input if "setup_input" not in i.key], app.session_state[prefix + "_correct_answers"]):
        widget.set_value(str(answer))
    next(b for b in app.button if b.label == "Submit").click().run()
    assert not app.exception and app.success
    stars = app.session_state[prefix + "_stars"]
    app.run()
    assert stars > 0 and app.session_state[prefix + "_stars"] == stars
    next(b for b in app.button if b.label == "New Question").click().run()
    assert app.session_state[prefix + "_setup_submission"] is None
    print(f"Friction/Distance: {count} displayed-fact cases and all 90 direction/target/level branches; exports, independent checks, feedback, resets, and final scoring passed.")


if __name__ == "__main__":
    main()
