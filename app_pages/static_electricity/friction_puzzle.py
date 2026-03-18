from __future__ import annotations

import random
import time
from string import ascii_uppercase

import streamlit as st

from utils.ui_components import build_performance_table, init_performance, performance_expander, record_performance
from utils.ui_state import State


def _build_logic_puzzle_case(difficulty: str) -> dict:
    if difficulty == "Easy":
        material_count = 3
        extra_clue_count = 0
    elif difficulty == "Medium":
        material_count = 4
        extra_clue_count = 1
    else:
        material_count = 5
        extra_clue_count = 2

    labels = list(ascii_uppercase[:material_count])
    hidden_order = random.sample(labels, k=material_count)
    clues: list[dict[str, str]] = []
    used_pairs: set[tuple[int, int]] = set()

    for index in range(material_count - 1):
        positive_label = hidden_order[index]
        negative_label = hidden_order[index + 1]
        clues.append(
            {
                "positive_label": positive_label,
                "negative_label": negative_label,
                "text": (
                    f"When {positive_label} is rubbed with {negative_label}, "
                    f"{positive_label} becomes positive and {negative_label} becomes negative."
                ),
            }
        )
        used_pairs.add((index, index + 1))

    candidate_pairs = [
        (left, right)
        for left in range(material_count)
        for right in range(left + 1, material_count)
        if (left, right) not in used_pairs
    ]
    random.shuffle(candidate_pairs)

    for left_index, right_index in candidate_pairs[:extra_clue_count]:
        positive_label = hidden_order[left_index]
        negative_label = hidden_order[right_index]
        clues.append(
            {
                "positive_label": positive_label,
                "negative_label": negative_label,
                "text": (
                    f"Rubbing {positive_label} with {negative_label} leaves "
                    f"{positive_label} positive and {negative_label} negative."
                ),
            }
        )

    random.shuffle(clues)
    return {"difficulty": difficulty, "labels": labels, "hidden_order": hidden_order, "clues": clues}


def _reset_logic_puzzle(state: State, difficulty: str) -> None:
    state.set("case", _build_logic_puzzle_case(difficulty))
    state.inc("question_number")
    state.set("submitted", False)
    state.set("last_result", None)


def _get_logic_puzzle_state() -> tuple[State, str, dict, int]:
    state = State("friction_puzzle")
    state.ensure("difficulty", "Medium")
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy("performance", lambda: init_performance(["Ranking Logic Puzzle"], ["Easy", "Medium", "Hard"]))
    difficulty = state.get("difficulty", "Medium")
    if not state.has("case"):
        _reset_logic_puzzle(state, difficulty)
        st.rerun()
    return state, difficulty, state.get("case"), state.get("question_number", 0)


def render() -> None:
    state, difficulty, case, question_number = _get_logic_puzzle_state()
    labels = case["labels"]
    hidden_order = case["hidden_order"]

    selected_difficulty = st.radio(
        "Puzzle Difficulty",
        options=("Easy", "Medium", "Hard"),
        index=("Easy", "Medium", "Hard").index(difficulty),
        horizontal=True,
        key=state.key("difficulty_select"),
    )
    if selected_difficulty != difficulty:
        state.set("difficulty", selected_difficulty)
        _reset_logic_puzzle(state, selected_difficulty)
        st.rerun()

    st.subheader("Ranking Logic Puzzle")
    st.write("Use the rubbing outcomes to reconstruct the full ranking from most likely to become positive to most likely to become negative.")

    clue_col, ranking_col = st.columns((3, 2), gap="large")
    with clue_col:
        st.markdown("**Clues**")
        for index, clue in enumerate(case["clues"], start=1):
            st.write(f"{index}. {clue['text']}")
            if difficulty == "Easy":
                st.caption(f"`{clue['positive_label']} > {clue['negative_label']}`")
        st.caption(f"This puzzle uses {len(labels)} anonymous materials.")

        result = state.get("last_result")
        if state.get("submitted") and result:
            if result["incomplete"]:
                st.warning("Fill every rank before checking the puzzle.")
            elif result["has_duplicates"]:
                st.warning("Each anonymous material can appear only once in the ranking.")
            elif result["is_correct"]:
                st.success("Correct.")
            else:
                st.error("Not quite.")

            st.caption(f"Correct ranking: {' > '.join(hidden_order)}")
            st.caption("Read the order from left to right as most likely to become positive through most likely to become negative.")

            if result["is_correct"]:
                st.caption("Loading the next puzzle...")
                time.sleep(0.8)
                _reset_logic_puzzle(state, difficulty)
                st.rerun()

        performance_expander(build_performance_table(state.get("performance"), ["Easy", "Medium", "Hard"]))

    with ranking_col:
        st.markdown("#### Build the Ranking")
        st.caption("Top slot = most likely to lose electrons and become positive. Bottom slot = most likely to gain electrons and become negative.")
        st.markdown("`+` Most likely positive")
        selected_order: list[str] = []
        options = ("Select...", *labels)
        for rank_index in range(len(labels)):
            choice = st.selectbox(
                f"Rank {rank_index + 1}",
                options=options,
                key=state.key(f"rank_{rank_index}_{question_number}"),
            )
            selected_order.append(choice)
            if rank_index < len(labels) - 1:
                st.caption("`>` more likely to become positive than the slot below")
        st.markdown("`-` Most likely negative")

    new_col, spacer_col, check_col = st.columns((1, 4, 1.2), gap="large")
    with new_col:
        new_puzzle_clicked = st.button("New Puzzle", key=state.key("new_puzzle"), type="secondary", use_container_width=True)
    with check_col:
        check_clicked = st.button("Check Puzzle", key=state.key("check_puzzle"), type="primary", use_container_width=True)

    if new_puzzle_clicked:
        _reset_logic_puzzle(state, difficulty)
        st.rerun()

    if check_clicked:
        incomplete = any(choice == "Select..." for choice in selected_order)
        has_duplicates = len({choice for choice in selected_order if choice != "Select..."}) != len(
            [choice for choice in selected_order if choice != "Select..."]
        )
        normalized_order = tuple(choice for choice in selected_order if choice != "Select...")
        is_correct = not incomplete and not has_duplicates and normalized_order == tuple(hidden_order)

        if not incomplete and not has_duplicates:
            performance = state.get("performance")
            state.set("performance", record_performance(performance, "Ranking Logic Puzzle", difficulty, is_correct))
        state.set("submitted", True)
        state.set(
            "last_result",
            {
                "incomplete": incomplete,
                "has_duplicates": has_duplicates,
                "is_correct": is_correct,
                "submitted_order": selected_order,
            },
        )
        st.rerun()
