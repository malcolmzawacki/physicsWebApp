"""First classroom prototype of a scaffold for friction calculations."""
import math
import streamlit as st


def render_force_plan(state, plan, question_id):
    with st.expander("Organizing help", expanded=False):
        entries = {}
        expected = {}
        with st.form(state.key(f"force_plan_form_{question_id}"), enter_to_submit=True, border=False):
            st.subheader("1. Given information", help="Values supplied in the question. Use the stated gravitational acceleration, g = 10 m/s².")
            columns = st.columns(len(plan["given"]))
            for index, (label, value) in enumerate(plan["given"].items()):
                key = f"given_{index}"
                entries[key] = columns[index].text_input(label, key=state.key(f"force_plan_{question_id}_{key}"))
                expected[key] = (label, value)
            st.subheader("2. Possible in-between calculations", help="These values are not found in the question. You can calculate them using the information above.")
            columns = st.columns(len(plan["steps"]))
            for index, step in enumerate(plan["steps"]):
                key = f"step_{index}"
                entries[key] = columns[index].text_input(step["label"], help=step["hint"], key=state.key(f"force_plan_{question_id}_{key}"))
                expected[key] = (step["label"], step["answer"])
            checked = st.form_submit_button("Check organized work")
        if checked:
            state.set("setup_submission", dict(entries))
        snapshot = state.get("setup_submission")
        if snapshot:
            for key, (label, value) in expected.items():
                if entries[key] != snapshot.get(key):
                    st.caption(f"{label}: changed — check again")
                    continue
                try:
                    actual = float(snapshot[key])
                except (ValueError, TypeError):
                    st.caption(f"{label}: enter a number when ready.")
                    continue
                if math.isfinite(actual) and math.isclose(actual, value, rel_tol=0.01, abs_tol=0.01):
                    st.success(f"{label}: correct")
                elif key.startswith("given"):
                    st.error(f"{label}: check the value supplied in the question.")
                else:
                    st.error(f"{label}: check your calculation using the relationship above.")
