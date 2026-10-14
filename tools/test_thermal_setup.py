"""Thermal organizer: displayed facts, positive losses, stage balance, and UI flow."""
import logging
import math
import random
import re
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.energy.thermal_loss import ThermalLossGenerator
from utils.thermal_organizer import STATES
from utils.solve_for import target_options, generate_selected
from xtrct_docs.payload_adapter import DocumentGenerator

METHODS = [("grav_to_kin", 3), ("kin_to_grav", 3), ("grav_to_elastic", 5),
           ("elastic_to_grav", 5), ("kinetic_to_elastic", 5), ("elastic_to_kinetic", 5)]


def verify(payload):
    plan = payload["extras"]["energy_plan"]
    facts = plan["givens"]
    patterns = {"m": r"([\d.]+) kg", "v": r"([\d.]+) m/s", "h": r"([\d.]+) meter", "x": r"([\d.]+) meter", "k": r"([\d.]+) N/m", "T": r"([\d.]+) Joules"}
    for key, value in facts.items():
        assert value in [float(v) for v in re.findall(patterns[key], payload["question"])], (key, value, payload["question"])
    assert plan["target"] not in facts
    v = {**facts, plan["target"]: payload["answers"][0]}
    assert all(math.isfinite(value) and value > 0 for value in v.values())
    def energy(kind):
        return v["m"]*10*v["h"] if kind == "gravity" else .5*v["m"]*v["v"]**2 if kind == "kinetic" else .5*v["k"]*v["x"]**2
    initial, final, *_ = STATES[plan["direction"]]
    ei, ef = energy(initial), energy(final)
    assert math.isclose(ei - ef, v["T"], rel_tol=1e-8, abs_tol=1e-8)
    assert [s["id"] for s in plan["steps"]] == ["Ei", "Ef"]
    assert math.isclose(plan["steps"][0]["value"], ei)
    assert math.isclose(plan["steps"][1]["value"], ef)
    assert {f["id"]: f["value"] for group in plan["groups"] for f in group["fields"]} == facts
    if plan["target"] == "T":
        assert payload["units"] == ["Thermal energy (J)"]
    assert "no energy loss" not in plan["given_help"]


def main():
    generator = ThermalLossGenerator()
    with patch.object(generator, "grav_to_kin_thermal_nums", side_effect=[(1, 1, 5, 1), (1, 1, 4, 2)]) as sampler:
        retried = generator.grav_to_kin_thermal_q("Hard", variant=0)
        assert sampler.call_count == 2
        assert retried["answers"] == [2]
        assert retried["extras"]["energy_plan"]["target"] == "T"
    count = 0
    for direction, variants in METHODS:
        for difficulty in ("Easy", "Medium", "Hard"):
            for variant in range(1 if difficulty == "Easy" else variants):
                for seed in range(60):
                    random.seed(seed)
                    verify(getattr(generator, direction + "_thermal_q")(difficulty, variant=variant))
                    count += 1
    for kind in generator.stored_metadata():
        for difficulty in ("Easy", "Medium", "Hard"):
            for option in target_options(generator, kind, difficulty):
                verify(generate_selected(generator, kind, difficulty, option["id"]))
                verify(DocumentGenerator(generator).question(kind, difficulty, option["id"]))
    for difficulty in ("Easy", "Medium", "Hard"):
        seen = set()
        for seed in range(120):
            random.seed(seed)
            result = generate_selected(generator, "Mixed", difficulty)
            verify(result)
            seen.add(result["extras"]["energy_plan"]["direction"])
        assert len(seen) == 6
        verify(DocumentGenerator(generator).question("Mixed", difficulty, "mixed"))
    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    app.session_state["router_section"] = "Energy"
    app.session_state["router_activity"] = "Thermal Energy"
    app.run()
    prefix = "thermal"
    for kind in generator.stored_metadata():
        app.selectbox(key=prefix + "_problem_type_select_unified").select(kind).run()
        for difficulty in ("Easy", "Medium", "Hard"):
            app.selectbox(key=prefix + "_difficulty_select_unified").select(difficulty).run()
            for target in [o["id"] for o in target_options(generator, kind, difficulty)] + ["mixed"]:
                if kind == "Mixed":
                    assert not any(s.label == "Solve for" for s in app.selectbox)
                else:
                    app.selectbox(key=prefix + "_solve_for_select").select(target).run()
                assert not app.exception
                qid = app.session_state[prefix + "_question_id"]
                plan = app.session_state[prefix + "_payload"].extras["energy_plan"]
                assert app.session_state[prefix + "_setup_submission"] is None
                fields = [f for group in plan["groups"] for f in group["fields"]] + plan["steps"]
                for field in fields:
                    app.text_input(key=f"{prefix}_energy_setup_input_{qid}_{field['id']}").set_value(str(field["value"]))
                app.run()
                assert not app.success
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert not app.exception and len(app.success) == len(fields)
                assert not app.session_state[prefix + "_submitted"]
                app.text_input(key=f"{prefix}_energy_setup_input_{qid}_Ei").set_value("-1").run()
                assert any("changed" in c.value for c in app.caption)
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert len(app.error) == 1
    qid = app.session_state[prefix + "_question_id"]
    app.session_state[f"{prefix}_cancel_next_{qid}"] = True
    next(i for i in app.text_input if "setup_input" not in i.key).set_value(str(app.session_state[prefix + "_correct_answers"][0]))
    next(b for b in app.button if b.label == "Submit").click().run()
    assert not app.exception and app.success
    stars = app.session_state[prefix + "_stars"]
    assert stars > 0
    app.run()
    assert app.session_state[prefix + "_stars"] == stars
    next(b for b in app.button if b.label == "New Question").click().run()
    assert app.session_state[prefix + "_setup_submission"] is None
    print(f"Thermal: {count} displayed-fact cases, all 58 direction/target/level branches, explicit/Mixed exports, isolated checks, feedback, resets, and scoring passed.")


if __name__ == "__main__":
    main()
