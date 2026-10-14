"""Conservation stage roles, displayed precision, and independent organizer flow."""
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
from utils.generators.energy.energy_conserv import EnergyConservationGenerator
from utils.solve_for import generate_selected, target_options
from xtrct_docs.payload_adapter import DocumentGenerator


def verify(payload):
    plan = payload["extras"]["energy_plan"]
    facts = plan["givens"]
    target = plan["target"]
    patterns = {"m": r"([\d.]+) kg", "v": r"([\d.]+) m/s", "h": r"([\d.]+) meters", "k": r"([\d.]+) N/m", "x": r"([\d.]+) meters"}
    for key, value in facts.items():
        # The two length roles can coexist; each expected fact must appear.
        numbers = [float(v) for v in re.findall(patterns[key], payload["question"])]
        assert value in numbers, (key, value, payload["question"])
    assert target not in facts
    fields = [f for group in plan["groups"] for f in group["fields"]]
    assert {f["id"]: f["value"] for f in fields} == facts
    v = dict(facts)
    v[target] = payload["answers"][0]
    assert all(math.isfinite(value) and value > 0 for value in v.values())
    if plan["family"] == "gravity_motion":
        left, right = v["m"]*10*v["h"], .5*v["m"]*v["v"]**2
    elif plan["family"] == "spring_motion":
        left, right = .5*v["k"]*v["x"]**2, .5*v["m"]*v["v"]**2
    else:
        left, right = v["m"]*10*v["h"], .5*v["k"]*v["x"]**2
    assert math.isclose(left, right, rel_tol=1e-9)
    assert len(plan["steps"]) == 1
    assert math.isclose(plan["steps"][0]["value"], left, rel_tol=1e-9)


def main():
    generator = EnergyConservationGenerator()
    branches = [("Gravitational <--> Kinetic", "kinetic_gravitational_problem", 4),
                ("Elastic <--> Kinetic", "elastic_kinetic_problem", 8),
                ("Gravitational <--> Elastic", "elastic_gravitational_problem", 8)]
    count = 0
    for kind, method, variants in branches:
        for difficulty in ("Easy", "Medium", "Hard"):
            for variant in range(variants):
                for seed in range(60):
                    random.seed(seed)
                    verify(getattr(generator, method)(difficulty, variant=variant))
                    count += 1
            for option in target_options(generator, kind, difficulty):
                verify(generate_selected(generator, kind, difficulty, option["id"]))
                verify(DocumentGenerator(generator).question(kind, difficulty, option["id"]))
            for _ in range(10):
                verify(generate_selected(generator, kind, difficulty, "mixed"))
    for difficulty in ("Easy", "Medium", "Hard"):
        seen = set()
        for seed in range(120):
            random.seed(seed)
            payload = generate_selected(generator, "Mixed", difficulty)
            verify(payload)
            plan = payload["extras"]["energy_plan"]
            seen.add((plan["family"], plan["reverse"]))
            assert payload["problem_type"] == "Mixed"
        assert len(seen) == 6
        assert not target_options(generator, "Mixed", difficulty)
        verify(DocumentGenerator(generator).question("Mixed", difficulty, "mixed"))
    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    prefix = "energy_conservation"
    app.session_state["router_section"] = "Energy"
    app.session_state["router_activity"] = "Conservation of Energy"
    app.run()
    for kind, _, _ in branches:
        app.selectbox(key=prefix + "_problem_type_select_unified").select(kind).run()
        for difficulty in ("Easy", "Medium", "Hard"):
            app.selectbox(key=prefix + "_difficulty_select_unified").select(difficulty).run()
            for target in [o["id"] for o in target_options(generator, kind, difficulty)] + ["mixed"]:
                app.selectbox(key=prefix + "_solve_for_select").select(target).run()
                assert not app.exception
                qid = app.session_state[prefix + "_question_id"]
                assert app.session_state[prefix + "_setup_submission"] is None
                plan = app.session_state[prefix + "_payload"].extras["energy_plan"]
                fields = [f for group in plan["groups"] for f in group["fields"]] + plan["steps"]
                for field in fields:
                    app.text_input(key=f"{prefix}_energy_setup_input_{qid}_{field['id']}").set_value(str(field["value"]))
                app.run()
                assert not app.success
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert not app.exception and len(app.success) == len(fields)
                assert not app.session_state[prefix + "_submitted"]
                app.text_input(key=f"{prefix}_energy_setup_input_{qid}_energy").set_value("-1").run()
                assert any("changed" in c.value for c in app.caption)
                next(b for b in app.button if b.label == "Check organized work").click().run()
                assert len(app.error) == 1
    app.selectbox(key=prefix + "_problem_type_select_unified").select("Mixed").run()
    assert not app.exception
    assert not any(s.label == "Solve for" for s in app.selectbox)
    assert app.session_state[prefix + "_problem_type"] == "Mixed"
    assert app.session_state[prefix + "_solve_for"] == "mixed"
    assert any(e.label == "Organizing help" for e in app.expander)
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
    print(f"Conservation: {count} family cases plus 360 Mixed cases, all 60 scenario/level branches, target/Mixed/export and organizer transition checks passed.")


if __name__ == "__main__":
    main()
