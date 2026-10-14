"""Optional axis organizer; checking never submits the final answer."""
import math
import streamlit as st


def render_projectile_workspace(state, plan, question_id):
    entries, locations = {}, {}
    with st.expander("Organizing help", expanded=False):
        with st.form(state.key(f"projectile_setup_form_{question_id}"), enter_to_submit=True, border=False):
            st.subheader("1. Given information", help="Use g = 10 m/s² and ignore air resistance. Angles are measured from horizontal. Speed is a magnitude; vertical velocity and displacement have signs. For calculated vertical quantities here, up is positive.")
            vector = [f for f in plan["fields"] if f["id"] in ("vi", "vf", "ai", "af", "tfirst")]
            axes = [f for f in plan["fields"] if f not in vector]

            def draw(field, column):
                with column:
                    key = field["id"]
                    entries[key] = st.text_input(field["label"], help=field["help"], key=state.key(f"projectile_setup_input_{question_id}_{key}"))
                    locations[key] = column

            if vector:
                columns = st.columns(2)
                for index, field in enumerate(vector):
                    draw(field, columns[index % 2])
            if axes:
                columns = st.columns(2)
                for column, heading in zip(columns, ("Horizontal", "Vertical")):
                    column.markdown(f"**{heading}**")
                for field in axes:
                    draw(field, columns[1 if field["id"] in ("h", "hmax", "dy", "vyi", "vyf") else 0])
            st.subheader("2. Possible in-between calculations", help="These values are not found in the question. You can calculate them using the information above. A value can be shared by both axes; use the same time interval for both.")
            columns = st.columns(2)
            for column, heading in zip(columns, ("Horizontal", "Vertical")):
                column.markdown(f"**{heading}**")
            for field in plan["steps"]:
                if field["id"] not in ("t", "tpeak", "vyi", "vyf"):
                    draw(field, columns[0 if field["id"] == "vx" else 1])
            velocities = [f for f in plan["steps"] if f["id"] in ("vyi", "vyf")]
            if velocities:
                with columns[1]:
                    velocity_columns = st.columns(len(velocities))
                    for field, column in zip(velocities, velocity_columns):
                        draw(field, column)
            time_fields = [f for f in plan["steps"] if f["id"] in ("t", "tpeak")]
            if time_fields:
                st.markdown("**Time**")
                columns = st.columns(2)
                for index, field in enumerate(time_fields):
                    draw(field, columns[index])
            checked = st.form_submit_button("Check organized work")
        if checked:
            state.set("setup_submission", dict(entries))
        snapshot = state.get("setup_submission")
        if snapshot is not None:
            for field in plan["fields"] + plan["steps"]:
                key = field["id"]
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
                        st.error("Check the value in the question." if key in plan["givens"] else "Check your calculation.")
