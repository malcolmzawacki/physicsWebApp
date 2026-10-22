"""Projectile axis organization, displayed facts, crossings, and form lifecycle."""
import logging
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from streamlit.testing.v1 import AppTest
from utils.generators.kinematics.projectile_generator import ProjectileGenerator
from utils.solve_for import target_options, generate_selected
from xtrct_docs.payload_adapter import DocumentGenerator


def verify(payload):
    p = payload["extras"]["projectile_plan"]
    diagram = payload["diagram_data"]
    assert diagram["givens"] == p["givens"]
    assert set(diagram) == {"scene", "givens", "launch_behind_edge"}
    assert not set(p["targets"]) & diagram["givens"].keys()
    v = p["values"]
    assert math.isclose(v["dy"], v["vyi"]*v["t"]-5*v["t"]**2, abs_tol=1e-6)
    assert math.isclose(v["vyf"], v["vyi"]-10*v["t"], abs_tol=1e-8)
    assert v["t"] > 0 and v["vx"] > 0
    assert math.isclose(v["vf"], math.hypot(v["vx"],v["vyf"]))
    assert payload["answers"] == [v[k] for k in p["targets"]]
    assert not set(p["targets"]) & p["givens"].keys()
    assert p["targets"][-1] not in [f["id"] for f in p["steps"]]
    for f in p["fields"]:
        assert str(f["value"]) in payload["question"] or f'{f["value"]:.2f}' in payload["question"]
    if p["kind"] == 2:
        assert v["dy"] == 0
        assert math.isclose(v["t"], 2*v["tpeak"])
    if p["kind"] == 3:
        assert v["vyf"] < 0
        if "tfirst" in p["givens"]:
            first = p["givens"]["tfirst"]
            assert math.isclose(v["vyi"]*first-5*first**2, p["givens"]["h"])
            assert first < v["tpeak"] < v["t"]
        if "back" in p["targets"]:
            assert v["back"] >= -.01


def main():
    g = ProjectileGenerator()
    count = 0
    for level in ("Easy", "Medium", "Hard"):
        for kind in g.stored_metadata():
            for option in target_options(g, kind, level) + [{"id": "mixed"}]:
                for seed in range(60):
                    random.seed(seed)
                    verify(generate_selected(g,kind,level,option["id"]))
                    count += 1
                verify(DocumentGenerator(g).question(kind,level,option["id"]))
    app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=25)
    app.session_state["router_section"] = "Kinematics"
    app.session_state["router_activity"] = "Projectiles"
    app.run()
    assert not app.exception
    assert any(e.label == "Diagram" and not e.proto.expanded for e in app.expander)
    prefix = "projectiles"
    for kind in g.stored_metadata():
        app.selectbox(key=prefix+"_problem_type_select_unified").select(kind).run()
        for level in ("Easy", "Medium", "Hard"):
            app.selectbox(key=prefix+"_difficulty_select_unified").select(level).run()
            assert not app.exception
            qid = app.session_state[prefix+"_question_id"]
            p = app.session_state[prefix+"_payload"].extras["projectile_plan"]
            fields = p["fields"]+p["steps"]
            for f in fields:
                app.text_input(key=f'{prefix}_projectile_setup_input_{qid}_{f["id"]}').set_value(str(f["value"]))
            # Form edits are sent by the submit button, without an intervening rerun.
            assert not app.success
            next(b for b in app.button if b.label=="Check organized work").click().run()
            assert not app.exception and len(app.success)==len(fields)
            assert not app.session_state[prefix+"_submitted"]
            # Model an external rerun with a changed saved form value.
            app.session_state[f'{prefix}_projectile_setup_input_{qid}_{fields[0]["id"]}'] = "999999"
            app.run()
            assert any("changed" in c.value for c in app.caption)
            next(b for b in app.button if b.label=="Check organized work").click().run()
            assert len(app.error)==1
    qid = app.session_state[prefix+"_question_id"]
    app.session_state[f"{prefix}_cancel_next_{qid}"] = True
    answer_inputs = [i for i in app.text_input if "setup_input" not in i.key]
    for widget, answer in zip(answer_inputs, app.session_state[prefix+"_correct_answers"]):
        widget.set_value(str(answer))
    next(b for b in app.button if b.label=="Submit").click().run()
    assert not app.exception and app.session_state[prefix+"_submitted"]
    stars = app.session_state[prefix+"_stars"]
    assert stars > 0
    app.run()
    assert app.session_state[prefix+"_stars"] == stars
    next(b for b in app.button if b.label=="New Question").click().run()
    assert app.session_state[prefix+"_setup_submission"] is None
    print(f"Projectiles: {count} sampled target cases, exports, axis form checks, stale feedback and resets passed.")


if __name__ == "__main__":
    main()
