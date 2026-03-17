import time

import streamlit as st

from utils.ui_components import (
    build_performance_table,
    init_performance,
    performance_expander,
    record_performance,
)
from utils.ui_state import State
from utils.generators.static_electricity import (
    FINAL_SIGN_OPTIONS,
    MECHANISM_OPTIONS,
    build_conduction_case,
    charge_count_label,
    charge_token_row,
    sign_label,
    sign_symbol,
)


def _render_conduction_box(box_name: str, state_data: dict) -> None:
    sign = state_data["sign"]
    chunks = state_data["chunks"]
    note = state_data["note"]
    sign_text = sign_label(sign)
    count_text = charge_count_label(sign, chunks)
    tokens = charge_token_row(sign, chunks)
    st.markdown(
        f"""
<div style="border:1px solid #b8bec8;border-radius:12px;padding:0.9rem 0.8rem;text-align:center;">
  <div style="font-weight:700;margin-bottom:0.35rem;">Box {box_name}</div>
  <div style="font-size:1.35rem;margin-bottom:0.2rem;"><code>{sign_symbol(sign)}</code> {sign_text}</div>
  <div style="margin-bottom:0.2rem;">Net charge: <code>{count_text}</code></div>
  <div style="font-size:0.95rem;margin-bottom:0.35rem;"><code>{tokens}</code></div>
  <div style="font-size:0.9rem;color:#5b6470;">{note}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_conduction_diagram(title: str, states: dict[str, dict]) -> None:
    st.markdown(f"#### {title}")
    left_col, right_col = st.columns(2)
    with left_col:
        _render_conduction_box("A", states["A"])
    with right_col:
        _render_conduction_box("B", states["B"])


def _reset_conduction_question(state: State, difficulty: str) -> None:
    state.set("case", build_conduction_case(difficulty))
    state.inc("question_number")
    state.set("submitted", False)
    state.set("last_result", None)


def _render_conduction_performance(state: State) -> None:
    performance = state.get("performance")
    df = build_performance_table(performance, ["Easy", "Medium", "Hard"])
    performance_expander(df)


def charging_by_conduction_page() -> None:
    state = State("conduction_practice")
    state.ensure("difficulty", "Medium")
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(["Charging by Conduction"], ["Easy", "Medium", "Hard"]),
    )

    st.write(
        "Predict what happens when one charged conductor touches an identical neutral conductor. "
        "Use the before-contact diagram to determine the final charges and what physically moved."
    )

    difficulty = st.radio(
        "Difficulty",
        options=("Easy", "Medium", "Hard"),
        index=("Easy", "Medium", "Hard").index(state.get("difficulty", "Medium")),
        horizontal=True,
        key=state.key("difficulty_select"),
    )
    previous_difficulty = state.get("difficulty")
    state.set("difficulty", difficulty)

    if not state.has("case"):
        _reset_conduction_question(state, difficulty)
        st.rerun()
    elif previous_difficulty != difficulty:
        _reset_conduction_question(state, difficulty)
        st.rerun()

    case = state.get("case")
    question_number = state.get("question_number", 0)

    st.subheader("Charging by Conduction")
    st.caption(f"Difficulty: {difficulty}")
    _render_conduction_diagram("Before Contact", case["before_states"])

    st.markdown("#### Predict the Outcome")
    if difficulty == "Easy":
        st.caption("Predict only the final sign of each box.")
        sign_col_a, sign_col_b = st.columns(2, gap="large")
        with sign_col_a:
            final_a = st.radio(
                "Final charge of Box A",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_a_{question_number}"),
            )
        with sign_col_b:
            final_b = st.radio(
                "Final charge of Box B",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_b_{question_number}"),
            )
        mechanism = None
        amount_a = None
        amount_b = None
    elif difficulty == "Medium":
        st.caption("Predict the final signs and identify what moved.")
        sign_col_a, sign_col_b, mech_col = st.columns((1, 1, 1.2), gap="large")
        with sign_col_a:
            final_a = st.radio(
                "Final charge of Box A",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_a_{question_number}"),
            )
        with sign_col_b:
            final_b = st.radio(
                "Final charge of Box B",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_b_{question_number}"),
            )
        with mech_col:
            mechanism = st.radio(
                "What moved during contact?",
                options=MECHANISM_OPTIONS,
                key=state.key(f"mechanism_{question_number}"),
            )
        amount_a = None
        amount_b = None
    else:
        st.caption("Predict the final signs, identify what moved, and give the final charge amount in each box.")
        sign_col_a, sign_col_b, mech_col = st.columns((1, 1, 1.2), gap="large")
        with sign_col_a:
            final_a = st.radio(
                "Final charge of Box A",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_a_{question_number}"),
            )
        with sign_col_b:
            final_b = st.radio(
                "Final charge of Box B",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"final_b_{question_number}"),
            )
        with mech_col:
            mechanism = st.radio(
                "What moved during contact?",
                options=MECHANISM_OPTIONS,
                key=state.key(f"mechanism_{question_number}"),
            )
        amount_options = tuple(range(0, case["initial_chunks"] + 1))
        amount_col_a, amount_col_b = st.columns(2, gap="large")
        with amount_col_a:
            amount_a = st.selectbox(
                "Final charge amount in Box A",
                options=amount_options,
                key=state.key(f"amount_a_{question_number}"),
            )
        with amount_col_b:
            amount_b = st.selectbox(
                "Final charge amount in Box B",
                options=amount_options,
                key=state.key(f"amount_b_{question_number}"),
            )

    score_col, action_col, check_col = st.columns((2, 1, 1))
    with score_col:
        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        if attempts == 0:
            st.caption("Score: 0/0")
        else:
            st.caption(f"Score: {correct}/{attempts}")
    with action_col:
        if st.button("New Scenario", key=state.key("new_scenario")):
            _reset_conduction_question(state, difficulty)
            st.rerun()
    with check_col:
        check_clicked = st.button("Check Answer", key=state.key("check_answer"))

    if check_clicked:
        expected_sign = sign_label(case["final_sign"])
        is_correct = final_a == expected_sign and final_b == expected_sign
        if difficulty in ("Medium", "Hard"):
            is_correct = is_correct and mechanism == case["mechanism_answer"]
        if difficulty == "Hard":
            is_correct = (
                is_correct
                and amount_a == case["final_chunks"]
                and amount_b == case["final_chunks"]
            )

        state.inc("attempt_count")
        if is_correct:
            state.inc("correct_count")
        performance = state.get("performance")
        updated = record_performance(
            performance, "Charging by Conduction", difficulty, is_correct
        )
        state.set("performance", updated)
        state.set("submitted", True)
        state.set(
            "last_result",
            {
                "is_correct": is_correct,
                "expected_sign": expected_sign,
                "expected_mechanism": case["mechanism_answer"],
                "expected_amount": case["final_chunks"],
            },
        )

    result = state.get("last_result")
    if state.get("submitted") and result:
        if result["is_correct"]:
            st.success("Correct.")
        else:
            st.error("Not quite.")

        _render_conduction_diagram("After Contact", case["after_states"])
        st.info(case["explanation"])
        if difficulty == "Easy":
            st.caption(
                f"Correct response: Box A = {result['expected_sign']}, Box B = {result['expected_sign']}."
            )
        elif difficulty == "Medium":
            st.caption(
                f"Correct response: Box A = {result['expected_sign']}, Box B = {result['expected_sign']}, "
                f"mechanism = {result['expected_mechanism']}."
            )
        else:
            st.caption(
                f"Correct response: Box A = {result['expected_sign']} with {result['expected_amount']}, "
                f"Box B = {result['expected_sign']} with {result['expected_amount']}, "
                f"mechanism = {result['expected_mechanism']}."
            )

        if result["is_correct"]:
            st.caption("Loading the next conduction scenario...")
            time.sleep(0.8)
            _reset_conduction_question(state, difficulty)
            st.rerun()

    _render_conduction_performance(state)
