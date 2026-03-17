from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriboelectricMaterial:
    key: str
    label: str
    rank: int
    description: str
    classroom_safe: bool = True


TRIBOELECTRIC_MODEL_NOTES = {
    "rule": (
        "Higher-ranked materials tend to lose electrons and become positive. "
        "Lower-ranked materials tend to gain electrons and become negative."
    ),
    "scope": (
        "This is a simplified classroom triboelectric series intended for "
        "qualitative charging-by-friction activities."
    ),
    "tie_behavior": (
        "Identical materials are treated as having no reliable net charging outcome."
    ),
}


TRIBOELECTRIC_MATERIALS: tuple[TriboelectricMaterial, ...] = (
    TriboelectricMaterial(
        key="glass",
        label="Glass",
        rank=0,
        description="Often used as a strongly electron-losing reference material.",
    ),
    TriboelectricMaterial(
        key="human_hair",
        label="Human Hair",
        rank=1,
        description="Common classroom example that tends to become positive.",
    ),
    TriboelectricMaterial(
        key="nylon",
        label="Nylon",
        rank=2,
        description="Synthetic fabric that tends to lose electrons relative to many plastics.",
    ),
    TriboelectricMaterial(
        key="wool",
        label="Wool",
        rank=3,
        description="Common rubbing material in introductory static electricity demos.",
    ),
    TriboelectricMaterial(
        key="silk",
        label="Silk",
        rank=4,
        description="Traditional triboelectric-series material used in charge-transfer examples.",
    ),
    TriboelectricMaterial(
        key="paper",
        label="Paper",
        rank=5,
        description="Mid-series material useful for comparison activities.",
    ),
    TriboelectricMaterial(
        key="cotton",
        label="Cotton",
        rank=6,
        description="Familiar fabric that sits near the middle of the simplified model.",
    ),
    TriboelectricMaterial(
        key="wood",
        label="Wood",
        rank=7,
        description="A moderate electron-gaining material in this simplified ranking.",
    ),
    TriboelectricMaterial(
        key="amber",
        label="Amber",
        rank=8,
        description="Classic historical example associated with static electricity.",
    ),
    TriboelectricMaterial(
        key="polyester",
        label="Polyester",
        rank=9,
        description="Common synthetic material that tends to gain electrons.",
    ),
    TriboelectricMaterial(
        key="styrofoam",
        label="Styrofoam",
        rank=10,
        description="Often becomes strongly negative after friction in classroom contexts.",
    ),
    TriboelectricMaterial(
        key="teflon",
        label="Teflon",
        rank=11,
        description="A strong electron-gaining endpoint for a simplified classroom series.",
    ),
)


DEFAULT_REFERENCE_SERIES_KEYS: tuple[str, ...] = (
    "glass",
    "human_hair",
    "nylon",
    "wool",
    "silk",
    "paper",
    "cotton",
    "amber",
    "polyester",
    "styrofoam",
    "teflon",
)


_MATERIALS_BY_KEY = {material.key: material for material in TRIBOELECTRIC_MATERIALS}


def get_triboelectric_materials() -> tuple[TriboelectricMaterial, ...]:
    return TRIBOELECTRIC_MATERIALS


def get_material(material_key: str) -> TriboelectricMaterial:
    try:
        return _MATERIALS_BY_KEY[material_key]
    except KeyError as exc:
        raise ValueError(f"Unknown triboelectric material key: {material_key}") from exc


def get_reference_series(
    material_keys: tuple[str, ...] | None = None,
) -> tuple[TriboelectricMaterial, ...]:
    keys = material_keys or DEFAULT_REFERENCE_SERIES_KEYS
    return tuple(get_material(key) for key in keys)


def compare_materials(first_key: str, second_key: str) -> int:
    first = get_material(first_key)
    second = get_material(second_key)
    if first.rank == second.rank:
        return 0
    if first.rank < second.rank:
        return 1
    return -1


def get_charge_outcome(first_key: str, second_key: str) -> dict[str, str | None]:
    comparison = compare_materials(first_key, second_key)
    if comparison == 0:
        return {
            "positive_key": None,
            "negative_key": None,
            "electron_giver_key": None,
            "electron_receiver_key": None,
        }
    if comparison > 0:
        return {
            "positive_key": first_key,
            "negative_key": second_key,
            "electron_giver_key": first_key,
            "electron_receiver_key": second_key,
        }
    return {
        "positive_key": second_key,
        "negative_key": first_key,
        "electron_giver_key": second_key,
        "electron_receiver_key": first_key,
    }


def describe_charge_outcome(first_key: str, second_key: str) -> dict[str, str]:
    first = get_material(first_key)
    second = get_material(second_key)
    outcome = get_charge_outcome(first_key, second_key)

    positive_key = outcome["positive_key"]
    if positive_key is None:
        return {
            "summary": f"{first.label} and {second.label} have no modeled net charging difference.",
            "electron_flow": "No net electron transfer is predicted by this simplified model.",
        }

    positive = get_material(positive_key)
    negative = get_material(outcome["negative_key"])
    return {
        "summary": f"{positive.label} becomes positive and {negative.label} becomes negative.",
        "electron_flow": f"Electrons move from {positive.label} to {negative.label}.",
    }
