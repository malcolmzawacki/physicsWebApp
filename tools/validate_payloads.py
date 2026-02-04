from __future__ import annotations

import sys
from typing import Dict, List, Tuple

from utils.generators.const_motion_generator import ConstantMotionGenerator
from utils.generators.linear_motion_generator import LinearMotionGenerator
from utils.generators.force_generator import ForceGenerator
from utils.generators.vector_generator import VectorGenerator
from utils.generators.projectile_generator import ProjectileGenerator
from utils.generators.waves_generator import WaveGenerator
from utils.generators.momentum_generators.collision_generator import CollisionGenerator
from utils.generators.motion_graph_generator import MotionGraphGenerator
from utils.generators.dist_disp_generator import DistDispGenerator
from utils.problem_payload import payload_from_dict, ProblemPayloadError


def validate_generator(gen, problem_types: List[str], difficulties: List[str]) -> Tuple[int, int, List[str]]:
    """Return (total, failures, messages)."""
    total = 0
    failures = 0
    messages: List[str] = []
    for p in problem_types:
        for d in difficulties:
            total += 1
            try:
                result = gen.choose_problem_dict(p, d)
                payload_from_dict(result)  # raises on error
            except Exception as e:
                failures += 1
                messages.append(f"{gen.__class__.__name__} [{p} | {d}]: {e}")
    return total, failures, messages


def main() -> int:
    difficulties = ["Easy", "Medium", "Hard"]

    checks: Dict[str, Tuple[object, List[str]]] = {
        "ConstantMotionGenerator": (
            ConstantMotionGenerator(),
            [
                "Constant Speed",
                "Average Speed",
                "Average Velocity",
                "Combined Constant Motion",
            ],
        ),
        "LinearMotionGenerator": (
            LinearMotionGenerator(),
            [
                "No Time",
                "No Distance",
                "No Acceleration",
                "No Final Velocity",
                "Mixed",
            ],
        ),
        "ForceGenerator": (
            ForceGenerator(),
            [
                "Type 1",
                "Type 2",
            ],
        ),
        "VectorGenerator": (
            VectorGenerator(),
            [
                "Find Components",
                "Find Resultant",
                "Summing Vectors",
            ],
        ),
        "ProjectileGenerator": (
            ProjectileGenerator(),
            [
                "Type 1",
                "Type 2",
            ],
        ),
        "WaveGenerator": (
            WaveGenerator(),
            [
                "Type 1",
                "Type 2",
            ],
        ),
        "CollisionGenerator": (
            CollisionGenerator(),
            [
                "Type 1",
                "Type 2",
            ],
        ),
        "MotionGraphGenerator": (
            MotionGraphGenerator(),
            [
                "Position-Time Graph",
                "Velocity-Time Graph",
            ],
        ),
        "DistDispGenerator": (
            DistDispGenerator(),
            [
                "1D Distance and Displacement",
            ],
        ),
    }

    total = failures = 0
    all_messages: List[str] = []
    for name, (gen, ptypes) in checks.items():
        t, f, msgs = validate_generator(gen, ptypes, difficulties)
        total += t
        failures += f
        all_messages.extend(msgs)

    print(f"Validated payloads: {total - failures}/{total} passed")
    if failures:
        print("Failures:")
        for m in all_messages:
            print(" -", m)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
