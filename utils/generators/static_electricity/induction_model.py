from __future__ import annotations

import random

from .conduction_model import charge_count_label, sign_label, sign_symbol


INDUCTION_MODEL_NOTES = {
    "rule": (
        "In this simplified model, a nearby charged object redistributes electrons without touching."
    ),
    "grounding": (
        "If the conductor is grounded while the charged object is nearby, electrons can enter or leave through the ground."
    ),
    "separation": (
        "If two touching conductors are polarized and then separated, they keep opposite charges."
    ),
}


FINAL_SIGN_OPTIONS: tuple[str, ...] = ("Positive", "Neutral", "Negative")


def opposite_sign(sign: str) -> str:
    return "negative" if sign == "positive" else "positive"


def build_induction_case(difficulty: str) -> dict:
    method = random.choice(("grounding", "separation"))
    inducer_sign = random.choice(("positive", "negative"))
    inducer_chunks = random.choice((4, 6, 8))
    transfer_chunks = {"Easy": 2, "Medium": 3, "Hard": 4}.get(difficulty, 3)

    if method == "grounding":
        return _build_grounding_case(difficulty, inducer_sign, inducer_chunks, transfer_chunks)
    return _build_separation_case(difficulty, inducer_sign, inducer_chunks, transfer_chunks)


def _build_grounding_case(
    difficulty: str, inducer_sign: str, inducer_chunks: int, transfer_chunks: int
) -> dict:
    final_sign = opposite_sign(inducer_sign)
    if inducer_sign == "negative":
        mechanism_answer = "Electrons moved from B to ground"
    else:
        mechanism_answer = "Electrons moved from ground to B"

    mechanism_options = (
        "Electrons moved from B to ground",
        "Electrons moved from ground to B",
        "Protons moved from B to ground",
        "Protons moved from ground to B",
    )

    return {
        "difficulty": difficulty,
        "method": "grounding",
        "title": "Induction with Grounding",
        "inducer_sign": inducer_sign,
        "inducer_chunks": inducer_chunks,
        "transfer_chunks": transfer_chunks,
        "asked_objects": ("B",),
        "mechanism_options": mechanism_options,
        "mechanism_answer": mechanism_answer,
        "expected_signs": {
            "B": sign_label(final_sign),
        },
        "expected_amounts": {
            "B": transfer_chunks,
        },
        "before_states": {
            "rod": {
                "label": "Charged Rod",
                "sign": inducer_sign,
                "chunks": inducer_chunks,
                "note": "Held near the conductor",
            },
            "B": {
                "label": "Conductor B",
                "sign": "neutral",
                "chunks": 0,
                "note": "Grounded while polarized",
            },
        },
        "after_states": {
            "rod": {
                "label": "Charged Rod",
                "sign": inducer_sign,
                "chunks": inducer_chunks,
                "note": "Never touches the conductor",
            },
            "B": {
                "label": "Conductor B",
                "sign": final_sign,
                "chunks": transfer_chunks,
                "note": "Ground removed first, then rod removed",
            },
        },
        "diagram_note_before": "A charged rod is brought near conductor B while B is connected to ground.",
        "diagram_note_after": "Ground is removed while the rod is still nearby, then the rod is taken away.",
        "explanation": (
            f"The rod never touches B, but it shifts electrons inside the conductor. "
            f"While grounded, {mechanism_answer.lower()}. "
            f"After the ground is removed, B is left {sign_label(final_sign).lower()} with "
            f"{charge_count_label(final_sign, transfer_chunks)}."
        ),
    }


def _build_separation_case(
    difficulty: str, inducer_sign: str, inducer_chunks: int, transfer_chunks: int
) -> dict:
    near_final_sign = opposite_sign(inducer_sign)
    far_final_sign = inducer_sign
    if inducer_sign == "negative":
        mechanism_answer = "Electrons moved from A to B"
    else:
        mechanism_answer = "Electrons moved from B to A"

    mechanism_options = (
        "Electrons moved from A to B",
        "Electrons moved from B to A",
        "Protons moved from A to B",
        "Protons moved from B to A",
    )

    return {
        "difficulty": difficulty,
        "method": "separation",
        "title": "Induction by Polarization and Separation",
        "inducer_sign": inducer_sign,
        "inducer_chunks": inducer_chunks,
        "transfer_chunks": transfer_chunks,
        "asked_objects": ("A", "B"),
        "mechanism_options": mechanism_options,
        "mechanism_answer": mechanism_answer,
        "expected_signs": {
            "A": sign_label(near_final_sign),
            "B": sign_label(far_final_sign),
        },
        "expected_amounts": {
            "A": transfer_chunks,
            "B": transfer_chunks,
        },
        "before_states": {
            "rod": {
                "label": "Charged Rod",
                "sign": inducer_sign,
                "chunks": inducer_chunks,
                "note": "Held near conductor A",
            },
            "A": {
                "label": "Conductor A",
                "sign": "neutral",
                "chunks": 0,
                "note": "Touching conductor B",
            },
            "B": {
                "label": "Conductor B",
                "sign": "neutral",
                "chunks": 0,
                "note": "Touching conductor A",
            },
        },
        "after_states": {
            "rod": {
                "label": "Charged Rod",
                "sign": inducer_sign,
                "chunks": inducer_chunks,
                "note": "Removed after the conductors separate",
            },
            "A": {
                "label": "Conductor A",
                "sign": near_final_sign,
                "chunks": transfer_chunks,
                "note": "The conductor closer to the rod",
            },
            "B": {
                "label": "Conductor B",
                "sign": far_final_sign,
                "chunks": transfer_chunks,
                "note": "The conductor farther from the rod",
            },
        },
        "diagram_note_before": "A charged rod is brought near two touching neutral conductors.",
        "diagram_note_after": "The conductors are pulled apart while the rod is still nearby, then the rod is removed.",
        "explanation": (
            f"The rod polarizes the touching conductors without touching them. "
            f"{mechanism_answer}. "
            f"Separating the conductors traps opposite charges: A ends {sign_label(near_final_sign).lower()} "
            f"with {charge_count_label(near_final_sign, transfer_chunks)}, and B ends "
            f"{sign_label(far_final_sign).lower()} with {charge_count_label(far_final_sign, transfer_chunks)}."
        ),
    }
