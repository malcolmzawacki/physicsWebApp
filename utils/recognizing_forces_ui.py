"""Streamlit workspace for C4: explicit checks, revisions, and session-local records."""
import random

import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.session_progress import record_answer
from utils.recognizing_forces import (
    FORCE_LABELS, PRACTICE_SETS, SCENARIO_BY_ID, available_scenarios,
    new_attempt, submit_attempt,
)
from utils.ui_state import State
from utils.ui_components import render_header


def render_recognizing_forces():
    state = State("recognizing_forces")
    state.ensure("records", [])
    state.ensure("question_id", 0)

    def start(scenario_id):
        previous = state.get("attempt")
        if previous is not None:
            state.set("records", [*state.get("records"), previous])
        state.inc("question_id")
        state.set("attempt", new_attempt(scenario_id))

    def fresh(context):
        remaining = [s.id for s in available_scenarios(context)
                     if s.id not in state.get("seen", [])]
        if not remaining:
            remaining = [s.id for s in available_scenarios(context)
                         if s.id != state.get("attempt", {}).get("scenario_id")]
            state.set("seen", [])
        scenario_id = random.choice(remaining)
        state.set("seen", [*state.get("seen", []), scenario_id])
        start(scenario_id)

    header_records = [*state.get("records"), state.get("attempt", {})]
    stars = sum(bool(record.get("completed")) for record in header_records)
    render_header("Recognizing Forces", stars)
    st.write("Identify the forces acting on one object. You can revise after checking.")
    context = st.selectbox("Practice contexts", PRACTICE_SETS, key=state.key("context"))
    if state.get("active_context") != context or not state.has("attempt"):
        state.set("active_context", context)
        state.set("seen", [])
        fresh(context)

    attempt = state.get("attempt")
    scenario = SCENARIO_BY_ID[attempt["scenario_id"]]
    question_id = state.get("question_id")
    # Clean up before rendering widgets, never after their form was instantiated.
    for key in list(st.session_state):
        if key.startswith(state.key("answer_")) and not key.startswith(state.key(f"answer_{question_id}_")):
            del st.session_state[key]
    st.markdown(f"**{scenario.title}**")
    st.write(scenario.situation)
    st.info(f"Consider only forces acting on **{scenario.target}**.")

    with st.expander("Force labels and conventions"):
        st.write("Use one label per interaction. A rope gives tension; a spring gives spring force; a surface gives normal force and possibly friction. Applied force means a direct push or pull, not another name for these forces.")
        st.write("Select forces on the named object, not forces it exerts on other objects. Motion and net force are not additional force types.")
    if attempt["hint_used"]:
        st.caption(scenario.hint)

    with st.form(state.key(f"form_{question_id}")):
        st.write("Select every force present. Leave all boxes empty if no forces act in this model.")
        columns = st.columns(2)
        selected = []
        for index, (force, label) in enumerate(FORCE_LABELS.items()):
            with columns[index % 2]:
                state.ensure(f"answer_{question_id}_{force}", force in attempt["selection"])
                if st.checkbox(label, key=state.key(f"answer_{question_id}_{force}"),
                               disabled=attempt["completed"]):
                    selected.append(force)
        check_col, hint_col = st.columns(2)
        with check_col:
            checked = st.form_submit_button(
                "Check forces", type="primary", use_container_width=True,
                disabled=attempt["completed"])
        with hint_col:
            hint_requested = st.form_submit_button(
                "Show interaction hint", use_container_width=True,
                disabled=attempt["completed"])
    if hint_requested:
        attempt["hint_used"] = True
        attempt["selection"] = tuple(selected)
        state.set("attempt", attempt)
        st.rerun()
    if checked:
        previous_checks = len(attempt["checks"])
        submit_attempt(attempt, selected)
        if len(attempt["checks"]) > previous_checks:
            record_answer("Recognizing Forces", scenario.situation + " Forces on: " + scenario.target,
                          [FORCE_LABELS[force] for force in selected] or "No forces",
                          [FORCE_LABELS[force] for force in scenario.forces] or "No forces",
                          attempt["last_result"]["correct"], explanation=" ".join(text for _, text in scenario.interactions))
        state.set("attempt", attempt)
        st.rerun()

    result = attempt["last_result"]
    if result:
        st.caption("Feedback describes your last check. After changing boxes, check again.")
        if result["correct"]:
            st.success("Correct — you identified every force. ⭐")
            for _, explanation in scenario.interactions:
                st.write(explanation)
            if not scenario.forces:
                st.write("No modeled interactions exert a force on the coasting probe.")
        else:
            st.warning("Revise your selection and check again.")
            for message in result["feedback"]:
                st.write(message)

    left, right = st.columns(2)
    with left:
        def next_question():
            if state.get("question_id") == question_id:
                fresh(context)
        st.button("Next question" if attempt["completed"] else "Skip question",
                  key=state.key(f"next_{question_id}"), use_container_width=True,
                  on_click=next_question)
    with right:
        def related():
            if state.get("question_id") == question_id:
                start(scenario.related)
                state.set("seen", [*state.get("seen", []), scenario.related])
        st.button("Try a related case", key=state.key(f"related_{question_id}"),
                  use_container_width=True, on_click=related)

    records = [*state.get("records"), attempt]
    completed = [r for r in records if r["completed"]]
    st.caption(f"{len(completed)} completed · {sum(r['outcome'] == 'First try' for r in completed)} first try without help")
    with st.expander("Your Performance"):
        st.caption("This session only. Repeated practice counts as another case; completion is not a mastery measure. One star per completed case. Skipped cases remain visible.")
        st.dataframe([
            {"Context": SCENARIO_BY_ID[r["scenario_id"]].context,
             "Case": SCENARIO_BY_ID[r["scenario_id"]].title,
             "Checks": len(r["checks"]), "Hint used": r["hint_used"],
             "Result": r["outcome"] or ("In progress" if r is attempt else "Skipped")}
            for r in records
        ], hide_index=True, use_container_width=True)
        def reset():
            state.set("records", [])
            state.pop("attempt")
            state.pop("active_context")
            state.set("seen", [])
        st.button("Reset practice", key=state.key("reset"), on_click=reset)

    if attempt["completed"]:
        def advance():
            if state.get("question_id") == question_id:
                fresh(context)
                st.rerun()
        next_question_countdown(state, question_id, advance, seconds=5)
