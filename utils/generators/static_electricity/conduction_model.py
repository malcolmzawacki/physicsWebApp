from __future__ import annotations

import random


CONDUCTION_MODEL_NOTES = {
    "rule": (
        "In this simplified model, identical conductors share charge equally after contact."
    ),
    "mechanism": (
        "Electrons move during conduction. Protons do not move from one solid object to another."
    ),
    "scope": (
        "Charge is represented here in discrete classroom charge chunks rather than physical units."
    ),
}


MECHANISM_OPTIONS: tuple[str, ...] = (
    "Electrons moved from A to B",
    "Electrons moved from B to A",
    "Protons moved from A to B",
    "Protons moved from B to A",
)


FINAL_SIGN_OPTIONS: tuple[str, ...] = ("Positive", "Neutral", "Negative")


def sign_label(sign: str) -> str:
    return {
        "positive": "Positive",
        "neutral": "Neutral",
        "negative": "Negative",
    }[sign]


def sign_symbol(sign: str) -> str:
    return {
        "positive": "+",
        "neutral": "0",
        "negative": "-",
    }[sign]


def charge_token_row(sign: str, chunks: int) -> str:
    if sign == "neutral" or chunks <= 0:
        return "0"
    token = sign_symbol(sign)
    return " ".join(token for _ in range(chunks))


def charge_count_label(sign: str, chunks: int) -> str:
    if sign == "neutral" or chunks <= 0:
        return "0"
    return f"{sign_symbol(sign)}{chunks}"


def build_conduction_case(difficulty: str) -> dict:
    chunk_options = {
        "Easy": (2, 4),
        "Medium": (4, 6),
        "Hard": (6, 8),
    }
    charged_box = random.choice(("A", "B"))
    neutral_box = "B" if charged_box == "A" else "A"
    initial_sign = random.choice(("positive", "negative"))
    initial_chunks = random.choice(chunk_options.get(difficulty, chunk_options["Medium"]))
    final_chunks = initial_chunks // 2

    if initial_sign == "negative":
        electron_source = charged_box
        electron_destination = neutral_box
    else:
        electron_source = neutral_box
        electron_destination = charged_box

    mechanism_answer = f"Electrons moved from {electron_source} to {electron_destination}"
    final_sign = initial_sign

    return {
        "difficulty": difficulty,
        "charged_box": charged_box,
        "neutral_box": neutral_box,
        "initial_sign": initial_sign,
        "initial_chunks": initial_chunks,
        "final_chunks": final_chunks,
        "final_sign": final_sign,
        "mechanism_answer": mechanism_answer,
        "before_states": {
            "A": {
                "sign": initial_sign if charged_box == "A" else "neutral",
                "chunks": initial_chunks if charged_box == "A" else 0,
                "note": "Initially charged conductor" if charged_box == "A" else "Initially neutral conductor",
            },
            "B": {
                "sign": initial_sign if charged_box == "B" else "neutral",
                "chunks": initial_chunks if charged_box == "B" else 0,
                "note": "Initially charged conductor" if charged_box == "B" else "Initially neutral conductor",
            },
        },
        "after_states": {
            "A": {
                "sign": final_sign,
                "chunks": final_chunks,
                "note": "After contact",
            },
            "B": {
                "sign": final_sign,
                "chunks": final_chunks,
                "note": "After contact",
            },
        },
        "explanation": (
            f"Because the conductors are identical, the initial charge splits equally. "
            f"Both boxes end {sign_label(final_sign).lower()} with {charge_count_label(final_sign, final_chunks)} each. "
            f"{mechanism_answer}."
        ),
    }
