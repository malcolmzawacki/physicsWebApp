"""Stage-aware conservation organizer, independent of final submission."""
import math
import streamlit as st


def render_energy_workspace(state, plan, question_id):
    with st.expander("Organizing help", expanded=False):
        entries, fields, locations = {}, {}, {}
        with st.form(state.key(f"energy_setup_form_{question_id}"), enter_to_submit=True, border=False):
            st.subheader("1. Given information", help=plan.get("given_help", "Use g = 10 m/s². Assume ideal springs and no energy loss. Vertical change is measured between the starting and ending positions, including any spring compression or expansion."))
            columns = st.columns(len(plan["groups"]))
            for column, group in zip(columns, plan["groups"]):
                with column:
                    st.markdown(f"**{group['label']}**")
                    for field in group["fields"]:
                        key = field["id"]
                        entries[key] = st.text_input(field["label"], key=state.key(f"energy_setup_input_{question_id}_{key}"))
                        fields[key], locations[key] = field, column
            if plan["steps"]:
                st.subheader("2. Possible in-between calculations", help="These values are not found in the question. You can calculate them using the information above.")
                step_columns = st.columns(len(plan["steps"]))
                for column, field in zip(step_columns, plan["steps"]):
                    key = field["id"]
                    entries[key] = column.text_input(field["label"], help=field["help"], key=state.key(f"energy_setup_input_{question_id}_{key}"))
                    fields[key], locations[key] = field, column
            checked = st.form_submit_button("Check organized work")
        if checked:
            state.set("setup_submission", dict(entries))
        snapshot = state.get("setup_submission")
        if snapshot is not None:
            for key, field in fields.items():
                with locations[key]:
                    if entries[key] != snapshot.get(key):
                        st.caption(f"{field['label']}: changed — check again")
                        continue
                    try:
                        value = float(snapshot[key])
                    except (ValueError, TypeError):
                        st.caption("Enter a number when ready.")
                        continue
                    if math.isfinite(value) and math.isclose(value, field["value"], rel_tol=.01, abs_tol=.01):
                        st.success("Correct")
                    else:
                        st.error("Check the value in the question." if key in plan.get("givens", {}) else "Check your calculation.")
