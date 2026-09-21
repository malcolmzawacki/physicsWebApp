"""Explicit question targets shared by browser controls and worksheet recipes.

The checked-in catalog describes existing question branches, not inferred algebra.
Target IDs are permanent within a generator/problem type. Unsupported targets fail
before generation; selecting mixed preserves the legacy sampling distribution.
"""
import json
import random
from functools import lru_cache
from pathlib import Path

MIXED = "mixed"


@lru_cache(maxsize=1)
def _catalog():
    return json.loads(Path(__file__).with_name("solve_for_catalog.json").read_text(encoding="utf-8"))


def target_options(generator, problem_type, difficulty):
    """Return declared targets for this exact type/level, without generating a case."""
    entries = _catalog().get(type(generator).__name__, {}).get(problem_type, [])
    return [dict(id=e["id"], label=e["label"]) for e in entries if difficulty in e["levels"]]


def generate_selected(generator, problem_type, difficulty, target_id=MIXED):
    """Generate a fresh complete payload using the same request in UI or export."""
    if target_id == MIXED:
        result = generator.choose_problem_dict(problem_type, difficulty)
    else:
        entries = _catalog().get(type(generator).__name__, {}).get(problem_type, [])
        entry = next((e for e in entries if e["id"] == target_id and difficulty in e["levels"]), None)
        if entry is None:
            raise ValueError(f"Unsupported solve-for {target_id!r} for {problem_type!r} / {difficulty}")
        call = random.choice(entry["calls"])
        kwargs = dict(call.get("kwargs", {}))
        if call.get("difficulty", True):
            kwargs["difficulty"] = difficulty
        result = getattr(generator, call["method"])(**kwargs)
    result = dict(result)
    result["problem_type"], result["difficulty"] = problem_type, difficulty
    result["extras"] = {**result.get("extras", {}), "requested_target_id": target_id}
    return result


def select_target(generator, problem_type, difficulty, state, *, key="solve_for_select"):
    """Render only useful selectors; discard invalid choices after a type/level change."""
    import streamlit as st
    options = target_options(generator, problem_type, difficulty)
    if len(options) < 2:
        return options[0]["id"] if options else MIXED
    labels = {MIXED: "Mixed practice", **{entry["id"]: entry["label"] for entry in options}}
    widget_key = state.key(key)
    if st.session_state.get(widget_key) not in labels:
        st.session_state[widget_key] = MIXED
    return st.selectbox("Solve for", list(labels), format_func=labels.get, key=widget_key,
                        help="Available targets follow this problem type and difficulty.")
