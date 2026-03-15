from __future__ import annotations

import ast
import importlib.util
import math
import random
import sys
import types
from pathlib import Path
from typing import Callable

# Ensure project-root imports work when running the script directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _install_streamlit_stub_if_missing() -> None:
    if importlib.util.find_spec("streamlit") is not None:
        return

    stub = types.ModuleType("streamlit")

    def _noop(*args, **kwargs):
        return None

    stub.session_state = {}
    stub.pyplot = _noop
    stub.write = _noop
    stub.markdown = _noop
    stub.warning = _noop
    stub.error = _noop
    stub.info = _noop
    stub.success = _noop
    stub.caption = _noop
    stub.subheader = _noop
    stub.header = _noop
    stub.title = _noop
    stub.expander = _noop
    stub.button = _noop
    stub.columns = lambda *args, **kwargs: []
    stub.container = _noop
    stub.empty = _noop
    stub.stop = _noop
    stub.rerun = _noop
    stub.experimental_rerun = _noop
    stub.__getattr__ = lambda _name: _noop
    sys.modules["streamlit"] = stub


_install_streamlit_stub_if_missing()

from utils.problem_payload import payload_from_dict
from utils.generators.force_generator import ForceGenerator
from utils.generators.forces.atwood_generator import AtwoodGenerator
from utils.generators.forces.incline_generator import InclineGenerator
from utils.generators.kinematics.projectile_generator import ProjectileGenerator
from utils.generators.kinematics.linear_motion_generator import LinearMotionGenerator
from utils.generators.kinematics.motion_graph_generator import MotionGraphGenerator
from utils.generators.momentum_generators.collision_generator import CollisionGenerator
from utils.generators.waves_generator import WaveGenerator


FailureList = list[str]


def _record_failure(failures: FailureList, context: str, error: Exception | str) -> None:
    failures.append(f"{context}: {error}")


def _assert_question_contains(question: str, required_tokens: list[str], context: str) -> None:
    text = question.lower()
    for token in required_tokens:
        if token.lower() not in text:
            raise AssertionError(
                f"{context} expected token '{token}' in question, got: {question}"
            )


def _validate_payload_dict(payload: dict, context: str) -> None:
    normalized = payload_from_dict(payload)
    if len(normalized.answers) != len(normalized.units):
        raise AssertionError(f"{context} answers/units length mismatch")


def _assert_finite_answers(payload: dict, context: str) -> None:
    answers = payload.get("answers", [])
    for idx, answer in enumerate(answers):
        if isinstance(answer, bool):
            continue
        if isinstance(answer, (int, float)) and not math.isfinite(float(answer)):
            raise AssertionError(f"{context} non-finite answer at index {idx}: {answer}")


def _assert_question_intent_matches_units(payload: dict, context: str) -> None:
    question = str(payload.get("question", "")).lower()
    units = [str(unit).lower() for unit in payload.get("units", [])]

    for unit in units:
        checks: list[list[str]] = []
        if "angle" in unit:
            checks.append(["angle"])
        if "height" in unit:
            checks.append(["height", "high"])
        if "distance" in unit:
            checks.append(["distance", "away", "far"])
        if "velocity" in unit:
            checks.append(["velocity", "speed", "fast"])
        if "acceleration" in unit:
            checks.append(["acceleration"])
        if "net force" in unit:
            checks.append(["net force"])
        if "coefficient" in unit:
            checks.append(["coefficient", "friction"])
        if "frequency" in unit:
            checks.append(["frequency", "hertz", "hz"])
        if "wavelength" in unit:
            checks.append(["wavelength"])

        for token_options in checks:
            if not any(token in question for token in token_options):
                joined = " / ".join(token_options)
                raise AssertionError(
                    f"{context} expected question to mention {joined} for unit '{unit}'"
                )


def _close_figures() -> None:
    try:
        import matplotlib.pyplot as plt

        plt.close("all")
    except Exception:
        pass


def _assert_payload_rejected(payload: dict, context: str) -> None:
    try:
        payload_from_dict(payload)
    except Exception:
        return
    raise AssertionError(f"{context} synthetic regression unexpectedly passed validation")


def check_explicit_solve_for_paths() -> FailureList:
    failures: FailureList = []

    atwood = AtwoodGenerator()
    incline = InclineGenerator()
    linear = LinearMotionGenerator()

    checks: list[tuple[str, Callable[[], dict], list[str]]] = [
        (
            "Atwood.frictionless_half_atwood(acceleration)",
            lambda: atwood.frictionless_half_atwood(solve_for="acceleration"),
            ["acceleration"],
        ),
        (
            "Atwood.frictionless_half_atwood(tension)",
            lambda: atwood.frictionless_half_atwood(solve_for="tension"),
            ["tension"],
        ),
        (
            "Incline.kinetic_friction_incline(coeff)",
            lambda: incline.kinetic_friction_incline(solve_for="coeff"),
            ["coefficient"],
        ),
        (
            "Linear.no_time_question(vf)",
            lambda: linear.no_time_question("Medium", solve_for="vf"),
            ["final velocity"],
        ),
        (
            "Linear.no_dist_question(a)",
            lambda: linear.no_dist_question("Medium", solve_for="a"),
            ["acceleration"],
        ),
    ]

    for context, factory, required_tokens in checks:
        try:
            payload = factory()
            _validate_payload_dict(payload, context)
            _assert_question_contains(payload["question"], required_tokens, context)
        except Exception as e:
            _record_failure(failures, context, e)

    return failures


def check_seeded_generator_regressions() -> FailureList:
    failures: FailureList = []

    force = ForceGenerator()
    projectile = ProjectileGenerator()
    collision = CollisionGenerator()
    wave = WaveGenerator()
    graph = MotionGraphGenerator()

    def run_seeded(
        context: str,
        factory: Callable[[], dict],
        required_tokens: list[str] | None = None,
    ) -> None:
        payload = factory()
        _validate_payload_dict(payload, context)
        _assert_finite_answers(payload, context)
        _assert_question_intent_matches_units(payload, context)
        if required_tokens:
            _assert_question_contains(payload["question"], required_tokens, context)

    checks: list[tuple[str, int, Callable[[], dict], list[str] | None]] = [
        (
            "Force.NewtonsSecondLaw(Hard)",
            101,
            lambda: force.choose_problem_dict("Newton's Second Law", "Hard"),
            ["net force"],
        ),
        (
            "Projectile.Type1(v_f and theta)",
            202,
            lambda: projectile._generate_type1_question("Hard", solve_for="v_f and theta"),
            ["speed", "angle"],
        ),
        (
            "Projectile.Type2(v_i and x)",
            203,
            lambda: projectile._generate_type2_question("Hard", solve_for="v_i and x"),
            ["initial speed"],
        ),
        (
            "Collision.Elastic(Hard)",
            301,
            lambda: collision.choose_problem_dict("Elastic Collision", "Hard"),
            ["how fast"],
        ),
        (
            "Collision.Inelastic(Hard)",
            302,
            lambda: collision.choose_problem_dict("Inelastic Collision", "Hard"),
            ["moving together"],
        ),
        (
            "Wave.deciBelScale(Hard)",
            401,
            lambda: wave.choose_problem_dict("deciBel Scale", "Hard"),
            None,
        ),
        (
            "Wave.StringHarmonics(Hard)",
            402,
            lambda: wave.choose_problem_dict("String Harmonics", "Hard"),
            None,
        ),
    ]

    graph_expectations = {
        "linear_positive": ("Positive", "Constant Velocity"),
        "linear_negative": ("Negative", "Constant Velocity"),
        "accelerating_positive": ("Positive", "Speeding Up"),
        "accelerating_negative": ("Negative", "Speeding Up"),
        "decelerating_positive": ("Positive", "Slowing Down"),
        "decelerating_negative": ("Negative", "Slowing Down"),
    }

    for graph_kind, expected in graph_expectations.items():
        checks.append(
            (
                f"MotionGraph.Position({graph_kind})",
                501,
                lambda g=graph_kind: graph.choose_problem_dict(
                    "Position-Time Graph", "Hard", graph_type=g
                ),
                None,
            )
        )
        checks.append(
            (
                f"MotionGraph.Velocity({graph_kind})",
                502,
                lambda g=graph_kind: graph.choose_problem_dict(
                    "Velocity-Time Graph", "Hard", graph_type=g
                ),
                None,
            )
        )

    for context, seed, factory, required_tokens in checks:
        try:
            random.seed(seed)
            payload = factory()
            run_seeded(context, lambda payload=payload: payload, required_tokens)
            if context.startswith("MotionGraph."):
                graph_type = payload["graph_type"]
                expected_direction, expected_motion = graph_expectations[graph_type]
                got_direction, got_motion = payload["answers"]
                if got_direction != expected_direction or got_motion != expected_motion:
                    raise AssertionError(
                        f"{context} expected {(expected_direction, expected_motion)}, got {(got_direction, got_motion)}"
                    )
        except Exception as e:
            _record_failure(failures, context, e)
        finally:
            _close_figures()

    return failures


def check_edge_case_seed_sweeps() -> FailureList:
    failures: FailureList = []
    sweep_seeds = range(0, 30)

    sweeps: list[tuple[str, object, list[str]]] = [
        ("ForceGenerator", ForceGenerator(), ["Newton's Second Law"]),
        ("ProjectileGenerator", ProjectileGenerator(), ["Type 1", "Type 2", "Type 3"]),
        ("CollisionGenerator", CollisionGenerator(), ["Elastic Collision", "Inelastic Collision"]),
        (
            "WaveGenerator",
            WaveGenerator(),
            [
                "Wave Properties",
                "String Harmonics",
                "Open Ended Column Harmonics",
                "Closed End Column Harmonics",
                "deciBel Scale",
            ],
        ),
        (
            "MotionGraphGenerator",
            MotionGraphGenerator(),
            ["Position-Time Graph", "Velocity-Time Graph"],
        ),
    ]

    for name, generator, problem_types in sweeps:
        for seed in sweep_seeds:
            for problem_type in problem_types:
                context = f"{name}[{problem_type}|Hard|seed={seed}]"
                try:
                    random.seed(seed)
                    payload = generator.choose_problem_dict(problem_type, "Hard")
                    _validate_payload_dict(payload, context)
                    _assert_finite_answers(payload, context)
                except Exception as e:
                    _record_failure(failures, context, e)
                finally:
                    _close_figures()

    return failures


def check_synthetic_regression_tripwires() -> FailureList:
    failures: FailureList = []

    checks: list[tuple[str, int, Callable[[], dict]]] = [
        (
            "ForceGenerator.synthetic",
            611,
            lambda: ForceGenerator().choose_problem_dict("Newton's Second Law", "Hard"),
        ),
        (
            "ProjectileGenerator.synthetic",
            612,
            lambda: ProjectileGenerator()._generate_type1_question("Hard", solve_for="v_f and theta"),
        ),
        (
            "CollisionGenerator.synthetic",
            613,
            lambda: CollisionGenerator().choose_problem_dict("Elastic Collision", "Hard"),
        ),
        (
            "WaveGenerator.synthetic",
            614,
            lambda: WaveGenerator().choose_problem_dict("String Harmonics", "Hard"),
        ),
        (
            "MotionGraphGenerator.synthetic",
            615,
            lambda: MotionGraphGenerator().choose_problem_dict(
                "Position-Time Graph", "Hard", graph_type="linear_positive"
            ),
        ),
    ]

    for context, seed, factory in checks:
        try:
            random.seed(seed)
            payload = factory()
            _validate_payload_dict(payload, context)

            bad_units = dict(payload)
            bad_units["units"] = list(payload["units"]) + ["synthetic_extra_unit"]
            _assert_payload_rejected(bad_units, f"{context}.units_mismatch")

            bad_question = dict(payload)
            bad_question["question"] = "   "
            _assert_payload_rejected(bad_question, f"{context}.blank_question")
        except Exception as e:
            _record_failure(failures, context, e)
        finally:
            _close_figures()

    return failures


def check_doc_question_organizer() -> FailureList:
    failures: FailureList = []
    from xtrct_docs.question_organizer import Org
    org = Org()

    methods: list[str] = [
        "funny_forces_practice",
        "projectile_quiz_CP",
        "projectile_quiz_H",
        "create_first_doc",
        "unit1_practice_doc",
        "constant_motion_quiz",
        "projectile_practice",
        "motion_graph_test",
        "mixed_motion_with_graphs",
        "mixed_motion_with_graphs_H",
    ]

    for name in methods:
        try:
            method = getattr(org, name)
            generated = method()
            sections = generated() if callable(generated) else generated
            if not isinstance(sections, list):
                raise AssertionError(f"Expected list of sections, got {type(sections).__name__}")

            for section_index, section in enumerate(sections):
                problems = section.get("problems", [])
                for problem_index, problem in enumerate(problems):
                    context = f"Org.{name}[section={section_index}, problem={problem_index}]"
                    _validate_payload_dict(problem, context)
            try:
                import matplotlib.pyplot as plt

                plt.close("all")
            except Exception:
                pass
        except Exception as e:
            _record_failure(failures, f"Org.{name}", e)

    return failures


def check_for_singular_unit_key() -> FailureList:
    failures: FailureList = []
    generator_root = PROJECT_ROOT / "utils" / "generators"
    for py_file in generator_root.rglob("*.py"):
        source = py_file.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=str(py_file))
        except SyntaxError as e:
            failures.append(f"{py_file.as_posix()}: parse error during unit-key scan: {e}")
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Return):
                continue
            if not isinstance(node.value, ast.Dict):
                continue

            keys = []
            for key in node.value.keys:
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    keys.append(key.value)

            if "question" in keys and "answers" in keys and "unit" in keys:
                failures.append(
                    f"{py_file.as_posix()}:{node.lineno}: return payload uses 'unit' instead of 'units'"
                )
    return failures


def main() -> int:
    checks = [
        ("explicit solve_for paths", check_explicit_solve_for_paths),
        ("seeded generator regressions", check_seeded_generator_regressions),
        ("edge-case seed sweeps", check_edge_case_seed_sweeps),
        ("synthetic regression tripwires", check_synthetic_regression_tripwires),
        ("question organizer factories", check_doc_question_organizer),
        ("payload key scan", check_for_singular_unit_key),
    ]

    all_failures: FailureList = []
    for label, runner in checks:
        failures = runner()
        if failures:
            all_failures.extend([f"[{label}] {msg}" for msg in failures])

    if all_failures:
        print(f"Prompt/answer guardrail FAILED ({len(all_failures)} issue(s))")
        for msg in all_failures:
            print(f" - {msg}")
        return 1

    print("Prompt/answer guardrail passed (no issues found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
