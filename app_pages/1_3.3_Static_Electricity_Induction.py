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
    INDUCTION_MODEL_NOTES,
    build_induction_case,
    charge_count_label,
    sign_label,
    sign_symbol,
)

AUTO_ADVANCE_DELAY_SECONDS = 2.2


def _render_induction_box(label: str, sign: str, chunks: int, note: str) -> None:
    charge_text = charge_count_label(sign, chunks)
    st.markdown(
        f"""
<div style="border:1px solid #b8bec8;border-radius:12px;padding:0.85rem 0.75rem;text-align:center;">
  <div style="font-weight:700;margin-bottom:0.35rem;">{label}</div>
  <div style="font-size:1.35rem;margin-bottom:0.15rem;"><code>{sign_symbol(sign)}</code> {sign_label(sign)}</div>
  <div style="margin-bottom:0.25rem;">Net charge: <code>{charge_text}</code></div>
  <div style="font-size:0.9rem;color:#5b6470;">{note}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _render_grounding_diagram(title: str, case: dict, stage_key: str) -> None:
    stage = case[stage_key]
    st.markdown(f"#### {title}")
    st.caption(case["diagram_note_before"] if stage_key == "before_states" else case["diagram_note_after"])
    rod_col, conductor_col = st.columns((1, 1.2), gap="large")
    with rod_col:
        rod = stage["rod"]
        _render_induction_box(rod["label"], rod["sign"], rod["chunks"], rod["note"])
        st.caption("No contact")
    with conductor_col:
        conductor = stage["B"]
        _render_induction_box(conductor["label"], conductor["sign"], conductor["chunks"], conductor["note"])
        if stage_key == "before_states":
            st.caption("Ground connection active")


def _render_separation_diagram(title: str, case: dict, stage_key: str) -> None:
    stage = case[stage_key]
    st.markdown(f"#### {title}")
    st.caption(case["diagram_note_before"] if stage_key == "before_states" else case["diagram_note_after"])
    rod_col, a_col, b_col = st.columns((1, 1, 1), gap="large")
    with rod_col:
        rod = stage["rod"]
        _render_induction_box(rod["label"], rod["sign"], rod["chunks"], rod["note"])
        st.caption("No contact")
    with a_col:
        conductor_a = stage["A"]
        _render_induction_box(conductor_a["label"], conductor_a["sign"], conductor_a["chunks"], conductor_a["note"])
    with b_col:
        conductor_b = stage["B"]
        _render_induction_box(conductor_b["label"], conductor_b["sign"], conductor_b["chunks"], conductor_b["note"])
    if stage_key == "before_states":
        st.caption("A and B are touching before separation.")


def _render_induction_diagram(title: str, case: dict, stage_key: str) -> None:
    if case["method"] == "grounding":
        _render_grounding_diagram(title, case, stage_key)
    else:
        _render_separation_diagram(title, case, stage_key)


def _reset_induction_question(state: State, difficulty: str) -> None:
    state.set("case", build_induction_case(difficulty))
    state.inc("question_number")
    state.set("submitted", False)
    state.set("last_result", None)


def _render_induction_performance(state: State) -> None:
    performance = state.get("performance")
    df = build_performance_table(performance, ["Easy", "Medium", "Hard"])
    performance_expander(df)


def charging_by_induction_page() -> None:
    state = State("induction_practice")
    state.ensure("difficulty", "Medium")
    state.ensure("correct_count", 0)
    state.ensure("attempt_count", 0)
    state.ensure("question_number", 0)
    state.ensure("submitted", False)
    state.ensure("last_result", None)
    state.ensure_lazy(
        "performance",
        lambda: init_performance(["Charging by Induction"], ["Easy", "Medium", "Hard"]),
    )

    st.write(
        "Predict what happens when a charged object is brought nearby without touching. "
        "This page mixes induction with grounding and induction by polarization plus separation."
    )
    st.caption(INDUCTION_MODEL_NOTES["rule"])

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
        _reset_induction_question(state, difficulty)
        st.rerun()
    elif previous_difficulty != difficulty:
        _reset_induction_question(state, difficulty)
        st.rerun()

    case = state.get("case")
    question_number = state.get("question_number", 0)
    result = state.get("last_result")

    st.subheader("Charging by Induction")
    st.caption(case["title"])
    st.caption(f"Difficulty: {difficulty}")
    _render_induction_diagram("Before the Final Step", case, "before_states")
    if state.get("submitted") and result and result["is_correct"]:
        _render_induction_diagram("After the Process", case, "after_states")
        st.info(case["explanation"])

        if difficulty == "Easy":
            answer_text = ", ".join(
                f"{obj} = {result['expected_signs'][obj]}" for obj in case["asked_objects"]
            )
        elif difficulty == "Medium":
            answer_text = ", ".join(
                f"{obj} = {result['expected_signs'][obj]}" for obj in case["asked_objects"]
            )
            answer_text = f"{answer_text}, mechanism = {result['expected_mechanism']}"
        else:
            object_parts = []
            for obj in case["asked_objects"]:
                object_parts.append(
                    f"{obj} = {result['expected_signs'][obj]} with {result['expected_amounts'][obj]}"
                )
            answer_text = ", ".join(object_parts)
            answer_text = f"{answer_text}, mechanism = {result['expected_mechanism']}"
        st.caption(f"Correct response: {answer_text}.")

    st.markdown("#### Predict the Outcome")
    if difficulty == "Easy":
        st.caption("Predict only the final sign of the induced conductor(s).")
    elif difficulty == "Medium":
        st.caption("Predict the final sign(s) and identify what moved.")
    else:
        st.caption("Predict the final sign(s), identify what moved, and give the final charge amount(s).")

    sign_columns = st.columns(len(case["asked_objects"]), gap="large")
    sign_answers: dict[str, str] = {}
    for index, obj in enumerate(case["asked_objects"]):
        with sign_columns[index]:
            sign_answers[obj] = st.radio(
                f"Final charge of {obj}",
                options=FINAL_SIGN_OPTIONS,
                horizontal=True,
                key=state.key(f"sign_{obj}_{question_number}"),
            )

    mechanism = None
    if difficulty in ("Medium", "Hard"):
        mechanism = st.radio(
            "What moved during this process?",
            options=case["mechanism_options"],
            key=state.key(f"mechanism_{question_number}"),
        )

    amount_answers: dict[str, int] = {}
    if difficulty == "Hard":
        amount_columns = st.columns(len(case["asked_objects"]), gap="large")
        amount_options = tuple(range(0, case["transfer_chunks"] * 2 + 1))
        for index, obj in enumerate(case["asked_objects"]):
            with amount_columns[index]:
                amount_answers[obj] = st.selectbox(
                    f"Final charge amount on {obj}",
                    options=amount_options,
                    key=state.key(f"amount_{obj}_{question_number}"),
                )

    score_col, action_col, spacer_col, check_col = st.columns((2, 1, 3, 1.2))
    with score_col:
        attempts = state.get("attempt_count", 0)
        correct = state.get("correct_count", 0)
        if attempts == 0:
            st.caption("Score: 0/0")
        else:
            st.caption(f"Score: {correct}/{attempts}")
    with action_col:
        if st.button("New Scenario", key=state.key("new_scenario"), type="secondary", use_container_width=True):
            _reset_induction_question(state, difficulty)
            st.rerun()
    with check_col:
        check_clicked = st.button(
            "Check Answer",
            key=state.key("check_answer"),
            type="primary",
            use_container_width=True,
        )

    if check_clicked:
        is_correct = True
        for obj in case["asked_objects"]:
            is_correct = is_correct and sign_answers[obj] == case["expected_signs"][obj]
        if difficulty in ("Medium", "Hard"):
            is_correct = is_correct and mechanism == case["mechanism_answer"]
        if difficulty == "Hard":
            for obj in case["asked_objects"]:
                is_correct = is_correct and amount_answers[obj] == case["expected_amounts"][obj]

        state.inc("attempt_count")
        if is_correct:
            state.inc("correct_count")
        performance = state.get("performance")
        updated = record_performance(
            performance, "Charging by Induction", difficulty, is_correct
        )
        state.set("performance", updated)
        state.set("submitted", True)
        state.set(
            "last_result",
            {
                "is_correct": is_correct,
                "expected_signs": case["expected_signs"],
                "expected_mechanism": case["mechanism_answer"],
                "expected_amounts": case["expected_amounts"],
            },
        )
        st.rerun()

    if state.get("submitted") and result:
        if result["is_correct"]:
            st.success("Correct.")
        else:
            st.error("Not quite.")

        if result["is_correct"]:
            st.caption("Loading the next induction scenario...")
            time.sleep(AUTO_ADVANCE_DELAY_SECONDS)
            _reset_induction_question(state, difficulty)
            st.rerun()

    _render_induction_performance(state)
