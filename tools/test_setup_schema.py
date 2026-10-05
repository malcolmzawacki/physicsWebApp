"""Architecture contract, target bindings, and a second-profile rendering check."""
import sys
from pathlib import Path
from copy import deepcopy
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.setup_schema import make_setup, validate_setup, expected_entries
from utils.quantities import equation
from utils.problem_payload import payload_from_dict, ProblemPayloadError
from utils.generators.kinematics.const_motion_generator import ConstantMotionGenerator
from utils.generators.kinematics.linear_motion_generator import LinearMotionGenerator
from utils.solve_for import generate_selected, target_options
from streamlit.testing.v1 import AppTest


def main():
    for generator, families in [(ConstantMotionGenerator(), ["Constant Speed"]),
                                (LinearMotionGenerator(), ["No Time", "No Distance", "No Acceleration", "No Final Velocity"])]:
        for family in families:
            for difficulty in ("Easy", "Medium", "Hard"):
                for target in target_options(generator, family, difficulty):
                    payload = payload_from_dict(generate_selected(generator, family, difficulty, target["id"]))
                    setup = payload.extras["setup"]
                    assert setup["target_roles"]
                    assert len([v for v in expected_entries(setup).values() if v == "?"]) == 1
    for _ in range(15):
        payload = payload_from_dict(generate_selected(LinearMotionGenerator(), "Mixed", "Easy"))
        assert payload.extras["requested_target_id"] == "mixed"
        assert len(payload.extras["setup"]["target_roles"]) == 1
    base = make_setup("constant_speed", {"d": 12, "t": 3, "v": 4}, ["t", "v"], ["d"])
    assert "value" not in base["fields"]["d"]
    invalid = []
    case=deepcopy(base); case["fields"]["d"]["value"]=12; invalid.append(case)
    case=deepcopy(base); case["fields"]["t"]["value"]=float("nan"); invalid.append(case)
    case=deepcopy(base); case["fields"]["t"]["status"]="implied"; invalid.append(case)
    case=deepcopy(base); case["target_roles"]=["v"]; invalid.append(case)
    case=deepcopy(base); case["profile"]="unknown"; invalid.append(case)
    case=deepcopy(base); del case["fields"]["v"]; invalid.append(case)
    for setup in invalid:
        try:
            payload_from_dict({"question":"Example", "answers":[12], "units":["m"], "extras":{"setup":setup}})
        except ProblemPayloadError:
            pass
        else:
            raise AssertionError("Invalid setup accepted")
    assert equation("linear_motion", "${vf} = ${vi} + ${a}${t}") == "v_f = v_i + at"
    assert equation("constant_speed", "${d} = ${v}${t}") == "d = vt"
    at=AppTest.from_string('''
from utils.setup_workspace import render_setup_workspace
from utils.ui_state import State
from utils.problem_payload import payload_from_dict
from utils.generators.kinematics.const_motion_generator import ConstantMotionGenerator
state=State("three")
state.ensure("question_id", 1)
state.ensure_lazy("payload", lambda: payload_from_dict(ConstantMotionGenerator().inst_speed_question("Distance")))
render_setup_workspace(state)
''').run()
    assert not at.exception
    assert [i.label for i in at.text_input] == ["Distance", "Time", "Speed"]
    print("Setup schema, explicit/mixed targets, invalid metadata, equations, and three-field rendering passed.")

if __name__ == "__main__":
    main()
