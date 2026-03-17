import random
import time
from string import ascii_uppercase

import streamlit as st

from utils.ui_components import (
    build_performance_table,
    init_performance,
    performance_expander,
    record_performance,
)
from utils.ui_state import State
from utils.generators.static_electricity import (
    TRIBOELECTRIC_MODEL_NOTES,
    compare_materials,
    describe_charge_outcome,
    get_material,
    get_reference_series,
    get_triboelectric_materials,
)


def _render_symbol_legend() -> None:
    st.caption("Legend: `+` = becomes positive, `-` = becomes negative, `e-` = electron flow")


def _render_reference_series(material_keys: tuple[str, ...] | None = None) -> None:
    series = get_reference_series(material_keys)
    st.markdown("#### Classroom Triboelectric Reference")
    st.caption(TRIBOELECTRIC_MODEL_NOTES["rule"])
    st.caption("Top of the list tends to lose electrons. Bottom of the list tends to gain electrons.")

    if not series:
        return

    st.markdown("`+` More likely to become positive")
    for material in series:
        st.markdown(f"`{material.rank + 1:>2}`  {material.label}")
    st.markdown("`-` More likely to become negative")


def _render_charge_flow_strip(first_key: str, second_key: str) -> None:
    first = get_material(first_key)
    second = get_material(second_key)
    comparison = compare_materials(first_key, second_key)

    if comparison == 0:
        st.caption(f"`{first.label}`  |  no clear net transfer  |  `{second.label}`")
        return

    positive = first if comparison > 0 else second
    negative = second if comparison > 0 else first
    st.markdown(
        f"`+ {positive.label}`  `e- ->`  `- {negative.label}`"
    )


def _build_comparison_case() -> dict[str, str]:
    materials = get_triboelectric_materials()
    first, second = random.sample(materials, 2)
    return {
        "left_key": first.key,
        "right_key": second.key,
    }


def _comparison_difficulty(first_key: str, second_key: str) -> str:
    gap = abs(get_material(first_key).rank - get_material(second_key).rank)
    if gap >= 6:
        return "Easy"
    if gap >= 3:
        return "Medium"
    return "Hard"


def _format_rank_gap(first_key: str, second_key: str) -> str:
    first = get_material(first_key)
    second = get_material(second_key)
    gap = abs(first.rank - second.rank)
    if gap == 0:
        return "same position"
    if gap == 1:
        return "adjacent positions"
    return f"{gap} positions apart"


def _render_outcome_card(first_key: str, second_key: str) -> None:
    first = get_material(first_key)
    second = get_material(second_key)
    outcome_text = describe_charge_outcome(first_key, second_key)
    comparison = compare_materials(first_key, second_key)

    st.markdown("#### Predicted Outcome")
    _render_charge_flow_strip(first_key, second_key)
    st.info(outcome_text["summary"])
    st.write(outcome_text["electron_flow"])

    if comparison == 0:
        st.caption("These are the same material in the simplified model, so no reliable net charging is predicted.")
        return

    stronger = first.label if comparison > 0 else second.label
    weaker = second.label if comparison > 0 else first.label
    st.caption(
        f"{stronger} is higher on the reference list than {weaker}, so it is modeled as losing electrons. "
        f"The two materials are {_format_rank_gap(first_key, second_key)}."
    )


def _render_explorer() -> None:
    state = State("friction_explorer")
    materials = get_triboelectric_materials()
    labels = {material.key: material.label for material in materials}
    keys = [material.key for material in materials]

    state.ensure("left_material", "glass")
    state.ensure("right_material", "teflon")

    st.subheader("Explorer")
    st.write("Choose two materials and inspect the predicted charging outcome after rubbing them together.")

    left_col, right_col = st.columns(2)
    with left_col:
        left_key = st.selectbox(
            "Material 1",
            options=keys,
            format_func=lambda key: labels[key],
            index=keys.index(state.get("left_material", "glass")),
            key=state.key("left_select"),
        )
    with right_col:
        right_key = st.selectbox(
            "Material 2",
            options=keys,
            format_func=lambda key: labels[key],
            index=keys.index(state.get("right_material", "teflon")),
            key=state.key("right_select"),
        )

    state.set("left_material", left_key)
    state.set("right_material", right_key)

    _render_outcome_card(left_key, right_key)

    with st.expander("Why this model works for the page", expanded=False):
        st.write(TRIBOELECTRIC_MODEL_NOTES["scope"])
        st.write(TRIBOELECTRIC_MODEL_NOTES["tie_behavior"])

    with st.expander("Material notes", expanded=False):
        first = get_material(left_key)
        second = get_material(right_key)
        st.markdown(f"**{first.label}:** {first.description}")
        st.markdown(f"**{second.label}:** {second.description}")


def _comparison_answer_options(left_key: str, right_key: str) -> tuple[str, ...]:
    left = get_material(left_key)
    right = get_material(right_key)
    return (
        left.label,
        right.label,
        "Neither / no reliable net charge difference",
    )


def _reset_comparison_question(state: State) -> None:
    case = _build_comparison_case()
    state.set("case", case)
    state.set("submitted", False)
    state.set("last_result", None)


def _render_comparison_performance(state: State) -> None:
    performance = state.get("performance")
    df = build_performance_table(performance, ["Easy", "Medium", "Hard"])
    performance_expander(df)


def _render_comparison_practice() -> None:
    state = State("friction_compare")
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure_lazy("case", _build_comparison_case)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(["Comparison Practice"], ["Easy", "Medium", "Hard"]),
    )
    state.ensure("submitted", False)
    state.ensure("last_result", None)

    case = state.get("case")
    left_key = case["left_key"]
    right_key = case["right_key"]
    left = get_material(left_key)
    right = get_material(right_key)
    difficulty = _comparison_difficulty(left_key, right_key)
    outcome = describe_charge_outcome(left_key, right_key)
    answer_options = _comparison_answer_options(left_key, right_key)

    st.subheader("Comparison Practice")
    st.write(
        "Use the reference series to decide which material becomes positive and which becomes negative after rubbing."
    )
    st.caption(f"Difficulty: {difficulty}")

    st.markdown(
        f"When **{left.label}** is rubbed with **{right.label}**, which material becomes positive and which becomes negative?"
    )
    _render_charge_flow_strip(left_key, right_key)

    positive_choice = st.radio(
        "Becomes positive",
        options=answer_options,
        key=state.key(f"positive_choice_{left_key}_{right_key}"),
    )
    negative_choice = st.radio(
        "Becomes negative",
        options=answer_options,
        key=state.key(f"negative_choice_{left_key}_{right_key}"),
    )

    score_col, next_col = st.columns((2, 1))
    with score_col:
        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        if attempts == 0:
            st.caption("Score: 0/0")
        else:
            st.caption(f"Score: {correct}/{attempts}")
    with next_col:
        if st.button("New Pair", key=state.key("new_pair")):
            _reset_comparison_question(state)
            st.rerun()

    if st.button("Check Answer", key=state.key("check_answer")):
        expected_positive = get_material(
            left_key if compare_materials(left_key, right_key) > 0 else right_key
        ).label
        expected_negative = get_material(
            right_key if compare_materials(left_key, right_key) > 0 else left_key
        ).label
        if compare_materials(left_key, right_key) == 0:
            expected_positive = "Neither / no reliable net charge difference"
            expected_negative = "Neither / no reliable net charge difference"

        is_valid = positive_choice != negative_choice or positive_choice == "Neither / no reliable net charge difference"
        is_correct = (
            is_valid
            and positive_choice == expected_positive
            and negative_choice == expected_negative
        )

        state.inc("attempt_count")
        if is_correct:
            state.inc("correct_count")
        performance = state.get("performance")
        updated = record_performance(performance, "Comparison Practice", difficulty, is_correct)
        state.set("performance", updated)
        state.set("submitted", True)
        state.set(
            "last_result",
            {
                "is_correct": is_correct,
                "is_valid": is_valid,
                "expected_positive": expected_positive,
                "expected_negative": expected_negative,
            },
        )

    result = state.get("last_result")
    if state.get("submitted") and result:
        if not result["is_valid"]:
            st.warning("A material cannot be both positive and negative in the same rubbing interaction.")
        elif result["is_correct"]:
            st.success("Correct.")
        else:
            st.error("Not quite.")

        st.write(outcome["summary"])
        st.write(outcome["electron_flow"])
        st.caption(
            f"Correct response: positive = {result['expected_positive']}; negative = {result['expected_negative']}."
        )
        st.caption(
            f"The two materials are {_format_rank_gap(left_key, right_key)} on the simplified triboelectric list."
        )
        if result["is_correct"]:
            st.caption("Loading the next comparison...")
            time.sleep(0.8)
            _reset_comparison_question(state)
            st.rerun()

    _render_comparison_performance(state)


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
    return {
        "difficulty": difficulty,
        "labels": labels,
        "hidden_order": hidden_order,
        "clues": clues,
    }


def _reset_logic_puzzle(state: State, difficulty: str) -> None:
    state.set("case", _build_logic_puzzle_case(difficulty))
    state.inc("question_number")
    state.set("submitted", False)
    state.set("last_result", None)


def _render_logic_puzzle_performance(state: State) -> None:
    performance = state.get("performance")
    df = build_performance_table(performance, ["Easy", "Medium", "Hard"])
    performance_expander(df)


def _get_logic_puzzle_state() -> tuple[State, str, dict, int]:
    state = State("friction_puzzle")
    state.ensure("difficulty", "Medium")
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(["Ranking Logic Puzzle"], ["Easy", "Medium", "Hard"]),
    )

    difficulty = state.get("difficulty", "Medium")
    if not state.has("case"):
        _reset_logic_puzzle(state, difficulty)
        st.rerun()
    case = state.get("case")
    question_number = state.get("question_number", 0)
    return state, difficulty, case, question_number


def _render_logic_puzzle_clues() -> None:
    state, difficulty, case, _question_number = _get_logic_puzzle_state()
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
    st.write(
        "Use the rubbing outcomes to reconstruct the full ranking from most likely to become positive "
        "to most likely to become negative."
    )

    st.markdown("**Clues**")
    for index, clue in enumerate(case["clues"], start=1):
        st.write(f"{index}. {clue['text']}")
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

        correct_order_text = " > ".join(hidden_order)
        st.caption(f"Correct ranking: {correct_order_text}")
        st.caption(
            "Read the order from left to right as most likely to become positive through most likely to become negative."
        )

        if result["is_correct"]:
            st.caption("Loading the next puzzle...")
            time.sleep(0.8)
            _reset_logic_puzzle(state, difficulty)
            st.rerun()

    _render_logic_puzzle_performance(state)


def _render_logic_puzzle_ranking() -> None:
    state, difficulty, case, question_number = _get_logic_puzzle_state()
    labels = case["labels"]
    hidden_order = case["hidden_order"]

    selected_order: list[str] = []
    st.markdown("#### Build the Ranking")
    st.caption(
        "Top slot = most likely to lose electrons and become positive. Bottom slot = most likely to gain electrons and become negative."
    )
    st.markdown("`+` Most likely positive")

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

    new_puzzle_clicked = st.button("New Puzzle", key=state.key("new_puzzle"))
    check_clicked = st.button("Check Puzzle", key=state.key("check_puzzle"))

    if new_puzzle_clicked:
        _reset_logic_puzzle(state, difficulty)
        st.rerun()

    if check_clicked:
        incomplete = any(choice == "Select..." for choice in selected_order)
        has_duplicates = len({choice for choice in selected_order if choice != "Select..."}) != len(
            [choice for choice in selected_order if choice != "Select..."]
        )
        normalized_order = tuple(choice for choice in selected_order if choice != "Select...")
        is_correct = (
            not incomplete
            and not has_duplicates
            and normalized_order == tuple(hidden_order)
        )

        if not incomplete and not has_duplicates:
            performance = state.get("performance")
            updated = record_performance(performance, "Ranking Logic Puzzle", difficulty, is_correct)
            state.set("performance", updated)
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


def _render_coming_soon(mode_name: str, summary: str) -> None:
    st.subheader(mode_name)
    st.write(summary)
    st.info("This mode is planned next. The shared triboelectric data and reference display are already in place for it.")


def charging_by_friction_page() -> None:
    state = State("static_electricity")
    state.ensure("mode", "Explorer")

    st.write(
        "Use the triboelectric reference to predict how materials charge when rubbed together. "
        "This first version includes the shared reference display and a material sandbox."
    )

    mode = st.radio(
        "Mode",
        options=("Explorer", "Comparison Practice", "Ranking Logic Puzzle"),
        horizontal=True,
        key=state.key("mode_select"),
    )
    state.set("mode", mode)

    if mode == "Ranking Logic Puzzle":
        clue_col, ranking_col = st.columns((3, 2), gap="large")
        with clue_col:
            _render_logic_puzzle_clues()
        with ranking_col:
            _render_logic_puzzle_ranking()
    else:
        content_col, guide_col = st.columns((3, 2), gap="large")

        with guide_col:
            _render_reference_series()
            _render_symbol_legend()

        with content_col:
            if mode == "Explorer":
                _render_explorer()
            else:
                _render_comparison_practice()
