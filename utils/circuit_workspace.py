"""Component-aware organizer for the reviewed two-resistor activities."""
import math

import streamlit as st
from utils.circuit_organizer import plan_from_case


def render_circuit_workspace(state, case):
    plan = case.get("organizer") or plan_from_case(case)
    # A live session may retain a case generated before organizers were added.
    # Recover from its displayed givens without replacing the student's question.
    if not plan:
        return
    question_id = state.get("question_number", 0)
    if state.get("circuit_setup_question") != question_id:
        state.set("circuit_setup_question", question_id)
        state.set("circuit_setup_submission", None)
    with st.expander("Organizing help", expanded=False):
        entries, expected, locations = {}, {}, {}
        with st.form(state.key(f"circuit_setup_form_{question_id}"), enter_to_submit=True, border=False):
            st.subheader("1. Given information", help="Values supplied by the circuit diagram.")
            columns = st.columns(len(plan["groups"]))
            for column, group in zip(columns, plan["groups"]):
                with column:
                    st.markdown(f"**{group['label']}**")
                    for field in group["fields"]:
                        key = field["id"]
                        entries[key] = st.text_input(field["label"], help=field.get("help"), key=state.key(f"circuit_setup_input_{question_id}_{key}"))
                        expected[key] = field
                        locations[key] = column
            if plan["steps"]:
                st.subheader("2. Possible in-between calculations", help="These values are not found in the question. You can calculate them using the information above.")
                columns = st.columns(len(plan["steps"]))
                for column, field in zip(columns, plan["steps"]):
                    key = field["id"]
                    entries[key] = column.text_input(field["label"], help=field["help"], key=state.key(f"circuit_setup_input_{question_id}_{key}"))
                    expected[key] = field
                    locations[key] = column
            checked = st.form_submit_button("Check organized work")
        if checked:
            state.set("circuit_setup_submission", dict(entries))
        snapshot = state.get("circuit_setup_submission")
        if snapshot is not None:
            for key, field in expected.items():
                with locations[key]:
                    if entries[key] != snapshot.get(key):
                        st.caption("Changed — check again")
                        continue
                    try:
                        value = float(snapshot[key])
                    except (ValueError, TypeError):
                        st.caption("Enter a number when ready.")
                        continue
                    if math.isfinite(value) and math.isclose(value, field["value"], rel_tol=0.01, abs_tol=0.01):
                        st.success("Correct")
                    else:
                        st.error("Check the diagram." if key in ("shared", "R1", "R2") else "Check your calculation.")


