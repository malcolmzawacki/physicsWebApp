"""Energy Basics: displayed physics, all finite sampling branches, and organizer flow."""
import logging
import math
import random
import re
import sys
from itertools import product
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.energy.energy_basics import EnergyBasicsGenerator
from utils.problem_payload import payload_from_dict
from utils.quantities import PROFILES
from utils.setup_schema import expected_entries
from utils.setup_feedback import evaluate_entry
from utils.solve_for import generate_selected, target_options
from xtrct_docs.payload_adapter import DocumentGenerator

FAMILIES = {
    "Elastic Potential Energy": ("elastic_energy", ("E", "x", "k"), {"E": "J", "k": "N/m", "x": "m"}),
    "Kinetic Energy": ("kinetic_energy", ("E", "v", "m"), {"E": "J", "m": "kg", "v": "m/s"}),
    "Gravitational Potential Energy": ("gravitational_energy", ("E", "h", "m"), {"E": "J", "m": "kg", "g": "m/s^2", "h": "m"}),
    "Work": ("work", ("W", "d", "F"), {"W": "J", "F": "N", "d": "m"}),
}


def check_payload(raw, family, target):
    payload = payload_from_dict(raw)
    profile, _, units = FAMILIES[family]
    setup = payload.extras["setup"]
    assert setup["profile"] == profile and setup["target_roles"] == [target]
    facts = {}
    for key, unit in units.items():
        match = re.search(r"(\d+\.\d+) " + re.escape(unit) + r"(?=[ .,]|$)", payload.question)
        if key == target:
            assert match is None and "value" not in setup["fields"][key]
        else:
            assert match, (key, payload.question)
            facts[key] = float(match.group(1))
    assert expected_entries(setup) == {key: "?" if key == target else facts[key] for key in units}
    if family == "Kinetic Energy":
        result = .5 * facts["m"] * facts["v"]**2 if target == "E" else math.sqrt(2 * facts["E"] / facts["m"]) if target == "v" else 2 * facts["E"] / facts["v"]**2
    elif family == "Elastic Potential Energy":
        result = .5 * facts["k"] * facts["x"]**2 if target == "E" else math.sqrt(2 * facts["E"] / facts["k"]) if target == "x" else 2 * facts["E"] / facts["x"]**2
        assert "relaxed length" in payload.question
    elif family == "Gravitational Potential Energy":
        result = facts["m"] * facts["g"] * facts["h"] if target == "E" else facts["E"] / (facts["m"] * facts["g"]) if target == "h" else facts["E"] / (facts["g"] * facts["h"])
        assert facts["g"] == 10 and "zero at ground level" in payload.question
    else:
        result = facts["F"] * facts["d"] if target == "W" else facts["W"] / facts["F"] if target == "d" else facts["W"] / facts["d"]
        assert "constant" in payload.question.lower() and "across flat ground" in payload.question
    assert math.isclose(payload.answers[0], result, abs_tol=1e-9)


def main():
    generator = EnergyBasicsGenerator()
    count = 0
    for difficulty, upper in (("Easy", 5), ("Medium", 10), ("Hard", 20)):
        for family, (profile, targets, _) in FAMILIES.items():
            options = target_options(generator, family, difficulty)
            assert len(options) == (1 if difficulty == "Easy" else 3)
            for variant, option in enumerate(options):
                first = range(2, upper + 1) if family == "Elastic Potential Energy" else range(1, upper + 1)
                for one, two in product(first, range(1, upper + 1)):
                    flips = (0, 1) if family in ("Elastic Potential Energy", "Kinetic Energy") else (None,)
                    for flip in flips:
                        directions = (0, 1) if family == "Elastic Potential Energy" else (None,)
                        for direction in directions:
                            samples = [one, two] + ([] if flip is None else [flip]) + ([] if direction is None else [direction])
                            with patch("utils.generators.energy.energy_basics.ri", side_effect=samples):
                                raw = generate_selected(generator, family, difficulty, option["id"])
                            check_payload(raw, family, targets[variant])
                            count += 1
                exported = DocumentGenerator(generator).question(family, difficulty, option["id"])
                check_payload(exported, family, targets[variant])
            seen = set()
            for seed in range(60):
                random.seed(seed)
                raw = generate_selected(generator, family, difficulty, "mixed")
                target = raw["extras"]["setup"]["target_roles"][0]
                seen.add(target)
                check_payload(raw, family, target)
            assert seen == set(targets[:1] if difficulty == "Easy" else targets)
    assert count == 11820, count
    roles = PROFILES["gravitational_energy"]
    assert evaluate_entry("10", "m", {"E": "?", "m": 10, "g": 10, "h": 2}, roles).status == "correct"
    feedback = evaluate_entry("10", "h", {"E": "?", "m": 3, "g": 10, "h": 2}, roles)
    assert feedback.code == "matches_other_given" and "start or the end" not in feedback.message

    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    app.session_state["router_section"] = "Energy"
    app.session_state["router_activity"] = "Types of Energy"
    app.run()
    prefix = "energy_basics"
    for family, (profile, _, _) in FAMILIES.items():
        app.selectbox(key=prefix + "_problem_type_select_unified").select(family).run()
        for difficulty in ("Easy", "Medium", "Hard"):
            app.selectbox(key=prefix + "_difficulty_select_unified").select(difficulty).run()
            ids = [o["id"] for o in target_options(generator, family, difficulty)] + ["mixed"] if difficulty != "Easy" else [None]
            for target_id in ids:
                if target_id is not None:
                    app.selectbox(key=prefix + "_solve_for_select").select(target_id).run()
                assert not app.exception
                qid = app.session_state[prefix + "_question_id"]
                assert app.session_state[prefix + "_setup_submission"] is None
                assert not any(app.session_state[prefix + "_setup_draft"].values())
                expected = expected_entries(app.session_state[prefix + "_payload"].extras["setup"])
                assert [i.label for i in app.text_input if "setup_input" in i.key] == [role.name for role in PROFILES[profile].values()]
                forms = [n.proto.form for n in app.get("form")]
                form = next(f for f in forms if f.form_id == f"{prefix}_setup_form_{qid}")
                assert form.enter_to_submit and not form.clear_on_submit
                assert any(f.form_id == prefix + "_form" for f in forms)
                for key, value in expected.items():
                    app.text_input(key=f"{prefix}_setup_input_{qid}_{key}").set_value(str(value))
                app.run()
                assert not app.success
                next(b for b in app.button if b.label == "Check setup").click().run()
                assert len(app.success) == len(expected) and not app.session_state[prefix + "_submitted"]
                assert app.session_state[prefix + "_question_id"] == qid
                requested = next(k for k, v in expected.items() if v == "?")
                given = next(v for v in expected.values() if v != "?")
                app.text_input(key=f"{prefix}_setup_input_{qid}_{requested}").set_value(str(given)).run()
                assert any("changed" in c.value for c in app.caption)
                next(b for b in app.button if b.label == "Check setup").click().run()
                assert len(app.error) == 1
                assert any("matches another given" in m.value for m in app.markdown)
    next(b for b in app.button if b.label == "New Question").click().run()
    assert app.session_state[prefix + "_setup_submission"] is None
    assert not any(app.session_state[prefix + "_setup_draft"].values())
    qid = app.session_state[prefix + "_question_id"]
    app.session_state[f"{prefix}_cancel_next_{qid}"] = True
    next(i for i in app.text_input if "setup_input" not in i.key).set_value(str(app.session_state[prefix + "_correct_answers"][0]))
    next(b for b in app.button if b.label == "Submit").click().run()
    assert not app.exception and app.success
    earned_stars = app.session_state[prefix + "_stars"]
    assert earned_stars > 0
    app.run()
    assert app.session_state[prefix + "_stars"] == earned_stars
    app.checkbox(key=f"{prefix}_cancel_next_{qid}").uncheck().run()
    assert app.session_state[prefix + "_question_id"] == qid + 1
    print(f"Energy Basics: {count} sampled-value combinations, 28 target/level branches, Mixed, forms, feedback, progression, and export payloads passed.")


if __name__ == "__main__":
    main()
