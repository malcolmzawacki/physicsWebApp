import random
from typing import Callable, Dict, List, Tuple


ShapeSpec = Dict[str, object]
ObjectSpec = Dict[str, object]


SHAPES: Dict[str, ShapeSpec] = {
    "solid_disk": {
        "label": "Solid disk",
        "axes": {
            "center": {
                "formula": "I = 1/2 m r^2",
                "calc": lambda m, r: 0.5 * m * r * r,
            }
        },
    },
    "thin_hoop": {
        "label": "Thin hoop",
        "axes": {
            "center": {
                "formula": "I = m r^2",
                "calc": lambda m, r: m * r * r,
            }
        },
    },
    "solid_sphere": {
        "label": "Solid sphere",
        "axes": {
            "center": {
                "formula": "I = 2/5 m r^2",
                "calc": lambda m, r: 0.4 * m * r * r,
            }
        },
    },
    "rod_center": {
        "label": "Thin rod (center)",
        "axes": {
            "center": {
                "formula": "I = 1/12 m L^2",
                "calc": lambda m, L: (1 / 12) * m * L * L,
            }
        },
    },
    "rod_end": {
        "label": "Thin rod (end)",
        "axes": {
            "end": {
                "formula": "I = 1/3 m L^2",
                "calc": lambda m, L: (1 / 3) * m * L * L,
            }
        },
    },
}


ROTATION_OBJECTS: List[ObjectSpec] = [
    {
        "name": "door",
        "pivot": "hinge",
        "context": "A door rotates about a hinge.",
        "shape_id": "rod_end",
        "lever_range_m": (0.4, 0.9),
    },
    {
        "name": "wheel",
        "pivot": "axle",
        "context": "A wheel rotates about its axle.",
        "shape_id": "thin_hoop",
        "lever_range_m": (0.2, 0.45),
    },
    {
        "name": "wrench",
        "pivot": "bolt",
        "context": "A wrench pivots about a bolt.",
        "shape_id": "rod_end",
        "lever_range_m": (0.12, 0.35),
    },
    {
        "name": "gate",
        "pivot": "hinge",
        "context": "A gate swings about a hinge.",
        "shape_id": "rod_end",
        "lever_range_m": (0.5, 1.2),
    },
    {
        "name": "steering wheel",
        "pivot": "axle",
        "context": "A steering wheel rotates about its axle.",
        "shape_id": "solid_disk",
        "lever_range_m": (0.12, 0.2),
    },
    {
        "name": "meter stick",
        "pivot": "pivot",
        "context": "A meter stick is mounted on a pivot.",
        "shape_id": "rod_center",
        "lever_range_m": (0.25, 0.5),
    },
    {
        "name": "fan blade",
        "pivot": "axle",
        "context": "A fan blade spins about its axle.",
        "shape_id": "rod_end",
        "lever_range_m": (0.1, 0.3),
    },
]


def pick_rotation_object(
    rng: random.Random | None = None, shape_filter: Callable[[ObjectSpec], bool] | None = None
) -> ObjectSpec:
    chooser = rng or random
    objects = ROTATION_OBJECTS
    if shape_filter is not None:
        objects = [obj for obj in objects if shape_filter(obj)]
    return chooser.choice(objects)


def sample_lever_arm(obj: ObjectSpec, difficulty: str, rng: random.Random | None = None) -> float:
    chooser = rng or random
    min_r, max_r = obj["lever_range_m"]
    if difficulty == "Easy":
        upper = min_r + (max_r - min_r) * 0.6
    elif difficulty == "Hard":
        upper = max_r
    else:
        upper = min_r + (max_r - min_r) * 0.85
    return chooser.uniform(min_r, upper)
